# Geographic evidence: what the work established

The Phase 1 geographic step, start to finish. Four satellite methods tried, the
borehole record read, the historic chart archives harvested. Most of the
headline results are negative, and they are more useful than they sound, because
each one closes off a line of enquiry with a number attached.

Detail lives in `SATELLITE-PLAN.md`, `SATELLITE-LEARNINGS.md`,
`SEDIMENT-CORES.md` and `KERALA-RECONSTRUCTION.md`.

---

## 1. The headline

**Imagery finds buried channels in arid terrain and cannot do it in Kerala.**
Multi-season optical PCA scores **AUC 0.814 in the Indus delta** and **0.752 in
Cholistan**, against a threshold of 0.75 fixed before any run. It scores **0.583
at the Periyar** and **0.456 at the Pamba**.

So **Barbarikon can be worked with imagery and the four Malabar ports cannot.**
That is the single most consequential outcome, and it redirects effort from
satellites to archives for most of the thesis.

## 2. Kerala defeats four independent methods

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

## 3. Nothing dates to the Periplus

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

## 4. What the archives gave, which was more than expected

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

## 5. Two claims in the literature that pull against each other

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

## 6. Modern water, measured

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

## 7. Methodological lessons worth keeping

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

## 8. What would change the picture

**Priju et al. 2018** maps buried channels in the Periyar basin by electrical
resistivity, which sees sand bodies through the engineered surface that defeated
everything we tried. The highest-value item outstanding.

**Narayana et al. 2001** on a palaeodelta at the Periyar mouth, about 50 km² and
up to 6 km wide, which is the Muziris landscape.

**Mathai and Nair 1988**, because the 2000 BP claim is load-bearing and unchecked.

**TanDEM-X at 12 m**, which would test whether terrain can contribute anywhere,
since the current failure is resolution rather than method.

**Ibn Battuta**, who was on this coast in 1342, within a year of the flood.

## 9. There is no measured bathymetry at any of the seven approaches

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
recorded in `FINDINGS.md` §8.

**The method is not at fault, which was checked rather than assumed.** The same
two layers over Monterey Bay and the Hudson shelf valley come back 100 per cent
measured. An empty mask on these coasts means an empty mask.

**What follows is the useful part.** The historic chart soundings were described
in §4 as the earliest bathymetry for Malabar. In the shallow approach they are
also the only point-measured bathymetry the project can obtain at all, short of
a national hydrographic office. The twenty soundings transcribed from the
pre-1700 Dutch sheet are not a curiosity to be checked against a modern survey.
There is no modern survey to check them against, so the charts carry the depth
evidence by themselves and the error budget on reading them matters more than
had been assumed.

## 10. The tide, which did not need the registration it was behind

`NEEDS-FROM-YOU.md` put the tide behind an AVISO or TPXO account. It does not
need one. The IOC Sea Level Station Monitoring Facility serves observed sea
level from 2,387 stations without an account, and the University of Hawaii
archive holds the long records, so the range can be fitted from observation
rather than taken from a model.

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

So on the Malabar coast **the season a sounding was taken in matters about as
much as the state of the tide**. That compounds §9: the chart soundings carry
the depth evidence alone, and they now carry two error terms of comparable size
rather than one.

**What this is not.** The fit is the astronomical tide. Surge is not in it, the
gauge datum is not the chart datum, and Aynuna's figure comes from 146 km up the
Gulf of Aqaba, which is the same body of water but not the same coast.

## 11. Wind, the fourth stream, started

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
