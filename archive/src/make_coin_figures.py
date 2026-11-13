"""Six figures on the coin evidence, for the appendix.

The argument they carry together is that Roman coinage is the wrong instrument
for locating a harbour: in India it sits inland, in East Africa there is none at
all, hoarded gold and excavated bronze are different kinds of evidence, and even
where coins are recovered most of them cannot be read.
"""
import csv, math, pathlib, collections
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import basemap as bm

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#8b8a85"
RULE = "#dfe5e9"
IND, LKA, ARB = "#2a78d6", "#c2703c", "#1baf7a"


def style(ax):
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    for s in ("left", "bottom"): ax.spines[s].set_color(RULE)
    ax.tick_params(colors=INK2, length=3, labelsize=9.5)


def head(fig, title, sub=None):
    """Title block positioned in inches, so short figures do not collide."""
    h = fig.get_figheight()
    fig.suptitle(title, x=0.012, y=1 - 0.33 / h, ha="left", fontsize=15, color=INK)
    if sub:
        fig.text(0.012, 1 - 0.70 / h, sub, ha="left", fontsize=10.2, color=INK2)


# ------------------------------------------------------------------ figure 1
def cumulative_distance():
    D = list(csv.DictReader(open(ROOT / "data/processed/chre_hoard_distances.csv")))
    fig, ax = plt.subplots(figsize=(9.6, 5.4)); fig.patch.set_facecolor("white")
    for ctry, col in [("India", IND), ("Sri Lanka", LKA)]:
        rows = [(float(r["dist_to_coast_km"]), int(r["coinCount"] or 0))
                for r in D if r["country"] == ctry and r["dist_to_coast_km"]]
        rows.sort()
        tot = sum(n for _, n in rows)
        xs, ys, run = [0], [0], 0
        for d, n in rows:
            run += n; xs.append(d); ys.append(run / tot * 100)
        ax.step(xs, ys, where="post", color=col, lw=2.6,
                label=f"{ctry}   {len(rows)} hoards, {tot:,} coins")
        ax.fill_between(xs, ys, step="post", color=col, alpha=0.07)
    ax.axvline(25, color=INK, lw=1.1, ls=(0, (4, 3)))
    ax.text(27, 6, "25 km from the sea", fontsize=9.5, color=INK,
            path_effects=[pe.withStroke(linewidth=3, foreground="white")])
    ax.set_xlim(0, 420); ax.set_ylim(0, 101)
    ax.set_xlabel("Distance of the findspot from the coast (km)", fontsize=10.5,
                  color=INK, labelpad=8)
    ax.set_ylabel("Share of all recorded coins (%)", fontsize=10.5, color=INK,
                  labelpad=8)
    style(ax)
    lg = ax.legend(loc="lower right", frameon=False, fontsize=10, labelcolor=INK2)
    head(fig, "Roman coins in India are an interior phenomenon, and Sri Lanka's are not")
    fig.subplots_adjust(left=0.085, right=0.985, top=0.845, bottom=0.125)
    fig.savefig(OUT / "20_coin_distance_curve.png", dpi=220, facecolor="white")
    print("wrote 20_coin_distance_curve.png")


