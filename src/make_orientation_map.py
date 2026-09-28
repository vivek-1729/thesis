"""Orientation map, keyed to what we actually know rather than to a 6/6 split.

Two encodings, deliberately orthogonal:
  colour  = how well the site is located (ordinal ramp, dark = secure)
  shape   = what a ship does there (calls / never goes / steers by)

Route lines connect ports of call only. The Periplus names places the ship never
visits -- ch. 51 says goods reach Barygaza from Paithana and Tagara "by wagons and
through great tracts without roads" -- so drawing those as sailing legs would be
wrong. Sites whose coordinates are gazetteer placeholders are marked as unknown
rather than plotted as if located.
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Ellipse

ROOT = Path(__file__).resolve().parent.parent
RAW, PROC, FIG = ROOT / "data/raw", ROOT / "data/processed", ROOT / "figures"

SURFACE, LAND, LAND_EDGE = "#fcfcfb", "#ebeae4", "#c3c2b7"
INK, INK_2, MUTED, HAIRLINE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
DISPUTED = "#eb6834"
# Validated ordinal ramp (single hue, monotone lightness, gaps >= 0.06)
TIER_COLOR = {"A": "#0d366b", "B": "#1c5cab", "C": "#2a78d6",
              "D": "#5598e7", "E": "#86b6ef"}
ROLE_MARKER = {"port of call": "o", "inland supply centre": "^",
               "landmark": "s", "position unknown": "X"}
BASIN, FS = (26, 95, -11.5, 33), 7.0

# This figure is the sailing picture, so it shows only what a ship encounters.
# Inland supply centres reached overland by wagon, and sites no source actually
# locates, are dropped from the VIEW -- they stay in the dataset, because inland
# centres still constrain their port from landward (Minnagar sits upriver from
# Barbarikon; Ozene, Paithana and Tagara feed Barygaza).
SHOW_ROLES = ("port of call",)
plt.rcParams.update({"font.family": ["Helvetica Neue", "Helvetica", "DejaVu Sans"]})


def load_land():
    t = (RAW / "ne_50m_land.js").read_text()
    out = []
    for f in json.loads(t[t.index("{"):])["features"]:
        g = f.get("geometry")
        if not g:
            continue
        for poly in ([g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]):
            for ring in poly:
                xs, ys = [p[0] for p in ring], [p[1] for p in ring]
                if max(xs) < BASIN[0] - 5 or min(xs) > BASIN[1] + 5: continue
                if max(ys) < BASIN[2] - 5 or min(ys) > BASIN[3] + 5: continue
                out.append((xs, ys))
    return out


def place_labels(ax, fig, items, fs=FS):
    """Greedy declutter with leader lines; contested sites get first pick."""
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
        for rad in (0.9, 1.9, 3.0, 4.4, 6.2):
            for dx, dy, ha in dirs:
                cx = it["lon"] + dx * (rad * 0.55 + w * 0.5)
                cy = it["lat"] + dy * (rad * 0.55 + h * 0.6)
                x0 = cx - (w / 2 if ha == "center" else (0 if ha == "left" else w))
                box = (x0, cy - h / 2, x0 + w, cy + h / 2)
                if not (BASIN[0] < box[0] and box[2] < BASIN[1]): continue
                if not (BASIN[2] < box[1] and box[3] < BASIN[3]): continue
                if any(box[0] < p[2] and box[2] > p[0] and box[1] < p[3] and box[3] > p[1]
                       for p in placed): continue
                best = (cx, cy, ha, box, rad); break
            if best: break
        if not best:
            continue
        cx, cy, ha, box, rad = best
        placed.append(box)
        if rad > 1.0:
            ax.plot([it["lon"], cx - (0.25 if ha == "left" else -0.25 if ha == "right" else 0)],
                    [it["lat"], cy], color=MUTED, lw=0.45, alpha=0.8, zorder=4)
        ax.text(cx, cy, it["name"], fontsize=fs, ha=ha, va="center", zorder=6,
                color=INK if it["key"] else INK_2,
                fontweight="bold" if it["key"] else "normal",
                path_effects=[pe.withStroke(linewidth=2.4, foreground=SURFACE)])


def main():
    FIG.mkdir(exist_ok=True)
    g = (pd.read_csv(PROC / "gazetteer.csv")
         .merge(pd.read_csv(PROC / "site_confidence.csv")[
             ["toponym", "tier", "route_role", "km_to_coast", "in_brief_disputed"]],
             on="toponym"))
    dropped = g[~g.route_role.isin(SHOW_ROLES)]
    g = g[g.route_role.isin(SHOW_ROLES)].copy()
    g["tier_letter"] = g.tier.str[0]

    fig = plt.figure(figsize=(17, 11.4), facecolor=SURFACE)
    ax = fig.add_axes([0.035, 0.045, 0.95, 0.835])
    for xs, ys in load_land():
        ax.fill(xs, ys, facecolor=LAND, edgecolor=LAND_EDGE, linewidth=0.5, zorder=1)
    ax.set_xlim(BASIN[0], BASIN[1]); ax.set_ylim(BASIN[2], BASIN[3])
    ax.set_aspect(1.0); ax.set_facecolor(SURFACE)
    ax.grid(color=HAIRLINE, lw=0.6, zorder=0)
    ax.tick_params(colors=MUTED, labelsize=8.5)
    ax.set_xlabel("longitude °E", fontsize=9, color=MUTED)
    ax.set_ylabel("latitude °", fontsize=9, color=MUTED)
    for s in ax.spines.values():
        s.set_color(LAND_EDGE); s.set_linewidth(0.8)

    # --- sailing legs: ports of call only, bridging across everything else -----
    # The text's chain runs through inland markets and landmarks in narrative order
    # (Berenike -> Meroe -> Ptolemais Theron). A ship sails Berenike -> Ptolemais
    # Theron. So walk each route's chain, drop the non-ports, and join what remains.
    pos = {r.toponym: (r.lon, r.lat) for r in g.itertuples() if pd.notna(r.lat)}
    role = {r.toponym: r.route_role for r in g.itertuples()}
    nxt = {r.toponym: r.next_on_route for r in g.itertuples()}
    route = {r.toponym: r.route for r in g.itertuples()}
    # A chain head is a site no SAME-ROUTE predecessor points at. Counting
    # cross-route edges here hides the entire eastern itinerary, because Rhapta
    # (western) points at Leukē Kōmē (eastern) and so disqualifies it as a head.
    targets = {b for a, b in nxt.items()
               if isinstance(b, str) and route.get(a) == route.get(b)}
    legs = []
    for start in [t for t in nxt if t not in targets]:      # heads of each chain
        chain, cur, seen = [], start, set()
        while cur and cur not in seen:
            seen.add(cur)
            if role.get(cur) == "port of call" and cur in pos:
                chain.append(cur)
            nx = nxt.get(cur)
            cur = nx if nx and route.get(nx) == route.get(cur) else None
        legs += list(zip(chain, chain[1:]))
    for a, b in legs:
        ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], color=LAND_EDGE,
                lw=0.9, alpha=0.9, zorder=2, solid_capstyle="round")

    # --- candidate spread for the six named in the brief ---------------------
    import math
    cand = pd.read_csv(RAW / "disputed_candidates.csv")
    for port, d in cand.groupby("port"):
        clat, clon = d.lat.mean(), d.lon.mean()
        r_km = max(math.hypot((x.lat - clat) * 110.57,
                              (x.lon - clon) * 111.32 * math.cos(math.radians(clat)))
                   for x in d.itertuples())
        ax.add_patch(Ellipse((clon, clat),
                             2 * r_km / (111.32 * math.cos(math.radians(clat))),
                             2 * r_km / 110.57, facecolor=DISPUTED, alpha=0.10,
                             edgecolor=DISPUTED, lw=0.9, ls=(0, (4, 3)), zorder=2.5))
        ax.scatter(d.lon, d.lat, s=18, marker="o", c="none", edgecolors=DISPUTED,
                   linewidths=1.0, zorder=4.5)

    for role_name, marker in ROLE_MARKER.items():
        for letter, color in TIER_COLOR.items():
            d = g[(g.route_role == role_name) & (g.tier_letter == letter)]
            if d.empty:
                continue
            ax.scatter(d.lon, d.lat, s=62 if marker != "X" else 46, marker=marker,
                       c=color, edgecolors=SURFACE, linewidths=1.1, zorder=5,
                       alpha=0.55 if marker == "X" else 1.0)

    place_labels(ax, fig, [{"name": r.toponym, "lon": r.lon, "lat": r.lat,
                            "key": bool(r.in_brief_disputed) or r.tier_letter == "A"}
                           for r in g.itertuples() if pd.notna(r.lat)])

    n = g.tier_letter.value_counts()
    tier_h = [Line2D([], [], marker="o", ls="", ms=8, mfc=TIER_COLOR[k], mec=SURFACE,
                     mew=1.1, label=lab)
              for k, lab in [("A", f"A  excavated / secure ({n.get('A',0)})"),
                             ("B", f"B  identified, sources agree ({n.get('B',0)})"),
                             ("C", f"C  proposed, single source ({n.get('C',0)})"),
                             ("D", f"D  conflicted or placeholder ({n.get('D',0)})"),
                             ("E", f"E  unlocated ({n.get('E',0)})")]
              if n.get(k, 0)]   # a tier with nothing in this view earns no legend row
    role_h = [Line2D([], [], color=LAND_EDGE, lw=1.6, label="Sailing leg given by the text"),
               Line2D([], [], marker="o", ls="", ms=10, mfc=(0.92, 0.41, 0.20, 0.12),
                      mec=DISPUTED, mew=0.9, label="Spread of proposed locations")]
    l1 = ax.legend(handles=tier_h, loc="lower right", frameon=True, fontsize=9,
                   title="How well located", labelcolor=INK, facecolor=SURFACE,
                   edgecolor=LAND_EDGE, borderpad=0.9, labelspacing=0.7,
                   bbox_to_anchor=(0.999, 0.02))
    l1.get_title().set_color(INK_2); l1.get_frame().set_linewidth(0.8); l1.set_zorder(9)
    ax.add_artist(l1)
    l2 = ax.legend(handles=role_h, loc="lower left", frameon=True, fontsize=9,
                   title="On the route", labelcolor=INK, facecolor=SURFACE,
                   edgecolor=LAND_EDGE, borderpad=0.9, labelspacing=0.7,
                   bbox_to_anchor=(0.30, 0.02))
    l2.get_title().set_color(INK_2); l2.get_frame().set_linewidth(0.8); l2.set_zorder(9)

    fig.text(0.035, 0.972, "The sailing world of the Periplus Maris Erythraei",
             fontsize=17.5, color=INK, va="top")
    fig.text(0.035, 0.936,
             f"The {len(g)} ports a ship called at, c. 50 AD, in the order the text gives. "
             "Colour grades how securely each one is located.",
             fontsize=10.5, color=INK_2, va="top")
    fig.text(0.035, 0.906,
             f"{int((g.tier_letter=='A').sum())} rest on an excavated identification — far more than the six the project began with. "
             f"Not shown: {int((dropped.route_role=='inland supply centre').sum())} inland supply centres reached overland by wagon, "
             f"{int((dropped.route_role=='landmark').sum())} landmarks with no trade attributed, and "
             f"{int((dropped.route_role=='position unknown').sum())} sites no source locates.\n"
             "Orange rings show the spread of competing identifications for the six ports originally targeted.\n"
             "Tiers: data/processed/site_confidence.csv · candidates: data/raw/disputed_candidates.csv",
             fontsize=8.5, color=MUTED, va="top", linespacing=1.5)

    out = FIG / "01_orientation_map.png"
    fig.savefig(out, dpi=190, facecolor=SURFACE)
    print("wrote", out)


if __name__ == "__main__":
    main()
