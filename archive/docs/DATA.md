# The data, in full

Everything the project holds, everything it can still reach, and everything that
does not exist. Counts are from an inventory of the files, not from memory.

**The whole thing is about 2.8 GB**: a 1.1 GB library of 456 documents and chart
scans, 1.0 GB of satellite composites, 567 MB of third-party geodata that is
gitignored and re-downloadable, 124 MB of gridded environmental cache, and 49
tables holding roughly 22,000 rows of curated and derived data.

**The limitation, stated once and then not repeated.** Nothing in any stream
dates to AD 50. The textual stream is first-century testimony about distances;
everything else is a prior on the landscape or a record of what was found in
it, not a measurement of either at the right date. The closest anything comes is
Das et al.'s 1.1 cal kyr BP at the Periyar mouth and Punwong's 1359 cal BP at
Unguja Ukuu, both around eight centuries late.

---

## 1. Textual

The only stream that speaks about the first century directly.

| Source | Status | Size |
|---|---|---|
| Periplus distance statements | Held, curated | 51, `distances.csv` |
| Periplus port passages | Held | 1,009, `port_passages.csv` |
| Ptolemy's coordinates | Held | 497 for India, 23 on these coasts |
| Ptolemy control points | Derived | 8, `ptolemy_control_points.csv` |
| Positional assertions across the literature | Hand-built | 61, `positional_assertions.csv` |
| **Datoo 1970, Rhapta** | **Held and read** | `library/scholarship`, via Harvard ILL |
| **Tamil Sangam corpus, in Tamil** | **Held** | **40 files, 17 works, `library/sangam`** |
| Sangam port-name counts | Derived | 46 rows, `sangam_port_mentions.csv` |
| Casson 1989, Schoff 1912, Ptolemy, Cosmas, McCrindle | Held | 6 PDFs, 123 MB |
| Pliny *NH* 6 | Held, via the above | |
| Muziris papyrus | Held, via Casson 1990 and de Romanis | |
| Tabula Peutingeriana | **Noted, never worked** | |

**What it supports.** Relative spacing along a coast, within a wide band. The
distances are rounded day-counts rather than measurements: 82 per cent of stadia
figures are multiples of 100, and every value at or above 2,000 is an exact
multiple of 1,000. They yield rankings, not fits.

**What the Sangam corpus adds**, now that it is read in the original rather than
at second hand: Muciri appears in Akananuru and Purananuru and nowhere else in
seventeen works, Tondi in six works, Yavana in sixteen of seventeen, and
Nelkynda not at all. Three other names cannot be counted because the Tamil word
is also an ordinary one.

---

## 2. Material

| Source | Status | Size |
|---|---|---|
| *Indian Archaeology: A Review*, 1953–2014 | Held, parsed | 7,053 entries from 78 volumes |
| IAR search hits for our sites | Derived | 312 |
| IAR findspots, geocoded | Hand-built | 24 |
| Coin Hoards of the Roman Empire, South Asia | Held, cleaned | 427 hoards, 7,811 coins |
| Hoard distances to coast and to candidates | Derived | 191 |
| Excavation campaigns at candidates | Hand-built | 27 campaigns, 26 sites |
| Excavation register | Hand-built | 13 |
| Quantified ceramic finds | Hand-built | 61 rows, 6 sites |
| Material observations | Derived | 48 |
| Ware typology, Tomber 2008 | Held | 43 wares |
| Survey effort per site | Hand-built | 65 sites |
| **Aynuna excavated coins** | **Extracted, checked** | **28, `aynuna_coins.csv`** |
| Site find coins | Derived | 25 |
| Excavation reports | Held | 25 PDFs, 289 MB |
| Single and stray coin finds, Turner 1989 | **Not acquired** | the category CHRE omits |

**What it supports.** A positive find of the right date is close to decisive. An
absence is almost always an absence of excavation: thirteen of twenty-two
candidates have never been dug, and only six sites have quantified finds.

**The Aynuna catalogue is the one place this stream reaches a port directly.**
Twenty-eight coins, checked against the excavator's own stated totals, with
nothing struck by an authority whose reign includes AD 50.

**Held and still unread:** the 450-page Aynuna report in full, Qana, Sumhuram,
Ras Hafun and the 387-page Myos Hormos report.

---

## 3. Geographic

