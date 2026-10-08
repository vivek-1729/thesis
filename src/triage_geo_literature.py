"""Mark which of the sweep's 575 hits are worth fetching.

The sweep matches on loose text, so it returns the right region with the wrong
question (groundwater salinity in the Periyar basin) and the right question in
the wrong region (beach ridges in Thailand). A hit is kept only when it clears
both: a place this thesis cares about, and a subject that bears on where a
shoreline, a channel or a water depth was.

The method group is the exception. It has no region, and is kept on subject
alone, because a shoreline-uncertainty method travels.
"""
import csv, re, pathlib

D = pathlib.Path(__file__).resolve().parents[1] / "data" / "processed"

PLACE = {
    "kerala-coastal-evolution": r"kerala|periyar|vembanad|muziris|kuttanad|alappuzha|malabar|cochin|kochi|ashtamudi|kollam|pattanam|kodungallur|chettuva|sw india|south.?west india",
    "kerala-dated-shoreline":   r"kerala|vembanad|pamba|periyar|alappuzha|malabar|muziris|south.?east asia.*india|maldives.*india|india.*sri lanka",
    "kerala-subsurface":        r"kerala|periyar|kuttanad|vembanad|alappuzha|malabar",
    "indus-delta":              r"indus|sindh|makran|pakistan|las bela|balochistan|banbhore|arabian sea.*(coast|pakistan)|kachchh|banni",
    "rhapta-tanzania":          r"tanzania|rufiji|zanzibar|mafia|east africa|swahili|rhapta|azania|unguja|pemba|kilwa",
    "red-sea-arabia":           r"red sea|arabia|aqaba|nabat|aynuna|hijaz|midyan|wajh|sinai|yemen|farasan",
    "method":                   r".",
}

# What the thesis actually needs from a paper: a date, a position, a depth,
# or a subsurface geometry.
SUBJECT = re.compile(
    r"holocene|quaternary|sea.?level|shoreline|coastal evolution|palaeo|paleo|"
    r"beach ridge|lagoon|delta|estuar|sediment|stratigraph|radiocarbon|"
    r"luminescence|osl|mangrove|core|borehole|resistivity|bathymetr|chart|"
    r"georeferen|tide|tidal|avulsion|channel|harbour|harbor|port|excavat|"
    r"geomorph|progradation|subsidence", re.I)

# The method group needs a narrower net still. It is kept for techniques this
# project either uses or could adopt: depth from reflectance, the error budget on
# an extracted shoreline, putting an old chart on the ground, and finding a
# channel in imagery. Everything else in remote sensing matches "shoreline".
METHOD_OK = re.compile(
    r"stumpf|satellite.?derived bathymetr|log.?ratio|depth from|"
    r"shoreline (change|position|uncertain|extract|monitor)|"
    r"uncertaint|error budget|positional accuracy|"
    r"georeferen|historical (chart|map|aerial|nautical)|"
    r"palaeochannel|paleochannel|buried channel|"
    r"tide (model|gauge)|tidal (model|datum|correction)|"
    r"archaeological prospection|crop mark", re.I)

# Subjects that share the vocabulary and answer a different question.
VETO = re.compile(
    r"salinity intrusion|groundwater potential|flood susceptib|drinking water|"
    r"heavy metal|radionuclide|carbon stock|soil carbon|ecosystem service|"
    r"livelihood|perception|climate change adaptation|whale|machine learning for "
    r"shoreline|urbanization|streamflow projection|land use land cover change|"
    r"water quality|pollution|fishery|aquaculture|tourism", re.I)


def main():
    path = D / "geo_literature_candidates.csv"
    rows = list(csv.DictReader(open(path)))
    for r in rows:
        t = r["title"]
        subject = METHOD_OK if r["gap"] == "method" else SUBJECT
        hit = (re.search(PLACE[r["gap"]], t, re.I)
               and subject.search(t) and not VETO.search(t)
               and r["is_oa"] == "Y" and r["oa_urls"])
        r["keep"] = "Y" if hit else ""

    fields = [f for f in rows[0] if f != "keep"] + ["keep"]
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader(); w.writerows(rows)

    from collections import Counter
    c = Counter(r["gap"] for r in rows if r["keep"] == "Y")
    print(f"{sum(c.values())} kept of {len(rows)}\n")
    for g in PLACE:
        print(f"  {g:26s} {c[g]:3d}")


if __name__ == "__main__":
    main()
