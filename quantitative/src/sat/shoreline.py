"""Shoreline position at several dates, with an honest error band on each.

Three satellite epochs that need no georeferencing: Landsat MSS 1972-76 at 79 m,
which is before the Thanneermukkom barrage and the Idukki dam; the JRC record
1984-2021 at 30 m; and Sentinel-2 at 10 m for the present. The historic charts
slot into the same machinery later as two earlier epochs, once georeferenced.

The method is the standard one in coastal change studies. Extract the land-water
boundary, attach a positional uncertainty, cast transects perpendicular to the
coast, and measure where each shoreline crosses each transect. Change is claimed
only where two bands fail to overlap, which separates real movement from the
error in locating the line.
"""

import numpy as np
from scipy import ndimage


def open_sea(water, side="west"):
    """Just the sea, not the backwaters behind the barrier.

    The three epochs define "water" differently: a frequency over 11 Landsat
    scenes, a percentage over 37 years of JRC, and a threshold on one Sentinel-2
    composite. Inside the lagoon those definitions disagree badly, and comparing
    them produced a spurious 290 m shift. On the open coast they agree, because
    the Arabian Sea is water under any definition. So the comparison is
    restricted to the connected body of water touching the seaward edge.
    """
    lab, n = ndimage.label(water)
    if n == 0:
        return water
    edge = lab[:, 0] if side == "west" else lab[:, -1]
    ids = [i for i in np.unique(edge) if i != 0]
    if not ids:
        return water
    keep = max(ids, key=lambda i: (lab == i).sum())
    return lab == keep


def boundary(water, smooth=1):
    """The land-water boundary as a boolean mask, one pixel wide."""
    w = ndimage.binary_closing(water, iterations=smooth)
    w = ndimage.binary_opening(w, iterations=smooth)
    return w & ~ndimage.binary_erosion(w)


def positional_error(pixel_m, extraction_px=0.5, registration_m=None):
    """Total positional uncertainty of an extracted shoreline, in metres.

    Three terms added in quadrature, which is the convention in the shoreline
    change literature:

      pixel size          the line can only be located to within a pixel
      extraction          where inside that pixel the threshold falls
      georegistration     how well the image sits on the ground

    Sentinel-2 and Landsat are already orthorectified to well under a pixel, so
    registration defaults to a third of a pixel. A scanned chart would carry a
    much larger term here, which is why the charts will widen their own band
    rather than borrowing this one.
    """
    reg = registration_m if registration_m is not None else pixel_m / 3.0
    return float(np.sqrt(pixel_m ** 2 + (extraction_px * pixel_m) ** 2 + reg ** 2))


def shore_column(sea, row):
    """Column index where the sea ends and land begins, on one raster row.

    The Malabar coast runs roughly north to south with the Arabian Sea to the
    west, so a per-row measurement is a clean cross-shore transect and needs no
    gradient estimate. Returns None where the row never leaves the sea or never
    reaches it, which happens at a river mouth and has to be dropped rather than
    guessed at.
    """
    r = sea[row]
    if not r.any() or r.all():
        return None
    idx = np.flatnonzero(r)
    last = idx.max()                      # easternmost sea pixel on this row
    if last >= len(r) - 1:
        return None                       # sea runs off the far edge; not a coast
    return float(last)


def compare(epochs, native_m, grid_m, step=4):
    """Shoreline position per epoch, measured on every `step`-th raster row.

    All epochs are resampled onto one common grid, so position converts from
    column to metres using `grid_m`, the size of a cell on that grid. The
    sensors' native resolutions in `native_m` enter only through the positional
    uncertainty, since a shoreline drawn from 79 m Landsat is locatable far less
    precisely than one from 10 m Sentinel-2 even after both are resampled.

    Using native resolution for the position itself was an earlier bug and
    produced apparent shifts of ten kilometres.
    """
    labels = list(epochs)
    h = epochs[labels[0]].shape[0]
    err = {k: positional_error(native_m[k]) for k in labels}
    rows = []
    for row in range(0, h, step):
        rec = {"row": row}
        for k in labels:
            x = shore_column(epochs[k], row)
            if x is None:
                rec = None
                break
            rec[k] = x * grid_m
        if rec:
            rows.append(rec)
    return rows, err


def _unused_coast_transects(water, n=40, length_px=60, smooth=9):
    """Points along the coast with an outward normal at each.

    The normal comes from the gradient of a heavily smoothed water mask, which
    gives a stable direction even where the coastline is ragged at pixel scale.
    """
    w = ndimage.gaussian_filter(water.astype("float32"), smooth)
    gy, gx = np.gradient(w)
    edge = np.argwhere(boundary(water))
    if len(edge) < n:
        return []
    # walk the boundary in order of along-shore position so transects are spread
    order = np.argsort(edge[:, 0] * 1.0 + edge[:, 1] * 0.0)
    picks = edge[order][:: max(1, len(edge) // n)][:n]

    out = []
    for r, c in picks:
        dy, dx = gy[r, c], gx[r, c]
        mag = np.hypot(dy, dx)
        if mag < 1e-6:
            continue
        out.append(((int(r), int(c)), (dy / mag, dx / mag), length_px))
    return out


def crossing(water, origin, normal, length_px):
    """Where along a transect the shoreline sits, in pixels from the origin.

    Walks outward from the origin and returns the first step at which the mask
    stops being water. Returns None if the transect never leaves water or never
    enters it, which happens at river mouths and has to be dropped rather than
    guessed at.
    """
    r0, c0 = origin
    dy, dx = normal
    h, w = water.shape
    prev = None
    for k in range(length_px):
        r = int(round(r0 + dy * (k - length_px / 2)))
        c = int(round(c0 + dx * (k - length_px / 2)))
        if not (0 <= r < h and 0 <= c < w):
            return None
        cur = bool(water[r, c])
        if prev is not None and cur != prev:
            return k - length_px / 2
        prev = cur
    return None


def significant(a, b, err_a, err_b, k=1.0):
    """Has the shoreline moved, beyond the two uncertainty bands?

    The bands overlap when the measured difference is smaller than the combined
    uncertainty, and in that case no movement can be claimed. k=1 uses one
    standard error on each side, which is the convention in this literature.
    """
    return abs(a - b) > k * np.sqrt(err_a ** 2 + err_b ** 2)
