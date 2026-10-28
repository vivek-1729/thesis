"""Train a segmenter on known dead rivers, test it on a continent it never saw.

The design, and the reason for each part of it.

**The label is a channel that really died.** JRC Global Surface Water classes 3
and 6 are water present in the Landsat record and absent by 2021, filtered to
elongated components so reservoirs and ponds are excluded. The position is
known because a satellite watched it dry.

**The evidence is separated from the label in time.** Features are Sentinel-2
composites from 2022 onward, after the water is gone. The model sees only the
trace.

**The holdout is geographic, not random.** Training tiles are in Central Asia,
the Aral basin, Sistan and the Tarim. The test tiles are in the Indus delta,
which is both another continent and one of the seven ports. Random patch
splitting would leak, because neighbouring patches of one channel are nearly the
same picture.

**The threshold is fixed before running**, as everywhere else in this project.
Two bars: the segmenter must reach AUC 0.75 on held-out pixels, the figure used
for the per-pixel detector, and it must beat that detector on the same pixels.
Failing the second would mean shape adds nothing, which is a real result.

**Present water is excluded from scoring** at both training and test. A model
that finds lakes has not learned anything about relict channels.
"""
import argparse, csv, json, pathlib, time

import numpy as np
import torch

from . import detect, relict, stack
from .segnet import UNet, auc, device, loss_fn, predict

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "processed" / "sat"
MODELS = ROOT / "data" / "processed" / "models"

TRAIN_AREAS = {"aral": [58.5, 42.2, 60.5, 43.6],
               "sistan": [61.0, 30.6, 62.2, 31.8],
               "tarim": [80.5, 40.0, 82.5, 41.4]}
TEST_AREAS = {"indus": [66.9, 24.1, 68.0, 25.1]}

# The seven, as boxes the detector is finally pointed at.
PORTS = {
    "indus": [67.45, 24.70, 67.70, 24.92],
    "periyar": [76.15, 10.10, 76.40, 10.32],
    "pamba": [76.33, 9.28, 76.55, 9.50],
    "tyndis": [75.80, 10.85, 76.02, 11.07],
    "aynuna": [35.08, 28.00, 35.30, 28.22],
    "rufiji": [39.00, -8.05, 39.22, -7.83],
}

PRE_REGISTERED_AUC = 0.75
PATCH = 128


def tiles(areas, per_area=4):
    out = []
    for name, bbox in areas.items():
        for i, t in enumerate(relict.scan(bbox)[:per_area]):
            out.append({"name": f"{name}{i}", **t})
    return out


def region(t, retry=2):
    """Build one tile's features and labels, cached by name."""
    for k in range(retry):
        try:
            return relict.build(f"relict_{t['name']}", t["bbox"])
        except Exception as e:
            if k == retry - 1:
                print(f"      {t['name']} failed: {str(e)[:70]}", flush=True)
                return None
            time.sleep(5)


