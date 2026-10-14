# Periplus port localisation

A Harvard joint Classics and Statistics senior thesis. The question is where
seven ports of the *Periplus Maris Erythraei* (c. AD 50) actually were.

**Leukē Kōmē** (Red Sea coast of Arabia), **Barbarikon** (Indus delta),
**Tyndis**, **Muziris**, **Nelkynda**, **Bakarē** (Malabar coast of Kerala),
**Rhapta** (coast of Tanzania). Six are genuinely disputed. Muziris is treated as
secure and is included because the security is narrower than it looks.

The classical contribution is the assembly and assessment of evidence that has
not previously been brought together. The statistical contribution is a framework
for inferring an unknown location from heterogeneous, noisy sources where the
missingness is itself informative.

## The governing plan

Sequential, and the order matters:

1. Find the proposed locations
2. Find the material evidence and overlay it
3. Find the wind, bathymetric, coastline and satellite evidence
4. Find whatever other evidence bears on it
5. Blend it all

**Currently at step 2, moving into step 3.** We are not making claims about where
the ports were. We are assembling data, asking intermediate questions, and
looking for patterns.

## Where things are

| Path | What |
|---|---|
| `docs/FINDINGS.md` | **The one document.** The problem, the method, everything established, the errors, what is left. Read this first |
| `docs/DATA.md` | Every dataset held, reachable or non-existent, plus the reading list by component |
| `docs/cities/*.md` | Generated. One file per port holding every mention in the library |
| `data/raw/` | Hand-curated tables. Candidates, ware typology, survey effort, CHRE export |
| `data/processed/` | Derived tables. IAR entries, distances, port passages, coins, cores, tides, wind |
| `data/cache/` | Gridded environmental pulls: bathymetry, tide gauges, wind |
| `src/` | Extraction, mining, satellite and mapping scripts |
| `src/env/` | Bathymetry, tides and wind |
| `figures/` | Output maps |
| `notebooks/` | Three notebooks reproducing the presentation figures |
| `../library/` | The PDF library, outside the repo. Text layers cached in `text-cache/` |

Large third-party geodata (HydroRIVERS, Natural Earth 10m) is gitignored and
re-downloadable.

Two Python environments. The existing work runs on
`/Library/Developer/CommandLineTools/usr/bin/python3` with pyshp, PyMuPDF,
matplotlib and pandas, and no GDAL. The geospatial work runs in `.venv`, Python
3.13, with rasterio (GDAL 3.12 bundled in the wheel), pystac-client, pyproj,
shapely and earthengine-api. `.venv` is gitignored.

Satellite imagery is read anonymously over STAC from
`earth-search.aws.element84.com/v1`, which serves `sentinel-2-l2a`,
`landsat-c2-l2` and `cop-dem-glo-30` as cloud-optimised GeoTIFFs. No Earth Engine
account is needed for this.

## Facts established so far

These are load-bearing and should not be re-derived. Full detail in
`docs/FINDINGS.md`.

- **The stadion calibrates to about 155 m**, not the conventional 185 m, from the
  median of four legs with securely identified endpoints.
- **82 per cent of stadia figures are multiples of 100.** Every value at or above
  200 is a round hundred. The only unround values are 20, 60 and 120, all local.
  The short upriver notices are therefore more reliable than the 500-stadia legs.
- **The Malabar distances are given "by river and sea"**, not along the coast.
  They run through the Vembanad backwaters and have never been measured that way
  by anyone, us included. This is the single most consequential unfinished
  measurement.
- **Casson's own table is internally inconsistent**, implying 144 m and 204 m on
  two legs the text gives as equal.
- **Thirteen of twenty-two disputed candidates have never been excavated.** In
  Kerala, only four fieldwork entries in sixty-one years of *Indian Archaeology:
  A Review* mention material of Periplus date. Absence is mostly absence of
  excavation.
- **Roman coins in India are an interior phenomenon.** 73 per cent of recorded
  coins lie more than 25 km inland, concentrated on the Palghat corridor. Coins
  cannot point at a harbour.
- **Every Kerala candidate is a documented later port** with no first-century
  evidence. That is a fact about how the candidate lists were assembled.

## How to work on this

- **Do not jump ahead to conclusions about where the ports were.** That is step 5
  and we are at step 2. Report what the data shows and stop there.
- **Report counts, not ordinals.**
- **Verify before reporting.** Several apparent findings have turned out to be
  extraction artefacts. The Devanagari-OCR incident and the three IAR extraction
  bugs are recorded in `docs/FINDINGS.md` §8 as a standing warning.
- **Distances should be stated as rankings, not fits**, until the sailed-versus-
  straight-line problem is resolved.
- **Write in full sentences. Sparing use of em dashes. Do not start in media
  res.**
- Bibliographic metrics and aggregate numismatic patterns have been judged not
  useful. Do not build more of them.

## Immediate work

- Measure the Malabar distances through the backwaters. Still the single most
  consequential unfinished measurement
- Build the excavation-coverage map for the whole basin, not just Kerala
- Read the four held excavation reports: Qana, Sumhuram, Ras Hafun, Myos Hormos
- Fix the city-record builder, which reports zero candidates for Leukē Kōmē
  while the candidate table holds four
- The nine open-access PDFs that need a browser, listed in `docs/DATA.md` §7
