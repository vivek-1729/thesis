"""Search the Indian Archaeology: A Review run for the disputed-port candidates.

IAR is the annual record of every excavation and exploration reported in India
since 1953. If a Kerala candidate for Tyndis, Nelkynda or Bakare has ever been
dug, it is recorded here. This is the only way to tell 'never excavated' from
'excavated but not in my library'.

Entries are numbered and headed, e.g.
    11. MENHIR, DISTRICT KOLLAM.-- P. Sreedharan of the Department of ...
so a hit can be resolved back to the excavation it belongs to.
"""
import csv, re, pathlib

TXT = pathlib.Path("/Users/vivek/Library/Mobile Documents/com~apple~CloudDocs/"
                   "A School/Harvard/Thesis/library/iar-text")
OUT = pathlib.Path(__file__).resolve().parents[1] / "data" / "processed"

TERMS = {
    # Tyndis candidates
    "Ponnani": "Tyndis", "Tanur": "Tyndis", "Kadalundi": "Tyndis",
    "Beypore": "Tyndis", "Chaliyam": "Tyndis", "Koyilandy": "Tyndis",
    "Pantalayini": "Tyndis", "Panthalayani": "Tyndis", "Quilandy": "Tyndis",
    # Nelkynda candidates
    "Niranam": "Nelkynda", "Neendakara": "Nelkynda", "Nindakara": "Nelkynda",
    "Quilon": "Nelkynda", "Kollam": "Nelkynda",
    # Bakare candidates
    "Purakkad": "Bakare", "Pirakkad": "Bakare", "Porakad": "Bakare",
    "Kallada": "Bakare", "Thevalakara": "Bakare", "Thevalakkara": "Bakare",
    # Muziris candidates
    "Pattanam": "Muziris", "Kodungallur": "Muziris", "Cranganore": "Muziris",
    "Mathilakam": "Muziris", "Madilakam": "Muziris", "Paravur": "Muziris",
    # ancient names, to catch discussion rather than fieldwork
    "Muziris": "ancient name", "Tyndis": "ancient name",
    "Nelcynda": "ancient name", "Nelkynda": "ancient name", "Bakare": "ancient name",
    # diagnostic finds worth knowing about anywhere on the Malabar coast
    "Roman coin": "diagnostic", "amphora": "diagnostic", "Rouletted": "diagnostic",
    "rouletted": "diagnostic", "Roman pottery": "diagnostic",
    "terra sigillata": "diagnostic", "Terra Sigillata": "diagnostic",
}

# "Kollam 563 (A.D. 1387-88)" is the Kollam ERA, a dating system used all over
# the Tamil country, not the port. It is the single commonest false positive.
FALSE_POSITIVE = [
    (r"Kollam", r"Kollam\s+\d{2,4}|Kollam\s+era|of\s+the\s+Kollam"),
    (r"Quilon", r"Quilon\s+era"),
]

ENTRY = re.compile(r"\n\s*(\d{1,4})\.\s+([A-Z][A-Z0-9 ,.'’\-/()&]{4,110}?)\s*[.\-—]{1,3}")
PAGE = re.compile(r"\[\[PAGE (\d+)\]\]")

def volume_year(name):
    m = re.search(r"IAR_(\d{4}-\d{2,4})__", name)
    return m.group(1) if m else "?"

def main():
    files = sorted(TXT.glob("*.txt"))
    rows = []
    for f in files:
        t = f.read_text(errors="ignore")
        year = volume_year(f.name)
        entries = [(m.start(), m.group(1), m.group(2).strip()) for m in ENTRY.finditer(t)]
        pages = [(m.start(), int(m.group(1))) for m in PAGE.finditer(t)]

        def enclosing(pos, arr, default=None):
            best = default
            for s, *v in arr:
                if s <= pos:
                    best = v
                else:
                    break
            return best

        for term, port in TERMS.items():
            pat = rf"\b{re.escape(term)}\b" if " " not in term else re.escape(term)
            for m in re.finditer(pat, t):
                ent = enclosing(m.start(), entries, ["", ""])
                pg = enclosing(m.start(), pages, [0])
                ctx = re.sub(r"\s+", " ", t[max(0, m.start()-320):m.start()+380]).strip()
                near = t[max(0, m.start()-40):m.start()+60]
                fp = any(re.search(bad, near) for trm, bad in FALSE_POSITIVE if trm == term)
                rows.append({
                    "year": year, "term": term, "port": port,
                    "entry_no": ent[0], "entry_head": ent[1][:110],
                    "page": pg[0], "likely_false_positive": "Y" if fp else "",
                    "context": ctx, "volume": f.name,
                })
    dest = OUT / "iar_hits.csv"
    with open(dest, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    from collections import Counter
    print(f"{len(files)} volumes searched -> {len(rows)} hits")
    print(f"years: {', '.join(sorted({volume_year(f.name) for f in files}))}\n")
    real = [r for r in rows if not r["likely_false_positive"]]
    print(f"{len(rows)-len(real)} hits flagged as likely false positives "
          f"(mostly the Kollam era dating system)\n")
    rows_all, rows = rows, real
    c = Counter((r["port"], r["term"]) for r in rows)
    print(f"{'port':12s}{'term':16s}{'hits':>5s}  years")
    for (port, term), n in sorted(c.items()):
        ys = sorted({r['year'] for r in rows if r['term'] == term})
        print(f"{port:12s}{term:16s}{n:5d}  {', '.join(ys)[:64]}")
    print("\n--- candidate terms with ZERO hits ---")
    seen = {r["term"] for r in rows}
    for term, port in TERMS.items():
        if term not in seen and port not in ("diagnostic",):
            print(f"  {port:12s} {term}")

if __name__ == "__main__":
    main()
