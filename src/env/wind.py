"""Monthly wind climatology at each port and across the open-sea legs.

Evidence stream four, which was declared and never started. `DATA.md` listed
ERA5 as available, and ERA5 needs a Copernicus key. The NCEP reanalysis does
not, runs from 1948, and is served over OPeNDAP as plain text, so no netCDF
library is needed either.

The cost is resolution: 2.5 degrees, about 275 km. That is too coarse for a
harbour and about right for a monsoon, which is a planetary feature, and the
monsoon is the thing the Periplus is sailing on. Nothing here should be read as
a local wind at a river mouth.

Two quantities per month. Mean speed is obvious. Steadiness is the length of the
vector mean divided by the mean speed, so it runs from 0 when the wind blows
every way in turn to 1 when it never shifts. A square-rigged ship on a monsoon
crossing cares about the second at least as much as the first, because a strong
wind that boxes the compass is not a passage.
"""
import math, pathlib, urllib.request, csv

ROOT = pathlib.Path(__file__).resolve().parents[2]
CACHE = ROOT / "data" / "cache" / "wind"
OUT = ROOT / "data" / "processed"

BASE = ("https://psl.noaa.gov/thredds/dodsC/Datasets/ncep.reanalysis.derived/"
        "surface/{v}.mon.mean.nc.ascii")

START_YEAR = 1948            # the reanalysis begins in January of this year

# The seven port approaches, plus the open water each route actually crosses.
# The crossing points matter more than the ports here: the Periplus legs that
# depend on wind are the ones out of sight of land.
SITES = {
    "Muziris approach": (10.0, 76.0),
    "Tyndis approach": (11.0, 75.5),
    "Nelkynda approach": (9.0, 76.0),
    "Barbarikon approach": (24.0, 67.0),
    "Leukē Kōmē approach": (28.0, 35.0),
    "Rhapta approach": (-8.0, 39.5),
    "Arabian Sea crossing": (14.0, 60.0),
    "Guardafui, gulf mouth": (12.0, 51.0),
    "Malabar landfall": (10.0, 72.0),
    "Red Sea, middle": (20.0, 38.0),
    "Mozambique channel, north": (-8.0, 41.0),
}


def idx(lat, lon):
    """Nearest cell on the 2.5 degree grid. Latitude runs north to south."""
    return int(round((90.0 - lat) / 2.5)), int(round((lon % 360.0) / 2.5))


def fetch(var, i_lat, i_lon):
    """One grid cell's whole monthly series, cached."""
    CACHE.mkdir(parents=True, exist_ok=True)
    p = CACHE / f"{var}_{i_lat}_{i_lon}.txt"
    if not p.exists():
        u = (BASE.format(v=var)
             + f"?{var}%5B0:937%5D%5B{i_lat}:{i_lat}%5D%5B{i_lon}:{i_lon}%5D")
        with urllib.request.urlopen(u, timeout=180) as r:
            p.write_bytes(r.read())
    vals = []
    for line in p.read_text().splitlines():
        if not line.startswith("[") or "," not in line:
            continue
        try:
            v = float(line.split(",")[-1])
        except ValueError:
            continue
        vals.append(None if v < -1e30 else v)       # the file's missing value
    return vals


def climatology(lat, lon):
    """Mean u, v, speed and steadiness for each calendar month.

    Averaging u and v separately then taking the length gives the vector mean,
    which is not the mean speed: they differ by exactly the amount the wind
    shifts about, and their ratio is the steadiness.
    """
    i_lat, i_lon = idx(lat, lon)
    u, v = fetch("uwnd", i_lat, i_lon), fetch("vwnd", i_lat, i_lon)
    n = min(len(u), len(v))
    months = {m: [] for m in range(1, 13)}
    for k in range(n):
        if u[k] is None or v[k] is None:
            continue
        months[(k % 12) + 1].append((u[k], v[k]))

    out = {}
    for m, pairs in months.items():
        if not pairs:
            continue
        mu = sum(a for a, _ in pairs) / len(pairs)
        mv = sum(b for _, b in pairs) / len(pairs)
        scalar = sum(math.hypot(a, b) for a, b in pairs) / len(pairs)
        vec = math.hypot(mu, mv)
        # Meteorological convention: the direction the wind blows *from*.
        bearing = (math.degrees(math.atan2(-mu, -mv)) + 360) % 360
        out[m] = {"u": mu, "v": mv, "speed": scalar, "vector": vec,
                  "steadiness": vec / scalar if scalar else 0.0,
                  "from_deg": bearing, "years": len(pairs)}
    return out


def compass(deg):
    pts = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
           "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    return pts[int((deg + 11.25) % 360 // 22.5)]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, (lat, lon) in SITES.items():
        c = climatology(lat, lon)
        if not c:
            print(f"  {name:26s} no data")
            continue
        for m, d in sorted(c.items()):
            rows.append({"site": name, "lat": lat, "lon": lon, "month": m,
                         "speed_ms": round(d["speed"], 2),
                         "vector_ms": round(d["vector"], 2),
                         "steadiness": round(d["steadiness"], 3),
                         "from_deg": round(d["from_deg"]),
                         "from_compass": compass(d["from_deg"]),
                         "years": d["years"]})
        jul, jan = c[7], c[1]
        print(f"  {name:26s} Jul {jul['speed']:4.1f} m/s from {compass(jul['from_deg']):3s} "
              f"(steadiness {jul['steadiness']:.2f})   "
              f"Jan {jan['speed']:4.1f} m/s from {compass(jan['from_deg']):3s} "
              f"(steadiness {jan['steadiness']:.2f})", flush=True)
    dest = OUT / "wind_climatology.csv"
    with open(dest, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    print(f"\n{len(rows)} rows -> {dest.name}  "
          f"({START_YEAR} onward, NCEP reanalysis at 2.5 degrees)")


if __name__ == "__main__":
    main()
