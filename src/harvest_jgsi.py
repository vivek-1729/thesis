"""Harvest the Geological Society of India's open archive.

The palaeochannel search in `docs/new_findings.md` section 7 concluded that no
agency publishes a buried-channel layer and that the maps exist only as figures
inside papers. Two of those papers then turned out to be sitting in an archive
nobody had tried: the Journal of the Geological Society of India runs an Open
Journal Systems instance with free PDFs back to the 1960s, and it is where the
Indian coastal-geomorphology literature was published.

That matters beyond the one paper. JGSI carries the Quaternary geology of the
Kerala basin, the Vembanad cores, the shoreline-change studies and the Kachchh
and Indus work, which is to say most of the geomorphic evidence for four of the
seven ports. It is not indexed by Unpaywall and only partly by Crossref, so the
earlier OpenAlex sweep in `src/query_geo_literature.py` never saw it.

Three things about this archive have to be handled rather than assumed.

The search is full text, not title, so a query for Periyar returns the Annual
General Meeting proceedings because somebody from the Periyar basin attended.
Relevance is therefore decided on the title, after the fact.

The same paper is often deposited twice under different identifiers, once in the
issue and once in a retrospective batch. The Periyar palaeodelta note is both
82164 and 83848. Deduplication is on the title, not the identifier.

The PDF link is not derivable from the article identifier. It carries a separate
galley number, which is only available from the article page's citation_pdf_url
meta tag, so every candidate costs one extra request.
"""
import csv, pathlib, re, time, urllib.parse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEST = ROOT / "library" / "geomorphology" / "jgsi"
OUT = pathlib.Path(__file__).resolve().parents[1] / "data" / "processed"

BASE = "https://www.geosocindia.org/index.php/jgsi"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# What to ask for, grouped by the port the answer would bear on. JGSI is an
# Indian journal, so it can speak to Malabar and to the Indus and says nothing
# about the Red Sea or Tanzania.
QUERIES = {
    "Malabar": ["palaeodelta", "palaeochannel Kerala", "paleochannel Kerala",
                "Vembanad", "Kerala coast Holocene", "Kerala shoreline change",
                "Kerala Quaternary", "Periyar river", "Cochin shelf",
                "Kerala lagoon sediment", "Kerala sea level", "mudbank Kerala",
                "Kerala strandline", "laterite Kerala coast"],
    "Barbarikon": ["Indus delta", "Kachchh palaeochannel", "Rann of Kachchh",
                   "Saraswati palaeochannel", "Nara river", "Gujarat shoreline",
                   "Kachchh Holocene", "Indus shelf"],
}

# A title has to name a place we care about and a process that moves coastline
# or channel. Both halves are required, because "Kerala" alone returns reviews
# of the Western Ghats and "palaeochannel" alone returns Gondwana coal basins.
PLACE = re.compile(
    r"kerala|vembanad|periyar|cochin|kochi|malabar|chalakudy|ashtamudi|"
    r"kayamkulam|alleppey|calicut|kozhikode|ponnani|western coast of india|"
    r"southwest coast of india|south ?west coast|indus|kachchh|kutch|rann|"
    r"saraswati|sarasvati|ghaggar|gujarat|sind|makran", re.I)
PROCESS = re.compile(
    r"palaeo|paleo|holocene|quaternary|shoreline|coastal|coast|delta|lagoon|"
    r"estuar|sea[- ]?level|strandline|beach|barrier|spit|channel|fluvial|"
    r"sediment|geomorph|landform|mudbank|mud bank|neotecton|subsid", re.I)

ART = re.compile(r"/jgsi/article/view/(\d+)")
PDF = re.compile(r'<meta name="citation_pdf_url" content="([^"]+)"')
META = re.compile(r'<meta name="citation_([a-z_]+)" content="([^"]*)"')


def get(url, tries=3):
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as exc:
            if attempt == tries - 1:
                print(f"      failed: {exc}")
                return b""
            time.sleep(2 * (attempt + 1))
    return b""