def sample(d, n=400, patch=PATCH, pos_frac=0.7, rng=None):
    """Patches, most of them containing channel.

    Positives are under two per cent of a scene, so uniform sampling would spend
    almost all its capacity on empty ground. Oversampling positives fixes the
    sampling; the loss handles what is left of the imbalance.
    """
    rng = rng or np.random.default_rng(0)
    X, y, v = d["X"], d["y"], d["valid"]
    C, H, W = X.shape
    if H < patch or W < patch:
        return []
    ys, xs = np.nonzero(y & v)
    out = []
    for i in range(n):
        if len(ys) and rng.random() < pos_frac:
            k = rng.integers(len(ys))
            r = int(np.clip(ys[k] - patch // 2, 0, H - patch))
            c = int(np.clip(xs[k] - patch // 2, 0, W - patch))
        else:
            r = int(rng.integers(0, H - patch + 1))
            c = int(rng.integers(0, W - patch + 1))
        vv = v[r:r + patch, c:c + patch]
        if vv.mean() < 0.5:
            continue
        out.append((X[:, r:r + patch, c:c + patch].copy(),
                    y[r:r + patch, c:c + patch].astype("float32"),
                    vv.astype("float32")))
    return out


def normaliser(patches):
    """Per-channel mean and standard deviation, from training patches only."""
    s = np.stack([p[0] for p in patches[:400]])
    mu = s.mean(axis=(0, 2, 3), keepdims=True)
    sd = s.std(axis=(0, 2, 3), keepdims=True) + 1e-6
    return mu[0], sd[0]


def train(patches, mu, sd, epochs=24, batch=8, lr=3e-4, seed=0):
    torch.manual_seed(seed)
    dev = device()
    C = patches[0][0].shape[0]
    model = UNet(C).to(dev)
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    pos = np.mean([p[1].mean() for p in patches])
    pos_weight = float(min(50.0, max(1.0, (1 - pos) / max(pos, 1e-4))))
    print(f"   {len(patches)} patches, {C} channels, positive rate {pos:.3%}, "
          f"pos_weight {pos_weight:.1f}, device {dev}", flush=True)
    rng = np.random.default_rng(seed)
    for ep in range(epochs):
        model.train()
        order = rng.permutation(len(patches))
        tot = 0.0
        for i in range(0, len(order) - batch + 1, batch):
            idx = order[i:i + batch]
            xb = np.stack([(patches[k][0] - mu) / sd for k in idx])
            yb = np.stack([patches[k][1] for k in idx])[:, None]
            vb = np.stack([patches[k][2] for k in idx])[:, None]
            xb = torch.from_numpy(xb).float().to(dev)
            yb = torch.from_numpy(yb).float().to(dev)
            vb = torch.from_numpy(vb).float().to(dev)
            opt.zero_grad()
            l = loss_fn(model(xb), yb, vb, pos_weight)
            l.backward(); opt.step()
            tot += float(l)
        if ep % 4 == 3 or ep == epochs - 1:
            print(f"      epoch {ep+1:2d}  loss {tot/max(1,len(order)//batch):.4f}", flush=True)
    return model


def baseline(d):
    """The existing per-pixel detector, on identical evidence."""
    comps = {}
    for season in ("dry", "wet"):
        med, _p, _s = stack.cached_composite(f"relict_{d['_name']}", d["bbox"],
                                             "2022-01-01", "2024-12-31", season)
        comps[season] = med
    return detect.spectral_score(comps)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-area", type=int, default=4)
    ap.add_argument("--epochs", type=int, default=24)
    ap.add_argument("--patches", type=int, default=400)
    a = ap.parse_args(argv)
    MODELS.mkdir(parents=True, exist_ok=True)

    print("scanning for tiles with dead channel ...", flush=True)
    tr = tiles(TRAIN_AREAS, a.per_area)
    te = tiles(TEST_AREAS, a.per_area)
    print(f"   {len(tr)} train tiles, {len(te)} held-out tiles\n", flush=True)

    print("building training regions ...", flush=True)
    patches = []
    for t in tr:
        d = region(t)
        if d is None:
            continue
        p = sample(d, a.patches)
        patches += p
        print(f"   {t['name']:10s} {d['y'].mean():6.3%} channel, {len(p)} patches", flush=True)
        del d
    if not patches:
        print("no training data"); return

    mu, sd = normaliser(patches)
    print("\ntraining ...", flush=True)
    model = train(patches, mu, sd, epochs=a.epochs)
    torch.save({"state": model.state_dict(), "mu": mu, "sd": sd,
                "channels": patches[0][0].shape[0]}, MODELS / "relict_unet.pt")

    print("\nheld-out evaluation, Indus delta, never seen in training\n", flush=True)
    rows = []
    for t in te:
        d = region(t)
        if d is None:
            continue
        d["_name"] = t["name"]
        Xn = (d["X"] - mu) / sd
        score = predict(model, Xn.astype("float32"))
        a_unet = auc(score, d["y"], d["valid"])
        try:
            a_base = auc(baseline(d), d["y"], d["valid"])
        except Exception as e:
            a_base = float("nan")
        rows.append({"tile": t["name"], "bbox": json.dumps(t["bbox"]),
                     "channel_frac": t["channel_frac"],
                     "auc_unet": round(a_unet, 3),
                     "auc_pixel_baseline": round(a_base, 3) if a_base == a_base else ""})
        print(f"   {t['name']:10s} channel {t['channel_frac']:6.3%}   "
              f"U-Net {a_unet:.3f}   per-pixel baseline {a_base:.3f}", flush=True)
        del d

    if rows:
        mu_u = np.mean([r["auc_unet"] for r in rows])
        mu_b = np.mean([r["auc_pixel_baseline"] for r in rows if r["auc_pixel_baseline"] != ""])
        print(f"\n   mean U-Net {mu_u:.3f}  mean baseline {mu_b:.3f}  "
              f"(pre-registered bar {PRE_REGISTERED_AUC})")
        print(f"   clears the bar: {mu_u >= PRE_REGISTERED_AUC}; "
              f"beats the baseline: {mu_u > mu_b}")
        with open(OUT / "relict_heldout.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader(); w.writerows(rows)
        print(f"   -> relict_heldout.csv")


if __name__ == "__main__":
    main()
