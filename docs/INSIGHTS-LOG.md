# Insights log

Running record of what the data has actually shown. Working notes, not prose.
Each entry says what was measured, on what, and what is still unverified.
Structure comes later.

---

## A. The Periplus as a measuring instrument

**A1. The text rounds large distances and not small ones.**
33 of 51 distance statements are in stadia. **82% are multiples of 100.** Every
value at or above 200 is a round hundred, without exception. The only unround
figures are 20, 60 and 120, all small and all local (20 stadia upriver at
Muziris, 120 stadia upriver at Nelkynda, 60 elsewhere).
→ Two classes of number with different precision. Large coastal legs are
estimates to the nearest hundred; short local measures may be direct knowledge.
→ **Implication: the upriver notices deserve more weight than the 500-stadia
legs. That is the reverse of how the literature uses them.**
*Source: `data/processed/distances.csv`.*

**A2. Most distance statements are not sailing legs.**
Only 22 of 51 are legs between ports. The rest: 7 inland, 5 offsets, 5 extents,
5 widths, 3 upriver, 2 runs. 18 of 51 are in days rather than stadia.
→ Any treatment of the Periplus as a list of sailing distances is using under
half the corpus.

**A3. The stadion calibrates to ~155 m, not the conventional 185 m.**
Median of four legs with securely identified endpoints. Shifts every derived
position by ~16%.
→ **Not yet done: per-leg values rather than a single median.** Whether the
implied stadion drifts by region, leg length or leg type is question 1 and is
the highest-value unrun analysis we have.

**A4. Straight-line vs sailed distance is an unresolved methodological gap.**
Every distance argument in this literature, ours included, compares a straight
line against a distance the text records as sailed along a coast. Measuring
along every vertex of the modern coastline roughly doubles the figure (Ponnani
75 km straight, 155 km by coastline vertices), but that path follows every
estuary and no vessel would. The true value sits between and nearer the low end.
→ Currently this means distance results should be stated as rankings, not fits.

---

## B. Numismatic patterns

**B1. Roman coins in India are inland.**
98 of 121 Indian hoards, and **73% of all recorded coins**, lie more than 25 km
from the coast. Densest concentration 100–200 km inland (4,802 coins in 29
hoards), in Coimbatore district and the Palghat gap. Holds at the Periplus
horizon: of 40 hoards closing AD 1–69, 76% of coins are inland.
→ Coins track bullion movement and hoarding, not harbour location.
*Source: `data/processed/chre_hoard_distances.csv`.*

**B2. Sri Lanka is the opposite and must not be pooled.**
67 hoards, 220,901 coins, 85% coastal. But these are enormous late-Roman
**bronze** hoards (Beragama 70,000; Godavaya 30,000; Tissamaharama 30,000),
4th–5th century. Aggregating them with Indian Julio-Claudian gold produced a
completely misleading first result.

**B3. Metal composition differs sharply by region.**
India: 790 gold, 184 silver, almost no bronze; 756 aurei, 180 denarii.
Aynuna (only excavated Arabian assemblage): 24 bronze, 1 silver.
→ Stored wealth vs money in daily use. **Not yet tested across all 627 hoards.**

**B4. Hoards and site finds are different evidence classes.**
CHRE holds hoards only. Indian Roman coins occur overwhelmingly as hoards and
rarely in excavation; the Red Sea reverse. For locating a harbour, site finds
are the informative category and are precisely what the database omits.

**B5. Coverage gaps are structural, not search failures.**
CHRE has **no country entry for Tanzania, Kenya, Somalia or Ethiopia**. Nearest
hoard to any Rhapta candidate: 2,100–2,400 km. Nearest to Banbhore: 406 km. To
Aynuna: 207 km. To Myos Hormos: 143 km.

**B6. Indian reign distribution is bimodal.**
985 specimens: Claudius 134, Tiberius 116, Augustus 114, Nero 92 (456
Julio-Claudian), then a second peak Hadrian 116, Antoninus Pius 75.

---

