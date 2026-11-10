# Material data

The archaeological tables built earlier in the project, moved here from `data/raw`
and `data/processed` in November 2026. Several are basin-wide rather than
Malabar-only: they cover all seven Periplus ports, including Aynuna, Banbhore and
the Rhapta candidates. The scripts that built them are in `archive/src/` and are
frozen, so they will not find these files at the new paths.

## pottery/

| File | What |
|---|---|
| `ware_typology.csv` | 43 ware classes after Tomber 2008, with origin, date range and diagnostic features. The controlled vocabulary for comparing assemblages |
| `material_finds.csv` | 61 hand-checked find statements with quantity, period and verbatim quote. Mostly Berenike and Myos Hormos |
| `material_observations.csv` | 48 count records, 42 of them Pattanam: per-season sherd counts by ware from Cherian's tables, 2007–2011 |
| `material_candidates.csv` | 1,217 machine-proposed site and ware co-mentions from the library. Unverified; see `archive/docs/FINDINGS.md` §6.3 |

## excavations/

| File | What |
|---|---|
| `excavation_campaigns.csv` | 27 campaigns at the candidate sites: who, when, seasons, trenches, area |
| `excavation_register.csv` | 13 excavations with whether natural soil was reached |
| `site_survey_effort.csv` | Excavation status and seasons for 65 sites |
| `candidate_evidence.csv` | What, if anything, of Periplus date has been found at each disputed candidate |
| `later_settlement.csv` | 20 sites with attested occupation after the Periplus horizon |
| `pattanam_trenches.csv` | All 61 KCHR trenches at Pattanam, 2007–2015, with GPS position, plot name and distance from the wharf plot, transcribed from Cherian 2015: 740–743, Table 1. Five rows have printed coordinates that are inconsistent or incomplete, flagged in `note` |

## iar/

| File | What |
|---|---|
| `iar_entries.csv` | 7,053 entries from *Indian Archaeology: A Review*, 1957–58 to 2013–14 |
| `iar_hits.csv` | Name-matched hits for the port candidates |
| `iar_findspots.csv` | 24 geocoded Kerala findspots |

## coins/

CHRE export (raw in `chre/`, cleaned in `chre_*_clean.csv`), hoard distances to
coast, site-find coins, and the Aynuna catalogue. Aggregate numismatic patterns
were judged not useful for locating ports; these are kept for reference.

## Known problems

- Pattanam figures disagree between sources by up to a factor of five on the
  import share (`archive/docs/FINDINGS.md` §24, item 3). The Cherian season
  tables in `material_observations.csv` are internally consistent, but other
  Pattanam publications give different totals.
- IAR chapter labels are unreliable in some volumes (`FINDINGS.md` §24, item 13).
