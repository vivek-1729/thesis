"""Five maps and one chart, one per slide, each carrying its own argument.

Each figure has a title and the graphic. Labels name places and finds and
nothing else; the reasoning belongs in the spoken bullets, not on the image.
"""
import csv, math, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Circle
import basemap as bm

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"
INK, INK2, MUTED = bm.INK, bm.INK_2, bm.MUTED
FOUND  = "#1baf7a"   # material of Periplus date recovered
TESTED = "#c2703c"   # excavated or surveyed, nothing of the right date
OTHER  = "#7a8794"   # excavated for unrelated reasons
NONE   = "#9aa3ab"   # never investigated
ARC    = "#2a78d6"

S = {r["site_key"]: r for r in csv.DictReader(open(ROOT / "data/raw/site_aliases.csv"))}
F = list(csv.DictReader(open(ROOT / "data/raw/iar_findspots.csv")))
LO, HI = 0.144, 0.204      # km per stadion, the range Casson's own legs imply


def xy(key):
    r = S[key]; return float(r["lon"]), float(r["lat"])


def frame(bbox, w=10.0, title="", min_flow=0.0):
    aspect = 1 / math.cos(math.radians((bbox[2] + bbox[3]) / 2))
    h = w * (bbox[3] - bbox[2]) * aspect / (bbox[1] - bbox[0])
    fig, ax = plt.subplots(figsize=(w, h + 0.75))
    fig.patch.set_facecolor("white")
    bm.draw(ax, bbox, river_lw=(0.6, 2.6), min_flow=min_flow)
    ax.set_xlim(bbox[0], bbox[1]); ax.set_ylim(bbox[2], bbox[3])
    ax.set_aspect(aspect)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    fig.suptitle(title, x=0.012, y=0.985, ha="left", fontsize=15, color=INK)
    fig.subplots_adjust(left=0.004, right=0.996, top=1 - 0.78 / (h + 0.75), bottom=0.004)
    return fig, ax


def ring(ax, lat, lon, km, **kw):
    la = km / 110.57
    lo = km / (111.32 * math.cos(math.radians(lat)))
    th = [i * math.pi / 180 for i in range(0, 361, 2)]
    ax.plot([lon + lo * math.cos(t) for t in th],
            [lat + la * math.sin(t) for t in th], **kw)


def band(ax, lat, lon, km_lo, km_hi, color=ARC, alpha=0.09):
    """A filled annulus, drawn as a wide dashed pair plus a soft fill."""
    for km in (km_lo, km_hi):
        ring(ax, lat, lon, km, color=color, lw=1.0, ls=(0, (5, 3)), zorder=3, alpha=0.85)
    la, lo = km_hi / 110.57, km_hi / (111.32 * math.cos(math.radians(lat)))
    ax.add_patch(Circle((lon, lat), 1, transform=ax.transData, visible=False))
    th = [i * math.pi / 180 for i in range(0, 361, 2)]
    outer = [(lon + lo * math.cos(t), lat + la * math.sin(t)) for t in th]
    lai, loi = km_lo / 110.57, km_lo / (111.32 * math.cos(math.radians(lat)))
    inner = [(lon + loi * math.cos(t), lat + lai * math.sin(t)) for t in reversed(th)]
    ax.fill([p[0] for p in outer + inner], [p[1] for p in outer + inner],
            color=color, alpha=alpha, lw=0, zorder=2)


def mark(ax, lon, lat, label, state=NONE, dx=0.0, dy=0.0, ha="left", size=10.5,
         ms=10, marker="o", weight="normal"):
    ax.plot([lon], [lat], marker=marker, ms=ms, mfc=state, mec="white", mew=1.6,
            zorder=8, ls="none")
    if label:
        ax.text(lon + dx, lat + dy, label, ha=ha, va="center", fontsize=size,
                color=INK, zorder=9, fontweight=weight,
                path_effects=[pe.withStroke(linewidth=3.2, foreground="white")])


def legend(ax, items, loc="lower left"):
    h = [plt.Line2D([], [], marker="o", ls="none", ms=9, mfc=c, mec="white",
                    mew=1.4, label=l) for l, c in items]
    lg = ax.legend(handles=h, loc=loc, frameon=True, fontsize=9.5,
                   labelcolor=INK2, handletextpad=0.5, borderpad=0.7)
    lg.get_frame().set_edgecolor("#dfe5e9"); lg.get_frame().set_facecolor("white")
    lg.get_frame().set_linewidth(0.8)


