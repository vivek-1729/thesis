"""Score how well-located each of the 92 sites actually is.

The thesis brief started from "6 known, 6 disputed". That split was inherited, not
measured. This grades every site on evidence instead, separating what can be derived
from the data automatically from what needs a scholarly judgement.

Two kinds of column, kept apart on purpose:
  * derived_*   computed from the sources; reproducible, no judgement
  * lit_*       a first pass from the identification literature, TO BE VERIFIED

The tier is a function of both. Sites left at lit_status "review" are the ones the
thesis still has to adjudicate by reading.
"""
import json, math
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROC, RAW = ROOT / "data/processed", ROOT / "data/raw"

# Identifications resting on an excavated site, or on unbroken name-and-place
# continuity. First pass -- every one of these needs checking against the
# excavation report before it is used as a calibration anchor.
EXCAVATED = {
    "Berenikē": "Berenike, Egypt -- excavated (Sidebotham)",
    "Muos Hormos": "Quseir al-Qadim -- excavated (Peacock & Blue)",
    "Adouli": "Adulis, Eritrea -- excavated",
    "Kanē": "Qana' / Bi'r Ali, Yemen -- excavated (Sedov)",
    "Moscha Limen": "Sumhuram / Khor Rori, Oman -- excavated (Avanzini)",
    "Opōnē": "Ras Hafun, Somalia -- excavated; identified 1970s survey",
    "Podoukē": "Arikamedu -- excavated (Wheeler, Begley)",
    "Axōmite metropolis": "Aksum -- excavated",
    "Meroē": "Meroe, Sudan -- excavated",
    "Zafar": "Zafar, Yemen -- excavated",
    "Ozēnē": "Ujjain -- excavated; name continuity",
    "Sēmulla": "Chaul -- excavated 2004, Roman pottery; Kanheri inscr. Chemulaka",
    "Souppara": "Sopara -- Buddhist remains (1882)",
    "Pasinou Kharax": "Charax Spasinou -- excavated",
    "Kolkhoi": "Korkai, Tamil Nadu",
    "Kalliena": "Kalyan -- named in Kanheri cave inscriptions",
    "Dioskouridou Island": "Socotra -- island, unambiguous",
    "Eudaimōn Arabia": "Aden -- place continuity",
    "Barygaza": "Bharuch -- name continuity",
    "Arsinoe": "Suez -- secure (Copeland only)",
    "Diospolis": "Thebes / Luxor -- secure (Copeland only)",
    "Gangēs": "Ganges mouth -- a region, not a point",
    "Malaō": "Berbera -- standard identification",
    "Aualitēs": "Zeila -- standard identification (sources differ on coordinate)",
    "Muziris": "Pattanam / Kodungallur -- excavated, but WHICH site is contested",
}

# Named in the brief as the targets. Kept as a flag, not as the definition of the problem.
BRIEF_DISPUTED = {"Rhapta", "Barbarikon", "Tyndis", "Nelkunda", "Bakarē", "Leukē Kōmē"}


def coast_distance(lat, lon, coast):
    """Kilometres to the nearest coastline vertex.

    Approximate: Natural Earth 50m puts vertices several km apart and does not resolve
    the Kerala backwaters at all, so lagoon sites read as further inland than they are.
    Good enough to separate 3 km from 300 km, which is the question being asked.
    """
    if pd.isna(lat):
        return np.nan
    dy = (coast[:, 1] - lat) * 110.57
    dx = (coast[:, 0] - lon) * 111.32 * math.cos(math.radians(lat))
    return float(np.sqrt(dx * dx + dy * dy).min())


def load_coast():
    t = (RAW / "ne_50m_land.js").read_text()
    j = json.loads(t[t.index("{"):])
    return np.array([(x, y) for f in j["features"] if f.get("geometry")
                     for poly in ([f["geometry"]["coordinates"]]
                                  if f["geometry"]["type"] == "Polygon"
                                  else f["geometry"]["coordinates"])
                     for ring in poly for x, y in ring
                     if 20 < x < 100 and -20 < y < 40])


def route_role(r):
    """What the ship actually does here.

    The Periplus is a coastal itinerary, but it also names places the ship never
    visits. Ch. 51 is explicit that goods reach Barygaza from Paithana and Tagara
    "by wagons and through great tracts without roads" -- those are overland supply
    centres, not stops.

    A landmark is a place with NO trade attributed to it. Testing on the name alone
    is not enough: Dioskouridou Island is Socotra, which the text gives 13 traded
    goods and 10 partners, and Puralaon Islands and Sarapis Island also trade. All
    three are ports of call that merely happen to be islands.
    """
    if r.place_type == "Inland market" or (pd.notna(r.km_to_coast) and r.km_to_coast > 25):
        return "inland supply centre"
    trades = (pd.notna(r.goods) and r.goods > 0) or r.place_type not in (None, "Unspecified")
    name = str(r.toponym)
    is_feature = any(w in name for w in ("Island", "Isle", "Cape"))
    if is_feature and not trades:
        return "landmark"
    return "port of call"


