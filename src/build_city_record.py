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
**Most likely: Aynuna, or rather Khuraybah on the shore below it.** My confidence
is moderate to high. The field's is high, but resting on an argument that does
not work.

**The text gives days, not stadia, and the origin is disputed.** The Periplus
(19) reads, in Casson, "To the left of Berenice, after a voyage of two or three
runs eastward from Myos Hormos past the gulf lying alongside, there is another
harbor with a fort called Leuke Kome." So the figure is two or three days' sail,
the only distance the text supplies, and under the ancient rule of thumb that is
1,000 to 1,500 stadia. Schoff held that "the words 'from Mussel Harbor' in the
text are probably there only through an error in copying," and that the distance
and direction suit Berenike, the port named at the start of the same sentence.
Casson defends the manuscript, arguing that the author backtracks to Myos Hormos
deliberately in order to cover the stretch of Red Sea north of Berenike. The one
distance we have therefore depends on which of two starting points is correct,
and they are about 350 km apart.

**The distance argument in the modern literature does not discriminate.** Nappo
2010, the standard treatment, argues for Aynuna from the distance to Myos
Hormos, but measures from Abu Sha'ar, which is no longer accepted as Myos
Hormos. Recomputed from Quseir al-Qadim, Aynuna at 236 km and al-Wajh at 222 km
both fall inside the window he derives.

**Aynuna and Khuraybah are not rival candidates. They are parts of one site
complex.** The names are used loosely and sometimes interchangeably in the
literature, which makes the evidence harder to follow than it needs to be. At
least four distinct places sit within about five kilometres of each other along
Wadi Aynuna:

- **Khuraybah**, "the little ruin", the modern fishing village on Aynuna Bay.
  This is the shore, and Casson puts the ancient harbour here.
- **Lower Aynuna**, the site the Polish-Saudi mission excavated between 2014 and
  2018. Gawlikowski places it on the western bank of the wadi about 3 km from
  the harbour, and suggests the ancient shoreline ran closer, which "may explain
  the lack of port facilities visible in the fishing port of Khurayba."
- **A small fortified town on the cliff** above the wadi breach, which
  Gawlikowski records in 2022 as still awaiting exploration.
- **Aynuna**, the modern township further inland.

So the question is not whether Leuke Kome is Aynuna or Khuraybah. If it is here
at all, it is the complex, with the anchorage at the shore and the settlement
and storehouses up the wadi. Two practical consequences. Our coordinate, at
28.10 N 35.21 E, points at the inland end, roughly 5 km from the water, and any
distance we compute from it is measured from the wrong point by that much. And
the excavated evidence and the harbour evidence come from different parts of the
complex, so "excavated" and "where the ships lay" are not the same statement.

Note also a name collision to avoid: Fiema discusses a different al-Khurayba
entirely, the Dedanite and Lihyanite settlement at the al-Ula oasis, far inland
and unrelated.

**What is actually at Khuraybah.** Casson's note (p.163) is the fullest
statement: the port "would have been not at 'Aynunah itself, which is a short
distance inland, but at the modern village of Khuraybah on the water. Between
the two sites archaeologists have identified signs of extensive occupation that
date to the early centuries A.D. or even before: remains of impressive building
complexes, a necropolis with over one hundred tombs, an abundance of
Nabataean-Roman pottery," citing Ingraham and others in Atlal 5 (1981), 76-78.
That is the same survey that produced the al-Wajh negative, so both halves of
the comparison come from one field season.

Burton saw it in 1878 and described "the remains called El-Khuraybah, the little
ruin. The tenements, large and well-built, still show their bases; and on the
ground are scattered fragments of sea-coloured glass varying in tint, like the
Roman." Gawlikowski's excavation report locates the dug site, Lower Aynuna, on
the western bank of Wadi Aynuna about 3 km from the harbour, notes that the
ancient shoreline may have run closer, and observes that this "may explain the
lack of port facilities visible in the fishing port of Khurayba." His 2022 paper
also records a small fortified town on the cliff above the wadi breach that
remains unexplored.

**Nappo does not mention Khuraybah at all**, and he calls the Aynuna evidence
"meager." He places the port "in the area of modern Aynuna, c.5 km from the
coast," citing surveys that revealed "extensive architecture, including a tower
and a necropolis." So the strongest material argument for Aynuna is made in the
excavation report and in Casson's footnote rather than in the article the field
cites for the identification.

**Al-Wajh has more modern support than a single proposal.** Nappo's article is
written to rebut Gatier and Salles, who suggested al-Wajh or possibly Qarna;
Cuvigny, who argued from the Periplus description and the site's setting; and
Hill, who argued from Chinese texts. Three independent modern advocates, and
Qarna is a further candidate we do not carry.

