"""The circa-1700 soundings at Cranganore and Purakkad, read off the chart.

A deliberately small, honest analysis. Twenty soundings transcribed by eye from
the Dutch sheet, which is far too few to interpolate a seabed from, but enough
to compare two approaches surveyed on the same day by the same hand. Comparing
within one chart means the vertical datum, whatever it was, cancels.
"""
import csv, pathlib
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

ROOT = pathlib.Path(__file__).resolve().parents[2]
FATHOM = 1.8288
CRAN, PUR, INK, DRAUGHT = "#b91c1c", "#1d4ed8", "#1f2937", "#f59e0b"

rows = list(csv.DictReader(open(ROOT / "data" / "raw" / "soundings_dutch_c1700.csv")))
for r in rows:
    r["m"] = float(r["fathoms"]) * FATHOM

fig = plt.figure(figsize=(15, 8.2))
gs = fig.add_gridspec(2, 2, width_ratios=[1.45, 1], hspace=0.16, wspace=0.14)

# the two chart crops with the transcribed soundings marked
for i, (place, crop) in enumerate([("Cranganore", "32a_chart_cranganore.png"),
                                   ("Purakkad", "32b_chart_purakkad.png")]):
    ax = fig.add_subplot(gs[i, 0])
    ax.imshow(Image.open(ROOT / "figures" / crop))
    sub = [r for r in rows if r["place"] == place]
    for r in sub:
        col = DRAUGHT if r["setting"] == "entrance" else (CRAN if place == "Cranganore" else PUR)
        ax.scatter(float(r["crop_x"]), float(r["crop_y"]), s=170, facecolors="none",
                   edgecolors=col, linewidths=2.1, zorder=3)
    ax.set_xticks([]); ax.set_yticks([])
    lab = "Cranckenoore and the Vypin entrance" if place == "Cranganore" else "Porcae, that is Purakkad"
    ax.set_title(f"{lab}   ({len(sub)} soundings transcribed)", fontsize=10.5, loc="left")

# the comparison
ax = fig.add_subplot(gs[:, 1])
groups = [("Cranganore\nentrance", [r for r in rows if r["place"] == "Cranganore" and r["setting"] == "entrance"], DRAUGHT),
          ("Cranganore\napproach", [r for r in rows if r["place"] == "Cranganore" and r["setting"] == "approach"], CRAN),
          ("Purakkad\napproach", [r for r in rows if r["place"] == "Purakkad"], PUR)]
rng = np.random.default_rng(1)
for x, (lab, sub, col) in enumerate(groups):
    v = [r["m"] for r in sub]
    ax.scatter(np.full(len(v), x) + rng.uniform(-.07, .07, len(v)), v,
               s=95, color=col, alpha=.85, zorder=3)
    ax.plot([x - .22, x + .22], [min(v)] * 2, color=col, lw=2.6, zorder=4)
    ax.text(x + .27, min(v), f"shallowest {min(v):.1f} m", fontsize=9, va="center", color=col)

ax.axhspan(2, 4.5, color=DRAUGHT, alpha=.13, zorder=0)
ax.text(2.42, 3.25, "draught of a Roman\nmerchant vessel", fontsize=9, color="#92400e",
        ha="right", va="center")
ax.set_xticks(range(3)); ax.set_xticklabels([g[0] for g in groups], fontsize=10)
ax.set_ylabel("sounded depth, metres", fontsize=10)
ax.set_ylim(0, 24); ax.set_xlim(-.5, 2.75)
ax.spines[["top", "right"]].set_visible(False)
ax.set_title("Same chart, same surveyor, so the datum cancels", fontsize=11.5, loc="left")

fig.suptitle("What the circa-1700 Dutch chart measures at the two Malabar entrances",
             fontsize=14, x=0.012, ha="left", y=0.985)
fig.text(0.012, 0.005,
         "Twenty soundings read by eye from the chart; too few to interpolate a seabed, enough to compare two "
         "approaches surveyed by one hand. The Cranganore entrance\nshoals to 5.5 m between drawn sand banks "
         "while Purakkad's approach holds 11 m and is open. Both clear a laden merchantman, so the chart does not "
         "show Cranganore closed\nin 1700; it shows it constricted. Pliny calls Bakarē \"alius utilior portus\", "
         "a more useful port.",
         fontsize=9, color="#4b5563", ha="left")
fig.tight_layout(rect=[0, 0.045, 1, 0.972])
fig.savefig(ROOT / "figures" / "32_soundings_1700.png", dpi=145, bbox_inches="tight")
print("wrote figures/32_soundings_1700.png")
