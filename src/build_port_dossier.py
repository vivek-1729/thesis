"""Write out every location-bearing passage in full, grouped by port and source.

This is meant to be read, not queried. Each entry is the matched sentence with
the sentence either side of it, so the passage stands on its own, and carries
its source and page. Nothing is summarised or paraphrased.
"""
import re, pathlib
from collections import defaultdict

LIB = pathlib.Path("/Users/vivek/Library/Mobile Documents/com~apple~CloudDocs/"
                   "A School/Harvard/Thesis/library")
OUT = pathlib.Path(__file__).resolve().parents[1] / "docs"

PORTS = {
 "Leuke Kome": r"Leuk[eē]\s*K[oō]m[eē]|Leucos Limen|Aynuna|'Aynuna|Khuraybah|al-Wajh|\bWajh\b",
 "Barbarikon": r"Barbarik[oó]n|Barbaricum|Banbhore|Bhambore|Bhanbhore|Minnagar",
 "Tyndis":     r"Tyndis|Tundis|Ponnani|\bTanur\b|Kadalundi|Beypore|Chaliyam|Koyilandy|Pantalayini|Panthalayani",
 "Nelkynda":   r"Nelkynda|Nelcynda|Nelkunda|Melkynda|Niranam|Neranom|Niranom|Neendakara|Nakkada",
 "Bakare":     r"Bakar[eē]|Becare|Barkare|Bacare|Purakkad|Pirakkad|Porakad|Kallada|Thevalakara|Markari|Varakkai|Nirkunnam|Kannetri",
 "Muziris":    r"Muziris|Muciri|Mouziris|Muzirim|Pattanam|Kodungallur|Cranganore",
 "Rhapta":     r"Rhapta|\bRapta\b|Menuthias|Menouthias|Azania|Rufiji|Unguja Ukuu|Menuthesias",
}

ARGUES = re.compile(
 r"identif|equat|locat(?:e|ed|ion)|situated|placed?\b|propos|suggest|argu|"
 r"must be|cannot be|probably|perhaps|generally accepted|consensus|"
 r"no doubt|certainly|disput|contest|controvers|problem|difficult|"
 r"evidence|excavat|yielded|recovered|discover|finds?\b|sherds?|amphora|"
 r"distance|stadia|stades|days'? sail|north of|south of|upriver|up the river|"
 r"mouth of|harbour|harbor|anchor|emporium|market[- ]town", re.I)
STRONG = re.compile(
 r"identif|equat|must be|cannot be|generally accepted|consensus|"
 r"disput|contest|controvers|no doubt|has not been|remains uncertain|"
 r"stadia|stades|yielded|excavat|coordinates|latitude", re.I)
JUNK = re.compile(r"\b(?:pp?\.|vol\.|eds?\.|forthcoming|in press)\b.*\d{4}|"
                  r"^[A-Z][a-z]+,\s+[A-Z]\.\s|ISBN|Printed by|Published by|"
                  r"Price in|Graphics Point|copyright|All rights reserved", re.I)

