# Evidence and data sources

Candidates for a given port sit 25 to 150 km apart. Anything that cannot resolve
at that scale is not worth the effort.

## 1. Geographic

The blocking stream. The Periplus gives the Malabar distances by river and by
sea, so nothing can be measured until the old channels are back on the map.

- **[FABDEM](https://doi.org/10.5523/bris.s5hqmjcdj8yo2ibzi9b4ew3sn).** Global 30 m elevation, with tree canopy and buildings stripped out. We use it to find dead river channels, which survive as troughs a metre or two deep.
- **[ICESat-2 ATL08](https://nsidc.org/data/atl08).** A satellite laser that reads ground height through gaps in the canopy. Used to check FABDEM where the vegetation is thick.
- **[CORONA](https://earthexplorer.usgs.gov/).** Declassified US spy photographs, 1960 to 1972. They show the ground before irrigation and road building wiped the channel traces out. Indexed for this region in the [CORONA Atlas](https://corona.cast.uark.edu/).
- **[ERA5](https://cds.climate.copernicus.eu/).** Hourly wind going back to 1940. Feeds the voyage simulation.
- **[GEBCO](https://www.gebco.net/).** Global seabed depth. Tells us where a ship could get in and anchor.
- **[HydroRIVERS](https://www.hydrosheds.org/products/hydrorivers).** Every river in the world as mapped lines. Gives the modern network to compare the old one against.
- **Historic charts.** Admiralty 750 and 751 from 1857, the manuscript originals in series ADM 352 at [The National Archives](https://discovery.nationalarchives.gov.uk/), and Survey of India sheets from 1911 to 1913. Paper maps, not a dataset, so they have to be scanned and georeferenced. They show the backwaters before the dams and the reclamation.
- **Kerala Holocene cores.** A handful of papers rather than a dataset, led by [Maya et al. 2022](https://doi.org/10.1016/b978-0-323-90085-0.00026-7). Boreholes through Kuttanad and the Vembanad lagoon. The only dated evidence of where water stood, and it is at the candidates.

## 2. Material

- **[Indian Archaeology: A Review](https://asi.nic.in/indian-archaeology-a-review/).** The Archaeological Survey of India's annual record of every excavation and survey in the country, 1953 to 2014. We use it to measure how hard anyone has looked at each candidate.
- **[Coin Hoards of the Roman Empire](https://chre.ashmus.ox.ac.uk/).** Findspots, contents and burial dates for Roman coin hoards worldwide. We use it for the distribution of Roman currency across the Indian interior.
- **Excavation campaigns.** Our own table, built from the site reports, recording seasons dug, depth reached and stated purpose for every candidate.
- **Quantified finds.** Our own table of pottery counts by type from the published site reports, classified against [Tomber's](https://www.ucl.ac.uk/) ware typology.

## 3. Textual

- **The ancient sources.** The [Periplus](https://depts.washington.edu/silkroad/texts/periplus/periplus.html) in Schoff and Casson, Ptolemy's *Geography* with McCrindle's commentary, [Pliny](https://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.02.0137%3Abook%3D6) book 6, the Muziris papyrus, the Tamil Sangam poems and the Peutinger Table. We extract the stated distances, the positional statements and the description of each port.
