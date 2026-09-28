# Numismatic evidence: CHRE

## The source

**Coin Hoards of the Roman Empire** (Ashmolean Museum with the Oxford Roman
Economy Project) holds c. 19,000 hoards and over 7 million coins. Since 2019 it
covers hoards of Roman coins found *outside* the empire, which is what makes it
usable here.

Pulled for the Indian Ocean and Red Sea world (`src/fetch_chre.py`):

| | rows |
|---|---|
| `data/raw/chre/chre_hoards.csv` | **627 hoards**, 62 fields, with coordinates, coin counts and closing dates |
| `data/raw/chre/chre_coins.csv` | **10,780 individual coins**, 47 fields, with reign, mint, denomination, metal, weight |
| `data/processed/chre_hoard_distances.csv` | every South Asian hoard with its distance to the coast |

The export is not documented; the working call is
`/search/?ox_hs[hoardCountries][]=<id>&format=csv` for hoards and
`format=csv-coins` for specimens.

**A first absence worth recording.** CHRE has no country option for Tanzania,
Kenya, Somalia or Ethiopia. The East African coast cannot be queried at all, so
Rhapta gets nothing from this layer — and that is an absence in the database,
not a result about the ground.

## The finding: Indian coin hoards do not mark ports

| | hoards | coins | inland share of coins |
|---|---|---|---|
| **India** | 121 | 11,063 | **73%** |
| **Sri Lanka** | 67 | 220,901 | 15% |
| **Pakistan** | 3 | 112 | 100% |

*Inland = more than 25 km from the coast (Natural Earth 10m).*

In India, **98 of 121 hoards and 73% of all recorded coins lie more than 25 km
inland**, and the single largest concentration sits 100–200 km inland — 4,802
coins in 29 hoards, the Coimbatore district and the Palghat gap. The pattern
holds at the Periplus horizon itself: of the 40 hoards closing between AD 1 and
69, 76% of the coins are inland.

This is the quantified version of what Tomber and Suresh argue qualitatively.
Roman coins in India travelled inland to the pepper and beryl sources and were
hoarded there. **They track bullion movement and hoarding behaviour, not harbour
location**, so the coin layer cannot be used to find Tyndis, Nelkynda or Bakarē.

The Sri Lankan figures look like the opposite case but are a different
phenomenon: enormous late-Roman *bronze* hoards on the south coast (Beragama
70,000 coins, Godavaya 30,000, Tissamaharama 30,000), fourth to fifth century,
not Julio-Claudian gold. Aggregating the two would be a mistake.

## The Indian coins themselves

Of 985 specimens recorded at coin level from India:

- **Gold 790, silver 184.** Aurei 756, denarii 180. Base metal is almost absent,
  which is itself the well-known anomaly — Rome's small change did not travel.
- Reigns peak under **Claudius (134), Tiberius (116), Augustus (114), Nero (92)**
  — 456 Julio-Claudian specimens — with a second peak under **Hadrian (116) and
  Antoninus Pius (75)**.

## The exception, and it is the interesting one

Kerala's coastal hoards cluster in one place, and it is Pattanam.

| Hoard | Coins | km from coast | km from Pattanam | Closing date |
|---|---|---|---|---|
| **PARUR** (North Paravur) | **1,000+ gold** | 2.2 | **3.1** | see caveat |
| VALUVALLY | 263 aurei + imitations | 2.2 | 5.3 | AD 145 |
| IYYAL (Eyyal) | 83 aurei, denarii, punch-marked | 13.7 | 56 | AD 98 |
| KUMBALAM | 9 aurei | 2.3 | 29 | AD 177 |

These are the four hoards Tomber names around Pattanam, now with counts and
coordinates. Together they make the Periyar delta the densest coastal
concentration of Roman gold in Kerala, against nothing comparable near Ponnani,
Niranam, Kollam or Purakkad.

**Caveat on PARUR.** CHRE gives it a terminal year of AD 1 while its summary
reads "Over 1000 gold coins. Uncertain issuers." It is the only Indian hoard in
the database dated to AD 1, and an uncertain-issuer hoard cannot support a
closing date. The size, the findspot and the 1998 discovery are solid; the date
is not, and nothing here should lean on it.

**A data error found and corrected.** CHRE places KOTTAYAM 1847 (74 aurei) at
9.591 N, 76.522 E — Kottayam town in central Kerala, which happens to be a
candidate for Nelkynda. But the record's own `county` field says **Kannur**, and
its summary says the coins were found "on the slope of a hill by the sea."
Central Kottayam is ~35 km inland behind the Vembanad backwaters. The county and
summary agree with each other against the coordinates, so the coordinates are
wrong; this is the well-known Kottayam-in-north-Malabar hoard, roughly 260 km
away. Excluded from the distance analysis (`SUSPECT` in `src/analyse_chre.py`)
rather than silently trusted. Without this correction the Nelkynda candidate
would appear to have a 74-aureus hoard sitting on top of it.

## What this contributes

1. **A negative that is now measured.** The coin layer cannot locate the
   disputed Malabar ports, and the 73% inland figure is the demonstration rather
   than an assertion borrowed from the literature.
2. **A positive for Pattanam.** The Periyar delta has Kerala's densest coastal
   Roman gold, which corroborates the Muziris identification without depending
   on the ceramics.
3. **Nothing for Barbarikon or Rhapta.** All three Pakistani hoards are over
   200 km inland, and East Africa is not in the database.

## Still outstanding

