"""Pre-extract HydroRIVERS reaches for the study windows.

HydroRIVERS ships ~1.4M reaches per continent with no spatial index, so scanning it
once per map panel is hopeless. Clip to the four windows we care about, keep only
reaches with real flow, and cache as compact JSON.
"""
import json
from pathlib import Path

import shapefile

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data/raw/hydrorivers"
OUT = ROOT / "data/processed/rivers_cache.json"

WINDOWS = {                       # name: (lon0, lon1, lat0, lat1)
    "kerala":   (74.3, 78.2,  7.6, 12.4),
    "indus":    (65.5, 70.5, 22.5, 26.5),
    "tanzania": (37.5, 41.5, -9.5, -4.0),
    "nwarabia": (33.5, 38.5, 23.5, 29.5),
}
MIN_FLOW = 0.4                    # m3/s — below this it is a seasonal creek


def main():
    out = {k: [] for k in WINDOWS}
    for shp in sorted(SRC.glob("HydroRIVERS_v10_*_shp/*.shp")):
        r = shapefile.Reader(str(shp))
        fields = [f[0] for f in r.fields[1:]]
        i_flow, i_ord = fields.index("DIS_AV_CMS"), fields.index("ORD_STRA")
        kept = 0
        for sr in r.iterShapeRecords():
            rec = sr.record
            if rec[i_flow] is None or rec[i_flow] < MIN_FLOW:
                continue
            pts = sr.shape.points
            if not pts:
                continue
            xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
            for name, (x0, x1, y0, y1) in WINDOWS.items():
                if max(xs) < x0 or min(xs) > x1 or max(ys) < y0 or min(ys) > y1:
                    continue
                out[name].append({"o": int(rec[i_ord]), "f": round(float(rec[i_flow]), 2),
                                  "p": [[round(x, 4), round(y, 4)] for x, y in pts]})
                kept += 1
        print(f"  {shp.parent.name}: kept {kept}")
    OUT.write_text(json.dumps(out))
    print(f"\nwrote {OUT}  ({OUT.stat().st_size//1024} KB)")
    for k, v in out.items():
        print(f"  {k:10s} {len(v):5d} reaches")


if __name__ == "__main__":
    main()
