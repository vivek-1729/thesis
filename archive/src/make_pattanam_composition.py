"""What Pattanam's pottery is actually made of.

Cherian's season tables, 2007-2011, are the only published quantification of
any candidate site in the study. The whole assemblage is drawn as one bar, and
the imported fraction is then magnified, because the interesting result is not
that Roman pottery is present but how little of the imported pottery is Roman.
"""
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[1]
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#8b8a85"
RULE = "#dfe5e9"

TOTAL_STATED = 3_557_118          # Cherian's printed total for all ceramics
LOCAL = 3_537_464
CLASSES = [                       # sherds, origin group, colour
    ("Rouletted Ware",        8_534, "Indian",        "#c2703c"),
    ("Roman amphora",         6_029, "Mediterranean", "#2a78d6"),
    ("Torpedo jar",           3_098, "Mesopotamian",  "#1baf7a"),
    ("Turquoise Glazed Pottery", 1_527, "Mesopotamian", "#1baf7a"),
    ("Terra sigillata",         122, "Mediterranean", "#2a78d6"),
]
NAMED = sum(c[1] for c in CLASSES)
IMPORT = TOTAL_STATED - LOCAL     # 19,654; the named classes leave 344 unassigned
TOTAL = TOTAL_STATED


def main():
    groups = {}
    for name, n, grp, col in CLASSES:
        g = groups.setdefault(grp, {"n": 0, "col": col, "parts": []})
        g["n"] += n; g["parts"].append((name, n))
    rest = IMPORT - NAMED
    if rest:
        groups["Unassigned"] = {"n": rest, "col": "#b7bcc2",
                                "parts": [("not broken out in the table", rest)]}

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11.2, 5.9),
                                   gridspec_kw={"height_ratios": [1, 1.5]})
    fig.patch.set_facecolor("white")

    # --- top: the whole assemblage
    ax1.barh([0], [LOCAL / TOTAL * 100], color="#d8d4cb", height=0.52)
    ax1.barh([0], [IMPORT / TOTAL * 100], left=LOCAL / TOTAL * 100,
             color=INK, height=0.52)
    ax1.text(LOCAL / TOTAL * 50, 0, f"Locally made   {LOCAL:,} sherds   99.45%",
             ha="center", va="center", fontsize=11, color=INK2)
    ax1.annotate(f"Imported   {IMPORT:,}   {IMPORT/TOTAL*100:.2f}%",
                 xy=(99.72, 0.26), xytext=(88, 0.85), fontsize=11, color=INK,
                 ha="center",
                 arrowprops=dict(arrowstyle="-", color=INK, lw=1.0,
                                 connectionstyle="angle,angleA=0,angleB=90,rad=0"))
    ax1.set_xlim(0, 100); ax1.set_ylim(-0.45, 1.15)
    ax1.set_yticks([]); ax1.set_xticks([])
    for s in ax1.spines.values(): s.set_visible(False)
    ax1.set_title("The whole assemblage, 3,557,118 sherds", loc="left",
                  fontsize=11, color=INK2, pad=8)

    # --- bottom: the imported fraction, magnified
    order = ["Indian", "Mediterranean", "Mesopotamian", "Unassigned"]
    left = 0
    for grp in order:
        g = groups[grp]
        w = g["n"] / IMPORT * 100
        ax2.barh([0], [w], left=left, color=g["col"], height=0.60)
        lab = f"{grp}\n{g['n']:,}   {w:.0f}%" if w > 6 else f"{w:.0f}%"
        ax2.text(left + w / 2, 0, lab, ha="center", va="center",
                 fontsize=11.5 if w > 6 else 9, color="white", linespacing=1.5,
                 fontweight="bold")
        for j, (nm, v) in enumerate(g["parts"] if w > 5 else []):
            ax2.text(left + w / 2, -0.46 - 0.20 * j, f"{nm}  {v:,}", ha="center",
                     va="center", fontsize=9.2, color=MUTED)
        left += w
    ax2.set_xlim(0, 100); ax2.set_ylim(-0.95, 0.55)
    ax2.set_yticks([]); ax2.set_xticks([])
    for s in ax2.spines.values(): s.set_visible(False)
    ax2.set_title("The imported fraction, magnified", loc="left",
                  fontsize=11, color=INK2, pad=8)

    fig.suptitle("Under a third of the imported pottery at Pattanam is Mediterranean",
                 x=0.012, y=0.975, ha="left", fontsize=15.5, color=INK)
    fig.text(0.012, 0.028,
             "Source: Cherian, KCHR excavations 2007–2011, Tamil Civilization 24.1–2, Tables 1–2.",
             ha="left", fontsize=8.4, color=MUTED)
    fig.subplots_adjust(left=0.035, right=0.985, top=0.845, bottom=0.115, hspace=0.62)
    out = ROOT / "figures/15_pattanam_composition.png"
    fig.savefig(out, dpi=220, facecolor="white")
    print("wrote", out)
    print(f"imported {IMPORT:,} = {IMPORT/TOTAL*100:.2f}%;  "
          f"Mesopotamian/Mediterranean = {groups['Mesopotamian']['n']/groups['Mediterranean']['n']:.2f}")


if __name__ == "__main__":
    main()
