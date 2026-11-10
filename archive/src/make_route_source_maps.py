"""Where each source puts the disputed ports, by itinerary.

Numbered markers with a key, rather than labels placed on the map. With 19 competing
claims packed into 200 km of the Malabar coast, any label-placement scheme produces a
web of leader lines that reads as noise; a numbered key is unambiguous and quiet.

Modern dataset coordinates (Barchi/Pleiades, Copeland) are excluded. They are not
published identifications, just numbers in a file, and they added seven points and
seven labels without adding an argument. They stay in coordinates_table.md.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D

sys.path.insert(0, str(Path(__file__).resolve().parent))
import basemap as bm
import mapkit as mk

plt.rcParams.update({"font.family": ["Helvetica Neue", "Helvetica", "DejaVu Sans"]})
SURFACE = "#fcfcfb"
SOURCES = [("Casson 1989", "#2a78d6"),
           ("Schoff 1912 / McCrindle 1885", "#eb6834"),
           ("Other scholarship", "#1baf7a")]
COLOR = dict(SOURCES)


def family(src):
    if src.startswith("Casson 1989"): return "Casson 1989"
    if src.startswith(("Schoff", "McCrindle", "Cunningham")): return "Schoff 1912 / McCrindle 1885"
    return "Other scholarship"


def load():
    d = pd.read_csv(mk.ROOT / "data/raw/positional_assertions.csv")
    d = d[d.lat.notna()
          & ~d.source.str.startswith("Ptolemy")
          & ~d.source.str.contains("Barchi|Copeland")].copy()
    d["fam"] = d.source.map(family)
    d["name"] = d.place_or_relation.fillna("\u2014")
    # One marker per PLACE, not per claim. Casson and Schoff both naming Ponnani is
    # one candidate with two backers -- and their agreement is itself information.
    rows = []
    for (port, name), g in d.groupby(["port", "name"], sort=False):
        fams = list(dict.fromkeys(g.fam))
        lead = next((f for f, _ in SOURCES if f in fams), fams[0])
        rows.append({"port": port, "name": name, "lat": g.lat.iloc[0], "lon": g.lon.iloc[0],
                     "fam": lead, "backers": len(fams),
                     "preferred": bool(g.verdict.isin(["preferred", "secure"]).any()),
                     "who": " · ".join(f.split()[0] for f in fams)})
    return pd.DataFrame(rows)


def fit_bbox(sub, slot_ratio, pad=0.6, floor=0.8):
    """A bbox that renders at exactly the panel's width:height ratio.

    basemap.draw sets aspect = 1/cos(lat), so displayed h/w = lat_span*aspect/lon_span.
    Solving for lon_span keeps every panel the same physical size.
    """
    import math
    clat = (sub.lat.min() + sub.lat.max()) / 2
    clon = (sub.lon.min() + sub.lon.max()) / 2
    lat_span = max(sub.lat.max() - sub.lat.min(), floor) * (1 + pad)
    aspect = 1 / math.cos(math.radians(clat))
    lon_span = lat_span * aspect * slot_ratio
    need = (sub.lon.max() - sub.lon.min()) * 1.5
    if need > lon_span:
        lon_span = need
        lat_span = lon_span / (aspect * slot_ratio)
    return (clon - lon_span/2, clon + lon_span/2, clat - lat_span/2, clat + lat_span/2)


def draw_numbered(ax, sub):
    """Numbered north-to-south, so the key reads down the coast."""
    sub = sub.sort_values("lat", ascending=False).reset_index(drop=True)
    for i, r in enumerate(sub.itertuples(), 1):
        if r.backers > 1:     # a second ring marks agreement between sources
            ax.scatter([r.lon], [r.lat], s=430, c="none", edgecolors=COLOR[r.fam],
                       linewidths=1.5, zorder=5)
        ax.scatter([r.lon], [r.lat], s=250, c=COLOR[r.fam], edgecolors=SURFACE,
                   linewidths=1.7, zorder=6)
        ax.text(r.lon, r.lat, str(i), fontsize=7.6, color="white", ha="center",
                va="center", zorder=7, fontweight="bold")
    return sub


def key_text(sub, per_line=1):
    lines = []
    for i, r in enumerate(sub.itertuples(), 1):
        mark = "★ " if r.preferred else ""
        lines.append(f"{i}.  {mark}{r.name}")
    return lines


def draw_key(fig, ax, sub, y0, fs=8.3):
    """Key beneath the panel, coloured by source, starred where the edition prefers it."""
    box = ax.get_position()
    x = box.x0
    dy = 0.030
    for i, r in enumerate(sub.itertuples(), 1):
        star = "★ " if r.preferred else ""
        fig.text(x, y0 - i * dy, f"{i}", fontsize=fs, color=COLOR[r.fam],
                 fontweight="bold", ha="left", va="top")
        fig.text(x + 0.0125, y0 - i * dy, f"{star}{r.name}", fontsize=fs,
                 color=bm.INK_2, ha="left", va="top")
        fig.text(x + 0.0125, y0 - i * dy - 0.0118, r.who, fontsize=fs - 1.5,
                 color=bm.MUTED, ha="left", va="top")


def legend(fig, anchor, ncol=3):
    h = [Line2D([], [], marker="o", ls="", ms=10, mfc=c, mec=SURFACE, mew=1.6, label=n)
         for n, c in SOURCES]
    h.append(Line2D([], [], marker="$★$", ls="", ms=9, color=bm.INK_2,
                    label="the standard edition's preferred reading"))
    lg = fig.legend(handles=h, loc="upper right", frameon=False, ncol=ncol, fontsize=9.4,
                    bbox_to_anchor=anchor, labelcolor=bm.INK, columnspacing=1.8,
                    handletextpad=0.7)
    lg.set_zorder(10)


def west(d):
    sub = d[d.port.isin(["Rhapta", "Menuthias"])]
    FIGW, FIGH = 11.0, 9.6
    AX = [0.045, 0.085, 0.52, 0.745]          # map on the left, key beside it
    fig = plt.figure(figsize=(FIGW, FIGH), facecolor=SURFACE)
    ax = fig.add_axes(AX)
    bbox = fit_bbox(sub, (AX[2] * FIGW) / (AX[3] * FIGH), pad=0.18)
    bm.draw(ax, bbox)
    ordered = draw_numbered(ax, sub)
    bm.scalebar(ax, bbox, x_frac=0.06, y_frac=0.035)
    # key to the right of the map, so seven entries always fit
    x = AX[0] + AX[2] + 0.055
    y0 = AX[1] + AX[3] - 0.03
    for i, r in enumerate(ordered.itertuples(), 1):
        star = "\u2605 " if r.preferred else ""
        fig.text(x, y0 - (i - 1) * 0.072, str(i), fontsize=9.5, color=COLOR[r.fam],
                 fontweight="bold", ha="left", va="top")
        fig.text(x + 0.022, y0 - (i - 1) * 0.072, f"{star}{r.name}", fontsize=9.5,
                 color=bm.INK, ha="left", va="top")
        fig.text(x + 0.022, y0 - (i - 1) * 0.072 - 0.026, r.who, fontsize=8.2,
                 color=bm.MUTED, ha="left", va="top")
    legend(fig, (0.965, 0.905), ncol=2)
    fig.text(0.045, 0.982, "Western route — Rhapta", fontsize=18, color=bm.INK, va="top")
    fig.text(0.045, 0.950,
             "The only disputed port on the African itinerary. Casson's two readings are conditional on\n"
             "which island Menuthias was: Pemba gives a Rhapta near Dar es Salaam, Zanzibar gives the\n"
             "Rufiji delta. Menuthias is itself unlocated, so the sailing constraint starts from an unknown.",
             fontsize=9.6, color=bm.INK_2, va="top", linespacing=1.55)
    out = mk.FIG / "06_route_west_rhapta.png"
    fig.savefig(out, dpi=200, facecolor=SURFACE); plt.close(fig); return out


def east(d):
    PANELS = [("Leukē Kōmē", ["Leuke Kome"], "no perennial rivers — a sheltered bay"),
              ("Barbarikon & Minnagar", ["Barbarikon", "Minnagar"],
               "on the middle of seven Indus mouths"),
              ("Tyndis & Muziris", ["Tyndis", "Muziris"],
               "Tyndis 500 stadia north of Muziris"),
              ("Nelkynda & Bakarē", ["Nelkynda", "Bakare"],
               "Nelkynda 120 stadia up Bakarē's river")]
    FIGW, FIGH = 15.5, 10.4
    L, R, T, B, WS = 0.025, 0.975, 0.755, 0.335, 0.055
    pw = (R - L) * FIGW / (4 + 3*WS)
    ratio = pw / ((T - B) * FIGH)
    fig = plt.figure(figsize=(FIGW, FIGH), facecolor=SURFACE)
    gs = fig.add_gridspec(1, 4, wspace=WS, left=L, right=R, top=T, bottom=B)
    for i, (name, ports, note) in enumerate(PANELS):
        sub = d[d.port.isin(ports)]
        ax = fig.add_subplot(gs[0, i])
        bbox = fit_bbox(sub, ratio, pad=0.45)
        bm.draw(ax, bbox)
        ordered = draw_numbered(ax, sub)
        bm.scalebar(ax, bbox)
        ax.set_title(f"{name}   ·   {len(sub)}", fontsize=11.5, color=bm.INK,
                     loc="left", pad=15)
        ax.text(0, 1.014, note, transform=ax.transAxes, fontsize=8.3, color=bm.INK_2,
                va="bottom", ha="left")
        draw_key(fig, ax, ordered, B - 0.028, fs=8.2)
    legend(fig, (0.975, 0.888), ncol=4)
    fig.text(0.025, 0.984, "Eastern route — the five disputed ports",
             fontsize=18, color=bm.INK, va="top")
    fig.text(0.025, 0.952,
             "One marker per proposed place, numbered north to south; a double ring means more than one source names it.\n"
             "Muziris and the Malabar ports share panels because the text fixes them relative to one another.",
             fontsize=9.6, color=bm.INK_2, va="top", linespacing=1.55)
    out = mk.FIG / "07_route_east_sources.png"
    fig.savefig(out, dpi=200, facecolor=SURFACE); plt.close(fig); return out


if __name__ == "__main__":
    d = load()
    print(f"{len(d)} published claims mapped (dataset coordinates excluded)")
    print("wrote", west(d))
    print("wrote", east(d))
