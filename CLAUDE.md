# Periplus port localisation

A Harvard joint Classics and Statistics senior thesis. The question is where
seven ports of the *Periplus Maris Erythraei* (c. AD 50) actually were.

**Leukē Kōmē** (Red Sea coast of Arabia), **Barbarikon** (Indus delta),
**Tyndis**, **Muziris**, **Nelkynda**, **Bakarē** (Malabar coast of Kerala),
**Rhapta** (coast of Tanzania). Six are genuinely disputed. Muziris is treated as
secure and is included because the security is narrower than it looks.

The classical contribution is the assembly and assessment of evidence that has
not previously been brought together. The statistical contribution is a Bayesian
framework for inferring an unknown location from heterogeneous, noisy sources
where the missingness is itself informative.

## The governing plan

Sequential, and the order matters:

1. Find the proposed locations
2. Find the material evidence and overlay it
3. Find the wind, bathymetric, coastline and satellite evidence
4. Find whatever other evidence bears on it
5. Blend it all

**Steps 1 and 2 are done. We are well into step 3.** We are not making claims
about where the ports were. We are assembling data, asking intermediate
questions, and looking for patterns.

## The four questions

The geographic evidence, and the thesis itself, is organised around four
questions. The textual distances and the archaeological record feed into them.

1. **Where was the coastline?** Historic charts, satellite epochs, dated
   shorelines.
2. **How deep was the water, and could a ship get in?** Chart soundings, tides,
   cores, a sea-level curve.
3. **Where did the rivers run?** Channel detection from imagery and terrain, and
   the waterways drawn on the historic charts.
4. **How fast did ships actually sail?** Wind reanalysis and measured
   square-rig performance, run as a voyage simulation.

`writing/outline.txt` holds the thesis outline: introduction, a statistical
framework chapter, two port case studies (each with a quantitative and a
qualitative section), and a conclusion. The two case studies are the Malabar
coast and Ed-Dur.

## Where things are

| Path | What |
|---|---|
| `archive/docs/FINDINGS.md` | **The main document.** The problem, the method, everything established, the errors, what is left. Read this first |
| `archive/docs/new_findings_v2.md` | The latest results, October 2026: the routed distances, the short notices, the ancient shoreline, the voyage model, and how each of the four questions stands. Not yet folded into `FINDINGS.md` |
| `archive/docs/new_findings.md` | The earlier October processing notes that `new_findings_v2.md` builds on |
| `archive/docs/DATA.md` | Every dataset held, reachable or non-existent, plus the reading list by component |
| `archive/docs/data_new.md` | Short list of data sources by question, with what is still to do |
| `archive/docs/things-for-you.md` | Everything that needs a person: logins, emails, proxy downloads, decisions |
| `archive/docs/TODO.md` | The processing queue. Partly done; check against `new_findings_v2.md` |
| `writing/` | Thesis outline and chapter drafts |
| `archive/docs/cities/*.md` | Generated. One file per port holding every mention in the library |
| `data/raw/` | Hand-curated tables. Candidates, distances, Ptolemy, cores, soundings |
| `sites/malabar/material/data/` | The archaeological tables: pottery, excavations, IAR entries, coins. See its README |
| `data/processed/` | Derived tables. Distances, port passages, cores, tides, wind, routing, JGSI catalogue |
| `data/processed/sat/` | Satellite arrays. Gitignored, about 2 GB, slow to regenerate |
| `data/cache/` | Gridded environmental pulls and the XRONOS export. Gitignored, about 1.4 GB |
| `sites/malabar/`, `sites/ed-dur/` | **Current work, per site.** `readings/` (gitignored) and `material/`, the qualitative analysis |
| `quantitative/` | **Current work, shared.** `coastline/`, `rivers/`, `voyage/`, each with `notes.md`, `data/` and `figures/`, plus the code in `src/` |
| `archive/src/` | The earlier extraction, mining and mapping scripts. Frozen; not expected to run |
| `quantitative/src/env/` | Bathymetry, tides, wind and the voyage simulator |
| `quantitative/src/sat/` | Channel detection, terrain, shoreline and water-network routing |
| `quantitative/src/charts/` | Georeferencing the historic charts and the Narayana 2001 figure |
| `archive/figures/` | Earlier output maps. The live `quantitative/src/sat` and `charts` scripts still read and write here |
| `archive/notebooks/` | Three notebooks reproducing the presentation figures: channel detection, shoreline change, water depth |
| `../library/` | The PDF library, outside the repo. Text layers cached in `text-cache/` |

Large third-party geodata (HydroRIVERS, Natural Earth 10m) is gitignored and
re-downloadable.

Two Python environments. The older scripts run on
`/Library/Developer/CommandLineTools/usr/bin/python3` with pyshp, PyMuPDF,
matplotlib and pandas, and no GDAL. The geospatial work runs in `.venv`, Python
3.13, with rasterio (GDAL 3.12 bundled in the wheel), pystac-client, pyproj,
shapely, scikit-image, scipy, torch and earthengine-api. `.venv` is gitignored.
Install packages sequentially; concurrent pip corrupted the previous environment.

