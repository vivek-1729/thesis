"""David Rumsey map catalogue for our four coasts.

Rumsey has about 56,000 georeferenced sheets and exposes a JSON search plus
IIIF, so the metadata is cheap to harvest and any sheet can be pulled at full
resolution afterwards.
"""
import csv, json, pathlib, time, urllib.parse, urllib.request

OUT = pathlib.Path(__file__).resolve().parents[2] / "library" / "charts-rumsey"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
BASE = "https://www.davidrumsey.com/luna/servlet/as/search"

TERMS = ["Malabar", "Travancore", "Cochin India", "Indus delta", "Scinde",
         "Red Sea", "Zanzibar", "Kerala", "Madras Presidency coast"]


def search(term, start=0, n=50):
    u = (f"{BASE}?q={urllib.parse.quote(term)}&os={start}&pgs={n}"
         "&fullData=true&format=json")
    d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=90))
    return d


def flatten(d):
    out = []
    for item in d.get("results", []) or []:
        f = {k: v for k, v in item.items() if isinstance(v, (str, int))}
        fields = {x.get("fieldName"): x.get("fieldValue")
                  for x in item.get("fieldValues", []) if isinstance(x, dict)}
        out.append({
            "id": f.get("id") or item.get("id", ""),
            "title": (fields.get("Title") or f.get("displayName") or "")[:300],
            "date": fields.get("Pub Date") or fields.get("Date") or "",
            "author": (fields.get("Author") or "")[:120],
            "area": (fields.get("Pub List No") or fields.get("Area") or "")[:80],
            "url": item.get("urlSize4") or item.get("urlSize3") or "",
            "link": f"https://www.davidrumsey.com/luna/servlet/detail/{item.get('id','')}",
        })
    return out


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    rows, seen = [], set()
    for term in TERMS:
        try:
            d = search(term)
        except Exception as e:
            print(f"{term:26s} FAILED {type(e).__name__}")
            continue
        total = d.get("totalResults", "?")
        got = flatten(d)
        new = 0
        for g in got:
            if g["id"] and g["id"] not in seen:
                seen.add(g["id"]); g["term"] = term; rows.append(g); new += 1
        print(f"{term:26s} {total:>5} results, {new} new")
        time.sleep(1.0)

    dest = OUT / "catalogue.csv"
    with open(dest, "w", newline="") as f:
        w = csv.DictWriter(f, ["term", "id", "date", "title", "author", "area", "link", "url"])
        w.writeheader(); w.writerows(rows)
    print(f"\n{len(rows)} unique sheets -> {dest}")
