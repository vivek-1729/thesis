"""The stadion implied by Casson's own identifications, leg by leg.

Every number here is Casson's: the stated stadia are his transcription of the
text, the actual distances are his measurements in nautical miles, and the
identifications that fix the endpoints are his. Appendix 2 supplies the legs he
tested for accuracy; Appendix 1, Table II supplies the two Malabar legs, which
he never tested.

The conventional 185 m stadion is not a metrological result. It is his stated
rule of thumb, "approximately ten stades correspond to a nautical mile", which
is 1852/10 exactly. It is drawn as the vertical line.

The top axis reads the same quantity as a speed. Casson's other rule of thumb
is 500 stades to a day's run, so an implied stadion is a daily distance made
good divided by 500. The scatter is therefore not textual corruption. It is the
range of speeds a square-rigged merchantman makes between coasting into a
headwind and running with the monsoon.
"""
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[1]
NM = 1852.0
CONV = NM / 10          # 185.2 m, the conventional stadion

INK, INK_2, MUTED = "#0b0b0b", "#52514e", "#8b8a85"
RULE, BAND = "#b4c2ca", "#eef2f4"

# Three states, each with its own colour AND marker, so identity never rests
# on colour alone.
CLASSES = {
    "redsea": ("#2a78d6", "o", "Red Sea and Arabia, tested in Appendix 2"),
    "india":  ("#c2703c", "^", "Indian waters, assessed in Appendix 2 prose"),
    "malabar": ("#1b1b1b", "D", "Malabar, Appendix 1 only, never tested"),
}

# label, stated stades (lo, hi), Casson's actual distance in nautical miles, class
LEGS = [
    ("Adulis to Avalitēs *",            (4800, 4800),  250, "redsea"),
    ("Berenikē to Muza",               (12000, 12000), 800, "redsea"),
    ("Berenikē to Adulis *",            (7000, 7000),  530, "redsea"),
    ("Okēlis to Eudaimōn Arabia",       (1200, 1200),   95, "redsea"),
    ("Tyndis to Muziris",                (500, 500),    39, "malabar"),
    ("Syagros to Asichōn *",            (2600, 2600),  230, "redsea"),
    ("Gulf of Zula, length",             (200, 200),    20, "redsea"),
    ("Eudaimōn Arabia to Kanē",         (2000, 2000),  205, "redsea"),
    ("Malaō to Cape Elephas",           (3000, 3500),  345, "redsea"),
    ("Muziris to Nelkynda",              (500, 500),    55, "malabar"),
    ("Zēnobios Is. to Sarapis Is.",     (2000, 2000),  235, "redsea"),
    ("Astakapra to end of Limyrikē",    (7000, 7000),  900, "india"),
    ("Barbarikon to Astakapra",         (3000, 3000),  450, "india"),
]


def implied(stades, nm):
    return nm * NM / stades


def main():
    rows = []
    for lab, (s_a, s_b), nm, cls in LEGS:
        lo, hi = sorted((implied(s_a, nm), implied(s_b, nm)))
        rows.append((lab, lo, hi, (lo + hi) / 2, s_a, s_b, nm, cls))
    rows.sort(key=lambda r: r[3])

    lo_all = min(r[1] for r in rows)
    hi_all = max(r[2] for r in rows)
    X0, X1 = 70, 300

    fig, ax = plt.subplots(figsize=(11.3, 6.6))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(X0, X1)
    ax.set_ylim(-0.75, len(rows) + 0.55)

    # The span the evidence actually covers, as a quiet backdrop.
    ax.axvspan(lo_all, hi_all, color=BAND, zorder=0)

    for i, (lab, lo, hi, mid, s_a, s_b, nm, cls) in enumerate(rows):
        col, mk, _ = CLASSES[cls]
        ax.plot([X0, lo - 3], [i, i], color=RULE, lw=0.6, ls=(0, (1, 2.6)),
                zorder=1)
        if hi - lo > 1:                       # a stated range, not a point
            ax.plot([lo, hi], [i, i], color=col, lw=2.8, solid_capstyle="round",
                    zorder=3, alpha=0.8)
        ax.plot([mid], [i], marker=mk, ms=8.5 if mk != "D" else 7.5,
                color=col, mec="white", mew=1.4, zorder=4, ls="none")
        stated = f"{s_a:,}" if s_a == s_b else f"{s_a:,}\u2013{s_b:,}"
        ax.text(X1 + 5, i, f"{stated} stadia / {nm} nm", ha="left", va="center",
                fontsize=8.6, color=MUTED, clip_on=False)

    # The conventional value.
    ax.axvline(CONV, color=INK, lw=1.3, zorder=5,
               ymin=0.0, ymax=0.90)
    ax.text(CONV - 4, len(rows) + 0.30,
            "185.2 m, the conventional stadion,\nwhich is 10 stades to the nautical mile",
            ha="right", va="top", fontsize=9, color=INK, linespacing=1.55,
            zorder=6)

    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=10, color=INK)
    for s in ("left", "right", "top"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(RULE)
    ax.tick_params(axis="y", length=0, pad=6)
    ax.tick_params(axis="x", colors=INK_2, length=3, labelsize=9.5)
    ax.set_xlabel("Stadion implied by Casson's own figures (metres)",
                  fontsize=10.5, color=INK, labelpad=9)

    # The same quantity read as a speed: 500 stades to a day's run.
    top = ax.secondary_xaxis("top", functions=(lambda m: m * 500 / NM,
                                               lambda d: d * NM / 500))
    top.set_xlabel("The same figure read as a day's run, at 500 stades to the "
                   "day (nautical miles)", fontsize=10.5, color=INK, labelpad=9)
    top.tick_params(colors=INK_2, length=3, labelsize=9.5)
    top.spines["top"].set_color(RULE)

    handles = [plt.Line2D([], [], marker=mk, ls="none", color=c, ms=8,
                          mec="white", mew=1.2, label=lbl)
               for c, mk, lbl in CLASSES.values()]
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(-0.265, -0.135),
              frameon=False, fontsize=9.2, handletextpad=0.5,
              labelcolor=INK_2, ncol=3, columnspacing=1.9)

    fig.suptitle("Casson's own identifications do not imply a single stadion",
                 x=0.010, y=0.982, ha="left", fontsize=15.5, color=INK)
    fig.text(0.010, 0.928,
             f"Thirteen legs, spanning {lo_all:.0f} to {hi_all:.0f} m, a "
             f"{hi_all/lo_all:.1f}-fold range. Stated stadia, measured distances "
             "and endpoint identifications are all his.",
             ha="left", fontsize=10.3, color=INK_2)
    fig.text(0.010, 0.020,
             "*  a figure the Periplus gives in parts, which Casson sums."
             "     Sources: Casson 1989, Appendix 2 and Appendix 1 Table II.",
             ha="left", fontsize=8.2, color=MUTED)

    fig.subplots_adjust(left=0.203, right=0.818, top=0.828, bottom=0.175)
    out = ROOT / "figures/09_implied_stadion.png"
    fig.savefig(out, dpi=220, facecolor="white")
    print("wrote", out)
    print(f"range {lo_all:.1f} - {hi_all:.1f} m  ({hi_all/lo_all:.2f}x)")


if __name__ == "__main__":
    main()
