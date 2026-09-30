# Statistical methods, with published precedents in reconstructing the past

Organised by the problem the thesis has, not by topic. Each entry is a method
the work needs, shown somewhere it has already been applied to a question about
the ancient world, so the reference carries both the technique and the evidence
that it transfers. Citations are Chicago, checked against Crossref.

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

## 2. Reconstructing the coastline and the river channels

The geographic layer. The Periplus gives the Malabar distances by river and by
sea, so the channels have to be reconstructed before the distances can be
measured against any candidate.

Orengo, Hector A., and Cameron A. Petrie. "Large-Scale, Multi-Temporal Remote Sensing of Palaeo-River Networks: A Case Study from Northwest India and Its Implications for the Indus Civilisation." *Remote Sensing* 9, no. 7 (2017): 735. https://doi.org/10.3390/rs9070735.

Mapping vanished river channels using multi-temporal satellite imagery, retaining a classification probability per pixel rather than a fixed map.

Giosan, Liviu, Peter D. Clift, Mark G. Macklin, Dorian Q. Fuller, Stefan Constantinescu, Julie A. Durcan, Thomas Stevens, et al. "Fluvial Landscapes of the Harappan Civilization." *Proceedings of the National Academy of Sciences* 109, no. 26 (2012). https://doi.org/10.1073/pnas.1112743109.

Reconstructing the fluvial setting of an ancient civilisation using topography, sediment cores and dated channel deposits, taking into account that the rivers have since avulsed.

Giosan, Liviu, Stefan Constantinescu, Peter D. Clift, Ali R. Tabrez, Muhammed Danish, and Asif Inam. "Recent Morphodynamics of the Indus Delta Shore and Shelf." *Continental Shelf Research* 26, no. 14 (2006): 1668–84. https://doi.org/10.1016/j.csr.2006.05.009.

Quantifying delta shoreline change using nineteenth-century Admiralty surveys digitised into a terrain model, taking into account the diversion of the river by modern barrages. The direct precedent for Barbarikon.

Cahill, Niamh, Andrew C. Kemp, Benjamin P. Horton, and Andrew C. Parnell. "Modeling Sea-Level Change Using Errors-in-Variables Integrated Gaussian Processes." *The Annals of Applied Statistics* 9, no. 2 (2015): 547–71. https://doi.org/10.1214/15-AOAS824.

Reconstructing sea level change using Gaussian processes, taking into account age uncertainty.

Haslett, John, and Andrew Parnell. "A Simple Monotone Process with Application to Radiocarbon-Dated Depth Chronologies." *Journal of the Royal Statistical Society: Series C (Applied Statistics)* 57, no. 4 (2008): 399–418. https://doi.org/10.1111/j.1467-9876.2008.00623.x.

Building age-depth chronologies from sediment cores using a monotone stochastic process, taking into account radiocarbon calibration error.

Alappat, Linto, Manfred Frechen, S. Sree Kumar, D. S. Suresh Babu, Rajan Ravur, and Sumiko Tsukamoto. "Evidence of Late Holocene Shoreline Progradation in the Coast of Kerala, South India, Obtained from OSL Dating of Palaeo-Beach Ridges." *Geomorphology* 245 (2015): 73–86. https://doi.org/10.1016/j.geomorph.2015.05.006.

Dating successive shoreline positions using optically stimulated luminescence on beach ridges, giving the Kerala coast at known dates.

Shaji, Jithu, Upasana S. Banerji, K. Maya, Kumar Batuk Joshi, Ankur J. Dabhi, Nisha Bharti, Ravi Bhushan, and D. Padmalal. "Holocene Monsoon and Sea-Level Variability from Coastal Lowlands of Kerala, SW India." *Quaternary International* 642 (2022): 48–62. https://doi.org/10.1016/j.quaint.2022.03.005.

Reconstructing the regional relative sea-level curve from coastal lowland cores, which is the datum the Kerala coastline prior is measured against.

---

## 3. Voyages and routes across this ocean

Turning wind into reachability, and the closest prior work on this particular
ocean.

Copeland, Conrad. "Riding the Monsoon: Geography and Iron Age Trade in the Indian Ocean." *The Economic History Review* 79, no. 1 (2026): 312–41. https://doi.org/10.1111/ehr.70016.

Modelling Indian Ocean trade routes using least-cost network analysis over monsoon wind vectors and palaeo sea-level, reporting 14-day outbound and 16-day return averages. The closest prior work to our voyage layer, and the source of the 44-port coordinate set in our gazetteer.

