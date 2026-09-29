# Statistical methods, with published precedents in reconstructing the past

Organised by method. For each, one or two papers where that method has been
applied to a question about the ancient world, so the reference shows both the
technique and that it transfers. Statistics journals where they exist, and
quantitative archaeology journals otherwise.

---

## 1. Errors-in-variables with Gaussian processes, for sea level and coastline

**Cahill, Kemp, Horton and Parnell, "Modeling sea-level change using
errors-in-variables integrated Gaussian processes", *Annals of Applied
Statistics* 9 (2015), 547-571.** doi:10.1214/15-AOAS824

The closest single precedent for what I am doing. A Gaussian process prior on
the rate of sea-level change, integrated and set in an errors-in-variables
frame so that age uncertainty in the proxies is carried through rather than
ignored. Inputs are tide gauges and sediment cores. I need the same structure
to put an uncertainty band on the first-century coastline, and the
errors-in-variables treatment is also what the textual distances need.

Preprint: https://arxiv.org/pdf/1312.6761

## 2. Stochastic process models for depth and age, for the cores

**Haslett and Parnell, "A simple monotone process with application to
radiocarbon-dated depth chronologies", *JRSS Series C* 57 (2008), 399-418.**
doi:10.1111/j.1467-9876.2008.00623.x

Age-depth reconstruction posed as inference on a partially observed monotone
stochastic process, built from gamma increments arriving in a Poisson fashion.
The template for turning sediment cores into dated surfaces with honest
uncertainty, which is what the palaeo-coastline layer rests on.

## 3. Simulation-based inference, for the voyage model

**DiNapoli et al., "Approximate Bayesian Computation of radiocarbon and
paleoenvironmental record shows population resilience on Rapa Nui", *Nature
Communications* 12 (2021).** https://www.nature.com/articles/s41467-021-24252-z

ABC used to fit a simulation model of the past to archaeological and
palaeoenvironmental data, with multi-model comparison. My wind and voyage model
is a simulator with no tractable likelihood, so this is the inferential route,
and this paper shows it working on archaeological data rather than in principle.

**Rubio-Campillo, "Model selection in historical research using approximate
Bayesian computation", *PLoS ONE* 11 (2016).**
https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0146491

The same idea applied to choosing between competing historical explanations,
which is structurally what choosing between candidate port locations is.

Background, if the method needs a canonical citation: **Cranmer, Brehmer and
Louppe, "The frontier of simulation-based inference", *PNAS* 117 (2020)**,
doi:10.1073/pnas.1912789117.

## 4. Preferential sampling, which is the core identification problem

**Diggle, Menezes and Su, "Geostatistical inference under preferential
sampling", *JRSS Series C* 59 (2010), 191-232.**
doi:10.1111/j.1467-9876.2009.00701.x

Sampling locations that depend stochastically on the quantity being sampled,
handled by modelling the sampling process as a log-Gaussian Cox process jointly
with the field of interest. This is exactly my problem: archaeologists
excavated where they already believed the port was, so an absence of finds is
not independent of the location being estimated.

**"Entropy-based methods to address sampling bias in archaeological predictive
modeling", arXiv:2508.02272.** https://arxiv.org/pdf/2508.02272

The archaeological statement of the same problem, and the current state of that
literature.

## 5. Spatial point processes for site distributions

**Crema, Bevan and Lake, "A probabilistic framework for assessing
spatio-temporal point patterns in the archaeological record", *Journal of
Archaeological Science* 37 (2010).**
https://www.sciencedirect.com/science/article/abs/pii/S0305440309004622

Point pattern analysis where both the location and the date of each find carry
uncertainty, which is the situation for the coin hoards.

**"Points, patterns, and predictions in archaeological settlement data",
*Journal of Archaeological Science* (2025).**
https://www.sciencedirect.com/science/article/pii/S0305440325002341

Inhomogeneous point process models with environmental covariates, used to
estimate site-environment relationships. This is the structure of my geographic
prior.

**"Looking at the big picture: using spatial statistical analyses to study
indigenous settlement patterns", *Journal of Computer Applications in
Archaeology* (2023).** https://journal.caa-international.org/articles/10.5334/jcaa.83

Open access, and a clean worked example of fitting point process models to
settlement data.

## 6. Spatial interaction models for trade networks

**Davies, Fry, Wilson et al., "Was Thebes necessary? Contingency in spatial
modelling", arXiv:1611.07839.** https://arxiv.org/pdf/1611.07839

Spatial interaction modelling applied to ancient settlement, with attention to
how sensitive the outcome is to initial conditions. The precedent for treating
the trade pattern as a gravity-type model, and a caution about how much weight
that layer can bear.

## 7. Bayesian summarisation of dated evidence

**"End-to-end Bayesian analysis for summarizing sets of radiocarbon dates",
*Journal of Archaeological Science* (2021).**
https://www.sciencedirect.com/science/article/pii/S0305440321001436

How to aggregate many individually uncertain dates without the artefacts that
naive summation produces. Relevant to combining the excavation record, where
each site's chronology is separately uncertain.

## 8. Remote sensing as a measurement problem

**Orengo and Petrie, "Large-scale, multi-temporal remote sensing of palaeo-river
networks", *Remote Sensing* 9 (2017).** https://www.mdpi.com/2072-4292/9/7/735

Recovering more than 8,000 km of relict channels in northwest India from
seasonal vegetation dynamics and spectral decomposition. Open access, and the
method I would use to reconstruct the Indus and Periyar channels. The output is
a classification probability per pixel, which is how it enters the model rather
than as an asserted map.

---

## If only three

Cahill et al. 2015 for the reconstruction machinery, Diggle et al. 2010 for the
identification problem, and DiNapoli et al. 2021 for simulation-based inference
on archaeological data. Between them they cover the three statistical problems
the thesis actually has.
