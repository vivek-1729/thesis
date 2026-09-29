# Statistical reading, by component

Organised against the four components of the proposal. Each entry says why it is
worth reading and what to take from it, since most of these are being read for a
method rather than for a result. Nothing here is held locally yet.

---

## Cross-cutting: Bayesian spatial models in archaeology

The closest existing literature to what the thesis is doing, and the place to
position it.

- **Entropy-Based Methods to Address Sampling Bias in Archaeological Predictive
  Modeling**, arXiv:2508.02272.
  https://arxiv.org/pdf/2508.02272
  The most directly relevant recent paper. Archaeological predictive modelling
  with explicit treatment of the fact that sites are found where people looked.
  Read it for how the field currently frames the bias problem, and for what our
  detection model adds over it.

- **Møller, Syversveen and Waagepetersen, "Log Gaussian Cox Processes"**,
  *Scandinavian Journal of Statistics* 25 (1998).
  https://archive.math.arizona.edu/jwatkins/log_Gaussian_Cox_Processes.pdf
  The foundational LGCP paper. Take the construction and the thinning property,
  which is how discovery probability enters the hoard model.

- **Diggle, "INLA for Spatial Statistics: Log-Gaussian Cox Processes"**, course
  notes.
  https://faculty.washington.edu/jonno/SISMIDmaterial/4-LGCPs.pdf
  Practical fitting rather than theory. Useful if the point-process layer is
  fitted in INLA rather than Stan.

---

## Component 1: Prior construction

### Travel time and maritime least-cost modelling

- **Leidwanger, "Modeling distance with time in ancient Mediterranean
  seafaring"**, *Journal of Archaeological Science* 41 (2014).
  https://www.sciencedirect.com/science/article/abs/pii/S0305440313001064
  The standard reference for treating sailing time rather than distance as the
  measure of separation. Directly supports our finding that the stadion behaves
  as a speed.

- **"Beyond Least Cost Paths: circuit theory, maritime mobility"**, *Journal of
  Archaeological Science* 2021.
  https://www.sciencedirect.com/science/article/pii/S0305440321002089
  Argues against single optimal routes in favour of a distribution over
  crossings. This is the argument for the Monte Carlo voyage simulation rather
  than a least-cost path.

- **Copeland, "Riding the monsoon: geography and Iron Age trade in the Indian
  Ocean"**, *Economic History Review* (2026).
  doi:10.1111/ehr.70016
  The only study doing network and least-cost analysis on this ocean with
  monsoon vectors and palaeo sea-level. Closest prior work to our voyage layer,
  and it reports 14-day outbound and 16-day return averages that our simulation
  should be checked against.

- **"Seafaring and Modelling"**, *Journal of Maritime Archaeology* (2025).
  doi:10.1007/s11457-025-09455-5
  A recent review of the modelling literature. Read for the survey rather than
  for a method.

### Sea level and palaeo-coastline, specifically for Kerala

- **"Holocene monsoon and sea-level variability from coastal lowlands of Kerala,
  SW India"**, *Quaternary International*.
  https://www.sciencedirect.com/science/article/abs/pii/S104061822200074X
  The regional relative sea-level curve. This is what the coastline prior needs.

- **"Evidence of Late Holocene shoreline progradation in the coast of Kerala"**,
  *Geomorphology* (2015).
  https://www.sciencedirect.com/science/article/abs/pii/S0169555X15002597
  Progradation rates. Reports beach-ridge formation along the whole Kerala coast
  between 3 and 5 ka, and a shoreline roughly 3 km inland of the present one at
  about 4 ka, which bounds how far the first-century coast can have moved.

---

## Component 2: The likelihood from textual evidence

### Rounding, heaping and coarse data

This is the right literature for the stadia, and it is better developed than
anything in classics.

- **Heitjan and Rubin, "Ignorability and Coarse Data"**, *Annals of Statistics*
  19 (1991).
  The foundational framework. Rounding, heaping, censoring and grouping are all
  treated as one thing, which is exactly how the Periplus figures should be
  modelled. Start here.