The largest stream by volume and the thinnest by date.

### Historic charts

| Collection | Status | Size |
|---|---|---|
| Admiralty sheets, Wikimedia | Held | 9 sheets, 153 MB, 80–176 MP each |
| Gallica, downloaded | Held | 26 sheets, 141 MB |
| Gallica, catalogued | Metadata | 915 sheets, 791 dated before 1800 |
| **Gallica, selected** | **Chosen, download blocked** | **132 naming a candidate's neighbourhood** |
| David Rumsey | Held | 50 files, 43 MB, noisy catalogue |
| Dutch chart soundings | Transcribed, error budget fitted | 20 points; ±0.58 m quantifiable, datum unknown |
| Survey of India 58 B/C/G, 1911–13 | **Not online** | Harvard Map Collection |
| ADM 352 manuscript originals | **Not online** | The National Archives |
| Qatar Digital Library | **Blocks scripts** | India Office Records |

Admiralty coverage: Malabar 749, 750 and 751 of 1857 cover the whole coast;
Indus 41 and 118 of 1897 are Oldham's survey; Red Sea 8a–8c of 1873 are
Moresby's. The pre-1700 Dutch sheet carries soundings and lands on Cranganore
and Purakkad.

### Satellite and gridded products

| Source | Resolution | Coverage | Status |
|---|---|---|---|
| Sentinel-2 L2A composites | 10 m | 2015– | 33 cached arrays, 1.0 GB |
| Landsat MSS | 79 m | 1972–76, pre-barrage | Streamed |
| JRC Global Surface Water | 30 m | 1984–2021 | 7 regions computed |
| ALOS PALSAR, L-band radar | 25 m | annual mosaics | Streamed |
| Copernicus DEM | 30 m | global | Streamed |
| ESA WorldCover | 10 m | 2021 | Streamed |
| HydroRIVERS | vector | global | Held, 535 MB, judged unusable as control |
| Natural Earth 10m | vector | global | Held, 32 MB |
| **ICESat-2 ATL24 bathymetry** | along-track | 2018– | **Needs a free Earthdata login**; 220–606 granules per port |
| NOAA multibeam and tracklines | survey | global | No multibeam at any port; **4 tracklines at Pamba, 12 at the Menuthias channels** |
| CORONA, declassified | 2–8 m | 1960–72 | **Needs a USGS account** |
| TanDEM-X | 12 m | global | **Needs a DLR proposal** |

### The measured environment

Gathered after it turned out none of it needed an account.

| Source | Status | Size |
|---|---|---|
| **GMRT bathymetry** | **Gathered, 6 port boxes** | 65 MB; **0 % measured at every one** |
| **Tidal range, fitted from observation** | **6 ports** | `tidal_range.csv`; IOC and Hawaii gauges, 59 MB |
| **NCEP wind climatology** | **11 sites × 12 months** | 132 rows, 1948– |
| **East African coast wind transect** | **5 latitudes × 12 months** | tests Datoo's meteorological claim |

### Subsurface and dated

| Source | Status | Size |
|---|---|---|
| Kerala boreholes, Maya et al. 2017 | Held, extracted | 17 cores, 27 radiocarbon dates |
| **Rufiji and Zanzibar cores, Punwong 2013** | **Extracted** | **26 dates, `tanzania_cores.csv`** |
| SEAMIS sea-level database, Mann et al. 2019 | Held | 213 index points, **none in Kerala** |
| Periyar palaeodelta, Narayana et al. 2001 | **Open access, one click** | ~50 km², 6 km wide |
| Periyar-mouth cores, Das et al. 2024 | **Open access, one click** | 3 cores, youngest 1.1 cal kyr BP |
| Kuttanad boreholes, Maya et al. 2022 | **Not acquired** | the five named cores |
| Periyar resistivity, Priju et al. 2018 | **Not acquired** | sees through the polders |
| OSL beach ridges, Alappat et al. 2015 | **Not acquired** | dated shorelines |
| Sea-level curve, Shaji et al. 2022 | **Not acquired** | the Kerala datum |
| Mathai and Nair 1988 | **Not acquired** | the 2000 BP claim, unchecked |

---

## 4. Voyage and wind

