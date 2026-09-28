# Statistical Plan

One statistical method per evidence stream, then an integration layer and a decision layer.

## Evidence streams

- **Textual distances**
  - *Approach:* Errors-in-variables regression with an interval-censored response.
  - *Details:* Stated stadia are rounded to the nearest 100, so the likelihood is the probability that the true distance divided by the stadion length falls inside the rounding interval. The stadion length is a parameter to be estimated, not a constant assumed in advance.
  - *Output:* A distance-consistency likelihood for each candidate location, and a posterior distribution for the stadion.

- **Archaeological record**
  - *Approach:* Occupancy model with imperfect detection.
  - *Details:* Detection probability is logistic in the number of excavation seasons, whether virgin soil was reached, and the decade of work. The detection model is fitted on the 7,053 extracted IAR entries and applied to the 23 candidate sites.
  - *Output:* A posterior probability that each candidate was an occupied port, with absence of evidence discounted in proportion to survey effort.

- **Coin hoards**
  - *Approach:* Log-Gaussian Cox process with thinning.
  - *Details:* Hoard intensity is modelled on distance to the coast, proximity to the Palghat gap, and elevation, then thinned by a modern discovery probability to correct for reporting bias.
  - *Output:* An intensity surface, and a test of whether hoard locations carry any locational signal at all.

- **Hydrology**
  - *Approach:* Supervised classification of relict channels.
  - *Details:* Multispectral satellite imagery classified against labelled palaeochannel training data; classification probabilities are retained rather than thresholded into a binary mask.
  - *Output:* A probabilistic covariate giving the chance that a navigable channel existed at a given location in antiquity.

- **Bathymetry**
  - *Approach:* Uncertainty propagation.
  - *Details:* Digital elevation model error and sea-level reconstruction error are pushed through to an anchorability index rather than treating depth as exactly known.
  - *Output:* An anchorability covariate carrying explicit error bars.

- **Wind and voyage**
  - *Approach:* Monte Carlo agent-based simulation.
  - *Details:* ERA5 wind climatology combined with a square-rig polar performance curve, run over thousands of simulated voyages.
  - *Output:* A reachability distribution, which replaces the conventional assumption of a fixed 500 stadia sailed per day.

## Integration layer

- **Approach:** Bayesian spatial logistic regression with a conditional autoregressive prior.
- **Details:** The covariates produced above enter as predictors, the occupancy layer supplies the observation model, and the whole is fitted by MCMC in Stan.
- **Output:** A posterior surface over coastal locations, and a posterior over identification sets that includes the possibility that the true site is none of the named candidates.

## Decision layer

- **Approach:** Bayesian optimal search allocation.
- **Details:** For each possible survey location, compute the expected reduction in posterior entropy that excavating there would produce.
- **Output:** A ranked list of where to excavate next, with expected information gain attached to each location.
