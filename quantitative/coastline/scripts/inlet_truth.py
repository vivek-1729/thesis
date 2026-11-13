"""Synthetic 'Selby surveys' of fully surveyed modern inlets, for validation_bathymetry.ipynb.

For one inlet this writes, to data/cache/validation/<site>/:
  eval.csv          the true seabed on a 100 m grid inside a local box the size of the Kerala one
  shore.csv, land.geojson, domain.geojson, mouth.csv
  maximin_grid.npy, endpoints.csv, truth.csv   for the controlling depth of the pass
  rep_<k>.csv       replicate surveys at the Kerala density and distance-offshore profile
  repch_<k>.csv     the same surveys plus a line of soundings down the true channel over the bar
"""
import pathlib, warnings
import numpy as np, pandas as pd, geopandas as gpd, rasterio
from rasterio.warp import reproject, Resampling, calculate_default_transform
from rasterio import features
from scipy import ndimage
from shapely.geometry import shape, box
from shapely.ops import unary_union
from shapely.affinity import scale as _scale
from pyproj import Transformer

ROOT = pathlib.Path(__file__).resolve().parents[3]
CUDEM = "/vsicurl/https://noaa-nos-coastal-lidar-pds.s3.amazonaws.com/dem/NCEI_ninth_Topobathy_2014_8483/TX/"
SITES = {  # CUDEM tiles, UTM EPSG, pass lon/lat, seaward azimuth, box offsets from the pass (W, S, E, N, km), name
    "slp": (["ncei19_n29x25_w095x25_2021v2.tif", "ncei19_n29x00_w095x25_2021v2.tif"], 32615, (-95.117, 29.083), 150,
            (-5, -4.5, 4, 4.5), "San Luis Pass"),
    "pc": (["ncei19_n28x50_w096x50_2021v1.tif"], 32614, (-96.386, 28.384), 135, (-6, -5.5, 2.5, 3), "Pass Cavallo"),
}
RES, FATHOM = 0.05, 1.8288


CACHE = {"slp": "san_luis_pass_50m.tif", "pc": "pass_cavallo_50m.tif"}


