# Bibliographic sweep: what exists, per site

## Method

Crossref for discovery, Unpaywall for open access, run identically over every
port and candidate (`src/query_literature.py`). **948 works retrieved, 344
on-topic, 241 open access.** Triage in `src/triage_literature.py`, results in
`data/processed/literature_candidates.csv`.

Relevance is judged by requiring a site name or a Periplus-specific term in the
**title**. This is strict, but it is applied the same way everywhere, which is
what makes cross-site comparison meaningful.

**Why raw hit counts are useless here.** Crossref's text search is token-based,
not phrase-based. Querying "Mafia Island" returns 181,994 works, nearly all
about organised crime; "Quseir al-Qadim" returns 1.5 million. Any attention
metric built on those numbers would be fiction. The title filter is the
correction.

**Two limitations to state plainly.** Crossref indexes DOIs, so pre-2000
archaeology — much of the Kerala and East African fieldwork — is largely
invisible to it; IAR fills that gap, not this. And OpenAlex, which covers
non-DOI works better, rate-limits this IP and could not be used.

## Each on-topic work is tagged by strand

| strand | works | what it is |
|---|---|---|
| archaeology | 134 | excavation, ceramics, coins, epigraphy, trade history |
| palaeoenvironment | 33 | mangroves, Holocene sediments, sea level, remote sensing |
| both | 4 | |
| other | 173 | loose token matches, mostly junk |

The "other" bucket is where a search for *Sindh* catches the *Sindh University
Research Journal* — which publishes ichthyology and lepidoptery. Those were
downloaded on a first pass, spotted, and deleted; the harvester is now
restricted to the two real strands.

## The finding: two ports have no archaeological literature, only environmental

| port | archaeology | palaeoenvironment |
|---|---|---|
| Berenike | 19 | 0 |
| Myos Hormos | 24 | 0 |
| Adulis | 9 | 0 |
| Muziris | 8 | 0 |
| Arikamedu | 5 | 0 |
| **Rhapta** | **13** | **12** |
| **Barbarikon** | **1** | **6** |
| Leuke Kome | 7 | 5 |

For the securely located ports the literature is archaeology and nothing else.
For **Barbarikon the sweep found a single archaeological work** — an
*Encyclopedia of Ancient History* entry with zero citations — against six
studies of Indus delta mangroves, dam impacts and land-cover change. Rhapta is
split almost evenly between archaeology and mangrove ecology.

This is the same asymmetry the material layer showed, arriving by a different
route. Where a port is undisputed, people dig and publish. Where it is disputed,
the only recent fieldwork in the landscape is environmental science.

## But the environmental strand is not noise — it is step 3

The mangrove and Holocene-sediment papers clustering around the Rufiji and Indus
deltas are exactly the palaeo-coastline evidence the plan needs, and they answer
the question asked earlier about locating ancient river mouths:

- Rufiji: mangrove dynamics and environmental change (*Veg. Hist. Archaeobot.*
  2012), mangrove cover change detection (2018, OA), L-band radar decomposition
  of the delta (*Remote Sensing* 2016), sediment dynamics (1996), organic-matter
  sourcing (*Applied Geochemistry* 2020).
- Unguja Ukuu: Holocene mangrove dynamics (*Quaternary International* 2013).
- Indus delta: land-use/land-cover change from satellite (2018, OA), mangrove
  management, dam impacts on the delta.
- Khor Rori: Upper Holocene palaeoenvironment and subsistence (*J. Quaternary
  Sci.* 2024).

These were retrieved as a by-product of searching for ports, and they should be
carried straight into the coastline layer rather than filtered out.

## Harvested

11 open-access PDFs into `library/oa-harvest/`, including:

- **Chami/Bita 2023** on Rhapta, *IJEGEO*
- **Fitton & Wynne-Jones 2017**, "Understanding the layout of early coastal
  settlement at Unguja Ukuu", *Antiquity*
- **Subramanian 2021**, "The Architectural Tradition of Ponnani, Kerala" — the
  only substantive Ponnani item the sweep produced, and it is architectural
  history, not archaeology
- **Kelly 2024**, stone beads and debitage from Pattanam
- Rufiji mangrove cover and carbon-stock studies
- Sumhuram 2021; Romano-Indian rouletted pottery in Indonesia (2010)

14 failed: publisher 403s, or Unpaywall pointing at a landing page or a book
review rather than the work. Logged with DOIs in
`data/processed/oa_harvest_log.csv`.

## Worth acquiring, newly identified

| Work | Why | DOI |
|---|---|---|
| **Chami 1999, "Roman Beads from the Rufiji Delta, Tanzania: First Incontrovertible Archaeological Link with the Periplus", *Current Anthropology*** | 47 citations, the single most-cited archaeological claim for Rhapta at Rufiji, and in a far stronger venue than the Chami papers already held | 10.1086/200009 |
| **Gurukkal 2001, "In search of Muziris", *JRA*** | The sceptical case on Muziris | 10.1017/s1047759400019978 |
| Chami 2021, "A Find of Transoceanic Pottery at Bwejuu Island of the Rufiji Delta and Mafia Island" | Directly on the Rhapta candidates; nominally OA but the publisher blocks retrieval | 10.11648/j.ija.20210901.14 |
| Peacock & Blue (eds), *Myos Hormos – Quseir al-Qadim* vol. 2 | Anchor assemblage | — |
| Van der Veen, *Consumption, Trade and Innovation* (Quseir al-Qadim botanicals) | Organic evidence at an anchor | — |

Still outstanding from before: Datoo 1970 (confirmed **not** open access,
doi:10.1080/00672707009511528), Turner 1989, Suresh 2004, the Salles & Sedov
Qāni' monograph.