**The stronger textual argument is Strabo's, and it is about roads rather than
sailing.** Strabo 16.781 has Leuke Kome on a well-travelled caravan route to
Petra, and at 16.4.24 he describes merchandise carried "from Leuce Come to
Petra, thence to Rhinocolura in Phoenicia near Egypt, and thence to other
nations." Casson notes, following Beeston and Kirwan, that this can hardly be
said of candidates as far south as Haura or Yanbu. A port that is a road-head
for Petra has to be in the north, and the overland distances make the point
quantitative: Petra lies 247 km from Khuraybah, 463 km from al-Wajh, 503 km
from al-Qusayr and 602 km from El Haura.

**Strabo also brackets it with a second port.** His account of Aelius Gallus's
expedition of 25 or 24 BC has the force landing at Leuke Kome and departing from
a port lower down the coast, Egra. Casson, following Bowersock, identifies Egra
with al-Wajh at 26 degrees 13 minutes north. **That matters for our candidate
list: on Casson's reading al-Wajh is Egra, a different port, so proposing it as
Leuke Kome contradicts the identification of the place it is usually contrasted
with.**

**Candidates we do not carry.** Schoff records that Leuke Kome "is placed by most
commentators at El Haura, 25 degrees 7 minutes north, 37 degrees 13 minutes
east," noting that the Arabic name Haura also means white and appears as Juara
in Ptolemy. Yanbu is mentioned as another southern proposal. Neither is in our
table, and El Haura was the majority view when Schoff wrote.

**The material is what actually separates them.** Aynuna produced harbour
installations, a large storehouse, two cemeteries and 25 coins, 24 of them
bronze, from Obodas III and Aretas IV to Tiberius, dated between the second
century BC and about AD 40. Bronze lost in occupation layers is small change in
daily use, at exactly the Periplus horizon. Al-Wajh has been surveyed rather than
excavated, and the only Roman coins there are three nummi of Maximianus from
AD 295 or 296 and three of Constantine I from the 320s, two and a half centuries
too late. That negative is a surface negative and weaker than it sounds.

**The geometry is weak regardless.** Leuke Kome hangs off a single leg from a
single securely located port, with no port beyond it to close the chain, so the
positional estimate will stay wide however good the material is.

**What is left to do here.**

1. Split the coordinate. Khuraybah on the shore and Lower Aynuna up the wadi
   should be separate rows, because the sailing distance is measured to one and
   the excavated evidence comes from the other.
2. Obtain Ingraham and others, Atlal 5 (1981), 76-78. It is the source for both
   the Khuraybah occupation and the al-Wajh negative, and we are citing both at
   second hand through Casson.
3. Add the candidates we do not carry: El Haura, which Schoff says was the
   majority view in his day, Yanbu, and Qarna, which Gatier and Salles raise
   alongside al-Wajh.
4. Read the Aynuna pottery. The 450-page excavation report has been mined for
   its coins and not for its ceramics, which is the assemblage that would let
   Leuke Kome enter the compositional analysis.
5. Establish whether the al-Wajh case rests on anything beyond the three
   arguments Nappo answers. Gatier and Salles, Cuvigny and Hill are cited by him
   and none is held locally.
6. The fortified town above the wadi is unexcavated. If the decision layer is
   asked where to dig for Leuke Kome, that is the obvious answer, and it can be
   stated before the model runs.
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
for the site. The field's is high, with Gurukkal dissenting. This is the only
port in the study where the excavation is good enough to argue with.

**What the KCHR actually did.** P. J. Cherian directed nine seasons between 2007
and 2015. Sixty trenches were opened, covering **less than one per cent of a
mound of about 70 hectares**. Excavation was locus-based with a Harris Matrix
used for the stratigraphic relationships, and ecofacts were recovered by
flotation. The 2011 season alone ran four months and opened ten trenches of
10 by 10 m and 9 by 4.5 m over about 250 square metres.

**Crucially, they reached the bottom.** The catalogue records a 5 by 4 m trench
taking two months "to reach the natural soil at a depth of 317 cm," and the
sequence runs Iron Age over natural soil, then an Iron Age to Early Historic
transition, then Early Historic, then medieval and modern. AMS radiocarbon on
charcoal from aeolian sand at 340 to 370 cm places the first settlement at about
1000 BC. **This is the direct contrast with Banbhore, where virgin soil has never
been reached.** At Pattanam the sequence is complete and the Periplus horizon
sits inside it rather than below the water table.

