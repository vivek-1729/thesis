"""Harvest every sentence in the library that says where one of the ports was.

Scans the cached text of all 95 documents for sentences that mention a port and also
carry locational language, then groups them by port. The output is a working file for
curation, not a finished document: OCR debris and false positives are expected.
"""
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT.parent / "library/text-cache"
# Raw working file; the readable summary is position_statements.md, written by hand.
OUT = ROOT / "data/processed/_position_statements_raw_harvest.md"

PORTS = {
    "Leuke Kome": ["leuke kome", "leuce come", "leukos limen", "aynuna", "aynunah",
                   "khuraybah", "al-wajh", "el wajh"],
    "Barbarikon": ["barbarikon", "barbaricum", "barbarike", "barbarei", "banbhore",
                   "bhambore", "bhanbhore", "daybul", "debal", "minnagar"],
    "Rhapta":     ["rhapta", "rhapton", "rhaptum", "menouthias", "menuthias", "menuthesias"],
    "Tyndis":     ["tyndis", "tundis", "ponnani", "tanur", "kadalundi", "koyilandy",
                   "panthalayani", "pantalayini", "naura", "naoura"],
    "Muziris":    ["muziris", "mouziris", "muchiri", "muciri", "pattanam", "kodungallur",
                   "cranganore", "cranganur", "periyar"],
    "Nelkynda":   ["nelkynda", "nelcynda", "melkynda", "neacyndi", "niranam", "niranom",
                   "nirannam", "kottayam", "pambiyar", "pampa"],
    "Bakare":     ["bakare", "bakarei", "becare", "barace", "purakkad", "pirakkad",
                   "porakad", "thevalakara", "kallada"],
}
# A sentence only counts if it actually says something about position.
LOCATIONAL = re.compile(
    r"\b(identif|locat|situat|lies?\b|lay\b|placed?\b|position|site of|modern|"
    r"north of|south of|east of|west of|mouth of|upriver|inland|coast|harbou?r|"
    r"stadia|nautical|kilometre|kilometer|\bkm\b|miles?\b|latitude|longitude|"
    r"proposed|suggest|equat|correspond)", re.I)
SENT = re.compile(r"(?<=[.;:])\s+")


def fold(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def main():
    found = defaultdict(list)
    files = sorted(CACHE.glob("*.txt"))
    for f in files:
        raw = re.sub(r"[ \t ]+", " ", f.read_text(errors="ignore"))
        raw = re.sub(r"-\s*\n\s*", "", raw)            # rejoin words split at line ends
        text = re.sub(r"\s*\n\s*", " ", raw)
        for sent in SENT.split(text):
            s = sent.strip()
            if not (40 < len(s) < 460) or not LOCATIONAL.search(s):
                continue
            low = fold(s)
            for port, terms in PORTS.items():
                if any(t in low for t in terms):
                    found[port].append((f.stem, s))
    lines = ["# Positional statements harvested from the library", "",
             f"Sentences from {len(files)} documents that name a port and say something about",
             "where it was. Raw harvest for curation — OCR debris and false positives included.", ""]
    for port in PORTS:
        rows = found[port]
        seen, uniq = set(), []
        for src, s in rows:
            k = fold(s)[:110]
            if k not in seen:
                seen.add(k); uniq.append((src, s))
        lines += [f"## {port}  — {len(uniq)} statements from "
                  f"{len({s for s, _ in uniq})} documents", ""]
        for src, s in uniq:
            lines.append(f"- **{src[:58]}** — {s}")
        lines.append("")
    OUT.write_text("\n".join(lines))
    print(f"wrote {OUT}  ({OUT.stat().st_size//1024} KB)")
    for port in PORTS:
        rows = found[port]
        print(f"  {port:12s} {len(rows):5d} raw  /  {len({s for s, _ in rows}):3d} docs")


if __name__ == "__main__":
    main()
