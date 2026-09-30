# Reading for the geographic and voyage layers

Not statistics. These are the domain papers behind Phase 1's geographic step and
the voyage layer: coastline and channel reconstruction, monsoon routing, and
worked archaeological applications of spatial models. Read for method and for
data, not to send to a statistician. The statistics papers are in
`READING-FOR-STATS-ADVISOR.md`.

Citations are Chicago, checked against Crossref.

---

## 1. Recovering vanished river channels

Orengo, Hector A., and Cameron A. Petrie. "Large-Scale, Multi-Temporal Remote Sensing of Palaeo-River Networks: A Case Study from Northwest India and Its Implications for the Indus Civilisation." *Remote Sensing* 9, no. 7 (2017): 735. https://doi.org/10.3390/rs9070735.

Mapping vanished river channels using multi-temporal satellite imagery, retaining a classification probability per pixel rather than a fixed map. Over 8,000 km of relict channels recovered in northwest India. This is the method for the Periyar and the Indus.

Giosan, Liviu, Peter D. Clift, Mark G. Macklin, Dorian Q. Fuller, Stefan Constantinescu, Julie A. Durcan, Thomas Stevens, et al. "Fluvial Landscapes of the Harappan Civilization." *Proceedings of the National Academy of Sciences* 109, no. 26 (2012). https://doi.org/10.1073/pnas.1112743109.

Reconstructing the fluvial setting of an ancient civilisation using topography, sediment cores and dated channel deposits, taking into account that the rivers have since avulsed.

Giosan, Liviu, Stefan Constantinescu, Peter D. Clift, Ali R. Tabrez, Muhammed Danish, and Asif Inam. "Recent Morphodynamics of the Indus Delta Shore and Shelf." *Continental Shelf Research* 26, no. 14 (2006): 1668–84. https://doi.org/10.1016/j.csr.2006.05.009.

Quantifying delta shoreline change using nineteenth-century Admiralty surveys digitised into a terrain model, taking into account the diversion of the river by modern barrages. The direct precedent for Barbarikon, and the proof that step 2 of the geographic plan works.

---

## 2. The Kerala coastline at known dates

Alappat, Linto, Manfred Frechen, S. Sree Kumar, D. S. Suresh Babu, Rajan Ravur, and Sumiko Tsukamoto. "Evidence of Late Holocene Shoreline Progradation in the Coast of Kerala, South India, Obtained from OSL Dating of Palaeo-Beach Ridges." *Geomorphology* 245 (2015): 73–86. https://doi.org/10.1016/j.geomorph.2015.05.006.

Dating successive shoreline positions using optically stimulated luminescence on beach ridges, giving the Kerala coast at known dates.

Shaji, Jithu, Upasana S. Banerji, K. Maya, Kumar Batuk Joshi, Ankur J. Dabhi, Nisha Bharti, Ravi Bhushan, and D. Padmalal. "Holocene Monsoon and Sea-Level Variability from Coastal Lowlands of Kerala, SW India." *Quaternary International* 642 (2022): 48–62. https://doi.org/10.1016/j.quaint.2022.03.005.

Reconstructing the regional relative sea-level curve from coastal lowland cores, which is the datum the Kerala coastline prior is measured against.

---

## 3. Voyages and routes across this ocean

Copeland, Conrad. "Riding the Monsoon: Geography and Iron Age Trade in the Indian Ocean." *The Economic History Review* 79, no. 1 (2026): 312–41. https://doi.org/10.1111/ehr.70016.

Modelling Indian Ocean trade routes using least-cost network analysis over monsoon wind vectors and palaeo sea-level, reporting 14-day outbound and 16-day return averages. The closest prior work to our voyage layer, and the source of the 44-port coordinate set in our gazetteer.

McLean, Andrew, and Xavier Rubio-Campillo. "Beyond Least Cost Paths: Circuit Theory, Maritime Mobility and Patterns of Urbanism in the Roman Adriatic." *Journal of Archaeological Science* 138 (2022): 105534. https://doi.org/10.1016/j.jas.2021.105534.

Modelling maritime movement as a distribution over crossings using circuit theory, rather than as a single optimal route. The argument for simulating voyages instead of computing one path.

Slayton, Emma, Katherine Jarriel, Alvaro Montenegro, Crystal Safadi, Karl Smith, and Sara Zaia. "Seafaring and Modelling." *Journal of Maritime Archaeology* 20, no. 3 (2025): 601–28. https://doi.org/10.1007/s11457-025-09455-5.

Reviewing the state of computational seafaring models, read for the survey rather than for a method.

Evans, Tim S., and Ray J. Rivers. "Was Thebes Necessary? Contingency in Spatial Modeling." *Frontiers in Digital Humanities* 4 (2017): 8. https://doi.org/10.3389/fdigh.2017.00008.

Modelling ancient settlement networks using a retail gravity model, taking into account how sensitive the outcome is to initial conditions.

---

## 4. Worked applications of spatial models to settlement

Examples rather than methods. Read for how the argument is presented and what
the output looks like.

Bilotti, Giacomo, Markus Reindel, Johny Isla, and Christian Mader. "Points, Patterns, and Predictions in Archaeological Settlement Data: Site-Environment Relationships of Paracas and Nasca Communities in the Peruvian Andes." *Journal of Archaeological Science* 183 (2025): 106385. https://doi.org/10.1016/j.jas.2025.106385.

Modelling where settlements are using inhomogeneous point processes with environmental covariates.

Herrera Malatesta, Eduardo, Jorge Ulloa Hung, and Corinne L. Hofman. "Looking at the Big Picture: Using Spatial Statistical Analyses to Study Indigenous Settlement Patterns in the North-Western Dominican Republic." *Journal of Computer Applications in Archaeology* 6, no. 1 (2023): 16–28. https://doi.org/10.5334/jcaa.83.

Studying settlement patterns using spatial point statistics against environmental variables, as an open-access worked example.
