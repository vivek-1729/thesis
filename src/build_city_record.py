"""One file per port, holding every mention of it that exists in the library.

Replaces the earlier dossiers. The dossiers were a passage dump; these are
organised, carry a table of contents that shows the whole record at a glance,
and separate what the ancient sources say from what modern scholars have
proposed from what has actually been excavated.

Only the local library is searched. Nothing here is drawn from the open web.
"""
import csv, re, pathlib, collections, html

ROOT = pathlib.Path(__file__).resolve().parents[1]
CACHE = ROOT.parent / "library/text-cache"
OUT = ROOT / "docs/cities"

PORTS = [
    ("leuke-kome", "Leukē Kōmē", [
        "Leuke Kome", "Leuké Kómé", "Leukos Limen", "Leuce Come", "White Village",
        "Aynuna", "Aynunah", "Aynūna", "al-Wajh", "al Wajh", "Khuraybah"]),
    ("barbarikon", "Barbarikon", [
        "Barbarikon", "Barbaricum", "Barbarike", "Barbarei", "Barbaricon",
        "Banbhore", "Bhambore", "Bhanbhore", "Daybul", "Debal", "Minnagar"]),
    ("tyndis", "Tyndis", [
        "Tyndis", "Tundis", "Tondi", "Tonḍi", "Ponnani", "Ponāni",
        "Kadalundi", "Beypore", "Koyilandy", "Pantalayani", "Panthalayani", "Tanur"]),
    ("muziris", "Muziris", [
        "Muziris", "Muchiri", "Muziri", "Muyirikkodu", "Musiri",
        "Pattanam", "Kodungallur", "Cranganore", "Kodungallūr"]),
    ("nelkynda", "Nelkynda", [
        "Nelkynda", "Nelcynda", "Nelcinda", "Melcynda", "Melkynda", "Nelkunda",
        "Niranam", "Neranom", "Niranom", "Nirkunnam", "Kottayam", "Quilon", "Kollam"]),
    ("bakare", "Bakarē", [
        "Bakare", "Becare", "Bacare", "Barace", "Bakarē",
        "Purakkad", "Porakad", "Pirakkad", "Porakkad", "Kallada", "Thevalakara"]),
    ("rhapta", "Rhapta", [
        "Rhapta", "Rhaptum", "Rhapton", "Menuthias", "Menouthias", "Menuthesias",
        "Azania", "Rufiji", "Pangani", "Mafia", "Unguja", "Fukuchani", "Kisimani"]),
]

# Which file is which kind of source, so the record can be ordered sensibly.
ANCIENT = ("Casson-1989", "Schoff-1912", "McCrindle", "Ptolemy-Geography", "Rylands")
FIELD = ("apa-RedSea-Aynuna", "apa-IndOc-Gulf-Qana", "apa-IndOc-Gulf-Sumhuram",
         "apa-IndOc-Gulf-Arikamedu", "apa-IndOc-Gulf-RasHafun", "apa-IndOc-Gulf-Socotra",
         "apa-RedSea-Adulis", "apa-RedSea-Berenike", "apa-RedSea-MyosHormos",
         "apa-RedSea-PtolemaisTheron", "apa-IndOc-Gulf-Somalia", "apa-IndOc-Gulf-Xiis",
         "Gawlikowski", "Felici", "Cherian", "PAMA", "Pakistan-Archaeology",
         "Sidebotham", "Cappers")

TITLES = {}   # filled from the filename, tidied


def pretty(stem):
    t = stem.replace("apa-IndOc-Gulf-", "").replace("apa-RedSea-", "")
    t = t.replace("-", " ").replace("_", " ")
    t = re.sub(r"\s+", " ", t).strip()
    return t


def kind(stem):
    if stem.startswith(ANCIENT): return "ancient"
    if any(stem.startswith(f) for f in FIELD): return "field"
    return "scholarship"


def pages(txt):
    parts = re.split(r"\n?\[{1,2}\s*(?:PAGE|Page|page)\s*(\d+)\s*\]{1,2}\n?", txt)
    if len(parts) < 3:
        yield 0, txt
        return
    for i in range(1, len(parts) - 1, 2):
        yield int(parts[i]), parts[i + 1]


def sweep(aliases):
    """Every sentence in the library naming any alias, with its page."""
    pat = re.compile("|".join(re.escape(a) for a in aliases), re.I)
    hits = collections.defaultdict(list)
    for f in sorted(CACHE.glob("*.txt")):
        txt = f.read_text(errors="ignore")
        if not pat.search(txt):
            continue
        for pg, body in pages(txt):
            if not pat.search(body):
                continue
            flat = re.sub(r"[ \t]+", " ", body.replace("\n", " "))
            for sent in re.split(r"(?<=[.;:!?])\s+", flat):
                sent = sent.strip()
                if not (30 < len(sent) < 700) or not pat.search(sent):
                    continue
                hits[f.stem].append((pg, sent))
    return hits


