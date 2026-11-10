"""Bibliographic sweep for the geographic gaps, which the first sweep did not cover.

`query_literature.py` asked Crossref about ports, excavations and trade. It found
archaeology and almost no palaeoenvironment, so the questions that actually block
the geographic layer -- where the shoreline was, when the Vembanad took its
present shape, what lies under the Kuttanad polders -- went unasked.

This sweep asks them. OpenAlex rather than Crossref, because the relevant work is
published in the Journal of the Geological Society of India, Current Science and
Indian university repositories, which Crossref indexes thinly and OpenAlex well.
OpenAlex also reports every open-access location for a work rather than one
"best" one, which matters because the host that serves a PDF without blocking a
script is often not the publisher.

Output is a candidate list, not a reading list. Topic strings match loosely.
"""
import urllib.request, urllib.parse, json, csv, time, pathlib, re

OUT = pathlib.Path(__file__).resolve().parents[1] / "data" / "processed"
MAIL = "vivekshah@college.harvard.edu"
UA = {"User-Agent": f"thesis-research/1.0 (mailto:{MAIL})"}

# Keyed by the gap each group is meant to close, so a result can be traced back
# to the question that justified looking for it.
QUERIES = {
    "kerala-coastal-evolution": [
        "Late Quaternary coastal evolution central Kerala Muziris sedimentary archives",
        "identification palaeodelta mouth Periyar River central Kerala",
        "Holocene coastal evolution Kerala beach ridge strand plain",
        "Kerala coast sea level change Holocene radiocarbon",
        "Vembanad lagoon Holocene evolution sediment core",
        "Kuttanad formation borehole lithology Quaternary Kerala",
        "Alappuzha coastal sediments geochemistry Quaternary",
        "Ashtamudi Kollam coastal wetland Holocene sediment",
    ],
    "kerala-dated-shoreline": [
        "OSL dating palaeo beach ridges Kerala shoreline progradation",
        "optically stimulated luminescence coastal dune ridge south India",
        "relative sea level reconstruction south west India late Holocene",
        "late Holocene Vembanad wetland paleolimnology anthropogenic",
        "Pamba basin peat floodplain Holocene south India",
    ],
    "kerala-subsurface": [
        "electrical resistivity tomography palaeochannel aquifer Kerala",
        "buried channel geophysical survey coastal plain India resistivity",
        "ground penetrating radar beach ridge India coastal",
        "aquifer systems Kuttanad hydrogeology Kerala",
    ],
    "indus-delta": [
        "Indus delta Holocene evolution shoreline change",
        "Indus river avulsion palaeochannel Sindh Holocene",
        "Indus delta sediment core radiocarbon late Holocene",
        "Arabian Sea Pakistan coast Holocene sea level peopling",
        "Makran Las Bela coast Holocene shoreline archaeology",
        "historical maps settlement alluvial floodplain reconstruction GIS",
    ],
    "rhapta-tanzania": [
        "Holocene mangrove dynamics relative sea level Tanzania coast",
        "Rufiji delta Holocene sediment core mangrove pollen",
        "Zanzibar Mafia island Holocene coastal change sea level",
        "East African coast late Holocene shoreline change",
        "Rhapta Azania location archaeology Tanzania",
    ],
    "red-sea-arabia": [
        "Red Sea Holocene relative sea level coastal Arabia",
        "Gulf of Aqaba coastal change Holocene shoreline",
        "Aynuna Leuke Kome Nabataean port Red Sea excavation",
        "Saudi Arabia Red Sea coast geomorphology wadi delta Holocene",
    ],
    "method": [
        "satellite derived bathymetry shallow water Stumpf log ratio",
        "shoreline change analysis uncertainty historical charts georeferencing",
        "palaeochannel detection multispectral satellite imagery archaeology",
        "historical nautical chart digitisation bathymetry change analysis",
        "tidal model FES TPXO validation coastal datum",
    ],
}


def get(url, tries=3):
    for i in range(tries):
        try:
            return json.load(urllib.request.urlopen(
                urllib.request.Request(url, headers=UA), timeout=60))
        except Exception as e:
            if i == tries - 1:
                return {"_err": str(e)[:60]}
            time.sleep(3 * (i + 1))


def openalex(q, per=25):
    u = "https://api.openalex.org/works?" + urllib.parse.urlencode(
        {"search": q, "per-page": per, "mailto": MAIL})
    d = get(u)
    return d.get("results", []) if "_err" not in d else []


def pdf_urls(w):
    """Every open-access location, publisher first, repository after.

    Kept as a list because publishers block scripts far more often than
    repositories do, so the fetcher needs somewhere else to try.
    """
    seen, out = set(), []
    for loc in (w.get("locations") or []):
        if not loc.get("is_oa"):
            continue
        u = loc.get("pdf_url") or loc.get("landing_page_url")
        if u and u not in seen:
            seen.add(u)
            out.append(u)
    return out


def main():
    rows, seen = [], set()
    for gap, qs in QUERIES.items():
        n0 = len(rows)
        for q in qs:
            for w in openalex(q):
                wid = w.get("id", "")
                if not wid or wid in seen:
                    continue
                seen.add(wid)
                auth = "; ".join(
                    (a.get("author") or {}).get("display_name", "")
                    for a in (w.get("authorships") or [])[:4])
                src = ((w.get("primary_location") or {}).get("source") or {})
                oa = w.get("open_access") or {}
                urls = pdf_urls(w)
                rows.append({
                    "gap": gap, "query": q,
                    "year": w.get("publication_year") or "",
                    "title": re.sub(r"\s+", " ", w.get("title") or "?")[:220],
                    "authors": auth[:160],
                    "venue": (src.get("display_name") or "")[:90],
                    "type": w.get("type", ""),
                    "cited_by": w.get("cited_by_count", 0),
                    "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
                    "is_oa": "Y" if oa.get("is_oa") else "N",
                    "n_oa_urls": len(urls),
                    "oa_urls": " | ".join(urls[:4]),
                })
            time.sleep(0.3)
        print(f"  {gap:26s} +{len(rows)-n0:4d} new  (total {len(rows)})", flush=True)

    dest = OUT / "geo_literature_candidates.csv"
    with open(dest, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    noa = sum(1 for r in rows if r["is_oa"] == "Y")
    print(f"\n{len(rows)} works -> {dest.name}   ({noa} open access, {noa/len(rows):.0%})")


if __name__ == "__main__":
    main()
