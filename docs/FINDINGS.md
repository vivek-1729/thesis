# The Periplus port project

Everything this project has established, and the method behind it. One document;
the working notes written during evidence gathering have been folded in here and
deleted.

The companion is `DATA.md`, which inventories what is held, what is still
reachable and what does not exist. Per-port detail with verbatim passages is in
`docs/cities/`, one generated file per port.

Everything in quotation marks is verbatim from the source named.

**Contents**

| Part | Sections |
|---|---|
| I. The problem and the approach | 1–3 |
| II. The text | 4 |
| III. The material record | 5–10 |
| IV. The landscape | 11–22 |
| V. Port by port | 23 |
| VI. What went wrong, and what is left | 24–27 |

---

# Part I. The problem and the approach

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
---

## 2. Four lines of geographic evidence

Written for a reader coming to the project cold. This is the method; what it
produced is in Part IV.

**The coastline reconstruction is not a refinement of this project. It is a
precondition the standard commentary states and then does not act on.** Casson,
Appendix 1: "A further complication is that extensive changes have taken place
in the coastline." And quoting Smith, who "prudently observes that 'the
extensive changes which have occurred in the rivers of Sind during the course of
eighteen centuries preclude the possibility of satisfactory identifications of
either of these towns [Barbarikon and Minnagar].'" Both are correct, both are
load-bearing, and both are routinely ignored by arguments that measure across
the modern coastline.

### 2.1 Where was the coastline?

**The question.** The Indian coast has moved. Before anything else, we need to
know whether a candidate site was on the water at all in AD 50.

**The evidence.** Old sea charts, because they are the only record of this coast
before modern engineering: a Dutch chart of around 1700, British Admiralty
surveys of 1857, and satellite imagery from 1972 onward. Alongside them, the
land itself. A beach ridge is a fossil shoreline, a sand bank stranded as the
coast built seaward, and Kerala has two sets that geologists have already dated.

**Steps**
1. Pin each historic chart onto modern coordinates by matching features that
   still exist, recording how well the fit worked.
2. Trace the coastline from each chart and each satellite epoch.
3. Map the beach ridges from elevation data.
4. Attach published dates to each ridge set.
5. Assemble the results into a sequence of dated coastlines.

**Output.** A coastline for each date, drawn as a band rather than a line, since
an eighteenth-century chart is not accurate to the metre. Plus one hard
geological boundary: land seaward of the younger ridge set formed after the
mid-Holocene and did not exist in antiquity.

**Why it matters.** It eliminates candidates. A proposed port standing on ground
that formed after AD 50 is finished without any further argument.

**Statistics**
1. Combine scanning, pinning and tracing error into a single positional
   uncertainty for each coastline.
2. Represent each coastline as a band of that width.
3. Claim the coast has moved only where two bands fail to overlap.

---

### 2.2 How deep was the water, and could a ship get in?

**The question.** A harbour is useless if a loaded ship cannot enter it. This is
the test that genuinely separates the candidates.

**The evidence.** The historic charts carry depth soundings, individual
measurements written across the water; both the 1700 Dutch sheet and the 1857
Admiralty sheet have them. Sediment cores, columns of mud drilled from the
ground, whose layers can be radiocarbon dated to establish how fast the seabed
filled in. And a published sea-level curve for this coast.

**Steps**
1. Transcribe the soundings from each chart as located points.
2. Record each chart's depth reference, or flag it as unknown, since surveys of
   this period measured from different baselines.
3. Correct for tide, which is the largest single source of error in historic
   soundings.
4. Extract the stratigraphy and radiocarbon dates from each core.
5. Reconstruct how much sediment has accumulated at each location since
   antiquity.
6. Subtract that from where sea level stood to obtain the depth of water
   available at any date.

**Output.** For each candidate, at each date, the probability that a ship of a
given draught could enter. A Roman merchant vessel drew roughly two to four and
a half metres.

**Why it matters.** This is the strongest discriminator available. Pliny writes
that Bakarē was "a more useful port" than Muziris; this converts that sentence
into a testable claim.

**Statistics**
1. Interpolate the soundings by a method that returns its own uncertainty, so
   depth far from any measurement is correctly reported as less certain.
2. Fit an age-depth model to each core: a curve from depth to date that can only
   increase, with error bars.
3. Fit a sea-level curve that carries the dating error of each point through to
   the result.
4. Combine all three, propagating every uncertainty, into a posterior on water
   depth.
5. Report the probability that a given draught could enter at a given date.

---

### 2.3 Where did the rivers run?

**The question.** The Periplus gives the Indian distances "by river and by sea".
They cannot be measured until we know where the water was.

**The evidence.** Satellite imagery, because a buried river leaves a damp line
that crops grow differently over. And the historic charts, which drew the
waterways directly.

**Steps**
1. Assemble several years of satellite imagery for each region.
2. Separate the images by season, since the signal is a soil-moisture effect
   strongest in the dry months.
3. Extract the pattern that recurs across dates, which is the buried channel,
   from the noise that does not.
4. Validate against a channel already known to exist, with the pass mark fixed
   in advance.
5. Where that fails, trace the waterways from the historic charts instead.
6. Build a network of navigable water for each date.

**Output.** A map of navigable water per epoch, usable as a network to measure
routes through.

**The result so far.** It works in the arid Indus delta, scoring 0.81 against a
pass mark of 0.75 set beforehand. It fails in Kerala at 0.58 and 0.46, because
that landscape has been cut through with paddy bunds and canals that resemble
ancient rivers. Four separate methods have now failed there, so Kerala rests on
the charts.

**Why it matters.** It converts a stated distance into something measurable
along a real route rather than a straight line across land.

**Statistics**
1. Keep the detector's output as a probability for each pixel rather than a
   binary map.
2. Validate against a known channel, with the threshold fixed before running.
3. Measure routes through each epoch's network separately.
4. Treat the disagreement between epochs as the genuine uncertainty on the
   landscape.

---

### 2.4 How fast did ships actually sail?

**The question.** The Periplus measures in stadia, but ancient sailors estimated
sea distances from elapsed time. The unit is therefore a speed, and we need to
know what speed.

**The evidence.** Modern wind records, reliable here because the monsoon has
changed little in two thousand years. And the measured performance of
square-rigged vessels.

**Steps**
1. Assemble wind climatology for the basin.
2. Attach a performance curve for a square-rigged ship.
3. Simulate many voyages between ports whose locations are secure.
4. Record the distribution of elapsed times.
5. Compare it against the durations the text actually states.

**Output.** A conversion from "three days' sail" into a distance with a range
attached.

**Why it matters.** Every distance in the text currently rests on an assumed
conversion. This replaces the assumption with a measurement.

**Statistics**
1. Run the simulation repeatedly to obtain a distribution of travel times rather
   than a single figure.
2. Compare that distribution against the stated durations.
3. Optionally, estimate the ship's performance from those durations, which
   requires a method for fitting models that can be simulated but whose
   likelihood cannot be written down.

---

### How the four combine

Lines 1 and 2 establish where a port could have been and whether a ship could
reach it. Line 3 supplies the routes along which distances are measured. Line 4
fixes the units the ancient text is written in.

Together they yield a probability map of where each lost port stood, with every
source of uncertainty carried through rather than assumed away.

---

## 3. The statistical plan

One method per evidence stream, then an integration layer and a decision layer.

### Evidence streams

- **Textual distances**
  - *Approach:* Errors-in-variables regression with an interval-censored response.
  - *Details:* Stated stadia are rounded to the nearest 100, so the likelihood is the probability that the true distance divided by the stadion length falls inside the rounding interval. The stadion length is a parameter to be estimated, not a constant assumed in advance.
  - *Output:* A distance-consistency likelihood for each candidate location, and a posterior distribution for the stadion.

- **Archaeological record**
  - *Approach:* Occupancy model with imperfect detection.
  - *Details:* Detection probability is logistic in the number of excavation seasons, whether virgin soil was reached, and the decade of work. The detection model is fitted on the 7,053 extracted IAR entries and applied to the 23 candidate sites.
  - *Output:* A posterior probability that each candidate was an occupied port, with absence of evidence discounted in proportion to survey effort.
  - *The column that makes this honest:* `targeted_at_port`. Kodungallur was dug
    in 1969–70 *because* it was the traditional Muziris and returned nothing
    earlier than the ninth century; Banbhore was dug as Islamic Daybul and the
    Barbarikon identification came later. Those two absences are not the same
    kind of evidence, and no amount of care about excavated area distinguishes
    them. Excavation effort is not independent of prior belief about location, so
    if detection is estimated separately and then fed into a location model, the
    field's existing opinion enters the likelihood disguised as evidence. The
    column has usable variation: of the twelve candidates excavated at all, six
    were targeted at the port and six were not.

- **Coin hoards**
  - *Approach:* Log-Gaussian Cox process with thinning.
  - *Details:* Hoard intensity is modelled on distance to the coast, proximity to the Palghat gap, and elevation, then thinned by a modern discovery probability to correct for reporting bias.
  - *Output:* An intensity surface, and a test of whether hoard locations carry any locational signal at all.

