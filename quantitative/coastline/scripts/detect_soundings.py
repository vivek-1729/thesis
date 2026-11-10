"""Find candidate sounding numerals in a window of an 1857 Admiralty sheet.

This only locates glyph clusters. It does not read them. Values are entered by
hand (see transcription workflow in the notebook), so detection errors show up
as clusters that are marked 'not a sounding' rather than as wrong depths.
"""
import sys, json, pathlib
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
from scipy import ndimage

Image.MAX_IMAGE_PIXELS = None
ROOT = pathlib.Path(__file__).resolve().parents[3]
CHART = ROOT.parent / "library" / "charts" / "malabar-749-1857.jpg"
OUT = ROOT / "quantitative" / "coastline" / "data" / "soundings_1857"

WINDOW = dict(x0=5600, y0=7600, x1=7300, y1=9300)   # Periyar / Kranganur entrance
TILE = 425

def detect(g):
    """Glyph clusters that look like a printed number.

    Numerals are inked strokes about 12-30 px tall with at least ~40 px of ink.
    The dash-dot depth contours break into strokes of 20-30 px of ink, so a
    mass threshold removes most of them. Small pieces (fraction digits, the
    stroke of a '1') are kept only when they sit next to a full numeral.
    """
    ink = g < 125
    lab, n = ndimage.label(ink)
    objs = ndimage.find_objects(lab)
    primary = np.zeros_like(ink); small = np.zeros_like(ink)
    for i, o in enumerate(objs, 1):
        h, w = o[0].stop - o[0].start, o[1].stop - o[1].start
        m = lab[o] == i
        area = m.sum()
        if 12 <= h <= 30 and w <= 30 and area >= 40:
            primary[o] |= m
        elif 4 <= h <= 30 and w <= 30 and area >= 6:
            small[o] |= m
    near = ndimage.binary_dilation(primary, np.ones((9, 15)))
    slab, _ = ndimage.label(small)
    attached = np.isin(slab, np.unique(slab[near & small]))
    attached &= slab > 0
    keep = primary | attached
    merged = ndimage.binary_dilation(keep, np.ones((7, 11)))
    clab, cn = ndimage.label(merged)
    rows = []
    for i, o in enumerate(ndimage.find_objects(clab), 1):
        h, w = o[0].stop - o[0].start, o[1].stop - o[1].start
        core = keep[o] & (clab[o] == i)
        if core.sum() < 40 or not (14 <= h <= 50 and 8 <= w <= 80):
            continue
        ys, xs = np.nonzero(core)
        rows.append(dict(cx=o[1].start + xs.mean(), cy=o[0].start + ys.mean(),
                         bx0=o[1].start, by0=o[0].start, bx1=o[1].stop, by1=o[0].stop,
                         ink_px=int(core.sum())))
    return pd.DataFrame(rows)

def main():
    w = WINDOW
    rgb = Image.open(CHART).crop((w["x0"], w["y0"], w["x1"], w["y1"]))
    g = np.asarray(rgb.convert("L")).astype(float)
    df = detect(g)
    df["chart_x"] = df.cx + w["x0"]; df["chart_y"] = df.cy + w["y0"]
    df["tile"] = (df.cy // TILE).astype(int) * 10 + (df.cx // TILE).astype(int)
    df = df.sort_values(["tile", "cy", "cx"]).reset_index(drop=True)
    df.insert(0, "id", [f"S{i:04d}" for i in range(len(df))])
    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / "candidates.csv", index=False)
    # tiles with numbered boxes, upscaled x2, for reading
    tiles = OUT / "tiles"; tiles.mkdir(exist_ok=True)
    for t, sub in df.groupby("tile"):
        ty, tx = divmod(t, 10)
        x0, y0 = tx * TILE, ty * TILE
        crop = rgb.crop((x0 - 20, y0 - 20, x0 + TILE + 20, y0 + TILE + 20)).resize(((TILE + 40) * 2,) * 2)
        d = ImageDraw.Draw(crop)
        for r in sub.itertuples():
            bx0, by0 = (r.bx0 - x0 + 20) * 2, (r.by0 - y0 + 20) * 2
            bx1, by1 = (r.bx1 - x0 + 20) * 2, (r.by1 - y0 + 20) * 2
            d.rectangle([bx0, by0, bx1, by1], outline=(220, 0, 0))
            d.text((bx1 + 2, by0 - 2), r.id[1:], fill=(0, 0, 200))
        crop.save(tiles / f"tile_{t:02d}.png")
    print(len(df), "candidate clusters in", df.tile.nunique(), "tiles")

if __name__ == "__main__":
    main()