- **Allen et al., "Proximity and gravity: modeling heaped self-reports"**,
  *Statistics in Medicine* (2017).
  doi:10.1002/sim.7327
  A workable likelihood for values that gravitate toward preferred numbers. Our
  mantissas are 1, 2, 3, 4, 5, 6, 8, 12, 15 and 18, which is a gravity pattern.

- **"Heaping and seeping, GAITD regression"**, *Annals of Applied Statistics*
  19.4 (2025).
  doi:10.1214/25-AOAS2065
  The current state of the art for count data with excess mass at preferred
  values. More machinery than we need, but it shows what a referee will expect.

### Sequence models over latent positions

- **Shalizi, "Hidden Markov Models and State Estimation"**, lecture notes,
  Carnegie Mellon.
  https://www.stat.cmu.edu/~cshalizi/dst/18/lectures/24/lecture-24.html
  Clean statement of forward-backward and of why the exact posterior is
  available on a discrete state space. This is the algorithm the position model
  runs on.

- **"Bayesian inference for continuous-time hidden Markov models with an unknown
  number of states"**, arXiv:2106.10660.
  https://arxiv.org/pdf/2106.10660
  Read for how to put priors on the transition parameters while marginalising
  the states, which is the structure of our fit.

---

## Component 3: The likelihood from archaeological evidence

### Occupancy and imperfect detection

- **MacKenzie et al., "Estimating site occupancy rates when detection
  probabilities are less than one"**, *Ecology* 83 (2002).
  The origin of the method. Everything downstream cites it.

- **Guillera-Arroita et al., "Design of occupancy studies with imperfect
  detection"**, *Methods in Ecology and Evolution* (2010).
  https://besjournals.onlinelibrary.wiley.com/doi/full/10.1111/j.2041-210X.2010.00017.x
  How to allocate survey effort, which is the same question as our decision
  layer, in a field that has thought about it longer.

- **Lahoz-Monfort et al., "Ignoring imperfect detection in biological surveys is
  dangerous"**, *PLoS ONE* 9 (2014).
  https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0099571
  The argument, stated bluntly, for why unadjusted absence is misleading. Useful
  for the methods chapter, since this is the case our thesis has to make to
  classicists.

- **"Intrinsic Bayesian Analysis for Occupancy Models"**, arXiv:1508.07403.
  https://arxiv.org/pdf/1508.07403
  Prior choice for occupancy models, which matters when the number of sites is
  small, as ours is.

### Assemblage composition

- **Aitchison, *The Statistical Analysis of Compositional Data*** (1986), and
  **Baxter and Freestone, "Log-ratio compositional data analysis in
  archaeometry"**, *Archaeometry* 48 (2006).
  https://www.researchgate.net/publication/229780545
  Why sherd proportions cannot be regressed directly, and what to do instead.
  Baxter is the archaeological entry point.

- **"A Dirichlet Regression Model for Compositional Data with Zeros"**,
  arXiv:1410.5011.
  https://arxiv.org/pdf/1410.5011
  Our assemblages are full of zeros, and both Aitchison's transform and plain
  Dirichlet regression break on them. This is the fix.

- **CRAN Task View: Compositional Data Analysis**.
  https://cran.r-project.org/web/views/CompositionalData.html
  Implementation survey rather than reading.

---

## Component 4: The decision layer

- **Ryan, Drovandi, McGree and Pettitt, "A review of modern computational
  algorithms for Bayesian optimal design"**, *International Statistical Review*
  84 (2016).
  https://eprints.qut.edu.au/75000/1/75000.pdf
  The main review. Expected information gain, and how to compute it when the
  likelihood is expensive, which ours is.

- **Shewry and Wynn, "Maximum entropy sampling"**, *Journal of Applied
  Statistics* 14 (1987).
  The original statement that choosing where to observe is choosing where
  entropy falls fastest. Short and still the clearest framing.