- **Hydrology**
  - *Approach:* Supervised classification of relict channels.
  - *Details:* Multispectral satellite imagery classified against labelled palaeochannel training data; classification probabilities are retained rather than thresholded into a binary mask.
  - *Output:* A probabilistic covariate giving the chance that a navigable channel existed at a given location in antiquity.

- **Bathymetry**
  - *Approach:* Uncertainty propagation.
  - *Details:* Digital elevation model error and sea-level reconstruction error are pushed through to an anchorability index rather than treating depth as exactly known.
  - *Output:* An anchorability covariate carrying explicit error bars.

- **Wind and voyage**
  - *Approach:* Monte Carlo agent-based simulation.
  - *Details:* ERA5 wind climatology combined with a square-rig polar performance curve, run over thousands of simulated voyages.
  - *Output:* A reachability distribution, which replaces the conventional assumption of a fixed 500 stadia sailed per day.
  - *Open decision:* as written this is forward simulation producing a covariate, not
    inference. It becomes simulation-based inference only if the simulator's own
    parameters, the daily run, leeway, and the seasonal departure window, are
    estimated by comparing simulated voyage durations against the durations the
    Periplus states. That version would let the stadion and the voyage model be
    estimated jointly rather than separately, and it is the only place in the plan
    where ABC would be doing real work. Not yet committed to.

### Integration layer

- **Approach:** Bayesian spatial logistic regression with a conditional autoregressive prior.
- **Details:** The covariates produced above enter as predictors, the occupancy layer supplies the observation model, and the whole is fitted by MCMC in Stan.
- **Output:** A posterior surface over coastal locations, and a posterior over identification sets that includes the possibility that the true site is none of the named candidates.

### Decision layer

- **Approach:** Bayesian optimal search allocation.
- **Details:** For each possible survey location, compute the expected reduction in posterior entropy that excavating there would produce.
- **Output:** A ranked list of where to excavate next, with expected information gain attached to each location.

---

# Part II. The text

## 4. The Periplus as a measuring instrument

### 4.1 The text rounds large distances and not small ones

33 of 51 distance statements are in stadia. **82 per cent are multiples of 100.**
Every value at or above 200 is a round hundred, without exception. The only
unround figures are 20, 60 and 120, all small and all local: 20 stadia upriver at
Muziris, 120 stadia upriver at Nelkynda, 60 elsewhere.

Two classes of number with different precision. Large coastal legs are estimates
to the nearest hundred. Short local measures may be direct knowledge.

The implication inverts the usual order of argument: **the upriver notices
deserve more weight than the 500-stadia legs**, which is the reverse of how the
literature uses them.

*Source: `data/processed/distances.csv`.*

### 4.2 Most distance statements are not sailing legs

Only 22 of 51 are legs between ports. The rest are 7 inland, 5 offsets, 5
extents, 5 widths, 3 upriver, 2 runs. 18 of 51 are in days rather than stadia.
Any treatment of the Periplus as a list of sailing distances is using under half
the corpus.

### 4.3 The stadion calibrates to about 155 m, not the conventional 185 m

Median of four legs with securely identified endpoints. That shifts every derived
position by about 16 per cent, which is enough to change which candidate fits.

Casson works from the ancient rule of thumb instead, stated in his Appendix 2:
"Their rule of thumb was 1000 stades to a day-and-night run, 500 to a day's run,"
and "approximately ten stades correspond to a nautical mile," which implies about
185 m.

**Not yet run, and the highest-value unrun analysis we have: per-leg implied
values rather than a single median.** Whether the implied stadion drifts by
region, leg length or leg type is the open question.

### 4.4 Casson's own table is internally inconsistent

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

### 4.5 "By river and sea" — the single most consequential textual finding

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

### 4.6 Straight-line against sailed distance is still unresolved

Every distance argument in this literature compares a straight line against a
distance the text records as sailed. Measuring along every vertex of the modern
coastline roughly doubles the figure — Ponnani is 75 km straight and 155 km by
coastline vertices — but that path follows every estuary and no vessel would.
The true value sits between and nearer the low end. **Distance results should
therefore be stated as rankings, not as fits.**

### 4.7 The stadion is not a length. It is a speed

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

### 4.8 Four further problems in Casson's use of the distances

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

### 4.9 What the error structure means for locating anything

The error is multiplicative, with **sd of log(stated/actual) = 0.311** across
Casson's eleven legs. A 500-stadia leg at a 155 m stadion is 77.5 km, with a
68 per cent band 49 km wide and a 95 per cent band 100 km wide. Candidates for a
single Kerala port sit 25 to 150 km apart, so **one 500-stadia leg cannot
separate adjacent candidates**. The 120-stadia Nelkynda-to-Bakarē figure has a
68 per cent band only 12 km wide.

That is the quantitative form of the finding in 2.1: the short local numbers
outrank the long ones, and now there is a number attached.


---

---

# Part III. The material record

## 5. The archaeological record

### 5.1 What was extracted

Searching *Indian Archaeology: A Review* for candidate names only finds sites
somebody had already connected to a Periplus port, and a site can be excavated
without anyone making that connection. So the whole state sections were lifted
instead.

**7,053 numbered entries** from the 50 volumes that parsed cleanly, running from
1957–58 to 2013–14 with eight years missing from the sequence, each with year, state, chapter, title, district, body and a period
classification derived from its own text. `data/processed/iar_entries.csv`, built
by `src/extract_iar_entries.py`.

This makes the question regional rather than site-by-site: not "has anyone dug at
Ponnani" but **"what has been found on this coast, of what date, since 1953."**

### 5.2 Kerala in full

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

### 5.3 Kerala is not under-investigated; it is under-yielding

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

### 5.4 Absence is mostly absence of excavation

**Thirteen of the twenty-two disputed candidates have never been excavated.**
Niranam, Neendakara, Purakkad, Pirakkad and Thevalakara have **zero appearances**
across the 50 volumes. Kallada has two, a neolithic axe from the river basin and a temple inscription, neither an excavation.

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

### 5.5 Two tested negatives, which are a different thing from untested absence

- **IAR 1978–79 no. 40.** The ASI Southern Circle explored Malappuram and Palghat
  "while investigating for the sites showing **Roman contact in the Ponnani
  valley**," recording megalithic topikal burials at Alancode, Ongallur,
  Ponumundum, Tennala, Thannairkod and Thavanur, and menhirs near Thirunavaya.
  No Roman material.
- **IAR 1969–70 no. 18.** A traditional identification tested and failed. Five
  localities around Cranganore excavated; all material ninth to eleventh century
  Chera. The next volume records the trial digs "had not yielded any tangible
  evidence."

### 5.6 Excavation is blocked by water, not by absence, at several sites

At Banbhore, Khan's trenches (1958–66) never reached virgin soil: "the virgin
soil was not reached due to heavy water infiltration, and information on the
early stages of life at Banbhore remained incomplete" (Felici et al.). The
Italian mission has not reported reaching it either. Mughal 2018 (*Pakistan
Archaeology* 33) publishes Red Polished Ware of the first century BC to second
century AD from the earliest reached levels. The same water-table problem holds
at Sumhuram and Myos Hormos.

The decisive fact at Banbhore is not what was recovered but that the trenches
stopped at the water table, which changes the meaning of everything above them.

### 5.7 No counterpart series exists outside India

*Indian Archaeology: A Review* has no equivalent for Arabia, Pakistan or East
Africa. For **Leukē Kōmē, Barbarikon and Rhapta** the equivalent has to be
assembled by hand from excavation reports and from the expeditions named in the
dossier passages: who dug, when, how many seasons, what depth or period was
reached, whether virgin soil was hit, and where it was published.

---

## 6. Material assemblages

### 6.1 The typology comes first

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

### 6.2 Pattanam, the only quantified candidate

Nine KCHR seasons, 2007 to 2015, sixty trenches over under one per cent of the
mound. Natural soil was reached at 317 cm and radiocarbon on charcoal at 340 to
370 cm puts first settlement near 1000 BC, so unlike Banbhore the sequence is
complete and the Periplus horizon lies inside it. The wharf context, with a
six-metre anjili canoe and nine teak bollards radiocarbon dated to the first
century BC or first century AD, is the strongest structural evidence for any
candidate in the study.

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

### 6.3 How the extraction was done and how well it worked

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

## 7. Coins

### 7.1 Roman coins in India do not mark ports

Of 121 Indian hoards in the Coin Hoards of the Roman Empire database, 98 lie more
than 25 km from the coast, and they account for **73 per cent of all recorded
coins**. The densest concentration is 100–200 km inland — 4,802 coins in 29
hoards — in Coimbatore district and the Palghat gap. It holds at the Periplus
horizon: of 40 hoards closing AD 1–69, 76 per cent of coins are inland.

Roman coins in India travelled inland towards the sources of pepper and beryl and
were buried there. They record the movement of bullion and the habit of hoarding,
not the location of harbours.

*Source: `data/processed/chre_hoard_distances.csv`. The CHRE bulk export was
cleaned first: of 627 hoards, 128 lay outside the study region (Britain and the
Adriatic), 69 had no coordinates, and the Kottayam 1847 hoard was dropped for a
georeferencing error of about 260 km. 427 hoards and 7,778 coins remain, built
by `src/clean_chre.py`.*

