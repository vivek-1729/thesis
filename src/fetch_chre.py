"""Pull Coin Hoards of the Roman Empire for the Indian Ocean and Red Sea world.

CHRE (Ashmolean / Oxford Roman Economy Project) holds c. 19,000 hoards and over
7 million coins. Since 2019 it covers hoards of Roman coins found OUTSIDE the
empire, which is what makes it usable here: the Indian finds are in it.

Two levels are fetched. The hoard table gives findspot, coordinates, coin count
and closing date; the coin table gives one row per recorded specimen, with
reign, mint, denomination, metal and weight. The second is what allows the
coin evidence to be dated rather than merely counted.
"""
import urllib.request, urllib.parse, pathlib, csv, io, time

OUT = pathlib.Path(__file__).resolve().parents[1] / "data" / "raw" / "chre"
BASE = "https://chre.ashmus.ox.ac.uk/search/"

# CHRE country ids. Note the absences: no Tanzania, Kenya, Somalia or Ethiopia
# exist as options at all, so the East African coast cannot be queried -- an
# absence in the database, not a result.
COUNTRIES = {
    19: "India", 127: "Pakistan", 111: "Sri Lanka", 120: "Maldives",
    12: "Egypt", 39: "Egypt (alt)", 1034: "Alexandria (Egypt)",
    107: "Yemen", 126: "Oman", 110: "Saudi Arabia", 31: "Arabia",
    109: "United Arab Emirates", 44: "Sudan", 108: "Eritrea",
    122: "Iran", 20: "Iraq", 117: "Afghanistan", 24: "Jordan",
    123: "Thailand", 115: "Uzbekistan", 114: "Turkmenistan",
}

def fetch(fmt, ids):
    q = [("ox_hs[hoardCountries][]", str(i)) for i in ids] + [("format", fmt)]
    url = BASE + "?" + urllib.parse.urlencode(q)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=300) as r:
                return r.read().decode("utf8", "ignore")
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(5)

def main():
    for fmt, name in [("csv", "hoards"), ("csv-coins", "coins")]:
        rows, seen = [], set()
        for cid, label in COUNTRIES.items():
            try:
                txt = fetch(fmt, [cid])
                rd = list(csv.DictReader(io.StringIO(txt)))
            except Exception as e:
                print(f"  {label:22s} ERR {str(e)[:40]}")
                continue
            new = 0
            for x in rd:
                key = x.get("id")
                if key and key in seen:
                    continue
                seen.add(key)
                x["_query_country"] = label
                rows.append(x); new += 1
            print(f"  {label:22s} {len(rd):5d} rows ({new} new)")
        if not rows:
            continue
        dest = OUT / f"chre_{name}.csv"
        cols = list(rows[0].keys())
        with open(dest, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
            w.writeheader(); w.writerows(rows)
        print(f"-> {dest.name}: {len(rows)} rows, {len(cols)} fields\n")

if __name__ == "__main__":
    main()
