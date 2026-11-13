"""Model inputs for the seabed model at each candidate mouth.

For each site in sounding_sites.GEOMETRY this writes, to data/soundings/<site>/model/:
  soundings.csv   usable soundings (ok + unsure) on the sea side of the charted coast, in UTM 43N km,
                  with depth_m and dist_km (distance to the charted coast)
  shore.csv       shoreline anchors every 50 m along the coast, outside the mouth cut-out
  land.geojson    land and unsounded backwater east of the coast, minus the mouth cut-out
  domain.geojson  the sounding window
  grid.csv        prediction cells every 100 m in the water, with dist_km and the distance from ref
  site.json       mouth and ref points, counts, chart and survey

Kodungallur's inputs already exist (data/pilot_1857/local/) and are copied into the same layout, so every
site can be fitted and compared the same way.

  python seabed_inputs.py            all sites
  python seabed_inputs.py ponnani    one site
"""
import sys, json, pathlib
import numpy as np, pandas as pd, geopandas as gpd
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union, split
from pyproj import Transformer

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from sounding_sites import SITES, GEOMETRY, ROOT, UTM_EPSG

DATA = ROOT / "quantitative/coastline/data"
GEOREF = json.loads((ROOT / "data/processed/charts/admiralty_georef.json").read_text())
TO_UTM = Transformer.from_crs("EPSG:4326", f"EPSG:{UTM_EPSG}", always_xy=True)


def win_to_km(site, xy):
    """Window pixels -> UTM 43N km, through the sheet's own georeference."""
    s = SITES[site]; g = GEOREF[s["sheet"]]; x0, y0 = s["window"][:2]
    xy = np.asarray(xy, float).reshape(-1, 2)
    cx, cy = xy[:, 0] + x0, xy[:, 1] + y0
    lat = g["lat_a"] * cy + g["lat_b"]
    lon = g["lon_anchor_deg"] + (cx - g["lon_anchor_px"]) / g["px_per_arcmin_lon"] / 60
    e, n = TO_UTM.transform(lon, lat)
    return np.c_[e, n] / 1000


def write(out, snd, shore, land, dom, grid, meta):
    out.mkdir(parents=True, exist_ok=True)
    snd.to_csv(out / "soundings.csv", index=False); shore.to_csv(out / "shore.csv", index=False)
    gpd.GeoSeries([land]).to_file(out / "land.geojson", driver="GeoJSON")
    gpd.GeoSeries([dom]).to_file(out / "domain.geojson", driver="GeoJSON")
    grid.to_csv(out / "grid.csv", index=False)
    (out / "site.json").write_text(json.dumps(meta, indent=1))


def make_grid(water, coast, ref, step=0.1):
    x0, y0, x1, y1 = water.bounds
    xs, ys = np.meshgrid(np.arange(x0 + step / 2, x1, step), np.arange(y0 + step / 2, y1, step))
    p = gpd.GeoSeries(gpd.points_from_xy(xs.ravel(), ys.ravel()))
    keep = p.within(water).values
    g = pd.DataFrame(dict(x_km=xs.ravel()[keep], y_km=ys.ravel()[keep]))
    g["dist_km"] = [coast.distance(Point(a, b)) for a, b in zip(g.x_km, g.y_km)]
    g["d_ref_km"] = np.hypot(g.x_km - ref[0], g.y_km - ref[1])
    return g


