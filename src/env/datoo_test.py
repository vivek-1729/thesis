"""Datoo's meteorological case for Rhapta, tested against the reanalysis.

Datoo (1970) is the source of the Pangani-to-Rufiji bracket that every later
Rhapta argument inherits, and the project had been citing it at second hand.
Read directly, he does not simply give a bracket. He weights it, on
meteorological grounds, and the weighting is the part that gets dropped.

His argument, from Met Office pilot charts: the north-east monsoon blows with a
constancy of 41 to 60 per cent only as far as about 4 degrees south in February
and retreats to the equator in March. A ship out of the Red Sea arrives in East
Africa in late February or March, so "it would be imprudent to sail far to the
south of these limits if the length of sojourn in East African waters was
intended to be relatively short." He concludes that "a higher probability of
port location for trade with the Red Sea can be assigned to the northern rather
than the southern section of this locality, that is, to the stretch between
Pangani and Dar es Salaam."

That is a claim about where the north-east monsoon stops being dependable, made
from 1960s pilot charts, and it is now checkable against seventy-eight years of
reanalysis. This runs a latitude transect down the East African coast and asks
in which months, and how far south, the flow still has a northerly component and
holds steady.
"""
import csv, math, pathlib

from . import wind

OUT = pathlib.Path(__file__).resolve().parents[2] / "data" / "processed"

# The 2.5 degree grid fixes the latitudes available. These run from the equator
# to Cape Delgado, just offshore of the coast Datoo is arguing about.
TRANSECT = [(0.0, 40.0), (-2.5, 40.0), (-5.0, 40.0), (-7.5, 40.0), (-10.0, 40.0)]

# Datoo's threshold, restated. He reads constancy off a pilot chart; the
# reanalysis equivalent is steadiness, the vector mean over the scalar mean.
# His 41-60 per cent band brackets 0.5, so that is the line used here, and the
# result is reported either side of it rather than resting on it.
THRESHOLD = 0.5


def northerly(d):
    """Does the flow carry a northerly component, which is what a ship rides south?"""
    return math.cos(math.radians(d["from_deg"])) > 0


def main():
    rows = []
    print("East African coast, 40E. Steadiness and direction by month.\n")
    print(f"   {'lat':>6s} " + " ".join(f"{m:>5s}" for m in
          "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()))
    for lat, lon in TRANSECT:
        c = wind.climatology(lat, lon)
        if not c:
            print(f"   {lat:6.1f}  no data")
            continue
        cells = []
        for m in range(1, 13):
            d = c[m]
            mark = f"{d['steadiness']:.2f}"
            cells.append(mark if northerly(d) else "  ·  ")
            rows.append({"lat": lat, "lon": lon, "month": m,
                         "speed_ms": round(d["speed"], 2),
                         "steadiness": round(d["steadiness"], 3),
                         "from_deg": round(d["from_deg"]),
                         "from_compass": wind.compass(d["from_deg"]),
                         "northerly": "Y" if northerly(d) else "",
                         "meets_datoo": "Y" if (northerly(d) and
                                                d["steadiness"] >= THRESHOLD) else ""})
        print(f"   {lat:6.1f} " + " ".join(f"{c_:>5s}" for c_ in cells))
    print("\n   A number is the steadiness of a flow with a northerly component.")
    print("   A dot is a month when the wind is not out of the north at all.\n")

    # The question Datoo is answering: how far south does a dependable
    # north-easterly reach in the months a Red Sea ship would arrive?
    for m, name in ((2, "February"), (3, "March"), (1, "January")):
        ok = [r for r in rows if r["month"] == m and r["meets_datoo"] == "Y"]
        if ok:
            south = min(r["lat"] for r in ok)
            print(f"   {name:9s} dependable northerly reaches {abs(south):.1f} S")
        else:
            print(f"   {name:9s} no dependable northerly anywhere on the transect")

    dest = OUT / "east_africa_wind_transect.csv"
    with open(dest, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    print(f"\n-> {dest.name}")


if __name__ == "__main__":
    main()
