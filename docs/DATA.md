# The data, in full

Everything the project can draw on: what is held, what is reachable, and what is
not obtainable at all. Counts are as of the last inventory.

Four evidence streams, plus the apparatus that ties them together. The honest
summary first: **nothing in any stream dates to AD 50.** The textual stream is
first-century testimony about distances; everything else is a prior on the
landscape, not a measurement of it at the right date.

---

## 1. Textual

The only stream that speaks about the first century directly.

| Source | Status | Size |
|---|---|---|
| Periplus distance statements | Held | 51, in `distances.csv` |
| Periplus port passages | Held | 1,009, in `port_passages.csv` |
| Ptolemy's coordinates for these coasts | Held | 23 relevant, 497 for India |
| Positional assertions across the literature | Held | 61 |
| Pliny, *NH* 6 | Held | |
| Muziris papyrus, de Romanis | Held | |
| Tamil Sangam poems | **At second hand only** | |
| Tabula Peutingeriana | Noted, not worked | |

**What it supports.** Relative spacing along a coast, within a wide band. The
distances are rounded day-counts, not measurements: 82 per cent of stadia are
multiples of 100, every value at or above 2,000 is an exact multiple of 1,000.
They yield rankings, not fits.

---

## 2. Material

| Source | Status | Size |
|---|---|---|
| *Indian Archaeology: A Review*, 1953–2014 | Held, parsed | 7,053 entries, 78 volumes |
| Coin Hoards of the Roman Empire, South Asia | Held, cleaned | 427 hoards, ~417,000 coins |
| Excavation campaigns at candidates | Hand-built | 27 campaigns, 26 sites |
| Quantified ceramic finds | Hand-built | 61 rows, 6 sites |
| Ware typology, Tomber 2008 | Held | 43 wares |
| Survey effort per site | Hand-built | 65 sites |
| Excavation reports | Held | 25 PDFs, 290 MB |
| Single and stray coin finds, Turner 1989 | **Not acquired** | the category CHRE omits |

**What it supports.** A positive find of the right date is close to decisive. An
absence is almost always an absence of excavation: thirteen of twenty-two
candidates have never been dug, and only six sites have quantified finds.

**Unread but held:** the 450-page Aynuna report, whose coin catalogue may settle
Leukē Kōmē, plus Qana, Sumhuram, Ras Hafun and Myos Hormos.

---

## 3. Geographic

The largest stream by volume and the thinnest by date.

### Historic charts

| Collection | Status | Size |
|---|---|---|
| Admiralty sheets, Wikimedia | Held | 9 sheets, 153 MB, 80–176 MP each |
| Gallica, downloaded | Held | 25 sheets, 142 MB |
| Gallica, catalogued | Metadata only | **915 sheets, 791 dated before 1800** |
| David Rumsey | Catalogued | 49 sheets |
| Survey of India 58 B/C/G, 1911–13 | **Not online** | Map Collection |
| ADM 352 manuscript originals | **Not online** | National Archives |
| Qatar Digital Library | **Blocks scripts** | India Office Records |

Coverage: Malabar 749, 750 and 751 of 1857 cover the whole coast; Indus 41 and
118 of 1897 are Oldham's survey; Red Sea 8a–8c of 1873 are Moresby's. The
pre-1700 Dutch sheet carries soundings and lands on Cranganore and Purakkad.

### Satellite and gridded products

| Source | Resolution | Coverage | Status |
|---|---|---|---|
| Sentinel-2 L2A | 10 m | 2015– | Streamed, 14 composites cached, 1 GB |
| Landsat MSS | 79 m | 1972–76, pre-barrage | Streamed |
| JRC Global Surface Water | 30 m | 1984–2021 | 7 regions computed |
| ALOS PALSAR, L-band radar | 25 m | annual mosaics | Streamed |
| Copernicus DEM | 30 m | global | Streamed |
| ESA WorldCover | 10 m | 2021 | Streamed |
| GEBCO bathymetry | ~450 m | global | Available, unused |
| ERA5 wind | hourly, 1940– | global | Available, unused |
| HydroRIVERS | vector | global | Held, judged unusable as control |
| CORONA, declassified | 2–8 m | 1960–72 | **Needs a USGS account** |
| TanDEM-X | 12 m | global | **Needs a DLR proposal** |

### Subsurface and dated

| Source | Status | Size |
|---|---|---|
| Kerala boreholes, Maya et al. 2017 | Held, extracted | 17 cores, 27 radiocarbon dates |
| Dutch chart soundings | Transcribed | 20, Cranganore and Purakkad |
| Kuttanad boreholes, Maya et al. 2022 | **Not acquired** | the five named cores |
| Periyar palaeodelta, Narayana et al. 2001 | **Not acquired** | ~50 km², 6 km wide |
| Periyar resistivity, Priju et al. 2018 | **Not acquired** | sees through the polders |
| OSL beach ridges, Alappat et al. 2015 | **Not acquired** | dated shorelines |
| Sea-level curve, Shaji et al. 2022 | **Not acquired** | the datum |
| Mathai and Nair 1988 | **Not acquired** | the 2000 BP claim, unchecked |
| Tide model, FES2022 or TPXO | **Needs registration** | largest error in soundings |

**The date problem, stated once.** Kerala's youngest radiocarbon dates are 2460,
2580 and 2730 BP, so roughly 510, 630 and 780 BC. The Indus shelf core carries a
hiatus from 8 ka to 1.3 ka. The charts reach 1700. The satellite record begins
1972. Nothing touches the first century.

---

## 4. Voyage and wind

| Source | Status |
|---|---|
| ERA5 wind climatology | Available, model not built |
| Square-rig performance, Whitewright 2007 | Held |
| Ship tonnage from the Muziris papyrus | Held, via de Romanis |
| Copeland's 44-port model coordinates | Held, in the gazetteer |
| Roman wreck from the Indian Ocean | **Does not exist** |

---

## 5. Apparatus

| Item | Size |
|---|---|
| Candidate gazetteer | 92 sites, 26 disputed candidates |
| Site aliases across the literature | 65 |
| Later settlement records | 20 |
| Extracted text of every PDF | 101 files |
| Scholarship library | 68 PDFs, 136 MB |
| Statistics reading | 6 PDFs |

---

## What the totality supports

**Can be built now.** A posterior over position for each port, from the distance
likelihood, routed through a reconstructed water network, truncated by where
ground existed and where a ship could reach. Wide, and honest about being wide.

**Can be built with one library session.** The same, with a dated sea-level
curve and the Kuttanad cores, which narrows the geographic prior considerably.

**Cannot be built from any of this.** A first-century channel network in Kerala;
four methods have failed. A reconstruction of the Vembanad before 1341, which
the consensus holds to be impossible. Absolute depths at any candidate in AD 50.
And a location for Rhapta, where there is one securely identified neighbour in
three thousand kilometres of coast.

**Only excavation closes it.** Everything here narrows the search. A dated
harbour structure or an inscription naming the port is what settles it, which is
what happened at Pattanam. The deliverable is therefore a ranked list of where
to dig, with the expected information gain attached.
