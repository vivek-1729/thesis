# Coastline

Where the shoreline stood, from historic charts, satellite epochs, beach ridges and dated cores.

## Method

Shared across both sites.

## Malabar

### Sources

- Admiralty sheet 749 (Selby, survey 1851–3, published 1857; the scan is the 1914 edition). Soundings in fathoms. The datum is not stated; low water springs is assumed, with a spring rise of 3 ft.
- 428 soundings transcribed by hand at the Kodungallur (Azhikode) mouth and checked a second time. They are in `data/soundings_1857/` (`soundings_1857.csv`, with the scripts in `scripts/`).
- Eleven c.1700 soundings (`data/raw/soundings_dutch_c1700.csv`), georeferenced from two control points.

### Results

- `bathymetry_1857.ipynb`: a stationary model and a Bakka barrier SPDE model, fitted in R-INLA through rpy2. The notebook runs in about 5 minutes.
- Noise sd is 0.66 m. Depth rises by about 1.7–1.8 m per kilometre offshore. Blocked cross-validation gives an RMSE of about 1.0 m, with 90% intervals covering 92–93%.
- **The data do not favour the barrier model.** No sounding has a spit between it and the open sea, so the barrier has nothing to separate. Where the two models differ, at the mouth, the barrier model is about 0.15 m shallower and more uncertain.
- **Near-shore model F** (section 8b) fixes the observation noise at the error budget (0.4 m) and adds a fine-scale field. The field's sd is about 1.6 m at the mouth, 0.45 m along the shore and 0.15 m offshore, set in `scripts/fine_scale.R`. F is used for the close-up and the mouth navigation figures.
- **Validation** (`validation_bathymetry.ipynb`). Two fully surveyed Texas inlets (NOAA CUDEM) were sounded the way Selby sounded Kodungallur, and the models were scored against the true seabed.
  - Offshore, every model is good to about 0.3–0.4 m.
  - Near the mouth, model D's 90% intervals cover the truth 21–47% of the time. Model F reaches 86–93% at San Luis Pass, where its profile was set, and 84–98% at Pass Cavallo, where it was not. Blocked CV on the soundings does not track the seabed error and should not be used to choose between these models.
- **The bar.** The minimum depth along the bar line comes out at about 1.5–1.9 m at low water springs under models A, B and D, and about 0.3 m under F. On either inlet, a survey with no line of soundings down the channel, which is Selby's situation, reads the controlling depth of the pass 1–2 m too shallow. These are lower bounds, not estimates. Nothing drawing 2.5 m or more crosses at low water on any model. "Small craft only" rests on the 1866 *Pilot*, which the soundings are consistent with.
- **The c.1700 soundings** do not follow the 1857 relation between depth and distance offshore (slope 0.6 against 1.7 m/km). Positional error dominates, so the chart cannot support a spatial model until it is georeferenced properly.

## Ed-Dur

### Sources

### Results

## Open questions
