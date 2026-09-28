# Material evidence: what was extracted and what it shows

Step 2 of the plan. Three tables now exist, built from the 96 PDFs in
`library/` with Roberta Tomber's *Indo-Roman Trade: From Pots to Pepper*
(Duckworth, 2008) supplying the vocabulary that makes the rest comparable.

| File | Rows | What it is |
|---|---|---|
| `data/raw/ware_typology.csv` | 42 | The controlled vocabulary: every artefact class, its origin, date range and what its presence actually licenses you to conclude |
| `data/processed/material_observations.csv` | 48 | Verified counts. Each read against its source |
| `data/raw/site_survey_effort.csv` | 65 | How much digging has happened at each site — the denominator |
| `data/processed/material_candidates.csv` | 1,217 | Every machine-proposed statement, with verdicts. Kept so the error rate is auditable |

## Why the typology comes first

Tomber's central warning is that much of the pottery called "Roman" in older
Indian reports is nothing of the kind. Torpedo jars are Mesopotamian; Rouletted
Ware and Red Polished Ware are Indian and were misread as Roman because of
their slip. Until every report is mapped onto one vocabulary, "Roman pottery at
X" and "Dressel 2-4 at Y" cannot be compared at all. That is what the 42-class
typology does, and it is why it had to be built before any counting.

Three classes carry real locational weight:

- **Coarse Red-slipped Ware with bamboo wiping.** In 2003 Tomber matched the
  internal tool marks on Red Sea cooking pots to the "scooping" technique still
  used by potters in North Kerala, and then to Pattanam. This is the tightest
  physical link between the Malabar coast and Egypt in the whole corpus.
- **Torpedo jars.** Bitumen-lined Mesopotamian wine jars, mostly Sasanian
  (AD 224–651), and — Tomber emphasises — *not* positively identified on any Red
  Sea site. Their presence points to Gulf traffic, and to a date after the
  Periplus, not to Rome.
- **Black pepper.** Sourced tightly to Malabar, but over 95% of all
  archaeological pepper comes from Egypt's Eastern Desert, so its distribution
  maps preservation conditions rather than trade.

## The finding that matters

**Thirteen of the twenty-two candidate locations have never been excavated.**

| Disputed port | Candidates | Excavated | Material in the corpus |
|---|---|---|---|
| Tyndis | Ponnani, Tanur, Kadalundi, Koyilandy | none | none |
| Nelkynda | Niranam, Kottayam, Kollam, Neendakara | Kollam only, medieval levels | none of Periplus date |
| Bakarē | Purakkad, Kallada, Thevalakara | none | none |
| Leukē Kōmē | Aynuna, al-Wajh, al-Qusayr | Aynuna only (5 seasons) | Aynuna only |
| Rhapta | Rufiji, Mafia, Pangani, Dar es Salaam | Rufiji and Mafia, test trenches, dating contested | contested |
| Barbarikon | Banbhore | 30 seasons, but published sequence is Islamic-period Daybul | thin for the Periplus horizon |

For Tyndis, Nelkynda and Bakarē the material layer cannot discriminate between
candidates, because there is nothing to discriminate with. Not one of the eleven
Kerala candidates has a published excavation reaching Early Historic levels.
This is not a gap I can close by reading more carefully; it is a gap in the
archaeological record.

The consequence for the thesis is a constraint worth stating plainly: **for the
three Malabar ports, material evidence can only ever be corroborative.** It can
confirm a location proposed on other grounds, if someone digs there. It cannot
select among candidates now. The argument for those three has to be carried by
the distance and coastal-geomorphology evidence, with material culture used to
show that the chosen candidate is at least not contradicted.

Leukē Kōmē is the opposite case. Aynuna is the only candidate with an
excavation, so the material evidence is real but asymmetric — it tells you
Aynuna was a Nabataean port, not that al-Wajh was not.

## Pattanam