| Source | Status |
|---|---|
| **NCEP wind climatology** | **Gathered**; speed, direction and steadiness per month |
| Square-rig performance, Whitewright 2007 | Held |
| Ship tonnage from the Muziris papyrus | Held, via de Romanis |
| Copeland's 44-port model coordinates | Held, in the gazetteer |
| Voyage simulator | Not built |
| Roman wreck from the Indian Ocean | **Does not exist** |

---

## 5. Apparatus

| Item | Size |
|---|---|
| Candidate gazetteer | 92 sites |
| Disputed candidates | 31 across 6 ports |
| Site aliases across the literature | 65 |
| Site confidence tiers | 92 |
| Later settlement records | 20 |
| Data coverage matrix | 60 |
| Extracted text of every PDF | 101 files, 17 MB |
| Literature sweeps | 950 archaeological, 575 geographic |
| Acquisition list from the geographic sweep | 70 |
| Scripts | 71 Python files |
| Figures | 39 PNG |
| Notebooks | 3 |

---

## 6. The library, by folder

456 files, 1.1 GB, outside the repo at `../library/`.

| Folder | Files | Size | What |
|---|---:|---:|---|
| `excavation-reports` | 25 | 289 MB | Pattanam, Aynuna, Banbhore, Berenike, Myos Hormos, Qana, Sumhuram, Ras Hafun |
| `oa-harvest` | 44 | 187 MB | Open-access papers from the two literature sweeps |
| `charts` | 9 | 153 MB | Admiralty, 1857–1897 |
| `charts-gallica` | 26 | 141 MB | French and Dutch, 1694–1799 |
| `scholarship` | 68 | 135 MB | Modern secondary literature |
| `ancient-sources` | 6 | 123 MB | Periplus, Ptolemy, Cosmas |
| `charts-rumsey` | 50 | 43 MB | David Rumsey sheets |
| `iar-text` | 78 | 24 MB | *Indian Archaeology: A Review* |
| `text-cache` | 101 | 17 MB | Extracted text layers |
| `stats` | 6 | 15 MB | Statistical method papers |
| `sangam` | 39 | 14 MB | Tamil Sangam corpus |
| `geomorphology` | 1 | 11 MB | Kerala cores |
| `reference` | 2 | 6.9 MB | Gazetteers |

---

## 7. What is not held

### Blocked on you

| Item | Blocker |
|---|---|
| CORONA 1960s imagery | USGS EarthExplorer registration |
| ICESat-2 ATL24, the best depth data that exists here | a free NASA Earthdata login |
| 16 NOAA tracklines: 4 at the Nelkynda approach, 12 at the Menuthias channels | an NCEI order |
| Nine open-access PDFs | a browser; publishers block scripts, not access |
| Eight paywalled papers | the Harvard proxy |
| 132 selected Gallica sheets | the address is Cloudflare-blocked after a too-fast run |
| Survey of India 58 B/C/G | the Map Collection, in person |
| ADM 352 manuscript charts | The National Archives, in person |
| Qatar Digital Library | blocks programmatic access entirely |
| Turner 1989, *Roman Coins from India* | out of print; Appendix 1 is the stray-find catalogue |

| Khan, *Banbhore: A Preliminary Report* | the original excavation |
| Salles and Sedov 2010, *Qāni'* | print only, 553 pp |
| Is Naura in or out? | your decision |
| Does the voyage simulator estimate its own parameters? | your decision |

**The nine that need only a browser**, since publishers now answer a scripted
request with a challenge page rather than the file: Das et al. 2024
(`10.1016/j.qsa.2024.100197`), Narayana et al. 2001 (`10.17491/jgsi/2001/570609`),
Tiwari et al. 2025 (`10.3390/quat8010003`), Roman metallurgy at Muziris 2026
(`10.1007/s44218-025-00115-8`), Biagi et al. 2024 (`10.1007/s44289-024-00003-y`),
the circum-Arabian sea-level database (`10.1016/j.quascirev.2021.106959`), East
African palaeo-shorelines (`10.1016/j.geomorph.2021.107896`), the Al Wajh lagoon
(`10.1111/sed.12955`) and Ryano and Chami 2021 (`10.11648/j.ija.20210901.14`).

### Does not exist, as far as any search has shown

