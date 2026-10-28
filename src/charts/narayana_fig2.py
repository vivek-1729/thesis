"""Georeference the Narayana, Priju and Chakrabarti 2001 geomorphic map.

Figure 2 of that short communication is the only published map of the
palaeo-landscape around the Periyar mouth. It marks two palaeodeltas, at
Munambam and at Varapuzha, two yazoo belts, and a line the authors label
ANCIENT SHORELINE running inland of the modern coast from near Krishnan Kotta
through Parur and on south past Edapalli and Chitrapuzha.

The search recorded in `docs/new_findings.md` section 7 concluded that no agency
anywhere publishes a buried-channel layer for Kerala. This figure is what exists
instead, and the point of this module is to turn a picture of a map into a map,
so that the features on it can be compared with the candidate positions, the
1857 Admiralty sheets and the satellite water record on the same ground.

It can be georeferenced for the same reason the Admiralty sheets can: it carries
its own graticule, labelled 76 degrees 10, 15, 20 and 25 minutes east along the
top and 10 degrees 15 down to 9 degrees 55 north down the right.

What the graticule will not give is accuracy better than the scan. The ticks on
the top border and the ticks on the bottom border do not agree on where a given
meridian sits, and they disagree by an amount that shrinks from 33 pixels at 76
degrees 15 to 16 pixels at 76 degrees 25. A rotation would give a constant
offset and a shear would too. A figure photographed or scanned from a bound
journal, with the page curving into the gutter, gives exactly this. So the
transform here is affine and fitted by least squares over every tick, the
residual is reported rather than hidden, and that residual is the honest
accuracy of anything read off this figure.

One date, and it is the important caveat. The paper assigns no age to the
ancient shoreline or to either palaeodelta. It closes by saying that efforts
are being made to date the various geomorphic elements. Nothing here is a
first-century coastline until something dates it.
"""
import csv, pathlib

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

ROOT = pathlib.Path(__file__).resolve().parents[2]
FIG = ROOT / "figures" / "sources" / "narayana2001_fig2.png"
OUT = ROOT / "data" / "processed"


def dms(d, m):
    return d + m / 60


# Tick positions in pixels, found by looking for short marks protruding outside
# each border, and the coordinate each one is labelled with.
#
# The top border is itself 10 degrees 15 north and the right border 76 degrees
# 25 east, which is why those ticks sit on the frame. The bottom border is not
# labelled with a tick but the latitude ticks on the right place it at 9
# degrees 55.0 by extrapolation, which is what the figure's own axis label
# says, and is the check that the reading of the graticule is right.
CONTROL = [
    # x, y, lon, lat, which border
    (588.0,  743.0, dms(76, 10), dms(10, 15), "top"),
    (1316.0, 743.0, dms(76, 15), dms(10, 15), "top"),
    (2051.0, 743.0, dms(76, 20), dms(10, 15), "top"),
    (2781.0, 743.0, dms(76, 25), dms(10, 15), "top"),
    (2792.0, 739.5, dms(76, 25), dms(10, 15), "right"),
    (2792.0, 1456.0, dms(76, 25), dms(10, 10), "right"),
    (2792.0, 2172.0, dms(76, 25), dms(10, 5), "right"),
    (2792.0, 2890.0, dms(76, 25), dms(10, 0), "right"),
    (1348.5, 3612.0, dms(76, 15), dms(9, 55), "bottom"),
    (2074.0, 3612.0, dms(76, 20), dms(9, 55), "bottom"),
    (2797.0, 3612.0, dms(76, 25), dms(9, 55), "bottom"),
]

# Places named on the figure, read off it, for checking the fit against
# somewhere independently known. These are the modern settlements, whose
# positions come from the gazetteer, not from this map.
CHECKS = {
    "Munambam": (76.1750, 10.1783),
    "Parur": (76.2244, 10.1436),
    "Alwaye": (76.3522, 10.1081),
    "Ernakulam": (76.2833, 9.9816),
    "Kodungallur": (76.1950, 10.2256),
}