Six figures carry this evidence, `20_` to `25_` in `figures/`, built by
`src/make_coin_figures.py`. Two results were added while making them. Measured
against hoards that close by AD 200, the nearest such hoard to any Rhapta
candidate is 2,223 to 2,496 km, while Pattanam has one 7 km away. And **98 per
cent of the Indian coins with a named mint were struck at western mints**,
overwhelmingly Rome and Lyon, against 15 per cent in Egypt's own hoards, where
41 per cent came from Alexandria. Egyptian circulating currency did not travel
east; what moved was western gold acting as specie.

### 7.2 Sri Lanka is the opposite case and must not be pooled

67 hoards, 220,901 coins, 85 per cent coastal. But these are enormous late-Roman
**bronze** hoards of the fourth and fifth centuries — Beragama 70,000, Godavaya
30,000, Tissamaharama 30,000. Aggregating them with Indian Julio-Claudian gold
produced a completely misleading first result.

### 7.3 Hoards and site finds are different evidence classes

India: 790 gold, 184 silver, almost no bronze; 756 aurei, 180 denarii. Aynuna,
the only excavated Arabian assemblage: 24 bronze, 1 silver. The first is stored
wealth, the second is money being spent. For locating a harbour the second is far
more informative, and it is precisely the category the hoard databases omit.

Indian Roman coins occur overwhelmingly as hoards and rarely in excavation; the
Red Sea is the reverse.

### 7.4 Coverage gaps are structural, not search failures

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

### 7.5 Indian reign distribution is bimodal

985 specimens. Claudius 134, Tiberius 116, Augustus 114, Nero 92, for 456
Julio-Claudian, then a second peak at Hadrian 116 and Antoninus Pius 75.

### 7.6 What we hold

`data/processed/site_find_coins.csv`, 30 records: Aynuna's 25 excavated coins
plus assemblage totals for Myos Hormos, Berenike and Sumhuram. Smagur 2025 in
*JRA* supplied Myos Hormos: 153 coins plus a lead token from the Chicago
excavations of 1978–82, with the striking detail that the 1999–2003 Southampton
excavations produced only 14 coins identifiable enough to publish.

**Aynuna is the one disputed candidate with real excavated coins.** Pattanam has
hoard evidence nearby, PARUR's 1,000+ gold coins 3 km away. Every other disputed
candidate has nothing, and for the East African ones there is nothing to find.

---

## 8. Later settlement, and the circularity it reveals

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

## 9. The Aynuna coin catalogue, read

The 450-page Aynuna report had been held and unread, and its coin catalogue was
described as possibly decisive for Leukē Kōmē. It has now been extracted to
`data/processed/aynuna_coins.csv`, twenty-eight coins with section, issuing
authority, metal, diameter and find context.

**The extraction is checked rather than trusted.** Gawlikowski states his own
totals in the paragraph after the catalogue: twenty-eight coins, two completely
obliterated, fourteen of the remainder Nabataean. The script reproduces all
three, and an earlier version did not. That version read twenty-five coins,
missed the opening entry because it sits under a section heading on the page
before the running head, missed a coin found stuck to another and published
under a shared inventory number, and carried a ruler list stopping at Hadrian,
so every fourth-century coin fell through as unattributed.

**The dated sequence.** Twenty-two of the twenty-eight carry a date.

| Authority | Count | Dates |
|---|---|---|
| Local Northwest Arabian imitation | 1 | 3rd–2nd c. BC |
| Anonymous Nabataean | 6 | 2nd–1st c. BC |
| Obodas III | 1 | 30–9 BC |
| Aretas IV | 4 | 9 BC – AD 40 |
| Elagabalus | 1 | AD 218–222 |
| Constantinian house | 4 | AD 306–340 |
| Khusro II imitation | 1 | AD 590–628 |
| Baybars | 1 | 1260–1277 |
| Ottoman and Egyptian | 2 | 1805–1861 |

**No coin at Aynuna was struck by an authority whose reign includes AD 50.** The
latest minting date before the Periplus is Aretas IV's death in AD 40, and the
next coin on the site is Elagabalus, 178 years later.

**The sharper form of this is Gawlikowski's own.** He writes that none can be
safely attributed to any Nabataean king after Aretas IV. The kings after Aretas
IV are Malichus II, AD 40 to 70, and Rabbel II, AD 70 to 106. Malichus II
reigned across the Periplus almost exactly, and his coinage is absent here.

**What this does not establish.** Coins circulate long after they are struck, so
an Aretas IV bronze lost in AD 50 is unremarkable and the site was plainly in
use. The absence is of coins *minted* in the Periplus window, not of occupation
during it, and twenty-eight coins is a small sample from four seasons. What it
does show is that the numismatic evidence at Aynuna peaks before the Periplus
and resumes long after, which is a different shape from the one a port at its
height in AD 50 would leave.

**A bug this surfaced.** `docs/cities/leuke-kome.md` reports zero proposed sites
and zero excavations, while `disputed_candidates.csv` holds four candidates for
the port including the excavated one. The city-record builder is not matching
the port name. Recorded here rather than fixed, since it affects the generated
documents and not the underlying tables.

## 10. The Sangam corpus, read in Tamil rather than at second hand

`DATA.md` recorded the Sangam poems as held at second hand only, meaning every
Sangam reference in this project was quoted from a modern scholar. Project
Madurai publishes the corpus in Tamil, public domain, so 40 files covering 17
works are now in `library/sangam`, with counts in
`data/processed/sangam_port_mentions.csv`.

This does not replace a translation. The standard English versions are in
copyright and the poems still have to be read. What the original gives is the
one thing a translation cannot be searched for reliably: which poems contain the
port names, counted rather than recalled.

**Most of the names cannot be counted, and finding that out was the work.** A
first pass searched for all eight names and reported 57 occurrences of Naura and
313 of Vanci. Both are artefacts. *Naravu* is the ordinary word for toddy, and
the Tamil commentaries printed alongside the poems gloss it as *kal*, toddy, in
nearly every instance. *Vanci* is an oath, a deceit, a creeper and a category of
poetry before it is the Cera capital. *Pakai* in this spelling appears inside a
poet's epithet, a sweet syrup and a headwrap. Those three are now marked
uncountable in the script rather than silently dropped.

**What can be counted.**

| Name | Occurrences | Distinct works |
|---|---|---|
| Yavana, a western foreigner | 295 | 16 of 17 |
| Korkai, the Pandya pearl port | 40 | 8 |
| Tondi, behind Tyndis | 23 | 6 |
| **Muciri, behind Muziris** | **9** | **2** |
| Nelkinda | **0** | 0 |

**Muciri appears in Akananuru and Purananuru and nowhere else in the corpus.**
That is the whole indigenous textual basis for the identification of Muziris,
and it matches the passages the scholarship cites. The counts include the modern
Tamil commentary printed with each poem, which repeats the name when glossing
it, so nine occurrences is an upper bound on nine distinct mentions.

**Nelkynda is absent entirely**, under this spelling, from all seventeen works.

This bears directly on the standing note in `CLAUDE.md` that Muziris is treated
as secure and included because the security is narrower than it looks. The
indigenous corpus names it in two works. It names the Yavanas who came to trade
in sixteen.

---

# Part IV. The landscape

## 11. Imagery finds buried channels in arid terrain and cannot do it in Kerala

Multi-season optical PCA scores **AUC 0.814 in the Indus delta** and **0.752 in
Cholistan**, against a threshold of 0.75 fixed before any run. It scores **0.583
at the Periyar** and **0.456 at the Pamba**.

So **Barbarikon can be worked with imagery and the four Malabar ports cannot.**
That is the single most consequential outcome, and it redirects effort from
satellites to archives for most of the thesis.

## 12. Kerala defeats four independent methods

| Method | Result |
|---|---|
| Multi-season optical PCA | 0.576 Periyar, 0.456 Pamba |
| L-band radar (ALOS PALSAR) added | 0.583 Periyar, 0.455 Pamba |
| Detrended Copernicus DEM | 0.537 Periyar, 0.430 Pamba |
| Borehole lithology | the buried sands are beach deposits |

**And the reason is not what I assumed.** I added radar because canopy seemed the
obstacle. It moved the Periyar by 0.007. Figure 28 shows the real problem: the
terrain is full of sharp linear structure and all of it is the Kuttanad polder
system, paddy bunds and canals in a dense mesh. An across-shore spectrum returns
2.1, 3.5 and 7.9 km, which are polder scales. **The Malabar surface has been
re-cut into features that look exactly like palaeochannels.**

The subsurface route fails separately. Eight of seventeen boreholes hold a sand
body sealed under finer sediment, the classic buried-channel signature, but
Maya and colleagues identify them as beach and littoral deposits from
transgressive and regressive cycles, and marine fauna appear in every thick one.

## 13. Nothing dates to the Periplus

This recurs across every stream and should be stated once, plainly.

- **Kerala cores.** 27 radiocarbon dates across 15 sites. The three youngest are
  2460, 2580 and 2730 BP, roughly 510, 630 and 780 BC. **Nothing within five
  centuries of AD 50.**
- **Indus shelf.** Core Indus-23 carries a hiatus from 8 ka to 1.3 ka. The
  Periplus falls inside the gap.
- **Historic charts.** 1857 for the Admiralty sheets, around 1700 for the
  earliest Dutch one. Seventeen centuries late at best.
