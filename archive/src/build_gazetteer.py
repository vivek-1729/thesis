"""Build the consolidated Periplus gazetteer.

Merges three sources that each hold part of the picture:
  1. Copeland's replication pack   -> full-precision coords for the 44 modelled ports
  2. Copeland's published Table 2  -> the names for those ports (the .dta files carry
                                      only numeric pcodes)
  3. Barchi / navigating-the-periplus -> all 85 sites in the text, with chapter numbers,
                                      Pleiades links, and the text's own route ordering

The two coordinate sets are kept side by side rather than reconciled. Where they
disagree is itself the signal: the well-attested ports agree to within a couple of
kilometres, the contested ones diverge by hundreds.
"""
import json, math, re, unicodedata
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW, OUT = ROOT / "data/raw", ROOT / "data/processed"
PACK = ROOT / "Replication Pack"

# The six ports the thesis is trying to locate, and the six it calibrates against.
DISPUTED = {"rhapta", "barbarikon", "tyndis", "nelkunda", "bakare", "leukekome"}
ANCHOR   = {"kane", "moschalimen", "berenike", "muoshormos", "barygaza", "muziris"}

# Copeland's region codes are finer than the region names printed in Table 2.
REGION_CODE = {100: "Egypt", 200: "Horn of Africa", 250: "East Africa", 300: "Arabia",
               350: "Persia", 400: "Persia", 450: "Scythia", 500: "India",
               550: "Scythia", 650: "East Asia"}


def slug(s):
    """Fold Greek transliterations to a comparable key: Nelkunda/Nelcynda, Bakarē/Bacare."""
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z]", "", s.lower())


# Barchi and Copeland romanise from different translations (Casson vs Schoff), so the
# same port appears under different spellings. Verified one by one against the 85
# toponyms Barchi actually publishes -- not guessed.
ALIAS = {  # Copeland spelling -> Barchi spelling
    "myoshormos": "muoshormos", "adulis": "adouli", "avalites": "aualites",
    "mosyllum": "mosullon", "mundus": "moundou", "tabae": "tabai",
    "menuthias": "menounthias", "pyralaaeislands": "puralaonislands",
    "cana": "kane", "dioscorida": "dioskouridouisland", "moscha": "moschalimen",
    "muza": "mouza", "ocelis": "okelis", "sarapis": "sarapisisland",
    "apologus": "apologos", "oraea": "horaia",
    "barbaricumminnagara": "barbarikon", "argaru": "argalou", "bacare": "bakare",
    "camara": "kamara", "nelcynda": "nelkunda", "paethana": "paithana",
    "palaesimundu": "palaisimoundou", "poduca": "podouke",
}

# Seven of Copeland's 44 ports are not among Barchi's 85 sites. Arsinoe and Diospolis
# are inland Egyptian cities outside the Periplus proper; Nicon and Sarapion are named
# in ch. 15 but omitted by Barchi; Ariace is a region rather than a port. These carry
# Copeland coordinates only.
COPELAND_ONLY = {"arsinoe", "diospolis", "nicon", "sarapion", "ariaca",
                 "dosarene", "besatae"}


def haversine(lat1, lon1, lat2, lon2):
    if any(pd.isna(v) for v in (lat1, lon1, lat2, lon2)):
        return float("nan")
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = (math.sin((p2 - p1) / 2) ** 2
         + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lon2 - lon1) / 2) ** 2)
    return 2 * 6371.0 * math.asin(math.sqrt(a))


def load_geojson_var(path):
    """The webmap ships GeoJSON wrapped in a `var x = {...}` assignment."""
    text = path.read_text()
    return json.loads(text[text.index("{"):])


def load_replication_ports():
    """44 ports with the coordinates Copeland's sailing model actually used."""
    frames = []
    for name in ("gravity_trade_data.dta", "gravity_trade_data_zeros.dta"):
        d = pd.read_stata(PACK / name)
        for side in ("1", "2"):
            frames.append(d[[f"pcode{side}", f"region{side}", f"lat{side}", f"lon{side}"]]
                          .set_axis(["pcode", "region_code", "lat", "lon"], axis=1))
    ports = (pd.concat(frames).drop_duplicates("pcode")
             .sort_values("pcode").reset_index(drop=True))
    ports["pcode"] = ports.pcode.astype(int)
    ports["region"] = ports.region_code.map(REGION_CODE)
    return ports


def name_replication_ports(ports, table2):
    """Table 2 prints names but rounds coordinates; the .dta files have precision but
    only numeric pcodes. Match them by proximity.

    The assignment is one-to-one: a greedy nearest-match assigns Sarapion to two
    different pcodes, because pcode 252's coordinates sit 177 km from where Table 2
    prints Nicon. Resolving globally forces 252 to take Nicon by elimination and
    surfaces that discrepancy instead of burying it.
    """
    pairs = sorted(
        (haversine(p.lat, p.lon, t.lat, t.lon), p.pcode, t.city, t.goods, t.partners)
        for _, p in ports.iterrows() for _, t in table2.iterrows())
    taken_p, taken_c, rows = set(), set(), []
    for dist, pcode, city, goods, partners in pairs:
        if pcode in taken_p or city in taken_c:
            continue
        taken_p.add(pcode); taken_c.add(city)
        rows.append({"pcode": pcode, "city": city, "table2_offset_km": round(dist, 2),
                     "goods": goods, "partners": partners})
    return ports.merge(pd.DataFrame(rows), on="pcode")


