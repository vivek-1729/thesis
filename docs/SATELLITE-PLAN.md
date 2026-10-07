# Satellite channel detection: plan and results

Can we recover buried river channels from satellite imagery, and does the method
transfer from the semi-arid northwest, where it was developed, to the wet and
heavily modified Malabar coast, where we need it?

This is set up as a replication with a pre-registered success criterion, not as a
survey. The outcome that matters most is an honest answer about Kerala, and a
failure there in week one is worth as much as a success.

---

## Phase 0. Environment — done

Python 3.13 in `.venv` with rasterio (GDAL 3.12 bundled), pystac-client, pyproj
and shapely. Imagery is read anonymously over STAC from AWS Earth Search, which
serves `sentinel-2-l2a`, `landsat-c2-l2` and `cop-dem-glo-30` as cloud-optimised
GeoTIFFs. Windowed reads confirmed working: a search plus one band over a 20 km
box takes about five seconds. No Earth Engine account required.

## Phase 1. Data layer

`src/sat/stack.py`. Given a bounding box and a date range: search the catalogue,
read only the needed window and bands from each scene, mask cloud and shadow
using the scene classification band, and reduce to a median composite per band
per season. Cache composites to `data/processed/sat/` so later phases do not
re-download.

Seasons matter because the signal is a soil-moisture and vegetation effect that
appears most strongly in the dry season. Composites are built separately for the
dry and wet halves of the year.

## Phase 2. Detection

`src/sat/detect.py`, two independent arms.

**Spectral.** Stack the seasonal band composites into a pixels-by-features
matrix and run principal components. A buried channel holds more moisture, so it
recurs across dates as a coherent linear anomaly while noise does not, which is
what the decomposition separates out.

**Topographic.** Pull the Copernicus 30 m DEM for the same window, detrend by
subtracting a smoothed surface so the regional slope does not swamp a channel's
one or two metres of relief, and compute curvature. A channel reads as a linear
negative anomaly.

Neither arm is thresholded. Both produce a continuous score per pixel.

## Phase 3. Validation

`src/sat/control.py`. The test is whether the pipeline separates
channel-associated ground from ordinary ground.

**Positive control.** A modern river course from HydroRIVERS, with the open-water
pixels masked out. Masking the water is the point: we want to know whether the
method detects the moisture and vegetation signature around a channel, which is
what a dry palaeochannel would leave, rather than detecting water.

**Negative control.** Lines of the same length and sinuosity placed at random in
the same box, away from any mapped river.

**Criterion, fixed before running.** The score distribution along the positive
control must separate from the negatives with AUC ≥ 0.75. Below that the method
has not transferred and we say so.

## Phase 4. Known palaeochannel landscape

Run the validated pipeline over the Ghaggar-Hakra near Anupgarh in Rajasthan,
which is Orengo and Petrie's kind of terrain and holds a well-documented dry bed.
A strong coherent lineament where HydroRIVERS maps nothing is the result we are
looking for. Their own channel vectors are not published, so this is a visual and
spatial comparison against the published literature rather than a vector overlay.

## Phase 5. Indus delta

Barbarikon. The same run around Banbhore, where the river has avulsed repeatedly
and the shelf record carries a hiatus across the Periplus period, so imagery is
carrying more of the weight than elsewhere.

## Phase 6. Kerala

The Periyar and the Pamba. The same pipeline, the same criterion. My expectation
is that it fails: the coast is wet, under dense canopy, and cut through with
paddy bunds and modern canals that will produce the same linear signatures. If it
fails, the Kerala channel reconstruction falls back on the historic charts and
the Kuttanad cores, which is a defensible outcome and worth establishing early.

---

## Results

Riparian control, which is the sound one. Threshold 0.75, fixed before any run.

| Site | Terrain | Optical | Optical+SAR | SAR only | DEM |
|---|---|---|---|---|---|
| Indus delta, Banbhore | arid delta | **0.814** | 0.798 | 0.525 | 0.491 |
| Cholistan, Hakra bed | desert | **0.752** | n/a | n/a | 0.503 |
| Periyar, Pattanam | wet, canopied | 0.576 | 0.583 | 0.555 | 0.537 |
| Pamba, Vembanad | wet, canopied | 0.456 | 0.455 | 0.500 | 0.430 |

**The method works in arid terrain and does not work in Kerala.** Both arid
sites pass. Neither Kerala site comes close, and the Pamba box is below chance
on most arms. Adding L-band radar, which was the one reason to hope, moves
Periyar from 0.576 to 0.583 and Pamba not at all.

**This was predicted in advance and is a usable result.** Orengo and Petrie's
method assumes crop marks on a relatively unmodified semi-arid surface. The
Malabar coast is wet, under thirty metres of coconut canopy, and cut through
with paddy bunds and modern canals that produce the same linear signatures as a
buried channel. Imagery cannot separate them. The Kerala channel reconstruction
therefore rests on the historic charts and the Kuttanad cores, and the Harvard
Map Collection appointment matters more to this thesis than any satellite work.

**The terrain arm fails everywhere, including where the optical arm works.** A
channel is one to two metres deep and the Copernicus DEM is 30 m horizontally
with metre-scale vertical noise, so the signal sits under the noise floor.
Detrending leaves a standard deviation of 1.2 to 4.7 m across these sites, the
same order as the feature. This is resolution, not method: TanDEM-X at 12 m
would be the test of whether terrain can contribute at all.

**HydroRIVERS is not a usable control and all those numbers should be ignored.**
It fails even at sites where the optical detector demonstrably works, because it
is built from a 500 m DEM: in the Ghaggar box its lines sat a median of 417 m
from any water and traced irrigation canals rather than channels. The riparian
control, the ring of dry ground just outside visible water, is derived from the
imagery and correctly located by construction.

**One validation gap remains.** The riparian control sits beside present water,
so it demonstrates detection of channel-associated ground, not of a channel that
is now dry. Closing it needs a hand-digitised relict meander in the Indus delta.

