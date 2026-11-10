"""Triage the Crossref sweep into things actually about our sites.

Crossref matches on loose tokens, so a raw hit count is meaningless: a search
for "Mafia Island" returns 182,000 works, nearly all about organised crime.
Relevance is judged here by requiring a site name or a Periplus-specific term
in the title, which is strict but defensible and, crucially, applied
identically to every port.
"""
import csv, re, pathlib
from collections import Counter, defaultdict

D = pathlib.Path(__file__).resolve().parents[1] / "data" / "processed"

# One or more of these in the title makes a work count as on-topic for that port.
KEY = {
    "Rhapta": r"Rhapta|Azania|Rufiji|Unguja Ukuu|Zanzibar|Mafia Island|Pangani|Tanzanian? coast|Swahili coast",
    "Barbarikon": r"Barbarikon|Banbhore|Bhambore|Bhanbhore|Indus delta|Daybul|Debal|Sindh",
    "Leuke Kome": r"Leuke Kome|Leukos Limen|Aynuna|'Aynuna|Wajh|Nabataean|Hegra|Egra",
    "Tyndis": r"Tyndis|Ponnani|Malabar|Kerala coast",
    "Nelkynda": r"Nelkynda|Nelcynda|Niranam|Malabar|Kerala coast",
    "Bakare": r"Bakare|Purakkad|Malabar|Kerala coast",
    "Muziris": r"Muziris|Pattanam|Kodungallur|Cranganore|Periyar|Muciri",
    "Berenike": r"Berenike|Berenice",
    "Myos Hormos": r"Myos Hormos|Quseir|Qusayr",
    "Kane / Qana": r"Qana|Qani|Kane|Hadramawt|Bir Ali|Yemen",
    "Moscha / Sumhuram": r"Sumhuram|Khor Rori|Moscha|Dhofar|Oman",
    "Barygaza": r"Barygaza|Bharuch|Broach|Gujarat",
    "Adulis": r"Adulis|Aksum|Axum|Eritrea|Ethiopia",
    "Arikamedu": r"Arikamedu|Poduke|Pondicherry|rouletted",
    "general": r"Periplus|Erythraean|Erythraei|Indo-Roman|Indian Ocean|Red Sea|monsoon",
}
# Titles that match a site word but belong to another field entirely.
NOISE = re.compile(r"\bmafia\b(?!\s+island)|organi[sz]ed crime|mafia-|cosa nostra|"
                   r"delta[- ]?(?:wing|function|rule|method|learning)|"
                   r"machine learning|neural network|clinical|patient|cancer|COVID|"
                   r"elasmobranch|fishery|fisheries|shark|tourism|seaweed|"
                   r"biodiversity|malaria|HIV|livelihood",
                   re.I)

def main():
    rows = list(csv.DictReader(open(D / "literature_candidates.csv")))
    for r in rows:
        pat = KEY.get(r["port"], "")
        t = r["title"]
        on = bool(pat and re.search(pat, t, re.I)) and not NOISE.search(t)
        r["on_topic"] = "Y" if on else ""
    with open(D / "literature_candidates.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    on = [r for r in rows if r["on_topic"]]
    print(f"{len(rows)} retrieved -> {len(on)} on-topic by title ({len(on)/len(rows):.0%})\n")
    print(f"{'port':20s}{'on-topic':>9}{'open access':>12}{'median yr':>10}")
    for port in KEY:
        g = [r for r in on if r["port"] == port]
        if not g: continue
        oa = sum(1 for r in g if r["is_oa"] == "Y")
        ys = sorted(int(r["year"]) for r in g if str(r["year"]).isdigit())
        med = ys[len(ys)//2] if ys else "-"
        print(f"  {port:18s}{len(g):>9}{oa:>12}{med:>10}")

    print("\nMost-cited on-topic works (a rough proxy for what the field treats as central):")
    for r in sorted(on, key=lambda x: -int(x["cited_by"] or 0))[:16]:
        flag = "OA" if r["is_oa"] == "Y" else "  "
        print(f"  [{flag}] {r['cited_by']:>4} {str(r['year']):>4}  {r['title'][:74]}")
        print(f"            {r['venue'][:66]}  {r['doi']}")

    newoa = [r for r in on if r["is_oa"] == "Y" and r["oa_pdf"]]
    print(f"\n{len(newoa)} on-topic works have a downloadable OA PDF")

if __name__ == "__main__":
    main()
