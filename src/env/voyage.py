"""Sail the Periplus route on the wind climatology, month by month.

The text states its own sailing season four times and in the same words: the
voyage from Egypt is made "about the month of July, that is Epiphi". Chapter 57
adds the mechanism, that the southwest wind the Greeks called Hippalus blows on
to the Indian shore while the Etesians blow at home, and it adds a detail that
is a quantitative claim rather than a general one. Those bound for Limyrike,
the Malabar coast, "throw the ship's head considerably off the wind", while
those bound for Barygaza, far to the north, do not.

So there are three things here that the wind record can be asked about without
anyone deciding first where a port was.

Is July actually the month? Does the Malabar course sit further off the summer
wind than the Barygaza course, which is what chapter 57 says and what no one
seems to have checked against a wind field? And does the round trip close
inside a year, since a ship that cannot get home is a ship that was never
sent.

**The ship.** Performance comes from Whitewright 2011 on ancient Mediterranean
rigs, which is the nearest measured evidence to a first-century hull and is
built from replica trials and historical observation rather than from a model.
A single square sail, close-hauled, holds a heading of sixty to sixty-five
degrees off the wind in light to moderate airs and calm seas, with a velocity
made good of up to two knots. Reaching and running it averages four to six
knots. Nothing closer to the wind than sixty degrees is sailed here, which is
the limit Palmer 2009 reaches independently for a square rig.

That is a performance envelope for good conditions, so it is an upper bound on
speed and therefore a lower bound on passage time. The point is not to predict
a voyage. It is to ask which months allow one at all.

**The wind.** The monthly climatology in `data/processed/wind_climatology.csv`,
fitted over seventy-eight years at eleven points along the route. Each month
carries a steadiness, the vector mean over the scalar mean, which is reported
beside every passage because a fast month with a steadiness of 0.3 is a month
whose average direction no one would sail on.
"""
import csv, json, math, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "processed"
WIND = OUT / "wind_climatology.csv"

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

# Whitewright 2011, in knots. The key numbers are the sixty-degree limit, the
# two-knot best velocity made good close-hauled, and four to six knots reaching
# or running; the midpoint is taken where a range is given.
CLOSEST_DEG = 60.0
VMG_CLOSE_HAULED_KT = 2.0
REACH_RUN_KT = 5.0

# The wind speed at which the rig is taken to be doing what Whitewright's
# trials describe as light to moderate. Below it, speed falls off with the
# wind; above it, nothing is gained, which is where a square rig of this period
# reefs rather than accelerates.
WIND_REF_MS = 5.0

KT_KM = 1.852

# The trunk route, as the text sails it, with the wind site that speaks for
# each leg. Inland and off-route places in the gazetteer are left out; these
# are the passages where the wind decides whether a ship moves.
LEGS = [
    ("Myos Hormos", (27.34, 33.95), "Okelis", (12.767, 43.651), "Red Sea, middle"),
    ("Okelis", (12.767, 43.651), "Kane", (14.025, 48.342), "Guardafui, gulf mouth"),
    ("Kane", (14.025, 48.342), "Muziris", (10.157, 76.209), "Arabian Sea crossing"),
    ("Kane", (14.025, 48.342), "Barygaza", (21.712, 72.993), "Arabian Sea crossing"),
    ("Muziris", (10.157, 76.209), "Kane", (14.025, 48.342), "Arabian Sea crossing"),
    ("Kane", (14.025, 48.342), "Okelis", (12.767, 43.651), "Guardafui, gulf mouth"),
    ("Okelis", (12.767, 43.651), "Myos Hormos", (27.34, 33.95), "Red Sea, middle"),
]


def bearing(a, b):
    """Initial great-circle bearing from a to b, in degrees clockwise of north."""
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dl = math.radians(b[1] - a[1])
    y = math.sin(dl) * math.cos(p2)
    x = math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl)
    return (math.degrees(math.atan2(y, x)) + 360) % 360


def great_circle_km(a, b):
    R = 6371.0
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp, dl = p2 - p1, math.radians(b[1] - a[1])
    h = (math.sin(dp / 2) ** 2
         + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(h))


