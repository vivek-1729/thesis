"""A quieter, more legible basemap than the 50m land polygons.

Rivers are not decoration on this project: the Periplus fixes Nelkynda 120 stadia up
a river whose mouth is Bakare, Muziris on the Periyar, and Barbarikon on one of seven
Indus mouths. A map of these ports without its rivers hides the evidence.

Uses Natural Earth 10m via pyshp, so no GDAL/geopandas dependency.
"""
import json
import math
from functools import lru_cache
from pathlib import Path

import shapefile
from matplotlib.collections import LineCollection, PolyCollection

NE = Path(__file__).resolve().parent.parent / "data/raw/ne10m"
RIVERS = Path(__file__).resolve().parent.parent / "data/processed/rivers_cache.json"

# Muted so the claim markers carry all the saturation on the page.
OCEAN, LAND = "#e9eef1", "#f7f5f0"
COAST, RIVER, LAKE = "#b4c2ca", "#9fb9c8", "#dde6ec"
INK, INK_2, MUTED = "#0b0b0b", "#52514e", "#8b8a85"


@lru_cache(maxsize=8)
def _read(name):
    """Shapes plus a couple of attributes, cached — each file is ~2-3 MB."""
    r = shapefile.Reader(str(NE / name))
    fields = [f[0] for f in r.fields[1:]]
    out = []
    for sr in r.shapeRecords():
        rec = dict(zip(fields, sr.record))
        out.append((sr.shape.points, list(sr.shape.parts), rec))
    return out


def _clip(pts, parts, bbox, pad=0.5):
    """Split a shape into its parts and keep those touching the window."""
    x0, x1, y0, y1 = bbox[0] - pad, bbox[1] + pad, bbox[2] - pad, bbox[3] + pad
    parts = list(parts) + [len(pts)]
    for a, b in zip(parts, parts[1:]):
        seg = pts[a:b]
        if len(seg) < 2:
            continue
        xs = [p[0] for p in seg]
        ys = [p[1] for p in seg]
        if max(xs) < x0 or min(xs) > x1 or max(ys) < y0 or min(ys) > y1:
            continue
        yield seg


@lru_cache(maxsize=1)
def _rivers():
    """HydroRIVERS reaches, pre-clipped to the study windows (see prep_rivers.py).

    Natural Earth 10m is far too coarse here — it carries three river features for the
    whole of Kerala and none of them is the Periyar.
    """
    return json.loads(RIVERS.read_text()) if RIVERS.exists() else {}


def _draw_rivers(ax, bbox, lw=(0.45, 2.3)):
    segs, widths = [], []
    for reaches in _rivers().values():
        for rr in reaches:
            pts = rr["p"]
            xs = [q[0] for q in pts]; ys = [q[1] for q in pts]
            if max(xs) < bbox[0] or min(xs) > bbox[1]: continue
            if max(ys) < bbox[2] or min(ys) > bbox[3]: continue
            # width on discharge, which reads better than Strahler order
            t = min(math.log10(rr["f"] + 1) / 2.6, 1.0)
            segs.append(pts); widths.append(lw[0] + (lw[1] - lw[0]) * t)
    if segs:
        ax.add_collection(LineCollection(segs, colors=RIVER, linewidths=widths,
                                         zorder=4, capstyle="round"))
    return len(segs)


def draw(ax, bbox, rivers=True, lakes=True, river_lw=(0.5, 1.6)):
    ax.set_facecolor(LAND)                     # land is the background; sea is drawn on top
    ocean = [s for pts, parts, _ in _read("ne_10m_ocean.shp")
             for s in _clip(pts, parts, bbox)]
    ax.add_collection(PolyCollection(ocean, facecolors=OCEAN, edgecolors="none", zorder=1))
    if lakes:
        lk = [s for pts, parts, _ in _read("ne_10m_lakes.shp")
              for s in _clip(pts, parts, bbox)]
        ax.add_collection(PolyCollection(lk, facecolors=LAKE, edgecolors=COAST,
                                         linewidths=0.4, zorder=2))
    cl = [s for pts, parts, _ in _read("ne_10m_coastline.shp")
          for s in _clip(pts, parts, bbox)]
    ax.add_collection(LineCollection(cl, colors=COAST, linewidths=0.9, zorder=3))
    if rivers:
        _draw_rivers(ax, bbox)
    ax.set_xlim(bbox[0], bbox[1]); ax.set_ylim(bbox[2], bbox[3])
    ax.set_aspect(1 / math.cos(math.radians((bbox[2] + bbox[3]) / 2)))
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])


def scalebar(ax, bbox, km=None, y_frac=0.055, x_frac=0.055):
    """A plain bar, since the axes carry no graticule."""
    lon_km = 111.32 * math.cos(math.radians((bbox[2] + bbox[3]) / 2))
    width = bbox[1] - bbox[0]
    if km is None:
        raw = width * lon_km / 4
        km = next((c for c in (5, 10, 20, 25, 50, 100, 200, 250, 500) if c >= raw), 500)
    dx = km / lon_km
    x = bbox[0] + width * x_frac
    y = bbox[2] + (bbox[3] - bbox[2]) * y_frac
    ax.plot([x, x + dx], [y, y], color=INK_2, lw=2.2, solid_capstyle="butt", zorder=9)
    ax.text(x + dx / 2, y + (bbox[3] - bbox[2]) * 0.016, f"{km} km", fontsize=7.4,
            color=INK_2, ha="center", va="bottom", zorder=9)
