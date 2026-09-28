# Findings

What the assembled evidence has actually shown, as of September 2026. This
distils the working documents written during evidence gathering; those have been
deleted and their content is here. Per-port detail with verbatim passages stays
in the seven dossiers.

Everything in quotation marks is verbatim from the source named.

---

## 1. The problem

The *Periplus Maris Erythraei* is a merchant's handbook to the Indian Ocean,
written in Greek around AD 50 by an anonymous trader working out of Roman Egypt.
It names the harbours between the Red Sea and the Bay of Bengal, gives distances
between them, and lists what could be bought and sold at each.

For many of the places it names, nobody knows where they were. Three reasons.
The text survives in one manuscript, a tenth-century copy in Heidelberg
(Pal. gr. 398), with a single later apograph, so there is no independent witness
against a corrupted name or a mistaken number. Distances come in stadia and in
days' sail, neither of which converts cleanly to kilometres. And the coastlines
have moved: rivers have switched channels, deltas have prograded kilometres
seaward, and harbours that were open water are now silted lagoon or dry land.

Seven ports are in scope. Six are genuinely disputed — **Leukē Kōmē** on the Red
Sea coast of Arabia, **Barbarikon** in the Indus delta, **Tyndis**, **Nelkynda**
and **Bakarē** on the Malabar coast, and **Rhapta** somewhere on the coast of
Tanzania. **Muziris** is treated as secure and is included because the security
is narrower than it looks.

---

## 2. The Periplus as a measuring instrument

### 2.1 The text rounds large distances and not small ones

33 of 51 distance statements are in stadia. **82 per cent are multiples of 100.**
Every value at or above 200 is a round hundred, without exception. The only
unround figures are 20, 60 and 120, all small and all local: 20 stadia upriver at
Muziris, 120 stadia downriver at Nelkynda, 60 elsewhere.

Two classes of number with different precision. Large coastal legs are estimates
to the nearest hundred. Short local measures may be direct knowledge.

The implication inverts the usual order of argument: **the upriver notices
deserve more weight than the 500-stadia legs**, which is the reverse of how the
literature uses them.

*Source: `data/processed/distances.csv`.*

### 2.2 Most distance statements are not sailing legs

Only 22 of 51 are legs between ports. The rest are 7 inland, 5 offsets, 5
extents, 5 widths, 3 upriver, 2 runs. 18 of 51 are in days rather than stadia.
Any treatment of the Periplus as a list of sailing distances is using under half
the corpus.

### 2.3 The stadion calibrates to about 155 m, not the conventional 185 m

Median of four legs with securely identified endpoints. That shifts every derived
position by about 16 per cent, which is enough to change which candidate fits.

Casson works from the ancient rule of thumb instead, stated in his Appendix 2:
"Their rule of thumb was 1000 stades to a day-and-night run, 500 to a day's run,"
and "approximately ten stades correspond to a nautical mile," which implies about
185 m.

**Not yet run, and the highest-value unrun analysis we have: per-leg implied
values rather than a single median.** Whether the implied stadion drifts by
region, leg length or leg type is the open question.

### 2.4 Casson's own table is internally inconsistent

Casson prints identifications with the distance in nautical miles between each
port and the next (Appendix 1, Table II). Two legs are given in the Periplus as
500 stadia each:

| Leg, as Casson identifies it | Nautical miles | Stated stadia | Implied stadion |
|---|---|---|---|
| Tyndis (Ponnani) to Muziris (Cranganore) | 39 | 500 | **144 m** |
| Muziris (Cranganore) to Nelkynda/Bakarē (Niranom–Pirakkad) | 55 | 500 | **204 m** |

