# Material evidence: table structure

Three tables, linked by `site_key`. The design exists to solve four problems that
have already caused errors in this project.

**Finds are heterogeneous.** Reports give sherd counts, weights, percentages,
minimum vessel counts, or just "abundant". These cannot be pooled, so the kind
of quantity is an explicit field rather than an assumption.

**A count is meaningless without its denominator.** Pattanam's 6,029 amphora
sherds mean one thing against 3.5 million local sherds and another against
50,000. Where the report gives a total, it is recorded.

**A count is meaningless without its scope.** The Pattanam torpedo-jar
contradiction, 3,098 against "about 398", is a scope problem: one figure is a
site total to 2011 and the other is something narrower. Scope is explicit.

**A count is meaningless without the effort behind it.** Wheeler's 116 amphora
sherds from Arikamedu and Pattanam's 6,029 may differ by trade or by field
method. Excavated area, depth and sieving live in a separate campaign table so
finds can be normalised.

---

## 1. `data/raw/excavation_campaigns.csv`

One row per campaign, not per site. Banbhore has Khan 1958–66 and the Italian
mission separately; Arikamedu has Wheeler 1945 and Begley 1989–92. Finds attach
to a campaign wherever the report allows it.

| column | meaning |
|---|---|
| `campaign_id` | `{site_key}_{first_year}`, the key finds join on |
| `site_key` | joins `data/raw/site_aliases.csv` for coordinates |
| `site_display` | name as normally printed |
| `port` | which disputed port this site is a candidate for, or `anchor` / `comparandum` |
| `investigators` | who dug |
| `institution` | sponsoring body |
| `year_from`, `year_to` | field years |
| `n_seasons` | seasons, as stated |
| `n_trenches` | trenches or squares, as stated |
| `area_excavated_m2` | excavated area |
| `max_depth_m` | deepest point reached |
| `volume_m3` | where computable or stated |
| `sieved` | `yes` / `no` / `partial` / `unstated` |
| `sieve_mesh_mm` | mesh, where stated |
| `reached_virgin_soil` | `yes` / `no` / `partly` / `unstated` |
| `reached_periplus_horizon` | `yes` / `no` / `contested` / `unknown` |
| `targeted_at_port` | `yes` / `no`: was this campaign undertaken **because** the site was already proposed as this Periplus port? The instrument that separates "nothing was found here" from "we only looked here because we already believed it" |
| `publication_status` | `full` / `interim` / `preliminary` / `none` |
| `source_file`, `page`, `quote` | provenance, verbatim |
| `note` | anything that qualifies the row |

## 2. `data/raw/material_finds.csv`

One row per quantified statement. Long format throughout: never a column per
ware, so new classes and new sites add rows and nothing else changes.

| column | meaning |
|---|---|
| `find_id` | sequential |
| `site_key`, `campaign_id` | `campaign_id` blank where the report does not separate campaigns |
| `ware_as_published` | the report's own words, verbatim, e.g. "Roman pottery", "Red Polished Ware" |
| `ware_id` | mapped onto `data/raw/ware_typology.csv`; blank if unmappable |
| `quantity_value` | the number |
| `quantity_type` | `count` / `percent` / `weight_g` / `mnv` / `eve` / `presence` |
| `quantity_unit` | `sherds` / `vessels` / `beads` / `coins` / `fragments` / `grams` / `percent` |
| `quantity_qualifier` | `exact` / `about` / `at_least` / `fewer_than` / `unquantified` |
| `scope` | `site_total` / `campaign_total` / `season` / `trench` / `context` / `phase` |
| `scope_detail` | which season, trench or phase |
| `denominator_value`, `denominator_type` | e.g. 3557118, `all_ceramics` |
| `period_as_published` | the report's own period label |
| `date_from`, `date_to` | numeric years, negative for BC |
| `periplus_horizon` | `yes` / `no` / `spans` / `unknown`, derived from the dates |
| `source_file`, `page`, `quote` | provenance, verbatim |
| `verified` | `y` only when a human has read the sentence |
| `confidence` | `high` / `medium` / `low` |
| `note` | conflicts recorded here, never silently reconciled |

## 3. `data/raw/ware_typology.csv` (existing, 43 classes)

Tomber's vocabulary. Carries `origin_region`, `date_from`, `date_to` and
`diagnostic_value`, so origin and date analysis is a join rather than a field
repeated on every find row.

---

## What this makes computable

Filtering to `quantity_type = count`, `quantity_unit = sherds`,
`scope = site_total` gives a comparable set across sites. Dividing by
`denominator_value` gives the import fraction, which is the quantity that says
how much material a real port actually yields, and therefore how much a trench
at an untested candidate should have been expected to produce. Joining
`ware_id` to the typology gives origin region, which separates Mediterranean
from Gulf traffic. Joining `campaign_id` to the campaign table normalises for
excavated volume and for sieving.


---

## Why `targeted_at_port` exists

Kodungallur was excavated in 1969–70 *because* it was the traditional Muziris,
and it returned nothing earlier than the ninth century. Banbhore was excavated
as Islamic Daybul and the Barbarikon identification came later. Those two
absences are not the same kind of evidence, and no amount of care about
excavated area will distinguish them.

Excavation effort is not independent of prior belief about location. If
detection is estimated separately and then fed into a location model, the
field's existing opinion enters the likelihood disguised as evidence. This
column is what lets the two be fitted jointly instead.

It has usable variation: of the twelve candidates that have been excavated at
all, six were targeted at the port and six were not.
