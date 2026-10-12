"""Bathymetry over each port's approach, and how much of it is actually measured.

`DATA.md` listed GEBCO as available and unused. GMRT serves the same areas at a
much finer cell with no registration, which looked like an improvement until the
data mask was checked.

GMRT publishes two layers. `topo` is the grid it will hand you, filled
everywhere. `topo-mask` is the same grid with the interpolated cells removed, so
differencing the two says which cells rest on a real sounding. That distinction
is the whole point of this module: a 60 m cell carrying no measurement is a
450 m GEBCO cell wearing a smaller coat, and reporting depth from it would be an
artefact of the kind this project has been caught by before.

So the output is a depth raster per port and a coverage table beside it, and the
coverage table is the part that should be read first.
"""
import pathlib, urllib.request, csv

import numpy as np
import rasterio

ROOT = pathlib.Path(__file__).resolve().parents[2]
CACHE = ROOT / "data" / "cache" / "bathymetry"
OUT = ROOT / "data" / "processed"

# The water boxes from `sat/run_water.py`, each pushed seaward so the approach
# a ship would use is inside the frame rather than clipped at the beach.
BOXES = {
    "periyar": ([75.85, 10.00, 76.45, 10.45], "Muziris: Periyar delta and its approach"),
    "pamba":   ([76.00, 9.15, 76.60, 9.60],  "Nelkynda and Bakarē: Pamba mouth and the Alappuzha roadstead"),
    "tyndis":  ([75.45, 10.95, 76.05, 11.40], "Tyndis: Kadalundi to Ponnani"),
    "indus":   ([67.00, 24.30, 67.85, 25.05], "Barbarikon: Indus delta and Gharo creek"),
    "aynuna":  ([35.00, 27.90, 35.45, 28.35], "Leukē Kōmē: Aynuna and the Gulf of Aqaba mouth"),
    "rufiji":  ([38.90, -8.30, 39.60, -7.60], "Rhapta: Rufiji delta and the Mafia channel"),
}

GRID = "https://www.gmrt.org/services/GridServer"


def fetch(name, bbox, layer="topo", resolution="max"):
    """One GMRT GeoTIFF, cached, since the service is slow and the grid is static."""
    CACHE.mkdir(parents=True, exist_ok=True)
    p = CACHE / f"{name}_{layer}.tif"
    if p.exists() and p.stat().st_size > 10000:
        return p
    q = (f"{GRID}?minlongitude={bbox[0]}&maxlongitude={bbox[2]}"
         f"&minlatitude={bbox[1]}&maxlatitude={bbox[3]}"
         f"&format=geotiff&resolution={resolution}&layer={layer}")
    with urllib.request.urlopen(q, timeout=300) as r:
        p.write_bytes(r.read())
    return p


def coverage(name, bbox):
    """Depth statistics for one box, and the fraction of it that is measured.

    Shallow water is reported separately because that is where the question
    lives. Whether a ship could approach a candidate depends on the bar, not on
    the depth four kilometres offshore, and a global compilation is least
    reliable exactly where the water is shallowest.
    """
    topo = rasterio.open(fetch(name, bbox, "topo")).read(1).astype("float32")
    mask = rasterio.open(fetch(name, bbox, "topo-mask")).read(1).astype("float32")

    sea = np.isfinite(topo) & (topo < 0)
    depth = -topo[sea]
    measured = np.isfinite(mask[sea])
    shallow = depth < 20

    return {
        "region": name,
        "cells": int(sea.sum()),
        "cell_m": round(float(rasterio.open(fetch(name, bbox, "topo")).res[0]) * 111320),
        "depth_p10": round(float(np.percentile(depth, 10)), 1) if sea.sum() else "",
        "depth_median": round(float(np.median(depth)), 1) if sea.sum() else "",
        "depth_p90": round(float(np.percentile(depth, 90)), 1) if sea.sum() else "",
        "measured_pct": round(float(measured.mean()) * 100, 1) if sea.sum() else "",
        "shallow_cells": int(shallow.sum()),
        "shallow_measured_pct": (round(float(measured[shallow].mean()) * 100, 1)
                                 if shallow.sum() else ""),
    }


# Two areas with dense multibeam, used to check that an empty mask means an
# empty mask rather than a misread layer. Both come back 100 per cent measured.
CONTROLS = {
    "monterey": [-122.10, 36.55, -121.75, 36.90],
    "hudson": [-73.95, 40.25, -73.55, 40.55],
}


def check_controls():
    for name, bbox in CONTROLS.items():
        r = coverage(name, bbox)
        print(f"  control {name:9s} measured {r['measured_pct']}%", flush=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, (bbox, note) in BOXES.items():
        r = coverage(name, bbox)
        r["note"] = note
        rows.append(r)
        print(f"  {name:9s} {r['cells']:>8} sea cells at {r['cell_m']} m | "
              f"median {r['depth_median']} m | measured {r['measured_pct']}% | "
              f"under 20 m measured {r['shallow_measured_pct']}%", flush=True)
    dest = OUT / "bathymetry_coverage.csv"
    with open(dest, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    print(f"\n-> {dest.name}\n")
    check_controls()


if __name__ == "__main__":
    main()
