"""What data exists for each port, and what is still missing.

Answers the question "what do we actually have?" before any modelling starts, so
the gaps drive the collection plan rather than being discovered halfway through.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mapkit as mk

PACK = mk.ROOT / "Replication Pack"


def main():
    g = mk.load_sites()
    ports = g[g.route_role == "port of call"].copy()

    # Copeland's sailing times are keyed by pcode; count how many partners each
    # port has a computed time for.
    pairs = pd.concat([
        pd.read_stata(PACK / f)[["pcode1", "pcode2", "p_sea_time_hr"]]
        for f in ("gravity_trade_data.dta", "gravity_trade_data_zeros.dta")]).dropna()
    n_times = (pd.concat([pairs.pcode1, pairs.pcode2]).value_counts())
    cand = pd.read_csv(mk.RAW / "disputed_candidates.csv").port.value_counts()

    ports["has_coords"] = ports.lat.notna()
    ports["has_pleiades"] = ports.pleiades.notna()
    ports["has_trade_basket"] = ports.goods.notna() & (ports.goods > 0)
    ports["n_sailing_times"] = ports.pcode.map(n_times).fillna(0).astype(int)
    ports["has_sailing_time"] = ports.n_sailing_times > 0
    ports["n_candidates"] = ports.toponym.map(cand).fillna(0).astype(int)
    ports["excavation_note"] = ports.tier_letter == "A"

    layers = ["has_coords", "has_pleiades", "has_trade_basket", "has_sailing_time",
              "excavation_note"]
    out = ports[["site_id", "toponym", "route", "chapter", "tier", "km_to_coast",
                 "n_sailing_times", "n_candidates"] + layers]
    out.to_csv(mk.PROC / "data_coverage.csv", index=False)

    print(f"=== coverage across {len(ports)} ports of call ===")
    for col in layers:
        n = int(ports[col].sum())
        print(f"  {col:20s} {n:3d} / {len(ports)}   ({n/len(ports)*100:4.0f}%)")
    print("\n=== by route ===")
    print(ports.groupby("route")[layers].sum().to_string())
    print("\n=== ports with NO sailing time (invisible to the existing model) ===")
    miss = ports[~ports.has_sailing_time].sort_values(["route", "chapter_num"])
    print(f"  {len(miss)} ports")
    for r, d in miss.groupby("route"):
        print(f"  {r}: " + ", ".join(d.toponym))
    print("\n=== ports with no trade basket recorded ===")
    nb = ports[~ports.has_trade_basket]
    print(f"  {len(nb)}: " + ", ".join(sorted(nb.toponym)))
    return out


if __name__ == "__main__":
    main()