# ------------------------------------------------------------------ figure 2
def inland_map():
    """Where the hoards sit, against where the ports could be.

    Each disputed port is drawn as a circle enclosing every location proposed
    for it, so the figure carries the width of the disagreement rather than
    asserting a point. Distance from the coast is contoured, which is figure 1
    put back into space.
    """
    import numpy as np
    D = [r for r in csv.DictReader(open(ROOT / "data/processed/chre_hoard_distances.csv"))
         if r["country"] == "India" and r["lat"]]
    S = {r["site_key"]: r for r in csv.DictReader(open(ROOT / "data/raw/site_aliases.csv"))}
    PORTS = [("Tyndis", ["ponnani", "tanur", "kadalundi", "koyilandy"]),
             ("Muziris", ["pattanam", "kodungallur"]),
             ("Nelkynda", ["niranam", "kottayam_kerala", "kollam", "neendakara"]),
             ("Bakar\u0113", ["purakkad", "kallada", "thevalakara"])]
    bbox = (74.0, 80.6, 7.9, 14.2)
    aspect = 1 / math.cos(math.radians((bbox[2] + bbox[3]) / 2))
    w = 9.6; h = w * (bbox[3] - bbox[2]) * aspect / (bbox[1] - bbox[0])
    fig, ax = plt.subplots(figsize=(w, h + 0.95)); fig.patch.set_facecolor("white")
    bm.draw(ax, bbox, river_lw=(0.4, 1.4), min_flow=200)

    pts = []
    for shp, parts, _ in bm._read("ne_10m_coastline.shp"):
        for seg in bm._clip(shp, parts, bbox, pad=3.0):
            pts.extend(seg)
    P = np.array(pts)
    gx = np.linspace(bbox[0], bbox[1], 190); gy = np.linspace(bbox[2], bbox[3], 190)
    GX, GY = np.meshgrid(gx, gy)
    kx = 111.32 * math.cos(math.radians((bbox[2] + bbox[3]) / 2))
    dist = np.full(GX.shape, 1e9)
    for i in range(0, len(P), 3):
        np.minimum(dist, np.hypot((GX - P[i, 0]) * kx, (GY - P[i, 1]) * 110.57), out=dist)
    cs = ax.contour(GX, GY, dist, levels=[25, 100, 200], colors="#b4459b",
                    linewidths=[1.3, 1.0, 1.0], linestyles=[(0, (5, 3))] * 3, zorder=5)
    ax.clabel(cs, fmt=lambda v: f"{v:.0f} km", fontsize=9, colors="#b4459b",
              inline_spacing=6)
    from matplotlib.collections import PolyCollection
    ocean = [sg for shp, parts, _ in bm._read("ne_10m_ocean.shp")
             for sg in bm._clip(shp, parts, bbox)]
    ax.add_collection(PolyCollection(ocean, facecolors=bm.OCEAN, edgecolors="none",
                                     zorder=5.5))

    for r in sorted(D, key=lambda x: int(x["coinCount"] or 0)):
        n = int(r["coinCount"] or 0)
        ax.plot([float(r["lon"])], [float(r["lat"])], "o",
                ms=4 + 13 * (min(n, 2500) / 2500) ** 0.45,
                mfc=IND, mec="white", mew=0.8, alpha=0.9, zorder=6)

    # each port as the circle enclosing every location proposed for it
    def km(a, b):
        la = (a[1] + b[1]) / 2
        return math.hypot((a[0] - b[0]) * 111.32 * math.cos(math.radians(la)),
                          (a[1] - b[1]) * 110.57)
    LBL = {"Tyndis": (0.52, 0.30, "left"), "Muziris": (0.24, 0.02, "left"),
           "Nelkynda": (0.50, 0.30, "left"), "Bakar\u0113": (0.46, -0.58, "left")}
    for name, keys in PORTS:
        q = [(float(S[k]["lon"]), float(S[k]["lat"])) for k in keys if k in S]
        cx = sum(x for x, _ in q) / len(q); cy = sum(y for _, y in q) / len(q)
        rad = max(km((cx, cy), t) for t in q)
        la = rad / 110.57; lo = rad / (111.32 * math.cos(math.radians(cy)))
        th = [i * math.pi / 180 for i in range(0, 361, 2)]
        xs = [cx + lo * math.cos(t) for t in th]; ys = [cy + la * math.sin(t) for t in th]
        ax.fill(xs, ys, color=ARB, alpha=0.16, lw=0, zorder=7)
        ax.plot(xs, ys, color=ARB, lw=1.7, zorder=7.5)
        for x, y in q:
            ax.plot([x], [y], marker="s", ms=5.5, mfc=ARB, mec="white", mew=1.0,
                    zorder=8)
        dx, dy, ha = LBL[name]
        ax.text(cx + dx, cy + dy, f"{name}\n{len(q)} proposals, {rad:.0f} km",
                ha=ha, va="center", fontsize=9.8, color=INK, fontweight="bold",
                linespacing=1.35, zorder=10,
                path_effects=[pe.withStroke(linewidth=3.6, foreground="white")])

    hh = [plt.Line2D([], [], marker="o", ls="none", ms=5, mfc=IND, mec="white",
                     label="Hoard of under 100 coins"),
          plt.Line2D([], [], marker="o", ls="none", ms=13, mfc=IND, mec="white",
                     label="Hoard of over 1,000 coins"),
          plt.Line2D([], [], marker="s", ls="none", ms=6, mfc=ARB, mec="white",
                     label="Proposed location for a port"),
          plt.Line2D([], [], color=ARB, lw=1.7,
                     label="Circle enclosing all proposals for one port"),
          plt.Line2D([], [], color="#b4459b", lw=1.2, ls=(0, (5, 3)),
                     label="Distance from the coast")]
    lg = ax.legend(handles=hh, loc="lower left", frameon=True, fontsize=9.2,
                   labelcolor=INK2, borderpad=0.7)
    lg.set_zorder(11)
    lg.get_frame().set_edgecolor(RULE); lg.get_frame().set_facecolor("white")
    ax.set_xlim(*bbox[:2]); ax.set_ylim(*bbox[2:]); ax.set_aspect(aspect)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_visible(False)
    head(fig, "The ports could be anywhere in these circles; the coins are inland of all of them")
    fig.subplots_adjust(left=0.006, right=0.994, top=1 - 0.95 / (h + 0.95), bottom=0.006)
    fig.savefig(OUT / "21_coin_inland_map.png", dpi=220, facecolor="white")
    print("wrote 21_coin_inland_map.png")