def build(site):
    s, geo = SITES[site], GEOMETRY[site]
    out = DATA / "soundings" / site / "model"
    x0, y0, x1, y1 = s["window"]; W, H = x1 - x0, y1 - y0
    coast = LineString(win_to_km(site, geo["coast"]))
    corners = win_to_km(site, [(0, 0), (W, 0), (W, H), (0, H)])
    dom = Polygon(corners)
    # land: split the window along the coast, extended past the window at both ends, and keep the piece
    # that holds no soundings (the sea side holds them all)
    c = np.asarray(geo["coast"], float)
    ext = np.r_[[c[0] + (c[0] - c[1]) / np.hypot(*(c[0] - c[1])) * 3000], c,
                [c[-1] + (c[-1] - c[-2]) / np.hypot(*(c[-1] - c[-2])) * 3000]]
    pieces = split(dom, LineString(win_to_km(site, ext))).geoms
    t0 = pd.read_csv(DATA / "soundings" / site / f"soundings_{site}.csv")
    sea_pt = Point(*win_to_km(site, [t0[t0.status == "ok"][["win_x", "win_y"]].median().values])[0])
    land = unary_union([g for g in pieces if not g.contains(sea_pt)])
    mouth = ref = None
    if geo["mouth"] is not None:
        mouth = win_to_km(site, [geo["mouth"]])[0]
        land = land.difference(Point(*mouth).buffer(geo["mouth_r_km"]))
    ref = win_to_km(site, [geo["ref"]])[0]
    water = dom.difference(land)
    # shoreline anchors every 50 m along the coast, outside the mouth cut-out
    pts = [coast.interpolate(t) for t in np.arange(0, coast.length, 0.05)]
    if mouth is not None:
        pts = [p for p in pts if p.distance(Point(*mouth)) > geo["mouth_r_km"]]
    shore = pd.DataFrame(dict(x_km=[p.x for p in pts], y_km=[p.y for p in pts]))
    # soundings
    t = pd.read_csv(DATA / "soundings" / site / f"soundings_{site}.csv")
    t = t[t.status.isin(["ok", "unsure"])].copy()
    xy = win_to_km(site, t[["win_x", "win_y"]].values); t["x_km"], t["y_km"] = xy[:, 0], xy[:, 1]
    inside = gpd.GeoSeries(gpd.points_from_xy(t.x_km, t.y_km)).within(water).values
    snd = t[inside].copy()
    snd["dist_km"] = [coast.distance(Point(a, b)) for a, b in zip(snd.x_km, snd.y_km)]
    snd = snd[["id", "x_km", "y_km", "depth_m", "fathoms", "status", "dist_km"]]
    grid = make_grid(water, coast, ref)
    meta = dict(site=site, port=s["port"], candidates=s["candidates"], sheet=s["sheet"], surveyed=s["surveyed"],
                mouth=None if mouth is None else list(mouth), ref=list(ref), mouth_r_km=geo["mouth_r_km"],
                soundings_used=int(len(snd)), soundings_excluded_landward=int((~inside).sum()),
                shore_anchors=int(len(shore)), grid_cells=int(len(grid)), water_km2=round(water.area, 1))
    write(out, snd, shore, land, dom, grid, meta)
    return meta


def build_kodungallur():
    """Copy the existing Kodungallur local-model inputs into the common layout."""
    src = DATA / "pilot_1857" / "local"; out = DATA / "soundings" / "kodungallur" / "model"
    snd = pd.read_csv(src / "soundings.csv"); shore = pd.read_csv(src / "shore.csv")
    land = gpd.read_file(src / "land.geojson").geometry[0]; dom = gpd.read_file(src / "domain.geojson").geometry[0]
    mouth = pd.read_csv(src / "mouth.csv").iloc[0][["x_km", "y_km"]].values.astype(float)
    coast = land.boundary.difference(dom.boundary.buffer(0.02))
    snd = snd[["id", "x_km", "y_km", "depth_m", "fathoms", "status", "dist_km"]]
    # the lagoon behind the long spit and the river channel east of the mouth were not sounded; they stay in
    # the mesh, as in bathymetry_1857.ipynb, but get no predictions. Same polygons as that notebook's
    # UNSOUNDED_PX (window pixels of the Kodungallur window on BA 749), copied here.
    from detect_soundings import WINDOW
    UNSOUNDED_PX = [
        [(1145, 1102), (1240, 1050), (1280, 1100), (1320, 1150), (1350, 1200), (1380, 1250), (1400, 1300),
         (1415, 1350), (1420, 1400), (1418, 1450), (1412, 1500), (1250, 1500), (1245, 1350), (1240, 1250),
         (1225, 1190), (1200, 1150), (1165, 1110)],
        [(1160, 770), (1460, 762), (1460, 812), (1160, 822)]]
    g = GEOREF["BA749"]

    def kwin(p):
        p = np.asarray(p, float); cx, cy = p[:, 0] + WINDOW["x0"], p[:, 1] + WINDOW["y0"]
        lat = g["lat_a"] * cy + g["lat_b"]; lon = g["lon_anchor_deg"] + (cx - g["lon_anchor_px"]) / g["px_per_arcmin_lon"] / 60
        e, n = TO_UTM.transform(lon, lat); return np.c_[e, n] / 1000

    unsounded = unary_union([Polygon(kwin(p)) for p in UNSOUNDED_PX])
    water = dom.difference(land).difference(unsounded)
    grid = make_grid(water, coast, mouth)
    meta = dict(site="kodungallur", port="Muziris", candidates="Kodungallur (Azhikode) mouth", sheet="BA749",
                surveyed="1851-3", mouth=list(mouth), ref=list(mouth), mouth_r_km=0,
                soundings_used=int(len(snd)), soundings_excluded_landward=0, shore_anchors=int(len(shore)),
                grid_cells=int(len(grid)), water_km2=round(water.area, 1),
                note="inputs from bathymetry_1857.ipynb section 8b; the unsounded lagoon and river channel are in "
                     "the mesh but get no predictions, as in that notebook")
    write(out, snd, shore, land, dom, grid, meta)
    return meta


if __name__ == "__main__":
    names = sys.argv[1:] or ["kodungallur", *GEOMETRY]
    rows = [build_kodungallur() if n == "kodungallur" else build(n) for n in names]
    cols = ["site", "port", "sheet", "surveyed", "soundings_used", "soundings_excluded_landward", "shore_anchors", "grid_cells", "water_km2"]
    print(pd.DataFrame(rows)[cols].to_string(index=False))