- **Measured bathymetry at any of the seven approaches.** 2.5 million marine
  cells across six port boxes, not one resting on a real sounding. NOAA's
  archive independently holds no multibeam at any of them and four single-beam
  tracklines across all six, those four at one port. Searched
  exhaustively: GMRT, GEBCO, NOAA multibeam, NOAA tracklines, crowd-sourced
  bathymetry, EMODnet, the Allen Coral Atlas and the Indian hydrographic
  office. ICESat-2 ATL24 is the only open source that would add measurement,
  and water clarity rather than coverage is what decides whether it works.
- **A Roman wreck from the Indian Ocean.**
- **A Kerala sea-level index point.** SEAMIS standardises 213 for the region and
  none is on the Malabar coast.
- **A counterpart to *Indian Archaeology: A Review* outside India.**
- **An open excavation report for Kollam, Niranam or Purakkad.**
- **Any dated evidence within five centuries of AD 50 on these coasts.**

---

## 8. What the totality supports

**Can be built now.** A posterior over position for each port, from the distance
likelihood, routed through a reconstructed water network, truncated by where
ground existed and where a ship could reach, with tide and wind attached. Wide,
and honest about being wide.

**Can be built with one library session.** The same, with a dated Kerala
sea-level curve and the Kuttanad cores, which narrows the geographic prior
considerably, and with Priju et al. 2018, which is the only method that has
seen through the Kuttanad polders.

**Cannot be built from any of this.** A first-century channel network in Kerala,
where four methods have failed. A reconstruction of the Vembanad before 1341,
which the consensus holds to be impossible. Absolute depths at any candidate in
AD 50. And a location for Rhapta, which now has a dated geographic layer but
still has one securely identified neighbour in three thousand kilometres of
coast.

**Only excavation closes it.** Everything here narrows the search. A dated
harbour structure or an inscription naming the port is what settles it, which is
what happened at Pattanam. The deliverable is therefore a ranked list of where
to dig, with the expected information gain attached.

---

## 9. What to read, and why

The method literature, organised against the four components of the statistical
plan in `FINDINGS.md` §3, then the geographic and voyage reading at more depth.
Each entry says what to take from it, since most of these are read for a method
rather than for a result. Almost none is held locally.

### Part A. Statistical method, by component

### Cross-cutting: Bayesian spatial models in archaeology

The closest existing literature to what the thesis is doing, and the place to
position it.

- **Entropy-Based Methods to Address Sampling Bias in Archaeological Predictive
  Modeling**, arXiv:2508.02272.
  https://arxiv.org/pdf/2508.02272
  The most directly relevant recent paper. Archaeological predictive modelling
  with explicit treatment of the fact that sites are found where people looked.
  Read it for how the field currently frames the bias problem, and for what our
  detection model adds over it.

- **Møller, Syversveen and Waagepetersen, "Log Gaussian Cox Processes"**,
  *Scandinavian Journal of Statistics* 25 (1998).
  https://archive.math.arizona.edu/jwatkins/log_Gaussian_Cox_Processes.pdf
  The foundational LGCP paper. Take the construction and the thinning property,
  which is how discovery probability enters the hoard model.

- **Diggle, "INLA for Spatial Statistics: Log-Gaussian Cox Processes"**, course
  notes.
  https://faculty.washington.edu/jonno/SISMIDmaterial/4-LGCPs.pdf
  Practical fitting rather than theory. Useful if the point-process layer is
  fitted in INLA rather than Stan.

---

### Component 1: Prior construction

#### Travel time and maritime least-cost modelling

- **Leidwanger, "Modeling distance with time in ancient Mediterranean
  seafaring"**, *Journal of Archaeological Science* 41 (2014).
  https://www.sciencedirect.com/science/article/abs/pii/S0305440313001064
  The standard reference for treating sailing time rather than distance as the
  measure of separation. Directly supports our finding that the stadion behaves
  as a speed.

- **"Beyond Least Cost Paths: circuit theory, maritime mobility"**, *Journal of
  Archaeological Science* 2021.
  https://www.sciencedirect.com/science/article/pii/S0305440321002089
  Argues against single optimal routes in favour of a distribution over
  crossings. This is the argument for the Monte Carlo voyage simulation rather
  than a least-cost path.

- **Copeland, "Riding the monsoon: geography and Iron Age trade in the Indian
  Ocean"**, *Economic History Review* (2026).
  doi:10.1111/ehr.70016
  The only study doing network and least-cost analysis on this ocean with
  monsoon vectors and palaeo sea-level. Closest prior work to our voyage layer,
  and it reports 14-day outbound and 16-day return averages that our simulation
  should be checked against.