## C. Material and excavation record

**C1. Absence is mostly absence of excavation.**
13 of 22 disputed candidates have never been excavated. Verified against 78
volumes of *Indian Archaeology: A Review*, 59 distinct years 1953–2014.
Niranam, Neendakara, Purakkad, Pirakkad, Thevalakara: **zero appearances**.
Kallada: one, for a neolithic axe.

**C2. One tested negative exists and it matters.**
IAR 1978–79 no. 40: ASI Southern Circle explored Malappuram and Palghat "while
investigating for the sites showing Roman contact in the Ponnani valley." Found
megalithic topikal burials at Alancode, Ongallur, Ponumundum, Tennala,
Thannairkod, Thavanur; menhirs near Thirunavaya. No Roman material.
→ Distinct from untested absence.

**C3. A traditional identification was tested and failed.**
IAR 1969–70 no. 18: ASI with the Kerala Department excavated five localities
around Cranganore. All material 9th–11th c. Chera. Next year's volume records
the trial digs "had not yielded any tangible evidence."

**C4. Pattanam's assemblage is 99.4% local.**
Total ceramics 3,557,118. Local 3,537,464 (99.45%). Rouletted Ware 8,534
(0.240%), Roman amphora 6,029 (0.169%), torpedo jar 3,098 (0.087%), TGP 1,527
(0.043%), terra sigillata 122 (0.003%).
→ Mesopotamian wares (4,625) are **three-quarters of the Roman total**. Torpedo
jars are largely Sasanian and absent from Red Sea sites, so a substantial part
of the imported pottery records Gulf traffic of the 3rd–7th c.

**C5. Scale contrast with the type site.**
Pattanam 6,029 Roman amphora sherds against Arikamedu's 116 from Wheeler's
excavation. Ratio ~52:1.

**C6. Every Kerala candidate is a documented later harbour.**
All 10 have attested medieval or early modern port activity; none has
first-century material. Koyilandy is Panthalayani Kollam (Ibn Battuta,
Flandarina of Odoric, Pandarani of the Portuguese). Kollam names the era
beginning AD 825.
→ Pattern about how candidate lists were assembled, not about antiquity.

**C7. Excavation is blocked by water, not absence, at Banbhore.**
Khan's trenches (1958–66) never reached virgin soil due to heavy water
infiltration; the Italian mission has not reported reaching it either. Mughal
2018 (*Pakistan Archaeology* 33) publishes Red Polished Ware of the 1st c. BC –
2nd c. AD from the earliest levels.

---

## D. Bibliographic structure

**D1. Extreme citation concentration.**
344 on-topic works. **60% have zero citations.** Top 10 hold 34% of all
citations; top 25 hold 58%. A handful of arguments carry the debate, and two of
them (Datoo 1970, Chami 1999) we still do not have.

**D2. Recent and accelerating.**
Fewer than 22 works before 1990. 102 in the 2010s, 115 already in the 2020s.

**D3. The palaeoenvironmental strand is new and growing.**
None before the 1990s. 5 (1990s) → 2 (2000s) → 10 (2010s) → 16 (2020s).
Approaching a third of current output on these landscapes.

**D4. The disputed ports have the *most recent* literature, not the least.**
Median publication year: Nelkynda 2023, Tyndis 2021, Barbarikon 2021, Muziris
2021, against Myos Hormos 2008 and Arikamedu 2005.
→ They are actively discussed. What is missing is fieldwork, not attention.

**D5. For some ports the literature is substantially encyclopaedic.**
Brill's New Pauly (9) and Der Neue Pauly (8) together account for 17 entries.
Genuine research venues: *Azania* 11, *Polish Archaeology in the Mediterranean*
9, *JRA* 8, *Antiquity* 7.

**D6. Regional asymmetry in what kind of work exists.**
Archaeology vs palaeoenvironment by port: Myos Hormos 24/0, Berenike 19/0,
Adulis 9/0, Muziris 8/0 — but Rhapta 13/12 and **Barbarikon 1/6**. Where a port
is undisputed the literature is archaeology; where disputed, the recent
fieldwork in that landscape is environmental science.

