# What data gathering is left

An audit of everything the project still needs to collect, what blocks each item,
and the order to do it in. Written against the inventory in `DATA.md`.

The shape of it: four evidence streams were declared, two were built. The
material stream is complete and the textual stream is complete. The geographic
stream is half built, with the satellite and chart work done and the
measured-environment work never started. The voyage stream has not been started
at all.

---

## A. Blocked on you, and nothing here can be done from the terminal

Unchanged from `NEEDS-FROM-YOU.md`. Listed for completeness, not re-argued.

| Item | Blocker |
|---|---|
| CORONA 1960s imagery | USGS EarthExplorer registration |
| Nine open-access PDFs | a browser; publishers block scripts |
| Eight paywalled papers | the Harvard proxy |
| Survey of India 58 B/C/G | the Map Collection |
| ADM 352 manuscript charts | the National Archives |
| Qatar Digital Library | blocks programmatic access |
| Naura in or out | your decision |

## B. Held in the library and never extracted

The library is larger than the tables drawn from it. These are reading and
tabulation jobs with no external dependency.

1. **The Aynuna coin catalogue.** 450 pages held, unread, and the coin list is
   the decisive evidence for Leukē Kōmē. A reported fourteen Nabataean coins
   with twelve of the first century or earlier. Highest single-item value on
   this page.
2. **Punwong's Rufiji and Zanzibar cores.** Radiocarbon dates, core altitudes
   relative to mean sea level, and sea-level index points with indicative
   ranges. The only dated geographic evidence Rhapta has.
3. **Four excavation reports.** Qana, Sumhuram, Ras Hafun and Myos Hormos, all
   held. These are the securely located ports, so they define what a confirmed
   Periplus port looks like and calibrate what counts as an absence elsewhere.

## C. Catalogued but not downloaded

4. **Gallica.** 915 sheets catalogued, 23 held. Downloading all of them is about
   five gigabytes and most of it would never be opened, so the right unit is the
   sheets whose titles name a place near a candidate.
5. **David Rumsey.** 49 sheets catalogued, none held. Small enough to take whole.

## D. Open datasets that were declared available and never gathered

This is the largest untouched block, and none of it needs an account.

6. **Bathymetry.** `DATA.md` lists GEBCO as available and unused. GMRT serves a
   higher-resolution grid over the same areas with no registration, which
   matters because the question is whether a ship could reach a candidate and
   GEBCO's half-kilometre cell is coarser than the approach channels.
7. **Tides.** Recorded as the largest error term on the chart soundings. The
   tide model needs registration, but observed hourly sea level does not: the
   University of Hawaii archive has long records at stations on these coasts,
   and a harmonic fit to them gives the range directly.
8. **Wind.** Evidence stream four, never started. ERA5 needs a key; the NCEP
   reanalysis does not, and runs from 1948. Enough to establish the monsoon
   climatology each Periplus leg was sailed in.

## E. Textual and gazetteer gaps

9. **Five candidates missing from the gazetteer**: Nakkada, Nirkunnam,
   Kannetri, Markari, Varakkai. Named in `CLAUDE.md` as immediate work. Naura is
   absent too, pending your decision.
10. **Tamil Sangam poems**, held at second hand only. Worth checking whether a
    public-domain translation can be taken directly.
11. **The Tabula Peutingeriana**, noted and never worked.

---

## Order

Value first, and cheap things that unblock other things before expensive ones.

1. The five missing candidates, because every geographic layer is sampled at
   candidate coordinates and the layers should be built once.
2. Bathymetry, tides and wind, which are the declared-but-missing stream.
3. The Aynuna coins and the Punwong cores.
4. The Rumsey sheets and the targeted Gallica subset.
5. The four excavation reports, which are long reading.
6. Sangam and the Tabula, which may turn out to be small.

---

## What happened when this was run

**Done, and recorded where the findings belong.**

| Item | Outcome |
|---|---|
| Five missing candidates | Added. Two without coordinates, which is the honest answer |
| Bathymetry | Gathered, and there is nothing under it. `GEOGRAPHIC-FINDINGS.md` §9 |
| Tides | Fitted from observation, no account needed. §10 |
| Aynuna coins | Extracted and checked against the author's totals. `FINDINGS.md` §11 |
| Rumsey sheets | 48 downloaded, 46 MB |
| Gallica selection | 132 sheets chosen from 915. **Download blocked** |

**The Gallica block, stated plainly.** The selection was run and then 132 IIIF
requests were fired in quick succession, and Cloudflare blocked the address.
Nothing was downloaded. Retrying would be both futile and a poor way to treat a
public archive, so it was stopped.

What survives is the more useful half. `data/processed/gallica_selection.csv`
lists the 132 sheets by ark, date, title and which port each bears on, filtered
from 915 by place name, so the acquisition is now a short browser job rather
than a search. `src/fetch_gallica_selection.py` will do it in one pass if the
block clears; it should be run with a real delay between sheets.

The filtering was worth doing on its own. Of 915 catalogued sheets, 132 name a
place near a candidate. The Malabar block is mostly Bombay, Goa, Surat and
Mahé, which are 400 to 1,000 km north of any port in this thesis, because the
harvest matched the word Malabar and the chartmakers' Malabar is longer than the
Periplus's. Two substring traps were caught on the way: the frigate *l'Aquilon*
contains "quilon" and pulled in three surveys of the Gulf of Ajaccio, and the
engraver Noel Cochin signed plates of sieges in Lorraine and Catalonia.

**The Rumsey catalogue is noisier than its count suggests.** All 48 sheets came
down, but the search that built the catalogue matched on loose text, so the haul
includes a red gurnard, a Baltic ice chart and a page on world religions. The
sheets are small and worth keeping; the count should not be quoted as 48 charts
of these coasts.

**Still to do from this page:** the Punwong cores, the four excavation reports,
Sangam and the Tabula. Wind was running when this was written.
