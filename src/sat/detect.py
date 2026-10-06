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
    e = 1e-6
    out = {}
    out["ndvi"] = (med["nir"] - med["red"]) / (med["nir"] + med["red"] + e)
    out["ndwi"] = (med["green"] - med["nir"]) / (med["green"] + med["nir"] + e)
    # NDMI: the standard soil and canopy moisture ratio
    out["ndmi"] = (med["nir"] - med["swir16"]) / (med["nir"] + med["swir16"] + e)
    # clay / hydroxyl ratio, which separates channel fill from surrounding soil
    out["clay"] = med["swir16"] / (med["swir22"] + e)
    return out


def spectral_score(composites, n_components=6, keep=3):
    """PCA over every band and index of every season.

    `composites` is {season: {band: array}}. Returns (score, components,
    explained_variance_ratio). The score is the component whose spatial
    structure is most linear, chosen by the caller from `components`; by default
    we return the summed absolute value of the first `keep` components after the
    first, since PC1 is almost always overall brightness.
    """
    feats, names = [], []
    for season, med in sorted(composites.items()):
        for b, a in sorted(med.items()):
            feats.append(a)
            names.append(f"{season}:{b}")
        for k, a in sorted(indices(med).items()):
            feats.append(a)
            names.append(f"{season}:{k}")

    shape = feats[0].shape
    X = np.column_stack([f.ravel() for f in feats])
    good = np.isfinite(X).all(axis=1)
    if good.sum() < 100:
        raise RuntimeError("almost no cloud-free pixels in common across seasons")

    Xg = X[good]
    Xg = (Xg - Xg.mean(0)) / (Xg.std(0) + 1e-9)
    p = PCA(n_components=min(n_components, Xg.shape[1]))
    Yg = p.fit_transform(Xg)

    comps = []
    for i in range(Yg.shape[1]):
        img = np.full(X.shape[0], np.nan, dtype="float32")
        img[good] = Yg[:, i]
        comps.append(img.reshape(shape))

    score = np.nansum([np.abs(c) for c in comps[1:1 + keep]], axis=0)
    score[~np.isfinite(comps[0])] = np.nan
    return score, comps, p.explained_variance_ratio_, names


# -------------------------------------------------------------- topographic

def copernicus_dem(bbox, like_profile=None, shape=None):
    """Copernicus 30 m DEM over the box, from the same STAC catalogue."""
    cat = pystac_client.Client.open(CATALOG)
    items = list(cat.search(collections=["cop-dem-glo-30"], bbox=bbox).items())
    if not items:
        raise RuntimeError(f"no Copernicus DEM tile for {bbox}")

    tiles = []
    for it in items:
        key = "data" if "data" in it.assets else list(it.assets)[0]
        with rasterio.open(it.assets[key].href) as src:
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
