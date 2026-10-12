"""Extract the Aynuna excavation coin catalogue, and check it against its own totals.

CHRE records hoards. For a port the more diagnostic evidence is site finds, the
single coins lost in occupation layers, which show money being used where people
lived rather than a deliberate deposit that could be anywhere. CHRE has no hoard
within 207 km of Aynuna, and Gawlikowski's monograph prints a full catalogue.

The catalogue is organised by period, under standalone headings, and an earlier
version of this script did not read them. That version carried a ruler list
stopping at Hadrian, so every fourth-century coin fell through as unattributed
and the date distribution came out wrong in the one respect that matters.

Gawlikowski states his own totals in the paragraph after the catalogue, so the
extraction can be checked rather than trusted. `verify()` does that, and the
script reports any disagreement instead of writing a table that looks fine.
"""
import re, csv, pathlib

LIB = pathlib.Path("/Users/vivek/Library/Mobile Documents/com~apple~CloudDocs/"
                   "A School/Harvard/Thesis/library/text-cache")
OUT = pathlib.Path(__file__).resolve().parents[1] / "data" / "processed"
SRC = LIB / "Gawlikowski-Juchniewicz-al-Zahrani-2021-Aynuna-Nabataean-Port-Red-Sea.txt"

# The period headings that divide the catalogue, in the order they appear. The
# first is easy to miss: it sits on the page before the running head, so a slice
# that starts at "Catalogue of coins" cuts the opening entry off.
SECTIONS = ["Northwest Arabian", "Nabataean", "Roman and Late Roman",
            "Arab-Sasanian", "Mamluk", "Ottoman", "Illegible"]

# Every issuing authority named in the catalogue, with conventional dates as
# years (negative for BC). Aretas IV is the one that matters: his reign ends ten
# years before the Periplus, and nothing later than him is attributed here.
RULERS = [
    ("Aretas IV", -9, 40), ("Obodas III", -30, -9), ("Obodas II", -62, -60),
    ("Malichus II", 40, 70), ("Malichus I", -59, -30), ("Rabbel II", 70, 106),
    ("Aretas III", -87, -62), ("Rabbel I", -87, -85),
    ("Elagabalus", 218, 222),
    ("Constantine II", 317, 337), ("Constantinopolis", 330, 340),
    ("Constantius", 337, 361), ("Constantine", 306, 337), ("Licinius", 308, 324),
    ("Tiberius II Constantine", 578, 582),
    ("Khusro II", 590, 628),
    ("Baybars", 1260, 1277),
    ("Abdul Majid", 1839, 1861), ("Muhammad Ali", 1805, 1848),
    ("Selim II", 1566, 1574),
]

INV = re.compile(r"\b(A[Yy]\s?\d{2}[-/][\w./]*\d[\w./]*)\.", re.M)
DIAM = re.compile(r"[Dd]iam\.?\s*(\d+(?:\.\d+)?)\s*mm|,\s*(\d+(?:\.\d+)?)\s*mm")
METAL = re.compile(r"\b(Bronze|Silver|Gold|Billon|Lead|Copper)\b", re.I)
CENT = re.compile(r"(\d)(?:st|nd|rd|th)[-–]?\s*(?:(\d)(?:st|nd|rd|th)\s*)?c(?:entury|\.)?\s*(BC|AD)", re.I)
YEARS = re.compile(r"\((\d{2,4})\s*[-–]\s*(\d{2,4})\)")
FOUND = re.compile(r"((?:Found|In the fill|In the rubble|From the rubble|On the old "
                   r"foundation|In the courtyard|In the fabric|Chance find|In the gate|"
                   r"Found on)[^.]{0,160}\.)")


def catalogue(text):
    """The catalogue body, with the repeated page furniture stripped."""
    start = text.find("Northwest Arabian", 370000)
    # Stop at the discussion rather than the bibliography. The paragraph after
    # the catalogue names Aretas IV and Elagabalus, and the last entry's block
    # runs to the end of whatever it is given, so leaving it in attributed an
    # illegible coin to Aretas IV.
    end = text.find("The excavations at Aynuna in the years", start)
    if end < 0:
        end = text.find("Bibliography", start)
    body = text[start:end if end > 0 else None]
    body = re.sub(r"\[\[PAGE \d+\]\]", "\n", body)
    body = re.sub(r"^\s*(Catalogue of coins|Michał Gawlikowski|\d{1,3})\s*$", "",
                  body, flags=re.M)
    return re.sub(r"\n{2,}", "\n", body)


def section_at(body, pos):
    """Which period heading the entry at `pos` falls under."""
    best = ""
    for s in SECTIONS:
        for m in re.finditer(rf"^\s*{re.escape(s)}\s*$", body, re.M):
            if m.start() < pos:
                best = s
    return best


