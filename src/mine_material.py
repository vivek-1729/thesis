"""Mine the library for statements of the form 'ware X at site Y'.

The output is a candidate list, not a dataset. Every row carries the verbatim
sentence and its page so the attribution can be checked; nothing here is
evidence until it has been read. Counts are lifted only where the source
states one -- an absent count is recorded as absent, never inferred.
"""
import csv, re, pathlib, sys
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]
CACHE = ROOT / "library" / "text-cache"
DATA = pathlib.Path(__file__).resolve().parents[1] / "data"

# --- ware search patterns -------------------------------------------------
# Keyed to ware_id in ware_typology.csv. Deliberately generous: false
# positives are cheap to discard on review, misses are invisible.
WARE_PATTERNS = {
    "dressel_2_4":      r"Dressel\s*2[-–/]\s*4|Dr\.?\s*2[-–/]\s*4",
    "koan":             r"\bKoan\b",
    "rhodian":          r"\bRhodian\b",
    "brindisian":       r"\bBrindisian\b",
    "dressel_6a":       r"Dressel\s*6\s*A",
    "dressel_7_11":     r"Dressel\s*7[-–]\s*11",
    "dressel_20":       r"Dressel\s*20",
    "gauloise_4":       r"Gauloise\s*4",
    "ae3":              r"Amphore\s+Egyptienne|\bAE\s?3\b",
    "lr1":              r"Late\s+Roman\s+(?:Amphora\s+)?1\b|\bLR\s?1\b",
    "lr2":              r"Late\s+Roman\s+(?:Amphora\s+)?2\b|\bLR\s?2\b",
    "lr3":              r"Late\s+Roman\s+(?:Amphora\s+)?3\b|\bLR\s?3\b",
    "aila":             r"Aila\s+amphora|Aqaba\s+amphora",
    "its":              r"Italian\s+[Ss]igillata|\bITS\b|Arretine",
    "sigillata_unspec": r"[Tt]erra\s+[Ss]igillata|\bsigillata\b",
    "esa":              r"Eastern\s+Sigillata\s*A|\bESA\b",
    "esb":              r"Eastern\s+Sigillata\s*B|\bESB\b",
    "egyptian_coarse":  r"Egyptian\s+(?:coarse|table)\s+ware",
    "rouletted_ware":   r"Rouletted\s+[Ww]are|\bRouletted\b|Wheeler\s+[Tt]ype\s+1\b|\bRW\b",
    "rpw":              r"Red\s+Polished\s+Ware|\bRPW\b",
    "crsw":             r"Coarse\s+Red[-\s]?slipped|\bCRSW\b|Wheeler\s+[Tt]ype\s+2[458]|\bhandi\b",
    "crsw_scooped":     r"bamboo|scooping|organic\s+(?:wiping|impression)",
    "organic_black_ware": r"Organic\s+Black\s+Ware|\bOBW\b",
    "paddle_impressed": r"Paddle\s+Impressed",
    "wheeler_74_75":    r"Wheeler\s+[Tt]ype\s+74|conical\s+(?:jar|amphora)",
    "nbp":              r"Northern\s+Black\s+Polished|\bNBP\b",
    "osj":              r"Organic\s+Storage\s+Jar",
    "wmcp":             r"[Ww]hole[-\s]mouth\s+[Cc]ooking",
    "torpedo_jar":      r"[Tt]orpedo",
    "mes_glazed":       r"Mesopotamian\s+Glazed|turquoise[-\s]glazed|alkaline[-\s]glazed",
    "aksumite_coarse":  r"Aksumite\s+(?:Coarse\s+)?[Ww]are|Axumite\s+[Ww]are",
    "red_sandy_ware":   r"(?:Red\s+)?Sandy\s+Red\s+Ware|Red\s+Sandy\s+Ware",
    "roman_amphora_unspec": r"Roman\s+amphora|Roman\s+amphorae|Mediterranean\s+amphora",
    "roman_pottery_unspec": r"Roman\s+(?:pottery|ceramic|ware|sherd)",
    "roman_coin":       r"Roman\s+coin|aure(?:us|i)\b|denari(?:us|i)\b|coin\s+hoard",
    "roman_glass":      r"Roman\s+glass|glass\s+vessel|glass\s+fragment",
    "bead":             r"\bbeads?\b",
    "intaglio":         r"intaglio|\bgemstone\b|engraved\s+gem",
    "lamp":             r"Roman\s+lamp|\blamps?\b",
    "black_pepper":     r"black\s+pepper|Piper\s+nigrum|peppercorn",
    "frankincense":     r"frankincense|Boswellia",
    "teak":             r"\bteak\b|Indian\s+timber|ship\s+timber",
}

