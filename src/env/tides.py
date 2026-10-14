"""Tidal range at each port, fitted from observed sea level rather than modelled.

The tide had been recorded as the largest error on the chart soundings, and put
behind an AVISO or TPXO registration. It does not have to be. The IOC Sea Level Station Monitoring Facility serves observed sea level from
2,387 stations with no account, and a harmonic fit to a year of it gives the
range directly, which is the quantity the soundings need.

The station geography is better than expected in three places and poor in one.
Cochin sits 9 km from the Periyar mouth, Keti Bandar is inside the Indus delta
itself, and Zanzibar is 194 km from the Rufiji. Aynuna has nothing closer than
Aqaba, 146 km up the gulf, which is the same body of water but not the same
coast, and the figure for Leukē Kōmē should be read with that attached.

What is fitted is the astronomical tide alone. A sounding reduced to chart datum
also carries surge and seasonal steric height, which are not in these numbers.
"""
import json, math, pathlib, urllib.request, urllib.parse, csv, datetime as dt

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
CACHE = ROOT / "data" / "cache" / "tides"
OUT = ROOT / "data" / "processed"
SERVICE = "https://www.ioc-sealevelmonitoring.org/service.php"

# Where each port's tide has to be known, and how far away the nearest gauge may
# sit before the answer stops being about that coast.
PORTS = {
    "Muziris": (10.20, 76.20),
    "Tyndis": (11.15, 75.80),
    "Nelkynda and Bakarē": (9.40, 76.35),
    "Barbarikon": (24.80, 67.40),
    "Leukē Kōmē": (28.10, 35.20),
    "Rhapta": (-7.90, 39.30),
}

# Frequencies in degrees per mean solar hour. The eight standard constituents
# plus two shallow-water overtides, which matter at a river mouth because they
# are what makes a flood tide shorter than its ebb.
CONSTITUENTS = {
    "M2": 28.9841042, "S2": 30.0000000, "N2": 28.4397295, "K2": 30.0821373,
    "K1": 15.0410686, "O1": 13.9430356, "P1": 14.9589314, "Q1": 13.3986609,
    "M4": 57.9682084, "MS4": 58.9841042,
}


def stations():
    CACHE.mkdir(parents=True, exist_ok=True)
    p = CACHE / "stationlist.json"
    if not p.exists():
        u = f"{SERVICE}?query=stationlist&showall=all&format=json"
        with urllib.request.urlopen(u, timeout=120) as r:
            p.write_bytes(r.read())
    return json.loads(p.read_text())


def km(a, b):
    return math.hypot((a[0] - b[0]) * 110.57,
                      (a[1] - b[1]) * 111.32 * math.cos(math.radians(a[0])))


def nearest(port_ll, n=3):
    out = []
    for s in stations():
        try:
            ll = (float(s["Lat"]), float(s["Lon"]))
        except (TypeError, ValueError, KeyError):
            continue
        if not s.get("Code"):
            continue
        out.append((km(port_ll, ll), s["Code"], s.get("Location") or "", ll))
    out.sort(key=lambda z: z[0])
    seen, keep = set(), []
    for d, code, loc, ll in out:
        if code in seen:
            continue
        seen.add(code)
        keep.append((d, code, loc, ll))
        if len(keep) == n:
            break
    return keep