def load_tables():
    d = {}
    d["camp"] = list(csv.DictReader(open(ROOT / "data/raw/excavation_campaigns.csv")))
    d["finds"] = list(csv.DictReader(open(ROOT / "data/raw/material_finds.csv")))
    d["iar"] = list(csv.DictReader(open(ROOT / "data/raw/iar_findspots.csv")))
    d["sites"] = list(csv.DictReader(open(ROOT / "data/raw/site_aliases.csv")))
    d["cand"] = list(csv.DictReader(open(ROOT / "data/raw/candidate_evidence.csv")))
    d["later"] = list(csv.DictReader(open(ROOT / "data/raw/later_settlement.csv")))
    d["ptol"] = list(csv.DictReader(open(ROOT / "data/raw/ptolemy_entries.csv")))
    return d


def anchor(s):
    return re.sub(r"[^a-z0-9 -]", "", s.lower()).replace(" ", "-")


def build(slug, name, aliases, T):
    hits = sweep(aliases)
    by_kind = collections.defaultdict(list)
    for stem, hh in hits.items():
        by_kind[kind(stem)].append((stem, hh))
    for k in by_kind:
        by_kind[k].sort(key=lambda x: -len(x[1]))
    total = sum(len(h) for h in hits.values())

    L = []
    W = L.append
    W(f"# {name}\n")
    W(f"Every mention of {name} and its proposed sites that exists in the local "
      f"library: {total:,} passages across {len(hits)} works. Nothing here is "
      f"drawn from the open web. Passages are verbatim and carry the page of "
      f"the PDF they were read from.\n")

    # ---- contents
    W("## Contents\n")
    W("- [The record in summary](#the-record-in-summary)")
    W("- [Proposed locations](#proposed-locations)")
    if [r for r in T["ptol"] if r["port"] == name.replace("\u0113", "e")]:
        W("- [Ptolemy's coordinates](#ptolemys-coordinates)")
    W("- [The excavation record](#the-excavation-record)")
    if any(r["port"].lower().startswith(name.split()[0][:4].lower()) for r in T["iar"]):
        W("- [Indian Archaeology: A Review](#indian-archaeology-a-review)")
    W("- [Quantified finds](#quantified-finds)")
    W("- [Mentions in the library](#mentions-in-the-library)")
    for lbl, key in [("Ancient sources", "ancient"),
                     ("Excavation reports", "field"),
                     ("Modern scholarship", "scholarship")]:
        if not by_kind.get(key):
            continue
        W(f"  - [{lbl}](#{anchor(lbl)})")
        for stem, hh in by_kind[key]:
            W(f"    - [{pretty(stem)}](#{anchor(pretty(stem))}) — {len(hh)}")
    W("")

    # ---- summary
    W("## The record in summary\n")
    cands = [c for c in T["cand"]
             if any(a.lower().replace("-", "_").replace(" ", "_") in c["site_key"]
                    for a in aliases)]
    camps = [c for c in T["camp"] if c["port"] == name or
             c["port"] == name.replace("ē", "e")]
    dug = [c for c in camps if c["n_seasons"] not in ("", "0")]
    W(f"| | |")
    W(f"|---|---|")
    W(f"| Proposed sites in our table | {len(camps)} |")
    W(f"| Of those, ever excavated | {len(dug)} |")
    W(f"| Passages in the library | {total:,} across {len(hits)} works |")
    W(f"| Ancient sources naming it | {len(by_kind.get('ancient', []))} |")
    W("")

    # ---- proposed locations
    W("## Proposed locations\n")
    if camps:
        W("| Site | Coordinates | Excavation | Reached Periplus horizon |")
        W("|---|---|---|---|")
        S = {s["site_key"]: s for s in T["sites"]}
        for c in sorted(camps, key=lambda r: r["site_display"]):
            s = S.get(c["site_key"], {})
            co = f'{s.get("lat","")}, {s.get("lon","")}' if s.get("lat") else "—"
            yrs = (f'{c["year_from"]}–{c["year_to"]}, {c["n_seasons"]} seasons'
                   if c["n_seasons"] not in ("", "0") else "never excavated")
            yrs = yrs.replace("1 seasons", "1 season")
            W(f'| {c["site_display"]} | {co} | {yrs} | {c["reached_periplus_horizon"] or "—"} |')
    else:
        W("_No proposed site for this port appears in the candidate table._")
    W("")

    # ---- Ptolemy
    pt = [r for r in T["ptol"] if r["port"] == name.replace("\u0113", "e")]
    if pt:
        W("## Ptolemy's coordinates\n")
        W("From the Stevenson translation of the *Geography*. Ptolemy's longitudes "
          "run from his own prime meridian and his latitudes are systematically "
          "compressed, so the figures are useful for the order and spacing of "
          "places rather than as positions. Degrees and minutes as printed.\n")
        W("| Place | Book | Longitude | Latitude | Note |")
        W("|---|---|---|---|---|")
        for r in pt:
            lat = f'{r["p_lat"]} {r["hemisphere"]}'
            W(f'| {r["ptolemy_name"]} | {r["book"]} | {r["p_lon"]} | {lat} | {r["note"]} |')
        W("")

    # ---- excavation record
    W("## The excavation record\n")
    if dug:
        for c in dug:
            W(f'**{c["site_display"]}**, {c["investigators"] or "investigator not recorded"}'
              f'{", " + c["institution"] if c["institution"] else ""}, '
              f'{c["year_from"]}–{c["year_to"]}, {c["n_seasons"]} seasons.')
            bits = []
            if c["reached_virgin_soil"]: bits.append(f'Virgin soil: {c["reached_virgin_soil"]}.')
            if c["targeted_at_port"]:
                bits.append("Excavated because the site was already proposed as this port."
                            if c["targeted_at_port"] == "yes"
                            else "Excavated for reasons unrelated to this identification.")
            if c["publication_status"]: bits.append(f'Publication: {c["publication_status"]}.')
            if bits: W(" ".join(bits))
            if c["quote"]: W(f'\n> {c["quote"]}')
            if c["note"]: W(f'\n{c["note"]}')
            W("")
    else:
        W("_No proposed site for this port has been excavated._\n")

    # ---- IAR
    iar = [r for r in T["iar"] if r["port"].lower().startswith(name[:4].lower().rstrip("ē"))]
    if iar:
        W("## Indian Archaeology: A Review\n")
        W("Findspots recorded in the annual series and geolocated to district level.\n")
        W("| Place | District | Volume | Recorded |")
        W("|---|---|---|---|")
        for r in sorted(iar, key=lambda x: x["iar_volume"]):
            W(f'| {r["name"]} | {r["district"]} | {r["iar_volume"]} | {r["what_was_found"]} |')
        W("")

    # ---- finds
    fnd = [f for f in T["finds"]
           if any(a.lower().replace(" ", "_").replace("-", "_") in f["site_key"] for a in aliases)]
    W("## Quantified finds\n")
    if fnd:
        W("| Class | Quantity | Scope | Source |")
        W("|---|---|---|---|")
        for f in fnd:
            q = f'{f["quantity_value"]} {f["quantity_unit"]}'
            if f["denominator_value"]:
                q += f' of {int(f["denominator_value"]):,}'
            W(f'| {f["ware_as_published"]} | {q} | {f["scope_detail"] or f["scope"]} '
              f'| {pretty(pathlib.Path(f["source_file"]).stem)} p.{f["page"]} |')
    else:
        W("_No quantified finds are recorded for any proposed site._")
    W("")

    # ---- the passages
    W("## Mentions in the library\n")
    seen_all = set()
    for lbl, key in [("Ancient sources", "ancient"),
                     ("Excavation reports", "field"),
                     ("Modern scholarship", "scholarship")]:
        if not by_kind.get(key):
            continue
        W(f"### {lbl}\n")
        for stem, hh in by_kind[key]:
            W(f"#### {pretty(stem)}\n")
            W(f"_{len(hh)} passages._\n")
            for pg, sent in hh:
                key2 = re.sub(r"\W", "", sent)[:110]
                if key2 in seen_all:
                    continue
                seen_all.add(key2)
                W(f"> p.{pg} — {sent}\n")
    return "\n".join(L)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    T = load_tables()
    idx = ["# The seven ports, port by port\n",
           "One file per port holding every mention of it in the local library, "
           "with the excavation record and the quantified finds alongside. "
           "Built by `src/build_city_record.py`.\n"]
    for slug, name, aliases in PORTS:
        md = build(slug, name, aliases, T)
        (OUT / f"{slug}.md").write_text(md)
        n = md.count("\n> p.")
        idx.append(f"- [{name}]({slug}.md) — {n:,} passages")
        print(f"{name:12s} {n:5,} passages  {len(md):>9,} chars")
    (OUT / "README.md").write_text("\n".join(idx) + "\n")


if __name__ == "__main__":
    main()
