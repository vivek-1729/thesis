# The second literature sweep, and what it closed

The first sweep asked Crossref about ports, excavations and trade, and returned
950 works that were almost entirely archaeology. The questions blocking the
geographic layer were never asked, so `DATA.md` recorded several gaps as
unclosable that had simply not been searched for.

This is the sweep that asks them. 575 works, seven gap groups, run on OpenAlex
rather than Crossref because the relevant literature sits in the *Journal of the
Geological Society of India*, *Current Science* and Indian university
repositories, which Crossref indexes thinly. Scripts in
`src/query_geo_literature.py`, `src/triage_geo_literature.py` and
`src/fetch_geo_pdfs.py`; candidates in `data/processed/geo_literature_candidates.csv`.

Of 575 hits, 98 cleared both filters, and 28 downloaded. The rest are listed in
`data/processed/geo_acquisition_list.csv`.

---

## What it closed

**Rhapta now has a dated geographic layer, which it did not have before.**
Punwong's 2013 Leeds thesis holds radiocarbon-dated cores from the northern
Rufiji Delta and from Unguja Ukuu and Makoba Bay on Zanzibar, with altitudes
recorded above and below mean sea level and formal sea-level index points
calculated from mangrove zonation. The Rufiji cores run to 1173 cal BP at
-0.94 m amsl; the Unguja Ukuu core B-UU-1 gives 1359 ± 48 cal BP. Held as
`library/oa-harvest/rhapta-tanzania_Punwong2013_*.pdf`, 295 pages.

This matters beyond the dates. The index points come with indicative ranges,
which is the form the errors-in-variables sea-level method in
`STATISTICAL-PLAN.md` expects, and no other port region has supplied them yet.

**A standardised regional sea-level database exists, and it stops short of
Kerala.** Mann and colleagues' SEAMIS database covers Southeast Asia, the
Maldives, India and Sri Lanka, with 213 index points and 333 limiting points.
Its two Indian sites are at 9.29°N 79.22°E and 13.75°N 80.21°E, both on the
southeastern coast. The Malabar coast contributes nothing to it. So SEAMIS
supplies the protocol and the glacial isostatic adjustment predictions but not
the Kerala datum, and the datum still has to come from Shaji et al. 2022.

**Narayana, Priju and Chakrabarti 2001 is open access**, which the acquisition
list did not know. It carries two DOIs for the same title, and the authored
record is the paper: *Journal of the Geological Society of India* 57, no. 6
(2001): 545–47, `10.17491/jgsi/2001/570609`. The second,
`10.17491/jgsi/2001/580409`, is two pages at 58, no. 4: 368–69, with no authors
attached, so it is probably a discussion. Worth taking both.

**Das et al. 2024 works the Muziris coast directly** and did not appear in the
first sweep. Three drilled cores at the Periyar mouth, geochemical,
mineralogical, palynological and geochronological, with Holocene sediments at
1.1–8.1 cal kyr BP. The youngest of those is around AD 850, against the 2460 BP
floor of the cores we hold. Open access in *Quaternary Science Advances* 14
(2024): 100197, `10.1016/j.qsa.2024.100197`.

---

## What it did not close

**Nothing reaches the first century.** The nearest dated material in anything
acquired is Das et al.'s 1.1 cal kyr BP at the Periyar mouth and Punwong's
1359 cal BP at Unguja Ukuu. Both are eight centuries late. The finding in
`GEOGRAPHIC-FINDINGS.md` §3 stands.

**Priju et al. 2018 is still the outstanding item.** The sweep turned up Priju
et al. 2021 instead, 33 vertical electrical soundings from Ernakulam to Chettuva
on the Muziris coast with a modelled subsurface lithology. It is a salinity
study: the words palaeochannel and buried do not occur in it. Useful as
subsurface control on the Periyar coast, not a substitute.

**Alappat et al. 2015 and Shaji et al. 2022 remain paywalled.** Both are
Elsevier, both are on the existing list, and the sweep found no open copy.

---

## A distinction the acquisition list was missing

Several of the blocked items are open access and blocked only to scripts.
Springer, MDPI, ScienceDirect and GeoScienceWorld now answer a scripted request
with a JavaScript challenge, so a download returns a challenge page with a 200
status rather than the file. Every fetch in `fetch_geo_pdfs.py` is checked for
the PDF magic bytes for that reason.

These need a browser, not the Harvard proxy, and are one click each:

| Item | Where |
|---|---|
| Das et al. 2024, Muziris cores | `10.1016/j.qsa.2024.100197` |
| Narayana et al. 2001, Periyar palaeodelta | `10.17491/jgsi/2001/570609` |
| Tiwari et al. 2025, Vembanad palaeolimnology | `10.3390/quat8010003` |
| Roman metallurgy at Muziris, 2026 | `10.1007/s44218-025-00115-8` |
| Biagi et al. 2024, Arabian Sea coast | `10.1007/s44289-024-00003-y` |
| Mid-Holocene circum-Arabian sea-level database | `10.1016/j.quascirev.2021.106959` |
| East African palaeo-shorelines, 2021 | `10.1016/j.geomorph.2021.107896` |
| Al Wajh platform lagoon, 2021 | `10.1111/sed.12955` |
| Ryano and Chami 2021, Bwejuu | `10.11648/j.ija.20210901.14` |

The Biagi preprint came through from Research Square and is held, so that row is
a better copy rather than a missing one.
