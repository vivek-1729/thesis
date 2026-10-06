"""End-to-end control test for one region.

Builds the seasonal composites, runs both detectors, scores each against the
HydroRIVERS control, and writes a figure and a JSON record. Every region is a
config entry rather than a new script.

    .venv/bin/python src/sat/run_region.py ghaggar
    .venv/bin/python src/sat/run_region.py --all
"""

import json
import pathlib
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from sat import stack, detect, control

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "processed" / "sat"
FIG = ROOT / "figures"

REGIONS = {
    # Orengo and Petrie's kind of terrain: the Ghaggar-Hakra dry bed on the
    # northern edge of the Thar, where the method was developed.
    "ghaggar": dict(bbox=[73.15, 29.15, 73.35, 29.32], hydro="as",
                    start="2022-01-01", end="2024-12-31",
                    note="Ghaggar-Hakra palaeochannel near Anupgarh, Rajasthan"),
    # Barbarikon. Repeated avulsion, and the shelf cores carry a hiatus over
    # the Periplus period, so imagery carries more weight here.
    "indus": dict(bbox=[67.45, 24.70, 67.70, 24.92], hydro="as",
                  start="2022-01-01", end="2024-12-31",
                  note="Indus delta around Banbhore"),
    # Muziris. Wet, canopied, and cut through with paddy bunds and canals.
    "periyar": dict(bbox=[76.15, 10.10, 76.40, 10.32], hydro="as",
                    start="2022-01-01", end="2024-12-31",
                    note="Periyar delta around Pattanam and Kodungallur"),
    # Nelkynda and Bakare, through the Vembanad backwaters.
    "pamba": dict(bbox=[76.33, 9.28, 76.55, 9.50], hydro="as",
                  start="2022-01-01", end="2024-12-31",
                  note="Pamba and the southern Vembanad, Niranam to Purakkad"),
}


def run(name, limit=10):
    cfg = REGIONS[name]
    bbox = cfg["bbox"]
    print(f"\n=== {name}: {cfg['note']}")

    comps, profile = {}, None
    for season in ("dry", "wet"):
        med, prof, used = stack.cached_composite(
            name, bbox, cfg["start"], cfg["end"], season, limit=limit)
        comps[season] = med
        profile = profile or prof
        print(f"  {season}: {len(used)} scenes, {med['red'].shape}, "
              f"{100 * np.isfinite(med['red']).mean():.0f}% valid")

    shape = comps["dry"]["red"].shape
    spec, pcs, evr, names = detect.spectral_score(comps)
    print(f"  PCA variance explained: {', '.join(f'{v:.2f}' for v in evr[:5])}")

    dem = detect.copernicus_dem(bbox, shape=shape)
    topo = detect.topographic_score(dem)
    print(f"  DEM relief {np.nanmin(dem):.0f} to {np.nanmax(dem):.0f} m; "
          f"detrended sd {np.nanstd(topo):.2f} m")

    results = []
    for label, score in (("spectral PCA", spec),
                         ("topographic", topo),
                         ("topographic, linear", detect.linearity(topo))):
        try:
            results.append(control.evaluate(
                score, bbox, profile, comps["dry"],
                region=cfg["hydro"], label=f"{name} / {label}"))
        except RuntimeError as e:
            print(f"  {label}: {e}")

    figure(name, cfg, comps, spec, topo, dem, profile)
    rec = {"region": name, **cfg, "shape": list(shape), "results": results}
    (OUT / f"{name}_control.json").write_text(json.dumps(rec, indent=1))
    return rec


def figure(name, cfg, comps, spec, topo, dem, profile):
    """True colour, the spectral score, and the detrended terrain, side by side."""
    def stretch(a, lo=2, hi=98):
        v = a[np.isfinite(a)]
        if v.size == 0:
            return np.zeros_like(a)
        p0, p1 = np.percentile(v, [lo, hi])
        return np.clip((a - p0) / (p1 - p0 + 1e-9), 0, 1)

    med = comps["dry"]
    rgb = np.dstack([stretch(med["red"]), stretch(med["green"]), stretch(med["blue"])])
    fig, ax = plt.subplots(1, 3, figsize=(16, 5.6))
    ax[0].imshow(rgb); ax[0].set_title("dry season, true colour", fontsize=10)
    ax[1].imshow(stretch(spec), cmap="magma")
    ax[1].set_title("spectral score (PCA 2-4)", fontsize=10)
    ax[2].imshow(stretch(topo), cmap="RdBu")
    ax[2].set_title("detrended terrain, blue = low", fontsize=10)
    for a in ax:
        a.set_xticks([]); a.set_yticks([])
    fig.suptitle(cfg["note"], fontsize=11)
    fig.tight_layout()
    FIG.mkdir(exist_ok=True)
    fig.savefig(FIG / f"sat_{name}.png", dpi=130, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    args = sys.argv[1:]
    names = list(REGIONS) if ("--all" in args or not args) else [a for a in args if not a.startswith("-")]
    out = [run(n) for n in names]
    print("\n=== summary")
    for rec in out:
        for r in rec["results"]:
            print(f"  {r['label']:34s} AUC={r['auc']:.3f}  {'PASS' if r['pass'] else 'FAIL'}")
