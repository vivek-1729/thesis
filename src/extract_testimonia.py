"""Pull the passages mentioning each disputed port out of the ancient texts we hold.

The Periplus is one witness. Strabo, Pliny and Ptolemy describe the same ports
independently, and where they disagree with the Periplus -- or with each other --
that disagreement is evidence about the location.
"""
import html
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "cities/_shared-general/ancient-texts-raw"

WORKS = {
    "strabo-book16D.html": ("Strabo, *Geography* 16.4",
                            "Loeb (Jones, 1932), via LacusCurtius",
                            "https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Strabo/16D*.html"),
    "pliny-nh-6b-attalus.html": ("Pliny the Elder, *Natural History* 6 (second half)",
                                 "Bostock & Riley, via attalus.org",
                                 "https://www.attalus.org/translate/pliny_hn6b.html"),
    "ptolemy-geography-stevenson.txt": (
        "Ptolemy, *Geography* (Africa bk 4, Arabia bk 6, India bk 7)",
        "Stevenson 1932, OCR from the Internet Archive scan",
        "https://archive.org/details/claudius-ptolemy-the-geography"),
}

# Spellings vary by translator; search on all of them.
CITIES = {
    "01-leuke-kome": ("Leukē Kōmē", ["Leuce Come", "Leuce Comê", "Leuke Kome", "Leuces"]),
    "02-barbarikon": ("Barbarikon", ["Barbaricum", "Barbarike", "Barbarei", "Patale", "Patala"]),
    "03-rhapta":     ("Rhapta", ["Rhapta", "Rhaptum", "Rhapton"]),
    "04-tyndis":     ("Tyndis", ["Tyndis", "Tundis", "Tyndi"]),
    "05-nelkunda":   ("Nelkunda", ["Neacyndi", "Nelcynda", "Melkynda", "Neacydon"]),
    "06-bakare":     ("Bakarē", ["Becare", "Bacare", "Barace", "Bakare"]),
}
WINDOW = 1500


def plain(path):
    """HTML gets stripped; a .txt file (OCR) is already plain."""
    t = path.read_text(errors="ignore")
    if path.suffix.lower() in (".html", ".htm"):
        t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return re.sub(r"[ \t\xa0]+", " ", t)


def ascii_fold(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def passages(text, terms):
    """Windows around each hit, merged where they overlap so a passage isn't split."""
    flat = ascii_fold(text)
    spans = []
    for term in terms:
        for m in re.finditer(re.escape(ascii_fold(term)), flat, re.I):
            spans.append((max(0, m.start() - WINDOW // 2),
                          min(len(text), m.end() + WINDOW)))
    spans.sort()
    merged = []
    for a, b in spans:
        if merged and a <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append((a, b))
    return [re.sub(r"\s+", " ", text[a:b]).strip() for a, b in merged]


def main():
    for slug, (name, terms) in CITIES.items():
        out = [f"# {name} — testimonia outside the Periplus", "",
               "Extracted automatically as context windows around each attestation, so the",
               "edges are ragged. Verify against the printed edition before quoting.", ""]
        found = False
        for fname, (work, edition, url) in WORKS.items():
            p = RAW / fname
            if not p.exists():
                continue
            hits = passages(plain(p), terms)
            if not hits:
                continue
            found = True
            out += [f"## {work}", f"*{edition}* — {url}", ""]
            for i, h in enumerate(hits, 1):
                out += [f"### passage {i}", "", "> " + h.replace("\n", " "), ""]
        if not found:
            out += ["*No attestation found in the texts held locally.*", "",
                    "Still to obtain: Ptolemy (Africa bk 4 / Arabia bk 6 / India bk 7),",
                    "Peutinger Table, Cosmas Indicopleustes, Stephanus of Byzantium."]
        dest = ROOT / f"cities/{slug}/ancient-sources/testimonia-strabo-pliny-ptolemy.md"
        dest.write_text("\n".join(out))
        print(f"{slug:16s} {'HIT ' if found else 'none'} {dest.stat().st_size:>6d} bytes")


if __name__ == "__main__":
    main()
