# Statistical methods, with precedents in reconstructing the past

Statistics papers only. Each is a process the thesis needs, and where possible
one that has already been applied to archaeological or historical data. Citations
are Chicago, checked against Crossref. The geographic, remote sensing and voyage
modelling literature is in `READING-GEOGRAPHIC.md`.

---

**1.** Diggle, Peter J., Raquel Menezes, and Ting-li Su. "Geostatistical Inference under Preferential Sampling." *Journal of the Royal Statistical Society: Series C (Applied Statistics)* 59, no. 2 (2010): 191–232. https://doi.org/10.1111/j.1467-9876.2009.00701.x.

Estimating a spatial field using a joint model for the sampling process, taking into account that the sample locations were chosen by what was expected to be found there.

**2.** Pati, Debdeep, Brian J. Reich, and David B. Dunson. "Bayesian Geostatistical Modelling with Informative Sampling Locations." *Biometrika* 98, no. 1 (2011): 35–48. https://doi.org/10.1093/biomet/asq067.

The same problem in a fully Bayesian frame, with the sampling intensity and the field linked through shared latent structure rather than through a single dependence parameter.

**3.** Diggle, Peter J., Paula Moraga, Barry Rowlingson, and Benjamin M. Taylor. "Spatial and Spatio-Temporal Log-Gaussian Cox Processes: Extending the Geostatistical Paradigm." *Statistical Science* 28, no. 4 (2013). https://doi.org/10.1214/13-STS441.

Modelling event locations as a point process whose intensity is itself a random field, which is the machinery underneath both the sampling correction and the hoard distribution.

**4.** Cahill, Niamh, Andrew C. Kemp, Benjamin P. Horton, and Andrew C. Parnell. "Modeling Sea-Level Change Using Errors-in-Variables Integrated Gaussian Processes." *The Annals of Applied Statistics* 9, no. 2 (2015): 547–71. https://doi.org/10.1214/15-AOAS824.

Reconstructing sea level change using Gaussian processes, taking into account age uncertainty.

**5.** Haslett, John, and Andrew Parnell. "A Simple Monotone Process with Application to Radiocarbon-Dated Depth Chronologies." *Journal of the Royal Statistical Society: Series C (Applied Statistics)* 57, no. 4 (2008): 399–418. https://doi.org/10.1111/j.1467-9876.2008.00623.x.

Building age-depth chronologies from sediment cores using a monotone stochastic process, taking into account radiocarbon calibration error.

**6.** Heaton, Timothy J. "Non-Parametric Calibration of Multiple Related Radiocarbon Determinations and Their Calendar Age Summarisation." *Journal of the Royal Statistical Society: Series C (Applied Statistics)* 71, no. 5 (2022): 1918–56. https://doi.org/10.1111/rssc.12599.

Calibrating a set of related radiocarbon dates jointly using a Dirichlet process mixture, taking into account that a non-monotone calibration curve turns single dates into multimodal posteriors.

**7.** Nicholls, Geoff, and Martin Jones. "Radiocarbon Dating with Temporal Order Constraints." *Journal of the Royal Statistical Society: Series C (Applied Statistics)* 50, no. 4 (2001): 503–21. https://doi.org/10.1111/1467-9876.00250.

Estimating calendar dates under known stratigraphic ordering, which is how excavation layers constrain each other and how a site sequence becomes one chronological model.

**8.** MacKenzie, Darryl I., James D. Nichols, Gideon B. Lachman, Sam Droege, J. Andrew Royle, and Catherine A. Langtimm. "Estimating Site Occupancy Rates When Detection Probabilities Are Less Than One." *Ecology* 83, no. 8 (2002): 2248–55. https://doi.org/10.1890/0012-9658(2002)083[2248:ESORWD]2.0.CO;2.

Separating a site being unoccupied from a site being occupied but undetected, with detection modelled as a function of survey effort. The excavation record has exactly this structure and is almost never treated this way.

**9.** Crema, Enrico R., Andrew Bevan, and Mark W. Lake. "A Probabilistic Framework for Assessing Spatio-Temporal Point Patterns in the Archaeological Record." *Journal of Archaeological Science* 37, no. 5 (2010): 1118–30. https://doi.org/10.1016/j.jas.2009.12.012.

Analysing site distributions using spatio-temporal point processes, taking into account uncertainty in both the location and the date of each find.

**10.** Buck, C. E., C. D. Litton, and A. F. M. Smith. "Calibration of Radiocarbon Results Pertaining to Related Archaeological Events." *Journal of Archaeological Science* 19, no. 5 (1992): 497–512. https://doi.org/10.1016/0305-4403(92)90025-X.

The paper that put archaeological chronology into a Bayesian frame, treating stratigraphic and historical knowledge as a prior over the dates rather than as commentary on them.

**11.** Price, Michael Holton, José M. Capriles, Julie A. Hoggarth, R. Kyle Bocinsky, Claire E. Ebert, and James Holland Jones. "End-to-End Bayesian Analysis for Summarizing Sets of Radiocarbon Dates." *Journal of Archaeological Science* 135 (2021): 105473. https://doi.org/10.1016/j.jas.2021.105473.

Summarising many radiocarbon dates using a single end-to-end Bayesian model, taking into account calibration uncertainty at every stage.

**12.** Rubio-Campillo, Xavier. "Model Selection in Historical Research Using Approximate Bayesian Computation." *PLOS ONE* 11, no. 1 (2016): e0146491. https://doi.org/10.1371/journal.pone.0146491.

Comparing competing historical explanations using approximate Bayesian computation, rather than fitting a single model.

**13.** Cranmer, Kyle, Johann Brehmer, and Gilles Louppe. "The Frontier of Simulation-Based Inference." *Proceedings of the National Academy of Sciences* 117, no. 48 (2020): 30055–62. https://doi.org/10.1073/pnas.1912789117.

Surveying methods for inference when a model can be simulated but its likelihood cannot be written down. Relevant only if the voyage simulator is used to estimate its own parameters rather than to produce a covariate, which is an open decision recorded in `STATISTICAL-PLAN.md`.

**14.** Crema, Enrico R. "Statistical Modelling in Archaeology: Some Recent Trends and Future Perspectives." *Journal of Archaeological Science* 180 (2025): 106295. https://doi.org/10.1016/j.jas.2025.106295.

A survey of where statistical modelling in archaeology currently stands, useful for locating this thesis within that literature.

**15.** Çadırcı, Mehmet Sıddık, and Golnaz Shahtahmassebi. "Entropy-Based Methods to Address Sampling Bias in Archaeological Predictive Modeling." arXiv, August 4, 2025. https://arxiv.org/abs/2508.02272.

Correcting archaeological predictive models using entropy-weighted measures of survey coverage. An unrefereed preprint, kept only because it is the one direct statement of the preferential sampling problem inside the archaeological literature.
