"""Historic Admiralty charts from Wikimedia Commons.

All public domain, 80 to 176 megapixels, which is enough to georeference and to
read the soundings. These are the surveys Giosan and colleagues used to quantify
Indus delta change, and the Malabar sheets cover every Kerala candidate.
"""
import json, pathlib, re, sys, urllib.parse, urllib.request

OUT = pathlib.Path(__file__).resolve().parents[2] / "library" / "charts"
UA = {"User-Agent": "thesis/1.0 (vivekshah@college.harvard.edu)"}

CHARTS = {
    # Malabar: 749 covers Tyndis and Muziris, 750 covers Nelkynda and Bakare.
    "malabar-749-1857": "Admiralty Chart No 749 Malabar Coast of India from 11° 2' to 9°50 north latitude, Published 1857.jpg",
    "malabar-750-1857": "Admiralty Chart No 750 Malabar Coast of India from 9°53' to 8°40' north latitude, Published 1857.jpg",
    "malabar-751-1857": "Admiralty Chart No 751 Sheet 13 West Coast of India Malabar Coast from Anjengo to Cape Comorin, Published 1857.jpg",
    # Indus delta: Oldham's 1895-96 survey as published in 1897, in two sheets.
    "indus-41-1897":    "Admiralty Chart No 41 Cape Monze to Kediwari Mouth, Published 1897.jpg",
    "indus-118-1897":   "Admiralty Chart No 118 Delta of the Indus, Kediwari Mouth to Nirani Creek, Published 1897.jpg",
    # Red Sea: the Moresby and Elwon survey as published.
    "redsea-8a-1873":   "Admiralty Chart No 8a Red Sea Sheet 1, Published 1873.jpg",
    "redsea-8b-1873":   "Admiralty Chart No 8b Red Sea Sheet 2, Published 1873.jpg",
    "redsea-8c-1873":   "Admiralty Chart No 8c Red Sea Sheet 3, Published 1873.jpg",
}


def info(titles):
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
        "action": "query", "prop": "imageinfo",
        "iiprop": "url|size|extmetadata", "format": "json",
        "titles": "|".join("File:" + t for t in titles)})
    d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60))
    out = {}
    for p in d["query"]["pages"].values():
        if "imageinfo" in p:
            out[p["title"][5:]] = p["imageinfo"][0]
    return out


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    meta = info(list(CHARTS.values()))
    index = []
    for key, title in CHARTS.items():
        ii = meta.get(title)
        if not ii:
            print(f"{key:20s} NOT FOUND"); continue
        dest = OUT / f"{key}.jpg"
        if not dest.exists():
            req = urllib.request.Request(ii["url"], headers=UA)
            with urllib.request.urlopen(req, timeout=600) as r, open(dest, "wb") as f:
                f.write(r.read())
        index.append({"key": key, "title": title, "file": dest.name,
                      "width": ii["width"], "height": ii["height"],
                      "bytes": dest.stat().st_size, "source": ii["descriptionurl"],
                      "licence": ii.get("extmetadata", {}).get("LicenseShortName", {}).get("value")})
        print(f"{key:20s} {ii['width']:6d}x{ii['height']:<6d} {dest.stat().st_size/1e6:6.1f} MB")
    (OUT / "index.json").write_text(json.dumps(index, indent=1))
    print(f"\n{len(index)} charts in {OUT}")