def fit(points):
    """Least-squares affine from (lon, lat) to (x, y), and its inverse."""
    A = np.array([[p[2], p[3], 1.0] for p in points])
    X = np.array([p[0] for p in points])
    Y = np.array([p[1] for p in points])
    cx, *_ = np.linalg.lstsq(A, X, rcond=None)
    cy, *_ = np.linalg.lstsq(A, Y, rcond=None)
    return cx, cy


def to_pixel(cx, cy, lon, lat):
    v = np.array([lon, lat, 1.0])
    return float(cx @ v), float(cy @ v)


def to_lonlat(cx, cy, x, y):
    M = np.array([[cx[0], cx[1]], [cy[0], cy[1]]])
    b = np.array([x - cx[2], y - cy[2]])
    lon, lat = np.linalg.solve(M, b)
    return float(lon), float(lat)


def main():
    cx, cy = fit(CONTROL)

    # Pixel size on the ground, from the transform itself.
    deg = 1 / 60 / 60
    x0, y0 = to_pixel(cx, cy, 76.3, 10.1)
    x1, y1 = to_pixel(cx, cy, 76.3 + deg, 10.1)
    x2, y2 = to_pixel(cx, cy, 76.3, 10.1 + deg)
    px_per_arcsec_lon = np.hypot(x1 - x0, y1 - y0)
    px_per_arcsec_lat = np.hypot(x2 - x0, y2 - y0)
    m_per_px = 30.87 / px_per_arcsec_lat  # 1 arcsec of latitude is 30.87 m

    print(f"figure {Image.open(FIG).size[0]} x {Image.open(FIG).size[1]} px")
    print(f"ground resolution {m_per_px:.1f} m per pixel\n")

    print("residuals at the control points")
    res = []
    for x, y, lon, lat, edge in CONTROL:
        px, py = to_pixel(cx, cy, lon, lat)
        d = np.hypot(px - x, py - y)
        res.append(d)
        print(f"   {edge:7s} {lon:9.4f} {lat:8.4f}   "
              f"{d:6.1f} px  {d * m_per_px:7.0f} m")
    rms = float(np.sqrt(np.mean(np.square(res))))
    print(f"\n   RMS {rms:.1f} px, {rms * m_per_px:.0f} m; "
          f"worst {max(res):.1f} px, {max(res) * m_per_px:.0f} m\n")

    print("named places, figure pixel against gazetteer position")
    rows = []
    for name, (lon, lat) in CHECKS.items():
        px, py = to_pixel(cx, cy, lon, lat)
        inside = 0 <= px < 3224 and 0 <= py < 4365
        print(f"   {name:12s} lon {lon:8.4f} lat {lat:7.4f} -> "
              f"({px:7.1f}, {py:7.1f}){'' if inside else '   OFF SHEET'}")
        rows.append(dict(name=name, lon=lon, lat=lat,
                         x=round(px, 1), y=round(py, 1)))

    dest = OUT / "narayana2001_fig2_georef.csv"
    with open(dest, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["item", "a", "b", "c"])
        w.writerow(["x_from_lonlat", *[f"{v:.10g}" for v in cx]])
        w.writerow(["y_from_lonlat", *[f"{v:.10g}" for v in cy]])
        w.writerow([])
        w.writerow(["control_x", "control_y", "lon", "lat", "edge",
                    "residual_px", "residual_m"])
        for (x, y, lon, lat, edge), d in zip(CONTROL, res):
            w.writerow([x, y, f"{lon:.6f}", f"{lat:.6f}", edge,
                        round(d, 1), round(d * m_per_px)])
        w.writerow([])
        w.writerow(["place", "lon", "lat", "x", "y"])
        for r in rows:
            w.writerow([r["name"], r["lon"], r["lat"], r["x"], r["y"]])
    print(f"\n-> {dest}")


if __name__ == "__main__":
    main()