The text gives the two legs as equal. Casson's identifications make the second 41
per cent longer. One stadion value cannot satisfy both. He is aware of the strain
on the northern leg: "Schoff puts Tyndis at Ponnani, which is somewhat short of
500 stades, while others put it at Kadalundi near Beypore (11°10'N), which is
somewhat over; the odds are slightly in favor of Ponnani."

Three readings, not exclusive. One or more identifications is wrong. The two legs
ran through different amounts of backwater. Or the author was simply not being
precise, which is what the rounding structure in 2.1 supports.

### 2.5 "By river and sea" — the single most consequential textual finding

The Periplus does not say the Malabar distances were sailed along the coast. It
says they were *διά τε ποταμοῦ καὶ διὰ θαλάσσης*, "by river and sea."

> "Muziris, of the same Kingdom, abounds in ships sent there with cargoes from
> Arabia, and by the Greeks; it is located on a river, distant from Tyndis **by
> river and sea** five hundred stadia, and up the river from the shore twenty
> stadia." — Schoff 1912

> "Nelcynda is distant from Muziris **by river and sea** about five hundred
> stadia." — Schoff 1912

Schoff draws the inference: "This can hardly refer to anything but the Cochin
backwaters."

Every distance measurement made for Tyndis, Muziris and Nelkynda, ours included
and every one in the modern literature, uses a straight line or an open-sea
coastal track. The text describes a route running partly through the Vembanad
backwater system. The correct measurement follows the channels, and the channels
have moved.

This also softens an inconsistency previously treated as fatal. No Nelkynda and
Bakarē pair satisfies both the 500-stadia and the 120-stadia notices under
straight-line measurement. If the 500 stadia runs through the backwaters, the
straight-line figure understates it, and candidates excluded as too far south may
sit at the correct distance along the water.

### 2.6 Straight-line against sailed distance is still unresolved

Every distance argument in this literature compares a straight line against a
distance the text records as sailed. Measuring along every vertex of the modern
coastline roughly doubles the figure — Ponnani is 75 km straight and 155 km by
coastline vertices — but that path follows every estuary and no vessel would.
The true value sits between and nearer the low end. **Distance results should
therefore be stated as rankings, not as fits.**

### 2.7 The stadion is not a length. It is a speed

Casson's Appendix 2 states how the figures were made: "The ancients never
actually measured distances at sea, for they lacked the means... Their rule of
thumb was 1000 stades to a day-and-night run, 500 to a day's run." He does not
carry that through, but the text confirms it. **All nine stadia figures at or
above 2000 are exact multiples of 1000**, with no exceptions, which is 2, 2, 2,
3, 3, 4, 4, 7 and 12 whole day-and-night runs. 79 per cent of all 33 values
carry one significant figure, and the only two-figure mantissas anywhere in the
text are 12, 15 and 18.

**The conventional stadion is an artefact of the same rule.** Casson writes
"approximately ten stades correspond to a nautical mile," which is 1852/10 =
185.2 m exactly. The figure the field uses was never measured from the text.

Computed leg by leg from his own numbers — his transcription of the stadia, his
measurements in nautical miles, his identifications fixing the endpoints —
**the legs of his Appendix 2 accuracy tables imply a stadion running from
96.5 m to 217.6 m, a 2.3-fold range**. Every endpoint in those nine is a
securely located place, so the scatter cannot be blamed on misidentification.
Adding the Indian legs he assesses in prose takes the range to 277.8 m.
Figure `09_implied_stadion.png`, built by `src/make_implied_stadion.py`, plots
the eight legs for which Casson states a single figure. Malaō to Cape Elephas
is excluded because the Periplus gives one of its sub-legs as "two, perhaps
three, runs", so Casson prints 3,000–3,500; its range sits inside the others and
leaving it out changes nothing.

Read as a speed rather than a length, those same values are daily runs of 26 to
59 nautical miles, which is the ordinary range for a square-rigged merchantman
between coasting into a headwind and running with the monsoon. **The scatter is
the wind.** That connects the textual stream directly to the voyage simulation
rather than leaving them as separate chapters.

### 2.8 Four further problems in Casson's use of the distances

1. **His stated error bounds are violated by his own numbers.** He says short
   legs are "either exact or at most twenty percent off"; Okēlis to Eudaimōn
   Arabia is 26.3 per cent off. He says long legs run 25 to 50 per cent high;
   Adulis to Avalitēs is 92 per cent high. The two Indian legs are
   *under*estimates of 33 and 22 per cent, breaking the rule in the region that
   matters most here.
2. **The claim that error grows with distance barely survives his own data.**
   Regressing log error on log stated distance across his eleven legs gives a
   slope of +0.067 and r = +0.24. There is essentially no relationship.
3. **The Malabar legs never appear in the appendix where he tests accuracy.**
   They are in Appendix 1 only. Tyndis to Muziris implies a 144.5 m stadion and
   a 28 per cent error, which violates his own short-leg bound; Muziris to
   Nelkynda implies 203.7 m.
4. **The cumulative argument is circular.** He validates the whole African route
   by comparing his stadia total against the real distance "Abu Sha'r to the
   vicinity of Dar es Salaam." Abu Sha'ar has since been rejected as Myos
   Hormos, and Rhapta at Dar es Salaam is the disputed thing being assumed. His
   own hedge on the Rhapta endpoint, 75 miles, is half his claimed 5 per cent
   accuracy. Separately, error cancellation in a sum is not accuracy: his legs
   range from 15 per cent low to 92 per cent high, so a 5 per cent total shows
   the errors are roughly mean-zero and says nothing about any single leg.

### 2.9 What the error structure means for locating anything

The error is multiplicative, with **sd of log(stated/actual) = 0.311** across
Casson's eleven legs. A 500-stadia leg at a 155 m stadion is 77.5 km, with a
68 per cent band 49 km wide and a 95 per cent band 100 km wide. Candidates for a
single Kerala port sit 25 to 150 km apart, so **one 500-stadia leg cannot
separate adjacent candidates**. The 120-stadia Nelkynda-to-Bakarē figure has a
68 per cent band only 12 km wide.

That is the quantitative form of the finding in 2.1: the short local numbers
outrank the long ones, and now there is a number attached.


---

## 3. The archaeological record

### 3.1 What was extracted

Searching *Indian Archaeology: A Review* for candidate names only finds sites
somebody had already connected to a Periplus port, and a site can be excavated
without anyone making that connection. So the whole state sections were lifted
instead.

**7,053 numbered entries** from 78 volumes covering 59 distinct years, 1953–54 to
2013–14, each with year, state, chapter, title, district, body and a period
classification derived from its own text. `data/processed/iar_entries.csv`, built
by `src/extract_iar_entries.py`.

This makes the question regional rather than site-by-site: not "has anyone dug at
Ponnani" but **"what has been found on this coast, of what date, since 1953."**

### 3.2 Kerala in full

308 entries fall in Kerala state blocks; 238 are confirmed by naming a Kerala
district; **75 of those sit in the fieldwork chapters** rather than in
conservation, epigraphy or chemistry. Entries can carry more than one period, so
shares exceed 100 per cent.

| Period | Entries | Share |
|---|---|---|
| Megalithic / Iron Age | 47 | 63% |
| Medieval | 25 | 33% |
| Early medieval | 14 | 19% |
| Mesolithic | 7 | 9% |
| Palaeolithic | 7 | 9% |
| **Early Historic** | **4** | **5%** |
| Neolithic | 2 | 3% |
| Islamic / colonial | 2 | 3% |

**Four entries in sixty-one years mention material of Periplus date.** In full:

- **1969–70, no. 18, Excavations at Cranganore, District Trichur.** The Southern
  Circle with the Kerala Department under K.V. Soundara Rajan excavated at
  Karuppadana, Kilattali, Mathilakam, Tirukkulasekharapuram and Tiruvanjikulam.
  Everything recovered was ninth to eleventh century.
- **1970–71, no. 24, Exploration in District Malappuram.** K. Chandrasekharan
  found umbrella stones at Alancode, Koduvayur, Melmuri, Parnundam and Ozhur;
  menhirs at Ananthavoor and Thirunavaya; urn burials at Alancode; and a laterite
  rock-cut cave at Kuttippala yielding a red-slipped bowl painted with
  Russet-coated ware.
- **1970–71, no. 26, Exploration in District Trichur.** Records that the
  Cranganore trial digs "had not yielded any tangible evidence," and reports the
  discovery **in Taluk Ponnani** of Russet-coated (wavy line) Painted Ware,
  "which overlaps with the megalithic Black-and-red Ware in the early centuries
  of the Christian era," calling it "of great significance."
- **2008–09, no. 29, Excavation and exploration at Pattanam, District Ernakulam.**
  The KCHR excavation.

Two of the four are Russet-coated Painted Ware in the Ponnani and Malappuram
area, reported in consecutive entries of the same volume. One is a negative
result at Cranganore. One is Pattanam.

So in the complete national record for Kerala, **Early Historic material has been
reported from essentially two places: Pattanam, and the Ponnani–Malappuram
area.** That is a stronger statement about Tyndis than any number of individual
absences at named villages, and it was invisible to a name-matched search because
the 1970–71 entries are filed under districts, not under Ponnani as a site.

### 3.3 Kerala is not under-investigated; it is under-yielding

Normalising fieldwork entries by state area:

| State | Fieldwork entries | Early Historic | EH share | Entries per 10,000 km² |
|---|---|---|---|---|
| Tamil Nadu | 595 | 83 | 14% | 45.7 |
| **Kerala** | **91** | **8** | **9%** | **23.4** |
| Andhra Pradesh | 381 | 23 | 6% | 23.4 |
| Karnataka | 345 | 87 | 25% | 18.0 |
| Gujarat | 305 | 69 | 23% | 15.6 |
| Maharashtra | 442 | 103 | 23% | 14.4 |

Kerala sits mid-range for intensity, above Gujarat and Maharashtra per unit area.
What is distinctive is the yield: an Early Historic share of 9 per cent against
23 to 25 per cent for Maharashtra, Gujarat and Karnataka.

The honest formulation is not that Kerala has been neglected. It is that Kerala
has been investigated at an ordinary rate and has produced markedly less Early
Historic material than comparable states. Whether that reflects preservation
conditions, the laterite geology, the concentration of effort on megalithic
burials, or a genuine difference in first-century settlement is a real question
and this extraction does not settle it.

*(The 8 and 91 come from state-block totals; the 4 and 75 above come from the
subset additionally verified by district name. The table is for comparison
between states, where the same method applies throughout.)*

### 3.4 Absence is mostly absence of excavation

**Thirteen of the twenty-two disputed candidates have never been excavated.**
Niranam, Neendakara, Purakkad, Pirakkad and Thevalakara have **zero appearances**
across 59 years. Kallada has one, for a neolithic axe.

| Disputed port | Candidates | Excavated | Material in the corpus |
|---|---|---|---|
| Tyndis | Ponnani, Tanur, Kadalundi, Koyilandy | none | none |
| Nelkynda | Niranam, Kottayam, Kollam, Neendakara | Kollam only, medieval levels | none of Periplus date |
| Bakarē | Purakkad, Kallada, Thevalakara | none | none |
| Leukē Kōmē | Aynuna, al-Wajh, al-Qusayr | Aynuna only, 5 seasons | Aynuna only |
| Rhapta | Rufiji, Mafia, Pangani, Dar es Salaam | Rufiji and Mafia, test trenches, dating contested | contested |
| Barbarikon | Banbhore | 30 seasons, published sequence is Islamic-period Daybul | thin for the Periplus horizon |

**Consequence worth stating plainly: for the three Malabar ports, material
evidence can only ever be corroborative.** It can confirm a location proposed on
other grounds if someone digs there. It cannot select among candidates now. The
argument for those three has to be carried by distance and coastal geomorphology,
with material culture used to show the chosen candidate is at least not
contradicted.

### 3.5 Two tested negatives, which are a different thing from untested absence

- **IAR 1978–79 no. 40.** The ASI Southern Circle explored Malappuram and Palghat
  "while investigating for the sites showing **Roman contact in the Ponnani
  valley**," recording megalithic topikal burials at Alancode, Ongallur,
  Ponumundum, Tennala, Thannairkod and Thavanur, and menhirs near Thirunavaya.
  No Roman material.
- **IAR 1969–70 no. 18.** A traditional identification tested and failed. Five
  localities around Cranganore excavated; all material ninth to eleventh century
  Chera. The next volume records the trial digs "had not yielded any tangible
  evidence."

### 3.6 Excavation is blocked by water, not by absence, at several sites

At Banbhore, Khan's trenches (1958–66) never reached virgin soil: "the virgin
soil was not reached due to heavy water infiltration, and information on the
early stages of life at Banbhore remained incomplete" (Felici et al.). The
Italian mission has not reported reaching it either. Mughal 2018 (*Pakistan
Archaeology* 33) publishes Red Polished Ware of the first century BC to second
century AD from the earliest reached levels. The same water-table problem holds
at Sumhuram and Myos Hormos.

The decisive fact at Banbhore is not what was recovered but that the trenches
stopped at the water table, which changes the meaning of everything above them.

### 3.7 No counterpart series exists outside India

*Indian Archaeology: A Review* has no equivalent for Arabia, Pakistan or East
Africa. For **Leukē Kōmē, Barbarikon and Rhapta** the equivalent has to be
assembled by hand from excavation reports and from the expeditions named in the
dossier passages: who dug, when, how many seasons, what depth or period was
reached, whether virgin soil was hit, and where it was published.

---

## 4. Material assemblages

### 4.1 The typology comes first

Roberta Tomber's *Indo-Roman Trade: From Pots to Pepper* (Duckworth 2008)
supplies the controlled vocabulary. Her central warning is that much of the
pottery called "Roman" in older Indian reports is nothing of the kind. Torpedo
jars are Mesopotamian; Rouletted Ware and Red Polished Ware are Indian and were
misread as Roman because of their slip. Until every report is mapped onto one
vocabulary, "Roman pottery at X" and "Dressel 2-4 at Y" cannot be compared at
all. `data/raw/ware_typology.csv`, 43 classes.

Three classes carry real locational weight:

- **Coarse Red-slipped Ware with bamboo wiping.** In 2003 Tomber matched the
  internal tool marks on Red Sea cooking pots to the "scooping" technique still
  used by potters in North Kerala, and then to Pattanam. The tightest physical
  link between the Malabar coast and Egypt in the corpus.
- **Torpedo jars.** Bitumen-lined Mesopotamian wine jars, mostly Sasanian
  (AD 224–651), and not positively identified on any Red Sea site. Their presence
  points to Gulf traffic and to a date after the Periplus, not to Rome.
- **Black pepper.** Sourced tightly to Malabar, but over 95 per cent of all
  archaeological pepper comes from Egypt's Eastern Desert, so its distribution
  maps preservation conditions rather than trade.

### 4.2 Pattanam, the only quantified candidate

From P.J. Cherian's KCHR excavations, 2007–2011, *Tamil Civilization* 24.1–2,
Tables 1–2. Every row re-added and checked.

| Class | Sherds | Share of all ceramics |
|---|---|---|
| Local coarse pottery | 3,537,464 | 99.45% |
| Rouletted Ware (Indian) | 8,534 | 0.240% |
| Roman amphora | 6,029 | 0.169% |
| Torpedo jar (Mesopotamian) | 3,098 | 0.087% |
| Turquoise Glazed Pottery (Mesopotamian) | 1,527 | 0.043% |
| Terra sigillata | 122 | 0.003% |
| **Total** | **3,557,118** | |

Two things follow. Pattanam's Roman material is enormous by regional standards:
Wheeler's 1945 excavation at Arikamedu, the type site for Indo-Roman contact,
produced 116 amphora sherds and 38 of sigillata, so Pattanam exceeds it roughly
fiftyfold. And, less often said, Roman wares are 0.17 per cent of the assemblage
while Mesopotamian wares together (4,625 sherds) come to three-quarters of the
Roman total. Since torpedo jars are largely Sasanian and absent from Red Sea
sites, a substantial part of Pattanam's imported pottery records Gulf traffic of
the third to seventh centuries, not Mediterranean traffic of the first.
**Pattanam was a port for much longer than it was Muziris.**

### 4.3 How the extraction was done and how well it worked

A miner scans all 96 library texts for a site name and an artefact class in the
same sentence, binds any quantity to the nearest artefact mention, and records
the verbatim sentence and page. It proposes; it does not decide. Of 1,217
proposed statements, 30 carried a quantity and all 30 were read: **13 accepted,
2 recoded, 15 rejected.**

The rejects show why this cannot be fully automated. PDF extraction inlines
superscript footnote markers, so "Sri Lanka.180 There were also beads" parses as
180 beads. Ware names contain digits, so "Dressel 2-4" parses as four amphorae.
Page ranges in footnotes parse as counts. And comparative sentences attach one
site's finds to another: "three rim sherds clearly resemble Type 1 from
Arikamedu" describes Pattanam. Masking type numerals, dates, measurements,
footnote markers and running headers, requiring an explicit unit, and binding
counts to the nearest ware raised usable precision from about 28 per cent to 50
per cent. The remaining errors are semantic and need a reader.

---

## 5. Coins

### 5.1 Roman coins in India do not mark ports

Of 121 Indian hoards in the Coin Hoards of the Roman Empire database, 98 lie more
than 25 km from the coast, and they account for **73 per cent of all recorded
coins**. The densest concentration is 100–200 km inland — 4,802 coins in 29
hoards — in Coimbatore district and the Palghat gap. It holds at the Periplus
horizon: of 40 hoards closing AD 1–69, 76 per cent of coins are inland.

Roman coins in India travelled inland towards the sources of pepper and beryl and
were buried there. They record the movement of bullion and the habit of hoarding,
not the location of harbours.

*Source: `data/processed/chre_hoard_distances.csv`, 627 hoards and 10,813
individually recorded coins.*

### 5.2 Sri Lanka is the opposite case and must not be pooled

67 hoards, 220,901 coins, 85 per cent coastal. But these are enormous late-Roman
**bronze** hoards of the fourth and fifth centuries — Beragama 70,000, Godavaya
30,000, Tissamaharama 30,000. Aggregating them with Indian Julio-Claudian gold
produced a completely misleading first result.

### 5.3 Hoards and site finds are different evidence classes

India: 790 gold, 184 silver, almost no bronze; 756 aurei, 180 denarii. Aynuna,
the only excavated Arabian assemblage: 24 bronze, 1 silver. The first is stored
wealth, the second is money being spent. For locating a harbour the second is far
more informative, and it is precisely the category the hoard databases omit.

Indian Roman coins occur overwhelmingly as hoards and rarely in excavation; the
Red Sea is the reverse.

### 5.4 Coverage gaps are structural, not search failures

CHRE has **no country entry for Tanzania, Kenya, Somalia or Ethiopia**. Nearest
hoard to any Rhapta candidate: 2,100–2,400 km. To Banbhore: 406 km. To Aynuna:
207 km. To Myos Hormos: 143 km.

Crossref was queried for numismatic publications at every site CHRE does not
reach (`src/query_coin_literature.py`, 110 hits, 41 naming a relevant place).
**Nothing site-specific exists for** Ras Hafun, Ptolemais Theron, Charax
Spasinou, Xiis, Chandraketugarh, Tamluk, Dwarka, Nagara, Madayipara, Pangani,
Dar es Salaam or Fukuchani. That is itself the answer: nobody has published coins
from them.

Every coin recorded at a Rhapta candidate is Islamic or later. Unguja Ukuu:
eighth-century Muslim gold found in 1866, later silver, a Chinese Northern Song
bronze. Kilwa: sultanate coins c. 1200–1400. Mafia: medieval coins from Kisimani
Mafia.

### 5.5 Indian reign distribution is bimodal

985 specimens. Claudius 134, Tiberius 116, Augustus 114, Nero 92, for 456
Julio-Claudian, then a second peak at Hadrian 116 and Antoninus Pius 75.

### 5.6 What we hold

`data/processed/site_find_coins.csv`, 30 records: Aynuna's 25 excavated coins
plus assemblage totals for Myos Hormos, Berenike and Sumhuram. Smagur 2025 in
*JRA* supplied Myos Hormos: 153 coins plus a lead token from the Chicago
excavations of 1978–82, with the striking detail that the 1999–2003 Southampton
excavations produced only 14 coins identifiable enough to publish.

**Aynuna is the one disputed candidate with real excavated coins.** Pattanam has
hoard evidence nearby, PARUR's 1,000+ gold coins 3 km away. Every other disputed
candidate has nothing, and for the East African ones there is nothing to find.

---

## 6. Later settlement, and the circularity it reveals

`data/raw/later_settlement.csv`, 20 sites with attested occupation after the
Periplus horizon, each with period range, evidence, confidence grade and source.
Eleven graded high, five medium, four low.

**Every Kerala candidate for Tyndis, Nelkynda and Bakarē is a documented later
port with no first-century evidence whatever.** Koyilandy is Panthalayani Kollam,
named by Ibn Battuta, called Flandarina by Friar Odoric and Pandarani by the
Portuguese. Kollam gives its name to the Kollam era beginning AD 825. Beypore
built ocean-going *uru* into the twentieth century. Kodungallur held a Portuguese
fort from 1523.

That is a finding about how the candidate lists were built. These places were not
proposed because anything Roman was found at them. They were proposed because
they are known harbours in medieval and early modern sources, and the
identification was projected backwards onto a first-century text.

It cuts both ways and the thesis should say both.

- **For.** Continuity is genuine evidence of viability. A river mouth that
  supported a port for a thousand years was probably usable in the first century,
  and absence of early material at a site buried under a medieval and modern town
  is close to uninformative. The stated reason Ponnani, Kodungallur and Kollam
  have never been dug is that a living town sits on them.
- **Against.** "Medieval port, therefore ancient port" does not follow.
  Coastlines prograde, rivers switch channels, and the Malabar harbours that
  mattered in AD 1400 need not be the ones that mattered in AD 50. **Kodungallur
  is the warning**: excavated in 1969–70 precisely because it was the traditional
  Muziris, and it returned nothing earlier than the ninth century.

Exceptions worth noting. Kallada, Thevalakara, al-Qusayr, Fukuchani and the
Rufiji delta have no attested later occupation either; they are candidates on
topographic or textual grounds alone. **Aynuna reverses the Kerala pattern**:
real Periplus-horizon evidence and only limited later material. It was a port at
the right date and then stopped being one, which is why it can be excavated at
all. Banbhore has both, and that is its problem.

---

## 7. Port by port

### Leukē Kōmē

A harbour in Nabataean territory with a customs post and a Roman garrison. Two
candidates on the north-west coast of Saudi Arabia: **Aynuna** near the head of
the Gulf of Aqaba, excavated by a joint Saudi–Polish mission 2014–2018, and
**al-Wajh** about 200 km south, argued from sailing distance from Egypt.

The standard treatment is Nappo 2010 in *JRA*, arguing for Aynuna from the
distance to Myos Hormos. **Nappo measured from Abu Sha'ar**, now generally
rejected as Myos Hormos, which is placed at Quseir al-Qadim. Measured from Quseir
al-Qadim, Aynuna lies 236 km away and al-Wajh 222 km, and **both fall inside
Nappo's own 185–278 km window**. The distance argument does not discriminate.

The material does. Aynuna produced harbour installations, a large storehouse and
two cemeteries, all Nabataean, plus **25 coins, 24 of them bronze**, from Obodas
III and Aretas IV through to Tiberius, dating between the second century BC and
about AD 40. Bronze lost in occupation layers is small change in daily use: the
signature of a working harbour at exactly the Periplus horizon.

Al-Wajh has never been excavated, but it is a **tested negative rather than an
untested absence**. Ingraham's 1981 survey found a coin findspot about a
kilometre from the proposed site consisting of three late Roman *nummi* of
Maximianus struck in AD 295 or 296, with a second findspot nearby holding three
of Constantine I from the AD 320s. Two and a half centuries too late.

This is the one disputed port where material evidence settles something, and it
does so for a better reason than the distance argument usually cited.

### Barbarikon

> "Smith prudently observes that 'the **extensive changes which have occurred in
> the rivers of Sind** during the course of eighteen centuries **preclude the
> possibility of satisfactory identifications** of either of these towns
> [Barbarikon and Minnagar].'" — Casson 1989

The field does not regard this as settled. Felici et al. hedge even on *Daybul*,
the Islamic identification, which is far better attested than the Roman one.
Mughal 2018 writes that Banbhore "**could be identified** with the famed port
city of Barbarikon"; his editor's preface says the study "establishes and
identifies." The hedge belongs to the author.

**Minnagar is a separate and unsolved problem.** The Periplus ties Barbarikon to
an inland capital to which cargoes were taken upriver. Cunningham put Minnagar
near Tatta, Müller at Indore, Vincent Smith at Madhyamika near Chitor, McCrindle
and Fabricius in Kathiawar; McCrindle cites three further identifications. These
are hundreds of kilometres apart. Locating Barbarikon and locating Minnagar are
the same problem, and the second is in worse shape.

### Tyndis

Five hundred stadia north of Muziris, by river and sea. "A village in plain sight
on the shore."

> "The exact location of the port is still unknown; however, scholars have tried
> to identify this place with either modern day **Kadalundi or Ponnani or
> Pantalayani Kollam**." — Dayalan 2018

> "It is described as a village in plain sight on the shore, and may be
> identified with the modern **Ponnani** (10° 48' N., 75° 56' E.)." — Schoff 1912

> "there is fairly good evidence for locating Muziris near Cranganore, **Tyndis
> near Ponnani or Beypore**, Bakare near Pirakkad with Nelkynda some twelve miles
> inland." — Casson 1989, Appendix 1

> "Less important was Tyndis (= Tamil **Toṇḍi** = Ponnāni?), located some 500
> stadioi north of Muziris." — De Romanis

**An independent constraint usually overlooked.** Casson: "Ships sailing down the
coast came first to the Chera kingdom, whose northern border was just above
Tyndis and whose southern was somewhere between Muziris and Nelkynda, in modern
terms, **north of Ponnani and south of Cranganore**." Tyndis sits at or just
inside a political boundary, not merely at a distance.

Casson allows Ponnani *or Beypore*, 40 km apart. Schoff commits to Ponnani on the
distance. De Romanis marks it with a question mark. Nobody measures through the
backwaters, which is what the text specifies.

### Nelkynda and Bakarē

These must be treated as a pair. Nelkynda lies 500 stadia from Muziris by river
and sea; Bakarē is its harbour, "**120 stades downriver at the mouth**" (Casson,
Appendix 1).

Schoff puts Nelkynda at Kottayam on the Minachil and Bakarē at Purakkad,
claiming "**the distance from Kottayam is exactly in accord with the text**."
That does not survive measurement: Kottayam to Purakkad is 29.6 km straight,
against 18.6 km at a 155 m stadion or 22.2 km at 185 m.

Casson's own alternative is stronger: "The suggestion that Nelkynda was
**Niranom (Neranom)**, which is about 500 stades from Muziris and which is on the
Pambiyar twelve miles east of Pirakkad, at least puts the port of trade and its
harbor **on the same stream and the proper distance from each other**." Twelve
miles is 19.3 km, almost exactly 120 stadia at 155 m. Our own measurement of
Niranam to Purakkad gives 21.2 km.

**The contradiction.** The pair constraint picks Niranam–Purakkad at 21.2 km,
but the coastal distance from Muziris rejects Niranam at 106 km against a
72–102 km band. This is precisely what the backwater measurement in 2.5 may
dissolve.

De Romanis places "Becare-Nelkynda, located on a river that flowed **less than
500 stadioi south of Muziris**, pointing to a place in **the southern part of
Vembanad Lake**." Casson notes the consensus that the names are versions of
**Kuttanadu**, the Pambiyar valley, "noted for its fine pepper."

Casson also counts Bakarē among the *securer* identifications — "Five names —
Semylla, **Muziris, Bakare**, Red Mountain, Komar — can be identified with more
confidence than the others" — which is at odds with how unsettled the modern
discussion looks. And he flags the standing caveat: "A further complication is
that **extensive changes have taken place in the coastline**."

**Candidates still to add**, from Dayalan: Nakkada near Niranam, Nirkunnam,
Kannetri, Markari, Varakkai, and Beypore as a point separate from Kadalundi.

### Muziris

> "Muziris ... **is securely located, thanks to mention in Tamil literature**: a
> poem ... talks of the city where the beautiful vessels, the masterpieces of the
> Yavanas, **stir white foam on the Periyar**, river of Kerala." — Casson 1989

Note what this secures and what it does not. The Tamil poem places Muziris on the
Periyar. It does not place it at Pattanam rather than Kodungallur, which are 9 km
apart on the same delta. And the identification has moved a long way before:
Schoff records that "the earlier identification of Muziris and Nelcynda placed
them at **Mangalore and Nileshwar**," 300 km north of the modern consensus.

### Rhapta

The last market town on the African coast, two days' sail beyond an island called
Menuthias, called a metropolis. Ptolemy repeats the name. Nothing else survives.

The modern debate begins with Datoo 1970 in *Azania*, which narrowed the location
to the coast between the Pangani and Rufiji mouths, favouring the north. Every
later argument inherits this bracket. Mathew argued for the Pangani mouth;
Chittick and later Chami for the Rufiji delta, with Chami additionally reporting
submerged structures off Mafia Island. Hughes 2016 attempted a GIS approach.

The Periplus places Menuthias 300 stadia off the mainland, about 46.5 km at 155 m.
Measured island shore to mainland shore, **that favours Pemba at 42.9 km**
against a target of 46.5, not Zanzibar at 30.7 or Mafia at 14.8. (An earlier
version of this analysis claimed Zanzibar; that was wrong and is corrected here.)

The one claim of Periplus-period material is Chami's report of Roman glass beads
from the Rufiji delta, *Current Anthropology* 1999, "First Incontrovertible
Archaeological Link with the Periplus." It is the most cited archaeological claim
about Rhapta and its stratigraphy has been questioned.

One lead worth chasing. Juma 2004 (p. 24) writes that Rhapta "may be anywhere
between the Rufiji delta area, where ancient trade goods including Roman beads
have been excavated and further north, where a number of fortuitous discoveries
of **early Roman coins** have been made so far." Early Roman coin finds north of
the Rufiji would be the first Roman numismatic evidence on the Tanzanian coast.
He gives no reference.

---

## 8. Errors found

### In published sources

1. **CHRE georeferencing error.** Kottayam 1847 (74 aurei) is placed at 9.591 N,
   76.522 E in central Kerala, on top of a Nelkynda candidate. Its own county
   field says **Kannur** and its summary says "on the slope of a hill by the sea."
   Central Kottayam is about 35 km inland behind the backwaters. Wrong by roughly
   260 km. Worth reporting to CHRE. Excluded from our analysis.
2. **Arithmetic error in Cherian 2012 Table 1.** The ring-stones row reads
   0, 0, 0, 15, 9 with a printed total of 15. The seasons sum to 24. The printed
   grand total of 48,862 antiquities uses 15, so the error is in the row.
3. **Irreconcilable Pattanam figures.** Torpedo sherds 3,098 (Cherian, to 2011)
   against "about 398" (a later summary, to 2014). Glass 1,338 (to 2011) against
   "about 906" (to 2014). Both report *fewer* over a *longer* window. Recorded in
   the `note` field rather than silently reconciled.
4. **Nappo's Leukē Kōmē distance measured from the wrong port** (see §7).

### In our own work, corrected

1. Claimed Ponnani fits Tyndis "to within 2.5 km." That compared a straight line
   against a sailed distance. Only the ranking survives.
2. Claimed the 300-stadia Menuthias notice favours Zanzibar. Measured island
   shore to mainland shore it favours **Pemba**.
3. Claimed al-Wajh had a rival coin hoard. It is three nummi of AD 295.
4. Claimed *Pakistan Archaeology* was not online. It is, at doam.gov.pk.
5. Built a Barbarikon distance argument on a mis-extracted endpoint: the text
   says the promontory Papica, not Astakapra.
6. **Archive.org OCR is unusable for IAR.** The Digital Library of India scanned
   the volumes with a Devanagari OCR model, so English came out as mojibake. An
   early search over that derived text falsely showed every Kerala candidate
   absent from 59 years of reporting. Artefact, discarded. The PDFs carry a clean
   English text layer and were re-extracted from directly.
7. **Three IAR extraction bugs**, each of which changed the answer. "MADHYA
   PRADESH" carries three internal spaces, so the boundary regex missed it and
   Madhya Pradesh districts were absorbed into the Kerala block; six of eight
   apparent Kerala Early Historic entries were from Sagar, Vidisha, Chhatarpur,
   Dhar, Gwalior and Sehore. The born-digital volumes use two columns, titles
   broken across lines and a colon rather than an em-dash terminator, which hid
   Pattanam. And the first entry of every block was dropped because the pattern
   required whitespace after the separator, which silently removed the Cranganore
   excavation.
8. **Crossref search is token-based, not phrase-based.** "Mafia Island" returns
   182,000 works, mostly organised crime; "Quseir al-Qadim" 1.5 million. Raw hit
   counts are useless as an attention metric.

---

## 9. Open questions, not yet run

1. Per-leg implied stadion. Does it drift by region, leg length or leg type?
2. Malabar distances measured through the backwaters rather than the open coast.
3. Metal composition across all 627 hoards, not two sites.
4. Does the centroid of hoarding move between the first and fourth centuries?
5. Is the Pattanam assemblage stable across seasons, or do ware ratios shift?
6. Where has Indian archaeology worked by decade, and does it follow anything
   other than modern accessibility?
7. Does the text's own emphasis — designated harbours, goods listed, partners —
   predict archaeological visibility?
8. Ware co-occurrence: which classes travel together?

---

## 10. Maps that would serve these

Built: the six-port overview, the Malabar distance bands, and seven per-port
panels.

Still to build, in order of value:

1. **Excavation-coverage map of every Periplus port**, secure and disputed. The
   denominator for any claim about absence, and the visual form of the detection
   model. Extend to the whole basin to show that confidence decays eastward along
   the route.
2. **Implied-stadion route map.** Each leg coloured by the stadion its stated
   distance implies. Serves question 1; the result is not guessable in advance.
3. **Candidates by excavation status**, all 23 on one basin map. The simplest and
   most honest summary of where the field actually stands.
4. **Hoard map shaded by gold fraction**, and a second faceted by closing date,
   with the Palghat corridor drawn. Serves questions 3 and 4.
5. **Indian fieldwork by decade**, small multiples from the *Review* run. Serves
   question 6.
6. **Coastline displacement per port**, which is really a map of how wide each
   search window has to be.

Built since: `09_implied_stadion.png`, the stadion implied by each of the nine
legs in Casson's accuracy tables, with the conventional 185.2 m drawn as a
line and a second axis reading the same quantity as a day's run in nautical
miles. The disputed ports are deliberately absent, since plotting a Malabar leg
would assume the identification in question.