- **JRC water record.** Begins 1984, eight years after the Thanneermukkom
  barrage and the Idukki dam.

Every geographic layer is therefore a prior on the landscape, not a measurement
of it at the right date, and the posterior has to carry that.

## 14. What the archives gave, which was more than expected

I had been treating historic charts as a reading-room problem. They are not.

**Admiralty sheets, Wikimedia Commons, public domain, 80 to 176 megapixels.**
Malabar 749, 750 and 751 of 1857 covering the whole coast; Indus 41 and 118 of
1897, which is Oldham's survey and the exact material Giosan and colleagues
digitised; Red Sea 8a to 8c of 1873. Sheet 749 is the one covering Muziris and
Tyndis that I had reported missing.

**Gallica: 915 sheets catalogued, 791 of them dated before 1800.** 249 Malabar,
387 Red Sea, 147 Arabia, 50 Zanzibar, 36 Cochin, 27 Indus and Sind. Served over
IIIF at 50 to 95 megapixels. Twelve downloaded so far.

**David Rumsey: 49 sheets**, JSON search and IIIF both working.

**The best single item is the pre-1700 Dutch chart**, *"avec les Sondes"*,
covering 9°N to 16°N. Figure 29 crops its southern end at full scale and it
lands on our candidates: Cranckenoore for Kodungallur, Porcae for Purakkad with
the Dutch legend *Hyerbegint het Ryck Porcae*, the barrier spit, the backwater
behind it, and soundings in fathoms along the whole approach.

**Those soundings carry an argument.** Off Purakkad, 6 to 12 fathoms close
inshore, roughly 11 to 22 m, ample for any ancient vessel. At the Cranganore and
Vypin entrance, 3 to 5 fathoms, roughly 5 to 9 m, with shoals drawn at the mouth.
That is the pattern Gurukkal and Whittaker propose for Bakarē displacing Muziris,
a silted bar against a deep approach, recorded as measurement at the earliest
date anyone sounded this coast. It is around 1700, not AD 50, and proves nothing
about antiquity, but it is the earliest bathymetry for Malabar we have found.

## 15. Two claims in the literature that pull against each other

**The coast may have been finished before the Periplus.** Shajan and colleagues,
reporting Mathai and Nair 1988: the sand ridges and backwaters "emerged between
7000 and 2000 years BP", and "the development of the coast was almost completed
by 2000 years BP". If that holds, the first-century shoreline near the Periyar
is close to the modern one and the Muziris reconstruction problem is small.
Everything rests on one 1988 paper that the later literature cites without
rechecking, which is a pattern that has misled us before.

**The Vembanad is held to be unreconstructible.** Gurukkal and Whittaker on the
1341 cyclone that opened the Kochi gap: "it is almost anyone's guess where a
plausible port of Becare might have been situated", and "the huge changes in the
Vembanad waterways make it impossible to base much upon this evidence". That is
the consensus, and it applies exactly where Nelkynda and Bakarē sit.

Reconciling these two is the first substantive question for the Malabar chapter.

## 16. Modern water, measured

From the JRC 1984-2021 record, in km². Figure 26.

| Region | Ever water | Permanent | Seasonal | Lost since 1984 |
|---|---|---|---|---|
| Rhapta, Rufiji | 805 | 616 | 189 | 6.0% |
| Nelkynda and Bakarē, Pamba | 780 | 494 | 287 | 1.9% |
| Barbarikon, Indus | 565 | 226 | 339 | **9.8%** |
| Tyndis | 451 | 434 | 17 | 0.6% |
| Muziris, Periyar | 295 | 250 | 46 | 2.2% |
| Leukē Kōmē, Aynuna | 210 | 209 | 1 | 0.1% |

**The Pamba box is 37 per cent seasonal**, swinging from 494 to 780 km². Any
sailed distance through that system has to be quoted with a season attached.
**Aynuna is static**, which supports treating the Leukē Kōmē landscape as broadly
unchanged and spending the effort elsewhere. **The Indus is the most mobile of
the seven.**

## 17. Lessons worth keeping, methodological and technical

**Pre-registering the threshold is why the Kerala result is a finding** rather
than a disappointment to argue around.

**HydroRIVERS is not usable as ground truth.** Built from a 500 m DEM, its lines
sat a median of 417 m from any water and traced irrigation canals. It fails even
where the detector demonstrably works.

**A "principled" rule can be worse than an arbitrary one.** Choosing the PCA
component by spatial linearity picked PC1, which is brightness, and dropped the
Indus score from 0.814 to 0.719. Open water is linear too.

**Check what a test site actually looks like before building a test on it.** The
first site, the Ghaggar near Anupgarh, was chosen because it is in Orengo and
Petrie's study region and turned out to be wall-to-wall irrigated field grid.

**Four technical notes**, hard-won and easy to lose.

- GDAL's boundless read path builds a VRT per call and is **not thread-safe**.
  Require scenes that fully contain the box instead; Sentinel-2 tiles are 110 km
  and our boxes are 20 km, so most do.
- The Copernicus DEM is in a public S3 bucket and needs
  `AWS_NO_SIGN_REQUEST=YES`.
- Planetary Computer assets need `planetary_computer.sign_inplace`, which issues
  an anonymous token; no account.
- Negative controls should be a random pixel sample. Shape-matched placement
  never succeeds against a mask that is one large connected component, and a
  per-pixel AUC does not see shape anyway.


## 18. What would change the picture, ranked by what it would settle

The project's own decision layer, turned on its acquisition list. The question
is not which paper is most interesting but which one would most narrow the
posterior, and those are different orderings. An item that would move one port
from "unlocatable" to "bracketed" beats one that refines a port already
bracketed.

**Tier 1, would change a conclusion.**

1. **Priju et al. 2018**, buried channels in the Periyar basin by electrical
   resistivity. Still the highest-value item outstanding, and §11 and §12 are
   why: four surface methods failed in Kerala because the Kuttanad polders
   re-cut the ground into palaeochannel-like features. Resistivity reads the
   sand body under that surface. It is the only method anyone has applied here
   that is immune to the thing which defeated us, and it bears on Muziris, the
   port whose security §4 and §10 both show to be narrower than it looks.

2. **Maya et al. 2022**, the five lower Kuttanad boreholes by name. These sit
   inside the Nelkynda and Bakarē zone, which is the only part of the Malabar
   coast where no dated subsurface evidence exists at a candidate. Everything we
   hold for Kerala comes from Maya et al. 2017, whose nearest cores are not at
   the candidates.

3. **Shaji et al. 2022**, the Kerala sea-level curve. §22 established that the
   standardised regional database stops short of Malabar, so this is the datum
   and there is no substitute. Without it the coastline reconstruction in §2.1
   has no vertical reference and the depth work in §19 and §20 has nothing to
   reduce historic soundings to.

**Tier 2, would remove an assumption the thesis currently carries.**

4. **Mathai and Nair 1988.** The claim that the Kerala coast was "almost
   completed by 2000 years BP" is load-bearing: if true, the first-century
   shoreline near the Periyar is close to the modern one and the whole Muziris
   reconstruction problem shrinks. The later literature cites it without
   rechecking, which is the pattern recorded in §24 as having misled this
   project before.

5. **Narayana et al. 2001** and **Das et al. 2024**, both at the Periyar mouth
   and both open access, so both are a click rather than a request. Das reaches
   1.1 cal kyr BP, about 1,350 years younger than the floor of the cores we
   hold, which does not touch the Periplus but is the closest anything comes.

6. **Turner 1989, Appendix 1.** Single and stray coin finds are the one
   numismatic category that bears on harbour location, and §7 shows why the
   hoards do not. CHRE omits the category entirely.

**Tier 3, would put measurement where there is none, without settling a
location.** The first two of these are the answer to §19, and they are listed
below Tier 2 only because depth constrains a port rather than naming one.

7. **ICESat-2 ATL24, and it is the best answer to §19.** NASA's along-track
   coastal bathymetry product derives seafloor returns from the ATLAS photon
   lidar, with refraction correction and per-point uncertainty already applied,
   and reported accuracies of roughly 0.3 to 1 m RMSE in clear shallow water.
   An exhaustive search for better bathymetry turned up nothing else that is
   both open and actually measured. Coverage over the port boxes is not the
   constraint: 220 to 606 granules each, 2018 onward. **Water clarity is.** The
   Red Sea at Aynuna and the Mafia channel are the plausible cases; Kerala in
   monsoon turbidity is the doubtful one, and that is the test to run first.
   Needs a free NASA Earthdata registration, which is the same five minutes as
   the USGS account already on the blocked list.

8. **Sixteen NOAA bathymetry tracklines that nobody has ordered**: four across
   the Nelkynda and Bakarē approach, the one place on this coast where the
   depth question is sharpest, and twelve across the Pemba and Unguja channels,
   which is the water the Menuthias notice measures across. See §19.

9. **TanDEM-X at 12 m.** The Copernicus DEM failed at 30 m because a channel is
   one to two metres deep and detrending leaves a residual standard deviation of
   1.2 to 4.7 m. The failure is resolution, not method, so 12 m is the test of
   whether terrain can contribute anywhere. A DLR proposal, and speculative.

