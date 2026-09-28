"""Pull the passages that actually bear on where each port was.

Not every mention of a port is useful. What matters is the sentence that makes
an identification, gives a reason for or against one, reports what was found at
a site, or flags a problem. This scores passages on that basis and groups them
by port so they can be read rather than counted.
"""
import csv, re, pathlib
from collections import defaultdict

LIB = pathlib.Path("/Users/vivek/Library/Mobile Documents/com~apple~CloudDocs/"
                   "A School/Harvard/Thesis/library")
OUT = pathlib.Path(__file__).resolve().parents[1] / "docs"

PORTS = {
 "Leuke Kome": r"Leuk[eē]\s*K[oō]m[eē]|Leucos Limen|Aynuna|'Aynuna|Khuraybah|al-Wajh|Wajh",
 "Barbarikon": r"Barbarik[oó]n|Barbaricum|Banbhore|Bhambore|Bhanbhore|Minnagar",
 "Tyndis":     r"Tyndis|Tundis|Ponnani|Tanur|Kadalundi|Beypore|Chaliyam|Koyilandy|Pantalayini",
 "Nelkynda":   r"Nelkynda|Nelcynda|Nelkunda|Melkynda|Niranam|Neendakara",
 "Bakare":     r"Bakar[eē]|Becare|Purakkad|Pirakkad|Kallada|Thevalakara",
 "Muziris":    r"Muziris|Muciri|Mouziris|Pattanam|Kodungallur|Cranganore",
 "Rhapta":     r"Rhapta|Rapta|Menuthias|Menouthias|Azania|Rufiji|Unguja Ukuu",
}

# Language that marks a passage as making a claim rather than mentioning a name.
ARGUES = re.compile(
 r"identif|equat|locat(?:e|ed|ion)|situated|placed?\b|propos|suggest|argu|"
 r"must be|cannot be|probably|perhaps|generally accepted|consensus|"
 r"no doubt|certainly|disput|contest|controvers|problem|difficult|"
 r"evidence|excavat|yielded|recovered|discover|finds?\b|sherds?|"
 r"distance|stadia|days'? sail|north of|south of|upriver|up the river|mouth of",
 re.I)
STRONG = re.compile(
 r"identif|equat|must be|cannot be|generally accepted|consensus|"
 r"disput|contest|controvers|no doubt|has not been|remains uncertain|"
 r"stadia|yielded|excavat", re.I)
# Bibliography lines, indexes and running heads look like prose to a regex.
JUNK = re.compile(r"^\s*\d|\b(?:pp?\.|vol\.|ed\.|eds\.|forthcoming|in press)\b.*\d{4}|"
                  r"^[A-Z][a-z]+,\s+[A-Z]\.|\b\d{4}[a-z]?:\s*\d+", re.M)

def sentences(t):
    t = re.sub(r"-\n", "", t)
    t = re.sub(r"\s*\n\s*", " ", t)
    t = re.sub(r"\s{2,}", " ", t)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z(])", t)]

def page_index(text):
    return [(m.start(), int(m.group(1))) for m in re.finditer(r"\[\[PAGE (\d+)\]\]", text)]

def page_at(idx, pos):
    p = 0
    for s, n in idx:
        if s <= pos: p = n
        else: break
    return p

def main():
    files = sorted(LIB.glob("text-cache/*.txt")) + sorted(LIB.glob("iar-text/*.txt"))
    out = defaultdict(list)
    for f in files:
        text = f.read_text(errors="ignore")
        idx = page_index(text)
        flat = re.sub(r"\[\[PAGE \d+\]\]", " ", text)
        pos = 0
        for s in sentences(flat):
            start = flat.find(s[:40], pos) if len(s) > 40 else pos
            pos = max(pos, start + 1)
            if not (90 < len(s) < 700): continue
            if JUNK.search(s): continue
            if not ARGUES.search(s): continue
            for port, pat in PORTS.items():
                if not re.search(pat, s): continue
                score = len(STRONG.findall(s)) * 2 + len(ARGUES.findall(s))
                out[port].append((score, s, f.stem, page_at(idx, start)))
    tot = 0
    for port in PORTS:
        rows = out[port]
        seen, keep = set(), []
        for sc, s, src, pg in sorted(rows, key=lambda r: -r[0]):
            k = re.sub(r"\W+", "", s.lower())[:70]
            if k in seen: continue
            seen.add(k); keep.append((sc, s, src, pg))
        out[port] = keep
        tot += len(keep)
        print(f"  {port:12s}{len(rows):>6} matched{len(keep):>6} after dedupe")
    print(f"\n{tot} distinct passages")
    dest = OUT.parent / "data" / "processed" / "port_passages.csv"
    with open(dest, "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["port","score","passage","source","page"])
        for port in PORTS:
            for sc, s, src, pg in out[port]:
                w.writerow([port, sc, s, src, pg])
    print(f"-> {dest.name}")

if __name__ == "__main__":
    main()
