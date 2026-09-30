# Statistical methods, with precedents in reconstructing the past

Ten papers, ordered by how much work each does for the thesis. Weighted
toward reconstructing the physical setting, because that is what actually
locates a port; the excavation record can confirm a candidate but rarely
discriminates between them. Citations are Chicago, checked against
Crossref. The geographic, remote sensing and voyage modelling literature is in
`READING-GEOGRAPHIC.md`.

---

**1.** Cahill, Niamh, Andrew C. Kemp, Benjamin P. Horton, and Andrew C. Parnell. "Modeling Sea-Level Change Using Errors-in-Variables Integrated Gaussian Processes." *The Annals of Applied Statistics* 9, no. 2 (2015): 547–71. https://doi.org/10.1214/15-AOAS824.

Reconstructing sea level change using Gaussian processes, taking into account age uncertainty.

**2.** Lindgren, Finn, Håvard Rue, and Johan Lindström. "An Explicit Link between Gaussian Fields and Gaussian Markov Random Fields: The Stochastic Partial Differential Equation Approach." *Journal of the Royal Statistical Society: Series B (Statistical Methodology)* 73, no. 4 (2011): 423–98. https://doi.org/10.1111/j.1467-9868.2011.00777.x.

Representing a continuous spatial field as a sparse Markov random field by solving an SPDE on a triangulated domain, which makes irregular and constrained geographies tractable. The machinery the next two papers are built on.

**3.** Bakka, Haakon, Jarno Vanhatalo, Janine B. Illian, Daniel Simpson, and Håvard Rue. "Non-Stationary Gaussian Models with Physical Barriers." *Spatial Statistics* 29 (2019): 268–88. https://doi.org/10.1016/j.spasta.2019.01.002.

Building a spatial field in which correlation is blocked by land rather than travelling through it, so two points either side of a headland are not treated as neighbours. The right geometry for a coast with backwaters and islands.

**4.** Ver Hoef, Jay M., and Erin E. Peterson. "A Moving Average Approach for Spatial Statistical Models of Stream Networks." *Journal of the American Statistical Association* 105, no. 489 (2010): 6–18. https://doi.org/10.1198/jasa.2009.ap08248.

Geostatistics in which distance is measured along a branching channel network rather than in a straight line, and correlation follows flow. The Periplus gives the Malabar distances by river and by sea, which is this problem.

**5.** Leon, Javier X., Gerard B. M. Heuvelink, and Stuart R. Phinn. "Incorporating DEM Uncertainty in Coastal Inundation Mapping." *PLOS ONE* 9, no. 9 (2014): e108727. https://doi.org/10.1371/journal.pone.0108727.

Treating elevation error as a spatially correlated random field, simulating from it, and propagating the result through to where the land and water boundary falls. The only one of these that produces a shoreline position rather than a sea level.

**6.** Haslett, John, and Andrew Parnell. "A Simple Monotone Process with Application to Radiocarbon-Dated Depth Chronologies." *Journal of the Royal Statistical Society: Series C (Applied Statistics)* 57, no. 4 (2008): 399–418. https://doi.org/10.1111/j.1467-9876.2008.00623.x.

Building age-depth chronologies from sediment cores using a monotone stochastic process, taking into account radiocarbon calibration error.

**7.** Ashe, Erica L., Niamh Cahill, Carling Hay, Nicole S. Khan, Andrew Kemp, Simon E. Engelhart, Benjamin P. Horton, Andrew C. Parnell, and Robert E. Kopp. "Statistical Modeling of Rates and Trends in Holocene Relative Sea Level." *Quaternary Science Reviews* 204 (2019): 58–77. https://doi.org/10.1016/j.quascirev.2018.10.032.

Putting the competing approaches to sea-level reconstruction, from spline regression to Gaussian process priors, into a single hierarchical framework so they can be compared rather than argued over.

**8.** Upton, Maeve, Andrew Parnell, Andrew Kemp, Gerard McCarthy, and Niamh Cahill. "A Noisy-Input Generalized Additive Model for Relative Sea-Level Change along the Atlantic Coast of North America." *Journal of the Royal Statistical Society: Series C (Applied Statistics)* 74, no. 1 (2024): 34–82. https://doi.org/10.1093/jrsssc/qlae044.

Reconstructing sea level with a generalised additive model whose inputs are themselves uncertain, decomposing the signal into regional, local and common components.

**9.** Ashe, Erica L., Nicole S. Khan, Lauren T. Toth, Andrea Dutton, and Robert E. Kopp. "A Statistical Framework for Integrating Nonparametric Proxy Distributions into Geological Reconstructions of Relative Sea Level." *Advances in Statistical Climatology, Meteorology and Oceanography* 8, no. 1 (2022): 1–29. https://doi.org/10.5194/ascmo-8-1-2022.

Combining proxies whose individual uncertainties are non-Gaussian and differently shaped, without forcing them into a common parametric form first.

**10.** MacKenzie, Darryl I., James D. Nichols, Gideon B. Lachman, Sam Droege, J. Andrew Royle, and Catherine A. Langtimm. "Estimating Site Occupancy Rates When Detection Probabilities Are Less Than One." *Ecology* 83, no. 8 (2002): 2248–55. https://doi.org/10.1890/0012-9658(2002)083[2248:ESORWD]2.0.CO;2.

Separating a site being unoccupied from a site being occupied but undetected, with detection modelled as a function of survey effort. The excavation record has exactly this structure and is almost never treated this way.
