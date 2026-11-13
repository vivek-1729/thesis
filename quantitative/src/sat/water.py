"""Water history and land cover, from global products that are already made.

Giosan and colleagues quantified Indus delta change by differencing a
nineteenth-century Admiralty survey against a modern surface. We do not have the
charts yet, but the modern half can be built now, and one of these products
reaches further back than any imagery we can process ourselves.

The JRC Global Surface Water layers are derived from every Landsat scene from
1984 to 2021. The `transitions` layer in particular records where permanent
water has been lost, which on the Malabar coast maps the Kuttanad reclamation
directly. That is a measured lower bound on how much water has been taken out of
the system, which is exactly the quantity the pre-dam question needs.
"""

import time
import numpy as np
import rasterio
import pystac_client
import planetary_computer as pc
from rasterio.windows import from_bounds
from rasterio.enums import Resampling

CATALOG = "https://planetarycomputer.microsoft.com/api/stac/v1"

# JRC transition classes, from the product documentation.
TRANSITIONS = {
    0: "not water", 1: "permanent", 2: "new permanent", 3: "lost permanent",
    4: "seasonal", 5: "new seasonal", 6: "lost seasonal",
    7: "seasonal to permanent", 8: "permanent to seasonal",
    9: "ephemeral permanent", 10: "ephemeral seasonal",
}
LOST = {3, 6}                 # permanent or seasonal water that is now gone
GAINED = {2, 5}

# ESA WorldCover classes we care about separating.
WORLDCOVER = {10: "tree cover", 20: "shrubland", 30: "grassland",
              40: "cropland", 50: "built-up", 60: "bare", 70: "snow",
              80: "permanent water", 90: "herbaceous wetland",
              95: "mangroves", 100: "moss"}


def _client():
    return pystac_client.Client.open(CATALOG, modifier=pc.sign_inplace)


def _read(href, bbox, shape=None, resampling=Resampling.nearest, tries=3):
    """Windowed read, retried. These are large global mosaics served over HTTP
    and a single range request failing is common enough to be worth retrying."""
    last = None
    for attempt in range(tries):
        try:
            with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
                              GDAL_HTTP_MAX_RETRY="3", GDAL_HTTP_RETRY_DELAY="2"):
                with rasterio.open(href) as src:
                    w = from_bounds(*bbox, src.transform)
                    if w.width < 2 or w.height < 2:
                        return None
                    out_shape = shape or (int(round(w.height)), int(round(w.width)))
                    return src.read(1, window=w, out_shape=out_shape,
                                    resampling=resampling)
        except Exception as e:
            last = e
            time.sleep(2 * (attempt + 1))
    raise last


def surface_water(bbox, shape=None, layers=("occurrence", "seasonality",
                                            "transitions", "change")):
    """JRC Global Surface Water over the box, 1984 to 2021, about 30 m.

    The product is tiled 10 degrees square, so a box that crosses a tile
    boundary intersects more than one. An earlier version of this function read
    whichever tile the search happened to return first, which for such a box
    means requesting a window that is mostly outside the tile and getting an
    array that looks plausible and is wrong. One Aral Sea box read that way
    reported six times the lost water it actually has.

    Boxes inside a single tile, which includes all seven port boxes, were never
    affected. Boxes that cross a boundary are now mosaicked.
    """
    items = list(_client().search(collections=["jrc-gsw"], bbox=bbox).items())
    if not items:
        raise RuntimeError(f"no JRC surface water tile over {bbox}")
    out = {}
    for k in layers:
        here = [it for it in items if k in it.assets]
        if not here:
            continue
        if len(here) == 1:
            a = _read(here[0].assets[k].href, bbox, shape)
            if a is not None:
                out[k] = a
            continue
        out[k] = _mosaic(here, k, bbox, shape)
    return out