**Turner 1989**, *Roman Coins from India*, Appendix 1 catalogues every Roman
coin find in India with findspots. CHRE covers hoards; Turner also covers stray
and single finds, which are the more sensitive indicator of low-level exchange
at a harbour. Comparing the two would test whether CHRE's Indian coverage is
complete. **Suresh 2004** would do the same for non-numismatic Roman objects.

---

# Coverage audit: do we have coins for every site?

No, and the gap is structural rather than a matter of searching harder.

## What CHRE reaches

Every one of the 65 sites was measured against the 627 hoards
(`src/analyse_chre.py` logic, applied per site).

| Site | Hoards within 25 km | Nearest |
|---|---|---|
| Pattanam | 2 | 3 km (PARUR) |
| Kottayam | 3 | see the georeferencing error above |
| Kodungallur | 2 | 9 km |
| Al-Wajh | 2 | 1 km |
| Berenike | 1 | 4 km |
| Arikamedu | 1 | 0 km |
| Ponnani, Kadalundi, Koyilandy, Niranam, Purakkad | 1 each | 10–25 km |
| **Myos Hormos** | 0 | 143 km |
| **Aynuna** | 0 | **207 km** |
| **Banbhore** | 0 | **406 km** |
| **Qana, Sumhuram, Ras Hafun** | 0 | 205–812 km |
| **All six Rhapta candidates** | 0 | **2,100–2,400 km** |

## The structural gap: hoards are not site finds

CHRE is a hoard database. A hoard is a deliberate deposit and can be buried
anywhere; a **site find** — a single coin lost in an occupation layer — shows
money being used where people actually lived. For locating a port the second is
the better evidence, and CHRE contains none of it.

This matters differently by region. For India it matters less than it looks:
Roman coins there occur overwhelmingly as hoards and only rarely in
excavations, so CHRE captures most of the record. Against roughly 170 recorded
finds over 130 sites in the literature, our 123 Indian hoards is decent
coverage.

For the Red Sea and Arabian anchors it matters a great deal, because those sites
have been excavated and their coins published as site finds that CHRE never
took in.

## Site finds recovered from the library

`data/processed/site_find_coins.csv`, built by `src/extract_aynuna_coins.py`.

**Aynuna — 25 excavated coins**, from Gawlikowski, Juchniewicz & al-Zahrani's
catalogue. CHRE has no hoard within 207 km, so without this the leading
Leukē Kōmē candidate has no numismatic record at all.

- **24 bronze, 1 silver.** Low-value coinage, which is the signature of money in
  everyday use rather than stored wealth.
- Attributed: Aretas IV (4), Obodas III (1), Tiberius (1), anonymous Nabataean
  (6), unattributed (13).
- Dated range **2nd century BC to AD 40** — squarely the Periplus horizon.

This is the opposite profile to the Indian material, which is 790 gold against
184 silver and almost no bronze. Aynuna looks like a working harbour where small
change circulated; the Indian hoards look like stored bullion.

Three more figures found in the library but not yet extracted:

- **Sumhuram**: about 600 coins from recent excavations and roughly 1,300 coin
  *blanks* from the first campaigns, which together support a mint at the site
  (Avanzini 2011). The blanks have never been described or analysed.
- **Berenike**: over 41% of identifiable excavated coins belong to one period
  band (Sidebotham 2011), alongside the 9% / 34% figures already recorded.
- **Myos Hormos**: "No foreign coins have turned up in excavations at Myos
  Hormos" (Sidebotham 2011) — a negative worth holding, since it bears on
  whether Indian traders were resident.

## What is still missing

1. **Turner 1989, Appendix 1** — the catalogue of Roman coin finds in India
   *including single and stray finds*. This is the one source that would test
   whether CHRE's Indian coverage is complete and add the site-find layer.
2. **Suresh 2004** — the same for non-numismatic Roman objects.
3. **Qana coin report.** Sedov records several hundred bronze coins from the
   Russian-Yemeni excavations; the detail is in the Salles & Sedov monograph,
   which we do not have. That would be a second bronze site-find assemblage to
   set beside Aynuna.
4. **Banbhore coins.** The site has 30 seasons of excavation and no hoard within
   406 km; whatever coins exist are in *Pakistan Archaeology* or the
   Italian-Pakistani reports.
5. **East Africa: nothing exists to find.** CHRE has no country option for
   Tanzania, Kenya, Somalia or Ethiopia. Rhapta cannot be approached through
   coins at all, and this is a fact about the archaeological record, not about
   the database.

**FLAME** (Princeton) was checked and set aside: it covers CE 325–750, which
begins nearly three centuries after the Periplus. It would only be useful for
the late antique tail — Berenike's fourth- and fifth-century coins, and Sri
Lanka's late bronze.

## A correction the port panels surfaced

Building `figures/port_leuke_kome.png` showed that al-Wajh does have two coin
findspots within a couple of kilometres — but each is **three late-Roman
nummi**: AL WAJH, three of Maximianus (AD 295–296), and BI'R QUNAIR, three of
Constantine I (AD 327–333). They sit two and a half centuries after the
Periplus and say nothing about a first-century harbour.

So the proximity is real and the relevance is not. Set against Aynuna's 25
excavated bronzes running from the 2nd century BC to AD 40, the numismatic
evidence does not balance between the two candidates — it favours Aynuna, and
the distance-to-nearest-hoard measure used in the coverage audit was the wrong
instrument for seeing that. Nearness is not the same as pertinence, and a
count of hoards within a radius will not distinguish them.