- **Koopman, *Search and Screening*** (1946, reissued 1980).
  The naval search-theory origin of optimal allocation of search effort over a
  posterior. Worth reading for the framing even though the modern Bayesian
  design literature supersedes the mathematics.

---

## What to read first

Four papers would cover the framing of the whole thesis. Heitjan and Rubin for
the textual likelihood, MacKenzie for the archaeological one, Leidwanger for why
distance should be time, and the entropy-based sampling-bias paper for where the
archaeological modelling literature currently stands.

---

# Coastlines, deltas and voyages

The reading for Component 1, at more depth. These are the methods that build the
prior, and they are where most of the technical work will sit.

## Reconstructing coasts and deltas

1. **"Spatial analysis of Holocene delta compound clinoforms"**, *Communications
   Earth and Environment* (2024). https://www.nature.com/articles/s43247-024-01652-9
   Quantitative treatment of how deltas build seaward. The method for turning a
   progradation rate into a palaeo-shoreline position.

2. **Stouthamer and Berendsen, "Avulsion frequency, avulsion duration, and
   interavulsion period of Holocene channel belts in the Rhine-Meuse delta"**.
   The reference study for how often a delta channel jumps and how long the jump
   takes. Gives the base rates our Indus and Periyar reconstructions need, and a
   prior for how many channels were active at once.

3. **"Conceptual framework for assessing the response of delta channel networks
   to Holocene sea level rise"**, *Quaternary Science Reviews* (2009).
   https://www.sciencedirect.com/science/article/abs/pii/S0277379109000742
   Links sea-level forcing to channel behaviour. This is what connects the
   Kerala sea-level curve to the Vembanad channel network.

4. **"Large-scale coastal and fluvial models constrain the late Holocene
   evolution of the Ebro delta"**, *Earth Surface Dynamics* 5 (2017).
   https://esurf.copernicus.org/articles/5/585/2017/
   A worked example of reconstructing a specific delta's late Holocene shape
   from models plus cores. The closest template for doing the Indus.

5. **"Shoreline reconstruction since the Middle Holocene"**, *Quaternary
   Research* (2009).
   https://www.sciencedirect.com/science/article/abs/pii/S1040618209001918
   Method for drawing past shorelines from dated indicators rather than
   asserting them.

## Palaeochannels from satellite imagery

6. **Orengo and Petrie, "Large-scale, multi-temporal remote sensing of
   palaeo-river networks"**, *Remote Sensing* 9 (2017).
   https://www.mdpi.com/2072-4292/9/7/735
   The key paper. A seasonal multi-temporal method using long-term vegetation
   dynamics and spectral decomposition, which recovered more than 8,000 km of
   palaeo-channels in northwest India. This is the method for step 1 of the
   thesis, and it is written for exactly our region.

7. **"Reconstructing long-term settlement histories on complex alluvial
   floodplains"**, *Heritage Science* (2023).
   https://www.nature.com/articles/s40494-023-00985-6
   Joins the channel reconstruction to site distributions, which is the join
   we need between the coastline prior and the candidate sites.

8. **"Identification and Characterization of Palaeochannels"**, Springer (2025).
   https://link.springer.com/chapter/10.1007/978-3-031-92021-9_3
   Recent methods chapter. Multi-sensor fusion of SAR and optical data with
   moisture and vegetation indices, which is the practical recipe.

9. **"Potential of satellite based sensors for studying distribution of
   archaeological sites along palaeo channels"**, *Journal of Archaeological
   Science* (2010).
   https://www.sciencedirect.com/science/article/abs/pii/S0305440310002827
   Older and narrower, but it is the archaeological framing of the same method.

## Harbour geoarchaeology

10. **Marriner and Morhange, "Geoscience of ancient Mediterranean harbours"**,
    *Earth-Science Reviews* (2007), and their "Coastal and ancient harbour
    geoarchaeology".
    https://www.researchgate.net/publication/229990285
    The standard treatment of what a buried harbour basin looks like in a core.
    Defines the sedimentary signature our anchorability index is trying to
    predict.