# --- count extraction -----------------------------------------------------
UNIT = (r"sherds?|shreds?|fragments?|vessels?|examples?|specimens?|pieces?|"
        r"rims?|coins?|beads?|amphorae|amphoras?|jars?|EVEs?|MNI|finds?|"
        r"hoards?|objects?|artefacts?|artifacts?|bowls?|dishes|lamps?")
WORDNUM = {"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,
           "eight":8,"nine":9,"ten":10,"eleven":11,"twelve":12,"fifteen":15,
           "twenty":20,"thirty":30,"forty":40,"fifty":50,"hundred":100}
MINIMUM = r"over|more\s+than|at\s+least|upwards\s+of|in\s+excess\s+of|no\s+fewer\s+than"
# The unit rarely sits flush against the figure; allow a short descriptive run
# but no punctuation, which would mean a new clause and probably a new subject.
GAP = r"(?:\s+[A-Za-z][\w'-]*){0,3}\s*"
APPROX  = r"c\.|ca\.|about|approximately|around|nearly|some|roughly|almost"

# Spans whose digits are never quantities of artefacts. Masked out before any
# count is read, preserving offsets so ware/count proximity stays meaningful.
NOISE = re.compile(
    # ware and reference designations
    r"Dressel\s*\d+\s*(?:[-–/]\s*\d+)?\s*[a-c]?"
    r"|Wheeler\s+[Tt]ype[s]?\s*\d+\s*(?:[-–/]\s*\d+)?"
    r"|\bLR\s?\d\b|Late\s+Roman\s+(?:Amphora\s+)?\d"
    r"|\bAE\s?\d(?:[-–.]\d+)*|Gauloise\s*\d|Keay\s*\d+"
    r"|\bfig(?:ure)?s?\.?\s*\d+[\d,\s–-]*|\btables?\s*\d+"
    r"|\bpl(?:ate)?s?\.?\s*\d+|\bnos?\.?\s*[\d,\s–-]+"
    r"|\bpp?\.\s*[\d,\s–-]+|\bsec(?:tion)?s?\.?\s*\d+|\bPME\s*\d+"
    r"|\bch(?:ap(?:ter)?)?\.?\s*\d+|\bvol\.?\s*\d+|\bn\.\s*\d+"
    # dates, in either order, and centuries
    r"|\d+\s*(?:BC|BCE|AD|CE|b\.?c\.?(?:e\.?)?|c\.?e\.?)\b"
    r"|\b(?:BC|BCE|AD|CE)\s*\d+|\b[12]\d{3}\b"
    r"|\b(?:1st|2nd|3rd|\d+th)\s+(?:century|centuries|millennium)"
    r"|\b\d+\s*(?:st|nd|rd|th)\s+(?:century|centuries)"
    # footnote markers: PDF extraction inlines superscripts, so
    # "Sri Lanka.180 There were" looks like a count of 180 somethings
    r"|(?<=[a-z\)”])[.,]\s?\d{1,3}(?=\s+[A-Za-z])"
    # running headers and facing page numbers: "218 EGYPT", "74 75 Stone"
    r"|^\s*\d{1,4}\s+(?=[A-Z]{3,})|^\s*\d{1,4}\s+\d{1,4}(?=\s)"
    # section numbering: "3.5 Text and Symbol"
    r"|\b\d+\.\d+(?=\s+[A-Z])"
    # measurements and durations
    r"|\d+(?:\.\d+)?\s*(?:mm|cm|km|ha|kg|m2|m²|m\b|g\b)"
    r"|\d+\s*(?:days?|months?|years?|weeks?|hours?|seasons?|stadia)"
    , re.I)

