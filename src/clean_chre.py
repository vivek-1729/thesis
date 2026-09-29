"""Restrict the CHRE export to the region this project is about.

The bulk export was pulled with a query that also returned material from
Britain and the Adriatic. Those hoards are real but irrelevant here, and left
in they inflate every headline figure. This writes a cleaned pair of tables and
records what was removed and why.

Also drops the Kottayam 1847 hoard, whose published coordinates put it in
central Kerala on top of a Nelkynda candidate although its own county field
says Kannur and its summary says "on the slope of a hill by the sea". The
error is about 260 km.
"""
import csv, math, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/chre"
OUT = ROOT / "data/processed"

# The Erythraean world as the Periplus describes it, plus its hinterlands.
OUT_OF_REGION = {"Scotland; United Kingdom", "Montenegro",
                 "United Kingdom; England; United Arab Emirates"}
BBOX = (20.0, 95.0, -15.0, 45.0)     # lon0, lon1, lat0, lat1
KOTTAYAM_ERROR = "KOTTAYAM 1847"   # 74 aurei; county says Kannur, coordinates say central Kerala


def main():
    H = list(csv.DictReader(open(RAW / "chre_hoards.csv")))
    C = list(csv.DictReader(open(RAW / "chre_coins.csv")))

    country = {}
    for c in C:
        if c["hoard"]:
            country.setdefault(c["hoard"], c["country"] or "")

    kept, dropped = [], collections.Counter()
    for h in H:
        ctry = country.get(h["id"], "")
        h["country"] = ctry
        if ctry in OUT_OF_REGION:
            dropped["outside the study region"] += 1
            continue
        if not h["latitude"].strip():
            dropped["no coordinates"] += 1
            continue
        lat, lon = float(h["latitude"]), float(h["longitude"])
        if not (BBOX[0] <= lon <= BBOX[1] and BBOX[2] <= lat <= BBOX[3]):
            dropped["coordinates outside the bounding box"] += 1
            continue
        if (h["hoardName"] or "").strip().upper() == KOTTAYAM_ERROR:
            dropped["known georeferencing error (Kottayam 1847)"] += 1
            continue
        kept.append(h)

    keep_ids = {h["id"] for h in kept}
    coins = [c for c in C if c["hoard"] in keep_ids]

    cols_h = list(H[0].keys())
    if "country" not in cols_h:
        cols_h.append("country")
    with (OUT / "chre_hoards_clean.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols_h, extrasaction="ignore")
        w.writeheader(); w.writerows(kept)
    with (OUT / "chre_coins_clean.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(C[0].keys()), extrasaction="ignore")
        w.writeheader(); w.writerows(coins)

    print(f"hoards {len(H)} -> {len(kept)};  coins {len(C):,} -> {len(coins):,}")
    for k, v in dropped.most_common():
        print(f"  dropped, {k}: {v}")
    print("\nby country:")
    for k, v in collections.Counter(h["country"] or "(unstated)" for h in kept).most_common(12):
        print(f"  {k[:34]:36s} {v}")


if __name__ == "__main__":
    main()
