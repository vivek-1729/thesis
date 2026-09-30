# Statistical methods, with precedents in reconstructing the past

These papers are about building the prior: modelling sea level change, the water
surface and the river channels, to put a coastline somewhere at a given date.
The evidence is scattered dated points; the object wanted is a surface.

Eight papers, ordered by how much work each does for the thesis. One plain
sentence each. Citations are Chicago, checked against Crossref. The geographic
and voyage modelling literature is in `READING-GEOGRAPHIC.md`.

---

**1.** Cahill, Niamh, Andrew C. Kemp, Benjamin P. Horton, and Andrew C. Parnell. "Modeling Sea-Level Change Using Errors-in-Variables Integrated Gaussian Processes." *The Annals of Applied Statistics* 9, no. 2 (2015): 547–71. https://doi.org/10.1214/15-AOAS824.

Reconstructing sea level change using Gaussian processes, taking into account age uncertainty.

**2.** Lindgren, Finn, Håvard Rue, and Johan Lindström. "An Explicit Link between Gaussian Fields and Gaussian Markov Random Fields: The Stochastic Partial Differential Equation Approach." *Journal of the Royal Statistical Society: Series B (Statistical Methodology)* 73, no. 4 (2011): 423–98. https://doi.org/10.1111/j.1467-9868.2011.00777.x.

Reconstructing a continuous surface over an irregular domain by meshing it and solving an SPDE, which we can use to construct a water surface from scattered data points

**3.** Ver Hoef, Jay M., and Erin E. Peterson. "A Moving Average Approach for Spatial Statistical Models of Stream Networks." *Journal of the American Statistical Association* 105, no. 489 (2010): 6–18. https://doi.org/10.1198/jasa.2009.ap08248.

Geostatistics in which distance runs along a branching river network rather than in a straight line.

**4.** Leon, Javier X., Gerard B. M. Heuvelink, and Stuart R. Phinn. "Incorporating DEM Uncertainty in Coastal Inundation Mapping." *PLOS ONE* 9, no. 9 (2014): e108727. https://doi.org/10.1371/journal.pone.0108727.

Turning elevation error into a shoreline position, by treating the error as a random field and simulating from it.

**5.** Haslett, John, and Andrew Parnell. "A Simple Monotone Process with Application to Radiocarbon-Dated Depth Chronologies." *Journal of the Royal Statistical Society: Series C (Applied Statistics)* 57, no. 4 (2008): 399–418. https://doi.org/10.1111/j.1467-9876.2008.00623.x.

Turning a sediment core into a dated sequence, with the radiocarbon uncertainty carried through.

**6.** Ashe, Erica L., Niamh Cahill, Carling Hay, Nicole S. Khan, Andrew Kemp, Simon E. Engelhart, Benjamin P. Horton, Andrew C. Parnell, and Robert E. Kopp. "Statistical Modeling of Rates and Trends in Holocene Relative Sea Level." *Quaternary Science Reviews* 204 (2019): 58–77. https://doi.org/10.1016/j.quascirev.2018.10.032.

A review putting the competing approaches to sea-level reconstruction into one hierarchical framework.

**7.** Upton, Maeve, Andrew Parnell, Andrew Kemp, Gerard McCarthy, and Niamh Cahill. "A Noisy-Input Generalized Additive Model for Relative Sea-Level Change along the Atlantic Coast of North America." *Journal of the Royal Statistical Society: Series C (Applied Statistics)* 74, no. 1 (2024): 34–82. https://doi.org/10.1093/jrsssc/qlae044.

Separating a sea-level signal into regional, local and common parts when the inputs are themselves uncertain.
**8.** Ashe, Erica L., Nicole S. Khan, Lauren T. Toth, Andrea Dutton, and Robert E. Kopp. "A Statistical Framework for Integrating Nonparametric Proxy Distributions into Geological Reconstructions of Relative Sea Level." *Advances in Statistical Climatology, Meteorology and Oceanography* 8, no. 1 (2022): 1–29. https://doi.org/10.5194/ascmo-8-1-2022.

Combining proxies whose uncertainties are differently shaped, without first forcing them into a common form.
