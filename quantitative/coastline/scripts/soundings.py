"""Generic sounding pipeline for the windows in sounding_sites.py.

  python soundings.py detect <site>   glyph detection, candidates.csv and numbered reading tiles
  python soundings.py build  <site>   join the hand readings (transcriptions/<site>.py) and georeference
  python soundings.py check  <site>   contact sheets of every reading beside its chart crop
  python soundings.py overview <site> the window at reduced size, with tile numbers, for orientation

Readings use the same format and status codes as transcription_1857.py (Kodungallur), plus one:
  later   a sounding inside an area the chart marks as added after the original survey (e.g. "soundings
          in 1901" on BA 750); kept in the table, excluded from the 1850s model.
"""
import sys, json, importlib.util, pathlib
import numpy as np, pandas as pd
from PIL import Image, ImageDraw
from pyproj import Transformer

Image.MAX_IMAGE_PIXELS = None
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from sounding_sites import SITES, CHARTS, ROOT, UTM_EPSG
from detect_soundings import detect, TILE

FATHOM_M = 1.8288


def paths(site):
    d = ROOT / "quantitative" / "coastline" / "data" / "soundings" / site
    return d, d / "tiles", d / "check"


def window_image(site):
    s = SITES[site]; x0, y0, x1, y1 = s["window"]
    return Image.open(CHARTS / s["file"]).crop((x0, y0, x1, y1))


