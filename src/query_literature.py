"""Systematic bibliographic sweep for every port and candidate.

Crossref for discovery, Unpaywall to resolve open access. The point is not to
find things I already have but to establish, per site, how much scholarship
exists at all -- which is a second, independent measure of the attention
asymmetry the material layer already showed.

Output is a candidate bibliography, not a reading list: Crossref matches on
loose text, so relevance has to be judged afterwards.
"""
import urllib.request, urllib.parse, json, csv, time, pathlib, re

OUT = pathlib.Path(__file__).resolve().parents[1] / "data" / "processed"
MAIL = "vivekshah@college.harvard.edu"
UA = {"User-Agent": f"thesis-research/1.0 (mailto:{MAIL})"}

QUERIES = {
    "Rhapta": ["Rhapta Periplus", "Rhapta Azania metropolis", "Rufiji delta archaeology",
               "Mafia Island archaeology Roman", "Unguja Ukuu Zanzibar trade",
               "Tanzania coast early Iron Age Indian Ocean trade", "Azania Periplus East Africa"],
    "Barbarikon": ["Barbarikon Periplus", "Banbhore excavation Sindh", "Bhambore Indus delta",
                   "Indus delta ancient port archaeology", "Daybul Debal port"],
    "Leuke Kome": ["Leuke Kome", "Aynuna Nabataean port Red Sea", "al-Wajh survey Saudi Arabia",
                   "Nabataean Red Sea harbour", "Leuke Kome location Periplus"],
    "Tyndis": ["Tyndis Periplus Malabar", "Ponnani ancient port Kerala",
               "Malabar coast Roman trade ports"],
    "Nelkynda": ["Nelkynda Periplus", "Nelcynda Malabar port", "Niranam Kerala archaeology"],
    "Bakare": ["Bakare Periplus Malabar", "Purakkad Kerala port history"],
    "Muziris": ["Muziris location", "Pattanam excavation Kerala", "Muziris papyrus",
                "Periyar delta archaeology Muziris"],
    "Berenike": ["Berenike Red Sea excavation", "Berenike Egypt Indian Ocean trade"],
    "Myos Hormos": ["Myos Hormos Quseir al-Qadim", "Quseir al-Qadim Roman port"],
    "Kane / Qana": ["Qana Hadramawt port", "Kane Periplus South Arabia", "Bir Ali Qani excavation"],
    "Moscha / Sumhuram": ["Sumhuram Khor Rori", "Moscha Limen frankincense port"],
    "Barygaza": ["Barygaza Bharuch ancient port", "Gujarat Roman trade Barygaza"],
    "Adulis": ["Adulis Eritrea excavation", "Adulis Aksum Red Sea port"],
    "Arikamedu": ["Arikamedu excavation Roman", "Arikamedu rouletted ware"],
    "general": ["Periplus Maris Erythraei", "Indo-Roman trade ceramics",
                "Roman Red Sea trade archaeology", "monsoon Indian Ocean Roman navigation",
                "Roman coins India distribution"],
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

def crossref(q, rows=25):
    u = "https://api.crossref.org/works?" + urllib.parse.urlencode(
        {"query": q, "rows": rows, "mailto": MAIL,
         "select": "DOI,title,author,issued,container-title,type,abstract,URL,is-referenced-by-count"})
    d = get(u)
    return d.get("message", {}).get("items", []) if "_err" not in d else []

def oa(doi):
    d = get(f"https://api.unpaywall.org/v2/{doi}?email={MAIL}", tries=2)
    if "_err" in d:
        return "", "", ""
    loc = d.get("best_oa_location") or {}
    return ("Y" if d.get("is_oa") else "N",
            loc.get("url_for_pdf") or "",
            d.get("journal_name") or "")

def main():
    rows, seen = [], set()
    for port, qs in QUERIES.items():
        n0 = len(rows)
        for q in qs:
            for it in crossref(q):
                doi = (it.get("DOI") or "").lower()
                if not doi or doi in seen:
                    continue
                seen.add(doi)
                yr = (it.get("issued", {}).get("date-parts") or [[None]])[0][0]
                auth = "; ".join(
                    f"{a.get('family','')}, {a.get('given','')[:1]}."
                    for a in (it.get("author") or [])[:4])
                rows.append({
                    "port": port, "query": q,
                    "year": yr or "",
                    "title": re.sub(r"\s+", " ", (it.get("title") or ["?"])[0])[:220],
                    "authors": auth[:160],
                    "venue": ((it.get("container-title") or [""])[0])[:90],
                    "type": it.get("type", ""),
                    "cited_by": it.get("is-referenced-by-count", 0),
                    "doi": doi, "url": it.get("URL", ""),
                    "is_oa": "", "oa_pdf": "",
                })
            time.sleep(0.4)
        print(f"  {port:20s} +{len(rows)-n0:4d} new  (total {len(rows)})", flush=True)

    print("\nresolving open access via Unpaywall ...")
    for i, r in enumerate(rows, 1):
        r["is_oa"], r["oa_pdf"], jn = oa(r["doi"])
        if not r["venue"] and jn:
            r["venue"] = jn[:90]
        if i % 100 == 0:
            print(f"   {i}/{len(rows)}", flush=True)
        time.sleep(0.12)

    dest = OUT / "literature_candidates.csv"
    with open(dest, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    noa = sum(1 for r in rows if r["is_oa"] == "Y")
    print(f"\n{len(rows)} works -> {dest.name}   ({noa} open access, {noa/len(rows):.0%})")

if __name__ == "__main__":
    main()
