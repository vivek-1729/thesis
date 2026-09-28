"""Extract the Aynuna excavation coin catalogue.

CHRE records hoards. For a port, the more diagnostic evidence is site finds --
single coins lost in occupation layers, which show money actually being used
where people lived, rather than a deliberate deposit that could be anywhere.
CHRE has no hoard within 207 km of Aynuna, but Gawlikowski's monograph prints a
full catalogue of excavated coins. This turns it into data.
"""
import re, csv, pathlib

LIB = pathlib.Path("/Users/vivek/Library/Mobile Documents/com~apple~CloudDocs/"
                   "A School/Harvard/Thesis/library/text-cache")
OUT = pathlib.Path(__file__).resolve().parents[1] / "data" / "processed"
SRC = LIB / "Gawlikowski-Juchniewicz-al-Zahrani-2021-Aynuna-Nabataean-Port-Red-Sea.txt"

INV = re.compile(r"\b(A[Yy]\s?\d{2}[-/][\w./]*\d[\w./]*)\.", re.M)
DIAM = re.compile(r"[Dd]iam\.?\s*(\d+(?:\.\d+)?)\s*mm")
METAL = re.compile(r"\b(Bronze|Silver|Gold|Billon|Lead|Copper)\b", re.I)
FOUND = re.compile(r"(Found[^.]{0,150}\.|In the fill[^.]{0,120}\.|From the rubble[^.]{0,120}\.|"
                   r"On the old foundation[^.]{0,120}\.)")
# Rulers named in the catalogue, with conventional dates.
RULERS = [
    ("Aretas IV", -9, 40), ("Obodas III", -30, -9), ("Obodas II", -62, -60),
    ("Malichus I", -59, -30), ("Malichus II", 40, 70), ("Rabbel II", 70, 106),
    ("Aretas III", -87, -62), ("Rabbel I", -87, -85),
    ("Augustus", -27, 14), ("Tiberius", 14, 37), ("Claudius", 41, 54),
    ("Nero", 54, 68), ("Vespasian", 69, 79), ("Trajan", 98, 117),
    ("Hadrian", 117, 138),
]
CENT = re.compile(r"(\d)(?:st|nd|rd|th)[-–\s]*(?:(\d)(?:st|nd|rd|th)\s*)?c(?:entury|\.)?\s*(BC|AD)", re.I)

def main():
    t = SRC.read_text(errors="ignore")
    start = t.find("Catalogue of coins", 300000)
    body = t[start:]
    end = body.find("Bibliography")
    if end > 0:
        body = body[:end]
    body = re.sub(r"\[\[PAGE (\d+)\]\]", r"|||PAGE\1|||", body)

    # Split into entries on the inventory number, which always opens one.
    parts = INV.split(body)
    rows = []
    for i in range(1, len(parts) - 1, 2):
        inv = re.sub(r"\s+", "", parts[i])
        blk = parts[i + 1][:900]
        page = ""
        m = re.search(r"\|\|\|PAGE(\d+)\|\|\|", blk)
        if m: page = m.group(1)
        blk_clean = re.sub(r"\|\|\|PAGE\d+\|\|\|", " ", blk)
        blk_clean = re.sub(r"\s+", " ", blk_clean).strip()

        ruler, y0, y1 = "", "", ""
        for name, a, b in RULERS:
            if re.search(re.escape(name), blk_clean):
                ruler, y0, y1 = name, a, b
                break
        if not ruler and re.search(r"Anonymous", blk_clean, re.I):
            ruler = "Anonymous"
        c = CENT.search(blk_clean)
        if c and not y0:
            hi, lo, era = int(c.group(1)), c.group(2), c.group(3).upper()
            lo = int(lo) if lo else hi
            if era == "BC":
                y0, y1 = -hi * 100, -(lo - 1) * 100
            else:
                y0, y1 = (hi - 1) * 100, lo * 100

        md = DIAM.search(blk_clean); mm = METAL.search(blk_clean); fd = FOUND.search(blk_clean)
        rows.append({
            "site_key": "aynuna", "site_display": "Aynuna / Khuraybah",
            "port_candidate_for": "Leuke Kome",
            "inventory": inv,
            "metal": mm.group(1).title() if mm else "",
            "diameter_mm": md.group(1) if md else "",
            "ruler": ruler,
            "date_from": y0, "date_to": y1,
            "find_context": (fd.group(1)[:150] if fd else ""),
            "description": blk_clean[:300],
            "page": page,
            "source": "Gawlikowski, Juchniewicz & al-Zahrani 2021, Aynuna catalogue of coins",
        })

    dest = OUT / "site_find_coins.csv"
    with open(dest, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    from collections import Counter
    print(f"{len(rows)} excavated coins -> {dest.name}\n")
    print("by ruler:")
    for k, v in Counter(r["ruler"] or "(unattributed)" for r in rows).most_common():
        print(f"   {k:20s}{v}")
    print("\nby metal:")
    for k, v in Counter(r["metal"] or "(unstated)" for r in rows).most_common():
        print(f"   {k:20s}{v}")
    dated = [r for r in rows if r["date_from"] != ""]
    print(f"\n{len(dated)}/{len(rows)} carry a date")
    if dated:
        print(f"range: {min(int(r['date_from']) for r in dated)} to "
              f"{max(int(r['date_to']) for r in dated)}")

if __name__ == "__main__":
    main()