- **"Seafaring and Modelling"**, *Journal of Maritime Archaeology* (2025).
  doi:10.1007/s11457-025-09455-5
  A recent review of the modelling literature. Read for the survey rather than
  for a method.

#### Sea level and palaeo-coastline, specifically for Kerala

- **"Holocene monsoon and sea-level variability from coastal lowlands of Kerala,
  SW India"**, *Quaternary International*.
  https://www.sciencedirect.com/science/article/abs/pii/S104061822200074X
  The regional relative sea-level curve. This is what the coastline prior needs.

- **"Evidence of Late Holocene shoreline progradation in the coast of Kerala"**,
  *Geomorphology* (2015).
  https://www.sciencedirect.com/science/article/abs/pii/S0169555X15002597
  Progradation rates. Reports beach-ridge formation along the whole Kerala coast
  between 3 and 5 ka, and a shoreline roughly 3 km inland of the present one at
  about 4 ka, which bounds how far the first-century coast can have moved.

---

### Component 2: The likelihood from textual evidence

#### Rounding, heaping and coarse data

This is the right literature for the stadia, and it is better developed than
anything in classics.

- **Heitjan and Rubin, "Ignorability and Coarse Data"**, *Annals of Statistics*
  19 (1991).
  The foundational framework. Rounding, heaping, censoring and grouping are all
  treated as one thing, which is exactly how the Periplus figures should be
  modelled. Start here.

- **Allen et al., "Proximity and gravity: modeling heaped self-reports"**,
  *Statistics in Medicine* (2017).
  doi:10.1002/sim.7327
  A workable likelihood for values that gravitate toward preferred numbers. Our
  mantissas are 1, 2, 3, 4, 5, 6, 8, 12, 15 and 18, which is a gravity pattern.

- **"Heaping and seeping, GAITD regression"**, *Annals of Applied Statistics*
  19.4 (2025).
  doi:10.1214/25-AOAS2065
  The current state of the art for count data with excess mass at preferred
  values. More machinery than we need, but it shows what a referee will expect.

#### Sequence models over latent positions

- **Shalizi, "Hidden Markov Models and State Estimation"**, lecture notes,
  Carnegie Mellon.
  https://www.stat.cmu.edu/~cshalizi/dst/18/lectures/24/lecture-24.html
  Clean statement of forward-backward and of why the exact posterior is
  available on a discrete state space. This is the algorithm the position model
  runs on.

- **"Bayesian inference for continuous-time hidden Markov models with an unknown
  number of states"**, arXiv:2106.10660.
  https://arxiv.org/pdf/2106.10660
  Read for how to put priors on the transition parameters while marginalising
  the states, which is the structure of our fit.

---

### Component 3: The likelihood from archaeological evidence

#### Occupancy and imperfect detection

- **MacKenzie et al., "Estimating site occupancy rates when detection
  probabilities are less than one"**, *Ecology* 83 (2002).
  The origin of the method. Everything downstream cites it.

- **Guillera-Arroita et al., "Design of occupancy studies with imperfect
  detection"**, *Methods in Ecology and Evolution* (2010).
  https://besjournals.onlinelibrary.wiley.com/doi/full/10.1111/j.2041-210X.2010.00017.x
  How to allocate survey effort, which is the same question as our decision
  layer, in a field that has thought about it longer.

- **Lahoz-Monfort et al., "Ignoring imperfect detection in biological surveys is
  dangerous"**, *PLoS ONE* 9 (2014).
  https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0099571
  The argument, stated bluntly, for why unadjusted absence is misleading. Useful
  for the methods chapter, since this is the case our thesis has to make to
  classicists.

- **"Intrinsic Bayesian Analysis for Occupancy Models"**, arXiv:1508.07403.
  https://arxiv.org/pdf/1508.07403
  Prior choice for occupancy models, which matters when the number of sites is
  small, as ours is.

#### Assemblage composition

- **Aitchison, *The Statistical Analysis of Compositional Data*** (1986), and
  **Baxter and Freestone, "Log-ratio compositional data analysis in
  archaeometry"**, *Archaeometry* 48 (2006).
  https://www.researchgate.net/publication/229780545
  Why sherd proportions cannot be regressed directly, and what to do instead.
  Baxter is the archaeological entry point.