10. **CORONA, 1960–72 at 2 to 8 m.** The sharpest pre-dam imagery available, and
   the only optical record before the Thanneermukkom barrage and the Idukki dam
   that is finer than Landsat's 79 m.

11. **Ibn Battuta**, on this coast in 1342, within a year of the flood that §15
   says reorganised the Vembanad.

**What has dropped off this list, and why that is worth recording.** Three items
sat here until recently as things that might change the picture, and each was
resolved by doing the work rather than by acquiring anything. The tide was
behind a registration and is now fitted from observation, §20. The depth layer
was assumed to be a download away and turned out to contain no measurement at
all, §19. Datoo 1970 was cited at second hand through every Rhapta argument in
the literature, and reading it directly changed what the bracket means, §23.
The lesson transfers: before acquiring, check whether the thing is already
answerable.

## 19. There is no measured bathymetry at any approach, and the grid that fills the gap is wrong where it matters

The depth layer was listed as available and unused, on the assumption that
gathering it was a download away. It was, and the download is worth almost
nothing, which is the finding.

GMRT serves a 61 m grid over all seven port boxes against GEBCO's 450 m, so it
looked like a clear improvement. It publishes two layers, though: the filled
grid it will hand you, and the same grid with the interpolated cells removed.
Differencing them says which cells rest on a real sounding.

| Region | Sea cells | Median depth | Measured | Cells under 20 m | Of those, measured |
|---|---|---|---|---|---|
| Muziris, Periyar | 455,968 | 27.9 m | **0.0%** | 102,917 | **0.0%** |
| Nelkynda and Bakarē, Pamba | 550,211 | 35.0 m | **0.0%** | 127,843 | **0.0%** |
| Tyndis | 533,764 | 29.0 m | **0.0%** | 121,556 | **0.0%** |
| Barbarikon, Indus | 431,731 | 11.6 m | **0.0%** | 310,479 | **0.0%** |
| Leukē Kōmē, Aynuna | 143,145 | 8.3 m | **0.0%** | 110,320 | **0.0%** |
| Rhapta, Rufiji | 511,556 | 7.9 m | **0.0%** | 425,155 | **0.0%** |

Two and a half million marine cells across the seven approaches, and not one of
them carries a measurement. The 61 m cell is a 450 m cell wearing a smaller
coat, and a depth read off it would have been an artefact of exactly the kind
recorded in §24.

**The method is not at fault, which was checked rather than assumed.** The same
two layers over Monterey Bay and the Hudson shelf valley come back 100 per cent
measured. An empty mask on these coasts means an empty mask.

**An independent archive, and it does not quite agree.** GMRT's mask could in
principle reflect what GMRT ingests rather than what exists, so the holdings of
the NOAA National Centers for Environmental Information, the largest public
bathymetry archive and a separate compilation, were queried over the same boxes.

| Box | Multibeam | Bathymetry tracklines |
|---|---:|---:|
| Muziris, Periyar | 0 | 0 |
| **Nelkynda and Bakarē, Pamba** | 0 | **4** |
| Tyndis | 0 | 0 |
| Barbarikon, Indus | 0 | 0 |
| Leukē Kōmē, Aynuna | 0 | 0 |
| Rhapta, Rufiji | 0 | 0 |
| Pemba and Unguja channels *(nearby)* | 0 | 12 |
| Mumbai shelf *(nearby)* | 0 | 6 |
| Monterey Bay *(control)* | 34 | 21 |
| Hudson shelf valley *(control)* | 16 | 45 |

**Four surveys across six port approaches, and no multibeam anywhere.** The
controls return 116, so the query is sound and the zeros are real. But the
Pamba box is not zero, and that correction matters more than the pattern it
spoils: a first pass tested only four of the six boxes, found nothing in any of
them, and would have gone into this document as "zero at every port". Four
tracklines cross the Nelkynda and Bakarē approach, which is the one place on
this coast where the depth question is sharpest, because Pliny calls Bakarē the
more useful port and §20 measures that contrast on a chart from 1700.

**The nearby counts carry the rest of it.** Twelve tracklines cross the Pemba
and Unguja channels and six the Mumbai shelf, so single-beam survey on these
coasts is not absent in general. It is absent at five of the six approaches in
particular. That is a statement about where research vessels have run, not
about the ocean, and it means the gap is closeable at specific places rather
than being a property of the sea.

**Two of those places bear on arguments already in this document.** The four
Pamba tracklines sit on the Nelkynda and Bakarē approach. The twelve in the
Pemba and Unguja channels sit on the water the 300-stadia Menuthias notice
measures across, which §23 currently settles on a grid with nothing under it.

### Is the interpolation at least approximately right?

An unmeasured grid is not automatically a wrong one, so the next question is
whether it reproduces the depths a surveyor actually recorded. The twenty
soundings transcribed from the circa-1700 Dutch sheet are the only ground truth
these coasts have. They carry chart-crop pixels rather than coordinates, so they
cannot be compared point to point with anything; they can be compared as a
distribution against the grid over the water the chart covers.

| Group | n | Chart, metres | Grid 5th–95th percentile |
|---|---:|---|---|
| Cranganore entrance | 3 | 5.5–9.1 | 8.4–30.5 |
| Cranganore approach | 8 | 9.1–21.9 | 8.4–30.5 |
| Purakkad approach | 9 | 11.0–21.9 | 4.8–32.8 |

**The grid cannot see the bar.** At Cranganore the chart's three entrance
soundings run 5.5 to 9.1 m, and the grid's fifth percentile over the same water
is 8.4 m: only **2.1 per cent of its cells are as shallow as the chart's
shoalest reading**. The shoal that the Dutch surveyor drew, sounded and labelled
is the one feature a global compilation smooths away, and it is the only feature
that decides whether a laden ship could enter.

That is the sharper form of the finding. The grid is not merely unmeasured in
the shallow approach. It is unmeasured and systematically too deep there, which
is the direction that would make a port look navigable when it was not.

**What follows.** The historic chart soundings were described in §14 as the
earliest bathymetry for Malabar. They are also the only bathymetry: there is
nothing modern to check them against, and the one modern product that covers
them disagrees in the shallows by more than the quantity under discussion. The
twenty transcribed soundings therefore carry the depth evidence by themselves,
and the error budget on reading them, which §20 sets out, matters more than had
been assumed.

**The honest limit on the comparison.** The grid box is larger than the water
the chart's soundings sit on, and the soundings are not georeferenced, so this
is a comparison of ranges rather than of places. Georeferencing the Dutch sheet
would convert it into a point-to-point test, and that is the single piece of
work that would most improve this section.

## 20. The tide, fitted from observation, and what it does to a historic sounding

The tide had been recorded as blocked on an AVISO or TPXO registration. It is
not. The IOC Sea Level Station Monitoring Facility serves observed sea level
from 2,387 stations without an account, and the University of Hawaii archive
holds the long records, so the range can be fitted from observation rather than
taken from a model.

The two sources are complementary rather than redundant. The IOC network is real
time, so several of its stations hold only weeks. Hawaii has forty years at
Zanzibar and ten at Karachi, and nothing at all in India.

| Port | Station | Distance | Spring range | Neap range | Regime |
|---|---|---|---|---|---|
| Muziris | Cochin | 27 km | 0.58 m | 0.26 m | mixed, mainly semidiurnal |
| Nelkynda and Bakarē | Cochin | 63 km | 0.58 m | 0.26 m | mixed, mainly semidiurnal |
| Tyndis | Cochin | 141 km | 0.58 m | 0.26 m | mixed, mainly semidiurnal |
| Barbarikon | Karachi | 43 km | 2.22 m | 1.01 m | mixed, mainly semidiurnal |
| Leukē Kōmē | Aqaba | 146 km | 0.72 m | 0.38 m | semidiurnal |
| Rhapta | Zanzibar | 194 km | 3.72 m | 1.29 m | semidiurnal |

**The spread is the point. Rhapta's spring tide is six times Muziris's.** A
navigability argument that treats the seven ports alike is wrong by metres at
one end of the range and by centimetres at the other. At the Rufiji a bar that
blocks a laden ship at low water is no obstacle six hours later; on the Malabar
coast the tide will not lift a ship over anything.

**Kerala's fit is poor, and the reason is a second finding.** The harmonic fit
explains 99 per cent of the variance at Zanzibar and 54 per cent at Cochin. That
is not a bad record. At Cochin the tidal standard deviation is 0.228 m and the
non-tidal residual is 0.213 m, so the two are the same size, and the monthly
means of the residual run from +0.27 m in March to −0.14 m in July. A seasonal
swing of 0.41 m against a 0.58 m spring range is the monsoon, and it averages
away over a month at Zanzibar but not here.

### What this makes a circa-1700 sounding worth

§19 left the twenty transcribed soundings carrying the depth evidence alone.
The tide fit turns that into an error budget.

| Term | Metres | Source |
|---|---:|---|
| Tide, half the Cochin spring range | ±0.29 | fitted, this project |
| Season, half the non-tidal annual swing | ±0.21 | fitted, this project |
| Reading a half-fathom engraving | ±0.46 | the chart's own precision |
| **Quantifiable, in quadrature** | **±0.58** | |
| Vertical datum of the sheet | unknown | and larger than all of the above |

