"""Ask the open date and core databases what they hold at the seven ports.

The thesis holds three dated subsurface records and they came from papers:
seventeen Kerala boreholes and twenty-seven Kerala core dates from Maya et al.
2017, and twenty-six Tanzanian dates read out of Punwong's 2013 thesis. Nothing
for the Red Sea and nothing for the Indus. Before going looking for more papers
it is worth asking the databases, because a date that has been deposited is
already standardised, already carries coordinates, and does not have to be read
off a table in a scan.

Four of them answer, and each had to be worked out rather than looked up.

XRONOS aggregates archaeological radiocarbon, 314,832 records of which 290,066
carry coordinates. Its own query API returns null for every country tried,
including ones it certainly holds, so this uses the bulk CSV export instead.

PANGAEA's public search takes a bounding box under the names minlat, maxlat,
minlon and maxlon, and ignores it in two different ways. A box passed as `bbox`
is dropped and the search returns all 445,551 datasets. A box passed correctly
but alongside a text query is also dropped, which is worse, because the result
looks regional until you read it: a query for cores in the half-degree box at
the Periyar returns North Atlantic foraminifera. So this goes to the Elasticsearch
index behind it instead, which carries each dataset's own bounding coordinates,
and filters on containment. Containment rather than overlap matters here. The
first Periyar hit from the overlap search declares an extent of 5 to 17 north
and 60 to 90 east, three thousand kilometres of the Indian Ocean, which overlaps
the port and says nothing about it.

The NOAA palaeoclimate archive accepts a bounding box and does not really use
it: a tenth-of-a-degree box returns 450 studies and a two-degree box returns
475. So the whole list is pulled once and filtered here on the coordinates each
study actually states.

Neotoma accepts `loc`, and accepts a bare bounding-box array without complaint
while matching nothing at all. It wants GeoJSON. The US Midwest returning zero
datasets is what showed this, since that is the best-sampled region it has.

Distances are to the nearest edge of the port box, not to its centre, and three
bands are reported. Inside the box is evidence about the port. Within fifty
kilometres is the same coastal cell. Within two hundred is a different place
that can still carry a sea-level datum, which is the quantity the Malabar work
has no local source for.
"""
import csv, json, math, pathlib, time, urllib.parse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
CACHE = ROOT / "data" / "cache" / "dated"
OUT = ROOT / "data" / "processed"

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# The same six boxes the bathymetry and water work uses, so a date found here
# can be laid over those results without re-projecting anything.
BOXES = {
    "Muziris":          ([75.85, 10.00, 76.45, 10.45], "Periyar delta"),
    "Nelkynda, Bakarē": ([76.00, 9.15, 76.60, 9.60], "Pamba mouth, Alappuzha"),
    "Tyndis":           ([75.45, 10.95, 76.05, 11.40], "Kadalundi to Ponnani"),
    "Barbarikon":       ([67.00, 24.30, 67.85, 25.05], "Indus delta"),
    "Leukē Kōmē":       ([35.00, 27.90, 35.45, 28.35], "Aynuna, Gulf of Aqaba"),
    "Rhapta":           ([38.90, -8.30, 39.60, -7.60], "Rufiji delta, Mafia"),
}

BANDS = [(0, "in box"), (50, "within 50 km"), (200, "within 200 km")]
FAR = 200.0

XRONOS_BULK = "https://xronos.ch/data.csv"
PANGAEA = "https://ws.pangaea.de/es/pangaea/panmd/_search"
NOAA = "https://www.ncei.noaa.gov/access/paleo-search/study/search.json"
NEOTOMA = "https://api.neotomadb.org/v2.0/data/datasets"


def get(url, timeout=300):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def cached(name, url, timeout=900):
    CACHE.mkdir(parents=True, exist_ok=True)
    p = CACHE / name
    if p.exists() and p.stat().st_size > 1000:
        return p
    print(f"   fetching {name} ...")
    p.write_bytes(get(url, timeout))
    return p


def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = (math.sin(dp / 2) ** 2
         + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(a))


def distance_to_box(lat, lon, box):
    """Kilometres to the nearest edge, and zero inside.

    Clamping the point to the rectangle and measuring to the clamped point is
    exact enough at these sizes and avoids the mistake of measuring to the
    centre, which would put a date on the far side of a half-degree box at the
    same distance as one on the near side.
    """
    x0, y0, x1, y1 = box
    cx = min(max(lon, x0), x1)
    cy = min(max(lat, y0), y1)
    if cx == lon and cy == lat:
        return 0.0
    return haversine(lat, lon, cy, cx)


