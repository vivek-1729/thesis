"""The chain of distances the Periplus gives along the Malabar coast.

Tyndis lies 500 stadia before Muziris and Nelkynda 500 stadia after it; Bakare
is 120 stadia downriver from Nelkynda. Each port is therefore fixed relative to
the one before, and the constraints chain.

Every arc is a band, not a line, because the stadion is not a fixed quantity.
Casson's own identifications imply 144 m on the Tyndis leg and 204 m on the
Nelkynda leg, so that range is used as the width of each band. The width is the
point: it shows how little the distances actually constrain.
"""
import csv, math, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe

import basemap as bm

ROOT = pathlib.Path(__file__).resolve().parents[1]
BLUE, MUZ, ARC, INK, INK2 = "#2a78d6", "#1baf7a", "#c2703c", bm.INK, bm.INK_2
LO, HI = 0.144, 0.204            # km per stadion, from Casson's own table

def main():
    S = {r["site_key"]: r for r in csv.DictReader(open(ROOT / "data/raw/site_aliases.csv"))}
    P = lambda k: (float(S[k]["lat"]), float(S[k]["lon"]))
    anchor = P("pattanam")

    bbox = (74.3, 77.6, 8.2, 12.2)
    aspect = 1 / math.cos(math.radians((bbox[2] + bbox[3]) / 2))
    W = 11.0
    H = W * (bbox[3] - bbox[2]) * aspect / (bbox[1] - bbox[0])
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    bm.draw(ax, bbox, river_lw=(0.5, 2.6))

    kmlat = 110.57
    kmlon = 111.32 * math.cos(math.radians(anchor[0]))

    def band(centre, st, th0, th1, colour, label=None, lab_ang=None):
        """An annulus sector at `st` stadia from `centre`, in km-true degrees."""
        r0, r1 = st * LO, st * HI
        for r, alpha in ((r0, 1.0), (r1, 1.0)):
            th = [math.radians(t) for t in range(int(th0), int(th1) + 1)]
            ax.plot([centre[1] + (r / kmlon) * math.cos(t) for t in th],
                    [centre[0] + (r / kmlat) * math.sin(t) for t in th],
                    color=colour, lw=1.3, alpha=0.85, zorder=6)
        th = [math.radians(t) for t in range(int(th0), int(th1) + 1)]
        xs = [centre[1] + (r0 / kmlon) * math.cos(t) for t in th] + \
             [centre[1] + (r1 / kmlon) * math.cos(t) for t in reversed(th)]
        ys = [centre[0] + (r0 / kmlat) * math.sin(t) for t in th] + \
             [centre[0] + (r1 / kmlat) * math.sin(t) for t in reversed(th)]
        ax.fill(xs, ys, color=colour, alpha=0.11, lw=0, zorder=5)
        if label:
            t = math.radians(lab_ang)
            rm = (r0 + r1) / 2
            ax.text(centre[1] + (rm / kmlon) * math.cos(t),
                    centre[0] + (rm / kmlat) * math.sin(t),
                    label, fontsize=9.4, color=colour, ha="center", va="center",
                    style="italic", zorder=9, rotation=0,
                    path_effects=[pe.withStroke(linewidth=3.2, foreground="white")])

    # 500 stadia north of Muziris, and 500 south
    band(anchor, 500, 40, 140, ARC, "500 stadia to Tyndis", 96)
    band(anchor, 500, 210, 320, ARC, "500 stadia to Nelkynda", 238)
    # 120 stadia from each Nelkynda candidate, where Bakare should lie
    for k in ["niranam", "kottayam_kerala", "kollam", "neendakara"]:
        band(P(k), 120, 0, 359, MUZ)

    def mark(k, colour, label, dx, dy, ha, small=False):
        la, lo = P(k)
        ax.plot(lo, la, "o", ms=6.5 if small else 8.5, mfc=colour, mec="white",
                mew=1.5, zorder=11)
        ax.text(lo + dx, la + dy, label, fontsize=9.6 if small else 11.2,
                color=INK if not small else INK2, ha=ha, va="center", zorder=12,
                path_effects=[pe.withStroke(linewidth=3.0, foreground="white")])

    mark("pattanam", MUZ, "Pattanam", 0.07, 0.00, "left")
    mark("kodungallur", MUZ, "Kodungallur", 0.07, 0.07, "left")
    for k, nm in [("ponnani", "Ponnani"), ("tanur", "Tanur"),
                  ("kadalundi", "Kadalundi"), ("koyilandy", "Koyilandy")]:
        mark(k, BLUE, nm, -0.07, 0, "right", small=True)
    for k, nm, dx, dy in [("niranam", "Niranam", 0.08, 0.0),
                          ("kottayam_kerala", "Kottayam", 0.08, 0.0),
                          ("kollam", "Kollam", -0.08, -0.09),
                          ("neendakara", "Neendakara", 0.08, 0.05)]:
        mark(k, BLUE, nm, dx, dy, "left" if dx > 0 else "right", small=True)
    for k, nm, dx, dy in [("purakkad", "Purakkad", -0.08, -0.06),
                          ("kallada", "Kallada", 0.09, 0.07),
                          ("thevalakara", "Thevalakara", -0.09, 0.05)]:
        mark(k, "#eb6834", nm, dx, dy, "left" if dx > 0 else "right", small=True)

    ax.text(0.022, 0.972, "The Periplus distances along the Malabar coast",
            transform=ax.transAxes, fontsize=16.5, color=INK, ha="left", va="top",
            path_effects=[pe.withStroke(linewidth=4, foreground="white")])
    ax.text(0.022, 0.928,
            "Each band is 500 or 120 stadia, drawn between 144 and 204 m per stadion,\n"
            "the range implied by Casson's own identifications.",
            transform=ax.transAxes, fontsize=9.6, color=INK2, ha="left", va="top",
            path_effects=[pe.withStroke(linewidth=3.4, foreground="white")])

    handles = [
        Line2D([], [], marker="o", ls="", ms=8, mfc=MUZ, mec="white",
               label="Muziris, the anchor for both distances"),
        Line2D([], [], marker="o", ls="", ms=7, mfc=BLUE, mec="white",
               label="candidates for Tyndis and Nelkynda"),
        Line2D([], [], marker="o", ls="", ms=7, mfc="#eb6834", mec="white",
               label="candidates for Bakarē"),
        Line2D([], [], color=ARC, lw=1.3, label="500 stadia from Muziris"),
        Line2D([], [], color=MUZ, lw=1.3, label="120 stadia from each Nelkynda candidate"),
    ]
    ax.legend(handles=handles, loc="lower left", frameon=False, fontsize=8.8,
              handletextpad=0.8, labelspacing=0.5, bbox_to_anchor=(0.018, 0.02))
    bm.scalebar(ax, bbox, km=50, x_frac=0.60, y_frac=0.045)

    out = ROOT / "figures" / "08_malabar_distance_bands.png"
    fig.savefig(out, dpi=200, facecolor="white")
    print(f"-> {out.name}")

if __name__ == "__main__":
    main()