def fetch(site):
    """Average the 1/9 arc-second tiles (about 3 m) to about 50 m and cache them; tiles are stacked north to south."""
    out = ROOT / "data/cache/cudem" / CACHE[site]
    if out.exists():
        return out
    out.parent.mkdir(parents=True, exist_ok=True)
    arrs, trs = [], []
    for t in SITES[site][0]:
        with rasterio.open(CUDEM + t) as s:
            a = s.read(1, out_shape=(s.height // 18, s.width // 18), resampling=Resampling.average).astype("float32")
            a[a <= -9999] = np.nan; crs = s.crs
            trs.append(s.transform * rasterio.Affine.scale(s.width / a.shape[1], s.height / a.shape[0])); arrs.append(a)
    order = np.argsort([-t.f for t in trs])
    a = np.vstack([arrs[i] for i in order]); tr = trs[order[0]]
    with rasterio.open(out, "w", driver="GTiff", height=a.shape[0], width=a.shape[1], count=1, dtype="float32",
                       crs=crs, transform=tr, nodata=np.nan) as d:
        d.write(a, 1)
    return out


def maximin(depth, gr, gc, a, b, iters=25):
    """Controlling depth: the deepest threshold at which cells a and b are joined by water deeper than it."""
    G = np.full((gr.max() + 1, gc.max() + 1), -99.0); G[gr, gc] = depth
    lo, hi = -5.0, min(depth[a], depth[b])
    for _ in range(iters):
        m = (lo + hi) / 2; lab, _ = ndimage.label(G > m, structure=np.ones((3, 3)))
        lo, hi = (m, hi) if lab[gr[a], gc[a]] and lab[gr[a], gc[a]] == lab[gr[b], gc[b]] else (lo, m)
    return lo


def build(site, n_rep=12, kerala_local=None):
    warnings.filterwarnings("ignore")
    tiles, epsg, pll, AZ, off, name = SITES[site]
    OUT = ROOT / f"data/cache/validation/{site}"; OUT.mkdir(parents=True, exist_ok=True)
    with rasterio.open(fetch(site)) as src:
        tr, w, h = calculate_default_transform(src.crs, f"EPSG:{epsg}", src.width, src.height, *src.bounds, resolution=RES * 1000)
        elev = np.full((h, w), np.nan, "float32")
        reproject(src.read(1), elev, src_transform=src.transform, src_crs=src.crs, dst_transform=tr, dst_crs=f"EPSG:{epsg}",
                  resampling=Resampling.bilinear, src_nodata=np.nan, dst_nodata=np.nan)
    H, W = elev.shape
    xs = (tr.c + (np.arange(W) + .5) * tr.a) / 1000; ys = (tr.f + (np.arange(H) + .5) * tr.e) / 1000
    XX, YY = np.meshgrid(xs, ys)
    inlet = np.array(Transformer.from_crs("EPSG:4326", f"EPSG:{epsg}", always_xy=True).transform(*pll)) / 1000
    bx = box(inlet[0] + off[0], inlet[1] + off[1], inlet[0] + off[2], inlet[1] + off[3])
    inb = (XX > bx.bounds[0]) & (XX < bx.bounds[2]) & (YY > bx.bounds[1]) & (YY < bx.bounds[3])
    assert np.isfinite(elev[inb]).all(), "box runs off the DEM"
    elev = np.where(np.isfinite(elev), elev, 99)
    land = ndimage.binary_opening(elev > 0.2, iterations=1)
    shelter = np.zeros_like(land)                      # a 4 km ray towards the open sea meets land: behind the barrier
    for k in range(1, int(4 / RES)):
        dc, dr = int(round(k * np.sin(np.radians(AZ)))), int(round(-k * np.cos(np.radians(AZ))))
        sh = np.zeros_like(land)
        sh[max(0, -dr):H - max(0, dr), max(0, -dc):W - max(0, dc)] = land[max(0, dr):H - max(0, -dr), max(0, dc):W - max(0, -dc)]
        shelter |= sh
    shelter &= ~land
    polys = [shape(g) for g, v in features.shapes((land & inb).astype("uint8"), transform=tr) if v == 1]
    land_l = _scale(unary_union([p for p in polys if p.area > 5e4]).simplify(30), 1e-3, 1e-3, origin=(0, 0)).intersection(bx)
    coast = land_l.boundary.difference(bx.boundary.buffer(0.02))
    dist = ndimage.distance_transform_edt(~land) * RES
    sel = inb & ~land
    ev = pd.DataFrame(dict(x_km=XX[sel], y_km=YY[sel], depth_true=-elev[sel], dist_km=dist[sel], lagoon=shelter[sel].astype(int)))
    ev["r"], ev["c"] = np.nonzero(sel)
    ev["d_mouth"] = np.hypot(ev.x_km - inlet[0], ev.y_km - inlet[1])
    ev = ev[(ev.r % 2 == 0) & (ev.c % 2 == 0)].reset_index(drop=True)       # 100 m
    ev.to_csv(OUT / "eval.csv", index=False)
    pd.DataFrame([(p.x, p.y) for p in (coast.interpolate(u) for u in np.arange(0, coast.length, 0.05))],
                 columns=["x_km", "y_km"]).to_csv(OUT / "shore.csv", index=False)
    gpd.GeoSeries([land_l]).to_file(OUT / "land.geojson", driver="GeoJSON")
    gpd.GeoSeries([bx]).to_file(OUT / "domain.geojson", driver="GeoJSON")
    pd.DataFrame(dict(x_km=[inlet[0]], y_km=[inlet[1]])).to_csv(OUT / "mouth.csv", index=False)

    # controlling depth from 3 km offshore of the pass to its throat, on the open-side 100 m cells
    o = ev[ev.lagoon == 0].reset_index(drop=True)
    gr, gc = (o.r // 2).values, (o.c // 2).values; gr = gr - gr.min(); gc = gc - gc.min()
    p_off = inlet + 3 * np.array([np.sin(np.radians(AZ)), np.cos(np.radians(AZ))])
    a = int(np.argmin(np.hypot(o.x_km - p_off[0], o.y_km - p_off[1])))
    near = np.where(o.d_mouth < 0.5)[0]; b = int(near[np.argmax(o.depth_true.values[near])])
    np.save(OUT / "maximin_grid.npy", np.c_[gr, gc]); pd.DataFrame(dict(a=[a], b=[b])).to_csv(OUT / "endpoints.csv", index=False)
    cd = maximin(o.depth_true.values, gr, gc, a, b)
    pd.DataFrame(dict(controlling_depth=[cd])).to_csv(OUT / "truth.csv", index=False)

    # fine-scale relief: what a 250 m Gaussian smoothing removes from the true seabed, by zone
    G = np.full((gr.max() + 1, gc.max() + 1), np.nan); G[gr, gc] = o.depth_true; M = np.isfinite(G)
    sm = ndimage.gaussian_filter(np.where(M, G, 0), 2.5) / np.maximum(ndimage.gaussian_filter(M.astype(float), 2.5), 1e-9)
    o["fine"] = (G - sm)[gr, gc]
    relief = {k: float(o.fine[m].std()) for k, m in {
        "pass <1 km": o.d_mouth < 1, "pass 1-2 km": (o.d_mouth >= 1) & (o.d_mouth < 2),
        "shore <1 km": (o.dist_km < 1) & (o.d_mouth >= 2), "offshore": (o.dist_km >= 1) & (o.d_mouth >= 2)}.items()}

    # replicate surveys at the Kerala local-box density and distance-offshore profile
    P = ROOT / "quantitative/coastline/data/pilot_1857/local"
    kl = pd.read_csv(P / "soundings.csv")
    kdom = gpd.read_file(P / "domain.geojson").geometry[0]; kland = gpd.read_file(P / "land.geojson").geometry[0]
    dens = len(kl) / kdom.difference(kland).area
    full = pd.DataFrame(dict(x_km=XX[sel], y_km=YY[sel], depth_true=-elev[sel], dist_km=dist[sel], lagoon=shelter[sel]))
    open_w = full[~full.lagoon & (full.dist_km <= kl.dist_km.max())]
    bins = np.r_[0, 0.25, 0.5, 1, 1.5, 2, 3, 4, 5, 8]
    target = np.histogram(kl.dist_km, bins)[0] / len(kl); have = np.histogram(open_w.dist_km, bins)[0]
    wts = np.nan_to_num(target / np.maximum(have, 1))[np.clip(np.digitize(open_w.dist_km, bins) - 1, 0, len(bins) - 2)]
    n_target = int(dens * len(full) * RES**2)

    def bad(x, y):
        c = np.clip(((np.asarray(x) * 1000 - tr.c) / tr.a).astype(int), 0, W - 1)
        r = np.clip(((np.asarray(y) * 1000 - tr.f) / tr.e).astype(int), 0, H - 1)
        return land[r, c] | shelter[r, c], dist[r, c]

    # the channel line: soundings every 150 m along the true deepest path within 2 km of the pass
    from skimage.graph import route_through_array
    Gd = np.full((gr.max() + 1, gc.max() + 1), -99.0); Gd[gr, gc] = o.depth_true
    cost = np.where(Gd >= cd - 1e-6, 1 + 1 / np.maximum(Gd - cd + 0.1, 0.1), 1e6)
    path, _ = route_through_array(cost, (gr[a], gc[a]), (gr[b], gc[b]), fully_connected=True, geometric=True)
    cell = {(r_, c_): i for i, (r_, c_) in enumerate(zip(gr, gc))}
    pidx = np.array([cell[tuple(p)] for p in path]); pidx = pidx[o.d_mouth.values[pidx] < 2.0]
    xy = o[["x_km", "y_km"]].values[pidx]; keep = [0]
    for i in range(1, len(xy)):
        if np.hypot(*(xy[i] - xy[keep[-1]])) >= 0.15:
            keep.append(i)
    line = o.iloc[pidx[keep]]

    cols = ["x_km", "y_km", "depth_m", "depth_true", "dist_km", "d_mouth"]
    for k in range(n_rep):
        rg = np.random.default_rng(500 + k)
        cand = open_w.sample(n=6 * n_target, weights=wts, random_state=500 + k); pts = []
        for row in cand.itertuples():                  # greedy thinning to ~250 m spacing
            if all((row.x_km - q.x_km)**2 + (row.y_km - q.y_km)**2 > 0.25**2 for q in pts):
                pts.append(row)
            if len(pts) >= n_target:
                break
        s = pd.DataFrame(pts)
        s["x_km"] += rg.normal(0, 0.06, len(s)); s["y_km"] += rg.normal(0, 0.06, len(s))   # 60 m position error
        bd, dd = bad(s.x_km, s.y_km); s = s[~bd].copy(); s["dist_km"] = dd[~bd]
        s["d_mouth"] = np.hypot(s.x_km - inlet[0], s.y_km - inlet[1])
        s["depth_m"] = np.round((s.depth_true + rg.normal(0, 0.3, len(s))) / FATHOM * 4) / 4 * FATHOM
        s[cols].to_csv(OUT / f"rep_{k}.csv", index=False)
        rc = np.random.default_rng(900 + k)
        l = line[["x_km", "y_km", "depth_true", "dist_km", "d_mouth"]].copy()
        l["depth_m"] = np.round((l.depth_true + rc.normal(0, 0.3, len(l))) / FATHOM * 4) / 4 * FATHOM
        pd.concat([s[cols], l[cols]], ignore_index=True).to_csv(OUT / f"repch_{k}.csv", index=False)
    return dict(site=site, name=name, box_km=f"{bx.bounds[2]-bx.bounds[0]:.1f} x {bx.bounds[3]-bx.bounds[1]:.1f}",
                cells=len(o), sheltered_share=round(float(ev.lagoon.mean()), 2), soundings=len(s),
                within_1km_of_pass=int((s.d_mouth < 1).sum()), channel_line=len(line),
                controlling_depth=round(cd, 2), **{f"relief {k}": round(v, 2) for k, v in relief.items()})


if __name__ == "__main__":
    import sys
    for s in sys.argv[1:] or SITES:
        print(build(s))
