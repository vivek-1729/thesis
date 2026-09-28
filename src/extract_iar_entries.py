"""Extract every numbered entry from the state sections of the IAR run.

Searching the Review for candidate names only finds sites somebody has already
connected to a Periplus port. A site can be excavated without that connection
ever being made, and would be invisible. This lifts whole state sections
instead, so the question becomes regional: what has been found on this coast,
of what date, since 1953.
"""
import csv, re, pathlib
from collections import Counter

TXT = pathlib.Path("/Users/vivek/Library/Mobile Documents/com~apple~CloudDocs/"
                   "A School/Harvard/Thesis/library/iar-text")
OUT = pathlib.Path(__file__).resolve().parents[1] / "data" / "processed"

STATES = ["KERALA", "TAMIL NADU", "TAMILNADU", "MADRAS", "GUJARAT", "MAHARASHTRA",
          "MYSORE", "KARNATAKA", "ANDHRA PRADESH", "PONDICHERRY"]
# State headings are typeset inconsistently: extra internal spaces ("MADHYA
# PRADESH" with three), and sometimes run inline after the previous entry
# rather than sitting on their own line. Both broke the first pass and put
# Madhya Pradesh districts into the Kerala block.
_STATE_WORDS = [
    "ANDAMAN", "ANDHRA PRADESH", "ARUNACHAL PRADESH", "ASSAM", "BIHAR",
    "CHANDIGARH", "DELHI", "GOA", "GUJARAT", "HARYANA", "HIMACHAL PRADESH",
    "JAMMU AND KASHMIR", "JAMMU", "JHARKHAND", "KARNATAKA", "KERALA",
    "LAKSHADWEEP", "MADHYA PRADESH", "MADRAS", "MAHARASHTRA", "MANIPUR",
    "MEGHALAYA", "MIZORAM", "MYSORE", "NAGALAND", "ORISSA", "PONDICHERRY",
    "PUNJAB", "RAJASTHAN", "SIKKIM", "TAMIL NADU", "TAMILNADU", "TRIPURA",
    "UTTAR PRADESH", "UTTARAKHAND", "WEST BENGAL",
]
ANY_STATE = "|".join(w.replace(" ", r"\s+") for w in _STATE_WORDS)
STATE_HEAD = r"(?:(?<=\n)|(?<=[.\u2014]\s))\s*(" + ANY_STATE + r")\s*(?=\n|\s+\d{1,3}\.)"

# Chapter headings, so a conservation notice is not mistaken for fieldwork.
CHAPTER = re.compile(r"\n\s*(EXPLORATIONS? AND EXCAVATIONS?|EXCAVATIONS?|"
                     r"EPIGRAPHY|PRESERVATION OF MONUMENTS|ARCHAEOLOGICAL CHEMISTRY|"
                     r"MUSEUMS|PUBLICATIONS|ARCHITECTURAL SURVEY|OTHER IMPORTANT DISCOVERIES|"
                     r"RADIOCARBON DATES|ARCHAEOZOOLOGICAL|PALAEOBOTANICAL)\s*\n", re.I)

# Pre-2000 volumes end an entry title with a full stop or em-dash; the
# born-digital ASI volumes use a colon and break titles across lines in a
# two-column layout. Whitespace is collapsed before this runs so both parse.
ENTRY = re.compile(r"(?:(?<=\s)|^)(\d{1,4})\.\s+([A-Z][A-Z0-9 ,.'\u2019\-/()&]{6,170}?)\s*"
                   r"(?:[.\u2014\-]{1,3}|:)\s*(?=[A-Z0-9(])")

PERIODS = [
    ("palaeolithic",  r"palaeolithic|paleolithic|stone age|acheulian|chopper|handaxe|cleaver"),
    ("mesolithic",    r"mesolithic|microlith"),
    ("neolithic",     r"\bneolithic\b|polished axe|celt\b"),
    ("megalithic/IA", r"megalith|iron age|black[- ]and[- ]red|\bBRW\b|cist|dolmen|"
                      r"urn[- ]burial|topikal|kudaikal|umbrella stone|menhir|rock[- ]cut cave"),
    ("early historic", r"early historic|rouletted|roman|amphora|sigillata|satavahana|"
                       r"punch[- ]marked|northern black polished|\bNBP\b|russet[- ]coated|"
                       r"kshatrapa|indo[- ]greek|kushan|sunga|maurya"),
    ("early medieval", r"chera|chola|pandya|rashtrakuta|pallava|gupta|"
                       r"ninth|tenth|eleventh|early medieval"),
    ("medieval",      r"medieval|vijayanagara|sultanate|mosque|\bfort\b|temple|inscription|"
                      r"sculpture|bronze image"),
    ("islamic/colonial", r"islamic|mughal|portuguese|dutch|british|colonial|epitaph"),
]

def main():
    rows = []
    for f in sorted(TXT.glob("*.txt")):
        yr = re.search(r"IAR_([\d-]+)__", f.name)
        year = yr.group(1) if yr else "?"
        t = f.read_text(errors="ignore")
        pages = [(m.start(), int(m.group(1))) for m in re.finditer(r"\[\[PAGE (\d+)\]\]", t)]
        chapters = [(m.start(), m.group(1).upper()) for m in CHAPTER.finditer(t)]

        def chapter_at(pos):
            c = "?"
            for s, name in chapters:
                if s <= pos: c = name
                else: break
            return c

        def page_at(pos):
            p = 0
            for s, n in pages:
                if s <= pos: p = n
                else: break
            return p

        for sm in re.finditer(STATE_HEAD, t):
            state = re.sub(r"\s+", " ", sm.group(1)).upper()
            if state not in STATES:
                continue
            nxt = re.search(STATE_HEAD, t[sm.end():])
            block = t[sm.end(): sm.end() + (nxt.start() if nxt else 9000)]
            if len(block) < 120:
                continue
            block = re.sub(r"\[\[PAGE \d+\]\]", " ", block)
            block = re.sub(r"\s+", " ", block)
            chap = chapter_at(sm.start())
            ents = list(ENTRY.finditer(block))
            for i, m in enumerate(ents):
                body = block[m.end(): ents[i + 1].start() if i + 1 < len(ents) else len(block)]
                body = re.sub(r"\s+", " ", body).strip()
                if len(body) < 60:
                    continue
                title = re.sub(r"\s+", " ", m.group(2)).strip()
                dm = re.search(r"DISTRICTS?\s+([A-Z][A-Za-z ,'\-]+)", title)
                hay = (title + " " + body)
                per = [name for name, pat in PERIODS if re.search(pat, hay, re.I)]
                rows.append({
                    "year": year, "state": state, "chapter": chap[:34],
                    "entry_no": m.group(1), "title": title[:150],
                    "district": (dm.group(1).strip() if dm else "")[:60],
                    "periods": "|".join(per),
                    "early_historic": "Y" if "early historic" in per else "",
                    "page": page_at(sm.start()),
                    "body": body[:900], "volume": f.stem,
                })
    dest = OUT / "iar_entries.csv"
    with open(dest, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"{len(rows)} entries -> {dest.name}\n")
    for k, v in Counter(r["state"] for r in rows).most_common():
        eh = sum(1 for r in rows if r["state"] == k and r["early_historic"])
        print(f"  {k:16s}{v:>6} entries{eh:>6} early historic")
    print(f"\n  volumes covered: {len({r['year'] for r in rows})}")
    print("\n  by chapter:")
    for k, v in Counter(r["chapter"] for r in rows).most_common(6):
        print(f"    {k[:40]:42s}{v}")

if __name__ == "__main__":
    main()