# ------------------------------------------------------------------ figure 3
def nearest_hoard():
    """How far the nearest recorded hoard lies from each port under study."""
    # Only hoards that close by AD 200 count. Al-Wajh has a findspot a kilometre
    # away, but it holds three nummi of AD 295, which says nothing about a
    # first-century harbour. Proximity without the right date is not evidence.
    allH = list(csv.DictReader(open(ROOT / "data/processed/chre_hoards_clean.csv")))
    def closing(h):
        v = (h.get("openingYear1") or "").strip()
        return int(v) if v.lstrip("-").isdigit() else None
    H = [h for h in allH if closing(h) is not None and closing(h) <= 200]
    S = {r["site_key"]: r for r in csv.DictReader(open(ROOT / "data/raw/site_aliases.csv"))}
    TARGETS = [("myos_hormos", "Myos Hormos", "secure"), ("berenike", "Berenike", "secure"),
               ("aynuna", "Aynuna", "Leukē Kōmē"),
               ("al_wajh", "Al-Wajh", "Leukē Kōmē"),
               ("banbhore", "Banbhore", "Barbarikon"),
               ("pattanam", "Pattanam", "Muziris"),
               ("ponnani", "Ponnani", "Tyndis"), ("niranam", "Niranam", "Nelkynda"),
               ("purakkad", "Purakkad", "Bakarē"),
               ("pangani", "Pangani", "Rhapta"), ("rufiji", "Rufiji delta", "Rhapta"),
               ("mafia", "Mafia", "Rhapta")]
    rows = []
    for k, lbl, grp in TARGETS:
        s = S[k]; la, lo = float(s["lat"]), float(s["lon"])
        best = min(math.hypot((float(h["longitude"]) - lo) * 111.32 *
                              math.cos(math.radians(la)),
                              (float(h["latitude"]) - la) * 110.57) for h in H)
        rows.append((lbl, grp, best))
    rows.sort(key=lambda r: r[2])
    fig, ax = plt.subplots(figsize=(9.6, 5.6)); fig.patch.set_facecolor("white")
    cols = {"secure": MUTED}
    for i, (lbl, grp, km) in enumerate(rows):
        c = cols.get(grp, LKA if km > 1000 else IND)
        ax.barh([i], [km], color=c, height=0.58)
        ax.text(km * 1.06, i, f"{km:,.0f} km", va="center", fontsize=10, color=INK)
        ax.text(-0.02, i, lbl, va="center", ha="right", fontsize=10.5, color=INK,
                transform=ax.get_yaxis_transform())
    ax.set_xscale("log"); ax.set_xlim(1.2, 9000)
    ax.set_ylim(-0.7, len(rows) - 0.3)
    ax.set_yticks([]); ax.set_xticks([100, 300, 1000, 3000])
    ax.set_xticklabels(["100", "300", "1,000", "3,000"])
    ax.set_xlabel("Distance to the nearest recorded Roman coin hoard (km, log scale)",
                  fontsize=10.5, color=INK, labelpad=8)
    style(ax); ax.spines["left"].set_visible(False)
    ax.set_xticks([3, 10, 30, 100, 300, 1000, 3000],
                  ["3", "10", "30", "100", "300", "1,000", "3,000"])
    head(fig, "For the East African candidates there is no coin evidence to assess",
         f"Nearest hoard closing by AD 200, from {len(H)} such hoards. "
         "The database has no entry at all for Tanzania, Kenya, Somalia or Ethiopia.")
    fig.subplots_adjust(left=0.155, right=0.965, top=0.825, bottom=0.125)
    fig.savefig(OUT / "22_nearest_hoard.png", dpi=220, facecolor="white")
    print("wrote 22_nearest_hoard.png")