- **"A Dirichlet Regression Model for Compositional Data with Zeros"**,
  arXiv:1410.5011.
  https://arxiv.org/pdf/1410.5011
  Our assemblages are full of zeros, and both Aitchison's transform and plain
  Dirichlet regression break on them. This is the fix.

- **CRAN Task View: Compositional Data Analysis**.
  https://cran.r-project.org/web/views/CompositionalData.html
  Implementation survey rather than reading.

---

### Component 4: The decision layer

- **Ryan, Drovandi, McGree and Pettitt, "A review of modern computational
  algorithms for Bayesian optimal design"**, *International Statistical Review*
  84 (2016).
  https://eprints.qut.edu.au/75000/1/75000.pdf
  The main review. Expected information gain, and how to compute it when the
  likelihood is expensive, which ours is.

- **Shewry and Wynn, "Maximum entropy sampling"**, *Journal of Applied
  Statistics* 14 (1987).
  The original statement that choosing where to observe is choosing where
  entropy falls fastest. Short and still the clearest framing.

- **Koopman, *Search and Screening*** (1946, reissued 1980).
  The naval search-theory origin of optimal allocation of search effort over a
  posterior. Worth reading for the framing even though the modern Bayesian
  design literature supersedes the mathematics.

---

### What to read first

Four papers would cover the framing of the whole thesis. Heitjan and Rubin for
the textual likelihood, MacKenzie for the archaeological one, Leidwanger for why
distance should be time, and the entropy-based sampling-bias paper for where the
archaeological modelling literature currently stands.

### Part B. Coastlines, deltas and voyages

The reading for Component 1, at more depth. These are the methods that build the
prior, and they are where most of the technical work will sit.

### Reconstructing coasts and deltas

1. **"Spatial analysis of Holocene delta compound clinoforms"**, *Communications
   Earth and Environment* (2024). https://www.nature.com/articles/s43247-024-01652-9
   Quantitative treatment of how deltas build seaward. The method for turning a
   progradation rate into a palaeo-shoreline position.

2. **Stouthamer and Berendsen, "Avulsion frequency, avulsion duration, and
   interavulsion period of Holocene channel belts in the Rhine-Meuse delta"**.
   The reference study for how often a delta channel jumps and how long the jump
   takes. Gives the base rates our Indus and Periyar reconstructions need, and a
   prior for how many channels were active at once.

3. **"Conceptual framework for assessing the response of delta channel networks
   to Holocene sea level rise"**, *Quaternary Science Reviews* (2009).
   https://www.sciencedirect.com/science/article/abs/pii/S0277379109000742
   Links sea-level forcing to channel behaviour. This is what connects the
   Kerala sea-level curve to the Vembanad channel network.

4. **"Large-scale coastal and fluvial models constrain the late Holocene
   evolution of the Ebro delta"**, *Earth Surface Dynamics* 5 (2017).
   https://esurf.copernicus.org/articles/5/585/2017/
   A worked example of reconstructing a specific delta's late Holocene shape
   from models plus cores. The closest template for doing the Indus.

5. **"Shoreline reconstruction since the Middle Holocene"**, *Quaternary
   Research* (2009).
   https://www.sciencedirect.com/science/article/abs/pii/S1040618209001918
   Method for drawing past shorelines from dated indicators rather than
   asserting them.

### Palaeochannels from satellite imagery

6. **Orengo and Petrie, "Large-scale, multi-temporal remote sensing of
   palaeo-river networks"**, *Remote Sensing* 9 (2017).
   https://www.mdpi.com/2072-4292/9/7/735
   The key paper. A seasonal multi-temporal method using long-term vegetation
   dynamics and spectral decomposition, which recovered more than 8,000 km of
   palaeo-channels in northwest India. This is the method for step 1 of the
   thesis, and it is written for exactly our region.

7. **"Reconstructing long-term settlement histories on complex alluvial
   floodplains"**, *Heritage Science* (2023).
   https://www.nature.com/articles/s40494-023-00985-6
   Joins the channel reconstruction to site distributions, which is the join
   we need between the coastline prior and the candidate sites.

