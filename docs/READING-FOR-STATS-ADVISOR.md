# Statistical methods, with precedents in reconstructing the past

Nine papers, one per statistical process the thesis needs, chosen so that
nothing here duplicates anything else. Weighted toward reconstructing the
physical setting, since that is what actually locates the ports. Citations are Chicago, checked against
Crossref. The geographic, remote sensing and voyage modelling literature is in
`READING-GEOGRAPHIC.md`.

---

**1.** Diggle, Peter J., Raquel Menezes, and Ting-li Su. "Geostatistical Inference under Preferential Sampling." *Journal of the Royal Statistical Society: Series C (Applied Statistics)* 59, no. 2 (2010): 191–232. https://doi.org/10.1111/j.1467-9876.2009.00701.x.

Estimating a spatial field using a joint model for the sampling process, taking into account that the sample locations were chosen by what was expected to be found there.

**2.** Diggle, Peter J., Paula Moraga, Barry Rowlingson, and Benjamin M. Taylor. "Spatial and Spatio-Temporal Log-Gaussian Cox Processes: Extending the Geostatistical Paradigm." *Statistical Science* 28, no. 4 (2013). https://doi.org/10.1214/13-STS441.

Modelling event locations as a point process whose intensity is itself a random field, which is the machinery underneath the sampling correction.

**3.** Cahill, Niamh, Andrew C. Kemp, Benjamin P. Horton, and Andrew C. Parnell. "Modeling Sea-Level Change Using Errors-in-Variables Integrated Gaussian Processes." *The Annals of Applied Statistics* 9, no. 2 (2015): 547–71. https://doi.org/10.1214/15-AOAS824.

Reconstructing sea level change using Gaussian processes, taking into account age uncertainty.

**4.** Ashe, Erica L., Niamh Cahill, Carling Hay, Nicole S. Khan, Andrew Kemp, Simon E. Engelhart, Benjamin P. Horton, Andrew C. Parnell, and Robert E. Kopp. "Statistical Modeling of Rates and Trends in Holocene Relative Sea Level." *Quaternary Science Reviews* 204 (2019): 58–77. https://doi.org/10.1016/j.quascirev.2018.10.032.

Putting the competing approaches to sea-level reconstruction, from spline regression to Gaussian process priors, into a single hierarchical framework so they can be compared rather than argued over.

**5.** Upton, Maeve, Andrew Parnell, Andrew Kemp, Gerard McCarthy, and Niamh Cahill. "A Noisy-Input Generalized Additive Model for Relative Sea-Level Change along the Atlantic Coast of North America." *Journal of the Royal Statistical Society: Series C (Applied Statistics)* 74, no. 1 (2024): 34–82. https://doi.org/10.1093/jrsssc/qlae044.

Reconstructing sea level with a generalised additive model whose inputs are themselves uncertain, decomposing the signal into regional, local and common components.

**6.** Ashe, Erica L., Nicole S. Khan, Lauren T. Toth, Andrea Dutton, and Robert E. Kopp. "A Statistical Framework for Integrating Nonparametric Proxy Distributions into Geological Reconstructions of Relative Sea Level." *Advances in Statistical Climatology, Meteorology and Oceanography* 8, no. 1 (2022): 1–29. https://doi.org/10.5194/ascmo-8-1-2022.

Combining proxies whose individual uncertainties are non-Gaussian and differently shaped, without forcing them into a common parametric form first.

**7.** Leon, Javier X., Gerard B. M. Heuvelink, and Stuart R. Phinn. "Incorporating DEM Uncertainty in Coastal Inundation Mapping." *PLOS ONE* 9, no. 9 (2014): e108727. https://doi.org/10.1371/journal.pone.0108727.

Treating elevation error as a spatially correlated random field, simulating from it, and propagating the result through to where the land and water boundary falls. The only one of these that produces a shoreline position rather than a sea level.

**8.** Haslett, John, and Andrew Parnell. "A Simple Monotone Process with Application to Radiocarbon-Dated Depth Chronologies." *Journal of the Royal Statistical Society: Series C (Applied Statistics)* 57, no. 4 (2008): 399–418. https://doi.org/10.1111/j.1467-9876.2008.00623.x.

Building age-depth chronologies from sediment cores using a monotone stochastic process, taking into account radiocarbon calibration error.

**9.** MacKenzie, Darryl I., James D. Nichols, Gideon B. Lachman, Sam Droege, J. Andrew Royle, and Catherine A. Langtimm. "Estimating Site Occupancy Rates When Detection Probabilities Are Less Than One." *Ecology* 83, no. 8 (2002): 2248–55. https://doi.org/10.1890/0012-9658(2002)083[2248:ESORWD]2.0.CO;2.

Separating a site being unoccupied from a site being occupied but undetected, with detection modelled as a function of survey effort. The excavation record has exactly this structure and is almost never treated this way.