def series(code, months=14, end=None):
    """Hourly sea level for one station, pulled a month at a time and cached.

    The service returns one-minute values, so each month is resampled to the
    hour before being kept. A year or more is needed because a shorter record
    cannot separate K1 from P1, or S2 from K2, and reporting a spring range off
    an unseparated fit would be wrong in a way that does not look wrong.
    """
    CACHE.mkdir(parents=True, exist_ok=True)
    end = end or dt.date.today().replace(day=1)
    times, levels = [], []
    for k in range(months):
        m0 = (end.replace(day=1) - dt.timedelta(days=1)).replace(day=1) if k else end
        end = m0
        m1 = (m0 + dt.timedelta(days=32)).replace(day=1)
        p = CACHE / f"{code}_{m0:%Y%m}.json"
        if not p.exists():
            q = urllib.parse.urlencode({"query": "data", "code": code,
                                        "timestart": f"{m0:%Y-%m-%d}",
                                        "timestop": f"{m1:%Y-%m-%d}",
                                        "format": "json"})
            try:
                with urllib.request.urlopen(f"{SERVICE}?{q}", timeout=180) as r:
                    p.write_bytes(r.read())
            except Exception:
                continue
        try:
            rows = json.loads(p.read_text())
        except Exception:
            continue
        if not isinstance(rows, list):
            continue
        # One station can carry several sensors; take whichever reported most.
        by = {}
        for r in rows:
            by.setdefault(r.get("sensor"), []).append(r)
        if not by:
            continue
        rows = max(by.values(), key=len)
        for r in rows:
            try:
                t = dt.datetime.strptime(r["stime"], "%Y-%m-%d %H:%M:%S")
                v = float(r["slevel"])
            except (KeyError, TypeError, ValueError):
                continue
            if t.minute == 0:
                times.append(t)
                levels.append(v)
    if not times:
        return None, None
    o = np.argsort(np.array(times))
    return np.array(times)[o], np.array(levels)[o]


# The IOC network is real time, so several of its stations hold only weeks of
# data. The long archival records are at the University of Hawaii, which has
# forty years at Zanzibar and ten at Karachi but nothing at all in India. So the
# two sources are complementary rather than redundant, and each port takes
# whichever one actually has a record near it.
UHSLC = "https://uhslc.soest.hawaii.edu/erddap/tabledap/global_hourly_rqds.json"

UHSLC_FOR = {
    "Barbarikon": (1471, "Karachi", 24.81, 66.97, "1990-01-01", "1991-01-01"),
    "Rhapta": (1511, "Zanzibar", -6.15, 39.18, "2015-01-01", "2016-01-01"),
}


