"""Water history per port region: permanent, seasonal, and what has changed."""
import json, pathlib, sys
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[2]
recs = json.loads((ROOT/"data"/"processed"/"sat"/"water_history.json").read_text())
recs = [r for r in recs if r["region"] != "cholistan"]
recs.sort(key=lambda r: r["ever_water_km2"], reverse=True)

LABEL = {"pamba":"Nelkynda, Bakarē\nPamba and S. Vembanad",
         "rufiji":"Rhapta\nRufiji delta",
         "indus":"Barbarikon\nIndus delta",
         "tyndis":"Tyndis\nKadalundi to Ponnani",
         "periyar":"Muziris\nPeriyar delta",
         "aynuna":"Leukē Kōmē\nAynuna"}
INK, PERM, SEAS, LOST = "#1f2937", "#2563eb", "#7dd3fc", "#dc2626"

fig, ax = plt.subplots(1, 2, figsize=(13.5, 5.2), gridspec_kw={"width_ratios":[1.35,1]})
y = np.arange(len(recs))
perm = [r["permanent_km2"] for r in recs]
seas = [r["seasonal_km2"] for r in recs]
ax[0].barh(y, perm, color=PERM, label="permanent, all twelve months")
ax[0].barh(y, seas, left=perm, color=SEAS, label="seasonal")
ax[0].set_yticks(y); ax[0].set_yticklabels([LABEL[r["region"]] for r in recs], fontsize=9)
ax[0].invert_yaxis(); ax[0].set_xlabel("water surface, km²", fontsize=9)
ax[0].set_title("How much water, and how much of it comes and goes", fontsize=11, loc="left")
ax[0].legend(fontsize=8.5, frameon=False, loc="lower right")
for i, r in enumerate(recs):
    ax[0].text(r["ever_water_km2"]+10, i, f"{r['ever_water_km2']:.0f}", va="center", fontsize=8.5, color=INK)

pct = [100*r["lost_km2"]/max(r["ever_water_km2"],1e-9) for r in recs]
ax[1].barh(y, pct, color=LOST)
ax[1].set_yticks(y); ax[1].set_yticklabels([]); ax[1].invert_yaxis()
ax[1].set_xlabel("per cent of water surface lost since 1984", fontsize=9)
ax[1].set_title("Water lost, 1984 to 2021", fontsize=11, loc="left")
for i, v in enumerate(pct):
    ax[1].text(v+0.15, i, f"{v:.1f}%", va="center", fontsize=8.5, color=INK)
for a in ax:
    a.spines[["top","right"]].set_visible(False); a.tick_params(labelsize=8.5)
fig.suptitle("Modern water baseline from the JRC Landsat record, 1984 to 2021",
             fontsize=12.5, x=0.012, ha="left")
fig.text(0.012, -0.03, "The record begins eight years after the Thanneermukkom barrage and the Idukki dam, "
         "so it is a modern baseline, not a pre-dam reconstruction.", fontsize=8.5, color="#6b7280", ha="left")
fig.tight_layout(rect=[0,0,1,0.94])
fig.savefig(ROOT/"figures"/"26_water_history.png", dpi=150, bbox_inches="tight")
print("wrote figures/26_water_history.png")
