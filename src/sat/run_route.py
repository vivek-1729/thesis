"""Measure the Malabar legs through water, which is how the text gives them.

The Periplus puts Muziris "distant from Tyndis by river and sea five hundred
stadia" and Nelkynda "distant from Muziris by river and sea about five hundred
stadia", and adds two short notices that are the unround and therefore more
trustworthy figures in the text: Muziris twenty stadia up the river from the
shore, Nelkynda one hundred and twenty stadia from the sea. Every reconstruction
this project has found measures the long legs as straight lines or as coastal
runs. Neither is what the sentence says, and CLAUDE.md calls this the single
most consequential unfinished measurement.

So this routes them through water. The network is modern, which is the honest
limitation and is restated in the output: the 1341 flood reorganised the
Vembanad and Gurukkal and Whittaker regard the result as not reconstructible.
These are not first-century distances. They are the first measurement of what
the text describes through any real water network, and what they establish is
how far a routed distance departs from the straight line everyone has used
instead, and in which direction.

Building a network a boat could use took four corrections, each forced by a
result that was obviously wrong.

**The sea has to be found, not read.** JRC is a land product and marks the ocean
as nodata 255, the same value it uses for everything it could not see. So the
sea here is the nodata region touching the frame, which separates the Arabian
Sea from nodata holes inland.

**A port must snap to the network, not to the nearest water.** Snapping to the
nearest water put Pattanam on an isolated pond a few hundred metres away, which
left it unreachable and reported every leg as having no route.

**A channel broken by the pixel grid is not a broken channel.** The Kuttanad
channels are about as wide as a 30 m Landsat pixel, so a reach that narrows
below one pixel registers as a gap and cuts the river in two. A small
morphological closing rejoins them, and it moved Kannetri from 3.3 km off the
network to 0.2 km.

**The sea is not where JRC's nodata is.** The two short notices are measured
from the sea inwards, so where the sea starts decides them. Taking it as the
nodata ocean put every Muziris candidate 30 km from the sea against a stated 20
stadia. The nodata ocean turns out to end a uniform 22 km offshore all along
this coast, because the near-shore strip is bright enough that JRC records it as
observed water rather than leaving it blank. Opening by reconstruction was tried and does not work
here, because the network is one component by construction, so reconstructing
from the eroded ocean gives the whole network back, lagoons included. What does
work has no tuning parameter in it: on this coast the sea lies to the west, so
the open sea is the water that has an unobstructed line due west to the frame.
A lagoon behind the barrier fails that test at every latitude except the mouths
themselves, which is correct, since a mouth is where the sea reaches in.

**Connectivity has to be counted the same way the route walks.**
`ndimage.label` uses four-connectivity by default, so two pixels touching only
at a corner belong to different components, while the path-finder steps
diagonally. A line drawn at a diagonal is therefore eight-connected to walk
along and four-disconnected to label, and the drawn river network came apart
into 25,123 components whose largest held 0.7 per cent of its pixels. Every
label here uses the eight-connected structure, which is what the router does.

**And the satellite cannot see a narrow river under trees.** Closing did nothing
for Niranam, which sat 13 km from navigable water at every threshold although it
is on the Pamba. Looking at the grid there, the only water within 13 km is the
Vembanad itself and a handful of ponds under half a square kilometre. The Pamba
is not in JRC at all above the lake, because Landsat at 30 m sees closed canopy
rather than the channel beneath it. HydroRIVERS, which is modelled from terrain
rather than observed from orbit, carries reaches of 37 cubic metres per second
past Niranam and 70 past Kottayam. Those are rivers. So the network is the union
of observed water and modelled river lines above a flow threshold, and the two
are reported separately because one is seen and the other is inferred.

Distances are reported as rankings and as ratios. No leg is fitted here.
"""
import csv, json, pathlib, sys

import numpy as np
from pyproj import Geod
from scipy import ndimage
from skimage.draw import line as bresenham
from skimage.graph import MCP_Geometric

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from sat import water  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "processed"
CACHE = ROOT / "data" / "cache" / "route"
RIVERS = OUT / "rivers_cache.json"
GEOD = Geod(ellps="WGS84")

