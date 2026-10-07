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
    """JRC Global Surface Water over the box, 1984 to 2021, about 30 m."""
    items = list(_client().search(collections=["jrc-gsw"], bbox=bbox).items())
    if not items:
        raise RuntimeError(f"no JRC surface water tile over {bbox}")
    out = {}
    for k in layers:
        for it in items:
            if k in it.assets:
                a = _read(it.assets[k].href, bbox, shape)
                if a is not None:
                    out[k] = a
                    break
    return out


def land_cover(bbox, shape=None, year=2021):
    """ESA WorldCover at 10 m, the most recent year available."""
    items = sorted(_client().search(collections=["esa-worldcover"], bbox=bbox).items(),
                   key=lambda i: i.datetime or 0)
    if not items:
        raise RuntimeError(f"no WorldCover tile over {bbox}")
    return _read(items[-1].assets["map"].href, bbox, shape)


def summarise(bbox, name=""):
    """Water extent, seasonality and loss, as areas in square kilometres."""
    gsw = surface_water(bbox)
    shape = gsw["occurrence"].shape
    lc = land_cover(bbox, shape=shape)

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
