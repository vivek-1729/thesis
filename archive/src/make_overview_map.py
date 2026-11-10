"""The six disputed ports, drawn with their uncertainty and the arcs that constrain them.

Each port is a numbered mark with a circle enclosing every location proposed
for it, so the figure carries the width of the disagreement rather than
asserting a point. The arcs are the distances the Periplus gives, drawn as
bands because the stadion is not a fixed quantity: Casson's own identifications
imply 144 m on one leg and 204 m on another, so every arc is a range.
"""
import csv, math, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.patheffects as pe

import basemap as bm

ROOT = pathlib.Path(__file__).resolve().parents[1]
BLUE, GREY, ARC = "#2a78d6", "#8a9097", "#c2703c"
MUZ = "#1baf7a"     # Muziris: the anchor the Malabar distances are measured from
INK, INK2 = bm.INK, bm.INK_2

PORTS = [
    ("Leukē Kōmē", ["aynuna", "al_wajh", "al_qusayr_arabia"],
     ["Aynuna", "Al-Wajh", "Al-Qusayr"], (3.4, 1.2, "left")),
    ("Barbarikon", ["banbhore"], ["Banbhore"], (0.6, 2.4, "left")),
    ("Tyndis", ["ponnani", "tanur", "kadalundi", "koyilandy"],
     ["Ponnani", "Tanur", "Kadalundi", "Koyilandy"], (-3.2, 5.4, "right")),
    ("Nelkynda", ["niranam", "kottayam_kerala", "kollam", "neendakara"],
     ["Niranam", "Kottayam", "Kollam", "Neendakara"], (-3.4, -3.4, "right")),
    ("Bakarē", ["purakkad", "kallada", "thevalakara"],
     ["Purakkad", "Kallada", "Thevalakara"], (-3.2, -9.0, "right")),
    ("Muziris", ["pattanam", "kodungallur"],
     ["Pattanam", "Kodungallur"], (-3.6, 0.9, "right")),
    ("Rhapta", ["rufiji", "mafia", "pangani", "dar_es_salaam",
                "unguja_ukuu", "fukuchani"],
     ["Rufiji delta", "Mafia", "Pangani", "Dar es Salaam",
      "Unguja Ukuu", "Fukuchani"], (2.8, 3.4, "left")),
]
EXTRA = {"Barbarikon": [(24.86, 67.01), (24.924, 69.022)]}

ANCHORS = [("berenike", "Berenikē", -0.7, 0, "right"),
           ("myos_hormos", "Myos Hormos", 0.8, -1.3, "left"),
           ("adulis", "Adulis", -0.7, 0, "right"),
           ("qana", "Kanē", 0, -1.1, "center"),
           ("sumhuram", "Moscha Limēn", 0.7, 0.3, "left"),
           ("socotra", "Dioskouridēs", 0, -1.2, "center"),
           ("barygaza", "Barygaza", 0.8, 0.3, "left"),
           ("arikamedu", "Poduke", 0.8, -0.6, "left")]


def ring(ax, lat, lon, km_r, **kw):
    la = km_r / 110.57
    lo = km_r / (111.32 * math.cos(math.radians(lat)))
    th = [i * math.pi / 180 for i in range(0, 361, 2)]
    ax.plot([lon + lo * math.cos(t) for t in th],
            [lat + la * math.sin(t) for t in th], **kw)

def main():
    S = {r["site_key"]: r for r in csv.DictReader(open(ROOT / "data/raw/site_aliases.csv"))}
    bbox = (29.0, 82.5, -11.0, 31.8)
    # basemap.draw sets aspect = 1/cos(mid-lat), so the figure must match the
    # window or matplotlib leaves white bands down either side.
    aspect = 1 / math.cos(math.radians((bbox[2] + bbox[3]) / 2))
    W = 16.0
    H = W * (bbox[3] - bbox[2]) * aspect / (bbox[1] - bbox[0])

    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    bm.draw(ax, bbox, rivers=False, lakes=False)

    # --- anchors --------------------------------------------------------
    for key, name, dx, dy, ha in ANCHORS:
        a, b = float(S[key]["lat"]), float(S[key]["lon"])
        ax.plot(b, a, "o", ms=4.2, mfc=GREY, mec="white", mew=0.9, zorder=8)
        ax.text(b + dx, a + dy, name, fontsize=9.2, color=GREY, ha=ha, va="center",
                style="italic", zorder=9,
                path_effects=[pe.withStroke(linewidth=2.6, foreground="white")])
    # --- the disputed ports ---------------------------------------------
    for i, (port, keys, names, (dx, dy, ha)) in enumerate(PORTS, 1):
        pts = [(float(S[k]["lat"]), float(S[k]["lon"])) for k in keys]
        pts += EXTRA.get(port, [])
        clat = sum(p[0] for p in pts) / len(pts)
        clon = sum(p[1] for p in pts) / len(pts)
        rad = max(max(math.hypot((p[0]-clat)*110.57,
                                 (p[1]-clon)*111.32*math.cos(math.radians(clat)))
                      for p in pts), 55)
        col = BLUE
        ring(ax, clat, clon, rad, color=col, lw=1.2, alpha=0.6, zorder=7)
        for p in pts:
            ax.plot(p[1], p[0], "o", ms=6.2, mfc=col, mec="white", mew=1.3, zorder=9)
        # badge on the circle itself, on the side the label sits, so the reader
        # can join number to place without a leader line
        rlo = rad / (111.32 * math.cos(math.radians(clat)))
        side = 1 if ha == "left" else -1
        ax.plot(clon + side * rlo, clat, "o", ms=14, mfc=col, mec="white",
                mew=1.7, zorder=11)
        ax.text(clon + side * rlo, clat, str(i), fontsize=8.4, fontweight="bold",
                color="white", ha="center", va="center", zorder=12)

        # The badge sits with the name. Nothing is drawn at the centroid,
        # because no one has proposed the centroid as a location.
        tx, ty = clon + dx, clat + dy
        bx = tx + (0.95 if ha == "left" else -0.95)
        ax.plot(bx, ty, "o", ms=17, mfc=col, mec="white", mew=1.8, zorder=12)
        ax.text(bx, ty, str(i), fontsize=9.8, fontweight="bold", color="white",
                ha="center", va="center", zorder=13)
        tx = tx + (2.05 if ha == "left" else -2.05)
        ax.text(tx, ty, port, fontsize=15.5, color=INK, ha=ha, va="center", zorder=12,
                path_effects=[pe.withStroke(linewidth=3.6, foreground="white")])
        for j, nm in enumerate(names):
            ax.text(tx, ty - 1.30 - j * 1.02, nm, fontsize=8.4, color=INK2, ha=ha,
                    va="center", zorder=12,
                    path_effects=[pe.withStroke(linewidth=2.8, foreground="white")])

    ax.text(0.014, 0.975, "Ports of the Periplus whose location is disputed",
            transform=ax.transAxes, fontsize=21, color=INK, ha="left", va="top",
            path_effects=[pe.withStroke(linewidth=4.5, foreground="white")])
    bm.scalebar(ax, bbox, km=500, x_frac=0.028, y_frac=0.038)

    out = ROOT / "figures" / "00_six_disputed_ports.png"
    fig.savefig(out, dpi=200, facecolor="white")
    print(f"-> {out.name}")

if __name__ == "__main__":
    main()