# ------------------------------------------------------------------ figure 4
def metal_mix():
    C = list(csv.DictReader(open(ROOT / "data/processed/chre_coins_clean.csv")))
    SF = list(csv.DictReader(open(ROOT / "data/processed/site_find_coins.csv")))
    def band(m):
        m = (m or "").lower()
        if "gold" in m: return "Gold"
        if "silver" in m: return "Silver"
        return "Bronze or copper alloy"
    groups = [("India, hoarded", collections.Counter(band(c["material"]) for c in C
                                                     if c["country"] == "India")),
              ("Sri Lanka, hoarded", collections.Counter(band(c["material"]) for c in C
                                                          if c["country"] == "Sri Lanka")),
              ("Egypt, hoarded", collections.Counter(band(c["material"]) for c in C
                                                      if c["country"] == "Egypt")),
              ("Aynuna, excavated", collections.Counter(band(s["metal"]) for s in SF
                                                         if "Aynuna" in s["site_display"]))]
    order = ["Gold", "Silver", "Bronze or copper alloy"]
    cols = {"Gold": "#d6a832", "Silver": "#9aa7b2", "Bronze or copper alloy": "#8c6239"}
    fig, ax = plt.subplots(figsize=(9.8, 5.0)); fig.patch.set_facecolor("white")
    for i, (lbl, cnt) in enumerate(groups):
        tot = sum(cnt.values()) or 1
        left = 0
        for m in order:
            w = cnt.get(m, 0) / tot * 100
            if w <= 0: continue
            ax.barh([i], [w], left=left, color=cols[m], height=0.6)
            if w > 7:
                ax.text(left + w / 2, i, f"{w:.0f}%", ha="center", va="center",
                        fontsize=10.5, color="white", fontweight="bold")
            left += w
        ax.text(-0.015, i, f"{lbl}\n{tot:,} coins", va="center", ha="right",
                fontsize=10.2, color=INK, linespacing=1.5,
                transform=ax.get_yaxis_transform())
    ax.set_xlim(0, 100); ax.set_ylim(-0.65, len(groups) - 0.35)
    ax.set_yticks([]); ax.set_xticks([])
    for s in ax.spines.values(): s.set_visible(False)
    h = [plt.Line2D([], [], marker="s", ls="none", ms=10, mfc=cols[m], mec="none",
                    label=m) for m in order]
    ax.legend(handles=h, loc="upper left", bbox_to_anchor=(0, -0.06), ncol=3,
              frameon=False, fontsize=10, labelcolor=INK2)
    head(fig, "Hoarded gold and excavated bronze are different kinds of evidence",
         "Coin lost in an occupation layer is money being spent; buried gold is stored wealth.")
    fig.subplots_adjust(left=0.185, right=0.985, top=0.775, bottom=0.185)
    fig.savefig(OUT / "23_coin_metal_mix.png", dpi=220, facecolor="white")
    print("wrote 23_coin_metal_mix.png")


