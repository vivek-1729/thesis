"""Pull Casson's commentary on each disputed port into the per-city dossiers.

Casson (1989) is the standard edition, and his General Commentary is where the
scholarly case for each identification is actually argued. Entries are keyed
chapter:page.line, so the relevant commentary is located by page range rather than
by string matching -- chapter numbers appear constantly as cross-references and
matching on them alone picks up the wrong pages.
"""
import re
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT.parent / "library"
CASSON = LIB / "ancient-sources" / "Casson-1989-Periplus-Maris-Erythraei-text-translation-commentary.pdf"

# city slug -> (label, PDF page range of the commentary, chapters covered)
SECTIONS = {
    "03-rhapta":     ("Rhapta and the Azanian coast", (152, 166), "15-18"),
    "01-leuke-kome": ("Leukē Kōmē", (161, 169), "19-20"),
    "02-barbarikon": ("Barbarikon, Minnagar and the Indus", (204, 221), "38-41"),
    "04-tyndis":     ("Tyndis and the Limyrike coast", (233, 240), "53-54"),
    "05-nelkunda":   ("Nelkynda", (234, 244), "53-56"),
    "06-bakare":     ("Bakarē", (236, 245), "54-56"),
}
APPENDICES = {
    "appendix-1-harbors-and-ports": (289, 297),
    "appendix-2-distances": (296, 302),
    "appendix-3-voyages": (301, 311),
}


def page_text(doc, i):
    t = re.sub(r"[ \t]+", " ", doc[i].get_text())
    return "\n".join(l.strip() for l in t.split("\n") if l.strip())


def write(doc, dest, title, lo, hi, note):
    out = [f"# {title}", "", "Source: Casson, *The Periplus Maris Erythraei* (Princeton 1989).",
           f"PDF pages {lo+1}-{hi}. {note}", "",
           "Raw text-layer extraction, including running heads and footnote debris.",
           "Verify against the page before quoting.", "", "---", ""]
    for i in range(lo, min(hi, doc.page_count)):
        out += [f"### PDF p.{i+1}", "", page_text(doc, i), ""]
    dest.write_text("\n".join(out))
    return dest.stat().st_size


def main():
    doc = fitz.open(CASSON)
    for slug, (label, (lo, hi), chaps) in SECTIONS.items():
        dest = ROOT / "cities" / slug / "casson-commentary.md"
        n = write(doc, dest, f"Casson on {label}", lo, hi,
                  f"Commentary on Periplus ch. {chaps}.")
        print(f"  {slug:16s} pp.{lo+1}-{hi}  {n:>7,d} bytes")
    outdir = ROOT / "cities" / "_casson-appendices"
    outdir.mkdir(exist_ok=True)
    for name, (lo, hi) in APPENDICES.items():
        n = write(doc, outdir / f"{name}.md", f"Casson — {name.replace('-', ' ')}",
                  lo, hi, "Casson's own tabulation.")
        print(f"  appendix        {name:34s} {n:>7,d} bytes")
    doc.close()


if __name__ == "__main__":
    main()