8. **"Identification and Characterization of Palaeochannels"**, Springer (2025).
   https://link.springer.com/chapter/10.1007/978-3-031-92021-9_3
   Recent methods chapter. Multi-sensor fusion of SAR and optical data with
   moisture and vegetation indices, which is the practical recipe.

9. **"Potential of satellite based sensors for studying distribution of
   archaeological sites along palaeo channels"**, *Journal of Archaeological
   Science* (2010).
   https://www.sciencedirect.com/science/article/abs/pii/S0305440310002827
   Older and narrower, but it is the archaeological framing of the same method.

### Harbour geoarchaeology

10. **Marriner and Morhange, "Geoscience of ancient Mediterranean harbours"**,
    *Earth-Science Reviews* (2007), and their "Coastal and ancient harbour
    geoarchaeology".
    https://www.researchgate.net/publication/229990285
    The standard treatment of what a buried harbour basin looks like in a core.
    Defines the sedimentary signature our anchorability index is trying to
    predict.

11. **"Geoarchaeology confirms location of the ancient harbour basin of
    Ostia"**, *Journal of Archaeological Science* (2014).
    https://www.sciencedirect.com/science/article/abs/pii/S0305440313003087
    A port located by coring rather than by excavation. The closest precedent
    for what we would recommend in the decision layer.

12. **"The Development and Characteristics of Ancient Harbours: Applying the
    PADM Chart"**, PLoS ONE (2016).
    https://pmc.ncbi.nlm.nih.gov/articles/PMC5025247/
    The Palaeoenvironmental Age-Depth Model. A transferable framework for
    reading harbour sequences, and it is open access.

### Monte Carlo voyage simulation

13. **"Seafaring and navigation in the Nordic Bronze Age: the application of an
    ocean voyage tool and boat performance data"**, *PLoS ONE* (2025).
    https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0320791
    The methodological template. Combines predicted vessel performance with
    agent-based simulation, and compares open crossings against coastal routes,
    which is precisely the Malabar question about open sea versus backwaters.
    Open access.

14. **Palmer, "Windward sailing capabilities of ancient vessels"**, *IJNA*
    (2009).
    https://www.ancientportsantiques.com/wp-content/uploads/Documents/ETUDESarchivees/Navires/Documents/Palmer2009-WindwardSailing.pdf
    The polar performance data for square rig. This is the input the simulation
    needs and we do not otherwise have it.

15. **"Sailing the Simulated Seas: a new simulation for evaluating prehistoric
    seafaring"**.
    https://www.researchgate.net/publication/398199778
    Agent-based modelling for drift against directed voyaging, built on open
    data and freeware. Useful for implementation choices.

16. **"A multi-criteria simulation of European coastal shipping routes"**,
    *Humanities and Social Sciences Communications* (2024).
    https://www.nature.com/articles/s41599-024-02906-9
    Shows how to combine several costs, not just wind, into one route model.
    Open access.

### Part C. Finding lost ports by reconstructing the landscape

Case studies where a harbour was located, or its disappearance explained, by
reconstructing the coast and the river rather than by excavating for it. This is
the genre the thesis belongs to, and it is where the Component 1 argument comes
from.

### The framework to work from

1. **Giaime, Marriner and Morhange, "Evolution of ancient harbours in deltaic
   contexts: a geoarchaeological typology"**, *Earth-Science Reviews* 191
   (2019), 141-167. doi:10.1016/j.earscirev.2019.01.022
   The single most useful item on this list. It defines five harbour types on
   clastic coasts: fluvial harbours subject to floods and channel change,
   infilled estuarine, submerged estuarine, lagoonal harbours dominated by
   sediment input, and basins altered by dredging and breakwaters. Our seven
   ports sort cleanly into it. Muziris on the Periyar is a fluvial harbour
   affected by channel change, which is exactly the 1341 event. Nelkynda and
   Bakarē on the Vembanad are lagoonal. Barbarikon is estuarine on a delta that
   has since prograded. Using their typology gives the geographic prior a
   published structure instead of an improvised one.

2. **Marriner and Morhange, "Geoscience of ancient Mediterranean harbours"**,
   *Earth-Science Reviews* 80 (2007).
   The review that established the field. Read for what a buried harbour basin
   looks like in a core, which is the signature the anchorability index is
   trying to predict.

### Harbours located or explained by reconstruction