# ------------------------------------------------------------------ figure 5
def attribution_funnel():
    """What survives of the information, not of the object, at Berenike."""
    steps = [("Recovered in seven seasons", 523),
             ("Datable to a period", 283),
             ("Assignable to an emperor", 43),
             ("Preserving a mint mark", 13)]
    fig, ax = plt.subplots(figsize=(9.2, 4.8)); fig.patch.set_facecolor("white")
    for i, (lbl, n) in enumerate(steps):
        w = n / steps[0][1] * 100
        ax.barh([-i], [w], color=IND if i == 0 else "#7fa9dd" if i < 3 else LKA,
                height=0.56)
        ax.text(w + 1.6, -i, f"{n}   {n/steps[0][1]*100:.0f}%", va="center",
                fontsize=10.5, color=INK)
        ax.text(-0.015, -i, lbl, va="center", ha="right", fontsize=10.5, color=INK,
                transform=ax.get_yaxis_transform())
    ax.set_xlim(0, 118); ax.set_ylim(-len(steps) + 0.4, 0.6)
    ax.set_yticks([]); ax.set_xticks([])
    for s in ax.spines.values(): s.set_visible(False)
    head(fig, "Excavation recovers objects without necessarily recovering information",
         "Berenike, seven seasons, 1994–2000. Sidebotham and Wendrich 2007, Tables 8-4 to 8-6.")
    fig.subplots_adjust(left=0.30, right=0.985, top=0.775, bottom=0.075)
    fig.savefig(OUT / "24_attribution_funnel.png", dpi=220, facecolor="white")
    print("wrote 24_attribution_funnel.png")


# ------------------------------------------------------------------ figure 6
def mint_profile():
    C = list(csv.DictReader(open(ROOT / "data/processed/chre_coins_clean.csv")))
    WEST = {"Rome", "Lyon (Lugdunum)", "Colonia Patricia", "Caesaraugusta",
            "Emerita", "Tarraco", "Ticinum", "Aquileia", "Mediolanum", "Trier"}
    def band(m):
        if not m or m == "Uncertain": return None
        if m in WEST: return "Western mints, Rome and Gaul and Spain"
        if "Alexandria" in m: return "Alexandria"
        return "Other eastern mints"
    order = ["Western mints, Rome and Gaul and Spain", "Alexandria", "Other eastern mints"]
    cols = {order[0]: IND, order[1]: ARB, order[2]: MUTED}
    groups = []
    for ctry, lbl in [("India", "Hoards in India"), ("Egypt", "Hoards in Egypt"),
                      ("Jordan", "Hoards in Jordan")]:
        cnt = collections.Counter()
        for c in C:
            if c["country"] != ctry: continue
            b = band(c["mint"])
            if b: cnt[b] += 1
        groups.append((lbl, cnt))
    fig, ax = plt.subplots(figsize=(9.8, 4.6)); fig.patch.set_facecolor("white")
    for i, (lbl, cnt) in enumerate(groups):
        tot = sum(cnt.values()) or 1
        left = 0
        for m in order:
            w = cnt.get(m, 0) / tot * 100
            if w <= 0: continue
            ax.barh([i], [w], left=left, color=cols[m], height=0.6)
            if w > 8:
                ax.text(left + w / 2, i, f"{w:.0f}%", ha="center", va="center",
                        fontsize=10.5, color="white", fontweight="bold")
            left += w
        ax.text(-0.015, i, f"{lbl}\n{tot:,} coins with a named mint", va="center",
                ha="right", fontsize=10.2, color=INK, linespacing=1.5,
                transform=ax.get_yaxis_transform())
    ax.set_xlim(0, 100); ax.set_ylim(-0.65, len(groups) - 0.35)
    ax.set_yticks([]); ax.set_xticks([])
    for s in ax.spines.values(): s.set_visible(False)
    h = [plt.Line2D([], [], marker="s", ls="none", ms=10, mfc=cols[m], mec="none",
                    label=m) for m in order]
    ax.legend(handles=h, loc="upper left", bbox_to_anchor=(0, -0.08), ncol=3,
              frameon=False, fontsize=9.6, labelcolor=INK2)
    head(fig, "The coins that reached India were struck in the west, not in Egypt",
         "Egyptian currency stayed in Egypt. What went east was western gold moving as specie.")
    fig.subplots_adjust(left=0.235, right=0.985, top=0.755, bottom=0.205)
    fig.savefig(OUT / "25_mint_profile.png", dpi=220, facecolor="white")
    print("wrote 25_mint_profile.png")


if __name__ == "__main__":
    cumulative_distance(); inland_map(); nearest_hoard()
    metal_mix(); attribution_funnel(); mint_profile()