# ---------------------------------------------------------------- Leuke Kome
def leuke_kome():
    """Nappo's own window, measured from the accepted site of Myos Hormos,
    contains both candidates. The material does the separating, not the text."""
    bbox = (33.3, 37.9, 24.9, 29.2)
    fig, ax = frame(bbox, 10.0,
                    "The distance from Myos Hormos does not separate the candidates")
    mx, my = xy("myos_hormos")
    band(ax, my, mx, 185, 278)
    for k, lbl, st, dx, dy, ha in [
            ("aynuna", "Aynuna", FOUND, 0.14, 0.0, "left"),
            ("al_wajh", "Al-Wajh", TESTED, 0.14, 0.0, "left"),
            ("al_qusayr_arabia", "Al-Qusayr", NONE, 0.14, -0.02, "left")]:
        x, y = xy(k)
        ax.plot([mx, x], [my, y], color=MUTED, lw=0.8, ls=(0, (2, 3)), zorder=4)
        mark(ax, x, y, lbl, st, dx, dy, ha, weight="bold")
    mark(ax, mx, my, "Myos Hormos", OTHER, -0.16, 0.0, "right", size=10, ms=8)
    ax.text(35.55, 28.28, "236 km", fontsize=9, color=INK2, ha="center",
            path_effects=[pe.withStroke(linewidth=3, foreground="white")])
    ax.text(35.60, 25.95, "222 km", fontsize=9, color=INK2, ha="center",
            path_effects=[pe.withStroke(linewidth=3, foreground="white")])
    ax.text(34.62, 27.05, "185–278 km", fontsize=9.5, color=ARC, ha="center",
            rotation=-62, path_effects=[pe.withStroke(linewidth=3, foreground="white")])
    legend(ax, [("Periplus-period material recovered", FOUND),
                ("Surveyed, nothing of Periplus date", TESTED),
                ("Never investigated", NONE)], loc="upper right")
    bm.scalebar(ax, bbox)
    fig.savefig(OUT / "10_leuke_kome.png", dpi=220, facecolor="white")
    print("wrote 10_leuke_kome.png")


# --------------------------------------------------------------- Barbarikon
def barbarikon():
    """The text fixes Barbarikon on the middle of seven mouths of the Indus.
    HydroRIVERS models natural discharge and does not carry the delta
    distributaries, so the seven channels cannot be drawn from data we hold;
    that awaits the palaeochannel reconstruction. What the map can show is the
    consequence: the one proposed site now stands well inland of a coastline of
    shifting creeks."""
    bbox = (66.85, 68.95, 23.45, 25.30)
    fig, ax = frame(bbox, 10.0,
                    "Banbhore now stands 28 km inland of a delta coastline that has moved repeatedly",
                    min_flow=1.5)
    x, y = xy("banbhore")
    mark(ax, x, y, "Banbhore", OTHER, 0.045, 0.045, "left", weight="bold")
    ax.text(68.42, 25.02, "Indus", fontsize=12, color="#6f8fa3", style="italic",
            rotation=-52, path_effects=[pe.withStroke(linewidth=3, foreground="white")])
    cx, cy = 67.2555, 24.7480          # nearest point on the modern coastline
    ax.plot([cx, x], [cy, y], color=TESTED, lw=2.2, zorder=7, solid_capstyle="round")
    ax.text((cx + x) / 2, cy - 0.075, "28 km to open water", fontsize=10.5,
            color=TESTED, ha="center", fontweight="bold",
            path_effects=[pe.withStroke(linewidth=3.4, foreground="white")])
    h = [plt.Line2D([], [], marker="o", ls="none", ms=9, mfc=OTHER, mec="white",
                    mew=1.4, label="Excavated, but as Islamic Daybul"),
         plt.Line2D([], [], color=TESTED, lw=2.2, label="Distance to the modern shoreline")]
    lg = ax.legend(handles=h, loc="upper left", frameon=True, fontsize=9.5,
                   labelcolor=INK2, handletextpad=0.5, borderpad=0.7)
    lg.get_frame().set_edgecolor("#dfe5e9"); lg.get_frame().set_facecolor("white")
    lg.get_frame().set_linewidth(0.8)
    bm.scalebar(ax, bbox)
    fig.savefig(OUT / "11_barbarikon.png", dpi=220, facecolor="white")
    print("wrote 11_barbarikon.png")


