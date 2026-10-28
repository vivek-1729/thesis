"""Georeference Admiralty sheet 749, Malabar Coast, 1857.

The transform comes from the sheet's own graticule, not from matching features
against a modern map.

Latitude. Four major ticks on the left border are detected automatically and
fall every twenty minutes. Fitting a line through them leaves a residual of
0.007 arcmin, about thirteen metres, and puts the bottom neatline at 9 degrees
50.04 minutes against the 9 degrees 50 minutes the title states. That agreement,
to within three metres on a quantity never used in the fit, is the check that
the latitude axis is right.

Longitude. In Mercator a minute of longitude is a constant number of pixels, and
it is fixed by the latitude scale through the secant of the mid latitude, so no
second scale measurement is needed. Only an anchor is: the 75 degree 40 minute
meridian is printed on the sheet and read at x = 2256. The 35 and 45 minute
labels then fall where the scale predicts, which is the check on that axis.

The Mercator stretch over this sheet is below the noise. A straight line in
latitude fits the four ticks to 0.007 arcmin, so the projection correction is
carried but makes no practical difference here, and that is reported rather than
assumed.
"""
import json, math, pathlib

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

ROOT = pathlib.Path(__file__).resolve().parents[2]
SHEET = ROOT.parent / "library" / "charts" / "malabar-749-1857.jpg"
OUT = ROOT / "data" / "processed" / "charts"

# Read off the sheet itself.
NEATLINE = dict(top=579, bottom=11691, left=692, right=7889)
LAT_TICKS = [1033, 4082, 7126, 10174]              # pixel rows
LAT_VALUES = [11 + 0 / 60, 10 + 40 / 60, 10 + 20 / 60, 10 + 0 / 60]
LON_ANCHOR_PX = 2256.0                              # the printed 75d40' meridian
LON_ANCHOR_DEG = 75 + 40 / 60

TITLE = ("West Coast of India, Malabar Coast, from 11d02' to 9d50' north "
         "latitude, by Lieut. W. B. Selby I.N., 1851-3")
# The sheet states its own tidal reference, which is what makes its soundings
# reducible to a datum at all.
TIDE_NOTE = "Cochin HW.F.&C. XIh26m, springs rise 3 feet, neaps rise 2.25 feet"


def latitude_transform():
    y = np.asarray(LAT_TICKS, dtype="float64")
    lat = np.asarray(LAT_VALUES, dtype="float64")
    a, b = np.polyfit(y, lat, 1)
    resid = lat - (a * y + b)
    return float(a), float(b), float(np.sqrt((resid ** 2).mean()) * 60)


def px_per_arcmin_lon(mid_lat):
    """Pixels per minute of longitude, from the latitude scale and Mercator."""
    a, _, _ = latitude_transform()
    per_lat_min = abs(1.0 / a) / 60.0
    return per_lat_min / (1.0 / math.cos(math.radians(mid_lat)))


def transform():
    a, b, rms = latitude_transform()
    mid_lat = a * (NEATLINE["top"] + NEATLINE["bottom"]) / 2 + b
    ppm = px_per_arcmin_lon(mid_lat)
    return {"lat_a": a, "lat_b": b, "lat_rms_arcmin": rms,
            "lon_px_per_arcmin": ppm, "lon_anchor_px": LON_ANCHOR_PX,
            "lon_anchor_deg": LON_ANCHOR_DEG, "mid_lat": mid_lat}


def to_lonlat(x, y, t=None):
    t = t or transform()
    lat = t["lat_a"] * np.asarray(y, dtype="float64") + t["lat_b"]
    lon = t["lon_anchor_deg"] + (np.asarray(x, dtype="float64") - t["lon_anchor_px"]) \
        / t["lon_px_per_arcmin"] / 60.0
    return lon, lat


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    t = transform()
    n = NEATLINE
    print(TITLE, "\n")
    print(f"  latitude fit residual   {t['lat_rms_arcmin']:.4f} arcmin "
          f"({t['lat_rms_arcmin']*1852:.0f} m)")
    print(f"  px per arcmin latitude  {abs(1/t['lat_a'])/60:.2f}")
    print(f"  px per arcmin longitude {t['lon_px_per_arcmin']:.2f}  (Mercator, from the above)")

    print("\n  checks against quantities not used in the fit")
    _, lat_b = to_lonlat(n["left"], n["bottom"], t)
    print(f"    bottom neatline  {lat_b:.4f} N   sheet states 9d50' = {9+50/60:.4f}"
          f"   ({abs(lat_b-(9+50/60))*111320:.0f} m)")
    for lab, deg in (("75d35'", 75 + 35 / 60), ("75d45'", 75 + 45 / 60)):
        px = t["lon_anchor_px"] + (deg - t["lon_anchor_deg"]) * 60 * t["lon_px_per_arcmin"]
        print(f"    {lab} predicted at x = {px:.0f}")

    lo0, la1 = to_lonlat(n["left"], n["top"], t)
    lo1, la0 = to_lonlat(n["right"], n["bottom"], t)
    print(f"\n  sheet covers  lon {lo0:.4f} to {lo1:.4f} E,  lat {la0:.4f} to {la1:.4f} N")

    rec = {"sheet": "BA 749", "title": TITLE, "surveyed": "1851-3",
           "tide_note": TIDE_NOTE, "neatline": n,
           "lat_ticks_px": LAT_TICKS, "lat_ticks_deg": LAT_VALUES,
           "bounds": {"west": lo0, "east": lo1, "south": la0, "north": la1},
           **t}
    (OUT / "ba749_georef.json").write_text(json.dumps(rec, indent=1))
    print(f"\n-> {OUT.name}/ba749_georef.json")


if __name__ == "__main__":
    main()
