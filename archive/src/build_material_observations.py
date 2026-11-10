"""Verified material observations.

Every row here has been read against its source. The miner
(mine_material.py) proposes; this file is what survived adjudication, plus
tabulated data transcribed by hand from published finds tables.

Rejected rows are not deleted -- material_candidates.csv keeps them with the
verdict, so the false-positive rate stays auditable.
"""
import csv, pathlib

DATA = pathlib.Path(__file__).resolve().parents[1] / "data"
SITES = {r["site_key"]: r for r in csv.DictReader(open(DATA / "raw" / "site_aliases.csv"))}
WARES = {r["ware_id"]: r for r in csv.DictReader(open(DATA / "raw" / "ware_typology.csv"))}

# --- Pattanam, Cherian 2012 Tables 1-2 ----------------------------------
# Five seasons, 2007-2011. Transcribed by hand; every row re-added and
# checked against the printed total. The one discrepancy is noted below.
PATTANAM_CERAMICS = {            # ware_id: (2007, 2008, 2009, 2010, 2011, printed total)
    "roman_amphora_unspec": (177, 286, 572, 2215, 2779, 6029),
    "mes_glazed":           (71, 107, 66, 422, 861, 1527),      # "TGP" = Turquoise Glazed Pottery
    "torpedo_jar":          (50, 156, 142, 767, 1983, 3098),
    "rouletted_ware":       (1037, 1266, 442, 3320, 2469, 8534),
    "sigillata_unspec":     (2, 7, 0, 2, 111, 122),
}
PATTANAM_LOCAL = (517831, 367079, 286475, 1471870, 894209, 3537464)
PATTANAM_ANTIQ = {               # label: (per-season..., printed total, unit)
    "Gold objects":    ((1, 2, 4, 38, 22), 67, "objects"),
    "Copper objects":  ((6, 27, 18, 68, 42), 161, "objects"),
    "Coins":           ((13, 12, 18, 31, 24), 98, "coins"),
    "Lead objects":    ((4, 19, 23, 63, 100), 209, "objects"),
    "Iron objects":    ((529, 758, 906, 3033, 2358), 7584, "objects"),
    "Glass beads":     ((1122, 1915, 6373, 22214, 7094), 38718, "beads"),
    "Stone beads":     ((50, 7, 108, 234, 148), 547, "beads"),
    "Spindle whorls":  ((4, 6, 5, 15, 9), 39, "objects"),
    "Cameo blanks":    ((2, 6, 3, 8, 29), 48, "objects"),
    "Glass fragments": ((35, 53, 138, 334, 778), 1338, "fragments"),
    "Lamps":           ((0, 4, 4, 8, 22), 38, "lamps"),
    "Ring stones":     ((0, 0, 0, 15, 9), 15, "objects"),
}
ANTIQ_WARE = {"Coins": "roman_coin", "Glass beads": "bead", "Stone beads": "bead",
              "Glass fragments": "roman_glass", "Lamps": "lamp", "Cameo blanks": "intaglio"}
CHERIAN = ("Cherian-Pattanam-Evidence-of-Maritime-Exchanges", 4,
           "Cherian 2012, Tamil Civilization 24.1-2, Tables 1-2")

rows = []
def add(**kw):
    s = SITES[kw["site_key"]]; w = WARES[kw["ware_id"]]
    rows.append({
        "site_key": kw["site_key"], "site_display": s["display_name"],
        "role": s["role"], "region": s["region"], "lat": s["lat"], "lon": s["lon"],
        "ware_id": kw["ware_id"], "ware_name": w["ware_name"], "category": w["category"],
        "count": kw["count"], "count_unit": kw["unit"],
        "count_qualifier": kw.get("qual", "exact"),
        "scope": kw["scope"], "context": kw.get("context", "excavated"),
        "source": kw["source"], "page": kw["page"], "citation": kw["cite"],
        "quote": kw.get("quote", ""), "note": kw.get("note", ""),
    })

src, pg, cite = CHERIAN
for wid, vals in PATTANAM_CERAMICS.items():
    for yr, v in zip(range(2007, 2012), vals[:5]):
        add(site_key="pattanam", ware_id=wid, count=v, unit="sherds",
            scope=f"season {yr}", source=src, page=pg, cite=cite)
    assert sum(vals[:5]) == vals[5], wid
    add(site_key="pattanam", ware_id=wid, count=vals[5], unit="sherds",
        scope="2007-2011 (5 seasons)", source=src, page=pg, cite=cite,
        note="season figures sum exactly to the printed total")

# The denominator. Roman amphora is 6,029 sherds against 3.54 million local
# sherds -- without this row the imported wares look far more prominent than
# they are.
add(site_key="pattanam", ware_id="local_pottery", count=PATTANAM_LOCAL[5], unit="sherds",
    scope="2007-2011 (5 seasons)", source=src, page=pg, cite=cite,
    note="local coarse pottery; the assemblage denominator")

for label, (per, tot, unit) in PATTANAM_ANTIQ.items():
    wid = ANTIQ_WARE.get(label)
    if not wid:
        continue
    add(site_key="pattanam", ware_id=wid, count=tot, unit=unit,
        scope="2007-2011 (5 seasons)", source=src, page=pg, cite=cite,
        note=f"Cherian Table 1, '{label}'" +
             ("; printed total 15 but the season figures sum to 24 -- "
              "the printed grand total 48,862 uses 15" if label == "Ring stones" else ""))

