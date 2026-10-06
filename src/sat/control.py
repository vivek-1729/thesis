"""Does the detector separate channel ground from ordinary ground?

The positive control is a modern river course from HydroRIVERS with its open
water masked out. Masking the water is the whole point: we want to know whether
the method sees the moisture and vegetation signature *around* a channel, which
is what a dry palaeochannel leaves behind, rather than seeing water.

The negative control is a set of lines of the same length and shape dropped at
random in the same box, away from anything mapped.

The criterion is fixed before running: AUC >= 0.75 or the method has not
transferred to that landscape.
"""

import pathlib
import numpy as np
import shapefile
from pyproj import Transformer
from scipy import ndimage

AUC_THRESHOLD = 0.75
HYDRO = pathlib.Path(__file__).resolve().parents[2] / "data" / "raw" / "hydrorivers"


def rivers_in_box(bbox, region="as"):
    """HydroRIVERS centrelines clipped to the box, as lon/lat vertex lists."""
    shp = next((HYDRO / f"HydroRIVERS_v10_{region}_shp").glob("*.shp"))
    out = []
    with shapefile.Reader(str(shp)) as r:
        for sh in r.iterShapes():
            xs = [p[0] for p in sh.points]
            ys = [p[1] for p in sh.points]
            if max(xs) < bbox[0] or min(xs) > bbox[2]:
                continue
            if max(ys) < bbox[1] or min(ys) > bbox[3]:
                continue
            pts = [(x, y) for x, y in sh.points
                   if bbox[0] <= x <= bbox[2] and bbox[1] <= y <= bbox[3]]
            if len(pts) >= 2:
                out.append(pts)
    return out


def _to_pixels(pts, profile, shape):
    """lon/lat -> (row, col), dropping anything off the raster."""
    t = Transformer.from_crs("EPSG:4326", profile["crs"], always_xy=True)
    inv = ~profile["transform"]
    rc = []
    for lon, lat in pts:
        x, y = t.transform(lon, lat)
        c, r = inv * (x, y)
        r, c = int(round(r)), int(round(c))
        if 0 <= r < shape[0] and 0 <= c < shape[1]:
            rc.append((r, c))
    return rc


def _rasterise(lines, profile, shape, width_px=3):
    """Burn line vertices into a boolean mask, dilated to a plausible width."""
    m = np.zeros(shape, bool)
    for pts in lines:
        rc = _to_pixels(pts, profile, shape)
        for i in range(len(rc) - 1):
            (r0, c0), (r1, c1) = rc[i], rc[i + 1]
            n = max(abs(r1 - r0), abs(c1 - c0), 1)
            for k in range(n + 1):           # walk the segment
                r = int(round(r0 + (r1 - r0) * k / n))
                c = int(round(c0 + (c1 - c0) * k / n))
                m[r, c] = True
    if width_px > 1:
        m = ndimage.binary_dilation(m, iterations=width_px)
    return m


def water_mask(med, ndwi_cut=0.0):
    """Open water, from NDWI on the dry-season composite."""
    e = 1e-6
    ndwi = (med["green"] - med["nir"]) / (med["green"] + med["nir"] + e)
    return ndwi > ndwi_cut


def negative_controls(positive, shape, n_per_piece=8, buffer_px=25, rng=None):
    """Each river segment re-placed at random, away from any real one.

    Translating the whole mask at once never works: the segments are spread out,
    so every offset lands one of them back on top of another. Moving each
    connected piece independently keeps the length, width and sinuosity of a
    real channel while freeing the placement.
    """
    rng = rng or np.random.default_rng(0)
    keep_out = ndimage.binary_dilation(positive, iterations=buffer_px)
    out = np.zeros(shape, bool)

    labels, n = ndimage.label(positive)
    for k in range(1, n + 1):
        rows, cols = np.nonzero(labels == k)
        if len(rows) < 20:
            continue
        dr, dc = rows - rows.min(), cols - cols.min()
        h, w = dr.max() + 1, dc.max() + 1
        if h >= shape[0] or w >= shape[1]:
            continue
        placed = 0
        for _ in range(n_per_piece * 60):
            if placed >= n_per_piece:
                break
            r0 = rng.integers(0, shape[0] - h)
            c0 = rng.integers(0, shape[1] - w)
            rr, cc = dr + r0, dc + c0
            if keep_out[rr, cc].any() or out[rr, cc].any():
                continue
            out[rr, cc] = True
            placed += 1
    return out


