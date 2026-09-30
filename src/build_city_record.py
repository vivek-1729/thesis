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

ASSESS = {
"leuke-kome": """
**Most likely: Aynuna.** My confidence is moderate to high, and the field's is
high but resting on the wrong argument.

The distance evidence does not discriminate. Nappo's 2010 case for Aynuna is the
standard treatment, but he measured from Abu Sha'ar, and recomputed from Quseir
al-Qadim both Aynuna at 236 km and al-Wajh at 222 km fall inside his own
185 to 278 km window. Anyone citing the distance for Aynuna is citing something
that does not separate the two.

What does separate them is material. Aynuna produced harbour installations, a
large storehouse, two cemeteries and 25 coins, 24 of them bronze, running from
Obodas III and Aretas IV to Tiberius. Bronze lost in occupation layers is small
change in daily use, and the date range ends at about AD 40, which is the
Periplus horizon. The storehouse also suits a port with a customs post and a
garrison, which is what the text describes.

The case has one real weakness. Al-Wajh has been surveyed, not excavated, so its
negative is a surface negative and weaker than it sounds. The whole
identification therefore rests on a single excavated assemblage, and a first
season at al-Wajh could unsettle it.

The textual constraint is separately weak. Leukē Kōmē hangs off one three-day leg
from one securely located port, so the positional estimate will stay wide however
good the material is.
""",

"barbarikon": """
**Most likely: Banbhore, but the question is closer to unanswerable than to
answered, and our candidate list is thinner than the literature.** My confidence
is low. The field's is divided, and the scholar Casson leans on declined to
identify the port at all.

**The text is unusually specific and none of it can be used.** The Periplus
places Barbarikon on the middle of seven mouths of the Indus, says the other six
are shallow, marshy and unnavigable, puts a small island offshore, and sets the
capital Minnagara upriver. Ptolemy independently gives seven mouths and names
them, with the fourth, Cariphi, as the middle one. That is more positional
information than the Periplus gives any other port in this study.

**The delta moved within antiquity itself, and has kept moving.** Strabo, at
15.700 and 15.701, following Aristobulus who travelled with Alexander, reports
two mouths where Ptolemy and the Periplus report seven. Casson observes that
both figures can be right because the river changed course repeatedly, and cites
Strabo 15.693 on a shift that caused the abandonment of a thousand cities. He
also records a documented change in 1758 that moved the channel twelve to
fifteen miles, citing Cousens, The Antiquities of Sind (Archaeological Survey of
India 46, Calcutta 1929). A twenty-kilometre channel migration inside the modern
era is the scale of instability any reconstruction has to work against.

**The scholar behind the famous quotation refused to identify it.** The "Smith"
Casson cites is Vincent A. Smith, The Early History of India (Oxford, fourth
edition 1924), and the remark is at his page 245: "the extensive changes which
have occurred in the rivers of Sind during the course of eighteen centuries
preclude the possibility of satisfactory identifications of either of these
towns." Casson notes elsewhere that Smith "himself does not support the
identification and indeed abstains from attempting any." This is not caution
about a particular site. It is a considered judgment that the problem is not
soluble on the available evidence, from a historian who knew the region.

**Our candidate list is impoverished.** Casson writes that "a plethora of
locations have been offered for the port, no two alike," and names Müller,
Fabricius, Schoff, Tomaschek in Pauly-Wissowa (1896), Warmington, and
Cunningham's Ancient Geography of India (1871). We carry only Banbhore. Before
any model is fitted, those proposals need to be recovered and located, because
a candidate set of one guarantees the answer.

**Ptolemy does not corroborate a coastal Barbarikon.** He lists a Barbara at
7.1.59 but places it far inland, so the one external check that works for Bakare
fails here.

**And Banbhore's own evidence is thin for physical reasons.** Khan's trenches of
1958 to 1966 stopped at heavy water infiltration before virgin soil, and the
Pakistani-Italian mission has not reported reaching it. The site was excavated as
Islamic Daybul rather than as Barbarikon, so finding little of Periplus date
carries much less weight than thirty seasons would ordinarily imply. Mughal's
2018 paper states that Banbhore "could be identified" with Barbarikon; the
editor's preface to the same volume says the study "establishes and identifies"
it. The qualification belongs to the author.

**Minnagar is a second unsolved location tied to the first.** The name means
Saka-town. Ptolemy lists a Binagara in the area at 7.1.61, probably the same
place. Cunningham put it at or near Tatta, "as the position at the head of the
inferior Delta commanded the whole traffic of the river." McCrindle cites three
further identifications, all different. More recent opinion leans slightly to
Bahmanabad, following Herrmann in Pauly-Wissowa (1932) and Warmington, while
Tarn will go no further than "somewhere eastward of the Indus Delta." These
proposals lie hundreds of kilometres apart.

**One firm chronological anchor.** The Periplus says Barbarikon lay in Parthian
hands, and Gondophares, first of the Indo-Parthian kings, is securely dated to
AD 20 to 46. That brackets the passage tightly and is one of the better dating
controls in the whole text.

**What would change this.** Reaching virgin soil at Banbhore, which means
dewatering; recovering the palaeochannels of the delta from imagery; and
assembling the other proposed locations so that the model has something to
choose between.
""",

"tyndis": """
**Most likely: the Ponnani to Tanur stretch, with Ponnani itself the best single
candidate.** My confidence is moderate, and unusually for this project the
material points the same way as the text.

Three independent lines converge on the northern Malabar coast around the
Bharathapuzha mouth. The Periplus puts Tyndis 500 stadia north of Muziris.
Ptolemy independently places Tindis north of Muziris, at 116°00' against
117°00'. And Casson's Chera border argument, which the literature rarely uses,
puts the port north of Ponnani and south of Cranganore.

The material is the surprise. Across fifty-nine years of Indian Archaeology: A
Review, Early Historic material in Kerala has been reported from essentially two
places, and one of them is Taluk Ponnani, where the 1970–71 volume records
Russet-coated Painted Ware of the early centuries AD and calls it "of great
significance." De Romanis also cites a Tamil poem describing Tyndis among
coconut palms, and a tradition that the port was abandoned because of piracy.

Against that, the 1978–79 survey went into this valley explicitly looking for
Roman contact and found megalithic burials instead. That is a genuine negative,
though it was a survey rather than an excavation, and no candidate has ever been
dug.

The honest limit is resolution. Casson accepts Ponnani or Beypore, which are
40 km apart, and says only that "the odds are slightly in favor of Ponnani." A
500-stadia leg carries a 68 per cent interval about 49 km wide. The evidence
supports a stretch of coast, not a village.
""",

"muziris": """
**Most likely: Pattanam.** My confidence is high for the Periyar delta and good
for the site itself. The field's confidence is high, with Gurukkal dissenting.

This is the one port where a positive and a negative sit 9 km apart. Kodungallur
was excavated in 1969–70 precisely because it was the traditional identification,
and everything recovered was ninth to eleventh century; the following volume
records that the trial digs "had not yielded any tangible evidence." Pattanam, a
few kilometres away, has produced the only quantified Early Historic assemblage
of any candidate in this study, and the PARUR gold hoard lies 3 km off.

Note what the standard argument actually secures. The Tamil poem places Muziris
on the Periyar, which fixes the river and not the site. Ptolemy lists Muziris
emporium and the mouth of the Pseudostomus, generally taken as the Periyar, as
separate entries 20 minutes of longitude apart, which suggests the emporium was
not at the mouth itself.

Two things should temper the confidence. Schoff records that Muziris and Nelkynda
were once placed at Mangalore and Nileshwar, 300 km north, so this identification
has moved a long way before. And Pattanam's imports are mostly not Roman. Of
19,654 imported sherds, under a third are Mediterranean, and the Mesopotamian
material is largely Sasanian. Pattanam was a working port for centuries, of which
the Periplus phase is a thin slice.
""",

"nelkynda": """
**Most likely: Niranam among the named candidates, but with real weight on a site
nobody has proposed.** My confidence is low to moderate. The field's is low, and
this port has the most recent literature of the seven, with a median publication
year of 2023.

The two constraints in the text cannot both be satisfied by straight-line
measurement. Nelkynda lies 500 stadia from Muziris and Bakarē lies 120 stadia
downriver at the mouth. Niranam and Purakkad are 21.2 km apart, close to 120
stadia and matching Casson's own "twelve miles," and they sit on the same river.
But Niranam is 106 km from Muziris along the coast against a band of 72 to
102 km. Schoff's alternative, Kottayam, fails worse: it is 29.6 km from Purakkad
against 18.6 km at a 155 m stadion, and Casson notes it sits on a different
river.

I favour Niranam because it satisfies the more reliable of the two figures. Every
stated value at or above 200 stadia in the Periplus is a round hundred, while 120
is one of only three unround figures in the text, so the pairing constraint
should outrank the 500-stadia leg. The 500 is also the figure most likely to be
rescued by measuring through the Vembanad backwaters, which is what "by river and
sea" specifies and which nobody has done.

Two cautions. Ptolemy places Melcynda at 120°20' in his region Aii, south of the
Baris mouth rather than upstream of it, which does not match the Periplus's
upriver port. And Dayalan lists Nakkada, Nirkunnam, Kannetri, Markari and
Varakkai, none of which we have located. Niranam and Neendakara have zero entries
in the fifty volumes of Indian Archaeology we were able to parse, and no candidate has been excavated.
""",

"bakare": """
**Most likely: Purakkad, conditional on Niranam being Nelkynda.** My confidence
in the identification is moderate and wholly derivative. But the port itself is
better attested than the Periplus alone suggests, and it should not be treated
as a minor place.

**Three independent ancient sources name it, and they disagree about its
standing.** The Periplus calls it a village at the mouth of Nelkynda's river,
where ships waited in the roadstead "because the river is full of shoals and the
channels are not clear." Ptolemy lists Bakare at 7.1.8. And Pliny rates it above
Muziris: at Natural History 6.104 he writes of "alius utilior portus gentis
Neacyndon, qui vocatur Becare," another and more useful port of the Neacyndi,
having just called Muziris the first emporium of India. At 6.105 he adds that the
pepper country of Cottonara sends its cargo down to Becare in dugout canoes. For
Pliny this is the port a merchant should actually use. The modern literature has
followed the Periplus's "village" and largely passed over Pliny's assessment.

**The name we use is an editorial correction.** Casson records that the sole
Periplus manuscript reads "Barare," and that the accepted form Bakare is emended
on the authority of Ptolemy and Pliny. The external sources are therefore doing
real work, and the reading in our only witness is not the one anyone prints.

**The text does not give the distance everyone quotes.** The Periplus says
Nelkynda "is situated on a river, about one hundred and twenty stadia from the
sea," at the end of chapter 54, and then opens chapter 55 with Bakare at the
mouth of that river. The 120 stadia measures Nelkynda to the sea. Casson converts
it into a Nelkynda-to-Bakare distance by treating the river mouth and the sea as
one point, joining two sentences across a chapter division. That is reasonable on
an open coast and a strong assumption on a lagoon coast, where a river debouches
into the backwater and the backwater reaches the sea through a separate bar.
Every claim about 120 stadia constraining the pair rests on that reading, ours
included.

**Whether Ptolemy corroborates the river-mouth placement is unclear.** Casson
states that "Ptolemy agrees with the Periplus in placing it at the mouth of a
river." But Ptolemy's own coordinate list gives Bacare at 119 degrees 30 minutes
and the mouth of the Baris at 120 degrees, as two separate entries thirty minutes
apart, which is his ordinary spacing between neighbouring places on this coast.
Either Casson is reading the adjacency as agreement or he is drawing on a
descriptive passage the coordinate table does not reflect. This matters because
the same claimed agreement supports the emendation of the name, and we cannot
resolve it without the Greek.

**The archaeology is empty.** None of Purakkad, Kallada or Thevalakara has been
excavated. Purakkad and Thevalakara return no entries at all across the fifty
volumes of Indian Archaeology: A Review that parsed cleanly, and Kallada returns
two, a neolithic axe from the river basin in 2006-07 and a temple inscription at
East Kallada in 1963-64, neither of them an excavation.

**Who proposed what.** Schoff 1912 identified it with Porakad, "for which it is a
close transliteration," and on the distance from his Nelkynda at Kottayam. Casson
rejected Kottayam, on the grounds that it and Pirakkad sit on different rivers
and are further apart than 120 stades, but kept Purakkad and re-paired it with
Niranam. McCrindle 1885 proposed Kallada instead, because its river is "the only
navigable river on this south-west coast except the Perriyar near Kranganur," and
placed the Baris as a stream entering the backwater near Quilon. Dayalan reports
Markari or Varakkai, or a point between Kanetti and Kollam. That the Purakkad
identification survived the collapse of the argument that produced it is a
warning rather than a corroboration.

**Casson grades Bakare among the five names identifiable "with more confidence
than the others."** Given that no candidate has been excavated, that the pairing
distance is inferred, and that the proposal outlived its own justification, I do
not think that grade is earned. Because the location follows entirely from which
site is Nelkynda, the pair should be reported together.
""",

"rhapta": """
**No candidate is well supported, and the two ancient sources pull in opposite
directions.** My confidence in any single location is low. The field inherits
Datoo's bracket from Pangani to the Rufiji but disputes the point within it.

The Periplus places Rhapta two days' sail beyond Menuthias, an island 300 stadia
offshore. At a 155 m stadion that is 46.5 km, and measured from island shore to
mainland shore Pemba fits at 42.8 km against Zanzibar at 36.1 and Mafia at 14.8.
If Menuthias is Pemba, two days south lands near Pangani or a little below it,
favouring the northern end of the bracket.

Ptolemy points the other way. He puts Rhaptum promontory at 8°25' south, and the
Rufiji delta lies at about 7°54' south, so his latitude, which is less distorted
near the equator than further north, favours the Rufiji. He also places Menuthias
at 12°30' south next to Prasum, roughly four degrees below Rhaptum, which
contradicts the Periplus outright. If Ptolemy is right about Menuthias then the
offshore notice does not constrain Rhapta at all, and our Pemba measurement rests
on the Periplus reading alone.

The material cannot break the tie. There is no numismatic evidence to assess:
the Coin Hoards of the Roman Empire database has no entry for Tanzania, Kenya,
Somalia or Ethiopia, and every coin recovered at a candidate site is Islamic or
later. Chami's Roman glass beads from the Rufiji are the most cited archaeological
claim about Rhapta and their stratigraphy has been questioned. Unguja Ukuu's
occupation begins in the sixth or seventh century, already too late.

Two things would move this: Datoo 1970, which we still cite second-hand, and the
early Roman coin finds north of the Rufiji that Juma mentions without a reference.
"""
}



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
    W("## Assessment\n")
    W("A provisional reading of the evidence assembled below, written before the "
      "model has been fitted. It states what the present evidence supports and "
      "how firmly, and the fitted posterior may disagree with it.\n")
    W(ASSESS[slug].strip() + "\n")
    W("## Contents\n")
    W("- [Assessment](#assessment)")
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
    # README.md is maintained separately; it carries the one-line verdicts.


if __name__ == "__main__":
    main()
