"""How far the Muziris candidates sit from the shoreline Narayana 2001 maps.

Section 6 of `new_findings_v2.md` is the strongest negative result the project
has: the Periplus puts Muziris twenty stadia up the river from the shore, which
is 3.1 km at the calibrated stadion, and every candidate measures three to four
times that through the modern water network. Either the candidates are wrong or
the shoreline has moved.

Narayana, Priju and Chakrabarti 2001 draw a line they label ANCIENT SHORELINE
running inland of the modern coast from near Krishnan Kotta through Parur and
on south past Edapalli. `src/charts/narayana_fig2.py` georeferences that figure
to 67 m. This measures the candidates against the line.

**How the line was digitised, and what that costs.** By eye, off a render of the
figure with a two-arcminute graticule drawn on it from the fitted transform.
Five points, read where the drawn band crosses a latitude line. At the figure's
scale of 12.9 m per pixel a careful read is good to perhaps twenty pixels, so
each point carries roughly 300 m, and the georeference carries 67 m beneath
that. The result is therefore good to about a third of a kilometre, which is
enough to separate three kilometres from nine and not enough for anything
finer.

**What was traced, which is less than the paper describes.** The digitised
points cover the segment the figure letters ANCIENT SHORELINE, which runs from
about 10.156 N southward. The paper's text says the shoreline runs from
Krishnankotta through Parur and Ernakulam further to the south, and Krishnan
Kotta is north of where this tracing stops. So any candidate north of 10.156 N
is being measured to the end of a segment rather than to the line, and its
distance is an upper bound that should not be used to separate it from
anything. Kodungallur, at 10.226 N, is such a candidate.

**What the line is, and is not.** The paper offers it as a probable early
shoreline and assigns it no age at all, closing by saying that efforts are being
made to date the geomorphic elements. Its subject is Neogene evolution, so the
line is likely to be much older than the first century. It is therefore an inner
bound on where the coast has been, not a first-century coastline, and the modern
shore is the outer bound. Any first-century position lies between the two, which
is the only thing this script is entitled to conclude.
"""
import csv, math, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from charts.narayana_fig2 import CONTROL, fit, to_pixel  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parents[2] / "data" / "processed"

# Read north to south off the gridded render. Latitudes are the graticule lines
# the render drew; longitudes are where the band crosses them.
ANCIENT = [(10.1556, 76.2095), (10.1500, 76.2130), (10.1167, 76.2300),
           (10.0833, 76.2410), (10.0500, 76.2530)]
READ_ERROR_KM = 0.33

# Distance from the open sea through water, from `src/sat/run_route.py` at the
# fifty per cent threshold with the inferred rivers included.
MODERN_KM = {"Pattanam": 8.99, "Copeland model position": 8.99,
             "Kodungallur / Cranganore": 12.41}

CANDIDATES = {"Pattanam": (10.1536, 76.2131),
              "Kodungallur / Cranganore": (10.2256, 76.1950),
              "Copeland model position": (10.15654, 76.208982)}

STATED_STADIA = 20
STADION_M = {"calibrated 155 m": 155, "conventional 185 m": 185}


def km_between(a, b):
    """Local flat-earth distance, which at this size is exact enough."""
    mlat = math.radians(0.5 * (a[0] + b[0]))
    dx = (b[1] - a[1]) * 111.320 * math.cos(mlat)
    dy = (b[0] - a[0]) * 110.574
    return math.hypot(dx, dy)


def km_to_segment(p, a, b):
    """Shortest distance from a point to a segment, in km."""
    mlat = math.radians(p[0])
    def xy(q):
        return ((q[1] - a[1]) * 111.320 * math.cos(mlat),
                (q[0] - a[0]) * 110.574)
    px, py = xy(p)
    bx, by = xy(b)
    L2 = bx * bx + by * by
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, (px * bx + py * by) / L2))
    return math.hypot(px - t * bx, py - t * by)


def km_to_line(p, line=ANCIENT):
    return min(km_to_segment(p, line[i], line[i + 1])
               for i in range(len(line) - 1))


def main():
    length = sum(km_between(ANCIENT[i], ANCIENT[i + 1])
                 for i in range(len(ANCIENT) - 1))
    print(f"digitised ancient shoreline: {len(ANCIENT)} points, "
          f"{length:.1f} km, read to about {READ_ERROR_KM} km\n")
    for name, m in STADION_M.items():
        print(f"   {STATED_STADIA} stadia at {name} = "
              f"{STATED_STADIA * m / 1000:.2f} km")
    print()

    rows = []
    print(f"{'candidate':28s} {'to ancient':>11s} {'to modern sea':>14s} "
          f"{'bracket holds 3.1 km?':>22s}")
    for name, (la, lo) in CANDIDATES.items():
        anc = km_to_line((la, lo))
        mod = MODERN_KM.get(name)
        lo_b, hi_b = min(anc, mod), max(anc, mod)
        holds = lo_b - READ_ERROR_KM <= 3.1 <= hi_b
        # Beyond the traced segment only counts when it is beyond it by more
        # than the tracing is worth. Copeland sits 100 m north of the first
        # point, which is inside the read error and not off the line.
        north = (la - ANCIENT[0][0]) * 110.574 > READ_ERROR_KM
        note = "north of the trace" if north else str(holds)
        print(f"{name[:26]:28s} {anc:8.2f} km {mod:11.2f} km {note:>22s}")
        rows.append(dict(candidate=name, lat=la, lon=lo,
                         km_to_ancient_shoreline=round(anc, 2),
                         km_to_modern_sea_through_water=mod,
                         read_error_km=READ_ERROR_KM,
                         stated_stadia=STATED_STADIA,
                         stated_km_at_155m=round(STATED_STADIA * 0.155, 2),
                         bracket_contains_stated=("unusable, north of the trace"
                                                  if north else holds)))

    dest = OUT / "muziris_shoreline_bracket.csv"
    with open(dest, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    print(f"\n-> {dest.name}")
    print("\nThe bracket is between an undated line and the present coast. It "
          "says where\nthe shore can have been, not where it was.")


if __name__ == "__main__":
    main()
