"""Extract the navigable water network drawn on an 1857 Admiralty sheet.

Why this is worth doing. Findings section 4.5 calls measuring the Malabar
distances through the backwaters the single most consequential unfinished
measurement in the project, because the Periplus gives them "by river and sea"
and every measurement ever made, ours included, used a straight line. Section 12
records four independent methods failing to recover that network from satellite
imagery, because the Kuttanad polder system has re-cut the surface into features
that mimic palaeochannels.

The 1857 survey predates the reclamation, the Thanneermukkom barrage and the
Idukki dam, so it draws the network before the engineering that defeats the
satellites. Between sheets 749 and 750 it covers 98.8 per cent of the modern
backwater, the gap being a strip of the northern Vembanad east of sheet 749.

How the sheet distinguishes water from land, which took one wrong attempt to
establish. It does not tint either. Both land and sea are blank paper, and the
first approach here, separating stippled land from blank water by local texture,
called 74 per cent of a tile water because there was no texture difference to
find.

What the sheet actually draws is the *banks*. A waterway appears as a pair of
roughly parallel lines with blank paper between them. So the linework partitions
the blank space into regions, and a channel is a region that is long and thin
while a field or an island is a blob. That is the discriminator used here:
label the blank regions, measure elongation, keep the ribbons.

One practical trap. The inset harbour plans, Alleppey Road and Quilon Road on
sheet 750, are drawn in otherwise empty parts of the sheet and therefore sit on
top of geography they have nothing to do with. They have to be masked out by
pixel box before any of this runs, or Quilon's breakers appear in the middle of
the Kuttanad.
"""
import numpy as np
from scipy import ndimage


def ink_fraction(gray, radius=9, ink_below=150):
    """Local fraction of inked pixels, the texture measure that separates
    stippled land from blank water."""
    ink = (gray < ink_below).astype("float32")
    k = 2 * radius + 1
    return ndimage.uniform_filter(ink, size=k)


def elongation(mask):
    """Ratio of the principal axes of a blob. A reach scores high, a pond low."""
    ys, xs = np.nonzero(mask)
    if len(ys) < 8:
        return 0.0
    pts = np.column_stack([ys - ys.mean(), xs - xs.mean()]).astype("float64")
    ev = np.linalg.eigvalsh(pts.T @ pts / len(pts))
    return float(np.sqrt(ev[1] / max(ev[0], 1e-9)))


def channels(gray, ink_below=150, close_px=5, min_area=1500,
             min_elong=2.5, max_area_frac=0.25):
    """Waterways, as the elongated regions the bank lines enclose.

    `max_area_frac` drops any region covering more than a quarter of the tile,
    which is the open sea or the undrawn interior rather than a channel.
    """
    ink = gray < ink_below
    ink = ndimage.binary_closing(ink, np.ones((close_px, close_px)))
    blank = ~ink
    lab, n = ndimage.label(blank)
    out = np.zeros_like(blank)
    kept = []
    total = blank.size
    for i in range(1, n + 1):
        m = lab == i
        a = int(m.sum())
        if a < min_area or a > max_area_frac * total:
            continue
        e = elongation(m)
        if e < min_elong:
            continue
        out |= m
        kept.append((a, e))
    return out, kept


def water_mask(gray, radius=9, ink_below=150, max_ink=0.055,
               close_px=7, min_area=4000):
    """Blank areas of the sheet, which are water.

    `max_ink` is the share of inked pixels a neighbourhood may carry and still
    be called water. Stipple runs far above it and blank paper far below, so the
    threshold sits in a wide gap rather than on a knife edge.

    Soundings and names leave holes in the mask; closing fills them. Small
    isolated patches are dropped, since a true waterway on this coast is large
    and connected.
    """
    f = ink_fraction(gray, radius, ink_below)
    m = f < max_ink
    m = ndimage.binary_closing(m, np.ones((close_px, close_px)))
    lab, n = ndimage.label(m)
    if n:
        sizes = ndimage.sum(m, lab, range(1, n + 1))
        keep = np.isin(lab, 1 + np.flatnonzero(sizes >= min_area))
        m = keep
    return m, f


def separate_sea(mask, from_side="west"):
    """Split the water into the open sea and everything behind the coast.

    The sea is the component touching the seaward edge of the frame. What is
    left is the backwater, which is the part the Periplus distances run through.
    """
    lab, n = ndimage.label(mask)
    if n == 0:
        return mask, mask
    edge = lab[:, 0] if from_side == "west" else lab[:, -1]
    ids = [i for i in np.unique(edge) if i]
    if not ids:
        return np.zeros_like(mask), mask
    sea_id = max(ids, key=lambda i: (lab == i).sum())
    sea = lab == sea_id
    return sea, mask & ~sea