Satellite imagery is read anonymously over STAC from
`earth-search.aws.element84.com/v1`, which serves `sentinel-2-l2a`,
`landsat-c2-l2` and `cop-dem-glo-30` as cloud-optimised GeoTIFFs. No Earth Engine
account is needed for this.

The repository moved out of iCloud on 30 October 2026 after iCloud corrupted
`.git` twice. Never commit `.npz` arrays or anything over 50 MB; large files
already had to be stripped from history once to get under GitHub's limit.

## Facts established so far

These are load-bearing and should not be re-derived. Full detail in
`archive/docs/FINDINGS.md` and `archive/docs/new_findings_v2.md`.

**The text**

- **The stadion calibrates to about 155 m**, not the conventional 185 m, from the
  median of four legs with securely identified endpoints.
- **82 per cent of stadia figures are multiples of 100.** Every value at or above
  200 is a round hundred. The only unround values are 20, 60 and 120, all local.
  The short upriver notices are therefore more reliable than the 500-stadia legs.
- **The stadion is a speed, not a length.** Figures are sailing time converted by
  a rule of thumb, and the conventional 185.2 m is itself an artefact of that rule.
- **Casson's own table is internally inconsistent**, implying 144 m and 204 m on
  two legs the text gives as equal.

**The material record**

- **Thirteen of twenty-two disputed candidates have never been excavated.** In
  Kerala, only four fieldwork entries in sixty-one years of *Indian Archaeology:
  A Review* mention material of Periplus date. Absence is mostly absence of
  excavation.
- **Roman coins in India are an interior phenomenon.** 73 per cent of recorded
  coins lie more than 25 km inland, concentrated on the Palghat corridor. Coins
  cannot point at a harbour.
- **Every Kerala candidate is a documented later port** with no first-century
  evidence. That is a fact about how the candidate lists were assembled.

**The landscape**

- **Imagery finds buried channels in arid terrain and cannot do it in Kerala.**
  Four methods failed there because the Kuttanad polders mimic palaeochannels.
  Terrain beats optical, and the riparian control flatters any detector.
- **There is no measured bathymetry at any of the port approaches** in any modern
  source. The 1857 Admiralty sheets are the only measured depth, georeferenced to
  about 20 m from their own graticule. About twenty soundings are transcribed out
  of several thousand.
- **Spring tides run 3.72 m at Rhapta against 0.58 m at Muziris.**

**October 2026, from routing the Malabar legs through water**

- **The "by river and sea" distances are now measured through the backwaters.**
  Routed distance exceeds the straight line by a median of 1.13 and up to 1.69,
  not by a constant.
- **The implied stadion separates candidates by a factor of two.** Ponnani
  (about 167 m) and Nirkunnam (about 180 m) sit near the calibrated 155 m;
  Koyilandy and Kollam need more than 320 m. This is a ranking, not a fit, and
  rests on the modern water network.
- **No candidate satisfies the two short notices on the modern coast.** Muziris
  "20 stadia up the river" and Nelkynda "120 stadia from the sea" fit nothing.
  Pattanam sits 220 m from the undated ancient shoreline in Narayana, Priju and
  Chakrabarti 2001, which would make the 20 stadia satisfiable. Undated, so a
  bracket and not a position.
- **The voyage model corroborates the text without locating a port.** The July
  season is forced by the wind, and chapter 57's difference between the Malabar
  and Barygaza courses is real in the wind field.
- **The satellite shoreline comparison failed its own check** (every transect
  moved landward) and its numbers must not be used.

## How to work on this

- **Do not jump ahead to conclusions about where the ports were.** That is step 5.
  Report what the data shows and stop there.
- **Report counts, not ordinals.**
- **Verify before reporting.** Several apparent findings have turned out to be
  artefacts. The Devanagari-OCR incident, the IAR extraction bugs and the later
  pipeline errors are recorded in `archive/docs/FINDINGS.md` §24 as a standing warning.
- **Distances should be stated as rankings, not fits**, until the routes are
  measured through a network older than the modern one.
- **Write in full sentences. Sparing use of em dashes. Do not start in media
  res.** Keep chat answers short, and when asked to "just talk", do not build
  anything.
- Bibliographic metrics and aggregate numismatic patterns have been judged not
  useful. Do not build more of them.

## Immediate work

- Transcribe the 1857 Admiralty soundings. This alone unblocks the water-depth
  question
- Trace the 1857 backwater network and re-route the Malabar legs through it
- Date the Narayana ancient shoreline, or find something that does; extend the
  trace north to Krishnan Kotta so Kodungallur can be measured against it
- Fix the shoreline comparison: one water definition across epochs, and a
  Sentinel-2 epoch that builds
- Fold `archive/docs/new_findings_v2.md` into `archive/docs/FINDINGS.md`
- Fix the city-record builder, which reports zero candidates for Leukē Kōmē
  while the candidate table holds four
- Build the excavation-coverage map for the whole basin, not just Kerala
- Waiting on the user (`archive/docs/things-for-you.md`): the 69 JGSI papers through the
  Harvard proxy, the email to Priju for the Periyar resistivity reports, the
  Earthdata and EarthExplorer logins, and the open decisions in §7
