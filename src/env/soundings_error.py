"""What a circa-1700 sounding is actually worth, and whether the modern grid can replace it.

Section 19 established that no measured bathymetry exists at any of the seven
approaches, which leaves the historic charts carrying the depth evidence alone.
That raises two questions this module answers with numbers rather than prose.

**Can the modern interpolated grid stand in for the chart?** The twenty
transcribed soundings carry chart-crop pixels, not coordinates, so they cannot
be compared point to point with anything. They can be compared as a
distribution: whether the global grid reproduces the depth range a surveyor
recorded on the same water. If it does not, the grid is not merely unmeasured
but wrong, and that is worth knowing before anyone leans on it.

**How large is the error bar on a chart sounding?** Four terms, of which only
three can be quantified. The tide is now fitted from observation. The seasonal
non-tidal swing is fitted with it. Reading a number off a scanned engraving has
its own error. The vertical datum of a Dutch chart of about 1700 is unknown and
is the dominant term, which is why the comparison that matters is between two
approaches on the same sheet, where the datum cancels.
"""
import csv, pathlib, math

import numpy as np
import rasterio

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "processed"
CACHE = ROOT / "data" / "cache" / "bathymetry"

FATHOM = 1.8288

# Where each sheet's soundings sit, and the box offshore of it that the chart
# covers. The chart draws the approach, so the comparison samples water seaward
# of the entrance rather than the whole port box.
PLACES = {
    "Cranganore": {"region": "periyar", "box": (76.00, 10.05, 76.19, 10.35)},
    "Purakkad":   {"region": "pamba",   "box": (76.20, 9.25, 76.38, 9.50)},
}

# From `tidal_range.csv`, Cochin, the nearest gauge to both. Spring range is the
# full astronomical swing at springs, so half of it is the excursion either side
# of mean level, which is what a single sounding carries.
COCHIN = {"spring_range": 0.58, "neap_range": 0.26, "seasonal_range": 0.414}

# Transcribing a number from a scanned engraving. The chart prints whole and
# half fathoms, so a misread is half a fathom; this is the rounding half-width.
READING_M = 0.5 * FATHOM / 2


def grid_depths(region, box):
    """Modern interpolated depths inside a box, in metres, positive down."""
    p = CACHE / f"{region}_topo.tif"
    with rasterio.open(p) as s:
        a = s.read(1).astype("float32")
        t = s.transform
        rows, cols = a.shape
        xs = t.c + (np.arange(cols) + 0.5) * t.a
        ys = t.f + (np.arange(rows) + 0.5) * t.e
        cx = (xs >= box[0]) & (xs <= box[2])
        cy = (ys >= box[1]) & (ys <= box[3])
        sub = a[np.ix_(cy, cx)]
    sub = sub[np.isfinite(sub) & (sub < 0)]
    return -sub


def budget():
    """The error terms on one sounding, in metres, and their quadrature sum."""
    tide = COCHIN["spring_range"] / 2.0          # excursion either side of mean
    season = COCHIN["seasonal_range"] / 2.0
    read = READING_M
    known = math.sqrt(tide ** 2 + season ** 2 + read ** 2)
    return {"tide_m": tide, "seasonal_m": season, "reading_m": read,
            "quadrature_known_m": known}


def main():
    rows = list(csv.DictReader(open(ROOT / "data" / "raw" / "soundings_dutch_c1700.csv")))
    for r in rows:
        r["m"] = float(r["fathoms"]) * FATHOM

    b = budget()
    print("Error on a single circa-1700 sounding, in metres\n")
    print(f"   tide, half the Cochin spring range        ±{b['tide_m']:.2f}")
    print(f"   season, half the non-tidal annual swing   ±{b['seasonal_m']:.2f}")
    print(f"   reading a half-fathom engraving           ±{b['reading_m']:.2f}")
    print(f"   {'─'*46}")
    print(f"   quantifiable, in quadrature               ±{b['quadrature_known_m']:.2f}")
    print(f"   vertical datum of the sheet               unknown, and larger\n")

    out = []
    print("Against the modern interpolated grid\n")
    print(f"   {'group':24s} {'n':>3s} {'chart m':>16s} {'grid m':>16s}")
    for place, cfg in PLACES.items():
        g = grid_depths(cfg["region"], cfg["box"])
        for setting in ("entrance", "approach"):
            sub = [r for r in rows if r["place"] == place and r["setting"] == setting]
            if not sub:
                continue
            d = np.array([r["m"] for r in sub])
            label = f"{place} {setting}"
            print(f"   {label:24s} {len(d):3d} "
                  f"{d.min():6.1f}–{d.max():<9.1f} "
                  f"{np.percentile(g,5):6.1f}–{np.percentile(g,95):<9.1f}")
            out.append({"place": place, "setting": setting, "n": len(d),
                        "chart_min_m": round(float(d.min()), 2),
                        "chart_median_m": round(float(np.median(d)), 2),
                        "chart_max_m": round(float(d.max()), 2),
                        "grid_p5_m": round(float(np.percentile(g, 5)), 1),
                        "grid_median_m": round(float(np.median(g)), 1),
                        "grid_p95_m": round(float(np.percentile(g, 95)), 1),
                        "grid_cells": int(g.size),
                        "error_quadrature_m": round(b["quadrature_known_m"], 2)})

    # How shallow the grid thinks this water gets, against the chart's shoalest.
    print("\nWhat the grid misses\n")
    for place, cfg in PLACES.items():
        g = grid_depths(cfg["region"], cfg["box"])
        sub = [r["m"] for r in rows if r["place"] == place]
        shoalest = min(sub)
        frac = float((g <= shoalest).mean())
        print(f"   {place:12s} chart's shoalest {shoalest:5.1f} m; "
              f"{frac:5.1%} of grid cells are that shallow "
              f"(grid minimum {g.min():.1f} m)")

    # The comparison the datum cancels in, and the one the thesis needs.
    cran_e = np.array([r["m"] for r in rows if r["place"] == "Cranganore"
                       and r["setting"] == "entrance"])
    pur = np.array([r["m"] for r in rows if r["place"] == "Purakkad"])
    diff = pur.mean() - cran_e.mean()

    # The datum cancels within one sheet, but the tide and the season do not
    # average down the way the reading error does. A surveyor sounds one
    # approach over a few hours and the other on another day, so the tidal and
    # seasonal offsets are common to all the soundings at a place rather than
    # independent between them. Only the reading error is per sounding.
    common = math.sqrt(b["tide_m"] ** 2 + b["seasonal_m"] ** 2)
    se = math.sqrt(2 * common ** 2
                   + b["reading_m"] ** 2 * (1 / len(cran_e) + 1 / len(pur)))
    naive = b["quadrature_known_m"] * math.sqrt(1 / len(cran_e) + 1 / len(pur))
    print(f"\nPurakkad approach minus Cranganore entrance: "
          f"{diff:.2f} m ± {se:.2f}  ({diff / se:.1f} sigma)")
    print(f"   treating every term as independent would give ±{naive:.2f} "
          f"({diff / naive:.1f} sigma), which is too generous:")
    print("   the tide and the season are common to a visit, not per sounding.")
    print("   The datum cancels within one sheet, so this contrast is the usable result.")

    dest = OUT / "soundings_error_budget.csv"
    with open(dest, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader(); w.writerows(out)
    print(f"\n-> {dest.name}")


if __name__ == "__main__":
    main()
