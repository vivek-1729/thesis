# New findings

Running record of results established since the consolidation. Everything here
is reproducible from the scripts named.

---

## 1. The Admiralty sheets georeference themselves, to about twenty metres

The charts had been held for months and never georeferenced, which blocked both
the coastline question and the depth question: a sounding read off a chart with
no transform is a number with no position.

**The method.** The usual approach is to match features on the old map against a
modern one and fit a transform through the pairs, which imports every error in
the matching. An Admiralty chart does not need it. The sheet carries a printed
latitude and longitude graticule, graduated to the minute, drawn by the people
who surveyed it. Reading that graticule gives a transform in the chart's own
stated coordinates.

Major latitude ticks are found automatically as the strongest marks inside the
left border. Longitude needs no separate scale, because these are Mercator
charts, where a minute of longitude is a constant number of pixels fixed by the
latitude scale through the secant of the mid latitude. It needs only an anchor,
which is one printed meridian read off the sheet.

**The result.** Two sheets done, `src/charts/sheets.py`.

| Sheet | Latitude residual | Check against the title | Covers |
|---|---|---|---|
| BA 749, sheet XI | 0.0068 arcmin, 13 m | bottom neatline within **75 m** | 75.49–76.29 E, 9.83–11.05 N |
| BA 750, sheet XII | 0.0121 arcmin, 22 m | top neatline within **349 m** | 75.98–76.77 E, 8.67–9.89 N |

The checks use quantities never entered into the fit: the opposite neatline
against the latitude range printed in the title. On sheet 749 two further
meridians, 75°35' and 75°45', were predicted at x = 1507 and 3005 against 1510
and 2990 read independently off the sheet, which is three and fifteen pixels.

**Coverage.** Between them the two sheets carry **fifteen of the seventeen
Malabar candidates**, including every Nelkynda and Bakarē candidate. The two
misses are Kadalundi and Koyilandy, both Tyndis candidates lying north of sheet
749's top edge at 11.05 N.

---

## 2. What the sheets say about themselves

Metadata that was not previously recorded anywhere in the project.

Both Malabar sheets are the work of **Lieutenant W. B. Selby of the Indian
Navy**, sheet XII surveyed 1850 to 1852 and sheet XI 1851 to 1853, both at
1:146,000. These are a single continuous survey by one hand, not a compilation,
which matters for the error structure: a systematic offset in Selby's work is
common to both sheets and cancels in any comparison between them.

**Sheet 750 carries inset harbour plans of Alleppey Road and Quilon Road**, at
larger scale than the main chart. Those are the approaches to a Bakarē
candidate and a Nelkynda candidate respectively, surveyed in detail.

---

## 3. The chart states its own tidal datum, which the project had recorded as unknown

Section 20 of the findings makes the vertical datum of a historic chart the
dominant error on any sounding read from it, larger than the tide and the
reading error combined, and treats it as unrecoverable. That is why the only
usable depth result so far is a contrast within a single sheet, where the datum
cancels.

Sheet 749 prints the reference in its title block:

> Cochin HW.F.&C. XIh26m, Springs rise 3 feet, Neaps rise 2¼ feet.

That is high water at full and change, with the spring and neap rise above
chart datum. A rise stated above datum is what fixes the datum.

**And it disagrees with our own measurement.** Three feet is 0.91 m. The spring
range fitted from modern Cochin gauge records is 0.58 m. The chart's neap figure
of 2¼ feet is 0.69 m against a fitted 0.26 m.

Both are larger on the chart, by factors of 1.6 and 2.6. Candidate explanations,
none yet tested: the chart datum is not the level our harmonic fit is referred
to; "rise" in 1857 usage may not mean what range means now; the gauge record is
astronomical only while the chart figure may include weather; or the tide has
genuinely changed. This is flagged and left, not resolved.

---

---

## 4. Georeferencing turns the charts into evidence for all four questions

Worth setting out, because the charts had been treated as background and they
are not.

**Q1, the coastline.** The 1857 shoreline is now locatable to about twenty
metres, which is 115 years before the earliest satellite epoch the project
holds. Sheets 749 and 750 cover the whole Malabar candidate zone, so the coastal
change rate over that interval is measurable rather than assumed.

**Q2, the depth.** Section 19 established that no measured bathymetry exists at
any of the seven approaches, leaving the charts carrying the depth question
alone. Georeferencing makes their soundings located points rather than numbers,
and sheet 749 prints the datum they are reduced to.

**Q3, the rivers, and this is the one that matters most.** Section 12 records
four independent methods failing in Kerala because the Kuttanad polder system
has re-cut the surface into features that mimic palaeochannels. **The 1857
survey predates the reclamation, the Thanneermukkom barrage and the Idukki dam.**
It draws the backwater network as it stood before the engineering that defeats
the satellites. Section 4.5 calls measuring the Malabar distances through the
backwaters the single most consequential unfinished measurement in the project.
The network to measure them through is printed on these sheets.

**Q4, the sailing.** The sheets carry anchorage symbols, magnetic variation, and
coastal profile views drawn as a ship saw them, including one captioned "Quilon
from the Anchorage". That is direct evidence of where ships lay and what they
steered by.

---

## 5. The approaches to two candidates, measured and contrasted

Sheets 749 and 750 are one survey by one hand, so a comparison between two
places on them carries no instrument difference. Two candidates, read off the
charts at their approaches.

**Purakkad, the Bakarē candidate, written Porakad with the Dutch name Porca.**
Soundings grade evenly offshore, 1, 1¼, 1½, 2, 2½, 3, 3½, 4, 4½, 5, 5½, 6 and
on to 12 fathoms. The bottom is marked soft mud. An anchor symbol marks the
anchorage. No reef, no breakers, no rocks and no foul ground are drawn anywhere
in the approach.

**Quilon, the Nelkynda candidate.** Deep water offshore, 10 to 23 fathoms, and
then an obstructed inshore approach. The chart marks **Tangacheri Reef**,
**Breakers** at four separate places, **"Rocks above water in patches"**, and
writes **"very foul ground"** across the approach. Inshore soundings fall
erratically to 1 and 1¼ fathoms among the hazards.

This is a measured contrast between a clean anchorage and an obstructed one, and
it is the kind of discriminator the method chapter calls the strongest
available. It is not a claim about antiquity, and the next paragraph is why.

**What carries back two thousand years, and what does not.** A sandbar is mobile
on a decadal scale and the project has already measured the Indus delta losing a
tenth of its water surface in forty years. A rock reef is not. Tangacheri Reef
is a geological feature and was there in AD 50; the soft mud at Purakkad may
not have been. So the chart's **hazard marks transfer back far better than its
soundings do**, and the two should be weighted differently when either is
carried into antiquity.

---

## Still open from this work

- Sheets 751, Indus 41 and 118, and Red Sea 8a to 8c.
- Kadalundi and Koyilandy need whichever sheet covers north of 11.05 N.
- Trace the 1857 backwater network and route the Malabar distances through it.
- The tidal discrepancy in section 3.