**The transcription error is larger than the tide.** That is the opposite of
what the project assumed when it recorded the tide as the largest single source
of error in historic soundings. Half a fathom is 0.91 m, so a half-fathom
reading uncertainty is ±0.46 m, against ±0.29 m for the tide. Transcribing the
soundings more carefully, or at higher zoom, would buy more than the whole tide
model did.

**The datum is unknown and dominates, which is why the comparison is internal.**
Nobody knows what a Dutch chart of about 1700 reduced its soundings to. Within
one sheet, surveyed by one hand, that offset is common to every reading and
cancels on a difference. So the usable quantity is not an absolute depth at
either place but the contrast between them:

> **Purakkad approach minus Cranganore entrance: 8.84 m ± 0.59, which is 15
> standard errors.**

**The error propagation here is deliberately conservative**, and the naive
version would have been wrong in the flattering direction. Treating all three
terms as independent per sounding gives ±0.39 and 22.9 sigma. But a surveyor
sounds one approach over a few hours and the other on a different day, so the
tidal and seasonal offsets are common to a visit rather than independent between
readings within it, and only the transcription error averages down. Done that
way the figure is ±0.59, and 15 sigma rather than 23.

**What that contrast settles, and what it does not.** It settles that the
difference Gurukkal and Whittaker propose for Bakarē displacing Muziris, a
silted bar against a deep approach, is real in the earliest measurement anyone
made of this coast, and by a margin fifteen times its own uncertainty. It does
not settle anything about antiquity. The sheet is around 1700, seventeen
centuries late, and §13 applies to it as much as to everything else.

**What this is not.** The fit is the astronomical tide. Surge is not in it, the
gauge datum is not the chart datum, and Aynuna's figure comes from 146 km up the
Gulf of Aqaba, which is the same body of water but not the same coast.

## 21. Wind, the fourth stream, started

Evidence stream four had been declared and never begun, because `DATA.md`
listed ERA5 and ERA5 needs a Copernicus key. The NCEP reanalysis needs nothing,
runs from 1948, and is served as plain text, so the monsoon climatology is a
download. 132 rows in `data/processed/wind_climatology.csv`, eleven sites by
twelve months.

Two quantities per month. Speed is obvious. **Steadiness** is the vector mean
divided by the mean speed, so it runs from 0 when the wind blows every way in
turn to 1 when it never shifts. A square-rigged ship cares about the second at
least as much as the first, because a strong wind that boxes the compass is not
a passage.

### The Arabian Sea crossing, which is the Hippalus run

| | J | F | M | A | M | J | J | A | S | O | N | D |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| m/s | 6.8 | 5.2 | 3.2 | 1.4 | 4.2 | 11.5 | **14.6** | 13.0 | 7.2 | 2.3 | 6.3 | 7.3 |
| from | NE | NE | NE | NNE | SW | SW | **SW** | SW | SW | NNE | NE | NE |
| steadiness | 1.00 | 0.99 | 0.98 | 0.54 | 0.98 | 1.00 | **1.00** | 1.00 | 1.00 | 0.80 | 0.99 | 0.99 |

**Steadiness reaches 1.00 in both directions.** June to September the wind is
southwest at 11 to 15 m/s and never varies; November to February it is northeast
at 5 to 7 m/s and never varies. The two switching months, April and October, are
the only unreliable ones, at 0.54 and 0.80. The Periplus sails out on one and
home on the other, and the reanalysis says those are the only two months a ship
would want to avoid.

### The result that inverts the intuition

**The open-sea leg is the most reliable wind on the whole route, and the Red Sea
is the least.** Mid Red Sea steadiness runs 0.82 to 0.98 and the speed never
exceeds 4.3 m/s, and the direction is northerly in all twelve months. So the
sheltered coastal leg, where Leukē Kōmē sits, is the one with light and
comparatively variable wind and a foul breeze for anything working north, while
the thousand-mile open crossing is a conveyor belt. That is consistent with
Leukē Kōmē existing at all: a port that exists to put cargo onto camels is what
you build when the sea leg north is the hard part.

### The rest

**Malabar landfall** is westerly at 7.7 m/s in July and drops to 1.5 m/s in
November, so the approach is onshore and strong exactly when the crossing
delivers a ship to it. **Rhapta** reverses between NNE in January and SSE from
April to September, at a gentler 4 to 6 m/s, with steadiness above 0.97 in
eleven months of twelve.

### The limitation, which is not small

The grid is 2.5 degrees, about 275 km. **Muziris, Tyndis and Nelkynda fall in
one cell**, so the table cannot distinguish the three Malabar ports and does not
pretend to. This is a monsoon layer, not a local wind at a river mouth. It is
the right resolution for the open-sea legs, which are the legs that depend on
wind, and the wrong one for anything inshore.

## 22. What the second literature sweep closed

The first sweep asked Crossref about ports and excavations and returned
archaeology. The questions blocking the geographic layer went unasked, so
gaps were recorded as unclosable without having been searched for. A second
sweep on OpenAlex, 575 works over seven gap groups, asked them.


**Rhapta now has a dated geographic layer, which it did not have before.**
Punwong's 2013 Leeds thesis holds radiocarbon-dated cores from the northern
Rufiji Delta and from Unguja Ukuu and Makoba Bay on Zanzibar, with altitudes
recorded above and below mean sea level and formal sea-level index points
calculated from mangrove zonation. The Rufiji cores run to 1173 cal BP at
-0.94 m amsl; the Unguja Ukuu core B-UU-1 gives 1359 ± 48 cal BP. Held as
`library/oa-harvest/rhapta-tanzania_Punwong2013_*.pdf`, 295 pages.

This matters beyond the dates. The index points come with indicative ranges,
which is the form the errors-in-variables sea-level method in
§3 expects, and no other port region has supplied them yet.

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

### What it did not close

**Nothing reaches the first century.** The nearest dated material in anything
acquired is Das et al.'s 1.1 cal kyr BP at the Periyar mouth and Punwong's
1359 cal BP at Unguja Ukuu. Both are eight centuries late. The finding in
§13 stands.

**Priju et al. 2018 is still the outstanding item.** The sweep turned up Priju
et al. 2021 instead, 33 vertical electrical soundings from Ernakulam to Chettuva
on the Muziris coast with a modelled subsurface lithology. It is a salinity
study: the words palaeochannel and buried do not occur in it. Useful as
subsurface control on the Periyar coast, not a substitute.

**Alappat et al. 2015 and Shaji et al. 2022 remain paywalled.** Both are
Elsevier, both are on the existing list, and the sweep found no open copy.

---

---

# Part V. Port by port

## 23. Port by port

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
miles is 19.3 km, which would be almost exactly 120 stadia at 155 m. But Casson
derives his coordinate for Niranam *from* that twelve-mile statement, noting
that "the town is not indicated on modern maps, even on that done on the scale
of 1:250,000." Measured to the geocoded modern village at 9.3437 N, 76.5231 E,
Purakkad is **14.7 km** away, not 19.3. The figure that makes the pairing
attractive is overstated in the source by about a third.

**The contradiction, and it has changed sides.** We previously held a Niranam
coordinate 9 km south of the village, taken from an older gazetteer. Corrected
to the geocoded position, which agrees with Casson's own derived figure to
2.8 km, the two constraints swap. Niranam now sits **96.0 km** from Muziris in
a straight line, comfortably inside the 72–102 km band implied by 500 stadia;
and **14.7 km** from Purakkad, below the 17.3–24.5 km band implied by 120
stadia. Before the correction it satisfied the 120 and failed the 500. It now
satisfies the 500 and fails the 120. The pair still cannot satisfy both, but
the reason is the opposite of the one we reported.

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

**Gurukkal and Whittaker (2001) are routinely miscited, ours included.** Their
JRA article is not a sceptical case against the consensus. It confirms
Kodungallur and narrows it to the bays beyond the Periyar-Pullut confluence at
Kottamukku, which they say "is crying out for a serious excavation." They
published six years before the Pattanam dig began, and Pattanam lies 7 to 9 km
south of the spot they identified. The most careful pre-excavation survey of
this coast pointed one way and the evidence surfaced the other. They also read
the Muziris papyrus, with Rathbone, as "referring to Muziris" rather than
recording a contract made there, which removes it as evidence for a Roman agent
resident at the port; and they note that Periplus 54 is damaged at the point
where it gives Muziris's 20 stadia, so the referent is uncertain.

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

#### Datoo read directly, and his weighting tested

The bracket had been carried at second hand through every Rhapta argument in
this project. Read directly, Datoo does not simply give a bracket. He weights
it, and the weighting is the part the literature drops.

His bracket is explicit: "The outside limits of this locality might be said to
be the mouths of the Pangani and the Rufiji rivers, given that the port was
situated on a river (though not necessarily a large one)." So is the weighting:
"in view of the meteorological conditions analysed above, it is arguable that a
higher probability of port location for trade with the Red Sea can be assigned
to the northern rather than the southern section of this locality, that is, to
the stretch between Pangani and Dar es Salaam."

**The weighting rests on one meteorological claim**, taken from Met Office pilot
charts: the north-east monsoon blows with a constancy of 41 to 60 per cent only
as far as about 4°S in February, retreating to the equator in March. A ship out
of the Red Sea arrives in late February or March, so "it would be imprudent to
sail far to the south of these limits if the length of sojourn in East African
waters was intended to be relatively short."

