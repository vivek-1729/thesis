"""The stadion implied by each leg of Casson's own accuracy tables.

Every number here is Casson's: the stated stadia are his transcription of the
text, the actual distances are his measurements in nautical miles, and the
identifications fixing the endpoints are his. The legs are exactly the ones he
chose for Appendix 2 to demonstrate the author's accuracy, so every endpoint is
a securely located place and none of the disputed ports appears.

The vertical line is 185.2 m, which is his own rule of thumb that ten stades
correspond to a nautical mile, and which is the value the field uses.

The top axis reads the same quantity as a speed. His other rule of thumb is 500
stades to a day's run, so an implied stadion is a daily distance made good
divided by 500.
"""
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[1]
NM = 1852.0
CONV = NM / 10          # 185.2 m, the conventional stadion

INK, INK_2, MUTED = "#0b0b0b", "#52514e", "#8b8a85"
RULE, DOT = "#b4c2ca", "#2a78d6"

# label, stated stades (a, b), Casson's actual distance in nautical miles
# Casson 1989, Appendix 2, "Author's distances for short runs" and "for long runs".
LEGS = [
    ("Gulf of Zula, length",          (200, 200),    20),
    ("Malaō to Cape Elephas",   (3000, 3500),  345),
    ("Okēlis to Eudaimōn Arabia", (1200, 1200), 95),
    ("Eudaimōn Arabia to Kanē", (2000, 2000), 205),
    ("Syagros to Asichōn *",     (2600, 2600),  230),
    ("Zēnobios Is. to Sarapis Is.", (2000, 2000), 235),
    ("Berenikē to Adulis *", (7000, 7000), 530),
    ("Adulis to Avalitēs *",     (4800, 4800),  250),
    ("Berenikē to Muza",   (12000, 12000), 800),
]


def implied(stades, nm):
    return nm * NM / stades


def main():
    rows = []
    for lab, (s_a, s_b), nm in LEGS:
        lo, hi = sorted((implied(s_a, nm), implied(s_b, nm)))
        rows.append((lab, lo, hi, (lo + hi) / 2, s_a, s_b, nm))
    rows.sort(key=lambda r: r[3])

    lo_all = min(r[1] for r in rows)
    hi_all = max(r[2] for r in rows)
    X0, X1 = 80, 235

    fig, ax = plt.subplots(figsize=(10.4, 5.4))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(X0, X1)
    ax.set_ylim(-0.7, len(rows) - 0.3)

    for i, (lab, lo, hi, mid, s_a, s_b, nm) in enumerate(rows):
        ax.plot([X0, lo - 2.5], [i, i], color=RULE, lw=0.6, ls=(0, (1, 2.8)),
                zorder=1)
        if hi - lo > 1:                       # a stated range, not a point
            ax.plot([lo, hi], [i, i], color=DOT, lw=2.8, solid_capstyle="round",
                    zorder=3, alpha=0.8)
        ax.plot([mid], [i], marker="o", ms=8.5, color=DOT, mec="white", mew=1.4,
                zorder=4, ls="none")
        stated = f"{s_a:,}" if s_a == s_b else f"{s_a:,}–{s_b:,}"
        ax.text(X1 + 3.5, i, f"{stated} stadia / {nm} nm", ha="left",
                va="center", fontsize=8.6, color=MUTED, clip_on=False)

    ax.axvline(CONV, color=INK, lw=1.2, zorder=5)

    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=10, color=INK)
    ax.set_xticks([100, 125, 150, 185.2, 200, 225])
    ax.set_xticklabels(["100", "125", "150", "185.2", "200", "225"])
    for lbl, t in zip(ax.get_xticklabels(), ax.get_xticks()):
        if abs(t - CONV) < 0.5:
            lbl.set_color(INK)
            lbl.set_fontweight("bold")
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
    top.set_xlabel("The same figure as a day's run, at 500 stades to the day "
                   "(nautical miles)", fontsize=10.5, color=INK, labelpad=9)
    top.tick_params(colors=INK_2, length=3, labelsize=9.5)
    top.spines["top"].set_color(RULE)

    fig.suptitle("Casson's own identifications do not imply a single stadion",
                 x=0.011, y=0.975, ha="left", fontsize=15.5, color=INK)
    fig.text(0.011, 0.022,
             "*  a figure the Periplus gives in parts, which Casson sums."
             "     Source: Casson 1989, Appendix 2.",
             ha="left", fontsize=8.2, color=MUTED)

    fig.subplots_adjust(left=0.225, right=0.805, top=0.795, bottom=0.152)
    out = ROOT / "figures/09_implied_stadion.png"
    fig.savefig(out, dpi=220, facecolor="white")
    print("wrote", out)
    print(f"range {lo_all:.1f} - {hi_all:.1f} m  ({hi_all/lo_all:.2f}x)")
    print(f"daily runs {lo_all*500/NM:.0f} - {hi_all*500/NM:.0f} nm")


if __name__ == "__main__":
    main()
