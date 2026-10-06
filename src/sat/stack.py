"""Seasonal median composites of Sentinel-2 over an arbitrary box.

Reads windowed COGs straight from AWS Earth Search over STAC, so nothing is
downloaded whole and no credentials are needed. Cloud and shadow come out via
the scene classification layer that ships with L2A.

The composites are split by season because the thing we are looking for is a
soil-moisture effect: a buried channel holds water longer than the ground either
side of it, and the contrast is strongest when everything else has dried out.
"""

import json
import pathlib
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import rasterio
import pystac_client
from pyproj import Transformer
from rasterio.windows import from_bounds
from rasterio.enums import Resampling

CATALOG = "https://earth-search.aws.element84.com/v1"
CACHE = pathlib.Path(__file__).resolve().parents[2] / "data" / "processed" / "sat"

# Sentinel-2 asset keys on Earth Search. 10 m and 20 m bands; everything is
# resampled onto the 10 m grid of the first band read.
BANDS = ["blue", "green", "red", "rededge1", "nir", "nir08", "swir16", "swir22"]

# Scene classification values to drop: saturated, shadow, cloud medium, cloud
# high, thin cirrus, snow. Keeps vegetated, bare, water and unclassified.
SCL_DROP = {1, 3, 8, 9, 10, 11}

# Northern-hemisphere dry and wet halves. Kerala's monsoon runs June to
# September, the northwest Indian monsoon July to September, so the same split
# works for both.
SEASONS = {"dry": (11, 12, 1, 2, 3, 4, 5), "wet": (6, 7, 8, 9, 10)}


def search(bbox, start, end, max_cloud=20, collection="sentinel-2-l2a"):
    """Scenes intersecting bbox in [start, end] under max_cloud per cent."""
    cat = pystac_client.Client.open(CATALOG)
    hits = cat.search(
        collections=[collection],
        bbox=bbox,
        datetime=f"{start}/{end}",
        query={"eo:cloud_cover": {"lt": max_cloud}},
    )
    return sorted(hits.items(), key=lambda i: i.datetime)


def _window(src, bbox):
    """The pixel window of a lon/lat bbox in this scene's projection."""
    t = Transformer.from_crs("EPSG:4326", src.crs, always_xy=True)
    xs, ys = zip(*[t.transform(x, y) for x, y in
                   [(bbox[0], bbox[1]), (bbox[2], bbox[1]),
                    (bbox[2], bbox[3]), (bbox[0], bbox[3])]])
    return from_bounds(min(xs), min(ys), max(xs), max(ys), src.transform)


def read_scene(item, bbox, bands=BANDS):
    """One scene as {band: masked float array}, cloud and shadow set to nan.

    Returns None when the scene does not fully contain the box. Sentinel-2
    tiles are about 110 km across and our boxes are 20 km, so most scenes do;
    requiring containment avoids GDAL's boundless-read path, which builds a VRT
    per call and is not thread-safe.
    """
    if any(b not in item.assets for b in bands):
        return None

    # Shape and georeferencing come from the first 10 m band. Every other band
    # is resampled onto that grid so the 20 m ones line up exactly.
    with rasterio.open(item.assets[bands[0]].href) as src:
        w0 = _window(src, bbox)
        if (w0.col_off < 0 or w0.row_off < 0
                or w0.col_off + w0.width > src.width
                or w0.row_off + w0.height > src.height
                or w0.width < 8 or w0.height < 8):
            return None
        shape = (int(round(w0.height)), int(round(w0.width)))
        profile = {"crs": src.crs, "transform": src.window_transform(w0)}

    def grab(b):
        # COG reads are network-bound, so these parallelise almost linearly.
        # Each thread gets its own GDAL environment; sharing one is not safe.
        with rasterio.Env():
            with rasterio.open(item.assets[b].href) as src:
                w = _window(src, bbox)
                if (w.col_off < 0 or w.row_off < 0
                        or w.col_off + w.width > src.width
                        or w.row_off + w.height > src.height):
                    return b, None
                a = src.read(1, window=w, out_shape=shape,
                             resampling=Resampling.bilinear).astype("float32")
        a[a == 0] = np.nan            # 0 is nodata in L2A
        return b, a / 10000.0         # to surface reflectance

    with ThreadPoolExecutor(max_workers=len(bands)) as ex:
        out = dict(ex.map(grab, bands))
    if any(v is None for v in out.values()):
        return None

    with rasterio.Env():
        with rasterio.open(item.assets["scl"].href) as src:
            w = _window(src, bbox)
            if (w.col_off < 0 or w.row_off < 0
                    or w.col_off + w.width > src.width
                    or w.row_off + w.height > src.height):
                return None
            scl = src.read(1, window=w, out_shape=shape,
                           resampling=Resampling.nearest)
    bad = np.isin(scl, list(SCL_DROP))
    for b in out:
        out[b][bad] = np.nan

    if all(np.isnan(v).all() for v in out.values()):
        return None
    return out, profile


def composite(bbox, start, end, season, bands=BANDS, max_cloud=20, limit=None):
    """Per-band median over every usable scene of one season.

    The median rather than the mean because residual cloud edges the SCL misses
    are bright outliers, and a median ignores them.
    """
    months = SEASONS[season]
    items = [i for i in search(bbox, start, end, max_cloud)
             if i.datetime.month in months]
    if limit:
        items = items[:limit]

    stacks, profile, used = {b: [] for b in bands}, None, []
    with ThreadPoolExecutor(max_workers=6) as ex:
        results = list(ex.map(lambda it: (it, read_scene(it, bbox, bands)), items))
    for it, got in results:
        if got is None:
            continue
        arrays, prof = got
        if profile is None:
            profile = prof
        elif arrays[bands[0]].shape != stacks[bands[0]][0].shape:
            continue                   # different tile grid; skip
        for b in bands:
            stacks[b].append(arrays[b])
        used.append(it.id)

    if not used:
        raise RuntimeError(f"no usable {season} scenes for {bbox} in {start}..{end}")

    with np.errstate(invalid="ignore"):
        med = {b: np.nanmedian(np.dstack(stacks[b]), axis=2) for b in bands}
    return med, profile, used


def cached_composite(name, bbox, start, end, season, **kw):
    """composite(), saved to disk so later phases do not re-download."""
    CACHE.mkdir(parents=True, exist_ok=True)
    npz = CACHE / f"{name}_{season}.npz"
    meta = CACHE / f"{name}_{season}.json"
    if npz.exists() and meta.exists():
        d = np.load(npz)
        m = json.loads(meta.read_text())
        return ({k: d[k] for k in d.files},
                {"crs": rasterio.crs.CRS.from_string(m["crs"]),
                 "transform": rasterio.Affine(*m["transform"])},
                m["scenes"])

    med, profile, used = composite(bbox, start, end, season, **kw)
    np.savez_compressed(npz, **med)
    meta.write_text(json.dumps({
        "crs": profile["crs"].to_string(),
        "transform": list(profile["transform"])[:6],
        "bbox": bbox, "start": start, "end": end,
        "season": season, "scenes": used,
    }, indent=1))
    return med, profile, used
