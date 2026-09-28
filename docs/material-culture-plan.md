# Material culture: what to collect and how

## The question the material has to answer

For each **candidate** location: *is there stratified 1st-century-AD Indian Ocean trade
material here?*

Note "candidate", not "port". We do not need to collect material for Berenike or Qana' to
establish where they are — the material is *why* they are established. What we need is the
material record at Ponnani, Tanur, Koyilandy, Purakkad, Niranam, al-Wajh, Pangani, Banbhore
and the rest. That is the column that decides things.

My expectation is that most candidates have **no excavation at all**, and that absence is
itself a result: it says the material test cannot discriminate for that port, and it says
where a future excavation would be decisive.

## Diagnostic artefact classes

| class | why it dates and locates |
|---|---|
| Mediterranean amphorae | Dressel 2–4, Dressel 20, LR1/LR2, Egyptian/Palestinian types. The single best marker of Roman-era trade, and typologically tight |
| Terra sigillata | Italian (Arretine), Eastern Sigillata A/B. Narrow date ranges |
| Torpedo jars | Parthian/Mesopotamian — marks Gulf rather than Red Sea contact |
| Indian Rouletted Ware, Black-and-Red Ware | marks Indian contact at Red Sea and African sites; the reciprocal of the amphorae |
| Roman coins | denarii and aurei in India; bronze at Red Sea sites |
| Glass | Roman cast and blown vessels; beads |
| Intaglios, cameos, lamps | small but chronologically sharp |
| Organic residues | black pepper, rice, coconut — Berenike is the model |

## Two problems to settle before collecting, not after

**1. Reports do not quantify comparably.** Some publish sherd counts, some estimated vessel
equivalents, some weight, some only "amphorae present." You cannot put "50 amphora sherds at
Pattanam" beside "amphorae attested at Qana'" in the same column.

So the data model is **ordinal presence per class per site**, not counts:
`0 absent · 1 present · 2 common · 3 abundant`, with the citation recorded in the same cell.
Adopting counts and then discovering they are incommensurable would waste weeks.

**2. Excavation happens where people expect to find things.** Pattanam was dug because
someone thought Muziris was there. Finding Roman pottery confirms that trade happened at
that spot — not that the spot bore that name. The material test establishes *"a port
existed here"*; only combined with the textual constraints does it identify one. Worth
stating explicitly in the write-up, because a reviewer will raise it.

## Phases

**M1 — schema (1 day).** Columns: site, candidate-for, excavation status
(excavated / surveyed / surface finds / none located), then one ordinal column per artefact
class, a date-bracket column (pre-Roman / 1st c BC–1st c AD / 2nd–4th c / later), and a
citation column per cell.

**M2 — anchors, from reports already on disk (about a week).** Pattanam, Berenike, Qana',
Sumhuram, Arikamedu, Ras Hafun, Banbhore, Aynuna, Adulis, Xiis, Sopara, Chaul. Roughly
12 sites × 8 classes. This is the calibration: it establishes what a 1st-century Indian
Ocean port actually looks like materially, so "no material" at a candidate means something.

**M3 — candidate audit (one to two weeks, mostly reading).** All 26 candidates. For each:
has anyone excavated, surveyed, or reported surface finds? Record "no archaeological work
located" as a value.

**M4 — coins, only if M3 justifies it.** Scope from the dig-intensity check. If East Africa
is as thin as Copeland's figures suggest (0.2 recorded sites per port against 290 in Egypt),
the coin catalogues cannot help Rhapta and the work should be scoped to Kerala and the
Red Sea.

## What to acquire

**Essential**
- **Tomber, *Indo-Roman Trade: from Pots to Pepper* (2008)** — the synthesis that tabulates
  which sites have which wares. The highest-value single acquisition for this whole step.
- **Turner, *Roman Coins from India* (1989)** and **Suresh, *Symbols of Trade* (2004)** — the
  coin find-catalogues, for M4.

**For the candidate audit**
- *Indian Archaeology: A Review* (ASI annual) — records every excavation in India; the way to
  find out whether anyone has dug at Ponnani or Purakkad
- Kerala State Department of Archaeology reports
- *Atlal* (Saudi antiquities journal) for al-Wajh and the Red Sea coast
- *Pakistan Archaeology* and *Sindh Antiquities* for the Indus delta
- Tanzania Department of Antiquities; Chami's survey reports for the Rufiji and Mafia

**Databases**
- Coin Hoards of the Roman Empire (Ashmolean) — ask about bulk export; no API is documented
- *Roman Amphorae: a digital resource* (ADS) — typology reference rather than find data

## Output

A site × artefact-class matrix. It is directly a figure (an ordinal heatmap, sites down,
classes across, blank cells for "never investigated") and directly an input to the candidate
scoring. The blank cells will probably be the most informative part of it.
