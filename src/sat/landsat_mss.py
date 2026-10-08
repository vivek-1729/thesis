"""Pre-barrage satellite imagery, 1972 to 1976, from Landsat 1 and 2.

The Thanneermukkom barrage and the Idukki dam both date to 1976, and the JRC
water record only begins in 1984, so everything we have measured so far is the
engineered system. Landsat MSS reaches back before both. It is 79 m rather than
10 m, which is coarse for a channel and ample for the extent of a backwater.

MSS carries only green, red and two near-infrared bands. That is enough for
NDWI, which is all we want here: where the water was.
"""
import json, pathlib
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import rasterio
import pystac_client
import planetary_computer as pc
from pyproj import Transformer
from rasterio.windows import from_bounds
from rasterio.enums import Resampling

CATALOG = "https://planetarycomputer.microsoft.com/api/stac/v1"
CACHE = pathlib.Path(__file__).resolve().parents[2] / "data" / "processed" / "sat"
ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
           GDAL_HTTP_MAX_RETRY="3", GDAL_HTTP_RETRY_DELAY="2")

# MSS band names on Planetary Computer. nir08 is the 0.7-0.8 um band, which
# water absorbs almost completely, so green minus nir08 separates it cleanly.
BANDS = ["green", "red", "nir08", "nir09"]


def search(bbox, start="1972-01-01", end="1976-12-31", max_cloud=30):
    cat = pystac_client.Client.open(CATALOG, modifier=pc.sign_inplace)
    items = list(cat.search(collections=["landsat-c2-l1"], bbox=bbox,
                            datetime=f"{start}/{end}").items())
    keep = []
    for i in items:
        cc = i.properties.get("eo:cloud_cover")
        if cc is None or cc < max_cloud:
            keep.append(i)
    return sorted(keep, key=lambda i: i.datetime)


def _window(src, bbox):
    t = Transformer.from_crs("EPSG:4326", src.crs, always_xy=True)
    xs, ys = zip(*[t.transform(x, y) for x, y in
                   [(bbox[0], bbox[1]), (bbox[2], bbox[1]),
                    (bbox[2], bbox[3]), (bbox[0], bbox[3])]])
    return from_bounds(min(xs), min(ys), max(xs), max(ys), src.transform)


def read_scene(item, bbox, bands=BANDS):
    if any(b not in item.assets for b in bands):
        return None
    with rasterio.Env(**ENV), rasterio.open(item.assets[bands[0]].href) as src:
        w0 = _window(src, bbox)
        if (w0.col_off < 0 or w0.row_off < 0 or w0.width < 4 or w0.height < 4
                or w0.col_off + w0.width > src.width
                or w0.row_off + w0.height > src.height):
            return None
        shape = (int(round(w0.height)), int(round(w0.width)))
        profile = {"crs": src.crs, "transform": src.window_transform(w0)}

    def grab(b):
        with rasterio.Env(**ENV), rasterio.open(item.assets[b].href) as src:
            a = src.read(1, window=_window(src, bbox), out_shape=shape,
                         resampling=Resampling.bilinear).astype("float32")
        a[a == 0] = np.nan
        return b, a

    with ThreadPoolExecutor(max_workers=len(bands)) as ex:
        out = dict(ex.map(grab, bands))
    if all(np.isnan(v).all() for v in out.values()):
        return None
    return out, profile, shape