**D7. India has a systematic series; nowhere else does.**
We hold excavation reports from every region (Arabia 6, Yemen/Oman 4, Horn 4,
India 4, Egypt 3, Pakistan 2). What is India-only is the annual *Review*, which
is why "has anyone ever dug here" is answerable there and nowhere else.

---

## E. Errors found, in published sources and in our own work

**E1. CHRE georeferencing error.** Kottayam 1847 (74 aurei) is placed at 9.591 N,
76.522 E, central Kerala, on top of a Nelkynda candidate. Its own county field
says **Kannur** and its summary says "on the slope of a hill by the sea".
Central Kottayam is ~35 km inland behind the backwaters. Wrong by ~260 km.
Worth reporting to CHRE.

**E2. Arithmetic error in Cherian 2012 Table 1.** Ring stones row reads
0, 0, 0, 15, 9 with a printed total of 15. Seasons sum to 24. The printed grand
total of 48,862 uses 15.

**E3. Irreconcilable Pattanam figures.** Torpedo sherds: 3,098 (Cherian, to
2011) vs "about 398" (a later summary, to 2014). Glass: 1,338 (to 2011) vs
"about 906" (to 2014). Both report *fewer* over a *longer* window.

**E4. Nappo's Leukē Kōmē distance measured from the wrong port.** He used Abu
Sha'ar; Myos Hormos is now placed at Quseir al-Qadim. Recomputed, Aynuna (236
km) and al-Wajh (222 km) both fall inside his own 185–278 km window.

**E5. Archive.org OCR is unusable for IAR** but the PDFs carry a clean English
text layer. An early search over the derived text falsely showed every Kerala
candidate absent from 59 years of reporting. Artefact, discarded.

**E6. Crossref search is token-based, not phrase-based.** "Mafia Island" returns
182,000 works, mostly organised crime; "Quseir al-Qadim" 1.5 million. Raw hit
counts are useless as an attention metric.

**E7. Our own extraction precision.** Mined material counts went from ~28% to
50% usable after masking footnote markers, ware-type numerals, dates, page
ranges and running headers. The remaining errors are semantic.

**E8. Our own corrections.** (i) Claimed Ponnani fits Tyndis "to within 2.5 km";
this compared a straight line to a sailed distance, and only the ranking
survives. (ii) Claimed the 300-stadia Menuthias notice favours Zanzibar;
measured island-shore to mainland-shore it favours **Pemba** (42.9 km vs target
46.5; Zanzibar 30.7, Mafia 14.8). (iii) Claimed al-Wajh had a rival coin hoard;
it is three nummi of AD 295. (iv) Claimed *Pakistan Archaeology* was not online;
it is, at doam.gov.pk. (v) Built a Barbarikon distance argument on a
mis-extracted endpoint: the text says the promontory Papica, not Astakapra.

---

## F. Open questions, not yet run

1. Per-leg implied stadion. Does it drift by region, leg length, leg type?
2. Metal composition across all 627 hoards, not two sites.
3. Does the centroid of hoarding move between the 1st and 4th centuries?
4. Is the Pattanam assemblage stable across seasons, or do ware ratios shift?
5. Where has Indian archaeology worked by decade, and does it follow anything
   other than modern accessibility?
6. Does the text's own emphasis (designated harbours, goods listed, partners)
   predict archaeological visibility?
7. Ware co-occurrence: which classes travel together?

---

## G. Maps that would serve these

1. **Implied-stadion route map.** Each leg coloured by the stadion its stated
   distance implies. Serves F1. Highest value; result not guessable.
2. **Excavation-coverage map** of every Periplus port. The denominator for any
   claim about absence.
3. **Hoard map shaded by gold fraction**, and a second faceted by closing date.
   Serves F2 and F3.
4. **Indian fieldwork by decade**, small multiples from the *Review* run.
   Serves F5.
5. Seven per-port panels. Built.
