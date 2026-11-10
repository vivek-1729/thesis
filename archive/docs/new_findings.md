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

## 6. The backwater network will not come off the chart automatically

Section 4 above argued that the 1857 survey holds the pre-reclamation water
network, which is what the by-river-and-sea measurement needs. It does. Getting
it off the sheet is a different matter, and two approaches failed before the
reason became clear.

**Measured first, so the claim in section 4 is bounded.** Of the modern
backwater between 9.15 and 10.20 N, the two sheets cover **98.8 per cent**:
sheet 750 carries 84.9 and sheet 749 carries 17.7, overlapping. The gap is a
strip of the northern Vembanad east of sheet 749's edge at 76.294 E, between
9.887 and 10.199 N. So coverage is not the problem.

**The first attempt assumed the sheet tints land and leaves water blank**, and
separated them by local texture. It called 74 per cent of a tile water. The
sheet tints neither: land and sea are both blank paper and the coast is drawn
as a line.

**The second attempt assumed channels are ribbons** enclosed by two bank lines,
and looked for elongated blank regions. It found five regions in a tile, all of
them lettering and stipple, and no channels at all. The reason is scale. At
1:146,000 a backwater a hundred metres wide is under a millimetre on the paper,
so Selby drew the channels as **single lines, not as banks with water between
them**. They are linear features on this sheet, not areas.

**What would work.** Either curvilinear structure detection, separating thin
sinuous ink from the soundings, lettering, graticule, palm symbols and coastline
that share the sheet; or a hand trace of the main navigable route, which at this
scale is a few hours of work and would be more reliable than any of it. The
measurement needs connectivity and route length, not fine channel geometry, so
a traced centreline is sufficient.

**One practical trap, found the hard way.** The inset harbour plans of Alleppey
Road and Quilon Road are drawn in empty parts of sheet 750 and therefore sit on
top of geography they have nothing to do with. A tile pulled by coordinate
across one of them returns Quilon's breakers in the middle of the Kuttanad.
They must be masked by pixel box before anything is read by position.

---

## 7. Published palaeochannel maps: what exists, and none of it is a dataset

Searched for an existing map of buried channels that could stand in for the one
the charts will not yield: Zenodo, the ISRO Bhuvan geoportal, India-WRIS,
data.gov.in, and the publishers of the standard papers.

**No government or agency dataset exists.** Bhuvan advertises 14,491 layers over
its public map service, including 355 for Kerala. Searching every layer name and
title for palaeo, paleo, buried, relict, geomorphology, lineament and landform
returns **zero**. Its Kerala layers are modern thematic coverage: administration,
agriculture, built-up, canals, drainage, rail, road. India-WRIS and the
data.gov.in API did not respond at all.

**The maps that exist are figures inside papers, and two of them are the ones
already on the acquisition list.**

| Map | Region | Status |
|---|---|---|
| Narayana, Priju and Chakrabarti 2001, the Periyar palaeodelta, about 50 km² and up to 6 km wide | Muziris | **Open access**, blocked to scripts, one browser click |
| Priju et al. 2018, palaeochannels of the Periyar basin by electrical resistivity | Muziris | Paywalled, needs the proxy |
| Giosan et al. 2012, fluvial landscapes of the Harappan civilisation | Barbarikon | Publisher blocks scripts |
| Orengo and Petrie 2017, palaeo-river networks of the Sutlej and Ghaggar | adjacent to Barbarikon | Open access at MDPI, blocked to scripts |

Nothing was found for the Red Sea or the Tanzanian coast.

**So the answer is that the two palaeochannel maps this thesis most needs are
already on the list, one of them needing nothing but a browser.** There is no
shortcut dataset, and nobody has published the Kerala backwaters as a layer.

**One incidental find worth noting.** Bhuvan does publish canal line and polygon
layers per Kerala district, including Alappuzha, which is the modern navigable
network at district resolution. It is post-reclamation and therefore not what
section 6 wants, but it is a free vector network over the right ground and may
serve as the modern end of a comparison.

---

## 8. Three of the four maps are now held, from an archive no index covers

Section 7 said the four palaeochannel maps needed a browser or the proxy. Three
of them did not.

