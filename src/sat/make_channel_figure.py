"""What the control test actually established, shown rather than asserted.

An earlier version of this figure drew "detected channels" over the imagery. It
overclaimed: the traces it produced followed the visible modern creek, and we
have never validated detection of a channel that is now dry. What the control
test established is narrower and still useful: the detector separates ground
adjacent to a watercourse from ordinary ground, strongly in the arid Indus and
not at all in Kerala. That separation is what this figure shows.
"""
import pathlib, sys
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from sat import stack, detect, control

ROOT = pathlib.Path(__file__).resolve().parents[2]
REGIONS = {
    "indus":   dict(bbox=[67.45, 24.70, 67.70, 24.92],
                    title="Indus delta, Banbhore", sub="arid, unirrigated"),
    "periyar": dict(bbox=[76.15, 10.10, 76.40, 10.32],
                    title="Periyar delta, Pattanam", sub="wet, canopied, cut by paddy bunds"),
}
POS, NEG, INK = "#2563eb", "#9ca3af", "#1f2937"


def stretch(a, lo=2, hi=98):
    v = a[np.isfinite(a)]
    if v.size == 0:
        return np.zeros_like(a)
    p0, p1 = np.percentile(v, [lo, hi])
    return np.clip((a - p0) / (p1 - p0 + 1e-9), 0, 1)


fig, axes = plt.subplots(2, 3, figsize=(16, 10.6),
                         gridspec_kw={"width_ratios": [1, 1, 0.92]})
rng = np.random.default_rng(0)

for row, (name, cfg) in enumerate(REGIONS.items()):
    comps = {s: stack.cached_composite(name, cfg["bbox"], "2022-01-01", "2024-12-31", s)[0]
             for s in ("dry", "wet")}
    score, _, _, _, _, _ = detect.spectral_score(comps)
    med = comps["dry"]

    pos, water = control.riparian_control(med)
    keep_out = ndimage.binary_dilation(water, iterations=60)
    elig = (~keep_out) & np.isfinite(score) & ~pos

    rgb = np.dstack([stretch(med["red"]), stretch(med["green"]), stretch(med["blue"])])
    axes[row, 0].imshow(rgb)
    axes[row, 0].set_title(f"{cfg['title']}\n{cfg['sub']}", fontsize=10.5, loc="left")

    axes[row, 1].imshow(stretch(score), cmap="magma")
    ov = np.zeros((*pos.shape, 4)); ov[pos] = [0.15, 0.39, 0.92, 0.55]
    axes[row, 1].imshow(ov)
    axes[row, 1].set_title("detector score, with the test zone in blue", fontsize=10.5, loc="left")

    a = score[pos & np.isfinite(score)]
    b = score[elig]
    a = rng.choice(a, min(40000, a.size), replace=False)
    b = rng.choice(b, min(40000, b.size), replace=False)
    allv = np.concatenate([a, b]); r = allv.argsort().argsort() + 1.0
    auc = (r[:len(a)].sum() - len(a) * (len(a) + 1) / 2) / (len(a) * len(b))

    ax = axes[row, 2]
    lo, hi = np.percentile(np.concatenate([a, b]), [0.5, 99.5])
    bins = np.linspace(lo, hi, 70)
    ax.hist(b, bins=bins, color=NEG, alpha=.85, density=True, label="ordinary ground")
    ax.hist(a, bins=bins, color=POS, alpha=.70, density=True, label="ground beside water")
    ax.set_title(f"AUC = {auc:.2f}" + ("   passes" if auc >= .75 else "   fails"),
                 fontsize=12, loc="left", color=("#15803d" if auc >= .75 else "#b91c1c"))
    ax.set_xlabel("detector score", fontsize=9)
    ax.set_yticks([]); ax.tick_params(labelsize=8.5)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.legend(fontsize=8.5, frameon=False, loc="upper right")

    for a_ in axes[row, :2]:
        a_.set_xticks([]); a_.set_yticks([])

fig.suptitle("Does the detector tell channel ground from ordinary ground?",
             fontsize=14, x=0.012, ha="left", y=0.985)
fig.text(0.012, 0.004,
         "The test zone is the ring of dry land just outside visible water, which carries the moisture signature a "
         "buried channel would leave; open water itself is excluded.\nIt is compared against ground at least 600 m "
         "from any water. The threshold of 0.75 was fixed before any site was run. Four methods have now failed at "
         "the Periyar.",
         fontsize=9, color="#4b5563", ha="left")
fig.tight_layout(rect=[0, 0.035, 1, 0.972])
fig.savefig(ROOT / "figures" / "31_channel_separation.png", dpi=140, bbox_inches="tight")
print("wrote figures/31_channel_separation.png")
