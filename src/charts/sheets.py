"""Georeference Admiralty sheets from their own printed graticules.

The transform for each sheet comes off the sheet, not from matching features
against a modern map, which would import every error in the matching.

How each entry below is obtained. The neatline and the major latitude ticks are
detected automatically, since they are the strongest lines near each border.
The latitude values of those ticks, and the single longitude anchor, are read
from the sheet's own printed labels; there is no reliable way to OCR an 1850s
engraved italic numeral and no need to, because one anchor per sheet is enough.

Why one anchor is enough. These are Mercator charts, in which a minute of
longitude is the same number of pixels everywhere on the sheet, and that number
is fixed by the latitude scale through the secant of the mid latitude. So the
longitude axis needs a scale, which the latitude fit already supplies, and a
position, which is the anchor.

Each sheet is checked against a quantity not used in its fit, usually the
opposite neatline against the latitude range printed in the title.
"""
import json, math, pathlib

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
CHARTS = ROOT.parent / "library" / "charts"
OUT = ROOT / "data" / "processed" / "charts"


def dms(d, m=0):
    return d + m / 60.0


SHEETS = {
    "BA749": dict(
        file="malabar-749-1857.jpg",
        title="West Coast of India, Malabar Coast, sheet XI",
        frame="11d02' to 9d50' N", surveyor="Lieut. W. B. Selby I.N.",
        surveyed="1851-3", scale="1:146,000",
        tide="Cochin HW.F.&C. XIh26m, springs rise 3 ft, neaps rise 2.25 ft",
        neatline=dict(top=579, bottom=11691, left=692, right=7889),
        lat_px=[1033, 4082, 7126, 10174],
        lat_deg=[dms(11, 0), dms(10, 40), dms(10, 20), dms(10, 0)],
        lon_anchor_px=2256.0, lon_anchor_deg=dms(75, 40),
        check=("bottom neatline", 11691, dms(9, 50)),
    ),
    "BA750": dict(
        file="malabar-750-1857.jpg",
        title="West Coast of India, Malabar Coast, sheet XII",
        frame="9d53' to 8d40' N", surveyor="Lieut. W. B. Selby I.N.",
        surveyed="1850-2", scale="1:146,000",
        tide=None,
        neatline=dict(top=645, bottom=11729, left=686, right=7735),
        # the fourth tick coincides with the bottom neatline, which the
        # detector excludes as frame, so it is supplied here
        lat_px=[2642, 5672, 8696, 11729],
        lat_deg=[dms(9, 40), dms(9, 20), dms(9, 0), dms(8, 40)],
        lon_anchor_px=867.0, lon_anchor_deg=dms(76, 0),
        check=("top neatline", 645, dms(9, 53)),
    ),
}


def fit(sheet):
    y = np.asarray(sheet["lat_px"], dtype="float64")
    lat = np.asarray(sheet["lat_deg"], dtype="float64")
    a, b = np.polyfit(y, lat, 1)
    rms = float(np.sqrt(((lat - (a * y + b)) ** 2).mean()) * 60)
    n = sheet["neatline"]
    mid_lat = a * (n["top"] + n["bottom"]) / 2 + b
    px_lat_min = abs(1.0 / a) / 60.0
    px_lon_min = px_lat_min * math.cos(math.radians(mid_lat))
    return dict(lat_a=float(a), lat_b=float(b), lat_rms_arcmin=rms,
                px_per_arcmin_lat=px_lat_min, px_per_arcmin_lon=px_lon_min,
                mid_lat=float(mid_lat))


def to_lonlat(sheet, x, y, t=None):
    t = t or fit(sheet)
    lat = t["lat_a"] * np.asarray(y, dtype="float64") + t["lat_b"]
    lon = sheet["lon_anchor_deg"] + (np.asarray(x, dtype="float64")
                                     - sheet["lon_anchor_px"]) / t["px_per_arcmin_lon"] / 60.0
    return lon, lat


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    out = {}
    for key, s in SHEETS.items():
        t = fit(s)
        n = s["neatline"]
        w, north = to_lonlat(s, n["left"], n["top"], t)
        e, south = to_lonlat(s, n["right"], n["bottom"], t)
        label, px, stated = s["check"]
        _, got = to_lonlat(s, n["left"], px, t)
        err_m = abs(got - stated) * 111320

        print(f"{key}  {s['title']}")
        print(f"   {s['surveyor']}, {s['surveyed']}, {s['scale']}")
        print(f"   latitude residual {t['lat_rms_arcmin']:.4f} arcmin "
              f"({t['lat_rms_arcmin']*1852:.0f} m)   "
              f"{t['px_per_arcmin_lat']:.2f} px/arcmin")
        print(f"   check: {label} reads {got:.4f} N, sheet states {stated:.4f} "
              f"-> {err_m:.0f} m")
        print(f"   covers lon {w:.4f} to {e:.4f} E, lat {south:.4f} to {north:.4f} N\n")

        out[key] = {**{k: v for k, v in s.items() if k != "check"}, **t,
                    "bounds": dict(west=float(w), east=float(e),
                                   south=float(south), north=float(north)),
                    "check_error_m": float(err_m)}
    (OUT / "admiralty_georef.json").write_text(json.dumps(out, indent=1))
    print(f"-> charts/admiralty_georef.json  ({len(out)} sheets)")


if __name__ == "__main__":
    main()


def to_pixel(sheet, lon, lat, t=None):
    """Geographic coordinate to pixel on the sheet. Inverse of to_lonlat."""
    t = t or fit(sheet)
    y = (np.asarray(lat, dtype="float64") - t["lat_b"]) / t["lat_a"]
    x = sheet["lon_anchor_px"] + (np.asarray(lon, dtype="float64")
                                  - sheet["lon_anchor_deg"]) * 60 * t["px_per_arcmin_lon"]
    return x, y


def crop(key, west, south, east, north, out, max_px=2600):
    """Save the part of a sheet covering a geographic box."""
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    s = SHEETS[key]
    x0, y1 = to_pixel(s, west, south)
    x1, y0 = to_pixel(s, east, north)
    box = (int(max(0, x0)), int(max(0, y0)), int(x1), int(y1))
    im = Image.open(CHARTS / s["file"]).crop(box)
    if max(im.size) > max_px:
        f = max_px / max(im.size)
        im = im.resize((int(im.width * f), int(im.height * f)))
    im.save(out)
    return box, im.size
