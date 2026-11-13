"""Join the hand transcription to detector positions and georeference.

Output: soundings_1857.csv with one row per sounding, chart pixel position,
lon/lat (from the sheet's own graticule), UTM 43N x/y, depth in fathoms and metres.
"""
import json, pathlib, sys
import numpy as np, pandas as pd
from pyproj import Transformer

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
from transcription_1857 import READ, ADDED
from detect_soundings import WINDOW

DATA = ROOT / "quantitative" / "coastline" / "data" / "soundings_1857"
FATHOM_M = 1.8288

cand = pd.read_csv(DATA / "candidates.csv")
missing = set(cand.id) - set(READ)
assert not missing, f"untranscribed detector ids: {sorted(missing)[:10]}"

rows = []
for r in cand.itertuples():
    val, status = READ[r.id]
    rows.append(dict(id=r.id, win_x=r.cx, win_y=r.cy, fathoms=val, status=status, source="detector", note=""))
for i, (x, y, val, status, note) in enumerate(ADDED):
    rows.append(dict(id=f"A{i:03d}", win_x=x, win_y=y, fathoms=val, status=status, source="added by hand", note=note))
df = pd.DataFrame(rows)
df["chart_x"] = df.win_x + WINDOW["x0"]; df["chart_y"] = df.win_y + WINDOW["y0"]

g = json.loads((ROOT / "data" / "processed" / "charts" / "admiralty_georef.json").read_text())["BA749"]
df["lat"] = g["lat_a"] * df.chart_y + g["lat_b"]
df["lon"] = g["lon_anchor_deg"] + (df.chart_x - g["lon_anchor_px"]) / g["px_per_arcmin_lon"] / 60
utm = Transformer.from_crs("EPSG:4326", "EPSG:32643", always_xy=True)
df["x_m"], df["y_m"] = utm.transform(df.lon.values, df.lat.values)
df["depth_m"] = df.fathoms * FATHOM_M
df.to_csv(DATA / "soundings_1857.csv", index=False)
print(df.status.value_counts().to_string())
print("usable soundings:", df.status.isin(["ok", "unsure"]).sum())