11. **"Geoarchaeology confirms location of the ancient harbour basin of
    Ostia"**, *Journal of Archaeological Science* (2014).
    https://www.sciencedirect.com/science/article/abs/pii/S0305440313003087
    A port located by coring rather than by excavation. The closest precedent
    for what we would recommend in the decision layer.

12. **"The Development and Characteristics of Ancient Harbours: Applying the
    PADM Chart"**, PLoS ONE (2016).
    https://pmc.ncbi.nlm.nih.gov/articles/PMC5025247/
    The Palaeoenvironmental Age-Depth Model. A transferable framework for
    reading harbour sequences, and it is open access.

## Monte Carlo voyage simulation

13. **"Seafaring and navigation in the Nordic Bronze Age: the application of an
    ocean voyage tool and boat performance data"**, *PLoS ONE* (2025).
    https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0320791
    The methodological template. Combines predicted vessel performance with
    agent-based simulation, and compares open crossings against coastal routes,
    which is precisely the Malabar question about open sea versus backwaters.
    Open access.

14. **Palmer, "Windward sailing capabilities of ancient vessels"**, *IJNA*
    (2009).
    https://www.ancientportsantiques.com/wp-content/uploads/Documents/ETUDESarchivees/Navires/Documents/Palmer2009-WindwardSailing.pdf
    The polar performance data for square rig. This is the input the simulation
    needs and we do not otherwise have it.

15. **"Sailing the Simulated Seas: a new simulation for evaluating prehistoric
    seafaring"**.
    https://www.researchgate.net/publication/398199778
    Agent-based modelling for drift against directed voyaging, built on open
    data and freeware. Useful for implementation choices.

16. **"A multi-criteria simulation of European coastal shipping routes"**,
    *Humanities and Social Sciences Communications* (2024).
    https://www.nature.com/articles/s41599-024-02906-9
    Shows how to combine several costs, not just wind, into one route model.
    Open access.

---

# Finding lost ports by reconstructing the landscape

Case studies where a harbour was located, or its disappearance explained, by
reconstructing the coast and the river rather than by excavating for it. This is
the genre the thesis belongs to, and it is where the Component 1 argument comes
from.

## The framework to work from

1. **Giaime, Marriner and Morhange, "Evolution of ancient harbours in deltaic
   contexts: a geoarchaeological typology"**, *Earth-Science Reviews* 191
   (2019), 141-167. doi:10.1016/j.earscirev.2019.01.022
   The single most useful item on this list. It defines five harbour types on
   clastic coasts: fluvial harbours subject to floods and channel change,
   infilled estuarine, submerged estuarine, lagoonal harbours dominated by
   sediment input, and basins altered by dredging and breakwaters. Our seven
   ports sort cleanly into it. Muziris on the Periyar is a fluvial harbour
   affected by channel change, which is exactly the 1341 event. Nelkynda and
   Bakarē on the Vembanad are lagoonal. Barbarikon is estuarine on a delta that
   has since prograded. Using their typology gives the geographic prior a
   published structure instead of an improvised one.

2. **Marriner and Morhange, "Geoscience of ancient Mediterranean harbours"**,
   *Earth-Science Reviews* 80 (2007).
   The review that established the field. Read for what a buried harbour basin
   looks like in a core, which is the signature the anchorability index is
   trying to predict.

## Harbours located or explained by reconstruction

3. **"Holocene evolution of Portus Pisanus, the lost harbour of Pisa"**,
   *Scientific Reports* 8 (2018).
   https://www.nature.com/articles/s41598-018-29890-w
   Open access. A 10,500-year relative sea-level reconstruction and an
   8,000-year environmental reconstruction used to establish when the site
   became a sheltered embayment, and therefore when it could have been a
   harbour. This is the closest published example of the reasoning our prior
   performs, and it is the template to cite.