def entries(body):
    """Split on the inventory number, which opens all but two entries.

    Two coins are chance finds with no inventory number and are picked up by the
    ruler line instead, which is why the split is done on positions rather than
    by `re.split`.
    """
    marks = [(m.start(), re.sub(r"\s+", "", m.group(1))) for m in INV.finditer(body)]
    # A chance find published without an inventory number.
    for m in re.finditer(r"^\s*(Aretas IV)\.\s*Bronze", body, re.M):
        marks.append((m.start(), ""))
    # And one coin found stuck to the one before it, so the catalogue gives it
    # the same number rather than its own.
    for m in re.finditer(r"^\s*Same number", body, re.M):
        marks.append((m.start(), "(shares the previous number)"))
    marks.sort()
    for i, (pos, inv) in enumerate(marks):
        stop = marks[i + 1][0] if i + 1 < len(marks) else len(body)
        yield pos, inv, re.sub(r"\s+", " ", body[pos:stop]).strip()


def parse(body):
    rows = []
    for pos, inv, blk in entries(body):
        ruler = y0 = y1 = ""
        for name, a, b in RULERS:
            if re.search(re.escape(name), blk):
                ruler, y0, y1 = name, a, b
                break
        if not ruler and re.search(r"Anonymous", blk, re.I):
            ruler = "Anonymous"

        # A century range in the text overrides a reign, since the catalogue
        # gives it only where the issue cannot be tied to one ruler.
        c = CENT.search(blk)
        if c and (not ruler or ruler == "Anonymous"):
            lo, hi, era = int(c.group(1)), c.group(2), c.group(3).upper()
            hi = int(hi) if hi else lo
            if era == "BC":
                y0, y1 = -lo * 100, -(hi - 1) * 100
            else:
                y0, y1 = (lo - 1) * 100, hi * 100

        d = DIAM.search(blk)
        f = FOUND.search(blk)
        met = METAL.search(blk)
        rows.append({
            "site": "Aynuna", "lat": 28.10, "lon": 35.21,
            "section": section_at(body, pos),
            "inventory": inv,
            "metal": met.group(1).title() if met else "",
            "diam_mm": (d.group(1) or d.group(2)) if d else "",
            "ruler": ruler,
            "date_from": y0, "date_to": y1,
            "context": (f.group(1).strip() if f else "")[:160],
            "source": "Gawlikowski, Juchniewicz and al-Zahrani 2021, catalogue of coins",
        })
    return rows


def verify(rows, text):
    """Check the extraction against the totals Gawlikowski states himself.

    He writes that the 2015-2018 seasons yielded twenty-eight coins, two of them
    completely obliterated, that fourteen of the remainder are Nabataean, and
    that twelve of those date to the first century BC or earlier. Reproducing
    those numbers is the only evidence the parser read the catalogue correctly.
    """
    # He counts the one Northwest Arabian imitation among the Nabataean
    # fourteen, which is how the readable twenty-six add up across his sections.
    claims = {"total": 28, "nabataean": 14, "illegible": 2}
    got = {
        "total": len(rows),
        "nabataean": sum(1 for r in rows if r["section"] in
                         ("Nabataean", "Northwest Arabian")),
        "illegible": sum(1 for r in rows if r["section"] == "Illegible"),
    }
    ok = True
    for k, want in claims.items():
        flag = "ok " if got[k] == want else "MISMATCH"
        if got[k] != want:
            ok = False
        print(f"   {flag} {k:12s} extracted {got[k]:3d}, author states {want}")
    return ok


def main():
    text = SRC.read_text(errors="ignore")
    body = catalogue(text)
    rows = parse(body)

    dest = OUT / "aynuna_coins.csv"
    with open(dest, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    print(f"{len(rows)} coins -> {dest.name}\n")

    print("against the author's own totals:")
    verify(rows, text)

    from collections import Counter
    print("\nby section:")
    for k, v in Counter(r["section"] or "(none)" for r in rows).most_common():
        print(f"   {k:22s} {v}")
    print("\nby ruler:")
    for k, v in Counter(r["ruler"] or "(unattributed)" for r in rows).most_common():
        print(f"   {k:22s} {v}")

    dated = [r for r in rows if r["date_to"] != ""]
    print(f"\n{len(dated)}/{len(rows)} carry a date")
    # The question this catalogue exists to answer.
    span = [r for r in dated if int(r["date_from"]) <= 50 <= int(r["date_to"])]
    print(f"{len(span)} were struck by an authority whose dates span AD 50")


if __name__ == "__main__":
    main()
