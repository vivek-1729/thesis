# Coastline

Where the shoreline stood, from historic charts, satellite epochs, beach ridges and dated cores.

## Method

Shared across both sites.

## Files

| What | Where |
|---|---|
| Kodungallur seabed: transcription, models A, B, D and F, navigability, c.1700 | `bathymetry_1857.ipynb` (`scripts/make_notebook.py`) |
| Validation against two surveyed Texas inlets | `validation_bathymetry.ipynb` (`scripts/make_validation_notebook.py`, `scripts/inlet_truth.py`) |
| Model F at seven candidate mouths, compared | `seabed_mouths.ipynb` (`scripts/make_mouths_notebook.py`) |
| Sounding windows, traced coasts, mouths | `scripts/sounding_sites.py` |
| Detection, build and contact sheets for a window | `scripts/soundings.py` (Kodungallur: `detect_soundings.py`, `build_soundings_1857.py`) |
| Hand readings | `scripts/transcriptions/<site>.py` (Kodungallur: `transcription_1857.py`) |
| Model inputs per site | `scripts/seabed_inputs.py` -> `data/soundings/<site>/model/` |
| Model F, shared | `scripts/seabed_model.R`; fine-scale profile `scripts/fine_scale.R` |
| Chart georeferences | `../src/charts/sheets.py` (749, 750), `../src/charts/sheet64.py` (64) -> `data/processed/charts/admiralty_georef.json` |

Tiles, contact sheets and posterior draws (`samples.bin`) are gitignored and regenerate from the scripts.

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
- **Soundings at six more candidate mouths** (November 2026), read by eye from the tiles of `scripts/soundings.py` and checked a second time against contact sheets. Readings are in `scripts/transcriptions/<site>.py`, tables in `data/soundings/<site>/`. Usable soundings (ok + unsure):

  | Site | Port | Chart, survey | Usable | Depths (fathoms) |
  |---|---|---|---|---|
  | Ponnani | Tyndis | 749, 1851–3 | 390 | 0.5–15 |
  | Tanur | Tyndis | 749, 1851–3 | 386 | 0.5–15 |
  | Beypore, Chaliyam | Tyndis | 64, 1887 | 328 | 0.25–8 |
  | Koyilandy ("Kollam", Quilandi) | Tyndis | 64, 1887 | 279 | 0.25–7 |
  | Kollam, Neendakara, Thangassery | Nelkynda, Bakarē | 750, 1850–2 | 493 | 0.75–23 |
  | Purakkad, Nirkunnam | Nelkynda, Bakarē | 750, 1850–2 | 452 (plus 5 of 1901, kept apart) | 0.25–15 |

  Chart 64 states its datum (lowest low water springs, spring rise 5 ft); Selby's sheets do not. On chart 64 clearly printed lone fractions were marked ok; on the Selby sheets they were marked unsure. The "(soundings in 1901)" label on sheet 750 refers to one line of five soundings in a different typeface, all 4¾ fathoms. Sheet 750 marks the Porakad mud-bank anchorage and notes "good and safe Anchorage during the S.W. Monsoon after 1st burst in June". Kadalundi lies off the eastern edge of chart 64 and is not covered. Chart 64 is georeferenced from its title position and scale bar (`quantitative/src/charts/sheet64.py`) and has not yet been checked against an independent control point.
- **Model F at seven mouths** (`seabed_mouths.ipynb`; numbers in `data/soundings/mouths_comparison.csv`). These are the seabeds as surveyed in 1850–2, 1851–3 and 1887, not in the first century, and the comparison ranks the mouths without locating a port.
  - **Anchorage distance.** This is the distance seaward from the mouth, or from the shore off the town, at which water deep enough for a 3 m draught (3.5 m) becomes 90 per cent likely. Tanur 0.3 km; Kollam and Purakkad 0.8; Ponnani 1.0; Beypore 1.2; Kodungallur 1.3; Koyilandy 1.6. For a 4 m draught the distances are 0.5 to 2.2 km in the same order. Koyilandy's broad inshore mud shoal puts deep water furthest out; Tanur's steep beach puts it closest.
  - **Bar depth.** It can be estimated only where the entrance was sounded. Beypore (1887, 8 soundings within 500 m) is at least 2.0 m, and Kodungallur (2 soundings) at least 1.3 m. Both are lower bounds, for the reason the validation gives. **The Ponnani and Neendakara (Kollam) entrances were effectively not sounded**: 1 and 0 soundings within 500 m. No bar depth is given for them.
  - **Shelf depth at 2 km** is 4.6 m at Koyilandy and 6.1–8.6 m elsewhere.
  - Two methods were tried and rejected, and the notebook records why. The nearest deep cell in each draw gave spuriously short anchorage distances. A start point 500 m from the mouth bypassed the bar.
- **The c.1700 soundings** do not follow the 1857 relation between depth and distance offshore (slope 0.6 against 1.7 m/km). Positional error dominates, so the chart cannot support a spatial model until it is georeferenced properly.

## Ed-Dur

### Sources

### Results

## Open questions
