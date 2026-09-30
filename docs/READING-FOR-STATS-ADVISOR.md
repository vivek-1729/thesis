# Statistical methods, with published precedents in reconstructing the past

One line per paper. Each is a method the thesis needs, shown in a place where it
has already been applied to a question about the ancient world, so the reference
carries both the technique and the evidence that it transfers.

## Send these five

1. Modeling sea-level change using errors-in-variables integrated Gaussian processes; Cahill, Kemp, Horton and Parnell (2015). *Annals of Applied Statistics* 9, 547-571. doi:10.1214/15-AOAS824. A GP prior on the rate of change, integrated and set in an errors-in-variables frame so proxy age uncertainty carries through; the structure for putting a band on the first-century coastline, and for the textual distances. Preprint: https://arxiv.org/pdf/1312.6761
2. Geostatistical inference under preferential sampling; Diggle, Menezes and Su (2010). *JRSS Series C* 59, 191-232. doi:10.1111/j.1467-9876.2009.00701.x. Sampling locations that depend stochastically on the field being sampled, modelled jointly as a log-Gaussian Cox process; archaeologists dug where they already believed the port was, so absence of finds is not independent of the location being estimated.
3. Approximate Bayesian Computation of radiocarbon and paleoenvironmental record shows population resilience on Rapa Nui; DiNapoli, Crema, Lipo, Rieth and Hunt (2021). *Nature Communications* 12. https://www.nature.com/articles/s41467-021-24252-z. ABC fitting a simulation of the past to archaeological and palaeoenvironmental data with model comparison; the wind and voyage model is a simulator with no tractable likelihood, so this is the inferential route.
4. A simple monotone process with application to radiocarbon-dated depth chronologies; Haslett and Parnell (2008). *JRSS Series C* 57, 399-418. doi:10.1111/j.1467-9876.2008.00623.x. Age-depth reconstruction as inference on a partially observed monotone process built from gamma increments; the machinery for turning sediment cores into dated surfaces with honest uncertainty.
5. A probabilistic framework for assessing spatio-temporal point patterns in the archaeological record; Crema, Bevan and Lake (2010). *Journal of Archaeological Science* 37. https://www.sciencedirect.com/science/article/abs/pii/S0305440309004622. Point pattern analysis where both the location and the date of each find carry uncertainty, which is the situation for the coin hoards.

## The rest

6. Large-scale, multi-temporal remote sensing of palaeo-river networks; Orengo and Petrie (2017). *Remote Sensing* 9. https://www.mdpi.com/2072-4292/9/7/735. Over 8,000 km of relict channels recovered in northwest India from seasonal vegetation dynamics, output as a per-pixel classification probability rather than an asserted map; the method for the Indus and Periyar channels.
7. Model selection in historical research using approximate Bayesian computation; Rubio-Campillo (2016). *PLoS ONE* 11. https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0146491. ABC used to choose between competing historical explanations, which is structurally what choosing between candidate port locations is.
8. The frontier of simulation-based inference; Cranmer, Brehmer and Louppe (2020). *PNAS* 117. doi:10.1073/pnas.1912789117. The canonical citation if the method needs one.
9. Points, patterns, and predictions in archaeological settlement data; Bilotti, Reindel, Isla and Mader (2025). *Journal of Archaeological Science* 183. https://www.sciencedirect.com/science/article/pii/S0305440325002341. Inhomogeneous point process models with environmental covariates estimating site-environment relationships; the structure of the geographic prior.
10. Entropy-based methods to address sampling bias in archaeological predictive modeling; Çadırcı and Shahtahmassebi (2025). arXiv:2508.02272. https://arxiv.org/pdf/2508.02272. The archaeological statement of the preferential sampling problem and the current state of that literature.
11. End-to-end Bayesian analysis for summarizing sets of radiocarbon dates; Price, Capriles, Hoggarth, Bocinsky, Ebert and Jones (2021). *Journal of Archaeological Science* 135, 105473. https://www.sciencedirect.com/science/article/pii/S0305440321001436. Aggregating many individually uncertain dates without the artefacts naive summation produces; relevant to combining site chronologies across the excavation record.
12. Looking at the big picture: using spatial statistical analyses to study indigenous settlement patterns in the north-western Dominican Republic; Herrera Malatesta, Ulloa Hung and Hofman (2023). *Journal of Computer Applications in Archaeology* 6, 16-28. https://journal.caa-international.org/articles/10.5334/jcaa.83. Open access, and a clean worked example of fitting point process models to settlement data.
13. Was Thebes necessary? Contingency in spatial modelling; Evans and Rivers (2017). *Frontiers in Digital Humanities* 4:8. doi:10.3389/fdigh.2017.00008. A re-examination of the rise of the Greek city-states with the Rihll and Wilson retail gravity model, asking how much of the outcome is forced by geography; the precedent for the trade-network layer, and a caution about how much weight it can bear.

## If only three

Cahill et al. 2015 for the reconstruction machinery, Diggle et al. 2010 for the
identification problem, and DiNapoli et al. 2021 for simulation-based inference
on archaeological data. Between them they cover the three statistical problems
the thesis actually has.