def uhslc_series(record_id, start, stop):
    """One year of hourly sea level from the Hawaii archive, in metres."""
    CACHE.mkdir(parents=True, exist_ok=True)
    p = CACHE / f"uhslc_{record_id}_{start[:4]}.json"
    if not p.exists():
        q = urllib.parse.quote(
            f"time,sea_level&record_id={record_id}&time>={start}&time<={stop}",
            safe="?&=<>,")
        with urllib.request.urlopen(f"{UHSLC}?{q}", timeout=240) as r:
            p.write_bytes(r.read())
    rows = json.loads(p.read_text())["table"]["rows"]
    times, levels = [], []
    for t, v in rows:
        if v is None:
            continue
        times.append(dt.datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ"))
        levels.append(v / 1000.0)          # the archive reports millimetres
    return np.array(times), np.array(levels)


def harmonic(times, levels):
    """Least-squares amplitudes at the known tidal frequencies.

    The frequencies are astronomy, not something to be estimated, so this is an
    ordinary linear fit on sine and cosine pairs. Nodal corrections over the
    18.6-year cycle are not applied; they move M2 by a few per cent and that is
    well inside what the rest of this is good for.
    """
    t0 = times[0]
    h = np.array([(t - t0).total_seconds() / 3600.0 for t in times])
    good = np.isfinite(levels)
    h, y = h[good], levels[good]
    if len(y) < 2000:
        return None
    cols = [np.ones_like(h)]
    for speed in CONSTITUENTS.values():
        w = math.radians(speed)
        cols += [np.cos(w * h), np.sin(w * h)]
    A = np.column_stack(cols)
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    amp = {}
    for i, name in enumerate(CONSTITUENTS):
        a, b = coef[1 + 2 * i], coef[2 + 2 * i]
        amp[name] = float(math.hypot(a, b))
    resid = y - A @ coef
    amp["_n"] = len(y)
    amp["_rms_resid"] = float(np.sqrt(np.mean(resid ** 2)))
    amp["_var_explained"] = float(1 - np.var(resid) / np.var(y))

    # What the tide does not explain, separated into a seasonal part and the
    # rest. A low fit can mean a bad record or a coast where something other
    # than the moon moves the water, and those have opposite consequences for a
    # sounding. Monthly means of the residual tell them apart: noise averages
    # away over a month, a monsoon does not.
    months = {}
    for t, r in zip(np.array(times)[good], resid):
        months.setdefault(t.month, []).append(r)
    means = [float(np.mean(v)) for v in months.values()]
    amp["_seasonal_range"] = float(max(means) - min(means)) if len(means) > 2 else float("nan")
    amp["_resid_sd"] = float(np.std(resid))
    amp["_tide_sd"] = float(np.std(A @ coef))
    return amp


def summarise(amp):
    """The numbers a navigability argument actually uses."""
    M2, S2, K1, O1 = amp["M2"], amp["S2"], amp["K1"], amp["O1"]
    return {
        "spring_range_m": round(2 * (M2 + S2), 2),
        "neap_range_m": round(2 * abs(M2 - S2), 2),
        "form_factor": round((K1 + O1) / (M2 + S2), 2) if (M2 + S2) else "",
        "regime": ("semidiurnal" if (K1 + O1) / (M2 + S2) < 0.25 else
                   "mixed, mainly semidiurnal" if (K1 + O1) / (M2 + S2) < 1.5 else
                   "mixed, mainly diurnal" if (K1 + O1) / (M2 + S2) < 3 else "diurnal"),
        "M2_m": round(M2, 3), "S2_m": round(S2, 3),
        "K1_m": round(K1, 3), "O1_m": round(O1, 3),
        "hours_fitted": amp["_n"],
        "var_explained": round(amp["_var_explained"], 3),
        "rms_residual_m": round(amp["_rms_resid"], 3),
        "tide_sd_m": round(amp["_tide_sd"], 3),
        "nontidal_sd_m": round(amp["_resid_sd"], 3),
        "seasonal_range_m": round(amp["_seasonal_range"], 3),
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for port, ll in PORTS.items():
        if port in UHSLC_FOR:
            rid, loc, la, lo, a, b = UHSLC_FOR[port]
            t, y = uhslc_series(rid, a, b)
            amp = harmonic(t, y)
            if amp is not None:
                r = {"port": port, "station": loc, "code": f"uhslc:{rid}",
                     "distance_km": round(km(ll, (la, lo))), "lat": la, "lon": lo,
                     "span_start": str(t[0].date()), "span_end": str(t[-1].date())}
                r.update(summarise(amp))
                rows.append(r)
                print(f"  {port:22s} {loc[:18]:18s} {r['distance_km']:5d} km  "
                      f"spring {r['spring_range_m']:.2f} m  neap {r['neap_range_m']:.2f} m  "
                      f"{r['regime']}  (R2 {r['var_explained']:.2f}, "
                      f"{r['hours_fitted']} h)", flush=True)
                continue
        for dist, code, loc, sll in nearest(ll, n=3):
            t, y = series(code)
            if t is None:
                print(f"  {port:22s} {code:6s} {loc[:20]:20s} no data", flush=True)
                continue
            amp = harmonic(t, y)
            if amp is None:
                print(f"  {port:22s} {code:6s} {loc[:20]:20s} too short "
                      f"({len(t)} hours)", flush=True)
                continue
            r = {"port": port, "station": loc, "code": code,
                 "distance_km": round(dist), "lat": sll[0], "lon": sll[1],
                 "span_start": str(t[0].date()), "span_end": str(t[-1].date())}
            r.update(summarise(amp))
            rows.append(r)
            print(f"  {port:22s} {code:6s} {loc[:18]:18s} {dist:5.0f} km  "
                  f"spring {r['spring_range_m']:.2f} m  neap {r['neap_range_m']:.2f} m  "
                  f"{r['regime']}  (R2 {r['var_explained']:.2f}, "
                  f"{r['hours_fitted']} h)", flush=True)
            break      # the nearest station that actually has a usable record
    if not rows:
        print("no usable records")
        return
    dest = OUT / "tidal_range.csv"
    with open(dest, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    print(f"\n-> {dest.name}")


if __name__ == "__main__":
    main()