**Narayana, Priju and Chakrabarti 2001 is held.** It was never a browser-only
item. The Journal of the Geological Society of India runs an Open Journal
Systems instance with free PDFs back to the 1960s, and the paper downloads
directly from it. The reason the project had it marked otherwise is that the
publisher DOI resolves to a challenge page while the journal's own archive does
not, and no index had pointed at the archive: Unpaywall does not cover it and
the OpenAlex sweep in `src/query_geo_literature.py` never saw it.

That is the more useful finding. JGSI is where the Indian coastal-geomorphology
literature was published, which is to say most of the geomorphic evidence for
four of the seven ports. `src/harvest_jgsi.py` sweeps it on twenty-two queries
across Malabar and the Indus, filters on the title because the search is full
text and a query for Periyar returns the Annual General Meeting proceedings, and
deduplicates on the title because papers are often deposited twice under
different identifiers.

**Orengo and Petrie 2017 is held**, from the Cambridge repository rather than
from MDPI, which refuses scripted requests.

**Giosan et al. 2012 is not, and now has a definite reason.** It is in PubMed
Central as PMC3387054, but Europe PMC answers a request for the file with
`Article with id PMC3387054 is not open access one`. PNAS deposits under the
free-to-read-after-six-months arrangement rather than an open licence, so the
paper is free to a person in a browser and closed to anything else. That is a
one-click item and will not become anything else.

**Priju et al. 2018 is still paywalled, and there is a better target behind it.**
The author's institutional page at the Centre for Water Resources Development
and Management lists two funded projects behind the published chapter, one
funded by DST-SERB and one completed on 31 December 2022, titled *An integrated
study of Paleo-channel aquifers of Periyar river basin using hydrogeological,
geo-electrical and isotope methods*. Those carry final technical reports with
the sounding positions in them and none of it is published. The address is
`priju@cwrdm.org`, and an email is recorded in `docs/things-for-you.md` as the
highest-return action outstanding.

**A fourth paper turned up that was not being looked for.** Punwong, Selby and
Marchant 2018, in *Estuarine, Coastal and Shelf Science*, is the peer-reviewed
publication of the Tanzanian cores that `src/extract_punwong_cores.py` reads out
of Punwong's 2013 thesis. The accepted manuscript is open at White Rose. It
matters because it converts those dates into sea-level index points: it states
the indicative range for mangrove as -1.14 m to +0.57 m relative to mean tide
level, which the thesis does not, and it rejects two dates for reconstruction,
at 19 cm in core BNR and 115 cm in core CNR. Our extraction independently flags
the first of those as post-bomb, which is a check on the extraction passing.

---

## 9. The 2001 figure georeferences to about seventy metres

Figure 2 of Narayana, Priju and Chakrabarti is the only published map of the
palaeo-landscape at the Periyar mouth. It marks two palaeodeltas, at Munambam
and at Varapuzha, two yazoo belts, and a line labelled ANCIENT SHORELINE running
inland of the modern coast from near Krishnan Kotta through Parur and again
south of Edapalli past Chitrapuzha.

It georeferences for the same reason the Admiralty sheets do. It carries its own
graticule, labelled 76 degrees 10 to 25 minutes east along the top and 10
degrees 15 down to 9 degrees 55 north down the right. `src/charts/narayana_fig2.py`
fits an affine transform through eleven ticks.

**The result is 12.9 m per pixel, with an RMS residual of 5.2 pixels or 67 m and
a worst case of 117 m.** The figure is not better than that, and the reason is
visible in the ticks: the top and bottom borders disagree about where a given
meridian sits, by an amount that falls from 33 pixels at 76 degrees 15 to 16
pixels at 76 degrees 25. A rotation would give a constant offset and so would a
shear. A page curving into the binding of a scanned journal gives this.

**The fit was checked against five places the map names and the gazetteer
places independently**, at Munambam, Parur, Alwaye, Ernakulam and Kodungallur.
All five predicted positions land on their printed labels.

**The caveat is the one the paper states itself.** It assigns no age to the
ancient shoreline or to either palaeodelta, and closes by saying that efforts
are being made to date the geomorphic elements. Nothing on this figure is a
first-century coastline until something dates it. What the figure gives is a
mapped landform, at seventy metres, on the same ground as the candidates.

---

## 10. The date and core databases, asked directly