def otsu(x):
    """Threshold that best separates the two modes of a histogram.

    MSS level-1 data is raw digital numbers, not surface reflectance, so the
    NDWI distribution shifts between scenes with sun angle and atmosphere and a
    fixed cut is wrong. A fixed cut of 0.0 called 71 per cent of the Pamba box
    water against 30 per cent in the JRC record. Otsu finds the break in each
    scene's own histogram instead.
    """
    v = x[np.isfinite(x)]
    if v.size < 100:
        return None
    hist, edges = np.histogram(v, bins=256)
    centres = 0.5 * (edges[:-1] + edges[1:])
    w = np.cumsum(hist)
    tot = w[-1]
    if tot == 0:
        return None
    mu = np.cumsum(hist * centres)
    wb = w[:-1] / tot                       # weight below the split
    wf = 1.0 - wb
    good = (wb > 0) & (wf > 0)
    mb = np.where(good, mu[:-1] / np.maximum(w[:-1], 1e-9), 0)
    mf = np.where(good, (mu[-1] - mu[:-1]) / np.maximum(tot - w[:-1], 1e-9), 0)
    between = wb * wf * (mb - mf) ** 2
    between[~good] = -np.inf
    return float(centres[int(np.argmax(between))])


def water_extent(bbox, name, start="1972-01-01", end="1976-12-31"):
    """Fraction of usable scenes in which each pixel read as water.

    A frequency rather than a single mask, because any one MSS scene may catch
    an unusual stage of the monsoon. Values near 1 are permanent water, values
    in between are the seasonal swing.
    """
    CACHE.mkdir(parents=True, exist_ok=True)
    npz = CACHE / f"{name}_mss.npz"
    meta = CACHE / f"{name}_mss.json"
    if npz.exists() and meta.exists():
        d = np.load(npz)
        m = json.loads(meta.read_text())
        return d["frequency"], m

    items = search(bbox, start, end)
    wet, seen, used, shape, profile = None, None, [], None, None
    for it in items:
        got = read_scene(it, bbox)
        if got is None:
            continue
        arrays, prof, shp = got
        if shape is None:
            shape, profile = shp, prof
            wet = np.zeros(shape, "float32")
            seen = np.zeros(shape, "float32")
        elif shp != shape:
            continue
        g, n = arrays["green"], arrays["nir08"]
        ndwi = (g - n) / (g + n + 1e-6)
        cut = otsu(ndwi)
        # A hazy or near-uniform scene has no real bimodal split, and Otsu
        # returns an arbitrary point in it. Those scenes call large tracts of
        # land water, so reject any whose threshold falls outside the range a
        # genuine land-water split produces.
        if cut is None or not (0.0 <= cut <= 0.45):
            continue
        ok = np.isfinite(ndwi)
        wet[ok] += (ndwi[ok] > cut)
        seen[ok] += 1
        used.append({"id": it.id, "date": str(it.datetime.date()),
                     "platform": it.properties.get("platform"),
                     "ndwi_threshold": round(cut, 4)})

    if not used:
        raise RuntimeError(f"no usable MSS scenes for {name} {bbox}")

    freq = np.where(seen > 0, wet / np.maximum(seen, 1), np.nan)
    np.savez_compressed(npz, frequency=freq, seen=seen)
    m = {"bbox": bbox, "start": start, "end": end, "n_scenes": len(used),
         "crs": profile["crs"].to_string(),
         "transform": list(profile["transform"])[:6], "scenes": used}
    meta.write_text(json.dumps(m, indent=1))
    return freq, m


def composite(bbox, start="1972-01-01", end="1976-12-31"):
    """Median MSS composite over the period, for display.

    MSS has no blue band, so the conventional rendering is false colour with
    near-infrared standing in for red. Vegetation comes out red and water almost
    black, which suits a shoreline figure.
    """
    stacks, shape = {b: [] for b in BANDS}, None
    for it in search(bbox, start, end):
        got = read_scene(it, bbox)
        if got is None:
            continue
        arrays, _, shp = got
        if shape is None:
            shape = shp
        elif shp != shape:
            continue
        for b in BANDS:
            stacks[b].append(arrays[b])
    if shape is None:
        raise RuntimeError(f"no usable MSS scenes for {bbox}")
    with np.errstate(invalid="ignore"):
        return {b: np.nanmedian(np.dstack(v), axis=2) for b, v in stacks.items() if v}