def search(term):
    """Article identifiers for one query, following the result pages."""
    found, page = [], 1
    while page <= 5:
        url = (f"{BASE}/search/search?query={urllib.parse.quote(term)}"
               f"&searchPage={page}")
        html = get(url).decode("utf-8", "replace")
        ids = ART.findall(html)
        if not ids:
            break
        new = [i for i in ids if i not in found]
        found.extend(new)
        # OJS repeats the last page indefinitely rather than returning empty, so
        # stop when a page adds nothing new.
        if not new:
            break
        page += 1
        time.sleep(0.4)
    return found


def record(art_id):
    html = get(f"{BASE}/article/view/{art_id}").decode("utf-8", "replace")
    if not html:
        return None
    meta = {}
    for key, val in META.findall(html):
        meta.setdefault(key, val)
    pdf = PDF.search(html)
    return {
        "id": art_id,
        "title": re.sub(r"\s+", " ", meta.get("title", "")).strip(),
        "authors": meta.get("author", ""),
        "year": (meta.get("date") or "")[:4],
        "volume": meta.get("volume", ""),
        "firstpage": meta.get("firstpage", ""),
        "pdf_url": pdf.group(1) if pdf else "",
        "page_url": f"{BASE}/article/view/{art_id}",
    }


def slug(r):
    first = (r["authors"].split(",")[0] or "anon").split()[-1]
    stub = re.sub(r"[^a-z0-9]+", "-", r["title"].lower())[:70].strip("-")
    return f"{r['region']}_{first}{r['year']}_{stub}.pdf"


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    seen_ids, by_title, rows = set(), {}, []

    for region, terms in QUERIES.items():
        for term in terms:
            ids = search(term)
            print(f"{region:11s} {term:28s} {len(ids):4d} hits")
            for art_id in ids:
                if art_id in seen_ids:
                    continue
                seen_ids.add(art_id)
                r = record(art_id)
                time.sleep(0.3)
                if not r or not r["title"]:
                    continue
                t = r["title"]
                if not (PLACE.search(t) and PROCESS.search(t)):
                    continue
                key = re.sub(r"[^a-z0-9]", "", t.lower())
                if key in by_title:
                    by_title[key]["duplicate_ids"] += f" {art_id}"
                    continue
                r.update(region=region, query=term, duplicate_ids="")
                by_title[key] = r
                rows.append(r)
                print(f"    keep {r['year']}  {t[:78]}")

    print(f"\n{len(rows)} relevant of {len(seen_ids)} inspected\n")

    # Download last, so the catalogue exists even if the host tires of us.
    for r in rows:
        r["file"] = ""
        if not r["pdf_url"]:
            continue
        path = DEST / slug(r)
        if path.exists() and path.stat().st_size > 20000:
            r["file"] = path.name
            continue
        blob = get(r["pdf_url"])
        # The archive answers a missing galley with an HTML notice and a 200, so
        # the magic bytes decide whether this is a PDF.
        if blob[:5] != b"%PDF-":
            print(f"   not a pdf: {r['title'][:60]}")
            continue
        path.write_bytes(blob)
        r["file"] = path.name
        print(f"   {len(blob)//1024:5d} kB  {path.name[:76]}")
        time.sleep(0.5)

    fields = ["region", "year", "title", "authors", "volume", "firstpage",
              "file", "pdf_url", "page_url", "id", "duplicate_ids", "query"]
    dest = OUT / "jgsi_catalogue.csv"
    with open(dest, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows({k: r.get(k, "") for k in fields} for r in rows)

    got = sum(1 for r in rows if r["file"])
    print(f"\n{got} of {len(rows)} downloaded -> {DEST}")
    print(f"catalogue -> {dest}")
    from collections import Counter
    for k, v in Counter(r["region"] for r in rows).most_common():
        print(f"   {k:12s} {v}")


if __name__ == "__main__":
    main()