def mask(s):
    """Blank noise spans, keeping length so offsets remain valid."""
    return NOISE.sub(lambda m: " " * len(m.group(0)), s)

# An index, bibliography or finds-table line reads like prose to a regex but
# is a list of page or tally numbers. These produced the worst false counts.
def is_reference_line(s):
    if len(re.findall(r",\s*\d", s)) >= 4:
        return True
    if len(re.findall(r"\b\d+\b", s)) >= 8:      # finds-table dump
        return True
    digits = sum(c.isdigit() for c in s)
    alpha = sum(c.isalpha() for c in s) or 1
    return digits / alpha > 0.15 and s.count(",") >= 3

def find_counts(sent):
    """Every explicit quantity in the sentence, with its offset.

    A unit is mandatory. An unqualified bare number in this literature is
    almost always a date, a page or a footnote marker, so requiring a unit is
    what separates a count of sherds from a year.
    """
    t = mask(sent)
    out = []
    for m in re.finditer(rf"({MINIMUM})\s+(\d[\d,]*){GAP}({UNIT})", t, re.I):
        out.append((int(m.group(2).replace(",", "")), m.group(3).lower(), "minimum", m.start()))
    for m in re.finditer(rf"({APPROX})\s+(\d[\d,]*){GAP}({UNIT})", t, re.I):
        out.append((int(m.group(2).replace(",", "")), m.group(3).lower(), "approximate", m.start()))
    for m in re.finditer(r"(\d+(?:\.\d+)?)\s*(?:%|per\s?cent)", t, re.I):
        v = float(m.group(1))
        if v <= 100:
            out.append((v, "percent", "exact", m.start()))
    for m in re.finditer(rf"\b(\d[\d,]{{0,6}}){GAP}({UNIT})\b", t, re.I):
        n = m.group(1).replace(",", "")
        if n.isdigit() and 0 < int(n) < 500000:
            out.append((int(n), m.group(2).lower(), "exact", m.start()))
    for m in re.finditer(rf"\b({'|'.join(WORDNUM)}){GAP}({UNIT})\b", t, re.I):
        out.append((WORDNUM[m.group(1).lower()], m.group(2).lower(), "exact", m.start()))
    seen, uniq = set(), []
    for v, u, q, pos in sorted(out, key=lambda x: x[3]):
        if (v, u) in seen:
            continue
        seen.add((v, u)); uniq.append((v, u, q, pos))
    return uniq

NEGATION = re.compile(r"\b(no|not|none|absent|lack(?:s|ing)?|without|never|"
                      r"failed to|yet to be|has not|have not)\b", re.I)

def load_sites():
    rows = list(csv.DictReader(open(DATA / "raw" / "site_aliases.csv")))
    pats = []
    for r in rows:
        for a in r["aliases"].split("|"):
            a = a.strip()
            if a:
                pats.append((len(a), a, r))
    pats.sort(key=lambda t: -t[0])          # longest alias wins
    return rows, pats

def split_pages(text):
    parts = re.split(r"\[\[PAGE (\d+)\]\]", text)
    out = []
    for i in range(1, len(parts) - 1, 2):
        out.append((int(parts[i]), parts[i + 1]))
    return out or [(0, text)]

def sentences(chunk):
    # PDF text breaks lines mid-sentence; rejoin before splitting.
    t = re.sub(r"-\n", "", chunk)
    t = re.sub(r"\s*\n\s*", " ", t)
    t = re.sub(r"\s{2,}", " ", t)
    return [s.strip() for s in re.split(r"(?<=[.!?;])\s+(?=[A-Z(])", t) if len(s.strip()) > 25]