# One box for the whole coast, because the legs run between ports and a
# per-port box would cut every route in half.
BBOX = [75.50, 8.75, 76.85, 11.55]

THRESHOLDS = (25, 50, 75)   # JRC occurrence, per cent
BRIDGE = 2                  # closing radius in pixels, about 60 m
MIN_FLOW = 5.0              # m3/s; below this HydroRIVERS is a creek

# Eight-connectivity, because that is how the router steps.
EIGHT = np.ones((3, 3), bool)


# Candidates per port. Tyndis, Nelkynda and Bakarē come from the curated table.
# Muziris is carried as an anchor with one position, so the two places that
# anchor actually stands for are named here too, because CLAUDE.md includes
# Muziris precisely because its security is narrower than it looks.
EXTRA = {
    "Muziris": [
        ("Pattanam", 10.1536, 76.2131),
        ("Kodungallur / Cranganore", 10.2256, 76.1950),
        ("Copeland model position", 10.15654, 76.208982),
    ],
}

LEGS = [
    ("Tyndis", "Muziris", 500, "by river and sea"),
    ("Muziris", "Nelkunda", 500, "by river and sea, 'about'"),
]

# The two upriver notices. Each is a distance from the open sea to the site
# through water, which is a different measurement from a leg between ports.
UPRIVER = [("Muziris", 20, "up the river from the shore"),
           ("Nelkunda", 120, "from the sea")]


def candidates():
    rows = list(csv.DictReader(open(ROOT / "data" / "raw" /
                                    "disputed_candidates.csv")))
    out = {}
    for r in rows:
        if not r["lat"].strip() or not r["lon"].strip():
            continue
        out.setdefault(r["port"].strip(), []).append(
            (r["candidate"].strip(), float(r["lat"]), float(r["lon"])))
    for port, items in EXTRA.items():
        out.setdefault(port, []).extend(items)
    return out


def grid():
    """JRC occurrence over the whole coast, cached because it is a slow read."""
    CACHE.mkdir(parents=True, exist_ok=True)
    p = CACHE / "malabar_occurrence.npz"
    if p.exists():
        return np.load(p)["occ"]
    print("   reading JRC occurrence over the whole Malabar coast ...")
    occ = water.surface_water(BBOX, layers=("occurrence",))["occurrence"]
    np.savez_compressed(p, occ=occ)
    return occ


def to_rc(lon, lat, shape):
    lon0, lat0, lon1, lat1 = BBOX
    return (int(round((lat1 - lat) / (lat1 - lat0) * shape[0])),
            int(round((lon - lon0) / (lon1 - lon0) * shape[1])))


def to_lonlat(r, c, shape):
    lon0, lat0, lon1, lat1 = BBOX
    return (lon0 + (c + 0.5) / shape[1] * (lon1 - lon0),
            lat1 - (r + 0.5) / shape[0] * (lat1 - lat0))


def river_mask(shape, min_flow=MIN_FLOW):
    """HydroRIVERS reaches drawn as one-pixel lines.

    Inferred, not observed, which is why it is kept as its own layer and
    reported separately. A reach below the flow threshold is a creek and would
    let a route cut across a watershed on a line nobody could row.
    """
    if not RIVERS.exists():
        return np.zeros(shape, bool), 0
    reaches = json.load(open(RIVERS))["kerala"]
    m = np.zeros(shape, bool)
    used = 0
    for r in reaches:
        if r["f"] < min_flow:
            continue
        pts = [to_rc(x, y, shape) for x, y in r["p"]]
        drawn = False
        for (r0, c0), (r1, c1) in zip(pts, pts[1:]):
            if not (0 <= r0 < shape[0] and 0 <= c0 < shape[1]
                    and 0 <= r1 < shape[0] and 0 <= c1 < shape[1]):
                continue
            rr, cc = bresenham(r0, c0, r1, c1)
            m[rr, cc] = True
            drawn = True
        used += drawn
    return m, used


