"""One zoomed panel per disputed port: what has been found near each candidate.

The question each panel answers is local and concrete -- for this port, where
are the proposed locations, and what has anyone actually found around them.
Coastline is modern throughout; the ancient shoreline is a separate problem and
is not guessed at here.

Three things are plotted, and nothing else:
  candidate locations, Roman coin hoards (CHRE), and places where fieldwork is
  on record (Indian Archaeology: A Review, or an excavation report).
Rivers are drawn because at this scale they are the argument: the Periplus puts
Nelkynda 120 stadia up a river and Muziris on one.
"""
import csv, math, pathlib, textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe

import basemap as bm

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA, FIG = ROOT / "data", ROOT / "figures"

CAND, HOARD, WORK = "#2a78d6", "#eb6834", "#1baf7a"
LATER = "#8b8a85"          # deliberately muted: context, not a claim about the Periplus
DUG_EMPTY = "#9fb0bd"      # excavated, but nothing of Periplus date came up
INK, INK2, MUTED = bm.INK, bm.INK_2, bm.MUTED

# CHRE places this hoard in central Kerala, but its own county field says Kannur
# and its summary says "on the slope of a hill by the sea". See
# docs/numismatic-evidence.md. Excluded rather than silently plotted.
BAD_HOARDS = {"18598"}

PORTS = {
    "Muziris":     ("Muziris",     ["pattanam", "kodungallur"]),
    "Tyndis":      ("Tyndis",      ["ponnani", "tanur", "kadalundi", "koyilandy"]),
    "Nelkynda":    ("Nelkynda",    ["niranam", "kottayam_kerala", "kollam", "neendakara"]),
    "Bakare":      ("Bakarē",      ["purakkad", "kallada", "thevalakara"]),
    "Leuke Kome":  ("Leukē Kōmē",  ["aynuna", "al_wajh", "al_qusayr_arabia"]),
    "Barbarikon":  ("Barbarikon",  ["banbhore"]),
    "Rhapta":      ("Rhapta",      ["rufiji", "mafia", "pangani", "dar_es_salaam",
                                    "unguja_ukuu", "fukuchani"]),
}

def load():
    sites = {r["site_key"]: r for r in csv.DictReader(open(DATA / "raw" / "site_aliases.csv"))}
    eff = {r["site_key"]: r for r in csv.DictReader(open(DATA / "raw" / "site_survey_effort.csv"))}
    later = {r["site_key"]: r for r in csv.DictReader(open(DATA / "raw" / "later_settlement.csv"))}
    eviden = {r["site_key"]: r for r in csv.DictReader(open(DATA / "raw" / "candidate_evidence.csv"))}
    hoards = []
    for r in csv.DictReader(open(DATA / "raw" / "chre" / "chre_hoards.csv")):
        if r["id"] in BAD_HOARDS:
            continue
        try:
            hoards.append((float(r["latitude"]), float(r["longitude"]),
                           int(r["coinCount"] or 0), r["hoardName"], r["terminalYear1"]))
        except (TypeError, ValueError):
            continue
    work = []
    for r in csv.DictReader(open(DATA / "raw" / "iar_findspots.csv")):
        if "no recorded fieldwork" in r["what_was_found"]:
            continue
        if r["lat"]:
            work.append((float(r["lat"]), float(r["lon"]), r["name"],
                         r["what_was_found"], r["iar_volume"], r["port"]))
    return sites, eff, hoards, work, later, eviden

def km_between(a, b, c, d):
    p = math.pi / 180
    return 6371 * math.acos(max(-1, min(1, math.sin(a*p)*math.sin(c*p)
            + math.cos(a*p)*math.cos(c*p)*math.cos((d-b)*p))))


def window(pts, slot_ratio, pad_km=18, floor_km=45):
    """Fit the frame to the candidates plus a margin, then square it up.

    basemap.draw sets aspect = 1/cos(lat), so displayed h/w = lat_span*aspect/lon_span.
    Solving for lon_span keeps every panel the same physical shape.
    """
    la = [p[0] for p in pts]; lo = [p[1] for p in pts]
    clat, clon = (min(la) + max(la)) / 2, (min(lo) + max(lo)) / 2
    kmlat, kmlon = 110.57, 111.32 * math.cos(math.radians(clat))
    h = max((max(la) - min(la)) * kmlat + 2 * pad_km, floor_km)
    w = max((max(lo) - min(lo)) * kmlon + 2 * pad_km, floor_km)
    # enforce the panel's aspect
    if h / w > slot_ratio:
        w = h / slot_ratio
    else:
        h = w * slot_ratio
    dlat, dlon = h / 2 / kmlat, w / 2 / kmlon
    return (clon - dlon, clon + dlon, clat - dlat, clat + dlat)

