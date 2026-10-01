# Evidence

Every class of evidence this thesis needs, what it can actually settle, and where
we stand.

**The criterion is resolution.** Candidates for a given port sit 25 to 150 km
apart. Most of the field's standard methods establish that trade happened in a
region without distinguishing one village from its neighbour. Effort should
follow resolution, not availability.

---

## 1. Textual

| Evidence | What it can settle | Status |
|---|---|---|
| Periplus distances | Relative position along a coast, to within a wide band | 51 statements extracted; stadion calibrated to about 155 m |
| Periplus descriptions | Harbour type, river or open coast, upriver distance, goods | Extracted per port |
| Ptolemy coordinates | Order and rough spacing, not absolute position | 23 entries in `ptolemy_entries.csv` |
| Pliny | Independent corroboration, occasionally contradicting the Periplus | Held; the Bakarē preference is the key passage |
| Muziris papyrus | The trade itself, not the location | Held, de Romanis |
| Tamil Sangam poems | Which river a port sat on | Secondary only; needs a direct pass |
| Peutinger Table | Presence of a port, nothing finer | Noted, not worked |

**Limit.** The distances are rounded day-counts, not measurements. 82 per cent of
stadia figures are multiples of 100 and every value at or above 2,000 is an exact
multiple of 1,000. They give rankings, not fits.

## 2. Material

| Evidence | What it can settle | Status |
|---|---|---|
| Excavation campaigns | How hard anyone looked, which is what makes absence readable | 27 campaigns, all 23 candidates |
| Quantified ceramic finds | Whether a site traded, with whom, and when | 61 rows from 6 sites; thin |
| Ware typology | Makes "Roman pottery at X" comparable across reports | Held, Tomber 2008 |
| Harbour structures | Whether a site was a port rather than a consumer | Pattanam wharf, canoe and bollards only |
| Coin hoards | Regional trade intensity; cannot point at a harbour | 427 cleaned hoards; 73 per cent lie over 25 km inland |
| Single and stray coin finds | The category that does bear on harbour location | **Missing**; Turner 1989 |
| Organic remains | Cargo and diet, confirming long-distance contact | Pattanam and Berenike only |

**Limit.** A positive find of the right date is close to decisive. An absence is
almost always an absence of excavation: 13 of 22 candidates have never been dug.

## 3. Geographic

| Evidence | What it can settle | Status |
|---|---|---|
| Palaeo-shoreline | Whether a candidate's ground existed in the first century | Literature identified, not held |
| Sediment cores | Water or land at a known point at a known date | Five Kuttanad boreholes exist; see `SEDIMENT-CORES.md` |
| River channels | The route the "by river and sea" distances actually ran | Nothing yet; CORONA and FABDEM not ordered |
| Historic charts | The system before the barrages and reclamation | Identified, not acquired |
| Bathymetry | Whether a ship could enter and anchor | Nothing yet |
| Wind and monsoon | Which legs were sailable, and how fast | ERA5 available, model not built |

**Limit.** None of it dates to the first century on its own. Cores carry dates;
charts and imagery give a pre-industrial baseline that bounds how much has
changed.

## 4. Later settlement

| Evidence | What it can settle | Status |
|---|---|---|
| Medieval and early modern ports | Where the coast could support a harbour | `later_settlement.csv` |
| Place names | Continuity, weakly | Collected per port |
| Colonial survey maps | The landscape before modern engineering | Partially, via Gurukkal and Whittaker |

**Limit, and it is the important one.** Every Kerala candidate is a documented
later port with no first-century evidence. This category is how the candidate
lists were assembled, so it is a source of bias in the hypothesis set rather than
evidence for any member of it.