def navigable(occ, thr, bridge=BRIDGE, rivers=None):
    """The water a boat could use, as one connected network.

    Observed water at or above the threshold and capped at 100, so the nodata
    value cannot pass as permanent water; unioned with the modelled river lines
    if they are given; closed by a small disc, which rejoins both the channels
    the pixel grid cut and the river reaches that meet a pixel apart; unioned
    with the sea; then reduced to the largest connected component, because a
    pond that joins nothing is not navigable however much water is in it.
    """
    inland = (occ >= thr) & (occ <= 100)
    if rivers is not None:
        inland = inland | rivers
    # Close after the union, not before. Closing the observed water first left
    # the drawn river lines joined to nothing: HydroRIVERS reaches meet at
    # shared endpoints that land a pixel or two apart once rounded to this
    # grid, so the chain breaks at every junction and the whole river falls out
    # of the largest component. Closing the union bridges those joins and the
    # joins to the lake in the same step.
    if bridge:
        k = np.ones((2 * bridge + 1, 2 * bridge + 1), bool)
        inland = ndimage.binary_closing(inland, structure=k)
    nodata = occ == 255
    lab, _ = ndimage.label(nodata, structure=EIGHT)
    edge = [i for i in np.unique(np.concatenate(
        [lab[:, 0], lab[:, -1], lab[0, :], lab[-1, :]])) if i]
    sea = np.isin(lab, edge) if edge else np.zeros_like(nodata)

    both = inland | sea
    comp, k = ndimage.label(both, structure=EIGHT)
    if k == 0:
        return both, sea, 0.0
    sizes = ndimage.sum(both, comp, range(1, k + 1))
    net = comp == (int(np.argmax(sizes)) + 1)
    return net, sea & net, float(sizes.max() / both.sum())


def open_sea(net):
    """The ocean, separated from the lagoons behind the barrier.

    A pixel is open sea when every pixel between it and the western frame is
    also water, which on a coast running north to south with the sea to the
    west is the same as saying a ship could reach it without crossing land.
    Computed as a running logical and along each row, so it costs one pass.

    This is the whole definition. It has nothing to tune, which matters because
    the two short notices in the text are measured from the sea and so depend
    entirely on where the sea is taken to begin.
    """
    return np.logical_and.accumulate(net, axis=1)


def snap(mask, rc, shape, max_px=800):
    """Nearest pixel of the network, and how far it was, in km."""
    r0, c0 = rc
    h, w = mask.shape
    if 0 <= r0 < h and 0 <= c0 < w and mask[r0, c0]:
        return (r0, c0), 0.0
    for rad in (25, 50, 100, 200, 400, max_px):
        r1, r2 = max(0, r0 - rad), min(h, r0 + rad + 1)
        c1, c2 = max(0, c0 - rad), min(w, c0 + rad + 1)
        sub = mask[r1:r2, c1:c2]
        if not sub.any():
            continue
        rr, cc = np.nonzero(sub)
        i = int(np.argmin((rr + r1 - r0) ** 2 + (cc + c1 - c0) ** 2))
        got = (int(rr[i] + r1), int(cc[i] + c1))
        a, b = to_lonlat(r0, c0, shape), to_lonlat(*got, shape)
        return got, GEOD.inv(a[0], a[1], b[0], b[1])[2] / 1000
    return None, None


def straight_km(a, b):
    return GEOD.inv(a[1], a[0], b[1], b[0])[2] / 1000