def main():
    sites, eff, hoards, work, later, eviden = load()
    FIG.mkdir(exist_ok=True)
    made = []
    for key, (label, members) in PORTS.items():
        pts = [(float(sites[m]["lat"]), float(sites[m]["lon"])) for m in members if m in sites]
        if not pts:
            continue
        # Pull in any evidence close to a candidate so the frame contains it
        # whole, rather than clipping markers at the edge.
        near = list(pts)
        for la, lo, n, nm, term in hoards:
            if any(km_between(la, lo, a, b) <= 45 for a, b in pts):
                near.append((la, lo))
        for la, lo, nm, what, vol, port in work:
            if port in (key, label) and any(km_between(la, lo, a, b) <= 60 for a, b in pts):
                near.append((la, lo))

        fig = plt.figure(figsize=(7.7, 10.4))
        MAP_B, MAP_H = 0.315, 0.645
        ax = fig.add_axes([0.045, MAP_B, 0.91, MAP_H])
        # With a single candidate the frame can close in so tightly that no sea
        # appears at all, which is no use for a harbour. Banbhore in particular
        # sits about 30 km inland of the modern shoreline.
        floor = 45 if len({(round(a, 2), round(b, 2)) for a, b in pts}) > 1 else 115
        bbox = window(near, slot_ratio=MAP_H * 10.4 / (0.91 * 7.7), floor_km=floor)
        bm.draw(ax, bbox, river_lw=(0.5, 2.4))

        inb = lambda la, lo: bbox[0] <= lo <= bbox[1] and bbox[2] <= la <= bbox[3]
        rows = []                                  # key entries, numbered in order

        # --- fieldwork on record -------------------------------------------
        cand_names = {sites[m]["display_name"].split(" /")[0].split(" (")[0].strip().lower()
                      for m in members if m in sites}
        for la, lo, nm, what, vol, port in work:
            if not inb(la, lo) or port not in (key, label):
                continue
            if nm.strip().lower() in cand_names:
                continue
            ax.plot(lo, la, marker="s", ms=5.6, mfc=WORK, mec="white", mew=0.9,
                    zorder=7, clip_on=True)
            rows.append(("work", nm, f"{what}" + (f" (IAR {vol})" if vol != "-" else "")))

        # --- coin hoards ----------------------------------------------------
        for la, lo, n, nm, term in sorted((h for h in hoards if inb(h[0], h[1])),
                                          key=lambda h: -h[2]):
            s = 5.0 + 13.0 * (math.log10(n + 1) / 3.2) if n else 4.2
            ax.plot(lo, la, marker="o", ms=s, mfc=HOARD, mec="white", mew=0.9,
                    alpha=0.92, zorder=8, clip_on=True)
            cnt = f"{n:,} coins" if n else "count not recorded"
            when = ""
            if term and term.lstrip("-").isdigit():
                y = int(term)
                when = f", closes {abs(y)} BC" if y < 0 else f", closes AD {y}"
            rows.append(("hoard", nm.title(), cnt + when))

        # --- the candidates themselves --------------------------------------
        # The marker now carries the site's own evidence, because for a
        # candidate the findspot IS the site. A hollow circle means nobody has
        # dug; a grey one means somebody dug and found nothing of this date.
        for m in members:
            s_ = sites[m]; la, lo = float(s_["lat"]), float(s_["lon"])
            e = eff.get(m, {}); ev = eviden.get(m, {})
            lt = later.get(m)
            if lt:
                ax.plot(lo, la, marker="o", ms=21.5, mfc="none", mec=LATER,
                        mew=1.5, zorder=9, alpha=0.95)
            ph = ev.get("periplus_horizon", "unknown")
            style = {"yes":      dict(mfc=CAND, fill="full", txt="white"),
                     "contested":dict(mfc=CAND, fill="left", txt=CAND),
                     "no":       dict(mfc=DUG_EMPTY, fill="full", txt="white"),
                     }.get(ph, dict(mfc="white", fill="full", txt=CAND))
            ax.plot(lo, la, marker="o", ms=12.5, mfc=style["mfc"], mec=CAND,
                    mew=2.0, zorder=10, fillstyle=style["fill"],
                    mfcalt="white" if style["fill"] == "left" else style["mfc"])
            n = len([r for r in rows if r[0] == "cand"]) + 1
            # A half-filled marker has both a dark and a light side, so the
            # number needs an outline to stay legible over either.
            ax.text(lo, la, str(n), fontsize=7.4, fontweight="bold", ha="center",
                    va="center", color=style["txt"], zorder=11,
                    path_effects=[pe.withStroke(
                        linewidth=1.9,
                        foreground=CAND if style["txt"] == "white" else "white")])
            bits = [ev.get("what_was_found", "").strip()]
            if ev.get("site_coins", "").strip() not in ("", "none"):
                bits.append("Coins: " + ev["site_coins"].strip())
            if lt:
                bits.append(f"Still a port {lt['period_from']}-{lt['period_to']} AD "
                            f"({lt['period_label']})")
            rows.insert(n - 1, ("cand", s_["display_name"], ". ".join(b for b in bits if b)))

        bm.scalebar(ax, bbox)
        ax.set_title(f"{label}: the proposed locations, and what has been "
                     f"found at and around each",
                     fontsize=11.6, color=INK, pad=11, loc="left")

        # --- key -------------------------------------------------------------
        kx = fig.add_axes([0.045, 0.010, 0.91, MAP_B - 0.022]); kx.axis("off")
        # Only advertise a layer that is actually on this map; otherwise the
        # reader goes looking for something that is not there.
        n_h = len([r for r in rows if r[0] == "hoard"])
        n_w = len([r for r in rows if r[0] == "work"])
        n_l = sum(1 for m in members if m in later)
        present = {eviden.get(m, {}).get("periplus_horizon", "unknown") for m in members}
        handles = []
        if "yes" in present:
            handles.append(Line2D([], [], marker="o", ls="", ms=9, mfc=CAND, mec=CAND,
                                  label="material of Periplus date found at this site"))
        if "contested" in present:
            handles.append(Line2D([], [], marker="o", ls="", ms=9, mfc=CAND, mec=CAND,
                                  fillstyle="left", mfcalt="white",
                                  label="material claimed but the dating is disputed"))
        if "no" in present:
            handles.append(Line2D([], [], marker="o", ls="", ms=9, mfc=DUG_EMPTY, mec=CAND,
                                  label="excavated, but nothing of Periplus date"))
        if "unknown" in present:
            handles.append(Line2D([], [], marker="o", ls="", ms=9, mfc="white", mec=CAND,
                                  mew=1.8, label="never excavated, so untested"))
        if n_l:
            handles.append(Line2D([], [], marker="o", ls="", ms=13, mfc="none", mec=LATER,
                                  mew=1.3, label="outer ring: still a port in later centuries"))
        if n_h:
            handles.append(Line2D([], [], marker="o", ls="", ms=8, mfc=HOARD, mec="white",
                                  label="Roman coin hoard, sized by number of coins (CHRE)"))
        if n_w:
            handles.append(Line2D([], [], marker="s", ls="", ms=7, mfc=WORK, mec="white",
                                  label="fieldwork on record (Indian Archaeology: A Review)"))
        cands = [r for r in rows if r[0] == "cand"]
        others = [r for r in rows if r[0] != "cand"]
        lines = []
        for i, (_, nm, note) in enumerate(cands, 1):
            wrapped = textwrap.wrap(f"{i}.  {nm}. {note}", width=104,
                                    subsequent_indent="      ")
            lines.extend(wrapped)
        if others:
            lines.append("")
            room = 40
            for kind, nm, note in others[:room]:
                mark = "coins" if kind == "hoard" else "fieldwork"
                lines.extend(textwrap.wrap(f"     {nm} — {note}  [{mark}]", width=108,
                                           subsequent_indent="        "))
            if len(others) > room:
                lines.append(f"     … and {len(others)-room} more, listed in data/processed/")
        else:
            lines.append("")
            lines.append("     Nothing else recorded within this frame. The evidence "
                         "from each site itself is given above.")
        # Resize both panes now that the key's true length is known, so the
        # text is never clipped and the map takes whatever is left.
        n_lines = len(lines) + len(handles) + 2
        key_h = min(0.62, max(0.20, 0.0182 * n_lines + 0.035))
        ax.set_position([0.045, key_h + 0.035, 0.91, 0.955 - key_h - 0.045])
        kx.set_position([0.045, 0.010, 0.91, key_h + 0.012])
        kx.legend(handles=handles, loc="upper left", frameon=False, fontsize=8.2,
                  handletextpad=0.7, labelspacing=0.5,
                  bbox_to_anchor=(0, 1.0))
        legend_h = 0.0235 * len(handles) + 0.016          # figure fraction
        kx.text(0, 1.0 - legend_h / (key_h + 0.012), "\n".join(lines), fontsize=7.9,
                color=INK2, va="top", linespacing=1.5, family="DejaVu Sans",
                transform=kx.transAxes)

        out = FIG / f"port_{key.lower().replace(' ', '_')}.png"
        fig.savefig(out, dpi=190, facecolor="white")
        plt.close(fig)
        km = (bbox[1] - bbox[0]) * 111.32 * math.cos(math.radians((bbox[2]+bbox[3])/2))
        made.append((label, out.name, len(cands), len([r for r in rows if r[0]=='hoard']),
                     len([r for r in rows if r[0]=='work']), km))
    print(f"{'port':14s}{'cands':>6}{'hoards':>7}{'fieldwk':>8}{'width km':>10}  file")
    for lbl, fn, c, h, w, km in made:
        print(f"  {lbl:12s}{c:>6}{h:>7}{w:>8}{km:>10.0f}  {fn}")

if __name__ == "__main__":
    main()
