"""Surface the quantitative sentences in an excavation report so they can be read.

This proposes; it does not decide. Every row it prints still has to be read
against its page before it goes into material_finds.csv. The masking below is
the same defence used in mine_material.py: ware names contain digits, PDF
extraction inlines footnote markers, and page ranges in footnotes look like
counts.
"""
import re, sys, pathlib

CACHE = pathlib.Path(__file__).resolve().parents[2] / "library/text-cache"

NOISE = re.compile(
    r"Dressel\s*\d+\s*(?:[-–/]\s*\d+)?\s*[a-c]?"
    r"|Wheeler\s+[Tt]ype[s]?\s*\d+"
    r"|\b(?:Type|Form|Fig|Figs|Pl|Plate|Table|Phase|Period|Trench|Unit|Locus|SU|Context)\s*\.?\s*\d+[A-Za-z]?\b"
    r"|\d+\s*(?:BC|BCE|AD|CE|b\.?c\.?(?:e\.?)?|c\.?e\.?)\b"
    r"|\b(?:pp?\.|nos?\.|no\.)\s*\d+(?:\s*[-–]\s*\d+)?"
    r"|\b1[89]\d\d\b|\b20[0-2]\d\b"                     # publication years
    r"|(?<=[a-z\)”])[.,]\s?\d{1,3}(?=\s+[A-Z])",   # footnote markers
    re.I)

FINDS = re.compile(
    r"amphora|amphorae|sherd|sigillata|rouletted|torpedo|turquoise|glazed"
    r"|\bglass\b|\bbead|\bcoin|lamp|pottery|ceramic|\bware\b|wares\b|vessel"
    r"|fragment|Red Polished|RPW|\bTGP\b|terra sigillata|cooking pot|jar\b"
    r"|pepper|teak|ivory|\bshell|cowrie|textile|papyr|ostrac|inscription"
    r"|Aqaba|Eastern Desert|Indian|Nabataean|imported|import\b|local\b", re.I)

EFFORT = re.compile(
    r"virgin soil|bedrock|natural soil|sterile|water table|excavated area"
    r"|square met|sq\.? m|m²|hectare|\bha\b|sieve|sieving|screen(?:ed|ing)"
    r"|trench(?:es)?\b|season(?:s)?\b|campaign|depth of|deep(?:er)?\b|stratigraph", re.I)

# Any number of two digits or more, or any number carrying a thousands comma.
# Single digits produce far too much noise to be worth surfacing.
QTY = re.compile(r"(?<![\w.,])(\d{1,3}(?:,\d{3})+|\d{2,}(?:\.\d+)?)(?![\w.,]*\d)")
NEAR = 90          # characters between a quantity and a find term


def mask(s):
    return NOISE.sub(lambda m: " " * len(m.group(0)), s)


def pages(txt):
    """The cache carries page markers; yield (page, text)."""
    parts = re.split(r"\n?\[{1,2}\s*(?:PAGE|Page|page)\s*(\d+)\s*\]{1,2}\n?", txt)
    if len(parts) < 3:
        yield 0, txt
        return
    for i in range(1, len(parts) - 1, 2):
        yield int(parts[i]), parts[i + 1]


def main(stem, mode="finds", grep=None):
    path = next(CACHE.glob(f"*{stem}*.txt"))
    txt = path.read_text(errors="ignore")
    print(f"# {path.name}  ({len(txt):,} chars)\n")
    pat = FINDS if mode == "finds" else EFFORT
    n = 0
    for pg, body in pages(txt):
        for sent in re.split(r"(?<=[.;:!?])\s+", body.replace("\n", " ")):
            sent = re.sub(r"\s+", " ", sent).strip()
            if not (18 < len(sent) < 460):
                continue
            m = mask(sent)
            if grep:
                if not re.search(grep, sent, re.I):
                    continue
            else:
                hits = [(q.start(), q.end()) for q in QTY.finditer(m)]
                terms = [(t.start(), t.end()) for t in pat.finditer(m)]
                if not hits or not terms:
                    continue
                if not any(abs(a - d) < NEAR or abs(c - b) < NEAR
                           for a, b in hits for c, d in terms):
                    continue
            n += 1
            print(f"p.{pg}\t{sent}")
    print(f"\n# {n} candidate sentences", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "finds",
         sys.argv[3] if len(sys.argv) > 3 else None)