def main():
    occ = grid()
    shape = occ.shape
    lon0, lat0, lon1, lat1 = BBOX
    kx = GEOD.inv(lon0, (lat0 + lat1) / 2, lon1, (lat0 + lat1) / 2)[2] / 1000 / shape[1]
    ky = GEOD.inv((lon0 + lon1) / 2, lat0, (lon0 + lon1) / 2, lat1)[2] / 1000 / shape[0]
    print(f"grid {shape[0]} x {shape[1]}, pixel {kx*1000:.0f} x {ky*1000:.0f} m")

    riv, nreach = river_mask(shape)
    print(f"HydroRIVERS: {nreach} reaches at or above {MIN_FLOW} m3/s drawn\n")
    cands = candidates()

    rows, up_rows = [], []
    for thr in THRESHOLDS:
        for use_rivers in (False, True):
            tag = "observed + modelled rivers" if use_rivers else "observed only"
            net, sea, share = navigable(occ, thr, rivers=riv if use_rivers else None)
            print(f"=== occurrence >= {thr}%, {tag}: network is "
                  f"{100*net.mean():.1f}% of the box, {100*share:.1f}% of all water")

            costs = np.where(net, 1.0, np.inf)
            mcp = MCP_Geometric(costs, sampling=(ky, kx))

            # The legs between ports.
            for src, dst, stadia, how in LEGS:
                for sname, slat, slon in cands.get(src, []):
                    s_rc, s_snap = snap(net, to_rc(slon, slat, shape), shape)
                    if s_rc is None:
                        continue
                    cum, _ = mcp.find_costs([s_rc])
                    for dname, dlat, dlon in cands.get(dst, []):
                        d_rc, d_snap = snap(net, to_rc(dlon, dlat, shape), shape)
                        if d_rc is None:
                            continue
                        routed = float(cum[d_rc])
                        routed = None if not np.isfinite(routed) else routed
                        sl = straight_km((slat, slon), (dlat, dlon))
                        # The ratio has to compare like with like. A route runs
                        # between the snapped pixels, so comparing it to the
                        # straight line between the unsnapped sites made
                        # Nakkada, which snaps 16 km, look like a route shorter
                        # than a geodesic.
                        sa = to_lonlat(*s_rc, shape)
                        sb = to_lonlat(*d_rc, shape)
                        sl_snap = straight_km((sa[1], sa[0]), (sb[1], sb[0]))
                        rows.append(dict(
                            threshold=thr, network=tag, leg=f"{src} to {dst}",
                            stated_stadia=stadia, how=how,
                            origin=sname, destination=dname,
                            routed_km=None if routed is None else round(routed, 1),
                            straight_km=round(sl, 1),
                            straight_snapped_km=round(sl_snap, 1),
                            ratio=None if routed is None else round(routed / sl_snap, 2),
                            snap_origin_km=round(s_snap, 2),
                            snap_dest_km=round(d_snap, 2),
                            implied_stadion_m=(None if routed is None else
                                               round(routed * 1000 / stadia, 1))))

            # The two upriver notices, measured from the open sea inwards.
            ocean = open_sea(net)
            sea_rc = [tuple(x) for x in np.argwhere(ocean)[::2000]]
            if sea_rc:
                cum_sea, _ = mcp.find_costs(sea_rc)
                for port, stadia, how in UPRIVER:
                    for name, la, lo in cands.get(port, []):
                        p_rc, p_snap = snap(net, to_rc(lo, la, shape), shape)
                        if p_rc is None:
                            continue
                        d = float(cum_sea[p_rc])
                        d = None if not np.isfinite(d) else d
                        up_rows.append(dict(
                            threshold=thr, network=tag, port=port,
                            candidate=name, stated_stadia=stadia, how=how,
                            from_sea_km=None if d is None else round(d, 2),
                            snap_km=round(p_snap, 2),
                            implied_stadion_m=(None if d is None else
                                               round(d * 1000 / stadia, 1))))
            print()

    for name, data in (("malabar_routed.csv", rows),
                       ("malabar_upriver.csv", up_rows)):
        dest = OUT / name
        with open(dest, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(data[0]))
            w.writeheader()
            w.writerows(data)
        print(f"{len(data)} rows -> {dest.name}")

    ok = [r for r in rows if r["ratio"] is not None]
    rs = sorted(r["ratio"] for r in ok)
    print(f"\nrouted / straight over {len(ok)} pairs: median {rs[len(rs)//2]:.2f}, "
          f"range {rs[0]:.2f} to {rs[-1]:.2f}")


if __name__ == "__main__":
    main()
