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

## Still open from this work

- Sheets 751, Indus 41 and 118, and Red Sea 8a to 8c. The automatic tick
  detector works on the Malabar portrait sheets and fails on the others, whose
  borders are drawn differently.
- Kadalundi and Koyilandy need whichever sheet covers north of 11.05 N.
- The tidal discrepancy above.