def nearest_port(lat, lon):
    best, bestd = None, 1e9
    for port, (box, _) in BOXES.items():
        d = distance_to_box(lat, lon, box)
        if d < bestd:
            best, bestd = port, d
    return best, bestd


def band_of(km):
    for limit, name in BANDS:
        if km <= limit:
            return name
    return None


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


# --- XRONOS -----------------------------------------------------------------

def from_xronos():
    """Archaeological radiocarbon, from the bulk export.

    The export is half a gigabyte, so it is cached and streamed rather than
    loaded, and the filter runs as it reads.
    """
    path = cached("xronos.csv", XRONOS_BULK)
    csv.field_size_limit(10 ** 7)
    rows, total, located = [], 0, 0
    with open(path, newline="", encoding="utf-8", errors="replace") as fh:
        for r in csv.DictReader(fh):
            total += 1
            lat, lon = num(r["lat"]), num(r["lng"])
            if lat is None or lon is None:
                continue
            located += 1
            port, km = nearest_port(lat, lon)
            if km > FAR:
                continue
            rows.append(dict(
                source="XRONOS", port=port, km=round(km, 1),
                band=band_of(km), site=r["site"], lat=lat, lon=lon,
                kind=r["site_type"] or "", material=r["material"] or "",
                date=r["labnr"] or "", bp=r["bp"] or "", err=r["std"] or "",
                note=r["feature"] or "",
                reference=(r["reference"] or "")[:120]))
    print(f"   XRONOS {total} records, {located} located, {len(rows)} near a port")
    return rows


# --- PANGAEA ----------------------------------------------------------------

