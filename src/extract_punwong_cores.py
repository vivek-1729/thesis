"""Extract the Tanzanian mangrove cores and sea-level index points.

Rhapta had no dated geographic evidence at all until the second literature sweep
turned up Punwong's 2013 Leeds thesis. It holds radiocarbon-dated cores from the
northern Rufiji Delta, which is the Rhapta neighbourhood, and from Unguja Ukuu
and Makoba Bay on Zanzibar, which are the two nearest places anyone has dug.

What makes it worth tabulating rather than citing is the index points. A
mangrove grows within a known height band relative to sea level, so a dated
mangrove peat at a known altitude constrains where the sea stood, with an
indicative range attached. That is the form the errors-in-variables sea-level
method in `STATISTICAL-PLAN.md` expects, and no other port region has supplied
it.

The tables are laid out in columns that the PDF's text layer returns one cell
per line, so this reads them positionally rather than by regular expression, and
checks each row has the shape a date should have before keeping it.
"""
import csv, pathlib, re

import fitz

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = (ROOT / "library" / "oa-harvest" /
       "rhapta-tanzania_Punwong2013_Holocene-mangrove-dynamics-and-sea-level-changes-records-from.pdf")
OUT = pathlib.Path(__file__).resolve().parents[1] / "data" / "processed"

# Which site each core prefix belongs to, and where that site is. The thesis
# gives core locations in its site chapters rather than in the date tables.
SITES = {
    "NR": ("Rufiji Delta, northern", -7.80, 39.30),   # ANR, BNR, CNR
    "MAK": ("Makoba Bay, Zanzibar", -5.95, 39.22),
    "UU": ("Unguja Ukuu, Zanzibar", -6.35, 39.33),
}

LAB = re.compile(r"\b((?:UBA|Wk|SUERC|Beta|Poz|OxA)-?\s?\d{4,6})\b")
NUM = re.compile(r"^-?\d+(?:\.\d+)?$")


def site_of(core):
    for key, (name, lat, lon) in SITES.items():
        if core.upper().endswith(key) or key in core.upper():
            return name, lat, lon
    return "", "", ""


def rows_from(page_text):
    """One record per lab code, reading the cells that follow it.

    The columns are site, altitude, depth, lab code, delta13C, then the
    radiocarbon age and its calibrated range. Reading forward from the lab code
    is more robust than reading the line, because the text layer breaks a table
    row across many lines and not always the same number of them.
    """
    cells = [c.strip() for c in page_text.split("\n") if c.strip()]
    out = []
    for i, c in enumerate(cells):
        m = LAB.fullmatch(c) or LAB.fullmatch(c.replace(" ", ""))
        if not m:
            continue
        lab = m.group(1).replace(" ", "")
        back = cells[max(0, i - 3):i]
        # Stop at the next lab code. One sample, UBA-15386, failed to make
        # graphite and has no age at all, and an unbounded scan forward gave it
        # the age of the row below, which is a wrong number that looks right.
        fwd = []
        for f in cells[i + 1:i + 10]:
            if LAB.fullmatch(f) or LAB.fullmatch(f.replace(" ", "")):
                break
            fwd.append(f)
        core = next((b for b in back if re.match(r"^[A-Z]-?[A-Z]{2,4}-?\d?$", b)), "")
        nums_back = [b for b in back if NUM.match(b)]
        alt = nums_back[0] if len(nums_back) > 0 else ""
        depth = nums_back[1] if len(nums_back) > 1 else ""
        # The radiocarbon age is the first "N ± M" after the lab code.
        age = err = ""
        for j, f in enumerate(fwd):
            a = re.match(r"^(\d{3,5})\s*[±+]\s*(\d{1,3})$", f)
            if a:
                age, err = a.group(1), a.group(2)
                break
            a = re.match(r"^(\d{3,5})$", f)
            if a and j + 1 < len(fwd) and re.match(r"^[±+]?\s*\d{1,3}$", fwd[j + 1]):
                age, err = a.group(1), re.sub(r"[^\d]", "", fwd[j + 1])
                break
        cal = next((f for f in fwd if re.match(r"^\d{3,5}\s*[-–]\s*\d{3,5}$", f)), "")
        # Three samples returned post-bomb carbon, written variously as
        # "> A.D.1950" and "> A.D 1950", sometimes split across cells.
        modern = any(re.search(r"A\.?D\.?\s?1950", f) for f in fwd)
        out.append({"lab_code": lab, "core": core, "altitude_m_amsl": alt,
                    "depth_cm": depth, "c14_bp": age, "c14_err": err,
                    "cal_range_bp": cal, "post_1950": "Y" if modern else ""})
    return out


def main():
    doc = fitz.open(SRC)
    pages = [i for i in range(doc.page_count)
             if LAB.search(doc[i].get_text()) and "radiocarbon" in doc[i].get_text().lower()]
    rows, seen = [], set()
    for i in pages:
        for r in rows_from(doc[i].get_text()):
            if r["lab_code"] in seen:
                continue
            seen.add(r["lab_code"])
            name, lat, lon = site_of(r["core"])
            r.update({"site": name, "lat": lat, "lon": lon, "page": i + 1,
                      "source": "Punwong 2013, Univ. of Leeds PhD thesis"})
            rows.append(r)

    dest = OUT / "tanzania_cores.csv"
    fields = ["site", "core", "lab_code", "altitude_m_amsl", "depth_cm",
              "c14_bp", "c14_err", "cal_range_bp", "post_1950",
              "lat", "lon", "page", "source"]
    with open(dest, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows({k: r.get(k, "") for k in fields} for r in rows)

    print(f"{len(rows)} dates from pages {[p+1 for p in pages]} -> {dest.name}\n")
    from collections import Counter
    for k, v in Counter(r["site"] or "(core not matched)" for r in rows).most_common():
        print(f"   {k:28s} {v}")
    dated = [r for r in rows if r["c14_bp"]]
    print(f"\n{len(dated)} carry a radiocarbon age")
    if dated:
        ages = sorted(int(r["c14_bp"]) for r in dated)
        print(f"   youngest {ages[0]} BP, oldest {ages[-1]} BP")


if __name__ == "__main__":
    main()
