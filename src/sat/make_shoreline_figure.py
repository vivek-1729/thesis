import pathlib, sys
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage
sys.path.insert(0, 'src')
from sat import shoreline, landsat_mss as mss, water, stack

ROOT = pathlib.Path('.')
BBOX = [76.30, 9.20, 76.60, 9.55]
EARLY, LATE = "1972-74", "1984-2021"
C_EARLY, C_LATE, INK = "#f59e0b", "#38bdf8", "#1f2937"

freq, meta = mss.water_extent(BBOX, "pamba", start="1972-01-01", end="1975-12-31")
w_early = freq > 0.6
gsw = water.surface_water(BBOX, shape=w_early.shape, layers=("occurrence",))
w_late = gsw["occurrence"] > 60
sea = {EARLY: shoreline.open_sea(w_early), LATE: shoreline.open_sea(w_late)}
H, W = w_early.shape
grid_m = (BBOX[2]-BBOX[0])*111320*np.cos(np.radians(9.375))/W
rows, err = shoreline.compare(sea, {EARLY:79.0, LATE:30.0}, grid_m, step=2)
comb = np.hypot(err[EARLY], err[LATE])
shift = np.array([r[LATE]-r[EARLY] for r in rows])
lat = np.array([BBOX[3]-(r["row"]/H)*(BBOX[3]-BBOX[1]) for r in rows])
sig = np.abs(shift) > comb

def st(a, lo=2, hi=98):
    v=a[np.isfinite(a)]; p0,p1=np.percentile(v,[lo,hi]); return np.clip((a-p0)/(p1-p0+1e-9),0,1)

mssc = mss.composite(BBOX)
early_img = np.dstack([st(mssc["nir08"]), st(mssc["red"]), st(mssc["green"])])
med,_,_ = stack.cached_composite("pamba", BBOX, "2022-01-01","2024-12-31","dry")
z = np.array(w_early.shape)/np.array(med["red"].shape)
late_img = np.dstack([ndimage.zoom(st(med[b]), z, order=1) for b in ("red","green","blue")])
late_img = np.clip(late_img,0,1)

fig, ax = plt.subplots(1, 3, figsize=(15.5, 6.8), gridspec_kw={"width_ratios":[1,1,1.2]})
for a,(img,lab,col,sub) in zip(ax[:2], [
        (early_img, EARLY, C_EARLY, f"Landsat MSS false colour, 79 m, {meta['n_scenes']} scenes  ·  ±{err[EARLY]:.0f} m"),
        (late_img,  LATE,  C_LATE,  f"Sentinel-2 true colour, with the 1984-2021 water record  ·  ±{err[LATE]:.0f} m")]):
    a.imshow(img)
    b = shoreline.boundary(sea[lab])
    b = ndimage.binary_dilation(b, iterations=1)
    ov = np.zeros((*b.shape,4)); ov[b] = list(plt.matplotlib.colors.to_rgb(col))+[1.0]
    a.imshow(ov)
    a.set_title(f"{lab}   extracted shoreline\n{sub}", fontsize=10, loc="left")
    a.set_xticks([]); a.set_yticks([])

ax[2].axvspan(-comb, comb, color="#9ca3af", alpha=.25, zorder=0)
ax[2].scatter(shift[~sig], lat[~sig], s=18, color="#9ca3af", zorder=3, label="within error")
ax[2].scatter(shift[sig], lat[sig], s=22, color="#1d4ed8", zorder=4, label="beyond error")
ax[2].axvline(0, color=INK, lw=.9)
ax[2].axhline(9.36, color="#b91c1c", lw=1.1, ls="--", zorder=2)
ax[2].text(ax[2].get_xlim()[0]+10, 9.365, "Purakkad", fontsize=9, color="#b91c1c", va="bottom")
ax[2].set_xlabel("shoreline movement, metres  (positive = seaward)", fontsize=9.5, labelpad=14)
ax[2].set_ylabel("latitude °N", fontsize=9.5)
ax[2].set_title(f"Movement between the epochs\nmedian {np.median(shift):+.0f} m overall; {sig.sum()} of {len(rows)} rows exceed ±{comb:.0f} m",
                fontsize=10, loc="left")
ax[2].legend(fontsize=8.5, frameon=False, loc="lower right")
ax[2].spines[["top","right"]].set_visible(False); ax[2].tick_params(labelsize=8.5)

fig.suptitle("Did the Purakkad coast move? Shoreline change across the 1976 barrage",
             fontsize=13.5, x=0.012, ha="left", y=0.985)
fig.text(0.012, 0.005,
  "Shoreline taken from the sea's own edge in each epoch and measured across-shore on every second raster row. Uncertainty is pixel size, threshold position\n"
  "and registration in quadrature. The coast is stable overall, but accretes about 180 m just north of Purakkad between 9.36 and 9.42°N. The 1700 and 1857\n"
  "charts enter this same pipeline as two earlier epochs once georeferenced.",
  fontsize=8.8, color="#4b5563", ha="left")
fig.tight_layout(rect=[0,0.05,1,0.972])
fig.savefig(ROOT/"figures"/"33_shoreline_change.png", dpi=145, bbox_inches="tight")
print("wrote figures/33_shoreline_change.png")
