"""L-band radar from the ALOS PALSAR annual mosaics.

Optical imagery sees the top of the canopy. On the Malabar coast that is thirty
metres of coconut and the ground is never visible, which is why I expect the
spectral arm to fail there. L-band radar at 23 cm penetrates vegetation and
responds to soil moisture and surface roughness instead, so it can see ground
that optical cannot.

The mosaics are annual, already orthorectified to EPSG:4326 at about 25 m, and
free. Planetary Computer hands out an anonymous token, so no account is needed.
"""

import numpy as np
import rasterio
import pystac_client
import planetary_computer as pc
from pyproj import Transformer
from rasterio.windows import from_bounds
from rasterio.enums import Resampling

CATALOG = "https://planetarycomputer.microsoft.com/api/stac/v1"

# The published calibration for the PALSAR mosaics: gamma0 in dB from the
# stored digital number.
CALIBRATION_OFFSET = -83.0


def _to_db(dn):
    dn = dn.astype("float32")
    out = np.full(dn.shape, np.nan, "float32")
    good = dn > 0
    out[good] = 10 * np.log10(dn[good] ** 2) + CALIBRATION_OFFSET
    return out


def palsar(bbox, years=("2019", "2020", "2021"), shape=None, profile=None):
    """Annual HH, HV and their ratio, averaged over `years`.

    `shape` and `profile` put the result on the optical grid so the two arms
    can go into the same stack. Without them the native 25 m grid is returned.
    """
    cat = pystac_client.Client.open(CATALOG, modifier=pc.sign_inplace)
    items = list(cat.search(collections=["alos-palsar-mosaic"], bbox=bbox,
                            datetime=f"{min(years)}-01-01/{max(years)}-12-31").items())
    if not items:
        raise RuntimeError(f"no PALSAR mosaic over {bbox} in {years}")

    stacks = {"hh": [], "hv": []}
    for it in items:
        for pol, key in (("hh", "HH"), ("hv", "HV")):
            if key not in it.assets:
                continue
            with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR"):
                with rasterio.open(it.assets[key].href) as src:
                    if profile is not None:
                        # reproject the window corners into the mosaic's CRS
                        t = Transformer.from_crs("EPSG:4326", src.crs, always_xy=True)
                        x0, y0 = t.transform(bbox[0], bbox[1])
                        x1, y1 = t.transform(bbox[2], bbox[3])
                        w = from_bounds(min(x0, x1), min(y0, y1),
                                        max(x0, x1), max(y0, y1), src.transform)
                    else:
                        w = from_bounds(*bbox, src.transform)
                    if w.width < 2 or w.height < 2:
                        continue
                    out_shape = shape or (int(round(w.height)), int(round(w.width)))
                    a = src.read(1, window=w, out_shape=out_shape,
                                 resampling=Resampling.bilinear)
            stacks[pol].append(_to_db(a))

    if not stacks["hh"]:
        raise RuntimeError(f"PALSAR items found but none covered {bbox}")

    with np.errstate(invalid="ignore"):
        out = {f"sar_{p}": np.nanmean(np.dstack(v), axis=2)
               for p, v in stacks.items() if v}
        if "sar_hh" in out and "sar_hv" in out:
            # The cross- to co-polarised difference separates volume scattering
            # from vegetation out of surface scattering from bare or wet ground.
            out["sar_ratio"] = out["sar_hh"] - out["sar_hv"]
    return out
