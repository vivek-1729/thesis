"""Two outputs from the positional-assertions table.

  1. data/processed/coordinates_table.md -- every located claim, by port, with a one
     line summary of what that source actually says.
  2. figures/05_coordinates_by_source.png -- the same claims mapped, one panel per
     port, coloured by who is making the claim.

Ptolemy's coordinates are deliberately kept OUT of the map. They are given in his
own frame, measured from the Fortunate Isles and systematically distorted, so
plotting them on a modern basemap would be meaningless until they are rectified.
They appear in the table instead, flagged as his own degrees.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mapkit as mk

plt.rcParams.update({"font.family": ["Helvetica Neue", "Helvetica", "DejaVu Sans"]})

# Validated categorical slots 1-3, plus muted ink for the gazetteers, which are
# derivative rather than an independent scholarly claim.
SRC_COLOR = {"Casson 1989": "#2a78d6", "Schoff / McCrindle": "#eb6834",
             "Other scholarship": "#1baf7a", "Gazetteer": mk.MUTED}
PORTS = ["Leuke Kome", "Barbarikon", "Rhapta", "Tyndis", "Nelkynda", "Bakare"]


def square_bbox(sub, pad=0.45, floor=0.9):
    """A square window around one port's claims.

    Degrees of longitude shrink with latitude, so the window is widened by
    1/cos(lat) to keep the panels visually square and mutually comparable.
    """
    import math
    clat, clon = (sub.lat.min() + sub.lat.max()) / 2, (sub.lon.min() + sub.lon.max()) / 2
    half = max(sub.lat.max() - sub.lat.min(),
               (sub.lon.max() - sub.lon.min()) * math.cos(math.radians(clat)),
               floor) / 2 * (1 + pad)
    wlon = half / max(math.cos(math.radians(clat)), 0.2)
    return (clon - wlon, clon + wlon, clat - half, clat + half)


def family(src):
    if src.startswith("Casson 1989"):
        return "Casson 1989"
    if src.startswith(("Schoff", "McCrindle", "Cunningham")):
        return "Schoff / McCrindle"
    if "Barchi" in src or "Copeland" in src:
        return "Gazetteer"
    return "Other scholarship"


def build_table(d, context):
    out = ["# The disputed ports: state of the question", "",
           "For each port, the proposals on record and the coordinates each source gives.",
           "",
           "Ptolemy's figures are reproduced as he gives them, in his own frame — longitudes",
           "reckoned from the Fortunate Isles, latitudes systematically compressed — and are",
           "marked °P. They are not commensurable with the modern coordinates in the same",
           "columns. On the Indian coast his longitudes correlate closely with the true values",
           "(r = 0.97, residual c. 77 km), while his latitudes do not (r = 0.48, residual",
           "c. 470 km): he assigns Mouziris, Podouke and Kolkhoi latitudes of 14–15° where the",
           "true figures are 10.2°, 11.9° and 8.6°.", ""]
    for port in ["Leuke Kome", "Barbarikon", "Rhapta", "Tyndis", "Muziris",
                 "Nelkynda", "Bakare", "Menuthias", "Minnagar"]:
        sub = d[d.port == port]
        if sub.empty:
            continue
        out += [f"## {port}", "", context.get(port, "").strip(), "",
                "| source | places it at | lat | lon |", "|---|---|---|---|"]
        for r in sub.itertuples():
            ptol = str(r.source).startswith("Ptolemy")
            if pd.isna(r.lat):
                lat = lon = "—"
            elif ptol:
                lat, lon = f"{r.lat:.2f}°P", f"{r.lon:.2f}°P"
            else:
                lat, lon = f"{r.lat:.3f}", f"{r.lon:.3f}"
            place = str(r.place_or_relation) if pd.notna(r.place_or_relation) else "—"
            if place.strip() in ("-", ""):   # gazetteer rows carry no place-name
                place = "*(its own coordinate)*"
            if pd.notna(r.value):        # a stated distance, not a point
                place = f"{place} — **{int(r.value)} {r.unit}**"
            out.append(f"| {r.source} | {place} | {lat} | {lon} |")
        out.append("")
    return "\n".join(out)


def build_map(d):
    pts = d[d.lat.notna() & ~d.source.str.startswith("Ptolemy")].copy()
    pts["family"] = pts.source.map(family)
    fig = plt.figure(figsize=(15, 9.6), facecolor=mk.SURFACE)
    gs = fig.add_gridspec(2, 3, hspace=0.30, wspace=0.22,
                          left=0.04, right=0.985, top=0.855, bottom=0.075)
    for ax_i, port in enumerate(PORTS):
        sub = pts[pts.port == port]
        bbox = square_bbox(sub)
        ax = fig.add_subplot(gs[ax_i // 3, ax_i % 3])
        mk.draw_base(ax, bbox, lw=0.8)
        for fam, color in SRC_COLOR.items():
            f = sub[sub.family == fam]
            if f.empty:
                continue
            ax.scatter(f.lon, f.lat, s=95, c=color, edgecolors=mk.SURFACE,
                       linewidths=1.5, zorder=5,
                       marker="X" if fam == "Gazetteer" else "o")
        def label(r):
            p = r.place_or_relation
            if pd.isna(p) or str(p).strip() in ("-", ""):
                return "Barchi gazetteer" if "Barchi" in r.source else "Copeland model"
            return str(p)
        mk.place_labels(ax, fig, [{"name": label(r), "lon": r.lon, "lat": r.lat,
                                   "key": r.verdict in ("preferred", "secure")}
                                  for r in sub.itertuples()],
                        bbox, fs=7.2, rings=(0.9, 1.9, 3.2, 4.8))
        ax.set_title(f"{port}   ·   {len(sub)} located claims", fontsize=10.5,
                     color=mk.INK, loc="left", pad=6)
        ax.tick_params(labelsize=7)
    handles = [Line2D([], [], marker="X" if k == "Gazetteer" else "o", ls="", ms=9,
                      mfc=v, mec=mk.SURFACE, mew=1.4, label=k)
               for k, v in SRC_COLOR.items()]
    leg = fig.legend(handles=handles, loc="upper right", frameon=False, ncol=4,
                     fontsize=10, bbox_to_anchor=(0.985, 0.915), labelcolor=mk.INK,
                     columnspacing=2.0, handletextpad=0.7)
    leg.set_zorder(9)
    fig.text(0.04, 0.972, "Where each source puts the disputed ports",
             fontsize=17.5, color=mk.INK, va="top")
    fig.text(0.04, 0.936,
             "Every located claim from the ancient editions, the modern scholarship and the two digital gazetteers. "
             "Bold labels are the reading each port's\nstandard edition prefers. Ptolemy is omitted: his coordinates "
             "are in his own distorted frame and cannot be plotted until rectified.",
             fontsize=9.5, color=mk.INK_2, va="top", linespacing=1.5)
    out = mk.FIG / "05_coordinates_by_source.png"
    fig.savefig(out, dpi=190, facecolor=mk.SURFACE)
    return out


def main():
    d = pd.read_csv(mk.ROOT / "data/raw/positional_assertions.csv")
    raw = (mk.ROOT / "data/raw/port_context.md").read_text()
    context = {b.split("\n", 1)[0].strip(): b.split("\n", 1)[1]
               for b in raw.split("## ") if "\n" in b}
    t = mk.PROC / "coordinates_table.md"
    t.write_text(build_table(d, context))
    print("wrote", t)
    print("wrote", build_map(d))


if __name__ == "__main__":
    main()