NICE = {  # readable source labels
 "Casson-1989-Periplus-Maris-Erythraei-text-translation-commentary": "Casson 1989, *Periplus Maris Erythraei*",
 "Schoff-1912-Periplus-of-the-Erythraean-Sea": "Schoff 1912, *Periplus of the Erythraean Sea*",
 "Tomber-2008-Indo-Roman-Trade-From-Pots-to-Pepper": "Tomber 2008, *Indo-Roman Trade*",
 "Dayalan-2018-Ancient-Seaports-Western-Coast-India": "Dayalan 2018, Ancient Seaports of the Western Coast of India",
 "Ghosh-Barbarikon-in-the-Maritime-Trade-Network-of-Early-India": "Ghosh, Barbarikon in the Maritime Trade Network",
 "Felici-et-al-Banbhore-Pakistani-Italian-Excavations": "Felici et al., Banbhore: Pakistani-Italian Excavations",
 "Pakistan-Archaeology-33-2018": "Mughal 2018, *Pakistan Archaeology* 33",
 "Sidebotham-2011-Berenike-and-the-Ancient-Maritime-Spice": "Sidebotham 2011, *Berenike*",
 "Nappo-2010-JRA-23-On-the-Location-of-Leuke-Kome": "Nappo 2010, On the Location of Leuke Kome",
 "Gawlikowski-Juchniewicz-al-Zahrani-2021-Aynuna-Nabataean-Port-Red-Sea": "Gawlikowski et al. 2021, *Aynuna*",
 "Cherian-Pattanam-Evidence-of-Maritime-Exchanges": "Cherian 2012, Pattanam",
 "Shajan-Tomber-Selvakumar-Cherian-2004-JRA-Locating-the-Ancient-Port-of-Muziris": "Shajan et al. 2004, Locating Muziris",
}
def label(stem):
    if stem in NICE: return NICE[stem]
    if stem.startswith("IAR_"):
        return "*Indian Archaeology: A Review* " + stem.split("__")[0][4:]
    return stem.replace("apa-", "").replace("-", " ")

def sentences(t):
    t = re.sub(r"-\n", "", t)
    t = re.sub(r"\s*\n\s*", " ", t)
    t = re.sub(r"\s{2,}", " ", t)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z(“])", t)]

def main():
    files = sorted(LIB.glob("text-cache/*.txt")) + sorted(LIB.glob("iar-text/*.txt"))
    store = {p: defaultdict(list) for p in PORTS}
    for f in files:
        text = f.read_text(errors="ignore")
        pages = [(m.start(), int(m.group(1))) for m in re.finditer(r"\[\[PAGE (\d+)\]\]", text)]
        flat = re.sub(r"\[\[PAGE \d+\]\]", " ", text)
        sents = sentences(flat)
        pos = 0
        offs = []
        for s in sents:
            i = flat.find(s[:50], pos) if len(s) > 50 else pos
            offs.append(i if i >= 0 else pos)
            pos = max(pos, (i if i >= 0 else pos) + 1)
        for k, s in enumerate(sents):
            if not (70 < len(s) < 900): continue
            if JUNK.search(s): continue
            if not ARGUES.search(s): continue
            for port, pat in PORTS.items():
                if not re.search(pat, s): continue
                ctx = " ".join(sents[max(0, k-1): k+2]).strip()
                if len(ctx) > 1700: ctx = s
                pg = 0
                for st, n in pages:
                    if st <= offs[k]: pg = n
                    else: break
                sc = len(STRONG.findall(s)) * 2 + len(ARGUES.findall(s))
                store[port][f.stem].append((sc, ctx, pg))

    total = 0
    for port in PORTS:
        lines = [f"# {port}\n"]
        srcs = sorted(store[port].items(), key=lambda kv: -sum(1 for _ in kv[1]))
        n_port = 0
        for stem, rows in srcs:
            seen, keep = set(), []
            for sc, ctx, pg in sorted(rows, key=lambda r: -r[0]):
                key = re.sub(r"\W+", "", ctx.lower())[:90]
                if key in seen: continue
                seen.add(key); keep.append((sc, ctx, pg))
            if not keep: continue
            lines.append(f"\n## {label(stem)}\n")
            lines.append(f"*{len(keep)} passages. File: `{stem}`*\n")
            for sc, ctx, pg in keep:
                lines.append(f"\n**p. {pg}**\n")
                lines.append(f"> {ctx}\n")
            n_port += len(keep)
        lines.insert(1, f"\n*{n_port} passages from {len(srcs)} sources. "
                        f"Verbatim, with one sentence of context either side.*\n")
        dest = OUT / f"dossier-{port.lower().replace(' ', '-')}.md"
        dest.write_text("\n".join(lines))
        words = len(" ".join(lines).split())
        print(f"  {port:12s}{n_port:>5} passages  {words:>7,} words  -> {dest.name}")
        total += n_port
    print(f"\n{total} passages across seven files")

if __name__ == "__main__":
    main()
