"""Pull every measured statement out of the Periplus.

The text states distances in spelled-out words ("five hundred stadia", "two days'
sail"), and the numbers mean different things: some are legs between ports, some
are how far an island lies off the shore, some are the width of a bay. Mixing
those would corrupt any model built on them, so the kind is recorded alongside
the value and nothing is converted to kilometres here.
"""
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW, PROC = ROOT / "data/raw", ROOT / "data/processed"

UNITS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
         "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
         "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
         "eighteen": 18, "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40,
         "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}
SCALES = {"hundred": 100, "thousand": 1000}
NUMWORD = r"(?:" + "|".join(list(UNITS) + list(SCALES) + ["and", "a", "an"]) + r")"


def words_to_number(phrase):
    """'eighteen hundred' -> 1800; 'one hundred and twenty' -> 120; 'a' -> 1."""
    total, current = 0, 0
    seen = False
    toks = re.findall(r"[a-z]+", phrase.lower())
    # "a three-days' journey" is three days, not one-plus-three: the article only
    # carries a value when it is the only number word present.
    if len(toks) > 1 and toks[0] in ("a", "an"):
        toks = toks[1:]
    for w in toks:
        if w in ("and",):
            continue
        if w in ("a", "an"):
            current, seen = 1, True
        elif w in UNITS:
            current += UNITS[w]
            seen = True
        elif w in SCALES:
            # "eighteen hundred" = 18 x 100; a bare "hundred" means one hundred.
            current = (current or 1) * SCALES[w]
            if SCALES[w] == 1000:
                total += current
                current = 0
            seen = True
    return (total + current) if seen else None


def split_chapters(text):
    text = re.sub(r"\s+", " ", text)
    parts = re.split(r"(?<=[\.\s])(\d{1,2})\.\s+(?=[A-Z“\"])", text)
    out = {}
    for i in range(1, len(parts) - 1, 2):
        num = int(parts[i])
        if 1 <= num <= 66 and num not in out:
            out[num] = parts[i + 1].strip()
    return out


PATTERNS = [
    (r"\b((?:%s[\s-]*){1,5})\bstadia\b" % NUMWORD, "stadia"),
    (r"\b((?:%s[\s-]*){1,4})\bdays?[’'`]?\s*sail\b" % NUMWORD, "days_sail"),
    (r"\b((?:%s[\s-]*){1,4})\bdays?[’'`]?\s*(?:journey|course|run)\b" % NUMWORD,
     "days_journey"),
    (r"\bcourses?\s+of\s+a\s+day\s+and\s+night\b", "day_and_night"),
    (r"\b((?:%s[\s-]*){1,4})\bdays\b(?!\s*[’'`]?\s*(?:sail|journey|course|run))" % NUMWORD,
     "days_bare"),
]


def extract(chapters):
    rows = []
    for ch, body in sorted(chapters.items()):
        for pat, unit in PATTERNS:
            for m in re.finditer(pat, body, flags=re.I):
                value = words_to_number(m.group(1)) if m.lastindex else None
                lo = max(0, m.start() - 170)
                rows.append({
                    "chapter": ch, "pos": m.start(), "unit": unit, "value": value,
                    "match": m.group(0).strip(),
                    "context": body[lo:min(len(body), m.end() + 120)].strip(),
                })
    # Deduplicate on POSITION, not on value: ch. 13 and ch. 54 each state the same
    # number twice for different legs ("five hundred stadia" Tyndis->Muziris and
    # again Muziris->Nelcynda), and collapsing them loses a real measurement.
    df = pd.DataFrame(rows).drop_duplicates(["chapter", "pos"])
    return df.sort_values(["chapter", "pos"]).reset_index(drop=True)


def main():
    chapters = split_chapters((RAW / "periplus_schoff.txt").read_text())
    df = extract(chapters)
    df.to_csv(PROC / "_distance_statements_raw.csv", index=False)

    # Endpoints and kind are a reading judgement, not something a regex can settle,
    # so they live in a hand-curated file keyed to chapter+position and are joined
    # back here. Nothing is converted to kilometres: the unit and the kind both
    # change what the number means.
    df["key"] = df.chapter.astype(str) + "," + df.pos.astype(str)
    cur = pd.read_csv(RAW / "distance_curation.csv")
    out = df.merge(cur, on="key", how="left")
    missing = out[out.kind.isna()]
    if len(missing):
        print("UNCURATED:", missing[["chapter", "pos", "match"]].to_dict("records"))
    out[["chapter", "pos", "kind", "from_site", "to_site", "unit", "value",
         "match", "note", "context"]].to_csv(PROC / "distances.csv", index=False)
    print(f"chapters parsed: {len(chapters)}  (1..{max(chapters)})")
    print(f"statements found: {len(df)}")
    print(df.unit.value_counts().to_string())
    print("\nby kind:")
    print(out.kind.value_counts().to_string())
    return out


if __name__ == "__main__":
    df = main()
    for r in df.itertuples():
        v = "?" if pd.isna(r.value) else int(r.value)
        print(f"\nch{r.chapter:>3} {r.unit:14s} {str(v):>6s}  | {r.match}")
        print(f"        …{r.context[:230]}…")