# ------------------------------------------------------------------- Tyndis
def tyndis():
    """The only fieldwork bearing on Tyndis, plotted. One survey went looking
    for Roman material in this valley and recorded megaliths instead."""
    bbox = (75.50, 76.50, 10.58, 11.58)
    fig, ax = frame(bbox, 9.4,
                    "Fieldwork in the Ponnani valley recorded megaliths and no Roman material",
                    min_flow=12)
    RCW = [f for f in F if f["port"] == "Tyndis" and "Russet" in f["what_was_found"]]
    MEG = [f for f in F if f["port"] == "Tyndis" and
           ("megalithic" in f["what_was_found"] or "menhir" in f["what_was_found"])]
    for f in MEG:
        if not f["lat"]: continue
        lo, la = float(f["lon"]), float(f["lat"])
        if not (bbox[0] < lo < bbox[1] and bbox[2] < la < bbox[3]): continue
        ax.plot([lo], [la], marker="^", ms=7, mfc=TESTED, mec="white", mew=1.2, zorder=7)
        ax.text(lo + 0.018, la, f["name"], fontsize=8.4, color=INK2, va="center",
                path_effects=[pe.withStroke(linewidth=2.6, foreground="white")])
    for f in RCW:
        if not f["lat"]: continue
        lo, la = float(f["lon"]), float(f["lat"])
        ax.plot([lo], [la], marker="s", ms=9, mfc=FOUND, mec="white", mew=1.4, zorder=8)
        ax.text(lo - 0.022, la + 0.055, "Russet-coated\nPainted Ware", fontsize=9.5,
                color=INK, va="center", ha="right", linespacing=1.3, fontweight="bold",
                path_effects=[pe.withStroke(linewidth=3.4, foreground="white")])
    for k, lbl, dx, ha in [("koyilandy", "Koyilandy", -0.03, "right"),
                           ("kadalundi", "Kadalundi", -0.03, "right"),
                           ("tanur", "Tanur", -0.03, "right"),
                           ("ponnani", "Ponnani", -0.03, "right")]:
        lo, la = xy(k)
        mark(ax, lo, la, lbl, NONE, dx, 0.0, ha, weight="bold")
    ax.text(76.12, 10.735, "Bharathapuzha", fontsize=10, color="#6f8fa3", style="italic",
            rotation=-6, ha="center",
            path_effects=[pe.withStroke(linewidth=3, foreground="white")])
    legend(ax, [("Candidate, never excavated", NONE),
                ("Early Historic material", FOUND),
                ("Megalithic burials and menhirs", TESTED)], loc="upper right")
    bm.scalebar(ax, bbox)
    fig.savefig(OUT / "12_tyndis.png", dpi=220, facecolor="white")
    print("wrote 12_tyndis.png")


# ---------------------------------------------------- Nelkynda and Bakare
def nelkynda_bakare():
    """The Periplus says Nelkynda sits on a river about 120 stadia from the sea,
    and that Bakare is at that river's mouth. Casson reads the two as the same
    point, which makes 120 stadia the Nelkynda-to-Bakare distance. That reading
    is what this map tests; the text itself does not state it."""
    bbox = (76.02, 76.98, 8.82, 9.92)
    fig, ax = frame(bbox, 8.4,
                    "Casson reads the text's 120 stadia as the distance from Nelkynda to Bakarē",
                    min_flow=28)
    for k, col in [("niranam", ARC), ("kottayam_kerala", "#b4459b")]:
        lo, la = xy(k)
        band(ax, la, lo, 120 * LO, 120 * HI, color=col, alpha=0.10)
    for k, lbl, dx, dy, ha in [("niranam", "Niranam", 0.035, 0.03, "left"),
                               ("kottayam_kerala", "Kottayam", 0.035, 0.0, "left"),
                               ("kollam", "Kollam", 0.035, 0.0, "left"),
                               ("neendakara", "Neendakara", 0.035, -0.02, "left")]:
        lo, la = xy(k)
        mark(ax, lo, la, lbl, NONE, dx, dy, ha, weight="bold")
    for k, lbl, dx, ha in [("purakkad", "Purakkad", -0.035, "right"),
                           ("kallada", "Kallada", 0.035, "left"),
                           ("thevalakara", "Thevalakara", -0.035, "right")]:
        lo, la = xy(k)
        mark(ax, lo, la, lbl, NONE, dx, 0.0, ha, marker="D", ms=8, weight="bold")
    pux, puy = xy("purakkad")
    for k, col, km, dy in [("niranam", ARC, "21.2 km", -0.030),
                           ("kottayam_kerala", "#b4459b", "29.6 km", 0.030)]:
        kx, ky = xy(k)
        ax.plot([pux, kx], [puy, ky], color=col, lw=2.0, zorder=7,
                solid_capstyle="round")
        ax.text((pux + kx) / 2, (puy + ky) / 2 + dy, km, fontsize=10.5, color=col,
                ha="center", fontweight="bold",
                path_effects=[pe.withStroke(linewidth=3.6, foreground="white")])
    ax.text(76.22, 9.02, "120 stadia\nfrom Niranam", fontsize=9.2, color=ARC,
            ha="center", linespacing=1.3, fontweight="bold",
            path_effects=[pe.withStroke(linewidth=3.4, foreground="white")])
    ax.text(76.90, 9.83, "120 stadia\nfrom Kottayam", fontsize=9.2, color="#b4459b",
            ha="right", linespacing=1.3, fontweight="bold",
            path_effects=[pe.withStroke(linewidth=3.4, foreground="white")])
    h = [plt.Line2D([], [], marker="o", ls="none", ms=9, mfc=NONE, mec="white",
                    mew=1.4, label="Proposed for Nelkynda"),
         plt.Line2D([], [], marker="D", ls="none", ms=8, mfc=NONE, mec="white",
                    mew=1.4, label="Proposed for Bakarē"),
         plt.Line2D([], [], color=ARC, lw=2.0,
                    label="Measured distance to Purakkad")]
    lg = ax.legend(handles=h, loc="upper left", frameon=True, fontsize=9.3,
                   labelcolor=INK2, handletextpad=0.5, borderpad=0.7)
    lg.get_frame().set_edgecolor("#dfe5e9"); lg.get_frame().set_facecolor("white")
    lg.get_frame().set_linewidth(0.8)
    bm.scalebar(ax, bbox)
    fig.savefig(OUT / "13_nelkynda_bakare.png", dpi=220, facecolor="white")
    print("wrote 13_nelkynda_bakare.png")


