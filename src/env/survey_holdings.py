"""Who holds a real sounding at each port, asked of an archive other than GMRT.

Section 19 found that GMRT's data mask is empty at all seven approaches. A mask
reflects what one compilation ingested, so on its own it cannot distinguish "no
survey exists" from "GMRT does not have it". This asks the other side: NOAA's
National Centers for Environmental Information, the largest public bathymetry
archive and a separate compilation, queried for multibeam surveys and for
single-beam bathymetry tracklines over the same boxes.

Controls are queried in the same run, because a count of zero means nothing
unless the same query returns a positive count somewhere it should. Monterey Bay
and the Hudson shelf valley are the controls, and two boxes near but not at the
ports are included as well, since they turn out to carry the more useful result:
survey on these coasts is not absent in general, it misses the port approaches
in particular.

The service is slow and intermittently drops a connection, so each query is
tried more than once and a failure is reported rather than silently counted as
zero.
"""
import csv, json, pathlib, time, urllib.parse, urllib.request

OUT = pathlib.Path(__file__).resolve().parents[2] / "data" / "processed"

BOXES = {
    "Muziris, Periyar": ([75.85, 10.00, 76.45, 10.45], "port"),
    "Nelkynda and Bakarē, Pamba": ([76.00, 9.15, 76.60, 9.60], "port"),
    "Tyndis": ([75.45, 10.95, 76.05, 11.40], "port"),
    "Barbarikon, Indus": ([67.00, 24.30, 67.85, 25.05], "port"),
    "Leukē Kōmē, Aynuna": ([35.00, 27.90, 35.45, 28.35], "port"),
    "Rhapta, Rufiji": ([38.90, -8.30, 39.60, -7.60], "port"),
    "Pemba and Unguja channels": ([38.70, -6.70, 40.10, -4.70], "nearby"),
    "Mumbai shelf": ([72.40, 18.70, 73.00, 19.20], "nearby"),
    "Monterey Bay": ([-122.10, 36.55, -121.75, 36.90], "control"),
    "Hudson shelf valley": ([-73.95, 40.25, -73.55, 40.55], "control"),
}

BASE = "https://gis.ngdc.noaa.gov/arcgis/rest/services/web_mercator"
SERVICES = {
    "multibeam": f"{BASE}/multibeam_dynamic/MapServer/0/query",
    "trackline_bathymetry": f"{BASE}/trackline_combined_dynamic/MapServer/1/query",
}


def count(url, bbox, tries=3):
    p = {"geometry": ",".join(map(str, bbox)), "geometryType": "esriGeometryEnvelope",
         "inSR": "4326", "spatialRel": "esriSpatialRelIntersects",
         "returnCountOnly": "true", "f": "json"}
    for i in range(tries):
        try:
            with urllib.request.urlopen(url + "?" + urllib.parse.urlencode(p),
                                        timeout=120) as r:
                return json.load(r).get("count")
        except Exception:
            time.sleep(4 * (i + 1))
    return None


def main():
    rows = []
    for name, (bbox, kind) in BOXES.items():
        rec = {"box": name, "kind": kind,
               "west": bbox[0], "south": bbox[1], "east": bbox[2], "north": bbox[3]}
        for svc, url in SERVICES.items():
            n = count(url, bbox)
            rec[svc] = "" if n is None else n
        rows.append(rec)
        mb, tl = rec["multibeam"], rec["trackline_bathymetry"]
        print(f"   {kind:8s} {name:28s} multibeam {str(mb):>4s}   "
              f"tracklines {str(tl):>4s}", flush=True)

    dest = OUT / "survey_holdings.csv"
    with open(dest, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    print(f"\n-> {dest.name}")
    ports = [r for r in rows if r["kind"] == "port"]
    tot = sum(int(r[s] or 0) for r in ports for s in SERVICES)
    ctrl = [r for r in rows if r["kind"] == "control"]
    print(f"   {tot} surveys across {len(ports)} port approaches; "
          f"controls return "
          f"{sum(int(r[s] or 0) for r in ctrl for s in SERVICES)}")


if __name__ == "__main__":
    main()