def off_wind(course_deg, wind_from_deg):
    """Angle between the course and the wind's eye, 0 to 180 degrees.

    Zero is sailing straight into the wind and is impossible; 180 is running
    dead before it. This is the only angle the polar needs.
    """
    d = abs((course_deg - wind_from_deg + 180) % 360 - 180)
    return d


# Speed at the closest heading the rig can hold, recovered from the trials.
# Whitewright reports a velocity made good of two knots at sixty to sixty-five
# degrees, and velocity made good is speed times the cosine of the angle, so
# the speed itself is a little over four knots.
CLOSE_HAULED_KT = VMG_CLOSE_HAULED_KT / math.cos(math.radians(62.5))


def boat_speed_kt(angle, wind_ms):
    """Speed through the water, from the measured envelope.

    Two anchors and a straight line between them. At the closest heading the
    rig can hold, the trials give two knots made good to windward, which is
    about four and a third knots through the water. From ninety degrees round
    to dead astern they give four to six knots, taken at the midpoint. Between
    sixty and ninety the speed is interpolated.

    Recovering the close-hauled speed by dividing two knots by the cosine of
    the angle at every heading, rather than only at the closest one, was the
    first version of this and it is wrong: the cosine goes to zero at ninety
    degrees, so a beam reach came out at hundreds of knots and the Red Sea
    took a third of a day.
    """
    if angle < CLOSEST_DEG:
        return 0.0
    gust = min(1.0, wind_ms / WIND_REF_MS)
    if angle < 90.0:
        f = (angle - CLOSEST_DEG) / (90.0 - CLOSEST_DEG)
        return (CLOSE_HAULED_KT + f * (REACH_RUN_KT - CLOSE_HAULED_KT)) * gust
    return REACH_RUN_KT * gust


def tacking_speed_kt(angle, wind_ms):
    """Speed made good along the course, beating if the course is unsailable.

    A square rig cannot hold a course inside sixty degrees of the wind, but it
    can still work to windward by tacking, which costs the cosine of the angle
    between the course and the closest heading it can hold. Below about thirty
    degrees off the wind that progress is slower than the current and the leg
    is called impossible rather than slow.
    """
    if angle >= CLOSEST_DEG:
        return boat_speed_kt(angle, wind_ms)
    if angle < 30.0:
        return 0.0
    speed = boat_speed_kt(CLOSEST_DEG, wind_ms)
    return speed * math.cos(math.radians(CLOSEST_DEG - angle))


def load_wind():
    out = {}
    for r in csv.DictReader(open(WIND)):
        out[(r["site"], int(r["month"]))] = dict(
            speed=float(r["speed_ms"]), steadiness=float(r["steadiness"]),
            from_deg=float(r["from_deg"]), compass=r["from_compass"])
    return out


