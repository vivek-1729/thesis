# Sediment cores: what exists near each port, and where it comes from

An earlier note in this repository said we have essentially no core evidence for
any of the seven ports. That was wrong, and it was wrong because it searched our
own PDF library rather than the places core data actually lives. This file
records what a proper search found.

---

## 1. Where core data comes from

Three tiers, and most of what we need is in the third.

**Open repositories.** `PANGAEA` (pangaea.de), run by AWI and MARUM Bremen, is the
main archive for marine and palaeo datasets and holds the raw measurements from
European research cruises. NOAA's `NCEI Paleoclimatology` archive and its `Index
to Marine and Lacustrine Geological Samples` index physical core holdings
worldwide. `Neotoma` holds pollen and diatom records. `HOLSEA` holds standardised
Holocene sea-level index points. These are searchable and free.

**The institution that collected the core.** Where nothing is archived, the
cruise or the laboratory still holds it. For our regions that means MARUM Bremen
and R/V *Meteor* for the Tanzanian margin, Woods Hole and Giosan for the Indus
shelf, and for Kerala the National Centre for Earth Science Studies in
Thiruvananthapuram, the Agharkar Research Institute in Pune for the palynology,
the Physical Research Laboratory in Ahmedabad for the radiocarbon, and the
National Institute of Oceanography in Goa. The Geological Survey of India holds
borehole logs that are not open.

**Published in a paper and nowhere else.** This covers almost all the Indian
material. The core is described in the text, the dates are in a table, and there
is no archived dataset. Getting the data means reading the paper and typing it
out. Plan for that.

**What the search showed about the repositories.** Querying PANGAEA by region
returns real cores off Tanzania and nothing usable for Kerala, the Indus delta or
north-west Arabia. The absence in PANGAEA is not an absence of cores. It reflects
which research fleets archive their data there.

---

## 2. Kerala: Tyndis, Muziris, Nelkynda, Bakarē

**The best-served region, and the cores are close to the candidates.**

Five named borehole cores were taken through lower Kuttanad at **Nedumudi,
Alappuzha, Kaniyamkulam, Thakazhi and Kidangara**, to establish the stratigraphic
architecture of the region. That is the Nelkynda and Bakarē zone directly.
Thakazhi sits near Purakkad, Nedumudi is in the Vembanad, Kidangara is toward the
Pamba. These are onshore cores at our candidate locations, which is the situation
we want and did not have anywhere else.

Radiocarbon on the Holocene mud facies from Vembanad cores runs from 9700 ± 130
to 3220 ± 90 BP. Peat from the lagoon has been dated to around 40,000 BP.

Maya, K., D. Padmalal, M. Vandana, S. Vishnu Mohan, V. R. Vivek, Ruta B. Limaye, and K. P. N. Kumaran. "Holocene Changes in Fluvial Geomorphology, Depositional Environments, and Evolution of Coastal Wetlands: A Multiproxy Study from Southwest India." In *Holocene Climate Change and Environment*, 483–513. Elsevier, 2022. https://doi.org/10.1016/b978-0-323-90085-0.00026-7.

Maya, K., S. Vishnu Mohan, Ruta B. Limaye, Damodaran Padmalal, and Navnith K. P. Kumaran. "Geomorphic Response to Sea Level and Climate Changes during Late Quaternary in a Humid Tropical Coastline: Terrain Evolution Model from Southwest India." *PLOS ONE* 12, no. 5 (2017): e0176775. https://doi.org/10.1371/journal.pone.0176775.

Padmalal, D., K. P. N. Kumaran, K. M. Nair, B. Baijulal, Ruta B. Limaye, and S. Vishnu Mohan. "Evolution of the Coastal Wetland Systems of SW India during the Holocene: Evidence from Marine and Terrestrial Archives of Kollam Coast, Kerala." *Quaternary International* 237, no. 1–2 (2011): 123–39. https://doi.org/10.1016/j.quaint.2010.12.021.

Narayana, A. C., Vinu Prakash, P. K. Gautam, and Swati Tripathi. "Holocene Environmental Changes as Recorded in Sediments of a Paleodelta, Southwest Coast of India." *Quaternary International* 443 (2017): 115–23. https://doi.org/10.1016/j.quaint.2017.04.016.

Tiwari, Pooja, Biswajeet Thakur, Purnima Srivastava, Sanjay Kumar Singh Gahlaud, Ravi Bhusan, and Rajesh Agnihotri. "Paleolimnology and Natural Versus Anthropogenic Influx During the Late Holocene from Vembanad Wetland, Ramsar Site, Kerala, India." *Quaternary* 8, no. 1 (2025): 3. https://doi.org/10.3390/quat8010003.

Also relevant, already in `READING-GEOGRAPHIC.md`: Alappat et al. 2015 on OSL
dating of beach ridges, and Shaji et al. 2022 on the regional sea-level curve.

**Why Narayana et al. 2017 matters specifically.** A Holocene palaeodelta on the
southwest coast is the Muziris question in geological form. Read this one first.

---

### What we now hold

Maya et al. 2017 is open access and has been acquired. It is a larger dataset
than the abstract suggests: **17 boreholes, 8 to 26 m long, with 27 radiocarbon
dates across 15 sites**, plus lithology, grain size, heavy minerals and
palynology. Extracted to `data/raw/kerala_cores.csv`.

The transect runs through Thottapally, Haripad, Thakazhi, Ramapuram, Muthukulam,
Ayiramthengu and Pathiyur, which is the Nelkynda and Bakarē stretch.

**The record does not reach the Periplus.** Of 27 dates, 16 are Late Pleistocene
and 11 Holocene, and the three youngest are 2460 ± 120 BP at Ramapuram, 2580 ±
110 BP at Ayiramthengu and 2730 ± 30 BP at Vatta kayal. In calendar terms those
are roughly 510, 630 and 780 BC. **Nothing in this dataset dates within five
centuries of AD 50.** The Kerala core record therefore has a gap over the
Periplus horizon, in the same way the Indus shelf does, and the gap has to be
stated rather than interpolated across.

What the dates do establish is the Late Pleistocene to mid-Holocene framework:
when the lagoons formed, where the sea stood, and which surfaces are too young
to have existed in antiquity. That is a prior on the landscape, not a
measurement of it at the right date.

Still to acquire, all paywalled and all available through Harvard: Maya et al.
2022 for the five Kuttanad boreholes specifically, Narayana et al. 2017 on the
palaeodelta, Padmalal et al. 2011 on Kollam, Alappat et al. 2015 for the OSL
beach-ridge dates, and Shaji et al. 2022 for the sea-level curve. Tiwari et al.
2025 on Vembanad is open access but MDPI blocks automated download.

---

## 3. Indus delta: Barbarikon

**Offshore only, and the record has a hole exactly where we need it.**

Two shelf cores, **Indus-23** near the modern river mouth and **Indus-10** about
100 km west, spanning the early Holocene to the present. The critical finding is
a **hiatus at Indus-23 from 8 ka until 1.3 ka**, meaning non-deposition or
erosion. The Periplus falls inside that gap. Whatever the shelf record can do for
us, it cannot date the first-century shoreline at that location.

Limmer, David R., Philipp Böning, Liviu Giosan, Camilo Ponton, Cornelia M. Köhler, Matthew J. Cooper, Ali R. Tabrez, and Peter D. Clift. "Geochemical Record of Holocene to Recent Sedimentation on the Western Indus Continental Shelf, Arabian Sea." *Geochemistry, Geophysics, Geosystems* 13, no. 1 (2012). https://doi.org/10.1029/2011GC003845.

Giosan et al. 2012 in *PNAS* has onshore cores across the Indus plain, but they
were taken to address the Harappan period rather than the Roman one.

**No published core at or near Banbhore.** This is a genuine gap and it is worth
saying so in the thesis rather than working around it.

---

## 4. Rufiji delta: Rhapta

**Good offshore coverage, nothing onshore.**

Core **GeoB12624-1**, at 8°14.05′S 39°45.16′E in 655 m of water, 600 cm long,
recovered by R/V *Meteor* on cruise M75/2 in February 2008, sits directly
offshore the Rufiji mouth. Its Fe/Ca and Ti/Ca ratios track Rufiji discharge
directly, which makes it a continuous record of what the river was doing. The
datasets are open on PANGAEA: pollen and spore counts, XRF core scans, grain-size
distributions, and planktic oxygen isotopes. Nearby cores GeoB12615-4 and
GeoB12610-2 add isotope and Mg/Ca records.

Bouimetarhan, I., L. Dupont, H. Kuhlmann, J. Pätzold, M. Prange, E. Schefuß, and K. Zonneveld. "Northern Hemisphere Control of Deglacial Vegetation Changes in the Rufiji Uplands (Tanzania)." *Climate of the Past* 11 (2015): 751–64. https://doi.org/10.5194/cp-11-751-2015.

Liu, Xiting, Rebecca Rendle-Bühring, Inka Meyer, and Rüdiger Henrich. "Holocene Shelf Sedimentation Patterns off Equatorial East Africa Constrained by Climatic and Sea-Level Changes." *Sedimentary Geology* 331 (2016): 1–11. https://doi.org/10.1016/j.sedgeo.2015.10.009.

Pollen dataset: https://doi.org/10.1594/PANGAEA.835316

**What is missing** is any core in the delta itself. The offshore record tells us
about discharge and about shelf sedimentation, not about where the shoreline was
standing in the first century.

---

## 5. Leukē Kōmē

**Nothing at the site. A close analogue 250 km away, and a regional sea-level
curve with a tectonic warning attached.**

Five shallow cores, 1.1 to 2.2 m long, were taken from the intertidal flat
bordering the Dumaygh Lagoon and the mouths of wadis Antar and Haramil at north
Al-Wajh. Two stacked facies: grey lagoonal mud at the base, yellowish-brown
intertidal sand above. This is a wadi-mouth lagoon on the same coast, which is
exactly the Aynuna setting, and the core design is the one we would want
replicated at Aynuna.

Ghandour, Ibrahim M., Jawad Majeed, Aaid G. Al-Zubieri, Ammar A. Mannaa, Mohammed H. Aljahdali, and Rashad A. Bantan. "Late Holocene Red Sea Coastal Evolution: Evidence from Shallow Subsurface Sedimentary Facies, North Al-Wajh, Saudi Arabia." *Thalassas: An International Journal of Marine Sciences* 37, no. 1 (2020): 1–12. https://doi.org/10.1007/s41208-020-00248-2.

Weil, Noa, Mordechai Stein, Yonathan Shaked, Boaz Lazar, and Amotz Agnon. "Holocene Sea Levels at the Gulf of Aqaba, Northern Red Sea." *Quaternary Science Reviews* 277 (2022): 107278. https://doi.org/10.1016/j.quascirev.2021.107278.

Manaa, Ammar A., Brian G. Jones, Helen V. McGregor, Jian-xin Zhao, and David M. Price. "Dating Quaternary Raised Coral Terraces along the Saudi Arabian Red Sea Coast." *Marine Geology* 374 (2016): 59–72. https://doi.org/10.1016/j.margeo.2016.02.002.

**The warning.** The Aqaba curve puts sea level 1 to 2 m above modern between 6.8
and 5.5 ka, based on U–Th ages of corals from levelled fossil reefs. But the
Saudi coast north of Duba has been progressively uplifted by transform faulting
in the Gulf of Aqaba, reaching 16 to 20 m near Haql since 108 to 120 ka. Aynuna
is in that zone. A relative sea-level curve from there is not a eustatic curve,
and the tectonic component has to be separated before it can be used.

---

## 6. What this changes

The geographic plan's step 1 was written as "collect the published cores," on the
assumption that they exist. They do in Kerala and they largely do not elsewhere,
so the step splits:

- **Kerala.** Acquire the five papers, extract the core logs and every
  radiocarbon date into a table, and locate the five Kuttanad boreholes
  precisely. This is data entry, not new science, and it directly constrains
  Nelkynda and Bakarē.
- **Barbarikon.** Accept that the shelf record has a hiatus over the Periplus
  period and rely on the historic charts and channel reconstruction instead.
- **Rhapta.** Use GeoB12624 as a discharge record rather than a shoreline record,
  and be explicit about the difference.
- **Leukē Kōmē.** Use Al-Wajh as the facies model and the Aqaba curve as the
  datum, after subtracting the tectonic uplift, which nobody has done for Aynuna.
