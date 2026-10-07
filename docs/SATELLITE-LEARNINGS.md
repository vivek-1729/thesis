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

## The gap still open

The riparian control sits beside present water, so it demonstrates detection of
channel-associated ground rather than of a channel that is now dry. Closing it
needs a hand-digitised relict meander in the Indus delta as a second positive.
