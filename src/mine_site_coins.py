"""Mine the library for excavation coin assemblages, site by site.

CHRE holds hoards. This looks for the other kind of evidence -- coins recovered
from occupation layers -- which is what actually indicates a place where money
changed hands. Numbers are only taken from the same sentence as the site name,
and each one keeps its verbatim quote so the attribution can be checked.
"""
import csv, re, pathlib

LIB = pathlib.Path("/Users/vivek/Library/Mobile Documents/com~apple~CloudDocs/"
                   "A School/Harvard/Thesis/library/text-cache")
DATA = pathlib.Path(__file__).resolve().parents[1] / "data"

SITES = {r["site_key"]: r for r in csv.DictReader(open(DATA / "raw" / "site_aliases.csv"))}

COIN = (r"coins?|coinage|aurei|aureus|denarii|denarius|solidi|solidus|"
        r"tetradrachm|drachm|sestertii|folles|numismatic|coin[- ]blanks?|"
        r"countermark|mint")
UNIT = r"coins?|specimens?|examples?|pieces?|blanks?|issues?|finds?"
MIN = r"over|more\s+than|at\s+least|upwards\s+of|some|about|approximately|c\.|ca\.|nearly|around"
GAP = r"(?:\s+[A-Za-z][\w'-]*){0,3}\s*"

# Numbers that are dates, references or measurements, not quantities of coins.
NOISE = re.compile(
    r"\d+\s*(?:BC|BCE|AD|CE|b\.?c\.?(?:e\.?)?|c\.?e\.?)\b"
    r"|\b(?:BC|BCE|AD|CE)\s*\d+|\b[12]\d{3}\b"
    r"|\b(?:1st|2nd|3rd|\d+th)\s+(?:century|centuries)"
    r"|\bfigs?\.?\s*\d+|\btables?\s*\d+|\bpls?\.?\s*\d+|\bnos?\.?\s*[\d,\s-]+"
    r"|\bpp?\.\s*[\d,\s-]+|\d+(?:\.\d+)?\s*(?:mm|cm|km|m\b|g\b)"
    r"|(?<=[a-z\)])[.,]\s?\d{1,3}(?=\s+[A-Za-z])", re.I)

NEG = re.compile(r"\bno\b|\bnot\b|\bnone\b|absent|without|have not|has not|"
                 r"never|failed to|yet to be", re.I)

def mask(s):
    return NOISE.sub(lambda m: " " * len(m.group(0)), s)

def counts(sent):
    t = mask(sent)
    out = []
    for m in re.finditer(rf"({MIN})\s+(\d[\d,]*){GAP}({UNIT})", t, re.I):
        out.append((int(m.group(2).replace(",", "")), m.group(3).lower(), "approximate"))
    for m in re.finditer(rf"\b(\d[\d,]{{0,6}}){GAP}({UNIT})\b", t, re.I):
        n = m.group(1).replace(",", "")
        if n.isdigit() and 0 < int(n) < 200000:
            out.append((int(n), m.group(2).lower(), "exact"))
    for m in re.finditer(r"(\d+(?:\.\d+)?)\s*(?:%|per\s?cent)", t, re.I):
        v = float(m.group(1))
        if v <= 100:
            out.append((v, "percent", "exact"))
    seen, uniq = set(), []
    for v, u, q in out:
        if (v, u) in seen: continue
        seen.add((v, u)); uniq.append((v, u, q))
    return uniq

def sentences(t):
    t = re.sub(r"-\n", "", t)
    t = re.sub(r"\s*\n\s*", " ", t)
    return [s.strip() for s in re.split(r"(?<=[.!?;])\s+(?=[A-Z(])", t) if 30 < len(s) < 700]

def main():
    pats = []
    for r in SITES.values():
        for a in r["aliases"].split("|"):
            a = a.strip()
            if a: pats.append((len(a), a, r))
    pats.sort(key=lambda t: -t[0])
    coin_re = re.compile(COIN, re.I)

    rows, seen = [], set()
    for f in sorted(LIB.glob("*.txt")):
        text = f.read_text(errors="ignore")
        for page, chunk in [(int(m.group(1)), s) for m, s in
                            zip(re.finditer(r"\[\[PAGE (\d+)\]\]", text),
                                re.split(r"\[\[PAGE \d+\]\]", text)[1:])] or [(0, text)]:
            for s in sentences(chunk):
                if not coin_re.search(s):
                    continue
                hit, spans = None, []
                for _, alias, row in pats:
                    m = re.search(rf"\b{re.escape(alias)}\b", s)
                    if m:
                        hit = row; break
                if not hit:
                    continue
                cs = counts(s)
                key = (hit["site_key"], f.stem, page, s[:70])
                if key in seen: continue
                seen.add(key)
                for v, u, q in (cs or [("", "", "")]):
                    rows.append({
                        "site_key": hit["site_key"], "site_display": hit["display_name"],
                        "role": hit["role"], "region": hit["region"],
                        "count": v, "count_unit": u, "count_qualifier": q,
                        "negated": "Y" if NEG.search(s) else "",
                        "quote": s[:520], "source": f.stem, "page": page,
                        "verified": "",
                    })
    dest = DATA / "processed" / "site_coin_candidates.csv"
    with open(dest, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    from collections import Counter
    withn = [r for r in rows if r["count"] != ""]
    print(f"{len(rows)} coin passages -> {dest.name}   ({len(withn)} carry a figure)")
    print(f"{len({r['site_key'] for r in rows})} sites mentioned\n")
    c = Counter(r["site_display"] for r in withn)
    for k, v in c.most_common(18):
        print(f"   {k[:34]:34s}{v}")

if __name__ == "__main__":
    main()
