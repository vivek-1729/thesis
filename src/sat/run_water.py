"""Water history for every port region, from the JRC 1984-2021 record."""
import json, pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from sat import water

OUT = pathlib.Path(__file__).resolve().parents[2] / "data" / "processed" / "sat"

# All seven ports plus the two arid controls. Boxes are drawn to hold the
# candidate sites and the water they would have used.
REGIONS = {
    "periyar":   ([76.10, 10.05, 76.45, 10.40], "Muziris: Periyar delta, Pattanam and Kodungallur"),
    "pamba":     ([76.25, 9.20, 76.60, 9.55], "Nelkynda and Bakare: Pamba and southern Vembanad"),
    "tyndis":    ([75.70, 11.00, 76.05, 11.35], "Tyndis: Kadalundi to Ponnani"),
    "indus":     ([67.30, 24.55, 67.85, 25.05], "Barbarikon: Indus delta around Banbhore"),
    "aynuna":    ([35.05, 27.95, 35.40, 28.30], "Leuke Kome: Aynuna and Khuraybah"),
    "rufiji":    ([39.00, -8.20, 39.50, -7.70], "Rhapta: Rufiji delta"),
    "cholistan": ([71.20, 28.68, 71.55, 28.98], "control: Hakra bed, Cholistan"),
}

if __name__ == "__main__":
    out = []
    for name, (bbox, note) in REGIONS.items():
        try:
            rec, gsw, lc = water.summarise(bbox, name)
        except Exception as e:
            print(f"{name:10s} FAILED: {type(e).__name__}: {str(e)[:90]}")
            continue
        rec["note"] = note
        out.append(rec)
        pct = 100 * rec["lost_km2"] / max(rec["ever_water_km2"], 1e-9)
        print(f"{name:10s} ever water {rec['ever_water_km2']:7.1f} km2 | "
              f"permanent {rec['permanent_km2']:7.1f} | seasonal {rec['seasonal_km2']:7.1f} | "
              f"lost {rec['lost_km2']:6.1f} ({pct:4.1f}%) | gained {rec['gained_km2']:6.1f} | "
              f"net {rec['net_change_km2']:+7.1f}")
    (OUT / "water_history.json").write_text(json.dumps(out, indent=1))
    print(f"\nwrote {OUT / 'water_history.json'}")