def _mosaic(items, layer, bbox, shape=None):
    """Read each intersecting tile over its own share of the box and join them.

    Each tile is read only over the part of the requested box it actually
    covers, then placed into the output by that sub-box's position. Tiles
    overlap by nothing, so no blending is needed; gaps stay zero, which for
    every JRC layer means "not water".
    """
    lon0, lat0, lon1, lat1 = bbox
    probe = None
    for it in items:
        tb = it.bbox
        sub = [max(lon0, tb[0]), max(lat0, tb[1]), min(lon1, tb[2]), min(lat1, tb[3])]
        if sub[2] <= sub[0] or sub[3] <= sub[1]:
            continue
        a = _read(it.assets[layer].href, sub)
        if a is None:
            continue
        probe = probe or {}
        probe[tuple(sub)] = a

    if not probe:
        return None
    # Work out a common grid from the finest piece, then place each piece.
    px = max(a.shape[1] / (sb[2] - sb[0]) for sb, a in probe.items())
    py = max(a.shape[0] / (sb[3] - sb[1]) for sb, a in probe.items())
    H = int(round((lat1 - lat0) * py))
    W = int(round((lon1 - lon0) * px))
    first = next(iter(probe.values()))
    out = np.zeros((H, W), dtype=first.dtype)
    for sb, a in probe.items():
        c0 = int(round((sb[0] - lon0) * px))
        c1 = min(W, c0 + int(round((sb[2] - sb[0]) * px)))
        r0 = int(round((lat1 - sb[3]) * py))
        r1 = min(H, r0 + int(round((sb[3] - sb[1]) * py)))
        if r1 <= r0 or c1 <= c0:
            continue
        ys = (np.linspace(0, a.shape[0] - 1, r1 - r0)).astype(int)
        xs = (np.linspace(0, a.shape[1] - 1, c1 - c0)).astype(int)
        out[r0:r1, c0:c1] = a[np.ix_(ys, xs)]

    if shape is not None and out.shape != tuple(shape):
        ys = np.linspace(0, out.shape[0] - 1, shape[0]).astype(int)
        xs = np.linspace(0, out.shape[1] - 1, shape[1]).astype(int)
        out = out[np.ix_(ys, xs)]
    return out


def land_cover(bbox, shape=None):
    """ESA WorldCover at 10 m, from whichever tile covers the box.

    The tiles are 3 degrees square, so a box can return several items of which
    only one actually contains it. Taking the most recent blindly fails on the
    Rufiji, which straddles a tile edge; try each and keep the first that reads.
    """
    items = sorted(_client().search(collections=["esa-worldcover"], bbox=bbox).items(),
                   key=lambda i: i.datetime or 0, reverse=True)
    for it in items:
        if "map" not in it.assets:
            continue
        try:
            a = _read(it.assets["map"].href, bbox, shape, tries=1)
        except Exception:
            continue
        if a is not None and (a > 0).any():
            return a
    return None


def summarise(bbox, name=""):
    """Water extent, seasonality and loss, as areas in square kilometres."""
    gsw = surface_water(bbox)
    shape = gsw["occurrence"].shape
    try:
        lc = land_cover(bbox, shape=shape)
    except Exception:
        lc = None

    # Pixel area from the box, which is adequate at these latitudes.
    import math
    lat = 0.5 * (bbox[1] + bbox[3])
    km2 = ((bbox[2] - bbox[0]) * 111.32 * math.cos(math.radians(lat))
           * (bbox[3] - bbox[1]) * 110.57) / (shape[0] * shape[1])

    occ, seas, trans = gsw["occurrence"], gsw["seasonality"], gsw["transitions"]
    ever = occ > 0
    permanent = seas >= 12                      # water in all twelve months
    lost = np.isin(trans, list(LOST))
    gained = np.isin(trans, list(GAINED))

    rec = {
        "region": name, "bbox": bbox, "pixel_km2": km2,
        "ever_water_km2": float(ever.sum() * km2),
        "permanent_km2": float(permanent.sum() * km2),
        "seasonal_km2": float(((occ > 0) & ~permanent).sum() * km2),
        "lost_km2": float(lost.sum() * km2),
        "gained_km2": float(gained.sum() * km2),
        "net_change_km2": float((gained.sum() - lost.sum()) * km2),
    }
    if lc is not None:
        rec["land_cover_km2"] = {
            WORLDCOVER.get(int(v), str(v)): float((lc == v).sum() * km2)
            for v in np.unique(lc) if v in WORLDCOVER
        }
    return rec, gsw, lc