def main():
    wind = load_wind()
    rows = []
    for a_name, a, b_name, b, site in LEGS:
        km = great_circle_km(a, b)
        crs = bearing(a, b)
        for m in range(1, 13):
            w = wind.get((site, m))
            if not w:
                continue
            ang = off_wind(crs, w["from_deg"])
            v = tacking_speed_kt(ang, w["speed"])
            days = (km / (v * KT_KM * 24)) if v > 0 else None
            rows.append(dict(
                leg=f"{a_name} to {b_name}", km=round(km, 0),
                course_deg=round(crs, 0), month=MONTHS[m - 1], month_num=m,
                wind_site=site, wind_from=w["compass"],
                wind_from_deg=round(w["from_deg"]),
                wind_ms=round(w["speed"], 2),
                steadiness=round(w["steadiness"], 3),
                off_wind_deg=round(ang, 0),
                point_of_sail=("into the wind" if ang < 30 else
                               "beating" if ang < CLOSEST_DEG else
                               "close-hauled" if ang < 90 else
                               "reaching" if ang < 135 else "running"),
                speed_kt=round(v, 2),
                days=None if days is None else round(days, 1)))

    with open(OUT / "voyage_legs.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

    print(f"{len(rows)} leg-months -> voyage_legs.csv\n")
    for leg in dict.fromkeys(r["leg"] for r in rows):
        g = [r for r in rows if r["leg"] == leg]
        ok = [r for r in g if r["days"]]
        print(f"=== {leg}  {g[0]['km']:.0f} km, course {g[0]['course_deg']:.0f} deg")
        for r in g:
            mark = "  <-- the text's month" if r["month"] == "July" else ""
            d = f"{r['days']:6.1f} d" if r["days"] else "   none"
            print(f"   {r['month'][:3]} wind {r['wind_from']:>3s} {r['wind_ms']:4.1f} m/s "
                  f"steadiness {r['steadiness']:5.3f}  {r['off_wind_deg']:3.0f} deg off  "
                  f"{r['point_of_sail']:14s} {d}{mark}")
        if ok:
            best = min(ok, key=lambda r: r["days"])
            print(f"   fastest {best['month']} at {best['days']} days; "
                  f"{len(g)-len(ok)} months impossible")
        print()
    round_trip(rows)


def sail(chain, start_month, legs_by_month, hold=0.0):
    """Walk a chain of legs from a departure month, month by month.

    The month advances as the ship sails, so a leg entered in July may be
    finished in August and the next leg takes August's wind. A leg that cannot
    be sailed in the month the ship arrives makes it wait, and waiting is
    counted, because a ship held four months for a wind is the thing the
    sailing season exists to avoid.
    """
    day, month, log = 0.0, start_month, []
    for leg in chain:
        waited = 0
        while True:
            r = legs_by_month.get((leg, month))
            if r and r["days"]:
                break
            waited += 1
            if waited > 12:
                return None, None, log
            day += 30.4
            month = month % 12 + 1
        log.append(dict(leg=leg, month=MONTHS[month - 1], days=r["days"],
                        waited_months=waited, point=r["point_of_sail"],
                        steadiness=r["steadiness"]))
        day += r["days"] + hold
        month = int((start_month - 1 + day // 30.4) % 12) + 1
    return day, month, log


def round_trip(rows):
    """Out to Muziris and home again, from each possible departure month."""
    by = {(r["leg"], r["month_num"]): r for r in rows}
    out = ["Myos Hormos to Okelis", "Okelis to Kane", "Kane to Muziris"]
    back = ["Muziris to Kane", "Kane to Okelis", "Okelis to Myos Hormos"]
    print("\n=== round trip, Egypt to Muziris and home, 30 days in port")
    print(f"   {'depart':10s} {'arrive':11s} {'sail out':>9s} {'home':11s} "
          f"{'total':>7s} {'waiting':>8s}")
    best = []
    for m in range(1, 13):
        d_out, m_arr, log_out = sail(out, m, by)
        if d_out is None:
            print(f"   {MONTHS[m-1]:10s} never arrives")
            continue
        m_leave = int((m_arr - 1 + 1) % 12) + 1          # 30 days in port
        d_back, m_home, log_back = sail(back, m_leave, by)
        if d_back is None:
            print(f"   {MONTHS[m-1]:10s} {MONTHS[m_arr-1]:11s} "
                  f"{d_out:7.1f} d  never gets home")
            continue
        wait = sum(l["waited_months"] for l in log_out + log_back)
        total = d_out + 30.4 + d_back
        best.append((total, m, wait))
        print(f"   {MONTHS[m-1]:10s} {MONTHS[m_arr-1]:11s} {d_out:7.1f} d "
              f"{MONTHS[m_home-1]:11s} {total:6.0f} d {wait:6d} mo")
    if best:
        best.sort()
        print(f"\n   shortest round trip departs {MONTHS[best[0][1]-1]} "
              f"at {best[0][0]:.0f} days")
        nowait = [b for b in best if b[2] == 0]
        if nowait:
            print("   departures with no waiting at all: "
                  + ", ".join(MONTHS[b[1]-1] for b in sorted(nowait, key=lambda b: b[1])))


if __name__ == "__main__":
    main()