# ------------------------------------------------------------------- Rhapta
def rhapta():
    """300 stadia offshore is 46.5 km. The three candidate islands are measured
    shore to shore against the Natural Earth coastline, not by eye, and the
    endpoints below come from data/processed/menuthias_distances.json."""
    import json
    D = json.loads((ROOT / "data/processed/menuthias_distances.json").read_text())
    bbox = (38.30, 40.45, -8.45, -4.42)
    fig, ax = frame(bbox, 7.6,
                    "Menuthias lies 300 stadia offshore, which is 46.5 km",
                    min_flow=30)
    TARGET = 46.5
    order = ["Pemba", "Zanzibar", "Mafia"]
    LBL = {"Pemba": (0.10, -0.20), "Zanzibar": (0.10, -0.22), "Mafia": (0.10, -0.26)}
    for name in order:
        d = D[name]
        (ilon, ilat), (mlon, mlat) = d["island"], d["mainland"]
        near = abs(d["km"] - TARGET) < 6
        col = FOUND if near else TESTED
        ax.plot([mlon, ilon], [mlat, ilat], color=col, lw=2.4, zorder=7,
                solid_capstyle="butt")
        for x, y in ((mlon, mlat), (ilon, ilat)):
            ax.plot([x], [y], marker="o", ms=4.5, mfc=col, mec="white", mew=1.0,
                    zorder=8, ls="none")
        mx, my = (mlon + ilon) / 2, (mlat + ilat) / 2
        off = -0.14 if name == "Pemba" else 0.12
        ax.text(mx, my + off, f"{d['km']:.1f} km", fontsize=10.5, color=col,
                ha="center", va="center", fontweight="bold",
                path_effects=[pe.withStroke(linewidth=3.4, foreground="white")])
        dx, dy = LBL[name]
        ax.text(ilon + dx, ilat + dy, name, fontsize=11.5, color=INK,
                fontweight="bold",
                path_effects=[pe.withStroke(linewidth=3.4, foreground="white")])
    # the target, drawn to the same scale so the three can be read against it
    ref_lat, ref_lon = -4.62, 38.40
    dlon = TARGET / (111.32 * math.cos(math.radians(ref_lat)))
    ax.plot([ref_lon, ref_lon + dlon], [ref_lat, ref_lat], color=INK, lw=2.6,
            zorder=7, solid_capstyle="butt")
    ax.text(ref_lon + dlon / 2, ref_lat + 0.11, "300 stadia = 46.5 km",
            fontsize=10, color=INK, ha="center", fontweight="bold",
            path_effects=[pe.withStroke(linewidth=3.4, foreground="white")])
    for k, lbl, dx, ha in [("pangani", "Pangani", -0.06, "right"),
                           ("dar_es_salaam", "Dar es Salaam", -0.06, "right"),
                           ("rufiji", "Rufiji delta", -0.06, "right")]:
        lo, la = xy(k)
        mark(ax, lo, la, lbl, NONE, dx, 0.0, ha, size=10, weight="bold")
    legend(ax, [("Mainland candidate for Rhapta", NONE),
                ("Island shore to mainland shore", TESTED)], loc="center right")
    bm.scalebar(ax, bbox)
    fig.savefig(OUT / "14_rhapta.png", dpi=220, facecolor="white")
    print("wrote 14_rhapta.png")


if __name__ == "__main__":
    leuke_kome(); barbarikon(); tyndis(); nelkynda_bakare(); rhapta()
