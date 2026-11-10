"""Parse Ptolemy's Indian coordinates out of McCrindle (1885).

No free machine-readable edition of the Geography exists; the authoritative one
(Stueckelberger & Grasshoff 2006, 6,331 places) ships on a CD with the book. So the
coordinates are parsed from archive.org's OCR of McCrindle's India volume, which
prints Ptolemy's tables in full.

Minutes must be followed by an apostrophe. Without that condition the parser eats
the leading digit of the latitude -- "116 deg 14 deg 30'" comes out as lat 4 deg 30'.
"""
import re
import unicodedata
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT.parent / "library/text-cache/McCrindle-1885-Ancient-India-as-Described-by-Ptolemy.txt"

DEG = r"[°o*^‘“]"
MIN = r"['’′´]"
PAT = re.compile(
    r"([A-Z][A-Za-zéâ ,.'\-]{2,32}?)\s*"
    r"(\d{2,3})\s*" + DEG + r"\s*(?:(\d{1,2})\s*" + MIN + r"\s*)?"
    r"(\d{1,2})\s*" + DEG + r"\s*(?:(\d{1,2})\s*" + MIN + r")?")


def ascii_key(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z]", "", s.lower())


def parse():
    text = re.sub(r"[ \t]+", " ", SRC.read_text(errors="ignore"))
    out, seen = [], set()
    for name, lod, lom, lad, lam in PAT.findall(text):
        clean = name.strip(" ,.").split(",")[0].strip()
        k = ascii_key(clean)
        if len(k) < 4 or k in seen:
            continue
        seen.add(k)
        out.append({"ptolemy_name": clean, "key": k,
                    "p_lon": int(lod) + (int(lom)/60 if lom else 0),
                    "p_lat": int(lad) + (int(lam)/60 if lam else 0)})
    return pd.DataFrame(out)


# Ptolemy name -> (modern place, lat, lon, how secure the identification is)
CONTROL = {
    "barygaza":  ("Bharuch",        21.705,  72.993, "excavated / name continuity"),
    "soupara":   ("Sopara",         19.434,  72.805, "excavated"),
    "simylla":   ("Chaul",          18.571,  72.925, "excavated; Kanheri inscr. Chemulaka"),
    "podouke":   ("Arikamedu",      11.936,  79.823, "excavated"),
    "kolkhoi":   ("Korkai",          8.627,  78.062, "identified"),
    "mouziris":  ("Kodungallur",    10.217,  76.200, "Tamil poem; contested vs Pattanam"),
    "ozene":     ("Ujjain",         23.179,  75.785, "excavated / name continuity"),
    "modoura":   ("Madurai",         9.925,  78.119, "name continuity"),
    "baithana":  ("Paithan",        19.475,  75.386, "name continuity"),
    "tagara":    ("Ter",            18.321,  76.133, "identified"),
    "mandagara": ("Bankot",         17.970,  73.050, "Casson App.5 — weaker"),
}
TARGETS = {"tyndis": "Tyndis", "bakarei": "Bakare", "melkynda": "Nelkynda"}


def main():
    df = parse()
    df.to_csv(ROOT / "data/processed/ptolemy_india_coordinates.csv", index=False)
    print(f"parsed {len(df)} Ptolemy entries from McCrindle")
    ctrl = df[df.key.isin(CONTROL)].copy()
    for c in ("modern", "m_lat", "m_lon", "basis"):
        ctrl[c] = [CONTROL[k]["modern m_lat m_lon basis".split().index(c)] for k in ctrl.key]
    ctrl.to_csv(ROOT / "data/processed/ptolemy_control_points.csv", index=False)
    print(f"\ncontrol points matched: {len(ctrl)} / {len(CONTROL)}")
    print(ctrl[["ptolemy_name", "p_lon", "p_lat", "modern", "m_lat", "m_lon"]]
          .to_string(index=False))
    miss = set(CONTROL) - set(ctrl.key)
    if miss:
        print("\nnot found in the OCR:", ", ".join(sorted(miss)))
    print("\ntargets:")
    print(df[df.key.isin(TARGETS)][["ptolemy_name", "p_lon", "p_lat"]].to_string(index=False))


if __name__ == "__main__":
    main()
