"""Do Roman coin hoards in South India sit at the ports or behind them?

If hoards clustered at harbours, the coin layer would help locate a port. The
standing suspicion in the literature (Tomber, Suresh) is that they do not --
that coins travelled inland and were hoarded near the sources of pepper and
beryl, along the Palghat gap. This measures it.

Distance to coast comes from Natural Earth 10m, which is coarse for a single
site but fine for separating 'on the shore' from '100 km inland'.
"""
import csv, math, pathlib, shapefile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CH = ROOT / "data" / "raw" / "chre"

# CHRE gives Kottayam 1847 coordinates in central Kerala, but its own county
# field says Kannur and its summary says the coins were found "on the slope of
# a hill by the sea". Central Kottayam is ~35 km inland behind the Vembanad
# backwaters. The coordinates are wrong; the record is excluded from
# distance-based analysis rather than silently trusted.
SUSPECT = {"18598"}

def coast_points(bbox):
    sf = shapefile.Reader(str(ROOT / "data" / "raw" / "ne10m" / "ne_10m_coastline"))
    pts = []
    for s in sf.shapes():
        x0, y0, x1, y1 = s.bbox
        if x1 < bbox[0] or x0 > bbox[2] or y1 < bbox[1] or y0 > bbox[3]:
            continue
        pts.extend(s.points)
    return pts

def km(a, b, c, d):
    p = math.pi / 180
    return 6371 * math.acos(max(-1, min(1, math.sin(a*p)*math.sin(c*p)
            + math.cos(a*p)*math.cos(c*p)*math.cos((d-b)*p))))

def main():
    H = list(csv.DictReader(open(CH / "chre_hoards.csv")))
    def f(v):
        try: return float(v)
        except: return None

    sub = [x for x in H if x["_query_country"] in ("India", "Sri Lanka", "Pakistan")
           and f(x["latitude"]) is not None and x["id"] not in SUSPECT]
    pts = coast_points((66, 5, 92, 28))
    print(f"{len(pts)} coastline vertices in the South Asia window")

    out = []
    for x in sub:
        la, lo = f(x["latitude"]), f(x["longitude"])
        d = min(km(la, lo, p[1], p[0]) for p in pts)
        n = int(x["coinCount"] or 0)
        out.append((d, n, x))

    bands = [(0, 10), (10, 25), (25, 50), (50, 100), (100, 200), (200, 10000)]
    print(f"\n{'distance to coast':22s}{'hoards':>8}{'coins':>10}{'median coins':>14}")
    for lo_, hi in bands:
        g = [(d, n) for d, n, _ in out if lo_ <= d < hi]
        if not g: continue
        ns = sorted(n for _, n in g)
        med = ns[len(ns)//2]
        lbl = f"{lo_}-{hi} km" if hi < 10000 else f"{lo_}+ km"
        print(f"  {lbl:20s}{len(g):>8}{sum(ns):>10}{med:>14}")

    print(f"\nlargest hoards, with distance inland:")
    for d, n, x in sorted(out, key=lambda t: -t[1])[:14]:
        print(f"  {x['hoardName'][:26]:26s} {n:>6} coins  {d:6.1f} km inland  "
              f"term={x['terminalYear1'] or '?':>5}  {x.get('county','')[:18]}")

    coastal = [(d, n) for d, n, _ in out if d <= 25]
    inland = [(d, n) for d, n, _ in out if d > 25]
    print(f"\ncoastal (<=25 km): {len(coastal)} hoards, {sum(n for _, n in coastal):,} coins")
    print(f"inland  (> 25 km): {len(inland)} hoards, {sum(n for _, n in inland):,} coins")
    tot = sum(n for _, n in coastal) + sum(n for _, n in inland)
    if tot:
        print(f"inland share of all recorded coins: "
              f"{100*sum(n for _, n in inland)/tot:.0f}%")

    dest = ROOT / "data" / "processed" / "chre_hoard_distances.csv"
    with open(dest, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "hoardName", "country", "county", "lat", "lon",
                    "coinCount", "terminalYear1", "dist_to_coast_km"])
        for d, n, x in sorted(out, key=lambda t: t[0]):
            w.writerow([x["id"], x["hoardName"], x["_query_country"], x.get("county", ""),
                        x["latitude"], x["longitude"], n, x["terminalYear1"], round(d, 1)])
    print(f"\n-> {dest.name}")

if __name__ == "__main__":
    main()
