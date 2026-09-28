# What I need you to pull — coins and the no-coin sites

Everything below was checked against Unpaywall. "Open" means I already have it or
can fetch it; the rest need Harvard access.

## Already fetched, no action needed

- **Smagur 2025, "Everyday transactions in transit: contextualizing coins in the
  ports of Berenike and Myos Hormos", *JRA*** — open access, downloaded.
  doi:10.1017/s1047759425100561
  This one filled the Myos Hormos gap on its own: 153 coins plus a lead token
  from the Chicago excavations of 1978–82, with a breakdown by reign, and the
  striking detail that the 1999–2003 Southampton excavations produced only 14
  coins identifiable enough to publish.

## Priority 1 — the arguments I am currently taking on trust

| Work | Why it matters | Link |
|---|---|---|
| **Datoo 1970, "Rhapta: the Location and Importance of East Africa's First Port", *Azania* 5, 65–75** | The origin of the Pangani–Rufiji bracket that every later Rhapta argument inherits. Confirmed **not** open access. | https://doi.org/10.1080/00672707009511528 |
| **Chami 1999, "Roman Beads from the Rufiji Delta, Tanzania: First Incontrovertible Archaeological Link with the Periplus", *Current Anthropology*** | 47 citations; the single most-cited archaeological claim for Rhapta at Rufiji, in a much stronger venue than the Chami papers I hold. | https://doi.org/10.1086/200009 |
| **Turner 1989, *Roman Coins from India*** | Appendix 1 catalogues every Roman coin find in India **including single and stray finds**. CHRE gives me hoards only; this is the one source that adds site finds and tests whether CHRE's Indian coverage is complete. | Routledge reissue 9780367605827 |
| **Gurukkal 2001, "In search of Muziris", *JRA*** | The sceptical case against the Muziris consensus. | https://doi.org/10.1017/s1047759400019978 |

## Priority 2 — second anchor assemblages

| Work | Why | Link |
|---|---|---|
| **Salles & Sedov (eds), *Qāni'. Le port antique du Hadramawt*, Brepols 2010** | Several hundred bronze coins from the Russian-Yemeni excavations. Would give a second bronze site-find assemblage to set beside Aynuna's 25. Print only. | https://www.brepols.net/products/IS-9782503991054-1 |
| **"The coinage of ancient Hadramawt: the pre-Islamic coins in the al-Mukallā Museum", *AAE* 1995** | The regional coinage behind both Qana and Sumhuram. | https://doi.org/10.1111/j.1600-0471.1995.tb00075.x |
| **"Three unpublished collections of South Arabian coins", *AAE* 2003** | Same. | https://doi.org/10.1034/j.1600-0471.2003.00006.x |
| **Shajan, Tomber, Selvakumar & Cherian 2004, "Locating the ancient port of Muziris", *JRA*** | I hold the PDF but not through a stable link; worth having properly. | https://doi.org/10.1017/s1047759400008278 |
| **Suresh 2004, *Symbols of Trade*** | Non-numismatic Roman objects in India, systematically collated. | ISBN 9788173045523, Manohar |

## Priority 3 — Banbhore: partly resolved, and I was wrong about the journal

I said *Pakistan Archaeology* was not online. It is. The Department of
Archaeology and Museums serves it at `doam.gov.pk`, and volume 33 (2018) is now
in `library/excavation-reports/`. Its lead article is Mohammad Rafique Mughal,
"The Scytho-Parthian Red Polished Ware (RPW) from the port city of Banbhore
(Barbarikon), southern Pakistan", which publishes pottery of the first century
BC to second century AD from the site's earliest levels and identifies Banbhore
with Barbarikon on that basis.

Still wanted: **F. A. Khan, *Banbhore: A Preliminary Report on the Recent
Archaeological Excavations at Banbhore*** (Department of Archaeology and
Museums, Government of Pakistan), the original report on the 1958-66
excavations, which describes the Scytho-Parthian coins. Other volumes of
*Pakistan Archaeology* should also be swept from the same site.

---

# Sites searched for coin publications, with the result

Crossref was queried for numismatic publications at every site CHRE does not
reach (`src/query_coin_literature.py`, 110 hits, 41 naming a relevant place).

**Nothing site-specific exists for:** Ras Hafun, Ptolemais Theron, Charax
Spasinou, Xiis, Chandraketugarh, Tamluk, Dwarka, Nagara, Madayipara, Pangani,
Dar es Salaam, Fukuchani. For these the searches returned only generic Roman
numismatic methodology — which is itself the answer: no one has published coins
from them.

**East Africa is the clearest case.** Every coin recorded at a Rhapta candidate
is **Islamic or later**:

- Unguja Ukuu — 8th-c. Muslim gold coins found in 1866, Period IIa silver, a
  Chinese Northern Song bronze (960–1126)
- Kilwa — sultanate coins, c. 1200–1400
- Mafia (Kisimani Mafia) — coins reported by Chittick, medieval

**One lead worth chasing.** Juma 2004 (p. 24) writes that Rhapta "may be
anywhere between the Rufiji delta area, where ancient trade goods including
Roman beads have been excavated and further north, where a number of fortuitous
discoveries of early Roman coins have been made so far." Early Roman coin finds
north of the Rufiji would be the first Roman numismatic evidence on the
Tanzanian coast. He gives no reference. **If you can get Chami 1999 that trail
probably starts there.**

## The bottom line on coins

`data/processed/site_find_coins.csv` now holds 30 records: Aynuna 25 excavated
coins, plus assemblage totals for Myos Hormos, Berenike and Sumhuram.

- **Aynuna** is the one disputed candidate with real excavated coins — 24 bronze
  to 1 silver, Aretas IV to Tiberius, 2nd c. BC to AD 40. Small change in
  everyday use at the Periplus horizon.
- **Pattanam** has the hoard evidence: PARUR's 1,000+ gold coins 3 km away.
- **Every other disputed candidate has nothing**, and for the East African ones
  there is nothing to find.
