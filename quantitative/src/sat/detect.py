"""Two independent ways of finding a buried channel, neither thresholded.

Spectral: a channel holds moisture, so it recurs across dates as a coherent
linear anomaly while noise does not. Principal components over a multi-season
band stack pull that recurrence out.

Topographic: a channel is a shallow trough. Subtracting a smoothed surface
removes the regional slope, which is a hundred times larger than the signal,
and curvature then reads the trough.

Both return a continuous score per pixel. Thresholding happens, if at all, after
validation against a control.
"""

import numpy as np
import rasterio
import pystac_client
from pyproj import Transformer
from rasterio.windows import from_bounds
from rasterio.enums import Resampling
from scipy import ndimage
from sklearn.decomposition import PCA

CATALOG = "https://earth-search.aws.element84.com/v1"


# ----------------------------------------------------------------- spectral

def indices(med):
    """Moisture and vegetation ratios, which carry the signal more directly
    than raw reflectance and are insensitive to overall brightness."""
    if not {"nir", "red", "green", "swir16", "swir22"} <= set(med):
        return {}          # a non-optical stack, e.g. radar only
    e = 1e-6
    out = {}
    out["ndvi"] = (med["nir"] - med["red"]) / (med["nir"] + med["red"] + e)
    out["ndwi"] = (med["green"] - med["nir"]) / (med["green"] + med["nir"] + e)
    # NDMI: the standard soil and canopy moisture ratio
    out["ndmi"] = (med["nir"] - med["swir16"]) / (med["nir"] + med["swir16"] + e)
    # clay / hydroxyl ratio, which separates channel fill from surrounding soil
    out["clay"] = med["swir16"] / (med["swir22"] + e)
    return out


def spectral_score(composites, extra=None, n_components=8):
    """PCA over every band and index of every season, plus any extra layers.

    Which component carries the channel is not known in advance and is not
    always the same one, so picking PC2 or summing PC2 to PC4 is arbitrary. Here
    the component is chosen by how linear its spatial structure is, measured on
    the component itself. That rule never looks at the control, so it cannot
    launder the control's answer back into the score.
    """
    feats, names = [], []
    for season, med in sorted(composites.items()):
        for b, a in sorted(med.items()):
            feats.append(a); names.append(f"{season}:{b}")
        for k, a in sorted(indices(med).items()):
            feats.append(a); names.append(f"{season}:{k}")
    for k, a in sorted((extra or {}).items()):
        feats.append(a); names.append(k)

    shape = feats[0].shape
    X = np.column_stack([f.ravel() for f in feats])
    good = np.isfinite(X).all(axis=1)
    if good.sum() < 100:
        raise RuntimeError("almost no pixels valid across every layer")

    Xg = X[good]
    Xg = (Xg - Xg.mean(0)) / (Xg.std(0) + 1e-9)
    p = PCA(n_components=min(n_components, Xg.shape[1]))
    Yg = p.fit_transform(Xg)

    comps = []
    for i in range(Yg.shape[1]):
        img = np.full(X.shape[0], np.nan, dtype="float32")
        img[good] = Yg[:, i]
        comps.append(img.reshape(shape))

    # PC1 is reliably overall brightness and carries no channel information, so
    # it is dropped. The primary score is the summed magnitude of the next
    # three, which is the rule fixed before any control was run and which
    # scored 0.814 in the Indus delta.
    score = np.nansum([np.abs(c) for c in comps[1:4]], axis=0)
    score[~np.isfinite(comps[0])] = np.nan

    # A second, differently motivated score, reported alongside rather than
    # instead: among the components after the first, the one whose structure is
    # most one-directional. Choosing by linearity over all components picked
    # PC1 and did worse, because open water is linear too.
    lin = [float(np.nanmean(np.abs(linearity(c)))) for c in comps[1:]]
    pick = int(np.argmax(lin)) + 1
    alt = np.abs(comps[pick])
    alt[~np.isfinite(comps[0])] = np.nan
    return score, comps, p.explained_variance_ratio_, names, pick, alt


# -------------------------------------------------------------- topographic

def copernicus_dem(bbox, like_profile=None, shape=None):
    """Copernicus 30 m DEM over the box, from the same STAC catalogue."""
    cat = pystac_client.Client.open(CATALOG)
    items = list(cat.search(collections=["cop-dem-glo-30"], bbox=bbox).items())
    if not items:
        raise RuntimeError(f"no Copernicus DEM tile for {bbox}")

    # The Copernicus DEM sits in a public S3 bucket, so GDAL has to be told to
    # make unsigned requests rather than looking for credentials it will not find.
    env = rasterio.Env(AWS_NO_SIGN_REQUEST="YES",
                       GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR")

    tiles = []
    for it in items:
        key = "data" if "data" in it.assets else list(it.assets)[0]
        with env, rasterio.open(it.assets[key].href) as src:
            t = Transformer.from_crs("EPSG:4326", src.crs, always_xy=True)
            x0, y0 = t.transform(bbox[0], bbox[1])
            x1, y1 = t.transform(bbox[2], bbox[3])
            w = from_bounds(min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1),
                            src.transform)
            if w.width < 1 or w.height < 1:
                continue
            out_shape = shape if shape else (int(round(w.height)), int(round(w.width)))
            a = src.read(1, window=w, out_shape=out_shape, boundless=True,
                         fill_value=np.nan, resampling=Resampling.bilinear)
            tiles.append(a.astype("float32"))
    if not tiles:
        raise RuntimeError(f"DEM tiles found but none overlap {bbox}")
    return np.nanmean(np.dstack(tiles), axis=2) if len(tiles) > 1 else tiles[0]


def topographic_score(dem, smooth_px=40):
    """Detrended depth below the local surface.

    A channel is one to two metres below ground over a width of a few hundred
    metres, sitting on a regional slope of tens of metres. Subtracting a heavily
    smoothed copy removes the slope and leaves the trough. Positive score means
    lower than its surroundings.
    """
    z = dem.astype("float32").copy()
    bad = ~np.isfinite(z)
    if bad.any():
        z[bad] = np.nanmedian(z)
    trend = ndimage.gaussian_filter(z, smooth_px)
    resid = trend - z                       # positive where ground sits low
    resid[bad] = np.nan
    return resid


def linearity(score, sigma=2):
    """How linear the local structure is, from the Hessian eigenvalues.

    A channel is a ridge in score space: strongly curved across its width,
    barely curved along its length. The ratio of the two eigenvalues separates
    that from blobs and from noise.
    """
    s = np.where(np.isfinite(score), score, 0.0)
    gxx = ndimage.gaussian_filter(s, sigma, order=[0, 2])
    gyy = ndimage.gaussian_filter(s, sigma, order=[2, 0])
    gxy = ndimage.gaussian_filter(s, sigma, order=[1, 1])
    tmp = np.sqrt((gxx - gyy) ** 2 + 4 * gxy ** 2)
    l1, l2 = 0.5 * (gxx + gyy + tmp), 0.5 * (gxx + gyy - tmp)
    big = np.maximum(np.abs(l1), np.abs(l2))
    small = np.minimum(np.abs(l1), np.abs(l2))
    out = big - small                        # large where one direction dominates
    out[~np.isfinite(score)] = np.nan
    return out
