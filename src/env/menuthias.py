"""The 300-stadia Menuthias notice, measured rather than quoted.

The Periplus puts Menuthias "about three hundred stadia from the mainland". Two
islands are in contention: Pemba and Unguja, the latter usually called Zanzibar.
Datoo (1970) argues for Pemba partly on this figure, reporting the channels as
30 and 22.5 statute miles at their narrowest against 300 stadia of "c. 34.5
miles". His 34.5 miles is 300 x 185.2 m, the conventional stadion, which this
project has found to be an artefact of the ancient rule of thumb rather than a
measurement: ten stades to a nautical mile, so 1852/10.

Our own calibration from legs with secure endpoints gives about 155 m, so the
notice is worth re-measuring on both figures. The channel widths are taken from
the GMRT grid rather than from Datoo, since his are quoted without a source and
a strait is easy to measure.
"""
import math, pathlib, urllib.request

import numpy as np
import rasterio
from scipy import ndimage
from pyproj import Geod

ROOT = pathlib.Path(__file__).resolve().parents[2]
CACHE = ROOT / "data" / "cache" / "bathymetry"
GEOD = Geod(ellps="WGS84")

BOX = (38.70, -6.70, 40.10, -4.70)        # Pemba and Unguja with their channels
STADIA = 300
STADION = {"this project, from secure legs": 155.0,
           "conventional, 1852/10": 185.2}

# The islands are identified as connected land components rather than by
# coordinates, because a row-by-row walk across the channel measures the gap to
# the nearest mangrove islet instead of to the island, and the Pemba and
# Zanzibar channels are full of them. A first attempt that way returned 0.1 km.
ISLANDS = {
    "Pemba": (39.56, 39.88, -5.49, -4.89),
    "Unguja (Zanzibar)": (39.18, 39.58, -6.48, -5.72),
}


def grid():
    """The GMRT tile covering both channels, cached."""
    CACHE.mkdir(parents=True, exist_ok=True)
    p = CACHE / "menuthias_topo.tif"
    if not p.exists():
        q = ("https://www.gmrt.org/services/GridServer?"
             f"minlongitude={BOX[0]}&maxlongitude={BOX[2]}"
             f"&minlatitude={BOX[1]}&maxlatitude={BOX[3]}"
             "&format=geotiff&resolution=max&layer=topo")
        with urllib.request.urlopen(q, timeout=300) as r:
            p.write_bytes(r.read())
    return p


def components():
    """Land as labelled components, with the grid's coordinate axes."""
    with rasterio.open(grid()) as s:
        a = s.read(1).astype("float32")
        t = s.transform
    land = np.isfinite(a) & (a >= 0)
    lab, n = ndimage.label(land)
    rows, cols = a.shape
    xs = t.c + (np.arange(cols) + 0.5) * t.a
    ys = t.f + (np.arange(rows) + 0.5) * t.e
    return lab, n, xs, ys


def pick(lab, n, xs, ys, bbox=None):
    """The largest component, or the largest inside a bounding box."""
    best, best_size = None, 0
    for i in range(1, n + 1):
        m = lab == i
        size = int(m.sum())
        if size < 1000 or size <= best_size:
            continue
        if bbox:
            yy, xx = np.nonzero(m)
            if not (bbox[0] <= xs[xx].min() and xs[xx].max() <= bbox[1]
                    and bbox[2] <= ys[yy].min() and ys[yy].max() <= bbox[3]):
                continue
        best, best_size = i, size
    return best


def min_gap(lab, a_id, b_id, xs, ys):
    """Shortest water distance between two land components, in km.

    Compares the two coastlines rather than every pixel, since only boundary
    pixels can be closest, and that is what makes this cheap enough to run.
    """
    out = []
    for cid in (a_id, b_id):
        m = lab == cid
        edge = m & ~ndimage.binary_erosion(m)
        yy, xx = np.nonzero(edge)
        out.append((xs[xx], ys[yy]))
    (ax, ay), (bx, by) = out
    best = (1e9, None, None)
    # Chunked so the pairwise distance never materialises in full.
    for k in range(0, len(ax), 2000):
        axc, ayc = ax[k:k + 2000], ay[k:k + 2000]
        dlon = (bx[None, :] - axc[:, None]) * np.cos(np.radians(ayc[:, None])) * 111.32
        dlat = (by[None, :] - ayc[:, None]) * 110.57
        d = np.hypot(dlon, dlat)
        i, j = np.unravel_index(np.argmin(d), d.shape)
        if d[i, j] < best[0]:
            best = (float(d[i, j]), (float(axc[i]), float(ayc[i])),
                    (float(bx[j]), float(by[j])))
    # Re-measure the winning pair on the ellipsoid.
    _, _, m = GEOD.inv(best[1][0], best[1][1], best[2][0], best[2][1])
    return m / 1000.0, best[1], best[2]


def main():
    print(f"{STADIA} stadia is\n")
    for name, m in STADION.items():
        km = STADIA * m / 1000
        print(f"   {km:6.1f} km  ({km/1.609:5.1f} statute miles)   {name}, {m:.1f} m")

    print("\nNarrowest channel, measured between coastlines on the GMRT grid\n")
    lab, n, xs, ys = components()
    mainland = pick(lab, n, xs, ys)
    res = {}
    for island, bbox in ISLANDS.items():
        iid = pick(lab, n, xs, ys, bbox)
        if iid is None:
            print(f"   {island:20s} not resolved")
            continue
        km, pa, pb = min_gap(lab, mainland, iid, xs, ys)
        res[island] = km
        print(f"   {island:20s} {km:5.1f} km  ({km/1.609:4.1f} miles)"
              f"   mainland {pa[1]:.2f} S to island {pb[1]:.2f} S")

    print("\nHow each stadion reads the notice\n")
    print(f"   {'island':20s} " + "  ".join(f"{n.split(',')[0]:>22s}" for n in STADION))
    for island, km in res.items():
        cells = []
        for name, m in STADION.items():
            pred = STADIA * m / 1000
            cells.append(f"{pred/km:>6.0%} of measured{'':>4s}")
        print(f"   {island:20s} " + "  ".join(cells))
    print("\n   A figure near 100 per cent means the notice fits that island on that stadion.")


if __name__ == "__main__":
    main()
