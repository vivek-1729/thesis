# Acquisition list

What I found, what I can fetch myself, and what needs you.

## 1. Indian Archaeology: A Review — RESOLVED, held locally

> **Done.** 78 volumes covering 59 years (1953–54 to 2013–14) are now in
> `library/iar-text/`. No OCR was needed: the PDFs carry a clean English
> text layer even though archive.org's derived text is unusable.
> Findings in `docs/iar-findings.md`. The notes below are kept as the record
> of how it was sourced.

This is the source that decides whether the Kerala candidates were never
excavated or merely never excavated *in my library*. The full run is free.

**ASI, 2001–2014** (13 volumes, born-digital, good text). Pattern:
`https://asi.nic.in/admin/publications/ePublicationReportsDetails/download/{ID}`

| Volume | ID | Volume | ID |
|---|---|---|---|
| 2013–14 | 15 | 2006–07 | 22 |
| 2012–13 | 16 | 2005–06 | 113 |
| 2011–12 | 17 | 2004–05 | 116 |
| 2010–11 | 18 | 2003–04 | 115 |
| 2009–10 | 19 | 2002–03 | 112 |
| 2008–09 | 20 | 2001–02 | 114 |
| 2007–08 | 21 | | |

Index page: https://asi.nic.in/pages/Publications/indianArchaelogyReports
Verified working — 2007–08 returns a 54 MB PDF.

**archive.org, 1953–2001** (~46 volumes). Examples:
- 1953–54 https://archive.org/details/indian-archaeology-1953-54-a-review-1954
- 1969–70 https://archive.org/details/indianarchaeology196970areview_284_b
- 1985–86 https://archive.org/details/indianarchaeology198586areview_527_t
- 1993–94 https://archive.org/details/indian-archaeology-1993-94-a-review
- 2003–04 https://archive.org/details/tdl.49427-indian-archaeology-2003-2004-a-review

Full list retrievable from the archive.org search API; I have the 46 identifiers.

**The catch.** I downloaded the OCR text for all 46 and 44 are unusable: the
Digital Library of India scanned them with a Devanagari OCR model, so English
text came out as mojibake. A first pass appeared to show every Kerala candidate
absent from the entire series — that result was an artefact of the bad OCR and
I have discarded it.

The three volumes with clean text confirm the method works. In 1993–94, Kerala
has exactly two entries: a menhir in Kollam district and conservation work at
St Francis Church, Cochin. No port excavation.

**Fix, as it turned out:** no OCR at all. The bad text is only archive.org's
derived `_djvu.txt`; extracting from the PDF directly gives clean English.

## 2. Free, direct download — I can fetch these without you

- **Pattanam 5th season field report** (Cherian 2011)
  https://kchr.ac.in/images/img/ptm2011_field%20Report.pdf *(already held)*
- **KCHR Pattanam research archive**
  https://www.kchr.ac.in/archive/87/Pattanam-Archaeological-Research.html
- **Banbhore, Pakistani-Italian excavations** (Felici et al.)
  https://easaa.org/wp-content/uploads/2023/01/Felici-et-al-8.pdf *(already held)*
- **ATLAL 27 (2019)**, Saudi Journal of Archaeology
  https://dial.uclouvain.be/pr/boreal/en/object/boreal:181698/datastream/PDF_01/view
- **al-Wajh–al-ʿUla Survey, 2016 season** (Fiema et al., ATLAL 29, 2020, 81–112)
  https://www.academia.edu/38569594/ — directly relevant to Leukē Kōmē: this is
  the only systematic survey covering the al-Wajh candidate.
- **al-ʿUla–al-Wajh Survey, 2013 reconnaissance** (ATLAL 28, 109–119)
  https://www.academia.edu/43092469/
- **Turner, *Roman Coins from India*** — review with summary of contents
  https://www.academia.edu/79763793/
- **Turner, "Updating Roman Coins from India"** (Brepols, open PDF)
  https://www.brepolsonline.net/doi/pdf/10.1484/M.WSA-EB.5.145163?download=true

## 3. Needs you — paywalled or print-only

| Item | Why it matters | Where |
|---|---|---|
| **Datoo 1970, "Rhapta: the Location and Importance of East Africa's First Port", *Azania* 5, 65–75** | The origin of the Pangani–Rufiji bracket every later Rhapta argument inherits. I have been citing it secondhand. | https://www.tandfonline.com/doi/abs/10.1080/00672707009511528 — Harvard has Taylor & Francis |
| **Salles & Sedov (eds), *Qāni'. Le port antique du Hadramawt*, Brepols 2010** | The full Qana excavation, 553 pp. Would give a second quantified anchor assemblage beside Pattanam. | https://www.brepols.net/products/IS-9782503991054-1 — print; HOLLIS or ILL |
| **Sedov 1992, "New archaeological and epigraphical material from Qana", *AAE* 3** | Interim Qana report | https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1600-0471.1992.tb00033.x |
| **Turner 1989, *Roman Coins from India*** | Appendix 1 is a catalogue of every Roman coin find in India — the raw data for the coin layer, with findspots. | Routledge reissue 9780367605827; HOLLIS |
| **Suresh 2004, *Symbols of Trade*** | The systematic collation of Roman objects in India, incl. the distribution problem. | ISBN 9788173045523; Manohar. HOLLIS/ILL |
| **ATLAL back volumes 1–26** | Aynuna and the NW Arabian coast before the Saudi-Polish mission | No complete open archive found; NYU Manifold has a partial listing |
| **Pakistan Archaeology / Sindh Antiquities** | Banbhore pre-Islamic levels | Not found online; likely ILL only |

## 4. Not found online at all

- Kerala State Department of Archaeology excavation reports as a series. Only
  Pattanam is published accessibly. If reports exist for Kollam, Niranam or
  Purakkad they are not on the open web.
- A complete open ATLAL archive.

## Priority

1. ~~Re-OCR the IAR run~~ — done, and no OCR was needed.
2. Datoo 1970 — I should not keep citing the foundational Rhapta argument at second hand.
3. Turner 1989 appendix — the coin catalogue with findspots.
4. Qana monograph — the second anchor assemblage.
