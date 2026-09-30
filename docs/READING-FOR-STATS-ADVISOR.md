# Statistical methods, with published precedents in reconstructing the past

Each paper is a method the thesis needs, shown somewhere it has already been
applied to a question about the ancient world, so the reference carries both the
technique and the evidence that it transfers. Citations are Chicago, and the
metadata was checked against Crossref.

---

## Send these five

**1.** Diggle, Peter J., Raquel Menezes, and Ting-li Su. "Geostatistical Inference under Preferential Sampling." *Journal of the Royal Statistical Society: Series C (Applied Statistics)* 59, no. 2 (2010): 191–232. https://doi.org/10.1111/j.1467-9876.2009.00701.x.

Estimating a spatial field using a joint model for the sampling process, taking into account that the sample locations were chosen by what was expected to be found there.

**2.** Cahill, Niamh, Andrew C. Kemp, Benjamin P. Horton, and Andrew C. Parnell. "Modeling Sea-Level Change Using Errors-in-Variables Integrated Gaussian Processes." *The Annals of Applied Statistics* 9, no. 2 (2015): 547–71. https://doi.org/10.1214/15-AOAS824.

Reconstructing sea level change using Gaussian processes, taking into account age uncertainty.

**3.** DiNapoli, Robert J., Enrico R. Crema, Carl P. Lipo, Timothy M. Rieth, and Terry L. Hunt. "Approximate Bayesian Computation of Radiocarbon and Paleoenvironmental Record Shows Population Resilience on Rapa Nui (Easter Island)." *Nature Communications* 12, no. 1 (2021): 3939. https://doi.org/10.1038/s41467-021-24252-z.

Inferring past population change using approximate Bayesian computation, taking into account a simulation model with no tractable likelihood.

**4.** Haslett, John, and Andrew Parnell. "A Simple Monotone Process with Application to Radiocarbon-Dated Depth Chronologies." *Journal of the Royal Statistical Society: Series C (Applied Statistics)* 57, no. 4 (2008): 399–418. https://doi.org/10.1111/j.1467-9876.2008.00623.x.

Building age-depth chronologies from sediment cores using a monotone stochastic process, taking into account radiocarbon calibration error.

**5.** Crema, Enrico R., Andrew Bevan, and Mark W. Lake. "A Probabilistic Framework for Assessing Spatio-Temporal Point Patterns in the Archaeological Record." *Journal of Archaeological Science* 37, no. 5 (2010): 1118–30. https://doi.org/10.1016/j.jas.2009.12.012.

Analysing site distributions using spatio-temporal point processes, taking into account uncertainty in both the location and the date of each find.

---

## The rest

**6.** Orengo, Hector A., and Cameron A. Petrie. "Large-Scale, Multi-Temporal Remote Sensing of Palaeo-River Networks: A Case Study from Northwest India and Its Implications for the Indus Civilisation." *Remote Sensing* 9, no. 7 (2017): 735. https://doi.org/10.3390/rs9070735.

Mapping vanished river channels using multi-temporal satellite imagery, retaining a classification probability per pixel rather than a fixed map.

**7.** Rubio-Campillo, Xavier. "Model Selection in Historical Research Using Approximate Bayesian Computation." *PLOS ONE* 11, no. 1 (2016): e0146491. https://doi.org/10.1371/journal.pone.0146491.

Comparing competing historical explanations using approximate Bayesian computation, rather than fitting a single model.

**8.** Cranmer, Kyle, Johann Brehmer, and Gilles Louppe. "The Frontier of Simulation-Based Inference." *Proceedings of the National Academy of Sciences* 117, no. 48 (2020): 30055–62. https://doi.org/10.1073/pnas.1912789117.

Surveying methods for inference when a model can be simulated but its likelihood cannot be written down.

**9.** Bilotti, Giacomo, Markus Reindel, Johny Isla, and Christian Mader. "Points, Patterns, and Predictions in Archaeological Settlement Data: Site-Environment Relationships of Paracas and Nasca Communities in the Peruvian Andes." *Journal of Archaeological Science* 183 (2025): 106385. https://doi.org/10.1016/j.jas.2025.106385.

Modelling where settlements are using inhomogeneous point processes with environmental covariates.

**10.** Çadırcı, Mehmet Sıddık, and Golnaz Shahtahmassebi. "Entropy-Based Methods to Address Sampling Bias in Archaeological Predictive Modeling." arXiv, August 4, 2025. https://arxiv.org/abs/2508.02272.

Correcting archaeological predictive models using entropy-weighted measures of survey coverage, taking into account uneven sampling.

**11.** Price, Michael Holton, José M. Capriles, Julie A. Hoggarth, R. Kyle Bocinsky, Claire E. Ebert, and James Holland Jones. "End-to-End Bayesian Analysis for Summarizing Sets of Radiocarbon Dates." *Journal of Archaeological Science* 135 (2021): 105473. https://doi.org/10.1016/j.jas.2021.105473.

Summarising many radiocarbon dates using a single end-to-end Bayesian model, taking into account calibration uncertainty at every stage.

**12.** Herrera Malatesta, Eduardo, Jorge Ulloa Hung, and Corinne L. Hofman. "Looking at the Big Picture: Using Spatial Statistical Analyses to Study Indigenous Settlement Patterns in the North-Western Dominican Republic." *Journal of Computer Applications in Archaeology* 6, no. 1 (2023): 16–28. https://doi.org/10.5334/jcaa.83.

Studying settlement patterns using spatial point statistics against environmental variables, as an open-access worked example.

**13.** Evans, Tim S., and Ray J. Rivers. "Was Thebes Necessary? Contingency in Spatial Modeling." *Frontiers in Digital Humanities* 4 (2017): 8. https://doi.org/10.3389/fdigh.2017.00008.

Modelling ancient settlement networks using a retail gravity model, taking into account how sensitive the outcome is to initial conditions.

---

## If only three

Diggle et al. 2010 for the identification problem, Cahill et al. 2015 for the
reconstruction machinery, and DiNapoli et al. 2021 for simulation-based
inference on archaeological data. Between them they cover the three statistical
problems the thesis actually has.