# --- adjudicated survivors from the miner --------------------------------
add(site_key="berenike", ware_id="bead", count=650, unit="beads", qual="approximate",
    scope="2014-2015 seasons", source="PAM-27-2020-includes-Aynuna-on-the-Red-Sea", page=204,
    cite="Then-Oblduska, PAM 27/1 (2018)",
    quote="Almost 650 beads and pendants, most of them of glass and faience, were excavated over two seasons in 2014 and 2015 at Berenike")
add(site_key="berenike", ware_id="roman_coin", count=9, unit="percent",
    scope="2nd-3rd c. AD share of the coin assemblage",
    source="Sidebotham-2011-Berenike-and-the-Ancient-Maritime-Spice", page=265,
    cite="Sidebotham 2011: 265",
    quote="Second- and third-century issues account for only about 9 percent of the total")
add(site_key="berenike", ware_id="roman_coin", count=34, unit="percent",
    scope="2nd quarter 4th - early 5th c. AD share of the coin assemblage",
    source="Sidebotham-2011-Berenike-and-the-Ancient-Maritime-Spice", page=265,
    cite="Sidebotham 2011: 265",
    quote="coins from the second quarter of the fourth into the late fourth and the early fifth centuries make up about 34 percent of the total")
add(site_key="pattanam", ware_id="roman_glass", count=400, unit="fragments",
    scope="season 2011", source="Cherian-2011-Pattanam-5th-Season-Field-Report", page=5,
    cite="Cherian 2011, 5th season field report",
    quote="400 glass fragments were recovered and this is so far the largest number reported from Pattanam",
    note="conflicts with Cherian 2012 Table 1, which gives 778 glass fragments for 2011")
add(site_key="pattanam", ware_id="roman_glass", count=906, unit="fragments", qual="approximate",
    scope="2007-2014", source="Historical-Archaeology-Iron-Age-Early-Historic-Kerala", page=10,
    cite="Historical Archaeology of Iron Age and Early Historic Kerala",
    quote="About 906 glass fragments including Roman pillared bowl were found at Pattanam from 2007-2014",
    note="conflicts with Cherian 2012 Table 1 (1,338 glass fragments by 2011); the later window reports fewer")
add(site_key="pattanam", ware_id="torpedo_jar", count=398, unit="sherds", qual="approximate",
    scope="2007-2014", source="Historical-Archaeology-Iron-Age-Early-Historic-Kerala", page=10,
    cite="Historical Archaeology of Iron Age and Early Historic Kerala",
    quote="About 398 Torpedo jar shreds were found at Pattanam excavations from 2007-2014",
    note="irreconcilable with Cherian 2012 (3,098 by 2011); probably a transcription slip for 3,098")
add(site_key="pattanam", ware_id="sigillata_unspec", count=2, unit="sherds",
    scope="stamped examples only", source="PAMA-Unearthing-Pattanam-Excavation-Catalogue", page=28,
    cite="PAMA, Unearthing Pattanam catalogue",
    quote="Pattanam has produced two stamped Terra Sigillata sherds",
    note="subset of the 122 sigillata sherds")
add(site_key="pattanam", ware_id="roman_coin", count=3, unit="hoards",
    scope="hoards in the vicinity", context="vicinity (not on site)",
    source="Shajan-Tomber-Selvakumar-Cherian-2004-JRA-Locating-the-Ancient-Port-of-Muziris", page=5,
    cite="Shajan, Tomber, Selvakumar & Cherian 2004, JRA 17",
    quote="4 were found in the vicinity of Pattanam: three containing Roman coins, at Eyyal, Valluvalli and Kumbalam",
    note="Eyyal, Valluvalli, Kumbalam; a 4th hoard at Puthenchira is punch-marked, not Roman")
add(site_key="arikamedu", ware_id="roman_amphora_unspec", count=116, unit="sherds",
    scope="Wheeler's 1945 excavation", source="Tomber-2008-Indo-Roman-Trade-From-Pots-to-Pepper", page=16,
    cite="Tomber 2008: 16, citing Wheeler et al. 1946",
    quote="Wheeler found 116 sherds of amphorae and 38 of terra sigillata",
    note="Pattanam's 6,029 amphora sherds now exceed Arikamedu by a factor of ~52")
add(site_key="arikamedu", ware_id="sigillata_unspec", count=38, unit="sherds",
    scope="Wheeler's 1945 excavation", source="Tomber-2008-Indo-Roman-Trade-From-Pots-to-Pepper", page=16,
    cite="Tomber 2008: 16, citing Wheeler et al. 1946",
    quote="Wheeler found 116 sherds of amphorae and 38 of terra sigillata")
add(site_key="xiis", ware_id="bead", count=2, unit="beads",
    scope="Tomb 14", source="apa-IndOc-Gulf-Xiis-Fernandez2022", page=22,
    cite="Fernandez et al. 2022",
    quote="found in Tomb 14, along with two cylindrical agate beads")

dest = DATA / "processed" / "material_observations.csv"
with open(dest, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print(f"{len(rows)} verified observations -> {dest.name}")
from collections import Counter
for k, v in Counter(r["site_display"] for r in rows).most_common():
    print(f"  {k:24s}{v}")