3. **"Holocene evolution of Portus Pisanus, the lost harbour of Pisa"**,
   *Scientific Reports* 8 (2018).
   https://www.nature.com/articles/s41598-018-29890-w
   Open access. A 10,500-year relative sea-level reconstruction and an
   8,000-year environmental reconstruction used to establish when the site
   became a sheltered embayment, and therefore when it could have been a
   harbour. This is the closest published example of the reasoning our prior
   performs, and it is the template to cite.

4. **Stanley et al., "Pelusium, an ancient port fortress on Egypt's Nile delta
   coast: its evolving environmental setting from foundation to demise"**,
   *Journal of Coastal Research* (2008).
   A port founded when tectonics gave it sea access and abandoned when
   progradation cut it off. The mechanism that probably ended Muziris, worked
   out in detail somewhere the evidence survives.

5. **"Palaeogeographic reconstruction of the Main Harbour of the ancient city"**,
   *Journal of Archaeological Science* (2023).
   https://www.sciencedirect.com/science/article/abs/pii/S0305440323001371
   Recent worked example of the method.

6. **"Geoarchaeology confirms location of the ancient harbour basin of Ostia"**,
   *Journal of Archaeological Science* (2014).
   https://www.sciencedirect.com/science/article/abs/pii/S0305440313003087
   A harbour located by coring rather than excavation. The precedent for what
   the decision layer should recommend at an untested Kerala candidate.

7. **"Geoarchaeology of Portus Mareoticus: ancient Alexandria's lake harbour"**,
   *Journal of Archaeological Science: Reports* (2017).
   A lagoonal harbour, which is the Vembanad case.

### The same problem, in South India

8. **Ramasamy et al., "Geoscientific perspectives of the submerged and lost
   harbours and ports: ancient port city Poompuhar, South India"** (2020).
   https://www.ancientportsantiques.com/wp-content/uploads/Documents/PLACES/IndOc-Gulf/Poompuhar-Ramasamy2020b.pdf
   A lost South Indian port sought through submerged delta reconstruction, with
   a harbour-like structure reported 25 km offshore on an older Cauvery delta.
   The nearest thing to our problem in our own subcontinent, and open access.

9. **"Tracing the Late Quaternary coastal evolution of Central Kerala"** (2024).
   https://www.sciencedirect.com/science/article/pii/S2666033424000352
   The regional coastal reconstruction for exactly the stretch that holds
   Muziris, Nelkynda and Bakarē. This is the paper the Malabar prior should be
   built on.

10. **"Roman metallurgy and early Anthropocene footprints in Kerala, South
    India"**, *Ambio* / Springer (2025).
    https://link.springer.com/article/10.1007/s44218-025-00115-8
    Lead levels at Pattanam falling in the medieval layers, read against the
    1341 flood. Independent dating evidence for the event that reorganised the
    Periyar, which the coastline reconstruction needs.

11. **Cherian et al., "Chronology of Pattanam: a multi-cultural port site on the
    Malabar coast"**.
    https://www.researchgate.net/publication/229061657
    The site's own dating, described as a palaeo-delta at the mouth of the
    north-flowing Periyar.

### Recovering the channels themselves

12. **Orengo and Petrie, "Large-scale, multi-temporal remote sensing of
    palaeo-river networks"**, *Remote Sensing* 9 (2017).
    https://www.mdpi.com/2072-4292/9/7/735
    Open access, and written for northwest India. Recovered more than 8,000 km
    of palaeochannels from seasonal vegetation dynamics and spectral
    decomposition. This is the method for the Indus delta, and the one to
    imitate rather than invent.

13. **"Reconstructing long-term settlement histories on complex alluvial
    floodplains"**, *Heritage Science* (2023).
    https://www.nature.com/articles/s40494-023-00985-6
    Joins reconstructed channels to the distribution of known sites, which is
    the join between our prior and our candidates.

14. **"Reconstruction of the lost Saraswati river course and its associated
    archaeological sites"** (2025).
    https://www.sciencedirect.com/science/article/abs/pii/S2352938525001120
    A river reconstructed from imagery and then used to explain a site
    distribution. The most ambitious version of the argument, and a useful
    warning about how far it can be pushed.

### What to read first

Giaime et al. for the framework, Portus Pisanus for the worked example, the
Central Kerala coastal evolution paper for our own region, and Orengo and Petrie
for the channel method. Three of those four are open access.