def cmd_detect(site):
    d, tiles, _ = paths(site); tiles.mkdir(parents=True, exist_ok=True)
    rgb = window_image(site); x0, y0 = SITES[site]["window"][:2]
    df = detect(np.asarray(rgb.convert("L")).astype(float), SITES[site].get("ink", 125))
    df["chart_x"] = df.cx + x0; df["chart_y"] = df.cy + y0
    df["tile"] = (df.cy // TILE).astype(int) * 10 + (df.cx // TILE).astype(int)
    df = df.sort_values(["tile", "cy", "cx"]).reset_index(drop=True)
    df.insert(0, "id", [f"S{i:04d}" for i in range(len(df))])
    df.to_csv(d / "candidates.csv", index=False)
    for t, sub in df.groupby("tile"):
        ty, tx = divmod(t, 10); tx0, ty0 = tx * TILE, ty * TILE
        crop = rgb.crop((tx0 - 20, ty0 - 20, tx0 + TILE + 20, ty0 + TILE + 20)).resize(((TILE + 40) * 2,) * 2)
        dr = ImageDraw.Draw(crop)
        for r in sub.itertuples():
            bx0, by0, bx1, by1 = [(v - o + 20) * 2 for v, o in ((r.bx0, tx0), (r.by0, ty0), (r.bx1, tx0), (r.by1, ty0))]
            dr.rectangle([bx0, by0, bx1, by1], outline=(220, 0, 0))
            dr.text((bx1 + 2, by0 - 2), r.id[1:], fill=(0, 0, 200))
        # pixel grid every 50 window px, labelled, so missed numbers can be positioned
        for g in range(0, TILE + 1, 50):
            dr.line([((g + 20) * 2, 0), ((g + 20) * 2, 8)], fill=(0, 140, 0)); dr.text(((g + 20) * 2 + 2, 0), str(tx0 + g), fill=(0, 140, 0))
            dr.line([(0, (g + 20) * 2), (8, (g + 20) * 2)], fill=(0, 140, 0)); dr.text((2, (g + 20) * 2 + 2), str(ty0 + g), fill=(0, 140, 0))
        crop.save(tiles / f"tile_{t:02d}.png")
    print(site, len(df), "candidate clusters in", df.tile.nunique(), "tiles")


def cmd_overview(site):
    d, _, _ = paths(site); d.mkdir(parents=True, exist_ok=True)
    im = window_image(site); W, H = im.size; sc = 1000 / max(W, H)
    small = im.resize((int(W * sc), int(H * sc))); dr = ImageDraw.Draw(small)
    for ty in range(0, H, TILE):
        for tx in range(0, W, TILE):
            dr.rectangle([tx * sc, ty * sc, (tx + TILE) * sc, (ty + TILE) * sc], outline=(0, 140, 0))
            dr.text((tx * sc + 3, ty * sc + 3), f"{(ty // TILE) * 10 + tx // TILE:02d}", fill=(0, 140, 0))
    small.save(d / "overview.png")


def load_readings(site):
    f = HERE / "transcriptions" / f"{site}.py"
    spec = importlib.util.spec_from_file_location(f"tr_{site}", f); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.READ, m.ADDED


def cmd_build(site):
    d, _, _ = paths(site); s = SITES[site]; x0, y0 = s["window"][:2]
    cand = pd.read_csv(d / "candidates.csv"); READ, ADDED = load_readings(site)
    missing = set(cand.id) - set(READ)
    assert not missing, f"untranscribed detector ids: {sorted(missing)[:10]}"
    rows = [dict(id=r.id, win_x=r.cx, win_y=r.cy, fathoms=READ[r.id][0], status=READ[r.id][1], source="detector", note="")
            for r in cand.itertuples()]
    rows += [dict(id=f"A{i:03d}", win_x=x, win_y=y, fathoms=v, status=st, source="added by hand", note=n)
             for i, (x, y, v, st, n) in enumerate(ADDED)]
    df = pd.DataFrame(rows); df["chart_x"] = df.win_x + x0; df["chart_y"] = df.win_y + y0
    g = json.loads((ROOT / "data/processed/charts/admiralty_georef.json").read_text())[s["sheet"]]
    df["lat"] = g["lat_a"] * df.chart_y + g["lat_b"]
    df["lon"] = g["lon_anchor_deg"] + (df.chart_x - g["lon_anchor_px"]) / g["px_per_arcmin_lon"] / 60
    df["x_m"], df["y_m"] = Transformer.from_crs("EPSG:4326", f"EPSG:{UTM_EPSG}", always_xy=True).transform(df.lon.values, df.lat.values)
    df["depth_m"] = df.fathoms * FATHOM_M
    df.insert(0, "site", site); df.to_csv(d / f"soundings_{site}.csv", index=False)
    print(site, df.status.value_counts().to_dict(), "usable:", df.status.isin(["ok", "unsure"]).sum())


def cmd_check(site):
    d, _, out = paths(site); out.mkdir(parents=True, exist_ok=True)
    chart = Image.open(CHARTS / SITES[site]["file"])
    df = pd.read_csv(d / f"soundings_{site}.csv"); df = df[df.status.isin(["ok", "unsure", "later"])].reset_index(drop=True)
    W, H, S, COLS, ROWS = 64, 44, 2, 10, 8; per = COLS * ROWS
    for page in range(0, len(df), per):
        sub = df.iloc[page:page + per]
        sheet = Image.new("RGB", (COLS * W * S, ROWS * (H * S + 18)), "white"); dr = ImageDraw.Draw(sheet)
        for k, r in enumerate(sub.itertuples()):
            cx, cy = int(r.chart_x), int(r.chart_y)
            crop = chart.crop((cx - W // 2, cy - H // 2, cx + W // 2, cy + H // 2)).resize((W * S, H * S))
            px, py = (k % COLS) * W * S, (k // COLS) * (H * S + 18); sheet.paste(crop, (px, py))
            f = r.fathoms; txt = f"{r.id} = {int(f) if f == int(f) else f}{' ?' if r.status == 'unsure' else ''}{' L' if r.status == 'later' else ''}"
            dr.text((px + 3, py + H * S + 3), txt, fill=(200, 0, 0) if r.status != "ok" else (0, 0, 160))
        sheet.save(out / f"check_{page // per + 1}.png")
    print(site, len(df), "readings on", (len(df) + per - 1) // per, "sheets")


if __name__ == "__main__":
    cmd, site = sys.argv[1], sys.argv[2]
    {"detect": cmd_detect, "build": cmd_build, "check": cmd_check, "overview": cmd_overview}[cmd](site)