Everything dated the thesis holds came out of papers: seventeen Kerala boreholes
and twenty-seven Kerala core dates from Maya et al. 2017, and twenty-six
Tanzanian dates read out of Punwong's 2013 thesis. Nothing for the Red Sea and
nothing for the Indus. `src/query_dated_subsurface.py` asks the four open
databases what they hold at the six port boxes instead.

Getting an honest answer out of them took more care than querying them.
PANGAEA's public search accepts a bounding box alongside a text query and
silently drops the box, so a search for cores in the half-degree box at the
Periyar returns North Atlantic foraminifera. The NOAA archive accepts a box and
barely uses it: a tenth-of-a-degree box returns 450 studies and a two-degree box
475. Neotoma accepts a bare bounding-box array without complaint and matches
nothing, which only showed up because the US Midwest, its best-sampled region,
came back empty. XRONOS answers its own documented query API with null for every
country tried. Each needed a different route, and one intermediate check went
through a file on disk that a timed-out request failed to overwrite, so Kerala
briefly appeared to contain two lakes in Minnesota.

**What they hold, within fifty kilometres of a port.**

| Port | Records | Where from |
|---|---|---|
| Muziris | 2 | tree rings, inland |
| Nelkynda and Bakarē | 0 | |
| Tyndis | 1 | a marine core at 49 km |
| Barbarikon | 12 | 8 marine cores off the Indus, 3 meteorological series, 1 archaeological date |
| Leukē Kōmē | 32 | northern Red Sea cores, the GeoB series, and a coral |
| Rhapta | 13 | the Punwong cores, a Mafia coral, a pollen core at 17 km |

**And the number that matters. Of 828 records within two hundred kilometres of
any port, exactly one is both within fifty kilometres and spans AD 50**, and it
is a sea-surface-temperature reconstruction from a marine core 49 km off Tyndis,
which is not evidence about a harbour.

That is an independent confirmation rather than a new finding. `DATA.md` section
7 already records that no dated evidence within five centuries of AD 50 exists
on these coasts. It was asserted from the literature. Four databases, queried
over the ground itself, now say the same thing.

**Three things follow that are worth having.** The Punwong cores at the Rufiji
are dated at 392, 884, 1292, 4167, 4751 and 4931 BP, so the gap in them falls
across the Periplus period rather than the record stopping short of it.
Barbarikon and Leukē Kōmē, the two regions with no dated subsurface evidence in
the project at all, each turn out to have marine cores within fifty kilometres.
And all forty-eight NOAA records within fifty kilometres carry DOIs and need
nothing from anyone to download.

---

## 11. The Geological Society archive is a subscription, and holds the Malabar dating evidence

Section 8 reported that JGSI serves free PDFs. That was true of the paper it was
tested on and is not true generally. `src/harvest_jgsi.py` identified 74 papers
relevant to Malabar or the Indus and could download 5. The other 69 redirect to
a login carrying `payment.loginRequired.forArticle`. Both answers arrive as HTTP
200 and neither says so in the page, so the catalogue now classifies on the URL
the request lands on.

**Twenty-six of the sixty-nine are directly about dated coastline position**,
which is the quantity section 10 has just shown no database holds. Among them,
by title: *Quaternary Geology of Kerala: Evidence from Radiocarbon Dates*
(1989), *A Mid Holocene Strandline Deposit on the Inner Shelf of Cochin* (1992),
*On the Evolution of the Lagoon Barrier System* (1987), *Late Quaternary
Evolution of the Shelf Environment off North Kerala* (2007), and *Radiocarbon
Dates of Corals, Gastropods and Foraminifers from Saurashtra* (2002) for the
Indus side.

So the Malabar dating evidence is neither missing nor undiscovered. It is in one
journal, it is catalogued in `data/processed/jgsi_catalogue.csv` with a working
link for each paper, and it is behind a subscription the university has.

---

## Still open from this work

- Sheets 751, Indus 41 and 118, and Red Sea 8a to 8c.
- Kadalundi and Koyilandy need whichever sheet covers north of 11.05 N.
- Trace the 1857 backwater network, by hand or by curvilinear detection, and
  route the Malabar distances through it. See section 6.
- Mask the inset plan boxes on sheet 750 so coordinate lookups stop crossing them.
- The tidal discrepancy in section 3.