**That claim does not survive the reanalysis.** A latitude transect down the
coast at 40°E, from NCEP monthly means since 1948, gives the steadiness of any
flow carrying a northerly component:

| Latitude | Dec | Jan | Feb | Mar |
|---|---|---|---|---|
| 2.5°S | 0.97 | 0.99 | 0.98 | — |
| 5.0°S | 0.98 | 0.99 | 0.98 | — |
| 7.5°S | 0.98 | 0.99 | 0.98 | 0.85 |
| 10.0°S | 0.98 | 0.96 | 0.95 | — |

A dash is a month when the flow is not out of the north at all. In February a
dependable northerly reaches **at least 10°S**, the southern end of the
transect, not the 4°S Datoo reports, and it does so at a steadiness of 0.95 and
above. His northern weighting therefore loses the support it was resting on.

**Two honest limits on that test.** Steadiness, the vector mean over the scalar
mean, is not the Met Office's constancy, which counts the share of observations
falling in one direction octant; the two are related and not identical. And
Datoo's case is partly about the round trip, not just the outbound wind: he
argues a ship must be back in the Gulf of Aden by the end of April, before the
westerlies and the gales off the Horn. Nothing here tests that, and it is the
part a voyage simulation would address.

**What it changes.** The Rufiji end of the bracket was being discounted on a
basis that does not hold, and every satellite, water and core layer this project
has built for Rhapta sits in the Rufiji box. That work is on the part of the
bracket Datoo argued against, and the argument against it is weaker than it
looked.

#### Menuthias, measured

The Periplus places Menuthias 300 stadia off the mainland. Measured as the
shortest water gap between coastlines on a 61 m grid:

| Island | Narrowest channel | 300 stadia at 155 m | at the conventional 185.2 m |
|---|---|---|---|
| **Pemba** | **49.8 km** (31.0 miles) | 46.5 km, **93%** | 55.6 km, 112% |
| Unguja, that is Zanzibar | 35.5 km (22.1 miles) | 131% | 157% |

**Both stadia favour Pemba, and this project's calibration fits it better.** At
155 m the notice lands within 7 per cent of the Pemba channel, which is well
inside the rounding structure of §4.1, where 300 is a round hundred. Zanzibar is
out by 31 per cent on the most favourable reading available.

The measurement also confirms Datoo, who gives the channels as 30 and 22.5
miles without a source; independently measured they are 31.0 and 22.1. An
earlier figure in this file, 42.8 km for Pemba, was 7 km short and is corrected
here.

The one claim of Periplus-period material is Chami's report of four Roman glass
beads from Mkukutu, 40 km inland of the Rufiji delta, *Current Anthropology* 40
(1999), titled as the first incontrovertible archaeological link with the
Periplus. It is the most cited archaeological claim about Rhapta, and it does not
support the claim its title makes. The objections below are read off Chami's own
published table and text, not taken from a published critique; an earlier version
of this file asserted that the stratigraphy "has been questioned" without a
citation, which it should not have done.

1. **The radiocarbon does not reach the Periplus.** Chami's Table 1 gives three
   dates, and he writes that they "consistently fall between a.d. 200 and 400,"
   concluding the beads arrived "around the 3d century a.d." The Periplus is
   around AD 50.
2. **The dates are not in stratigraphic order.** Ua-11774 at 70-80 cm gives
   1,670 +/- 60 BP; Ua-11775 at 140-150 cm and Ua-11776 at 100-110 cm both give
   1,635 +/- 70. The shallowest sample is the oldest and the deeper two are
   identical, which is not what a sealed, undisturbed deposit produces.
3. **The deepest sample is from inside a cut feature.** Occupation bottoms out at
   130 cm except for a charcoal feature continuing to 150 cm, and Ua-11775 came
   "from the bottom of the blacksmithing feature." That dates the feature, not
   the layer it cuts.
4. **One of the four beads has no context.** The fourth was found near the surface
   where "the top 30 cm had been deposited by bulldozers," and is assigned to the
   sealed horizon because it resembles the others. The site had already been
   partly destroyed by bulldozers extracting gravel.
5. **The bead type cannot carry the date.** Chami acknowledges, citing Boon and
   Spaer, that gold and silver-in-glass beads were produced for about 1,500
   years. The Uppsala specialists dated the segmented bead to 100 BC to AD 400
   and the other three to "an unspecified time period."
6. **The dating is partly circular.** The beads are dated by association with
   Limbo pottery, Limbo is dated 100 BC to AD 300, and the association is then
   offered as evidence of Roman-period contact. The independent radiocarbon
   points to the later end.
7. **The sample is four beads from 8 square metres**, in four 2 by 1 m trenches,
   and Chami notes "the beads were the only foreign objects recovered from the
   four trenches." Small high-value ornaments circulate long after manufacture
   and travel far.

The fair summary is that Mkukutu shows Roman-manufactured glass reaching the
Rufiji hinterland, most plausibly in the third or fourth century AD. It does not
date contact to the Periplus and it does not locate Rhapta.

One lead worth chasing. Juma 2004 (p. 24) writes that Rhapta "may be anywhere
between the Rufiji delta area, where ancient trade goods including Roman beads
have been excavated and further north, where a number of fortuitous discoveries
of **early Roman coins** have been made so far." Early Roman coin finds north of
the Rufiji would be the first Roman numismatic evidence on the Tanzanian coast.
He gives no reference.

---

---

# Part VI. What went wrong, and what is left

## 24. Errors found

### In published sources

1. **CHRE georeferencing error.** Kottayam 1847 (74 aurei) is placed at 9.591 N,
   76.522 E in central Kerala, on top of a Nelkynda candidate. Its own county
   field says **Kannur** and its summary says "on the slope of a hill by the sea."
   Central Kottayam is about 35 km inland behind the backwaters. Wrong by roughly
   260 km. Worth reporting to CHRE. Excluded from our analysis.
2. **Arithmetic error in Cherian 2012 Table 1.** The ring-stones row reads
   0, 0, 0, 15, 9 with a printed total of 15. The seasons sum to 24. The printed
   grand total of 48,862 antiquities uses 15, so the error is in the row.
3. **Irreconcilable Pattanam figures, now four of them.** Torpedo sherds 3,098
   (Cherian, to 2011) against "about 398" (a later summary, to 2014). Glass
   1,338 against "about 906". Both report *fewer* over a *longer* window. The
   mound is 70 hectares in the exhibition catalogue and 45 elsewhere. And most
   seriously, **the import share is unstable by a factor of five**: Cherian's
   season tables give 3,557,118 sherds with 3,537,464 local, leaving about
   19,654 imported at 0.55 per cent, while the catalogue gives 4.5 million local
   body sherds, 516,676 diagnostic sherds and **140,165 non-Indian sherds**, an
   import share near 2.7 per cent. Four further seasons cannot raise imported
   material sevenfold when the first five produced 19,654, so the two are
   counting different things. Since the import fraction is what makes an absence
   at an untested candidate interpretable, **the expected yield at a Malabar
   port is uncertain by a factor of five until this is resolved.**
4. **Nappo's Leukē Kōmē distance measured from the wrong port** (see §7).

### In our own work, corrected

1. Claimed Ponnani fits Tyndis "to within 2.5 km." That compared a straight line
   against a sailed distance. Only the ranking survives.
2. **Stated that the Periplus places Bakarē 120 stadia from Nelkynda. It does
   not.** The text says Nelkynda "is situated on a river, about one hundred and
   twenty stadia from the sea," and that Bakarē is "another place at the mouth
   of this river." The 120 stadia therefore measures Nelkynda to the sea. Casson
   converts it into a Nelkynda-to-Bakarē distance by treating the river mouth
   and the sea as the same point, which is a reasonable reading on an open coast
   and a much stronger assumption on a lagoon coast, where a river debouches
   into the backwater and the backwater reaches the sea through a separate bar.
   Everything we have said about 120 stadia as the tightest constraint on the
   pair rests on Casson's reading, not on the text.
3. Claimed the 300-stadia Menuthias notice favours Zanzibar. Measured island
   shore to mainland shore it favours **Pemba**. The correction then carried a
   wrong number for three months: Pemba was recorded at 42.8 km, and measured
   as the shortest gap between coastlines on a 61 m grid it is 49.8 km. The
   conclusion was right and the figure under it was out by 7 km, which is the
   kind of error that survives because it points the way you already decided.
4. **Measured a strait by walking across raster rows, and got 0.1 km.** The
   first attempt at the Menuthias channels stepped west to east along each row
   looking for the first land, then the next, which in the Pemba and Zanzibar
   channels finds a mangrove islet rather than the far shore. Labelling land as
   connected components and taking the shortest distance between the mainland
   and the island gives the right answer. A result three orders of magnitude
   out is easy to catch; the lesson is that the same bug at ten per cent would
   not have been.
5. **Nearly propagated a correlated error as an independent one.** The
   Purakkad-to-Cranganore depth contrast in §20 came out at 22.9 sigma when all
   three error terms were averaged down across soundings. Two of them, the tide
   and the season, are common to a survey visit rather than independent between
   readings within it, so they do not average. Done correctly the figure is 15
   sigma. The conclusion held either way, which is exactly why it would not
   have been caught by looking at the conclusion.