**The wharf is the strongest structural evidence for any candidate in the
study.** Excavation in the north-eastern sector revealed a wharf and a warehouse,
a six-metre canoe of anjili wood in a waterlogged context, and nine teak
bollards. The wharf is a platform of laterite, clay and lime with brick lining
where it meets the water. The canoe and bollards are radiocarbon dated to the
first century BC to first century AD, which is the Periplus horizon exactly. A
clay layer 25 to 35 cm thick sealed the waterlogged deposit at about 3 m and
prevented oxidation, preserving rice, black pepper, cardamom, frankincense,
bark, leaves, roots, seeds, wood and pulses. Other features include brick
foundations, burnt clay floors, ring wells, toilet features, storage jars and a
kiln.

**But the published figures do not agree with each other, and the disagreement
is large.** Cherian's season tables to 2011, which we have used throughout, give
3,557,118 sherds of which 3,537,464 are local, leaving about 19,654 imported, or
0.55 per cent. The later catalogue gives **4.5 million local body sherds,
516,676 diagnostic sherds and 140,165 non-Indian sherds**, which is an import
share near 2.7 per cent. Four extra seasons cannot produce a sevenfold rise in
imported material when the first five produced 19,654, so the two are counting
different things, most likely diagnostic sherds against all sherds of non-Indian
fabric. We have no way to reconcile them from what we hold.

That matters because the import fraction is the number the whole detection
argument rests on. At 0.55 per cent a trench at an untested candidate should be
expected to yield essentially nothing; at 2.7 per cent it should yield five
times as much. **Until the basis of the two counts is established, the expected
yield at a Malabar port is uncertain by a factor of five.**

The mound area is unstable too, given as 70 hectares in the catalogue against 45
in other summaries, which is why our derived excavated area is only order of
magnitude. This joins three discrepancies already recorded: torpedo sherds given
as 3,098 to 2011 and "about 398" to 2014, glass as 1,338 and then about 906, and
an arithmetic error in the ring-stones row of Cherian's Table 1.

**What the identification does and does not secure.** The Tamil poem places
Muziris on the Periyar, which fixes the river and not the site; Pattanam and
Kodungallur are 9 km apart on the same delta. Ptolemy lists Muziris emporium and
the mouth of the Pseudostomus as separate entries twenty minutes of longitude
apart, which suggests the emporium was not at the mouth. Kodungallur was dug at
five localities in 1969-70 precisely because it was the traditional
identification, and everything recovered was ninth to eleventh century. And
Schoff records that Muziris and Nelkynda were once placed at Mangalore and
Nileshwar, 300 km north, so this identification has moved a long way before.

**Pattanam was a port for much longer than it was Muziris.** Of the imported
pottery, under a third is Mediterranean, and the Mesopotamian material is
largely Sasanian and of the third to seventh centuries. The Periplus phase is a
thin slice of a long commercial life.

**What is still missing.**

1. The field reports for seasons six to nine, 2012 to 2015. We hold the fifth
   season report and the exhibition catalogue, and nothing between.
2. A reconciliation of the sherd counts. Establishing whether "non-Indian" in
   the catalogue means the same as "imported" in the season tables would settle
   the expected-yield figure.
3. Excavated area and depth trench by trench, which would let the assemblage be
   expressed as sherds per cubic metre and compared with Ras Hafun.
4. Gurukkal 2001, "In search of Muziris", the sceptical case against the
   consensus, which we cite at second hand.
5. Whether a final excavation report exists at all. Nine seasons have produced
   interim reports and a catalogue, and we have found no synthesis.
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

**The consensus on Purakkad is older than it looks.** Searching the corpus for
every spelling of the name, Purakkad, Porakad, Pirakkad and Porakkad, it appears
in exactly two works: Schoff 1912 and Casson 1989. It appears **zero times** in
Dayalan 2018, Dayalan 2019, De Romanis 2015, Tomber 2008 or Cobb 2018. No modern
treatment in the library asserts it.

What the recent literature does instead is decline to name a village. De Romanis
places "Becare-Nelkynda, located on a river that flowed less than 500 stadioi
south of Muziris, pointing to a place in the southern part of Vembanad Lake,"
and then names four candidate rivers rather than one: the Meenachil, Manimala,
Pampa and Achankovil. Note also his reading of "less than 500 stadioi" where the
text says about 500, which pulls the site north of where Schoff and Casson put
it. Dayalan lists Markari, Varakkai, or a point between Kanetti and Kollam, and
does not mention Purakkad at all.

So the apparent settlement is an artefact of which books one reads. The
identification is 1912 and 1989 vintage, and nobody writing in the last three
decades in this corpus has reasserted it.

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