def decimals(v):
    if pd.isna(v):
        return -1
    s = f"{v:.6f}".rstrip("0").rstrip(".")
    return len(s.split(".")[1]) if "." in s else 0


def tier(r):
    """A = anchor-grade, B = confident, C = proposed, D = conflicted, E = unlocated."""
    if r.derived_no_coords:
        return "E — unlocated"
    if r.derived_placeholder_any:
        return "D — placeholder coordinate"
    if pd.notna(r.disagree_km) and r.disagree_km > 50:
        return "D — sources conflict >50 km"
    if r.lit_excavated and (pd.isna(r.disagree_km) or r.disagree_km <= 10):
        return "A — excavated / secure"
    if r.lit_excavated:
        return "B — identified, coordinate unsettled"
    if pd.notna(r.disagree_km) and r.disagree_km <= 10:
        return "B — two sources agree"
    if r.derived_coord_dp >= 3 and r.derived_has_pleiades:
        return "C — single-source identification"
    return "C — weak / unverified"


def main():
    g = pd.read_csv(PROC / "gazetteer.csv")
    coast = load_coast()
    g["km_to_coast_merged"] = [coast_distance(r.lat, r.lon, coast) for r in g.itertuples()]
    g["derived_coord_dp"] = [min(decimals(a), decimals(b)) for a, b in zip(g.lat, g.lon)]
    g["derived_no_coords"] = g.lat.isna()
    # Exact half- or whole-degree coordinates are an approximation someone typed in,
    # not an identification -- five "island" sites in the gazetteer are marked Precise
    # while sitting on round numbers.
    def is_round(la, lo):
        return la.notna() & ((la * 2) % 1 == 0) & ((lo * 2) % 1 == 0)
    # Check BOTH source coordinates, not just the merged one: a placeholder sitting in
    # the source we did not adopt still means that source never really located the site,
    # and would otherwise masquerade as a genuine scholarly conflict.
    g["derived_placeholder_coord"] = is_round(g.lat, g.lon)
    g["derived_placeholder_any"] = (is_round(g.lat, g.lon)
                                    | is_round(g.cop_lat, g.cop_lon)
                                    | is_round(g.barchi_lat, g.barchi_lon))
    # A placeholder in ONE source does not erase a real coordinate in the other.
    # Bakare, Argalou and Masalia each have a genuine Copeland position while Barchi
    # parks them on a round number; treating them as unlocated would have dropped
    # Bakare, which is one of the ports the thesis is trying to find.
    cop_real = g.cop_lat.notna() & ~is_round(g.cop_lat, g.cop_lon)
    bar_real = g.barchi_lat.notna() & ~is_round(g.barchi_lat, g.barchi_lon)
    g["derived_has_real_coord"] = cop_real | bar_real
    g["best_lat"] = g.cop_lat.where(cop_real, g.barchi_lat.where(bar_real))
    g["best_lon"] = g.cop_lon.where(cop_real, g.barchi_lon.where(bar_real))
    g["derived_has_pleiades"] = g.pleiades.notna()
    g["derived_n_sources"] = g.cop_lat.notna().astype(int) + g.barchi_lat.notna().astype(int)
    g["lit_excavated"] = g.toponym.isin(EXCAVATED)
    g["lit_basis"] = g.toponym.map(EXCAVATED)
    g["lit_status"] = g.lit_excavated.map({True: "first pass — verify", False: "review"})
    g["in_brief_disputed"] = g.toponym.isin(BRIEF_DISPUTED)
    g["tier"] = g.apply(tier, axis=1)
    g["km_to_coast"] = [coast_distance(r.best_lat, r.best_lon, coast) for r in g.itertuples()]
    g["route_role"] = g.apply(route_role, axis=1)
    # Only genuinely coordinate-less sites are "position unknown". An island parked at
    # 17.5, 72.5 by every source has no position; one with a real coordinate elsewhere
    # is merely badly located, which the tier already records.
    g.loc[~g.derived_has_real_coord, "route_role"] = "position unknown"

    cols = ["site_id", "toponym", "chapter", "tier", "route_role", "km_to_coast",
            "lit_status", "lit_basis",
            "in_brief_disputed", "lat", "lon", "disagree_km", "derived_n_sources",
            "derived_coord_dp", "derived_placeholder_coord", "derived_placeholder_any",
            "derived_has_pleiades", "derived_has_real_coord",
            "derived_no_coords", "precision_flag", "in_copeland", "place_type", "pleiades"]
    out = g[cols].sort_values(["tier", "toponym"])
    out.to_csv(PROC / "site_confidence.csv", index=False)
    return out


if __name__ == "__main__":
    o = main()
    print("=== tiers across all 92 sites ===")
    print(o.tier.value_counts().sort_index().to_string())
    for t in sorted(o.tier.unique()):
        d = o[o.tier == t]
        print(f"\n--- {t}  (n={len(d)}) ---")
        print("  " + ", ".join(d.toponym))
    print("\n=== sites the brief calls disputed, and where they actually land ===")
    print(o[o.in_brief_disputed][["toponym", "tier", "disagree_km"]].to_string(index=False))
