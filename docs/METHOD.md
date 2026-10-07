# Reconstructing the ancient coast: four lines of evidence

Written for a reader coming to the project cold. The detailed record is in
`GEOGRAPHIC-FINDINGS.md`; this is the method.

---

## 1. Where was the coastline?

**The question.** The Indian coast has moved. Before anything else, we need to
know whether a candidate site was on the water at all in AD 50.

**The evidence.** Old sea charts, because they are the only record of this coast
before modern engineering: a Dutch chart of around 1700, British Admiralty
surveys of 1857, and satellite imagery from 1972 onward. Alongside them, the
land itself. A beach ridge is a fossil shoreline, a sand bank stranded as the
coast built seaward, and Kerala has two sets that geologists have already dated.

**Steps**
1. Pin each historic chart onto modern coordinates by matching features that
   still exist, recording how well the fit worked.
2. Trace the coastline from each chart and each satellite epoch.
3. Map the beach ridges from elevation data.
4. Attach published dates to each ridge set.
5. Assemble the results into a sequence of dated coastlines.

**Output.** A coastline for each date, drawn as a band rather than a line, since
an eighteenth-century chart is not accurate to the metre. Plus one hard
geological boundary: land seaward of the younger ridge set formed after the
mid-Holocene and did not exist in antiquity.

**Why it matters.** It eliminates candidates. A proposed port standing on ground
that formed after AD 50 is finished without any further argument.

**Statistics**
1. Combine scanning, pinning and tracing error into a single positional
   uncertainty for each coastline.
2. Represent each coastline as a band of that width.
3. Claim the coast has moved only where two bands fail to overlap.

---

## 2. How deep was the water, and could a ship get in?

**The question.** A harbour is useless if a loaded ship cannot enter it. This is
the test that genuinely separates the candidates.

**The evidence.** The historic charts carry depth soundings, individual
measurements written across the water; both the 1700 Dutch sheet and the 1857
Admiralty sheet have them. Sediment cores, columns of mud drilled from the
ground, whose layers can be radiocarbon dated to establish how fast the seabed
filled in. And a published sea-level curve for this coast.

**Steps**
1. Transcribe the soundings from each chart as located points.
2. Record each chart's depth reference, or flag it as unknown, since surveys of
   this period measured from different baselines.
3. Correct for tide, which is the largest single source of error in historic
   soundings.
4. Extract the stratigraphy and radiocarbon dates from each core.
5. Reconstruct how much sediment has accumulated at each location since
   antiquity.
6. Subtract that from where sea level stood to obtain the depth of water
   available at any date.

**Output.** For each candidate, at each date, the probability that a ship of a
given draught could enter. A Roman merchant vessel drew roughly two to four and
a half metres.

**Why it matters.** This is the strongest discriminator available. Pliny writes
that Bakarē was "a more useful port" than Muziris; this converts that sentence
into a testable claim.

**Statistics**
1. Interpolate the soundings by a method that returns its own uncertainty, so
   depth far from any measurement is correctly reported as less certain.
2. Fit an age-depth model to each core: a curve from depth to date that can only
   increase, with error bars.
3. Fit a sea-level curve that carries the dating error of each point through to
   the result.
4. Combine all three, propagating every uncertainty, into a posterior on water
   depth.
5. Report the probability that a given draught could enter at a given date.

---

## 3. Where did the rivers run?

**The question.** The Periplus gives the Indian distances "by river and by sea".
They cannot be measured until we know where the water was.

**The evidence.** Satellite imagery, because a buried river leaves a damp line
that crops grow differently over. And the historic charts, which drew the
waterways directly.

**Steps**
1. Assemble several years of satellite imagery for each region.
2. Separate the images by season, since the signal is a soil-moisture effect
   strongest in the dry months.
3. Extract the pattern that recurs across dates, which is the buried channel,
   from the noise that does not.
4. Validate against a channel already known to exist, with the pass mark fixed
   in advance.
5. Where that fails, trace the waterways from the historic charts instead.
6. Build a network of navigable water for each date.

**Output.** A map of navigable water per epoch, usable as a network to measure
routes through.

**The result so far.** It works in the arid Indus delta, scoring 0.81 against a
pass mark of 0.75 set beforehand. It fails in Kerala at 0.58 and 0.46, because
that landscape has been cut through with paddy bunds and canals that resemble
ancient rivers. Four separate methods have now failed there, so Kerala rests on
the charts.

**Why it matters.** It converts a stated distance into something measurable
along a real route rather than a straight line across land.

**Statistics**
1. Keep the detector's output as a probability for each pixel rather than a
   binary map.
2. Validate against a known channel, with the threshold fixed before running.
3. Measure routes through each epoch's network separately.
4. Treat the disagreement between epochs as the genuine uncertainty on the
   landscape.

---

## 4. How fast did ships actually sail?

**The question.** The Periplus measures in stadia, but ancient sailors estimated
sea distances from elapsed time. The unit is therefore a speed, and we need to
know what speed.

**The evidence.** Modern wind records, reliable here because the monsoon has
changed little in two thousand years. And the measured performance of
square-rigged vessels.

**Steps**
1. Assemble wind climatology for the basin.
2. Attach a performance curve for a square-rigged ship.
3. Simulate many voyages between ports whose locations are secure.
4. Record the distribution of elapsed times.
5. Compare it against the durations the text actually states.

**Output.** A conversion from "three days' sail" into a distance with a range
attached.

**Why it matters.** Every distance in the text currently rests on an assumed
conversion. This replaces the assumption with a measurement.

**Statistics**
1. Run the simulation repeatedly to obtain a distribution of travel times rather
   than a single figure.
2. Compare that distribution against the stated durations.
3. Optionally, estimate the ship's performance from those durations, which
   requires a method for fitting models that can be simulated but whose
   likelihood cannot be written down.

---

## How the four combine

Lines 1 and 2 establish where a port could have been and whether a ship could
reach it. Line 3 supplies the routes along which distances are measured. Line 4
fixes the units the ancient text is written in.

Together they yield a probability map of where each lost port stood, with every
source of uncertainty carried through rather than assumed away.
