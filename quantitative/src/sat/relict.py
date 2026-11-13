"""Ground truth for dead rivers, and the data to learn them from.

Every validation in this project so far has used a riparian control: a ring of
land just outside present water. That demonstrates the detector separates
channel-associated ground from ordinary ground, which is not the same as finding
a channel that is no longer there. The gap was recorded as needing a
hand-digitised relict meander, and it does not.

The JRC Global Surface Water transitions layer classifies every 30 m pixel on
earth by what happened to its water between 1984 and 2021, and two of its
classes, lost permanent and lost seasonal, are exactly a map of channels that
died inside the satellite record. Their positions are known, they are numerous,
and they are global.

That gives a supervised problem with the label and the evidence separated in
time. The label comes from Landsat imagery of the 1980s and 1990s. The features
come from Sentinel-2 composites of 2022 onward, by which date the water is gone
and only the trace it left is visible. A detector trained this way is asked the
archaeological question, with the answer known.

**The limit, stated here rather than buried.** A channel dry for twenty years is
not a channel dry for two thousand. The soil moisture, the vegetation contrast
and the sediment are all fresher. This validates the detector and the pipeline;
it does not establish that either transfers to AD 50, and §13 of the findings
applies in full.
"""
import numpy as np
import rasterio
from rasterio.warp import Resampling, reproject
from scipy import ndimage

from . import stack, water

# A reservoir drawn down and a river gone dry both read as lost water. Only the
# second has the shape this is about, so components are kept on elongation:
# the ratio of the principal axes of the pixel distribution. A straight reach
# scores high, a pond scores near one.
MIN_PIXELS = 60
MIN_ELONGATION = 3.0


def elongation(mask):
    """Ratio of major to minor axis of a binary blob, from its inertia tensor."""
    ys, xs = np.nonzero(mask)
    if len(ys) < 4:
        return 0.0
    pts = np.column_stack([ys - ys.mean(), xs - xs.mean()]).astype("float64")
    cov = pts.T @ pts / len(pts)
    ev = np.linalg.eigvalsh(cov)
    if ev[0] <= 1e-9:
        return 999.0
    return float(np.sqrt(ev[1] / ev[0]))


def lost_channels(transitions, min_px=MIN_PIXELS, min_elong=MIN_ELONGATION):
    """Elongated components of lost water: the dead channels.

    Returns the mask and, for reporting, how many components were dropped for
    being too small or too round, because that ratio is the honest measure of
    how much of "lost water" is actually river.
    """
    lost = np.isin(transitions, list(water.LOST))
    lab, n = ndimage.label(lost, structure=np.ones((3, 3)))
    keep = np.zeros_like(lost)
    kept = dropped_small = dropped_round = 0
    for i in range(1, n + 1):
        m = lab == i
        if m.sum() < min_px:
            dropped_small += 1
            continue
        if elongation(m) < min_elong:
            dropped_round += 1
            continue
        keep |= m
        kept += 1
    return keep, {"kept": kept, "dropped_small": dropped_small,
                  "dropped_round": dropped_round, "n_components": n}


def present_water(transitions):
    """Anything that holds water now, which is excluded from the problem.

    A net that finds present water has not learned anything about relict
    channels, so these pixels are neither positive nor negative: they are
    masked out of training and of scoring.
    """
    return np.isin(transitions, [1, 2, 4, 5, 7, 8, 9, 10])