4. **Stanley et al., "Pelusium, an ancient port fortress on Egypt's Nile delta
   coast: its evolving environmental setting from foundation to demise"**,
   *Journal of Coastal Research* (2008).
   A port founded when tectonics gave it sea access and abandoned when
   progradation cut it off. The mechanism that probably ended Muziris, worked
   out in detail somewhere the evidence survives.

5. **"Palaeogeographic reconstruction of the Main Harbour of the ancient city"**,
   *Journal of Archaeological Science* (2023).
   https://www.sciencedirect.com/science/article/abs/pii/S0305440323001371
   Recent worked example of the method.

6. **"Geoarchaeology confirms location of the ancient harbour basin of Ostia"**,
   *Journal of Archaeological Science* (2014).
   https://www.sciencedirect.com/science/article/abs/pii/S0305440313003087
   A harbour located by coring rather than excavation. The precedent for what
   the decision layer should recommend at an untested Kerala candidate.

7. **"Geoarchaeology of Portus Mareoticus: ancient Alexandria's lake harbour"**,
   *Journal of Archaeological Science: Reports* (2017).
   A lagoonal harbour, which is the Vembanad case.

## The same problem, in South India

8. **Ramasamy et al., "Geoscientific perspectives of the submerged and lost
   harbours and ports: ancient port city Poompuhar, South India"** (2020).
   https://www.ancientportsantiques.com/wp-content/uploads/Documents/PLACES/IndOc-Gulf/Poompuhar-Ramasamy2020b.pdf
   A lost South Indian port sought through submerged delta reconstruction, with
   a harbour-like structure reported 25 km offshore on an older Cauvery delta.
   The nearest thing to our problem in our own subcontinent, and open access.

9. **"Tracing the Late Quaternary coastal evolution of Central Kerala"** (2024).
   https://www.sciencedirect.com/science/article/pii/S2666033424000352
   The regional coastal reconstruction for exactly the stretch that holds
   Muziris, Nelkynda and Bakarē. This is the paper the Malabar prior should be
   built on.

10. **"Roman metallurgy and early Anthropocene footprints in Kerala, South
    India"**, *Ambio* / Springer (2025).
    https://link.springer.com/article/10.1007/s44218-025-00115-8
    Lead levels at Pattanam falling in the medieval layers, read against the
    1341 flood. Independent dating evidence for the event that reorganised the
    Periyar, which the coastline reconstruction needs.

11. **Cherian et al., "Chronology of Pattanam: a multi-cultural port site on the
    Malabar coast"**.
    https://www.researchgate.net/publication/229061657
    The site's own dating, described as a palaeo-delta at the mouth of the
    north-flowing Periyar.

## Recovering the channels themselves

12. **Orengo and Petrie, "Large-scale, multi-temporal remote sensing of
    palaeo-river networks"**, *Remote Sensing* 9 (2017).
    https://www.mdpi.com/2072-4292/9/7/735
    Open access, and written for northwest India. Recovered more than 8,000 km
    of palaeochannels from seasonal vegetation dynamics and spectral
    decomposition. This is the method for the Indus delta, and the one to
    imitate rather than invent.

13. **"Reconstructing long-term settlement histories on complex alluvial
    floodplains"**, *Heritage Science* (2023).
    https://www.nature.com/articles/s40494-023-00985-6
    Joins reconstructed channels to the distribution of known sites, which is
    the join between our prior and our candidates.

14. **"Reconstruction of the lost Saraswati river course and its associated
    archaeological sites"** (2025).
    https://www.sciencedirect.com/science/article/abs/pii/S2352938525001120
    A river reconstructed from imagery and then used to explain a site
    distribution. The most ambitious version of the argument, and a useful
    warning about how far it can be pushed.

## What to read first

Giaime et al. for the framework, Portus Pisanus for the worked example, the
Central Kerala coastal evolution paper for our own region, and Orengo and Petrie
for the channel method. Three of those four are open access.
