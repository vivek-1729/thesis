"""Shared drawing pieces for the Periplus maps.

Kept in one place so the basin map and the two route maps cannot drift apart in
palette, label placement or how a sailing leg is decided.
"""
import json
from pathlib import Path

import matplotlib.patheffects as pe
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Ellipse

ROOT = Path(__file__).resolve().parent.parent
RAW, PROC, FIG = ROOT / "data/raw", ROOT / "data/processed", ROOT / "figures"

SURFACE, LAND, LAND_EDGE = "#fcfcfb", "#ebeae4", "#c3c2b7"
INK, INK_2, MUTED, HAIRLINE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
DISPUTED = "#eb6834"
# Validated ordinal ramp: one hue, monotone lightness, adjacent gaps >= 0.06.
TIER_COLOR = {"A": "#0d366b", "B": "#1c5cab", "C": "#2a78d6",
              "D": "#5598e7", "E": "#86b6ef"}
TIER_LABEL = {"A": "excavated / secure", "B": "identified, sources agree",
              "C": "proposed, single source", "D": "conflicted or placeholder",
              "E": "unlocated"}


def load_sites():
    """Gazetteer joined to the confidence tiers, with the tier letter split out."""
    g = (pd.read_csv(PROC / "gazetteer.csv")
         .merge(pd.read_csv(PROC / "site_confidence.csv")[
             ["toponym", "tier", "route_role", "km_to_coast", "in_brief_disputed"]],
             on="toponym"))
    g["tier_letter"] = g.tier.str[0]
    return g


def load_land(bbox, pad=5):
    t = (RAW / "ne_50m_land.js").read_text()
    out = []
    for f in json.loads(t[t.index("{"):])["features"]:
        geom = f.get("geometry")
        if not geom:
            continue
        polys = ([geom["coordinates"]] if geom["type"] == "Polygon"
                 else geom["coordinates"])
        for poly in polys:
            for ring in poly:
                xs, ys = [p[0] for p in ring], [p[1] for p in ring]
                if max(xs) < bbox[0] - pad or min(xs) > bbox[1] + pad:
                    continue
                if max(ys) < bbox[2] - pad or min(ys) > bbox[3] + pad:
                    continue
                out.append((xs, ys))
    return out


def draw_base(ax, bbox, lw=0.5):
    for xs, ys in load_land(bbox):
        ax.fill(xs, ys, facecolor=LAND, edgecolor=LAND_EDGE, linewidth=lw, zorder=1)
    ax.set_xlim(bbox[0], bbox[1])
    ax.set_ylim(bbox[2], bbox[3])
    ax.set_aspect(1.0)
    ax.set_facecolor(SURFACE)
    ax.grid(color=HAIRLINE, lw=0.6, zorder=0)
    ax.tick_params(colors=MUTED, labelsize=8.5)
    for s in ax.spines.values():
        s.set_color(LAND_EDGE)
        s.set_linewidth(0.8)


def sailing_chains(g, roles=("port of call",)):
    """Ordered ports along each itinerary.

    The text's chain threads through inland markets and landmarks in narrative
    order (Berenike -> Meroe -> Ptolemais Theron), but a ship sails straight from
    Berenike to Ptolemais Theron. So walk each chain and keep only what a ship
    calls at. A head is a port no SAME-ROUTE predecessor points at -- counting
    cross-route edges hides the whole eastern itinerary, because Rhapta (western)
    points at Leuke Kome (eastern).
    """
    nxt = {r.toponym: r.next_on_route for r in g.itertuples()}
    route = {r.toponym: r.route for r in g.itertuples()}
    role = {r.toponym: r.route_role for r in g.itertuples()}
    pos = {r.toponym: (r.lon, r.lat) for r in g.itertuples() if pd.notna(r.lat)}
    targets = {b for a, b in nxt.items()
               if isinstance(b, str) and route.get(a) == route.get(b)}
    chains = {}
    for head in [t for t in nxt if t not in targets]:
        chain, cur, seen = [], head, set()
        while cur and cur not in seen:
            seen.add(cur)
            if role.get(cur) in roles and cur in pos:
                chain.append(cur)
            nx = nxt.get(cur)
            cur = nx if isinstance(nx, str) and route.get(nx) == route.get(cur) else None
        if len(chain) > 1:
            chains[route.get(head)] = chain
    return chains, pos


def draw_legs(ax, chain, pos, lw=1.0):
    for a, b in zip(chain, chain[1:]):
        ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]],
                color=LAND_EDGE, lw=lw, alpha=0.9, zorder=2, solid_capstyle="round")


