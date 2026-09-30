# Statistical methods, with published precedents in reconstructing the past

Statistics papers only. Each is a method the thesis needs, shown somewhere it has
already been applied to a question about the ancient world, so the reference
carries both the technique and the evidence that it transfers. Citations are
Chicago, checked against Crossref.

The geographic, remote sensing and voyage modelling literature is not statistics
and has been moved to `READING-GEOGRAPHIC.md`.

---

## 1. The sampling problem

The central statistical difficulty. Excavation happened where scholars already
believed the port was, so an absence of finds is not independent of the location
being estimated.

Diggle, Peter J., Raquel Menezes, and Ting-li Su. "Geostatistical Inference under Preferential Sampling." *Journal of the Royal Statistical Society: Series C (Applied Statistics)* 59, no. 2 (2010): 191–232. https://doi.org/10.1111/j.1467-9876.2009.00701.x.

Estimating a spatial field using a joint model for the sampling process, taking into account that the sample locations were chosen by what was expected to be found there.

Çadırcı, Mehmet Sıddık, and Golnaz Shahtahmassebi. "Entropy-Based Methods to Address Sampling Bias in Archaeological Predictive Modeling." arXiv, August 4, 2025. https://arxiv.org/abs/2508.02272.

Correcting archaeological predictive models using entropy-weighted measures of survey coverage, taking into account uneven sampling.

---

## 2. Reconstructing a past surface from dated proxies

The machinery behind the coastline layer. The evidence is dated points with error
bars, and the object wanted is a continuous surface with error bars.

Cahill, Niamh, Andrew C. Kemp, Benjamin P. Horton, and Andrew C. Parnell. "Modeling Sea-Level Change Using Errors-in-Variables Integrated Gaussian Processes." *The Annals of Applied Statistics* 9, no. 2 (2015): 547–71. https://doi.org/10.1214/15-AOAS824.

Reconstructing sea level change using Gaussian processes, taking into account age uncertainty.

Haslett, John, and Andrew Parnell. "A Simple Monotone Process with Application to Radiocarbon-Dated Depth Chronologies." *Journal of the Royal Statistical Society: Series C (Applied Statistics)* 57, no. 4 (2008): 399–418. https://doi.org/10.1111/j.1467-9876.2008.00623.x.

Building age-depth chronologies from sediment cores using a monotone stochastic process, taking into account radiocarbon calibration error.

---

## 3. Point processes for the distribution of finds

Crema, Enrico R., Andrew Bevan, and Mark W. Lake. "A Probabilistic Framework for Assessing Spatio-Temporal Point Patterns in the Archaeological Record." *Journal of Archaeological Science* 37, no. 5 (2010): 1118–30. https://doi.org/10.1016/j.jas.2009.12.012.

Analysing site distributions using spatio-temporal point processes, taking into account uncertainty in both the location and the date of each find.

---

## 4. Combining many uncertain dates

Price, Michael Holton, José M. Capriles, Julie A. Hoggarth, R. Kyle Bocinsky, Claire E. Ebert, and James Holland Jones. "End-to-End Bayesian Analysis for Summarizing Sets of Radiocarbon Dates." *Journal of Archaeological Science* 135 (2021): 105473. https://doi.org/10.1016/j.jas.2021.105473.

Summarising many radiocarbon dates using a single end-to-end Bayesian model, taking into account calibration uncertainty at every stage.

---

## 5. Simulation-based inference, only if we commit to it

Relevant only if the voyage simulator is used to *estimate* its own parameters
against the durations the Periplus states. If the simulator is only run forward
to produce a reachability covariate, this section is background rather than
method. That decision is open, and is recorded in `STATISTICAL-PLAN.md`.

DiNapoli, Robert J., Enrico R. Crema, Carl P. Lipo, Timothy M. Rieth, and Terry L. Hunt. "Approximate Bayesian Computation of Radiocarbon and Paleoenvironmental Record Shows Population Resilience on Rapa Nui (Easter Island)." *Nature Communications* 12, no. 1 (2021): 3939. https://doi.org/10.1038/s41467-021-24252-z.

Inferring past population change using approximate Bayesian computation, taking into account a simulation model with no tractable likelihood.

Rubio-Campillo, Xavier. "Model Selection in Historical Research Using Approximate Bayesian Computation." *PLOS ONE* 11, no. 1 (2016): e0146491. https://doi.org/10.1371/journal.pone.0146491.

Comparing competing historical explanations using approximate Bayesian computation, rather than fitting a single model.

Cranmer, Kyle, Johann Brehmer, and Gilles Louppe. "The Frontier of Simulation-Based Inference." *Proceedings of the National Academy of Sciences* 117, no. 48 (2020): 30055–62. https://doi.org/10.1073/pnas.1912789117.

Surveying methods for inference when a model can be simulated but its likelihood cannot be written down.
