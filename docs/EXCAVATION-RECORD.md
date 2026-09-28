# The archaeological record, extracted whole

## What was done

Previously we searched *Indian Archaeology: A Review* for candidate names.
That only finds sites somebody had already connected to a Periplus port, and a
site can be excavated without anyone making that connection. So the whole
state sections were lifted instead, from all 50 volumes we hold.

**7,053 numbered entries extracted**, each with year, state, chapter, title,
district, body and a period classification derived from its own text.
`data/processed/iar_entries.csv`; built by `src/extract_iar_entries.py`.

The question this lets us ask is regional rather than site-by-site: not "has
anyone dug at Ponnani" but **"what has been found on this coast, of what date,
since 1953."**

## Kerala, in full

308 entries fall in Kerala state blocks; 238 are confirmed by naming a Kerala
district; **75 of those sit in the fieldwork chapters** (Explorations and
Excavations, Other Important Discoveries) rather than in conservation,
epigraphy or chemistry.

Period profile of those 75 fieldwork entries. Entries can carry more than one
period, so the shares exceed 100 per cent.

| Period | Entries | Share |
|---|---|---|
| Megalithic / Iron Age | 47 | 63% |
| Medieval | 25 | 33% |
| Early medieval | 14 | 19% |
| Mesolithic | 7 | 9% |
| Palaeolithic | 7 | 9% |
| **Early Historic** | **4** | **5%** |
| Neolithic | 2 | 3% |
| Islamic / colonial | 2 | 3% |

**Four entries in sixty-one years mention material of Periplus date.** Here they
are, complete.

**1969–70, no. 18, Excavations at Cranganore, District Trichur.** The Southern
Circle with the Kerala Department under K.V. Soundara Rajan excavated at
Karuppadana, Kilattali, Mathilakam, Tirukkulasekharapuram and Tiruvanjikulam.
Everything recovered was ninth to eleventh century.

**1970–71, no. 24, Exploration in District Malappuram.** K. Chandrasekharan
found umbrella stones at Alancode, Koduvayur, Melmuri, Parnundam and Ozhur;
menhirs at Ananthavoor and Thirunavaya; urn burials at Alancode; and a
laterite rock-cut cave at Kuttippala yielding a red-slipped bowl painted with
Russet-coated ware.

**1970–71, no. 26, Exploration in District Trichur.** Records that the
Cranganore trial digs "had not yielded any tangible evidence," and reports the
discovery **in Taluk Ponnani** of Russet-coated (wavy line) Painted Ware,
"which overlaps with the megalithic Black-and-red Ware in the early centuries
of the Christian era," calling it "of great significance."

**2008–09, no. 29, Excavation and exploration at Pattanam, District
Ernakulam.** The KCHR excavation.

### What that distribution means

Two of the four are Russet-coated Painted Ware in the Ponnani and Malappuram
area, reported in consecutive entries of the same volume. One is a negative
result at Cranganore. One is Pattanam.

So in the complete national record for Kerala, **Early Historic material has
been reported from essentially two places: Pattanam, and the Ponnani–Malappuram
area.** That is a considerably stronger statement about Tyndis than any number
of individual absences at named villages, and it was invisible to a
name-matched search because the 1970–71 entries are filed under districts, not
under Ponnani as a site.

## Is Kerala simply under-investigated?

Not in the way I had assumed. Normalising fieldwork entries by state area:

| State | Fieldwork entries | Early Historic | EH share | Entries per 10,000 km² |
|---|---|---|---|---|
| Tamil Nadu | 595 | 83 | 14% | 45.7 |
| **Kerala** | **91** | **8** | **9%** | **23.4** |
| Andhra Pradesh | 381 | 23 | 6% | 23.4 |
| Karnataka | 345 | 87 | 25% | 18.0 |
| Gujarat | 305 | 69 | 23% | 15.6 |
| Maharashtra | 442 | 103 | 23% | 14.4 |

Kerala sits mid-range for intensity of investigation, above Gujarat and
Maharashtra per unit area. What is distinctive is the **yield**: an Early
Historic share of 9 per cent against 23 to 25 per cent for Maharashtra, Gujarat
and Karnataka.

So the honest formulation is not that Kerala has been neglected. It is that
Kerala has been investigated at an ordinary rate and has produced markedly
less Early Historic material than comparable states. Whether that reflects
preservation conditions, the laterite geology, the concentration of effort on
megalithic burials, or a genuine difference in first-century settlement, is a
real question and not one this extraction settles.

*(The 8 and 91 in this table come from state-block totals; the 4 and 75 above
come from the subset additionally verified by district name. The table is for
comparison between states, where the same method applies throughout.)*

## Three extraction bugs worth recording

The first pass produced 6,307 entries and I nearly reported from it. Three
faults, each of which changed the answer:

1. **State headings are typeset inconsistently.** "MADHYA   PRADESH" carries
   three internal spaces, so the boundary regex missed it and Madhya Pradesh
   districts were absorbed into the Kerala block. Six of eight apparent Kerala
   Early Historic entries were from Sagar, Vidisha, Chhatarpur, Dhar, Gwalior
   and Sehore.
2. **The born-digital volumes use a different layout.** Two columns, titles
   broken across lines, and a colon rather than an em-dash terminator. The
   Pattanam entry was invisible until this was handled.
3. **The first entry of every block was dropped** because the pattern required
   whitespace after the separator, and the older volumes run straight on
   ("DISTRICT TRICHUR.—The Southern Circle"). This silently removed the
   Cranganore excavation.

## What is missing, and what to do about it

*Indian Archaeology: A Review* has no counterpart for Arabia, Pakistan or East
Africa. For **Leukē Kōmē, Barbarikon and Rhapta** there is no annual series to
lift, so the equivalent has to be assembled by hand from the excavation reports
and from the expeditions named in the dossier passages: who dug, when, how many
seasons, what depth or period was reached, whether virgin soil was hit, and
where it was published.

The Banbhore case shows why the last two fields matter more than the finds
list. The decisive fact there is not what was recovered but that the trenches
stopped at the water table, which changes the meaning of everything above them.