def main():
    site_rows, site_pats = load_sites()
    wares = {w["ware_id"]: w for w in csv.DictReader(open(DATA / "raw" / "ware_typology.csv"))}
    ware_re = {k: re.compile(v) for k, v in WARE_PATTERNS.items()}

    out, seen = [], set()
    files = sorted(CACHE.glob("*.txt"))
    for f in files:
        text = f.read_text(errors="ignore")
        for page, chunk in split_pages(text):
            sents = sentences(chunk)
            recent = []                      # (site_row, sentence_index)
            for si, s in enumerate(sents):
                if is_reference_line(s):
                    continue
                # ---- sites in this sentence, longest alias wins ----
                hits, spans = [], []
                for _, alias, row in site_pats:
                    for m in re.finditer(rf"\b{re.escape(alias)}\b", s):
                        if any(m.start() < e and m.end() > b for b, e in spans):
                            continue
                        spans.append((m.start(), m.end()))
                        hits.append(row)
                for h in hits:
                    recent.append((h, si))
                recent = [(r, i) for r, i in recent if si - i <= 2]
                if not recent:
                    continue

                # ---- wares in this sentence, with positions ----
                ware_pos = {}
                for wid, rx in ware_re.items():
                    pos = [m.start() for m in rx.finditer(s)]
                    if pos:
                        ware_pos[wid] = pos
                if not ware_pos:
                    continue

                # ---- bind each quantity to its nearest ware ----
                bound = {}
                for val, unit, qual, cpos in find_counts(s):
                    best, bestd = None, 10**9
                    for wid, positions in ware_pos.items():
                        d = min(abs(cpos - q) for q in positions)
                        if d < bestd:
                            best, bestd = wid, d
                    if best is not None and bestd <= 150 and best not in bound:
                        bound[best] = (val, unit, qual, bestd)

                for wid in ware_pos:
                    targets = {id(r): (r, si - i) for r, i in recent}
                    for _, (srow, dist) in targets.items():
                        key = (srow["site_key"], wid, f.stem, page, s[:60])
                        if key in seen:
                            continue
                        seen.add(key)
                        # A quantity is credited only when site, ware and
                        # number stand in one sentence; across a window the
                        # figure routinely belongs to a different site.
                        cnt, unit, qual, cdist = bound.get(wid, ("", "", "", ""))
                        if dist != 0:
                            cnt, unit, qual, cdist = "", "", "", ""
                        out.append({
                            "site_key": srow["site_key"],
                            "site_display": srow["display_name"],
                            "role": srow["role"],
                            "region": srow["region"],
                            "lat": srow["lat"], "lon": srow["lon"],
                            "ware_id": wid,
                            "ware_name": wares[wid]["ware_name"],
                            "category": wares[wid]["category"],
                            "count": cnt,
                            "count_unit": unit,
                            "count_qualifier": qual,
                            "count_ware_gap": cdist,
                            "negated": "Y" if NEGATION.search(s) else "",
                            "proximity": "same_sentence" if dist == 0 else f"within_{dist}",
                            "quote": s[:600],
                            "source": f.stem,
                            "page": page,
                            "verified": "",
                        })

    cols = list(out[0].keys())
    dest = DATA / "processed" / "material_candidates.csv"
    with open(dest, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader(); w.writerows(out)
    print(f"{len(out)} candidate rows -> {dest.relative_to(DATA.parent)}")
    print(f"  files scanned      {len(files)}")
    print(f"  with a count       {sum(1 for r in out if r['count'] != '')}")
    print(f"  same-sentence      {sum(1 for r in out if r['proximity']=='same_sentence')}")
    print(f"  flagged negated    {sum(1 for r in out if r['negated'])}")
    print(f"  distinct sites     {len({r['site_key'] for r in out})} of {len(site_rows)}")
    print(f"  distinct wares     {len({r['ware_id'] for r in out})} of {len(wares)}")

if __name__ == "__main__":
    main()
