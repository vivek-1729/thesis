"""Shoreline position at three satellite epochs, for every port, with error bands.

The question each port asks is whether its coast has moved since anyone could
measure it, because a candidate's distance from the sea is only meaningful
against a shoreline that has stayed put. Three epochs need no georeferencing and
between them span half a century: Landsat MSS 1972 to 1976 at 79 m, which is
before the Idukki dam and the Thanneermukkom barrage; the JRC record 1984 to
2021 at 30 m; and Sentinel-2 for the present at 10 m.

Change is claimed only where two error bands fail to overlap. The band is the
pixel size, the extraction uncertainty and the georegistration added in
quadrature, which is the convention in the shoreline-change literature, and it
is what separates a real movement from the difficulty of saying where a line is.

The charts were meant to join this as two earlier epochs and cannot yet, for a
reason worth recording. Sheet 749 distinguishes sea from land by covering the
sea in sounding figures and leaving the land blank, so the coast can be found as
the eastern edge of the sounding field. Measured that way it is locatable to
about three kilometres, because the answer moves 266 pixels when the density
threshold moves from 0.02 to 0.05. The satellite epochs here resolve tens of
metres. A hand trace off the georeferenced sheet would sit at the
georeferencing accuracy of about twenty metres and would belong in this table;
an automatic one at three kilometres does not.
"""
import csv, json, pathlib, sys

import numpy as np
from scipy import ndimage

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from sat import landsat_mss as mss, shoreline, stack, water  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parents[2] / "data" / "processed" / "sat"

MSS, GSW, S2 = "MSS 1972-76", "JRC 1984-2021", "Sentinel-2 2022-24"
NATIVE = {MSS: 79.0, GSW: 30.0, S2: 10.0}

# Coastal strips, narrow in longitude so every raster row crosses the shore
# once. A box that reaches far inland picks up the backwaters and the per-row
# transect stops meaning anything.
REGIONS = {
    "Muziris, Periyar":    [76.10, 10.05, 76.30, 10.35],
    "Nelkynda, Pamba":     [76.25, 9.20, 76.45, 9.55],
    "Tyndis, Ponnani":     [75.75, 10.70, 75.95, 11.00],
    "Barbarikon, Indus":   [67.30, 24.60, 67.60, 24.90],
    "Rhapta, Rufiji":      [39.15, -8.10, 39.40, -7.80],
}


def epochs_for(name, bbox):
    """The three water masks, all on the JRC grid so columns are comparable."""
    out = {}
    try:
        freq, _ = mss.water_extent(bbox, name.split(",")[0].lower().strip())
        out[MSS] = freq > 0.6
    except Exception as exc:
        print(f"     {MSS}: {type(exc).__name__}: {str(exc)[:70]}")
    shape = out[MSS].shape if MSS in out else None
    gsw = water.surface_water(bbox, shape=shape, layers=("occurrence",))
    out[GSW] = gsw["occurrence"] > 60
    shape = shape or out[GSW].shape
    try:
        comp = stack.cached_composite(f"{name.split(',')[0].lower()}_shore",
                                      bbox, "2022-01-01", "2024-12-31", "dry")
        green, nir = comp["B03"].astype("f4"), comp["B08"].astype("f4")
        ndwi = (green - nir) / np.maximum(green + nir, 1e-6)
        w = ndwi > 0.0
        if w.shape != shape:
            ys = np.linspace(0, w.shape[0] - 1, shape[0]).astype(int)
            xs = np.linspace(0, w.shape[1] - 1, shape[1]).astype(int)
            w = w[np.ix_(ys, xs)]
        out[S2] = w
    except Exception as exc:
        print(f"     {S2}: {type(exc).__name__}: {str(exc)[:70]}")
    return {k: v for k, v in out.items() if v is not None}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows, summary = [], []
    for name, bbox in REGIONS.items():
        print(f"\n=== {name}")
        try:
            masks = epochs_for(name, bbox)
        except Exception as exc:
            print(f"   failed: {type(exc).__name__}: {str(exc)[:90]}")
            continue
        if len(masks) < 2:
            print("   fewer than two epochs; nothing to compare")
            continue

        # Which side the sea is on. The Indus delta faces south and west, the
        # rest of these face west, but open_sea only needs the side that is
        # certainly ocean, so west is right for all of them.
        sea = {k: shoreline.open_sea(v, "west") for k, v in masks.items()}
        H, W = next(iter(masks.values())).shape
        mid = 0.5 * (bbox[1] + bbox[3])
        grid_m = (bbox[2] - bbox[0]) * 111320 * np.cos(np.radians(mid)) / W
        recs, err = shoreline.compare(sea, {k: NATIVE[k] for k in masks},
                                      grid_m, step=4)
        print(f"   {len(recs)} transects, grid {grid_m:.1f} m/px, "
              f"bands " + ", ".join(f"{k} +-{err[k]:.0f} m" for k in masks))
        if not recs:
            continue

        keys = [k for k in (MSS, GSW, S2) if k in masks]
        for a, b in zip(keys, keys[1:]):
            shift = np.array([r[b] - r[a] for r in recs])
            band = float(np.hypot(err[a], err[b]))
            sig = np.abs(shift) > band
            summary.append(dict(
                region=name, earlier=a, later=b, transects=len(shift),
                band_m=round(band, 1),
                median_shift_m=round(float(np.median(shift)), 1),
                mean_shift_m=round(float(shift.mean()), 1),
                significant=int(sig.sum()),
                significant_pct=round(100 * float(sig.mean()), 1),
                seaward=int((shift[sig] < 0).sum()),
                landward=int((shift[sig] > 0).sum())))
            print(f"   {a} -> {b}: median {np.median(shift):+7.1f} m, "
                  f"band +-{band:.0f} m, {100*sig.mean():4.1f}% of transects "
                  f"move more than the band "
                  f"({(shift[sig]<0).sum()} seaward, {(shift[sig]>0).sum()} landward)")

        for r in recs:
            rows.append(dict(region=name, row=r["row"],
                             lat=round(bbox[3] - (r["row"] / H) * (bbox[3] - bbox[1]), 5),
                             **{k: round(r[k], 1) for k in keys}))

    with open(OUT / "shoreline_transects.csv", "w", newline="") as fh:
        fields = ["region", "row", "lat", MSS, GSW, S2]
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)
    with open(OUT / "shoreline_change.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(summary[0]))
        w.writeheader(); w.writerows(summary)
    print(f"\n{len(rows)} transects, {len(summary)} comparisons -> {OUT}")


if __name__ == "__main__":
    main()
