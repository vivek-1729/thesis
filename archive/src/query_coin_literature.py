"""Search for numismatic publications at the sites CHRE does not reach.

For each site with no hoard within range, ask whether anyone has published
coins from it at all. A site with excavated coins but no hoard is a gap in the
database; a site with neither is a gap in the record.
"""
import urllib.request, urllib.parse, json, csv, time, re, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "data" / "processed"
MAIL = "vivekshah@college.harvard.edu"
UA = {"User-Agent": f"thesis-research/1.0 (mailto:{MAIL})"}

TARGETS = {
    "Myos Hormos": ["Quseir al-Qadim coins numismatic", "Myos Hormos coins Roman Egypt"],
    "Banbhore": ["Banbhore coins numismatic Sindh", "Bhambore coin finds excavation"],
    "Qana / Kane": ["Qana Yemen coins Hadramawt numismatic", "Qani coins South Arabian"],
    "Sumhuram": ["Sumhuram coins mint Khor Rori", "Hadramawt coinage Sumhuram"],
    "Ras Hafun": ["Ras Hafun coins Somalia Roman", "Somalia Roman coins archaeology"],
    "Rufiji / Rhapta": ["Roman coins Tanzania archaeology", "Roman coins East Africa coast finds",
                        "Rufiji delta Roman finds coins"],
    "Unguja Ukuu": ["Unguja Ukuu coins Zanzibar numismatic"],
    "Mafia Island": ["Mafia Island coins archaeology Kisimani"],
    "Socotra": ["Socotra coins archaeology finds"],
    "Xiis / Heis": ["Xiis Heis Somalia coins necropolis"],
    "Hegra / Egra": ["Hegra Mada'in Salih coins Nabataean numismatic"],
    "Ptolemais Theron": ["Ptolemais Theron coins Sudan Red Sea"],
    "Sopara / Kalyan": ["Sopara coins Roman Konkan", "Kalyan Kalliena coins"],
    "Paithan / Nevasa": ["Paithan coins Satavahana Roman", "Nevasa coins excavation Roman"],
    "Chandraketugarh / Tamluk": ["Chandraketugarh coins", "Tamluk Tamralipti coins excavation"],
    "Charax": ["Charax Spasinou coins Characene"],
    "Dwarka / Nagara": ["Dwarka coins archaeology Gujarat", "Nagara Gujarat coins excavation"],
}

def get(u, tries=3):
    for i in range(tries):
        try:
            return json.load(urllib.request.urlopen(
                urllib.request.Request(u, headers=UA), timeout=60))
        except Exception:
            if i == tries - 1: return {}
            time.sleep(3)

def main():
    rows = []
    for site, qs in TARGETS.items():
        found = 0
        for q in qs:
            u = "https://api.crossref.org/works?" + urllib.parse.urlencode(
                {"query": q, "rows": 12, "mailto": MAIL,
                 "select": "DOI,title,author,issued,container-title,is-referenced-by-count"})
            for it in get(u).get("message", {}).get("items", []):
                title = re.sub(r"\s+", " ", (it.get("title") or ["?"])[0])
                # keep only titles that actually mention coins AND the region
                if not re.search(r"coin|numismat|hoard|mint|currency|denari|aurei", title, re.I):
                    continue
                rows.append({
                    "site": site, "query": q,
                    "year": (it.get("issued", {}).get("date-parts") or [[None]])[0][0] or "",
                    "title": title[:190],
                    "authors": "; ".join(f"{a.get('family','')}, {a.get('given','')[:1]}."
                                         for a in (it.get("author") or [])[:3])[:110],
                    "venue": ((it.get("container-title") or [""])[0])[:80],
                    "cited_by": it.get("is-referenced-by-count", 0),
                    "doi": it.get("DOI", ""),
                })
                found += 1
            time.sleep(0.4)
        print(f"  {site:26s} {found:>3} coin-titled hits", flush=True)
    # dedupe
    seen, uniq = set(), []
    for r in rows:
        if r["doi"] in seen: continue
        seen.add(r["doi"]); uniq.append(r)
    dest = OUT / "coin_literature_gaps.csv"
    with open(dest, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(uniq[0].keys()))
        w.writeheader(); w.writerows(uniq)
    print(f"\n{len(uniq)} distinct coin publications -> {dest.name}")

if __name__ == "__main__":
    main()