def load_barchi():
    """All 85 sites in the text, with the route ordering the thesis depends on."""
    rows = []
    for f in load_geojson_var(RAW / "periplus_sites.js")["features"]:
        p, g = f["properties"], f.get("geometry")
        rows.append({
            # Several toponyms carry trailing whitespace in the source ("Rhapta "),
            # which silently breaks joins on name. Strip everything on the way in.
            "toponym": p["ancient_toponym"].strip(),
            "barchi_lat": g["coordinates"][1] if g else float("nan"),
            "barchi_lon": g["coordinates"][0] if g else float("nan"),
            "precision_flag": p.get("location_precision"),
            "location_source": p.get("location_source"),
            "pleiades": p.get("pleiades_link"),
            "chapter": (p.get("periplus_chapter") or "").replace("PME, Ch.", "").strip(),
            "place_type": (p.get("periplus_place_type") or "").strip() or None,
            "route": (p.get("route") or "").title(),
            "next_on_route": (p.get("next_on_route") or "").strip() or None,
        })
    b = pd.DataFrame(rows)
    b["key"] = b.toponym.map(slug)
    return b


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    table2 = pd.read_csv(RAW / "copeland_table2.csv")
    cop = name_replication_ports(load_replication_ports(), table2)
    cop["key"] = cop.city.map(slug).map(lambda k: ALIAS.get(k, k))
    barchi = load_barchi()

    g = barchi.merge(
        cop[["key", "pcode", "city", "region", "lat", "lon", "goods", "partners",
             "table2_offset_km"]].rename(columns={"lat": "cop_lat", "lon": "cop_lon"}),
        on="key", how="outer")

    # Sites present only in Copeland keep their name; the rest come from Barchi.
    g["toponym"] = g.toponym.fillna(g.city)
    g["key"] = g.key.fillna(g.toponym.map(slug))

    g["disagree_km"] = [round(haversine(r.cop_lat, r.cop_lon, r.barchi_lat, r.barchi_lon), 1)
                        for r in g.itertuples()]
    # Prefer the coordinates Copeland's model ran on; fall back to Barchi.
    g["lat"] = g.cop_lat.fillna(g.barchi_lat)
    g["lon"] = g.cop_lon.fillna(g.barchi_lon)
    g["coord_source"] = g.cop_lat.notna().map({True: "copeland", False: "barchi"})
    g.loc[g.lat.isna(), "coord_source"] = "none"

    # Four ports exist only in Copeland and so carry no route from Barchi. Assign them
    # by the itinerary they geographically belong to: Arsinoe heads the Red Sea, Nicon
    # sits on the Azanian coast, Ariace and Dosarene are on the Indian run.
    g["route"] = g.route.fillna(g.toponym.map(
        {"Arsinoe": "Western Route", "Nicon": "Western Route",
         "Ariaca": "Eastern Route", "Dosarene": "Eastern Route"}))

    g["status"] = "other"
    g.loc[g.key.isin(ANCHOR), "status"] = "anchor"
    g.loc[g.key.isin(DISPUTED), "status"] = "disputed"
    g["in_copeland"] = g.pcode.notna()

    # Chapter number drives the reading order of the text; keep the first number cited.
    g["chapter_num"] = pd.to_numeric(g.chapter.str.extract(r"(\d+)")[0])
    g = g.sort_values(["chapter_num", "toponym"], na_position="last").reset_index(drop=True)
    g.insert(0, "site_id", range(1, len(g) + 1))

    cols = ["site_id", "key", "toponym", "city", "status", "chapter", "chapter_num",
            "route", "next_on_route", "place_type", "region", "lat", "lon",
            "coord_source", "cop_lat", "cop_lon", "barchi_lat", "barchi_lon",
            "disagree_km", "precision_flag", "location_source", "pleiades",
            "pcode", "goods", "partners", "table2_offset_km", "in_copeland"]
    g = g[cols]
    g.to_csv(OUT / "gazetteer.csv", index=False)

    feats = [{"type": "Feature",
              "geometry": None if pd.isna(r.lat) else
                          {"type": "Point", "coordinates": [r.lon, r.lat]},
              "properties": {k: (None if pd.isna(v) else v)
                             for k, v in r._asdict().items() if k != "Index"}}
             for r in g.itertuples()]
    (OUT / "gazetteer.geojson").write_text(json.dumps(
        {"type": "FeatureCollection", "features": feats}, ensure_ascii=False, indent=1))

    return g, cop


if __name__ == "__main__":
    g, cop = main()
    print(f"sites: {len(g)}   in Copeland: {int(g.in_copeland.sum())}   "
          f"with coords: {int(g.lat.notna().sum())}")
    print(f"\nCopeland ports that failed to match a Barchi site: "
          f"{sorted(cop.loc[~cop.key.isin(g.dropna(subset=['toponym']).key), 'city'])}")
    print(f"\nTable 2 vs replication-pack coordinate offsets > 1 km:")
    print(cop[cop.table2_offset_km > 1][["city", "pcode", "table2_offset_km"]]
          .to_string(index=False))