def auc(score, positive, negative):
    """Mann-Whitney AUC: P(score on a channel pixel > score off one).

    0.5 is chance. Rank-based, so it does not care about the score's units or
    whether its distribution is sensible.
    """
    a = score[positive & np.isfinite(score)]
    b = score[negative & np.isfinite(score)]
    if len(a) < 30 or len(b) < 30:
        raise RuntimeError(f"too few control pixels: {len(a)} positive, {len(b)} negative")
    allv = np.concatenate([a, b])
    ranks = allv.argsort().argsort().astype("float64") + 1
    ra = ranks[: len(a)].sum()
    return (ra - len(a) * (len(a) + 1) / 2) / (len(a) * len(b)), len(a), len(b)


def evaluate(score, bbox, profile, med, region="as", label=""):
    """Full control test. Returns a dict, and prints the verdict."""
    shape = score.shape
    lines = rivers_in_box(bbox, region)
    if not lines:
        raise RuntimeError(f"HydroRIVERS maps nothing inside {bbox}")

    pos = _rasterise(lines, profile, shape)
    pos &= ~water_mask(med)                 # the signature, not the water
    neg = negative_controls(pos, shape)

    a, npos, nneg = auc(score, pos, neg)
    verdict = "PASS" if a >= AUC_THRESHOLD else "FAIL"
    print(f"{label:28s} AUC={a:.3f}  ({npos} positive, {nneg} negative px)  {verdict}")
    return {"label": label, "auc": float(a), "n_pos": int(npos),
            "n_neg": int(nneg), "pass": bool(a >= AUC_THRESHOLD),
            "threshold": AUC_THRESHOLD}

def riparian_control(med, inner_px=2, outer_px=12, min_water_px=400):
    """Positive control derived from the imagery, not from an external network.

    HydroRIVERS turned out to be the wrong ground truth: it is built from a
    500 m DEM, so in the Ghaggar box its lines sat a median of 417 m from any
    water and followed irrigation canals rather than channels.

    This instead finds actual water in the dry-season composite and takes the
    ring of dry ground just outside it. That ring is where a channel's moisture
    signature lives, which is the same signature a dry palaeochannel leaves, and
    it is located correctly by construction. The water itself is excluded, so
    the detector is never simply seeing water.
    """
    water = water_mask(med)
    if water.sum() < min_water_px:
        raise RuntimeError(f"only {water.sum()} water pixels; no usable positive control")
    inner = ndimage.binary_dilation(water, iterations=inner_px)
    outer = ndimage.binary_dilation(water, iterations=outer_px)
    return outer & ~inner, water


def evaluate_riparian(score, med, label="", rng=None, n_sample=40000):
    """Control test against the imagery-derived riparian ring.

    Negatives are a random sample of pixels well away from any water. An earlier
    version tried to place shape-matched copies of the positive mask, which
    never succeeded: the ring around water is one huge connected component and
    there is nowhere to put it. Shape matching was over-engineering anyway,
    since the AUC is computed per pixel and does not see the mask's shape.
    """
    rng = rng or np.random.default_rng(0)
    pos, water = riparian_control(med)
    eligible = (~ndimage.binary_dilation(water, iterations=60)
                & np.isfinite(score) & ~pos)
    if eligible.sum() < 1000:
        raise RuntimeError("almost nothing far enough from water to sample as negative")

    pi = np.flatnonzero(pos.ravel() & np.isfinite(score).ravel())
    ni = np.flatnonzero(eligible.ravel())
    pi = rng.choice(pi, min(n_sample, pi.size), replace=False)
    ni = rng.choice(ni, min(n_sample, ni.size), replace=False)

    flat = score.ravel()
    a = flat[pi]
    b = flat[ni]
    allv = np.concatenate([a, b])
    ranks = allv.argsort().argsort().astype("float64") + 1
    auc_val = (ranks[: len(a)].sum() - len(a) * (len(a) + 1) / 2) / (len(a) * len(b))

    verdict = "PASS" if auc_val >= AUC_THRESHOLD else "FAIL"
    print(f"{label:38s} AUC={auc_val:.3f}  ({len(a)} positive, {len(b)} negative px)  {verdict}")
    return {"label": label, "auc": float(auc_val), "n_pos": int(len(a)),
            "n_neg": int(len(b)), "pass": bool(auc_val >= AUC_THRESHOLD),
            "threshold": AUC_THRESHOLD, "control": "riparian"}
