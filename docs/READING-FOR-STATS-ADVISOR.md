# Statistical methods, with precedents in reconstructing the past

Seven papers, one per statistical process the thesis needs, chosen so that
nothing here duplicates anything else. Citations are Chicago, checked against
Crossref. The geographic, remote sensing and voyage modelling literature is in
`READING-GEOGRAPHIC.md`.

---

**1.** Diggle, Peter J., Raquel Menezes, and Ting-li Su. "Geostatistical Inference under Preferential Sampling." *Journal of the Royal Statistical Society: Series C (Applied Statistics)* 59, no. 2 (2010): 191–232. https://doi.org/10.1111/j.1467-9876.2009.00701.x.

Estimating a spatial field using a joint model for the sampling process, taking into account that the sample locations were chosen by what was expected to be found there.

**2.** Diggle, Peter J., Paula Moraga, Barry Rowlingson, and Benjamin M. Taylor. "Spatial and Spatio-Temporal Log-Gaussian Cox Processes: Extending the Geostatistical Paradigm." *Statistical Science* 28, no. 4 (2013). https://doi.org/10.1214/13-STS441.

Modelling event locations as a point process whose intensity is itself a random field, which is the machinery underneath the sampling correction.

**3.** Cahill, Niamh, Andrew C. Kemp, Benjamin P. Horton, and Andrew C. Parnell. "Modeling Sea-Level Change Using Errors-in-Variables Integrated Gaussian Processes." *The Annals of Applied Statistics* 9, no. 2 (2015): 547–71. https://doi.org/10.1214/15-AOAS824.

Reconstructing sea level change using Gaussian processes, taking into account age uncertainty.

**4.** Haslett, John, and Andrew Parnell. "A Simple Monotone Process with Application to Radiocarbon-Dated Depth Chronologies." *Journal of the Royal Statistical Society: Series C (Applied Statistics)* 57, no. 4 (2008): 399–418. https://doi.org/10.1111/j.1467-9876.2008.00623.x.

Building age-depth chronologies from sediment cores using a monotone stochastic process, taking into account radiocarbon calibration error.

**5.** Heaton, Timothy J. "Non-Parametric Calibration of Multiple Related Radiocarbon Determinations and Their Calendar Age Summarisation." *Journal of the Royal Statistical Society: Series C (Applied Statistics)* 71, no. 5 (2022): 1918–56. https://doi.org/10.1111/rssc.12599.

Calibrating a set of related radiocarbon dates jointly using a Dirichlet process mixture, taking into account that a non-monotone calibration curve turns single dates into multimodal posteriors.

**6.** MacKenzie, Darryl I., James D. Nichols, Gideon B. Lachman, Sam Droege, J. Andrew Royle, and Catherine A. Langtimm. "Estimating Site Occupancy Rates When Detection Probabilities Are Less Than One." *Ecology* 83, no. 8 (2002): 2248–55. https://doi.org/10.1890/0012-9658(2002)083[2248:ESORWD]2.0.CO;2.

Separating a site being unoccupied from a site being occupied but undetected, with detection modelled as a function of survey effort. The excavation record has exactly this structure and is almost never treated this way.

**7.** Crema, Enrico R. "Statistical Modelling in Archaeology: Some Recent Trends and Future Perspectives." *Journal of Archaeological Science* 180 (2025): 106295. https://doi.org/10.1016/j.jas.2025.106295.

A survey of where statistical modelling in archaeology currently stands, included so the rest can be judged against what the field already does.