def build(name, bbox, start="2022-01-01", end="2024-12-31", shape=None):
    """Features, labels and a validity mask for one region.

    Features are the same multi-season stack the PCA baseline uses, so the two
    methods are compared on identical evidence and any difference is the model.
    """
    comps, prof = {}, None
    for season in ("dry", "wet"):
        med, prof, _scenes = stack.cached_composite(name, bbox, start, end, season)
        comps[season] = med
    shape = shape or comps["dry"][stack.BANDS[0]].shape

    # Labels are derived at the JRC's own 30 m resolution and then warped onto
    # the feature grid. Two things have to be right here and the first attempt
    # got both wrong.
    #
    # The filters are in pixels, so deriving them on a 10 m grid would admit
    # components nine times smaller in ground area than the same thresholds
    # admit at 30 m, and the label set would depend on the feature resolution.
    #
    # And the grids are in different projections. JRC is geographic, Sentinel-2
    # is UTM, so resampling one onto the other by array index is not a
    # reprojection at all: it produces an array of the right shape sitting on
    # the wrong ground. The check that caught it is cheap and worth keeping as
    # a habit: ask whether the imagery's own water index can find the water the
    # label says is there. Before the fix that scored 0.46, chance. After it,
    # it should be high.
    g = water.surface_water(bbox, layers=("transitions",))
    trans = g["transitions"]
    pos_native, stats = lost_channels(trans)
    now_native = present_water(trans)

    src_tf = rasterio.transform.from_bounds(bbox[0], bbox[1], bbox[2], bbox[3],
                                            trans.shape[1], trans.shape[0])

    def to_grid(a):
        out = np.zeros(shape, dtype="uint8")
        reproject(a.astype("uint8"), out,
                  src_transform=src_tf, src_crs="EPSG:4326",
                  dst_transform=prof["transform"], dst_crs=prof["crs"],
                  resampling=Resampling.nearest)
        return out.astype(bool)

    pos = to_grid(pos_native)
    now = to_grid(now_native)

    # Stack the bands and the indices, seasons concatenated, as the baseline does.
    layers, names = [], []
    for season in ("dry", "wet"):
        med = comps[season]
        for b in stack.BANDS:
            layers.append(med[b].astype("float32"))
            names.append(f"{season}_{b}")
        from .detect import indices
        for k, v in indices(med).items():
            layers.append(v.astype("float32"))
            names.append(f"{season}_{k}")
    X = np.stack(layers)

    valid = np.isfinite(X).all(axis=0) & ~now
    return {"X": X, "y": pos, "valid": valid, "names": names,
            "bbox": bbox, "stats": stats, "shape": shape}


def scan(bbox, tile_deg=0.25, min_channel_frac=0.0015, max_present=0.45):
    """Find sub-boxes worth fetching imagery for, cheaply.

    The JRC layer is 30 m and global, so it can be read over a wide area for
    almost nothing, while a Sentinel-2 composite over the same area is gigabytes
    and minutes. Scanning the labels first and fetching imagery only where the
    labels are dense is the difference between a pipeline that runs on a laptop
    and one that does not.

    Boxes that are mostly present water are rejected: there is little room left
    in them for relict channel, and they teach the model about lakes.
    """
    g = surface_water_cached(bbox)
    trans = g["transitions"]
    H, W = trans.shape
    lon0, lat0, lon1, lat1 = bbox
    nx = max(1, int(round((lon1 - lon0) / tile_deg)))
    ny = max(1, int(round((lat1 - lat0) / tile_deg)))
    out = []
    for j in range(ny):
        for i in range(nx):
            r0, r1 = int(j * H / ny), int((j + 1) * H / ny)
            c0, c1 = int(i * W / nx), int((i + 1) * W / nx)
            sub = trans[r0:r1, c0:c1]
            if sub.size == 0:
                continue
            m, _ = lost_channels(sub)
            now = present_water(sub)
            if m.mean() < min_channel_frac or now.mean() > max_present:
                continue
            # raster rows run north to south
            b = [lon0 + (lon1 - lon0) * c0 / W,
                 lat1 - (lat1 - lat0) * r1 / H,
                 lon0 + (lon1 - lon0) * c1 / W,
                 lat1 - (lat1 - lat0) * r0 / H]
            out.append({"bbox": [round(v, 4) for v in b],
                        "channel_frac": round(float(m.mean()), 5),
                        "present_water": round(float(now.mean()), 4)})
    out.sort(key=lambda d: -d["channel_frac"])
    return out


_SW_CACHE = {}


def surface_water_cached(bbox, layers=("transitions",)):
    key = (tuple(bbox), layers)
    if key not in _SW_CACHE:
        _SW_CACHE[key] = water.surface_water(bbox, layers=layers)
    return _SW_CACHE[key]