McLean, Andrew, and Xavier Rubio-Campillo. "Beyond Least Cost Paths: Circuit Theory, Maritime Mobility and Patterns of Urbanism in the Roman Adriatic." *Journal of Archaeological Science* 138 (2022): 105534. https://doi.org/10.1016/j.jas.2021.105534.

Modelling maritime movement as a distribution over crossings using circuit theory, rather than as a single optimal route. The argument for simulating voyages instead of computing one path.

Slayton, Emma, Katherine Jarriel, Alvaro Montenegro, Crystal Safadi, Karl Smith, and Sara Zaia. "Seafaring and Modelling." *Journal of Maritime Archaeology* 20, no. 3 (2025): 601–28. https://doi.org/10.1007/s11457-025-09455-5.

Reviewing the state of computational seafaring models, read for the survey rather than for a method.

Evans, Tim S., and Ray J. Rivers. "Was Thebes Necessary? Contingency in Spatial Modeling." *Frontiers in Digital Humanities* 4 (2017): 8. https://doi.org/10.3389/fdigh.2017.00008.

Modelling ancient settlement networks using a retail gravity model, taking into account how sensitive the outcome is to initial conditions.

---

## 4. Where sites are, given the landscape

The spatial prior, and the coin hoard layer.

Crema, Enrico R., Andrew Bevan, and Mark W. Lake. "A Probabilistic Framework for Assessing Spatio-Temporal Point Patterns in the Archaeological Record." *Journal of Archaeological Science* 37, no. 5 (2010): 1118–30. https://doi.org/10.1016/j.jas.2009.12.012.

Analysing site distributions using spatio-temporal point processes, taking into account uncertainty in both the location and the date of each find.

Bilotti, Giacomo, Markus Reindel, Johny Isla, and Christian Mader. "Points, Patterns, and Predictions in Archaeological Settlement Data: Site-Environment Relationships of Paracas and Nasca Communities in the Peruvian Andes." *Journal of Archaeological Science* 183 (2025): 106385. https://doi.org/10.1016/j.jas.2025.106385.

Modelling where settlements are using inhomogeneous point processes with environmental covariates.

Herrera Malatesta, Eduardo, Jorge Ulloa Hung, and Corinne L. Hofman. "Looking at the Big Picture: Using Spatial Statistical Analyses to Study Indigenous Settlement Patterns in the North-Western Dominican Republic." *Journal of Computer Applications in Archaeology* 6, no. 1 (2023): 16–28. https://doi.org/10.5334/jcaa.83.

Studying settlement patterns using spatial point statistics against environmental variables, as an open-access worked example.

---

## 5. Combining many uncertain dates

Price, Michael Holton, José M. Capriles, Julie A. Hoggarth, R. Kyle Bocinsky, Claire E. Ebert, and James Holland Jones. "End-to-End Bayesian Analysis for Summarizing Sets of Radiocarbon Dates." *Journal of Archaeological Science* 135 (2021): 105473. https://doi.org/10.1016/j.jas.2021.105473.

Summarising many radiocarbon dates using a single end-to-end Bayesian model, taking into account calibration uncertainty at every stage.

---

## 6. Simulation-based inference, only if we commit to it

These are relevant only if the voyage simulator is used to *estimate* its own
parameters against the Periplus's stated durations. If the simulator is only run
forward to produce a reachability covariate, this section is background reading
and not method. That decision is open. See the note in `STATISTICAL-PLAN.md`.

DiNapoli, Robert J., Enrico R. Crema, Carl P. Lipo, Timothy M. Rieth, and Terry L. Hunt. "Approximate Bayesian Computation of Radiocarbon and Paleoenvironmental Record Shows Population Resilience on Rapa Nui (Easter Island)." *Nature Communications* 12, no. 1 (2021): 3939. https://doi.org/10.1038/s41467-021-24252-z.

Inferring past population change using approximate Bayesian computation, taking into account a simulation model with no tractable likelihood.

Rubio-Campillo, Xavier. "Model Selection in Historical Research Using Approximate Bayesian Computation." *PLOS ONE* 11, no. 1 (2016): e0146491. https://doi.org/10.1371/journal.pone.0146491.

Comparing competing historical explanations using approximate Bayesian computation, rather than fitting a single model.

Cranmer, Kyle, Johann Brehmer, and Gilles Louppe. "The Frontier of Simulation-Based Inference." *Proceedings of the National Academy of Sciences* 117, no. 48 (2020): 30055–62. https://doi.org/10.1073/pnas.1912789117.

Surveying methods for inference when a model can be simulated but its likelihood cannot be written down.
