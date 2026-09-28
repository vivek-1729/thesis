"""Search every PDF in the dossier for mentions of the six disputed ports.

Extracts page-level text once and caches it, then writes a per-city digest of every
hit with its source and page number, so a claim can always be traced back to a page.
"""
import re
import sys
import unicodedata
from pathlib import Path

import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parent.parent          # .../Thesis/Code
LIB = ROOT.parent / "library"                          # .../Thesis/library
CITIES = ROOT / "cities"
CACHE = LIB / "text-cache"

TERMS = {
    "01-leuke-kome": ["Leuke Kome", "Leuce Come", "Leukos Limen", "Aynuna", "Ainuna",
                      "al-Wajh", "Wajh", "Khuraybah"],
    "02-barbarikon": ["Barbarikon", "Barbaricum", "Barbarike", "Banbhore", "Bhambore",
                      "Bhanbhore", "Debal", "Daybul", "Minnagar"],
    "03-rhapta":     ["Rhapta", "Rhapton", "Azania", "Rufiji", "Menouthias", "Menuthias",
                      "Pangani", "Mafia"],
    "04-tyndis":     ["Tyndis", "Tundis", "Ponnani", "Tanur", "Kadalundi", "Koyilandy",
                      "Panthalayani", "Pantalayini",
                      "Muziris", "Mouziris", "Muchiri", "Muciri", "Pattanam", "Kodungallur"],
    "05-nelkunda":   ["Nelkunda", "Nelcynda", "Melkynda", "Neacyndi", "Niranam",
                      "Nirannam", "Kottayam", "Kallada",
                      "Muziris", "Mouziris", "Pattanam", "Kodungallur"],
    "06-bakare":     ["Bakare", "Becare", "Barace", "Purakkad", "Porakad", "Pirakkad",
                      "Thevalakara",
                      "Muziris", "Mouziris", "Pattanam", "Kodungallur"],
}
WINDOW = 320


def fold(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def pages(pdf):
    """Page text, cached — re-extracting a 54 MB scan on every run is wasteful."""
    CACHE.mkdir(parents=True, exist_ok=True)
    cache = CACHE / (pdf.stem + ".txt")
    if cache.exists():
        return cache.read_text().split("\f")
    try:
        doc = fitz.open(pdf)
    except Exception as e:
        print(f"  !! cannot open {pdf.name}: {e}")
        return []
    out = [p.get_text() for p in doc]
    doc.close()
    cache.write_text("\f".join(out))
    return out


def main():
    pdfs = sorted(p for p in LIB.rglob("*.pdf") if "DUPLICATE" not in p.name)
    print(f"mining {len(pdfs)} PDFs\n")
    hits = {slug: [] for slug in TERMS}
    for pdf in pdfs:
        txt = pages(pdf)
        if not txt:
            continue
        rel = pdf.relative_to(LIB)
        n = 0
        for slug, terms in TERMS.items():
            for pno, page in enumerate(txt, 1):
                flat = fold(page)
                for t in terms:
                    for m in re.finditer(re.escape(fold(t)), flat):
                        a = max(0, m.start() - WINDOW // 3)
                        snippet = re.sub(r"\s+", " ", page[a:m.end() + WINDOW]).strip()
                        hits[slug].append((str(rel), pno, t, snippet))
                        n += 1
                        break          # one hit per term per page keeps the digest readable
        print(f"  {n:5d} hits  {rel}")

    print()
    for slug, rows in hits.items():
        srcs = sorted({r[0] for r in rows})
        out = [f"# {slug} — every mention across the PDF dossier", "",
               f"{len(rows)} passages from {len(srcs)} documents. Page numbers are PDF pages,",
               "not printed pages. Snippets are raw extraction — verify before quoting.", ""]
        for src in srcs:
            out += [f"## {src}", ""]
            for _, pno, term, snip in [r for r in rows if r[0] == src]:
                out += [f"**p.{pno}** · *{term}*", "", f"> {snip}", ""]
        dest = CITIES / slug / "pdf-mentions-digest.md"
        dest.write_text("\n".join(out))
        print(f"  {slug:16s} {len(rows):4d} passages / {len(srcs)} docs -> {dest.name}")


if __name__ == "__main__":
    main()
