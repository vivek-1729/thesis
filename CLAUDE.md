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
| `docs/FINDINGS.md` | Everything the evidence has shown. Read this first |
| `docs/STATISTICAL-PLAN.md` | The method per evidence stream, and the decision layer |
| `docs/TIMELINE.md` | Three phases, current position marked |
| `docs/LIBRARY.md` | What is held, and what to read per port |
|  `docs/cities/*.md` | One file per port holding every mention in the library |
| `data/raw/` | Hand-curated tables. Candidates, ware typology, survey effort, CHRE export |
| `data/processed/` | Derived tables. IAR entries, distances, port passages, hoard distances |
| `src/` | Extraction, mining and mapping scripts |
| `figures/` | Output maps |
| `../library/` | The PDF library, outside the repo. Text layers cached in `text-cache/` |

Large third-party geodata (HydroRIVERS, Natural Earth 10m) is gitignored and
re-downloadable.

Python is at `/Library/Developer/CommandLineTools/usr/bin/python3`. The stack is
pyshp, PyMuPDF, matplotlib and pandas. No GDAL, no geopandas.

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

- Measure the Malabar distances through the backwaters
- Add the five missing candidates: Nakkada, Nirkunnam, Kannetri, Markari, Varakkai
- Build the excavation-coverage map for the whole basin, not just Kerala
- Phase 1 geographic evidence: palaeochannels, coastlines, bathymetry