6. **Nearly reported "no survey at any port" from a four-of-six sample.** The
   NOAA holdings query was first run over four port boxes, returned zero in
   every one, and the pattern was written up. Running the remaining two found
   four bathymetry tracklines across the Nelkynda and Bakarē approach. The
   conclusion barely changed and the actionable item did: there is survey data
   to order at the one port where the depth argument is sharpest.
7. Claimed al-Wajh had a rival coin hoard. It is three nummi of AD 295.
8. Claimed *Pakistan Archaeology* was not online. It is, at doam.gov.pk.
9. Built a Barbarikon distance argument on a mis-extracted endpoint: the text
   says the promontory Papica, not Astakapra.
10. **Archive.org OCR is unusable for IAR.** The Digital Library of India scanned
   the volumes with a Devanagari OCR model, so English came out as mojibake. An
   early search over that derived text falsely showed every Kerala candidate
   absent from 59 years of reporting. Artefact, discarded. The PDFs carry a clean
   English text layer and were re-extracted from directly.
11. **Chapter and title assignment is unreliable in some IAR volumes, and one
   candidate notice was nearly lost to it.** The 2006-07 entry reporting "the
   first time a neolithic axe has been discovered from the higher reaches of the
   Kallada river basin" carries the title "MUGHAL INSCRIPTION, KANNAUJ" in our
   extraction, so a search on titles misses it. Chapter labels are also wrong in
   places: a neolithic site in Bangalore is filed under epigraphy, and an
   exploration in Mahbubnagar under archaeological chemistry. Any count that
   rests on the chapter field, including the 75 Kerala fieldwork entries in §3.2,
   should be treated as approximate until the chapter boundaries are re-derived.
12. **Three IAR extraction bugs**, each of which changed the answer. "MADHYA
   PRADESH" carries three internal spaces, so the boundary regex missed it and
   Madhya Pradesh districts were absorbed into the Kerala block; six of eight
   apparent Kerala Early Historic entries were from Sagar, Vidisha, Chhatarpur,
   Dhar, Gwalior and Sehore. The born-digital volumes use two columns, titles
   broken across lines and a colon rather than an em-dash terminator, which hid
   Pattanam. And the first entry of every block was dropped because the pattern
   required whitespace after the separator, which silently removed the Cranganore
   excavation.
13. **Crossref search is token-based, not phrase-based.** "Mafia Island" returns
   182,000 works, mostly organised crime; "Quseir al-Qadim" 1.5 million. Raw hit
   counts are useless as an attention metric.
---


## 25. Open questions, not yet run

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

## 26. Maps that would serve these

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

---

## 27. What in here is publishable, and what is not

An honest audit of originality. The test applied to each result is whether it is
new, non-obvious, defensible from evidence already held, and of interest to
someone who does not care about these seven ports. Most findings in this
document pass the first three and fail the fourth, which is normal: they are
thesis chapters, not papers. Three clear that bar.

### Paper 1. The stadion is a speed, not a length

**The claim.** The Periplus does not measure distance. It records sailing time,
converted to stadia by a fixed rule, and the conventional 185.2 m conversion
every modern reconstruction depends on is an artefact of that same rule rather
than a measurement of it.

**The evidence, all of it already assembled.**

1. The rounding structure. 33 stadia statements, 27 of them multiples of 100.
   All nine values at or above 2,000 are exact multiples of 1,000, which is 2,
   3, 4, 7 and 12 whole day-and-night runs. The only unround figures anywhere
   are 20, 60 and 120, and every one of them is a short local measure.
2. Casson's own appendix states the rule and does not carry it through: "Their
   rule of thumb was 1000 stades to a day-and-night run, 500 to a day's run."
3. The conventional figure is circular. "Approximately ten stades correspond to
   a nautical mile" gives 1852/10 = 185.2 m exactly. It was never measured from
   the text.
4. Computed leg by leg from Casson's own numbers, over legs whose endpoints are
   all securely located, the implied stadion runs from 96.5 m to 217.6 m, a
   2.3-fold spread that misidentification cannot explain.
5. Read as speed instead, those same figures are daily runs of 26 to 59 nautical
   miles, which is the ordinary range for a square-rigged merchantman between
   beating into a headwind and running with the monsoon.
6. **The wind data closes the loop.** On the Arabian Sea crossing the reanalysis
   gives 14.6 m/s from the south-west in July and 6.8 m/s from the north-east in
   January, both at steadiness 1.00. A ship's day-run differs by season and by
   leg, by about the factor the scatter shows. The scatter is not noise in the
   text. It is the wind.

**The out-of-sample test, which already passes.** The 155 m calibration was
fitted on four legs in the Red Sea and the Gulf of Aden. Applied to an
independent problem it does real work: the 300-stadia Menuthias notice lands
within 7 per cent of the measured Pemba channel at 155 m and misses by 12 per
cent at 185.2 m, and Zanzibar is out by 31 per cent on the best reading
available. A calibration that transfers to a problem it was not fitted on is
the strongest evidence here.

**Why anyone else cares.** Every reconstruction of Indian Ocean and Red Sea
geography from the Periplus inherits the 185.2 m figure. If the unit is a speed,
the error on a stated distance is not a measurement error but a wind
distribution, which changes both the central estimate and the shape of the
uncertainty on every port in the text. The argument is also general: the same
reasoning applies to any periplous.

**What is still needed.** The per-leg implied stadion as a function of season,
bearing and leg type, which is open question 1 in §25 and has not been run.
That is the analysis that would turn a strong argument into a quantitative one.

### Paper 2. Absence of evidence when the searching was not independent of the belief

**The claim.** In site-location problems the standard correction for unequal
survey effort is not enough, because effort is itself a function of the prior.
Excavators dig where they already believe the site was, so detection and
location cannot be estimated separately without the field's existing opinion
entering the likelihood disguised as evidence.

**The evidence.** Kodungallur was dug in 1969–70 *because* it was the
traditional Muziris and produced nothing earlier than the ninth century;
Banbhore was dug as Islamic Daybul and the Barbarikon identification came
afterwards. Those two absences are not the same kind of evidence and no amount
of care about excavated area will distinguish them. The project holds what is
needed to model it: 7,053 parsed fieldwork entries spanning 1953 to 2014, 27
excavation campaigns across 26 candidate sites, survey effort for 65 sites, and
the `targeted_at_port` flag with usable variation, six of the twelve excavated
candidates having been targeted at the port and six not. Thirteen of
twenty-two candidates have never been excavated at all.

**Why anyone else cares.** This is a general defect in archaeological predictive
modelling, and the fix is a joint model rather than a two-stage one. The nearest
existing literature treats sampling bias as a function of accessibility and
modern land use; treating it as a function of the hypothesis under test is the
step that has not been taken.

**What is still needed.** The model itself. Everything above is the data layer.

### Paper 3. A short methods note: global bathymetry grids are interpolation where harbours are

**The claim.** Work on ancient harbour navigability routinely reads depth from
global compilations. Across seven ancient approaches those compilations contain
no measurement at all, and they are biased deep exactly in the shallows, which
is the direction that makes a port look usable when it was not.

**The evidence.** 2.5 million marine cells across six port boxes, 1.2 million of
them shallower than 20 m, and the GMRT data mask is empty at every one.
Independently, NOAA's archive holds no multibeam at all in those boxes and four
bathymetry tracklines across all six, while returning 34 and 21 at Monterey Bay,
so the query and the mask are both sound. Tested against the only ground truth these
coasts have, the circa-1700 Dutch soundings, the grid's fifth percentile at the
Cranganore entrance is 8.4 m against chart readings of 5.5 to 9.1 m: 2.1 per
cent of its cells are as shallow as the chart's shoalest. The grid cannot see
the bar, and the bar is the whole question.

**Why anyone else cares.** It is a one-figure caution with a wide blast radius,
and the remedy is specific: check the data mask, not the grid, and prefer
ICESat-2 ATL24 or an archived trackline where one exists.

**What is still needed.** Nothing. This one is finished and could be written up
as it stands.

### What is not original, and should not be claimed

- **Menuthias is Pemba.** That is Datoo's, from 1970. Our contribution is to
  confirm his channel widths by independent measurement, 31.0 and 22.1 miles
  against his 30 and 22.5, and to note that the 155 m stadion fits him better
  than the conventional one does.
- **The Pangani-to-Rufiji bracket for Rhapta.** Also Datoo's. What is ours is
  that his meteorological weighting toward the northern half does not survive
  the reanalysis, which is a correction to him rather than a new result.
- **The 1341 flood and the reorganisation of the Vembanad.** Standard in the
  Kerala literature.
- **Roman coins in India being an interior phenomenon.** The pattern is known;
  our contribution is the quantity, 73 per cent more than 25 km inland, and the
  inference that coins cannot point at a harbour.
- **The failure of channel detection in Kerala.** The method is Orengo and
  Petrie's. The negative result and its cause, a polder system that mimics
  palaeochannels at exactly the scales the detector keys on, are ours and are
  worth a paragraph in someone else's methods section rather than a paper.
