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

- `bathymetry_1857.ipynb`: a stationary model and a Bakka barrier SPDE model, fitted in R-INLA through rpy2. The notebook runs in about 2.5 minutes.
- Noise sd is 0.66 m. Depth rises by about 1.7–1.8 m per kilometre offshore. Blocked cross-validation gives an RMSE of about 1.0 m, with 90% intervals covering 92–93%.
- **The data do not favour the barrier model.** No sounding has a spit between it and the open sea, so the barrier has nothing to separate. Where the two models differ, at the mouth, the barrier model is about 0.15 m shallower and more uncertain.
- **The bar.** Its minimum depth at low water springs is about 1.7–1.9 m. The probability that a 1.5 m-draught vessel with 0.5 m clearance gets over is 0.25–0.37, and nothing drawing 2.5 m or more crosses at low water. This agrees with the 1866 *Pilot*: "only available for small coasting craft."
- **The c.1700 soundings** do not follow the 1857 relation between depth and distance offshore (slope 0.6 against 1.7 m/km). Positional error dominates, so the chart cannot support a spatial model until it is georeferenced properly.

## Ed-Dur

### Sources

### Results

## Open questions
