"""Georeference an Admiralty chart from its own printed graticule.

The usual way to georeference a historic map is to match features on it against
a modern map and fit a transform through the pairs. That works and it imports
every error in your feature matching into the result.

An Admiralty chart does not need it. The sheet carries a printed latitude and
longitude graticule, graduated to the minute, drawn by the people who surveyed
it. Reading that graticule gives a transform from the chart's own stated
coordinates, and the only error is in locating a printed line to the pixel.

Sheet 749 of 1857 states its own frame: West Coast of India, Malabar Coast,
from 11 degrees 2 minutes to 9 degrees 50 minutes north latitude, surveyed by
Lieutenant W. B. Selby of the Indian Navy between 1851 and 1853, longitude east
from Greenwich. The bottom border is labelled 30, 35, 75 degrees 40, and 45
minutes, so the sheet spans roughly 75 and a half to 76 and a quarter degrees
east.

Projection. Admiralty charts of this period are Mercator, in which longitude is
linear in x and latitude is linear in the Mercator ordinate rather than in
degrees. Over the 72 minutes of latitude on this sheet the difference between
the two is small but it is not nothing, so the fit is done properly and the
residual of a linear fit is reported alongside, as a check on which is right.
"""
import math

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None


def mercator_y(lat_deg):
    """Mercator ordinate for a latitude in degrees, unit Earth radius."""
    phi = math.radians(lat_deg)
    return math.log(math.tan(math.pi / 4 + phi / 2))


def inverse_mercator_y(y):
    return math.degrees(2 * math.atan(math.exp(y)) - math.pi / 2)


def neatline(gray, search=1400):
    """The inner frame of the chart, as (top, bottom, left, right) in pixels.

    Found as the rows and columns carrying the most ink near each edge. The
    sheet has a heavy outer border and a finer inner neatline; the graticule is
    graduated against the inner one, which is the second strongest line in from
    each edge.
    """
    dark = gray < 110
    rows, cols = dark.sum(1), dark.sum(0)
    H, W = gray.shape

    def pick(v, lo, hi, want_second_from_edge, edge_at_low):
        seg = [(int(v[i]), i) for i in range(lo, hi)]
        seg.sort(reverse=True)
        keep = []
        for val, i in seg:
            if val < 0.2 * max(v):
                break
            if not any(abs(i - j) < 40 for _, j in keep):
                keep.append((val, i))
            if len(keep) >= 4:
                break
        idx = sorted(i for _, i in keep)
        if not idx:
            return None
        return idx[1] if (want_second_from_edge and len(idx) > 1 and edge_at_low) else (
            idx[-2] if (want_second_from_edge and len(idx) > 1) else idx[0])

    return (pick(rows, 150, search, True, True),
            pick(rows, H - search, H, True, False),
            pick(cols, 150, search, True, True),
            pick(cols, W - search, W, True, False))


def latitude_ticks(gray, top, bottom, left, band=46, min_ink=30):
    """Major graticule ticks on the left border, as pixel rows.

    On sheet 749 these fall every twenty minutes of latitude.
    """
    strip = gray[top:bottom, left + 4:left + band]
    d = strip < 120
    prof = d.sum(1)
    on = prof >= min_ink
    runs, s = [], None
    for i, v in enumerate(on):
        if v and s is None:
            s = i
        if not v and s is not None:
            runs.append((s, i - 1)); s = None
    if s is not None:
        runs.append((s, len(on) - 1))
    mids = [(a + b) / 2 + top for a, b in runs if b - a <= 12]
    # drop anything within a hundred pixels of the frame, which is the corner
    return [m for m in mids if m - top > 100 and bottom - m > 100]


def scale_blocks(gray, left, right, bar_row, half=6, min_width=40):
    """Boundaries of the alternating minute blocks on a graduated border.

    The border scale is printed as hatched and open blocks of one minute each,
    so every block edge is a minute mark. Returns the edges in pixels.
    """
    bar = gray[bar_row - half:bar_row + half + 1, left:right]
    prof = (bar < 140).mean(0)
    k = 9
    sm = np.convolve(prof, np.ones(k) / k, mode="same")
    on = sm > 0.45
    runs, s = [], None
    for i, v in enumerate(on):
        if v and s is None:
            s = i
        if not v and s is not None:
            runs.append((s, i - 1)); s = None
    if s is not None:
        runs.append((s, len(on) - 1))
    runs = [r for r in runs if r[1] - r[0] > min_width]
    return [(a + left, b + left) for a, b in runs]


def fit_latitude(tick_rows, tick_lats):
    """Pixel row to latitude, fitted on the Mercator ordinate.

    Returns the two transforms and the residual of each, so the choice between
    them is made on evidence rather than on the assumption that the chart is
    exactly Mercator.
    """
    y = np.asarray(tick_rows, dtype="float64")
    merc = np.array([mercator_y(v) for v in tick_lats])
    lin = np.array(tick_lats, dtype="float64")

    a_m, b_m = np.polyfit(y, merc, 1)
    a_l, b_l = np.polyfit(y, lin, 1)
    res_m = merc - (a_m * y + b_m)
    res_l = lin - (a_l * y + b_l)
    # residual expressed in minutes of latitude for comparability
    scale = 1.0 / abs(a_m) if a_m else 1.0
    return {
        "mercator": (a_m, b_m),
        "linear": (a_l, b_l),
        "rms_mercator_min": float(np.sqrt((res_m ** 2).mean()) * 60 * scale / scale),
        "rms_linear_min": float(np.sqrt((res_l ** 2).mean()) * 60),
    }
