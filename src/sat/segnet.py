"""A small U-Net for relict channels, and the honest way to score one.

The existing detector scores each pixel on its own spectrum. That is why it
cannot tell a palaeochannel from a paddy bund: both are anomalous, and only one
is anomalous *in the shape of a river*. A convolutional segmenter sees a
neighbourhood, so shape is available to it, which is the whole reason for
trying one.

The architecture is deliberately small. The training set is a few thousand
patches from a handful of regions, so a large model would memorise them, and the
question being asked is whether shape helps at all rather than how well a
well-funded model could do. Four down-sampling stages, base width 32, group
norm rather than batch norm because batches are small.

Scoring is per pixel and against the same held-out pixels the baseline sees, so
the comparison isolates the model from the evidence.
"""
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


def device():
    if torch.backends.mps.is_available():
        return torch.device("mps")
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


class Block(nn.Module):
    def __init__(self, c_in, c_out):
        super().__init__()
        self.a = nn.Conv2d(c_in, c_out, 3, padding=1)
        self.b = nn.Conv2d(c_out, c_out, 3, padding=1)
        self.na = nn.GroupNorm(8, c_out)
        self.nb = nn.GroupNorm(8, c_out)

    def forward(self, x):
        x = F.relu(self.na(self.a(x)))
        return F.relu(self.nb(self.b(x)))


class UNet(nn.Module):
    def __init__(self, c_in, base=32, depth=4):
        super().__init__()
        self.depth = depth
        self.down = nn.ModuleList()
        self.up = nn.ModuleList()
        self.upconv = nn.ModuleList()
        c = c_in
        widths = [base * 2 ** i for i in range(depth)]
        for w in widths:
            self.down.append(Block(c, w))
            c = w
        self.bottom = Block(c, c * 2)
        c = c * 2
        for w in reversed(widths):
            self.upconv.append(nn.ConvTranspose2d(c, w, 2, stride=2))
            self.up.append(Block(w * 2, w))
            c = w
        self.head = nn.Conv2d(c, 1, 1)

    def forward(self, x):
        skips = []
        for blk in self.down:
            x = blk(x)
            skips.append(x)
            x = F.max_pool2d(x, 2)
        x = self.bottom(x)
        for upc, blk, skip in zip(self.upconv, self.up, reversed(skips)):
            x = upc(x)
            if x.shape[-2:] != skip.shape[-2:]:
                x = F.interpolate(x, size=skip.shape[-2:], mode="nearest")
            x = blk(torch.cat([x, skip], 1))
        return self.head(x)


def loss_fn(logit, y, valid, pos_weight):
    """Weighted cross-entropy plus a soft Dice term, both masked to valid pixels.

    Relict channel is 0.1 to 1.5 per cent of a scene, so plain cross-entropy is
    minimised by predicting nothing. The positive weight fixes the gradient and
    Dice fixes the objective, since Dice is scale-free in the positive class.
    """
    m = valid.float()
    bce = F.binary_cross_entropy_with_logits(
        logit, y, weight=m, pos_weight=torch.as_tensor(pos_weight, device=logit.device))
    p = torch.sigmoid(logit) * m
    t = y * m
    inter = (p * t).sum(dim=(1, 2, 3))
    denom = p.sum(dim=(1, 2, 3)) + t.sum(dim=(1, 2, 3)) + 1.0
    dice = 1 - (2 * inter + 1.0) / denom
    return bce + dice.mean()


def auc(score, y, valid):
    """Rank AUC over valid pixels, by the same double-argsort the project uses."""
    s = score[valid].ravel()
    t = y[valid].ravel().astype(bool)
    a, b = s[t], s[~t]
    if len(a) == 0 or len(b) == 0:
        return float("nan")
    allv = np.concatenate([a, b])
    ranks = allv.argsort().argsort().astype("float64") + 1
    return float((ranks[:len(a)].sum() - len(a) * (len(a) + 1) / 2) / (len(a) * len(b)))


@torch.no_grad()
def predict(model, X, patch=256, overlap=32):
    """Score a whole scene by tiling, averaging the overlaps.

    Tiles overlap because a convolutional model is weakest at a patch edge where
    it has least context, and a seam running across a scene would look exactly
    like the linear feature being hunted.
    """
    model.eval()
    dev = next(model.parameters()).device
    C, H, W = X.shape
    out = np.zeros((H, W), "float32")
    hits = np.zeros((H, W), "float32")
    step = patch - overlap
    for y0 in range(0, max(H - overlap, 1), step):
        for x0 in range(0, max(W - overlap, 1), step):
            y1, x1 = min(y0 + patch, H), min(x0 + patch, W)
            y0a, x0a = max(0, y1 - patch), max(0, x1 - patch)
            tile = X[:, y0a:y1, x0a:x1]
            t = torch.from_numpy(tile[None]).to(dev)
            p = torch.sigmoid(model(t))[0, 0].cpu().numpy()
            out[y0a:y1, x0a:x1] += p
            hits[y0a:y1, x0a:x1] += 1
    return out / np.maximum(hits, 1)
