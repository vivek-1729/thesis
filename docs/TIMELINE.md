# Timeline

Locating six disputed ports of the *Periplus Maris Erythraei*, plus Muziris, by
combining classes of evidence that have not previously been brought together.

A joint thesis. The classical contribution is the assembly and assessment of the
evidence; the statistical contribution is a framework for inferring an unknown
location from heterogeneous, noisy sources where the missingness is itself
informative.

---

## Phase 1 — Evidence gathering  ⬅ current

- [x] **Establish the scope.** Fix which ports are genuinely disputed and which
      locations have been proposed for each
- [x] **Assemble the bibliography.** Survey the modern literature and build a
      working library of the primary reports
- [x] **Compile the textual evidence.** The distances and descriptions given by
      the Periplus, and the corroborating ancient sources
- [x] **Compile the material evidence.** The excavation record, the numismatic
      record, and the ceramic assemblages
- [ ] **Compile the geographic evidence.** Ancient river courses, coastlines and
      harbour conditions at each candidate
- [ ] **Obtain the outstanding sources.** The small number of works on which the
      standing arguments rest
- [ ] **Assess each class of evidence.** What it can determine, at what spatial
      resolution, and where it fails

## Phase 2 — Analysis and writing

The statistical method for each evidence stream is set out in
`STATISTICAL-PLAN.md`.

- [ ] **Model the Periplus as a measuring instrument.** The stated distances are
      rounded, and the distances they are compared against depend on
      identifications that are themselves uncertain. An errors-in-variables
      model with interval-censored measurements estimates the stadion with
      honest uncertainty, and tests the rounding structure rather than assuming it
- [ ] **Model detection in the archaeological record.** Absence of material is
      mostly absence of excavation. Treat site status as latent and detection as
      a function of survey effort and of whether excavation reached undisturbed
      ground, both of which are now measurable
- [ ] **Infer locations jointly.** The ports are linked by distances and form a
      chain rather than a set of independent problems. Combine the distance and
      detection models to obtain a posterior over location for each port
- [ ] **Compare competing identifications formally.** Assess whether any single
      set of proposed locations is consistent with the distances the text gives
- [ ] **Determine what would settle it.** Given the posterior, identify the
      single piece of fieldwork that would most reduce the remaining uncertainty
- [ ] **Methods.** The evidence available, its resolution, and its limits
- [ ] **A chapter for each port.** Scholarship, evidence, and assessment
- [ ] **Figures.** Final cartography and analytical graphics
- [ ] **Conclusion.** What can be established, and what would settle the rest

## Phase 3 — Revisions

- [ ] **Incorporate supervisory comments**
- [ ] **Verify citations and apparatus**
- [ ] **Consistency pass** across argument, figures and terminology
- [ ] **Final read**

---

**Dependency worth keeping visible.** The Periplus gives the Malabar distances
"by river and sea," so they cannot be measured correctly until the historic
channels are reconstructed. The geographic step in Phase 1 therefore blocks the
distance model in Phase 2.

**A note on scope.** Only a few classes of evidence resolve at the scale the
question demands. The candidates for a given port sit within 25 to 150 km of one
another, and most of the field's standard methods — graffiti, ship timbers,
documentary sources, radiocarbon — establish that trade occurred in a region
without distinguishing one village from its neighbour. Effort should follow
resolution.
