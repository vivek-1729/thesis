# Quantitative

The geographic work, shared across both case studies. The method is the same at
each site, so the code lives here once and each site gets its own section in
the notes.

| Folder | What |
|---|---|
| `src/env/` | Bathymetry, tides, wind and the voyage simulator |
| `src/sat/` | Channel detection, terrain, shoreline and water-network routing |
| `src/charts/` | Georeferencing the historic charts and the Narayana 2001 figure |
| `coastline/` | Where the shoreline stood |
| `rivers/` | Where the water ran |
| `voyage/` | Wind and sailing time |

Each of the last three has a `notes.md`, a `data/` and a `figures/`. Put the
site in the file name (`malabar_...`, `ed-dur_...`).

Scripts are run from the repository root, for example
`.venv/bin/python quantitative/src/sat/run_route.py`. They read and write the
shared `data/` at the root.
