# 9 · First corpus: the Ewoldt review

The first corpus is the set of hiPSC-CM studies cited by Ewoldt JK, DePalma SJ, et al., *Induced pluripotent stem cell-derived cardiomyocyte in vitro models: benchmarking progress and ongoing challenges*, *Nature Methods* 22, 24–40 (2025), doi:10.1038/s41592-024-02480-7. The review analyses 300 studies by how their models are made, matured and assessed. The field is `fields/hipsc_cm/`; the review is its cover (`cover.yaml`), shown on the explorer.

## What exists

**50 papers are recorded**, published 2014–2022, all passing all four gates (release `run-2026-11-12`):

- **2014–2016:** 2014_Yang, 2015_Guyette, 2015_Hinson, 2016_Han, 2016_Herron, 2016_Kerscher, 2016_Lind, 2016_Mannhardt, 2016_Masumoto, 2016_Ruan, 2016_Schwan.
- **2017–2018:** 2017_Correia, 2017_Mills, 2017_Richards, 2017_Shadrin, 2017_Tiburcy, 2018_Abilez, 2018_Gao, 2018_Leonard, 2018_Mosqueira, 2018_Ronaldson-Bouchard, 2018_Ulmer.
- **2019–2020:** 2019_Dwenger, 2019_Goldfracht, 2019_Kaiser, 2019_Yang, 2019_Zhao, 2020_Buikema, 2020_Feyen, 2020_Garbern, 2020_Giacomelli, 2020_Huang, 2020_Richards, 2020_Rupert-C, 2020_Saleem-U.
- **2021–2022:** 2021_Bliley, 2021_Knight, 2021_Silva, 2021_Tsan, 2021_Tsui, 2021_Zhang, 2021_deLange, 2022_Afzal, 2022_Ergir, 2022_Garay, 2022_Huebsch, 2022_Ronaldson-Bouchard, 2022_Shen, 2022_Strimaityte, 2022_Wickramasinghe.

| | `run-2026-11-12` |
| --- | --- |
| Evidence items | 7,704 |
| Stated claims | 2,641 |
| Values | 95,825 |
| Vocabulary | v69, 1,076 terms |
| Formula library | v33, 87 entries |
| Cross-paper comparisons | 35,798 |
| Measure × contrast strata with ≥ 2 papers | 42 |

**How papers are chosen.** Papers are drawn only from the studies the review cites. The first were the trial papers; since then each batch is ranked by code for what it would add to the release (citations, and the measures and contrasts the release's strata already share), so that papers meet; the ranking chooses what to read next and is not part of any record (`runs/<date>_candidates/`). Each batch is added as in [tab 7](07-building.md), *Adding papers unattended*.

## Fields for the review

The fields follow the review's own structure (its Figs. 1–4) and are declared in `fields/hipsc_cm/field.yaml`. *Adopted* fields take ids from a pinned ontology, with own terms allowed ([tab 3](03-vocabulary.md)). A field added in a later field set is *not yet read* in earlier records.

| Group | Fields | Kind |
| --- | --- | --- |
| Cell source | `cell_line` | adopted (Cellosaurus), set |
|  | `number_of_lines` | quantity |
| Differentiation | `differentiation_factors` | adopted (ChEBI), set |
|  | `hipsc_medium`, `hipsc_coating` | terms (sets) |
|  | `wnt_activation_days`, `wnt_inhibition_days`, `insulin_day`, `confluency` | quantity |
| Purification | `purification`, `purity_method` | terms (sets) |
|  | `purity` | quantity |
| Culture | `cm_medium`, `replating_coating` | terms (sets) |
|  | `supplements` | adopted (ChEBI), set |
|  | `seeding_density` (field set 3) | quantity |
|  | `dissociation_reagent` (field set 3) | terms (set) |
|  | `incubator_atmosphere` (field set 3) | quantity |
| Platform | `platform` (2D surfaces and 3D formats in one tree), `substrate` | terms (sets) |
|  | `cell_types`, `stromal_cell`, `endothelial_cell` | adopted (CL), sets |
|  | `composition` | quantity (fractions of cell types) |
|  | `cm_day_at_formation` | quantity (day of differentiation when cells were put into the platform) |
| Maturation | `maturation_strategy` | terms (set) |
| Assessment | computed per study from its items' measure terms and their `method` qualifier (not context fields: [tab 3](03-vocabulary.md), *Analysis method is not a context field*) | computed |
| Load and constructs | `mechanical_load`, `transgene` | terms (sets) |
| Donor | `donor_age` (states fetal … adult) | quantity |
|  | `species` (field set 2) | terms |
| Use | `treatment` | adopted (ChEBI), set |
|  | `genotype` | terms (set) |
|  | `disease_model` | adopted (MONDO), set |
| Measurement | `measure` | measure |
|  | `temperature`, `day_of_measurement`, `culture_calcium_mM`, `measurement_calcium_mM`; `time_point` (field set 2) | quantity |
|  | `pacing`, `preparation`; `measurement_medium` (field set 2) | terms (sets) |

`genotype` and `disease_model` are linked: a pair that differs only in them counts as one contrast. Field set 3 came from the field survey of 28 papers ([tab 3](03-vocabulary.md)). The review's yes/no maturation columns are not fields: they are computed from `maturation_strategy` terms at level 1.

**Flags go back to the records** and count as *flagged*, apart from *not stated*; flags per field are reported in each release as a finding about how the literature reports its methods.

## The curated table stays out

No agent may see the review's curated table or the archived validation study's vocabulary, which carries the table's spellings (including canaries such as "Sythemax" and "XAY939"). So the field vocabulary is built from the papers alone, never seeded from that vocabulary or the table; every synonym must be found in a source's text; and a test checks that no canary appears in `fields/`.

## Open items

- **The remaining cited studies:** most of the review's 300 are not yet recorded.
- **When to cut a review release:** decided from the plot of new terms per paper against paper order; no threshold is fixed in advance.
- **The refinement pass:** earlier papers on the refinement list re-mapped with the final vocabulary.
- **Analyses** on that release, computed from files, counts of studies with intervals, each opening to its anchors: what the field uses (share of studies per term, beside *not stated* and *flagged*); the same shares by publication year; what goes together and combinations no study has used; how comparable the literature is for each benchmark measure under its standing key; the review's Figs. 1–4 recomputed from anchored mappings beside its printed percentages, differences reported, not corrected; and reporting gaps per field.
