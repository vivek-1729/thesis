"""Contact sheets for checking the transcription: each sounding's chart crop
beside the value entered for it. Used for the second-pass check and for anyone
re-verifying by eye."""
import pathlib
import pandas as pd
from PIL import Image, ImageDraw

Image.MAX_IMAGE_PIXELS = None
ROOT = pathlib.Path(__file__).resolve().parents[3]
DATA = ROOT / "quantitative" / "coastline" / "data" / "soundings_1857"
chart = Image.open(ROOT.parent / "library" / "charts" / "malabar-749-1857.jpg")

df = pd.read_csv(DATA / "soundings_1857.csv")
df = df[df.status.isin(["ok", "unsure"])].reset_index(drop=True)
W, H, S, COLS, ROWS = 64, 44, 2, 10, 8
out = DATA / "check"; out.mkdir(exist_ok=True)
per = COLS * ROWS
for page in range(0, len(df), per):
    sub = df.iloc[page:page + per]
    sheet = Image.new("RGB", (COLS * W * S, ROWS * (H * S + 18)), "white")
    d = ImageDraw.Draw(sheet)
    for k, r in enumerate(sub.itertuples()):
        cx, cy = int(r.chart_x), int(r.chart_y)
        crop = chart.crop((cx - W // 2, cy - H // 2, cx + W // 2, cy + H // 2)).resize((W * S, H * S))
        x0, y0 = (k % COLS) * W * S, (k // COLS) * (H * S + 18)
        sheet.paste(crop, (x0, y0))
        f = r.fathoms
        txt = f"{r.id} = {int(f) if f == int(f) else f}{' ?' if r.status == 'unsure' else ''}"
        d.text((x0 + 3, y0 + H * S + 3), txt, fill=(200, 0, 0) if r.status == "unsure" else (0, 0, 160))
    sheet.save(out / f"check_{page // per + 1}.png")
print(len(df), "soundings on", (len(df) + per - 1) // per, "sheets")