def from_pangaea():
    """Deposited datasets whose own extent sits inside a port box.

    The index states four bounding coordinates per dataset, so the filter is
    four range clauses and the result needs no second request to place it. The
    title lives inside an XML blob rather than in a field of its own.
    """
    import re
    rows = []
    for port, (box, _) in BOXES.items():
        x0, y0, x1, y1 = box
        body = json.dumps({
            "size": 500,
            "query": {"bool": {"filter": [
                {"range": {"southBoundLatitude": {"gte": y0}}},
                {"range": {"northBoundLatitude": {"lte": y1}}},
                {"range": {"westBoundLongitude": {"gte": x0}}},
                {"range": {"eastBoundLongitude": {"lte": x1}}}]}},
            "_source": ["URI", "meanPosition", "agg-pubYear", "agg-author",
                        "agg-mainTopic", "agg-method", "agg-location",
                        "nDataPoints", "minDateTime", "maxDateTime",
                        "xml-thumb"]}).encode()
        req = urllib.request.Request(
            PANGAEA, data=body,
            headers={"User-Agent": UA, "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as r:
            d = json.loads(r.read())
        hits = d["hits"]["hits"]
        total = d["hits"]["total"]
        total = total if isinstance(total, int) else total.get("value", 0)
        print(f"   PANGAEA {port:18s} {total:5d} contained, {len(hits)} read")
        for h in hits:
            s = h["_source"]
            pos = s.get("meanPosition") or {}
            lat, lon = pos.get("lat"), pos.get("lon")
            if lat is None or lon is None:
                continue
            km = distance_to_box(lat, lon, box)
            # Some records declare a bounding box inside a port and a mean
            # position in the Pacific. The declared box is what the filter
            # matched and the position is what the data is, so the position
            # wins and the record is dropped.
            if km > FAR:
                continue
            title = re.search(r"<md:title>(.*?)</md:title>",
                              s.get("xml-thumb") or "", re.S)
            rows.append(dict(
                source="PANGAEA", port=port, km=round(km, 1),
                band=band_of(km),
                site="; ".join(s.get("agg-location") or [])[:60],
                lat=lat, lon=lon,
                kind=s.get("agg-mainTopic", ""),
                material="; ".join((s.get("agg-method") or [])[:2])[:60],
                date=s.get("URI", ""),
                bp=(s.get("minDateTime") or "")[:10],
                err=(s.get("maxDateTime") or "")[:10],
                note=f"{s.get('nDataPoints', '')} points",
                reference=(title.group(1).strip() if title else "")[:200]))
        time.sleep(0.4)
    return rows


# --- NOAA palaeoclimate ------------------------------------------------------

def site_points(site):
    """Every point a NOAA study states for a site.

    Some are POINT, some are POLYGON with the corners given as four strings in
    the order south, north, west, east, and some are the whole globe, which is
    what a hemispheric reconstruction records. The global ones are dropped,
    since a study covering 0 to 90 north is not evidence about a port.
    """
    geo = (site or {}).get("geo") or {}
    geom = geo.get("geometry") or {}
    coords = geom.get("coordinates") or []
    props = geo.get("properties") or {}
    if str(geom.get("type", "")).upper() == "POINT" and len(coords) >= 2:
        lat, lon = num(coords[0]), num(coords[1])
        if lat is not None and lon is not None:
            return [(lat, lon)]
        return []
    s, n = num(props.get("southernmostLatitude")), num(props.get("northernmostLatitude"))
    w, e = num(props.get("westernmostLongitude")), num(props.get("easternmostLongitude"))
    if None in (s, n, w, e):
        return []
    if (n - s) > 5 or (e - w) > 5:
        return []
    return [((s + n) / 2, (w + e) / 2)]


def from_noaa():
    """The NOAA palaeoclimate archive, filtered here because it will not filter."""
    url = (f"{NOAA}?minLat=-90&maxLat=90&minLon=-180&maxLon=180")
    path = cached("noaa_paleo.json", url, 600)
    studies = json.loads(path.read_text())["study"]
    rows = []
    for s in studies:
        for site in s.get("site") or []:
            for lat, lon in site_points(site):
                port, km = nearest_port(lat, lon)
                if km > FAR:
                    continue
                rows.append(dict(
                    source="NOAA Paleo", port=port, km=round(km, 1),
                    band=band_of(km), site=site.get("siteName", ""),
                    lat=lat, lon=lon, kind=s.get("dataType", ""),
                    material="", date="",
                    bp=s.get("earliestYearBP", ""),
                    err=s.get("mostRecentYearBP", ""),
                    note=s.get("doi", ""),
                    reference=(s.get("studyName") or "")[:160]))
    print(f"   NOAA Paleo {len(studies)} studies, {len(rows)} near a port")
    return rows


# --- Neotoma ----------------------------------------------------------------

def from_neotoma():
    """Palaeoecological datasets, which is to say pollen and plant cores."""
    rows = []
    for port, (box, _) in BOXES.items():
        x0, y0, x1, y1 = box
        poly = json.dumps({"type": "Polygon", "coordinates": [[
            [x0, y0], [x1, y0], [x1, y1], [x0, y1], [x0, y0]]]})
        q = urllib.parse.urlencode({"loc": poly, "limit": 500})
        # Read the body from the call. An earlier check of these boxes went
        # through a file on disk, and when the request timed out the file still
        # held the previous answer, so Kerala appeared to contain two lakes in
        # Minnesota.
        d = json.loads(get(f"{NEOTOMA}?{q}", 180))
        hits = d.get("data") or []
        print(f"   Neotoma {port:18s} {len(hits)}")
        for h in hits:
            site = h.get("site") or {}
            rows.append(dict(
                source="Neotoma", port=port, km=0.0, band="in box",
                site=site.get("sitename", ""), lat="", lon="",
                kind="palaeoecology", material="", date="", bp="", err="",
                note=str(site.get("siteid", "")),
                reference=(site.get("sitedescription") or "")[:160]))
        time.sleep(0.5)
    return rows


def main():
    rows = []
    for fn in (from_xronos, from_pangaea, from_noaa, from_neotoma):
        try:
            rows.extend(fn())
        except Exception as exc:
            print(f"   {fn.__name__} failed: {exc}")

    fields = ["source", "port", "band", "km", "site", "lat", "lon", "kind",
              "material", "date", "bp", "err", "note", "reference"]
    dest = OUT / "dated_subsurface.csv"
    with open(dest, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows({k: r.get(k, "") for k in fields} for r in rows)

    print(f"\n{len(rows)} records -> {dest}\n")
    print(f"{'port':20s} {'in box':>8s} {'<50 km':>8s} {'<200 km':>8s}")
    for port in BOXES:
        got = [r for r in rows if r["port"] == port]
        counts = [sum(1 for r in got if r["band"] == name)
                  for _, name in BANDS]
        print(f"{port:20s} {counts[0]:8d} {counts[1]:8d} {counts[2]:8d}")

    from collections import Counter
    print()
    for k, v in Counter(r["source"] for r in rows).most_common():
        print(f"   {k:14s} {v}")


if __name__ == "__main__":
    main()
