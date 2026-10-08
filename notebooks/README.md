# Notebooks

Each reproduces one of the figures used in the presentation, from the raw data
through to the plot, with the reasoning in the markdown cells.

| Notebook | Figure | Question |
|---|---|---|
| `01_channel_detection.ipynb` | 31 | Can satellite imagery find a river that is no longer there? |
| `02_shoreline_change.ipynb` | 33 | Did the Purakkad coast move across the 1976 barrage? |
| `03_water_depth.ipynb` | 30, 32 | How deep was the water, and could a ship get in? |

Run with the project venv:

```
.venv/bin/python -m jupyter lab notebooks/
```

Imagery is read over the network from public catalogues on first run and cached
in `data/processed/sat/`, so the first execution of notebooks 2 and 3 takes
several minutes. Nothing requires an account.

Each notebook ends with a section on what the result does and does not
establish. Those are not decoration: the channel test validates detection of
ground *beside* water, not of a channel that is now dry, and the shoreline work
reaches 1972 rather than antiquity.