Pattanam is the only candidate site with quantified, published, season-by-season
finds tables, from P.J. Cherian's KCHR excavations (2007–2011, *Tamil
Civilization* 24.1–2, Tables 1–2). Every row was re-added and checked.

| Class | Sherds | Share of all ceramics |
|---|---|---|
| Local coarse pottery | 3,537,464 | 99.45% |
| Rouletted Ware (Indian) | 8,534 | 0.240% |
| Roman amphora | 6,029 | 0.169% |
| Torpedo jar (Mesopotamian) | 3,098 | 0.087% |
| Turquoise Glazed Pottery (Mesopotamian) | 1,527 | 0.043% |
| Terra sigillata | 122 | 0.003% |
| **Total** | **3,557,118** | |

Two things follow. First, Pattanam's Roman material is enormous by the standards
of the region — Wheeler's 1945 excavation at Arikamedu, the type-site for
Indo-Roman contact, produced 116 amphora sherds and 38 of sigillata, so Pattanam
exceeds it roughly fiftyfold. Second, and less often said: Roman wares are
0.17% of the assemblage, and Mesopotamian wares together (4,625 sherds) come to
three-quarters of the Roman total. Since torpedo jars are largely Sasanian and
absent from Red Sea sites, a substantial part of Pattanam's imported pottery
records Gulf traffic of the third to seventh centuries, not Mediterranean
traffic of the first. Pattanam was a port for much longer than it was Muziris.

## Conflicts the extraction surfaced

These are recorded in the `note` field rather than silently reconciled.

1. **Torpedo jars at Pattanam.** Cherian gives 3,098 sherds to 2011. A later
   summary gives "about 398" for 2007–2014 — fewer sherds over a longer window.
   Almost certainly a transcription slip for 3,098, but I have not assumed so.
2. **Glass at Pattanam.** Cherian's Table 1 gives 1,338 fragments to 2011; a
   later summary gives about 906 for 2007–2014. Same direction of error.
3. **An arithmetic error in Cherian's Table 1.** The ring-stones row reads
   0, 0, 0, 15, 9 with a printed total of 15. The seasons sum to 24. The printed
   grand total of 48,862 antiquities uses 15, so the error is in the row, not
   the total.

## How the extraction was done, and how well it worked

A miner scans all 96 texts for a site name and an artefact class in the same
sentence, then binds any quantity to the *nearest* artefact mention and records
the verbatim sentence and page. It proposes; it does not decide. Of 1,217
proposed statements, 30 carried a quantity, and I read all 30: **13 accepted,
2 recoded, 15 rejected.**

The rejects are instructive about why this cannot be automated. PDF extraction
inlines superscript footnote markers, so "Sri Lanka.180 There were also beads"
parses as 180 beads. Ware names contain digits, so "Dressel 2-4" parsed as four
amphorae. Page ranges in footnotes ("77–78 for Mediterranean amphoras at Qana")
parse as 78 amphoras. And comparative sentences attach one site's finds to
another: "three rim sherds clearly resemble Type 1 from Arikamedu" describes
Pattanam. Successive fixes — masking type numerals, dates, measurements,
footnote markers and running headers; requiring an explicit unit; binding counts
to the nearest ware — raised usable precision from about 28% to 50%. The
remaining errors are semantic, not typographic, and need a reader.

## What is still missing

- **Indian Archaeology: A Review**, and the Kerala state reports. This is the
  only way to establish whether the eleven Kerala candidates have genuinely
  never been dug or have been dug without my finding the report. The distinction
  matters: the first is a fact about the record, the second a fact about my
  library.
- **Suresh 2004** and **Turner 1989** for the Roman coin and bead distributions.
- **Sedov's Qana reports** in full, for a second quantified anchor assemblage to
  set beside Pattanam.
- Two library PDFs are scan-only and still need OCR: McCrindle's Ptolemy and the
  Indian toponyms volume.
