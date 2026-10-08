# What the satellite work established

A record of what we tried, what held up, and what did not, so none of it has to
be rediscovered. Numbers and method are in `SATELLITE-PLAN.md`.

## The result

Multi-season optical PCA detects channel-associated ground at **AUC 0.814 in the
Indus delta** and **0.752 in Cholistan**, against a threshold of 0.75 fixed
before any run. It fails in Kerala: **0.583 at the Periyar, 0.456 at the Pamba**.

The split is by terrain, not by code. Orengo and Petrie's method assumes crop
marks on a relatively unmodified semi-arid surface. Malabar is wet, under thirty
metres of coconut canopy, and laced with paddy bunds and modern canals that
produce the same linear signatures as a buried channel.

**So imagery carries Barbarikon and contributes nothing to the Kerala ports.**
Kerala rests on the historic charts and the Kuttanad cores instead.

## What held up

**Pre-registering the threshold.** Fixing AUC ≥ 0.75 before running anything is
the only reason the Kerala result reads as a finding rather than as a
disappointment to be argued around.

**Two differently motivated scores agreeing.** The summed magnitude of PC2 to
PC4 gives 0.814 in the Indus; choosing instead the component after PC1 with the
most linear structure gives 0.817. Independent rules landing in the same place
is worth more than either number alone.

**Reading windowed COGs over STAC.** No credentials, no whole-scene downloads,
about five seconds for a search plus a band. Earth Engine turned out to be
unnecessary for anything at this scale.

## What did not

**HydroRIVERS as ground truth.** Built from a 500 m DEM, so at 10 m pixels its
lines sat a median of 417 m from any water in the Ghaggar box and traced
irrigation canals rather than channels. It fails even where the detector
demonstrably works. Any control built on it should be discarded.

**Picking the PCA component by linearity over all components.** It picks PC1,
which is overall brightness, because open water is linear too. This made the
detector measurably worse, 0.814 down to 0.719. Excluding PC1 first fixes it.

**L-band radar as the Kerala rescue.** ALOS PALSAR penetrates canopy, which was
the one reason to hope. It moves the Periyar from 0.576 to 0.583 and the Pamba
not at all. The problem is not that we cannot see the ground; it is that the
ground is covered in linear features that look exactly like palaeochannels.

**The Copernicus DEM for channel relief.** At chance everywhere, 0.43 to 0.54,
including at sites where optical works. A channel is one to two metres deep and
detrending a 30 m DEM leaves a standard deviation of 1.2 to 4.7 m, so the signal
is under the noise. This is resolution, not method.

## Site selection matters more than expected

The first test site, the Ghaggar near Anupgarh, was chosen because it is in
Orengo and Petrie's study region. It is wall-to-wall modern irrigated field
grid. Check what a box actually looks like before building a test on it.

## Technical notes worth keeping

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

## The circularity check, and it passes

The water index is one of the 24 features fed to the PCA, and the same index
defines the control labels, so the score and the label were not fully
independent. The detector could in principle have scored well beside water by
rediscovering the index it had been handed.

Re-running with features withheld settles it:

| Region | All 24 features | Water index removed | Index and its two bands removed |
|---|---|---|---|
| Indus delta | 0.814 | **0.816** | **0.820** |
| Periyar | 0.574 | 0.560 | 0.560 |

The Indus result does not depend on it at all, and in fact improves slightly as
the feature is withheld. Removing green and near-infrared as well, so that the
score shares no input with the label, still gives 0.820. The pass is real.

Kerala fails under every variant, so that result is not an artefact either.

## The gap still open

The riparian control sits beside present water, so it demonstrates detection of
channel-associated ground rather than of a channel that is now dry. Closing it
needs a hand-digitised relict meander in the Indus delta as a second positive.


## Water history, a second data layer

The JRC Global Surface Water product is built from every Landsat scene from 1984
to 2021 at 30 m, and is already made, so it needs no processing of ours. With
ESA WorldCover at 10 m it gives a modern water baseline for every port region.

| Region | Ever water km² | Permanent | Seasonal | Lost since 1984 |
|---|---|---|---|---|
| Rhapta, Rufiji delta | 805 | 616 | 189 | 6.0% |
| Nelkynda and Bakarē, Pamba | 780 | 494 | 287 | 1.9% |
| Barbarikon, Indus delta | 565 | 226 | 339 | **9.8%** |
| Tyndis, Kadalundi to Ponnani | 451 | 434 | 17 | 0.6% |
| Muziris, Periyar delta | 295 | 250 | 46 | 2.2% |
| Leukē Kōmē, Aynuna | 210 | 209 | 1 | 0.1% |

**The limitation comes first.** The record starts in 1984, eight years after the
Thanneermukkom barrage and the Idukki dam. It cannot answer the pre-dam
question. It is the modern surface that the historic charts will be differenced
against, which is the Giosan 2006 procedure with its first half still missing.

**What it does show.** The water body the Malabar distances ran through is not a
fixed thing even today: the Pamba box swings from 494 km² permanent to 780 km²
at full seasonal extent, so 37 per cent of its water surface is seasonal. Any
sailed distance through that system has to be quoted with a season attached.

The Indus delta is the most mobile, losing 9.8 per cent of its water surface in
under forty years, which is consistent with the barrage diversions and supports
treating Barbarikon's geography as the least stable of the seven.

Aynuna is the opposite, 209 of 210 km² permanent and 0.1 per cent lost. An arid
coast that has not moved, which is a reason to treat the Leukē Kōmē landscape as
broadly unchanged and to put the reconstruction effort elsewhere.

**One caution on the gained figures.** Kerala shows large gains, 154 km² net in
the Pamba box, which is almost certainly paddy, aquaculture and reservoirs
rather than natural water. "Gained" in this product means a surface that now
holds water, not a channel that has reopened.


## Why Kerala fails, shown rather than argued

Figure 28 puts the Copernicus DEM, its detrended residual and its slope over the
strand plain from Purakkad to Niranam. The terrain is not featureless. It is
full of sharp, high-contrast linear structure. All of it is the Kuttanad polder
system: paddy bunds, canals and field boundaries, in a dense rectilinear mesh
that reaches right across the plain.

That is the confound, and it is worth stating as a finding rather than as an
excuse. The problem on the Malabar coast is not that the ground is invisible
under canopy. It is that the visible ground has been comprehensively re-cut by
twentieth-century engineering into features that look exactly like
palaeochannels to any detector keyed on linearity. An across-shore spectrum of
the detrended surface returns dominant wavelengths of 2.1, 3.5 and 7.9 km, which
are polder and ridge-set scales, not the few hundred metres a single beach ridge
or channel occupies.

**So surface methods are exhausted for Kerala.** Optical failed at 0.58 and
0.46, L-band radar added 0.007, and terrain is dominated by modern
infrastructure. Three independent surface approaches, all negative.

## What is left, and it is not imagery

**Borehole stratigraphy.** A buried channel is a sand body at depth bounded by
finer sediment. This is subsurface, so it is immune to whatever has been done to
the surface since. We hold 17 cores with logged lithology from Maya et al. 2017
and the paper publishes transects between them. This is the method that works
here, and it is reading and tabulation rather than computation.

**The 1857 charts.** They record the surface before the polders, the barrage and
the reclamation. Already acquired.

**Somebody has already done this for Muziris.** Maya et al. cite Narayana,
Priju and Chakrabarti (2001), "Identification of a palaeo-delta near the mouth
of Periyar River in central Kerala." A buried delta at the Periyar mouth is the
Muziris question directly, and we have not read it. It should be added to the
acquisition list.