def draw_candidates(ax, ports, s=20):
    """Competing identifications from the literature, with a ring over their spread."""
    import math
    cand = pd.read_csv(RAW / "disputed_candidates.csv")
    cand = cand[cand.port.isin(ports)]
    for _, d in cand.groupby("port"):
        clat, clon = d.lat.mean(), d.lon.mean()
        r_km = max(math.hypot((x.lat - clat) * 110.57,
                              (x.lon - clon) * 111.32 * math.cos(math.radians(clat)))
                   for x in d.itertuples())
        ax.add_patch(Ellipse(
            (clon, clat), 2 * r_km / (111.32 * math.cos(math.radians(clat))),
            2 * r_km / 110.57, facecolor=DISPUTED, alpha=0.10, edgecolor=DISPUTED,
            lw=0.9, ls=(0, (4, 3)), zorder=2.5))
        ax.scatter(d.lon, d.lat, s=s, marker="o", c="none", edgecolors=DISPUTED,
                   linewidths=1.0, zorder=4.5)


def draw_sites(ax, g, size=68):
    for letter, color in TIER_COLOR.items():
        d = g[g.tier_letter == letter]
        if not d.empty:
            ax.scatter(d.lon, d.lat, s=size, c=color, marker="o",
                       edgecolors=SURFACE, linewidths=1.2, zorder=5)


def tier_legend(ax, g, **kw):
    n = g.tier_letter.value_counts()
    handles = [Line2D([], [], marker="o", ls="", ms=8, mfc=TIER_COLOR[k],
                      mec=SURFACE, mew=1.1, label=f"{k}  {TIER_LABEL[k]} ({n[k]})")
               for k in "ABCDE" if n.get(k, 0)]
    handles += [Line2D([], [], color=LAND_EDGE, lw=1.6, label="Sailing leg"),
                Line2D([], [], marker="o", ls="", ms=10, mfc=(0.92, 0.41, 0.20, 0.12),
                       mec=DISPUTED, mew=0.9, label="Spread of proposed locations")]
    leg = ax.legend(handles=handles, frameon=True, facecolor=SURFACE,
                    edgecolor=LAND_EDGE, labelcolor=INK, borderpad=0.9,
                    labelspacing=0.7, **kw)
    leg.get_frame().set_linewidth(0.8)
    leg.set_zorder(9)
    if leg.get_title():
        leg.get_title().set_color(INK_2)
    return leg


def place_labels(ax, fig, items, bbox, fs=7.0, rings=(0.9, 1.9, 3.0, 4.4, 6.2)):
    """Greedy declutter with leader lines; flagged sites get first pick of position."""
    bb = ax.get_position()
    xr, yr = ax.get_xlim()[1] - ax.get_xlim()[0], ax.get_ylim()[1] - ax.get_ylim()[0]
    px = xr / (bb.width * fig.get_size_inches()[0] * 72)
    py = yr / (bb.height * fig.get_size_inches()[1] * 72)
    dirs = [(1, 0, "left"), (-1, 0, "right"), (0.8, 0.8, "left"), (-0.8, 0.8, "right"),
            (0.8, -0.8, "left"), (-0.8, -0.8, "right"), (0, 1, "center"), (0, -1, "center")]
    placed = []
    for it in sorted(items, key=lambda r: (not r["key"], -r["lat"])):
        w, h = len(it["name"]) * fs * 0.58 * px, fs * 1.25 * py
        best = None
        for rad in rings:
            for dx, dy, ha in dirs:
                cx = it["lon"] + dx * (rad * 0.55 * (xr / 69) + w * 0.5)
                cy = it["lat"] + dy * (rad * 0.55 * (yr / 45) + h * 0.6)
                x0 = cx - (w / 2 if ha == "center" else (0 if ha == "left" else w))
                box = (x0, cy - h / 2, x0 + w, cy + h / 2)
                if not (bbox[0] < box[0] and box[2] < bbox[1]):
                    continue
                if not (bbox[2] < box[1] and box[3] < bbox[3]):
                    continue
                if any(box[0] < p[2] and box[2] > p[0]
                       and box[1] < p[3] and box[3] > p[1] for p in placed):
                    continue
                best = (cx, cy, ha, box, rad)
                break
            if best:
                break
        if not best:
            continue
        cx, cy, ha, box, rad = best
        placed.append(box)
        if rad > rings[0]:
            off = 0.25 * (xr / 69)
            ax.plot([it["lon"], cx - (off if ha == "left" else -off if ha == "right" else 0)],
                    [it["lat"], cy], color=MUTED, lw=0.45, alpha=0.8, zorder=4)
        ax.text(cx, cy, it["name"], fontsize=fs, ha=ha, va="center", zorder=6,
                color=INK if it["key"] else INK_2,
                fontweight="bold" if it["key"] else "normal",
                path_effects=[pe.withStroke(linewidth=2.4, foreground=SURFACE)])
