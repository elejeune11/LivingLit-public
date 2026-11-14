# 8 · Trials and decisions

This tab is the project's dated log. The other tabs describe LivingLit as it is; this one records how it got there: what each trial and run taught, and each decision with its date and who settled it. Entries are never deleted. When a later entry changes an earlier one, the later entry says so and the earlier one points to it. Reports are in `trials/` and `runs/`.

## Trials and runs

### Trials (before 2026-11-06)

Four trials on three hiPSC-CM papers (Tsan et al. 2021, Ronaldson-Bouchard et al. 2018, Zhang et al. 2021), one reader and scratch code; then a validation pilot of 30 studies against the Ewoldt table.

| Lesson | Decision |
| --- | --- |
| Every paper had real problems (consistent checks: 116/153, 63/80, 16/18). | The audit is the product ([tab 2](02-audit.md)). |
| Most problems were overstated claims, not wrong results. | Judge each stated claim by dimension against its own evidence ([tab 2](02-audit.md)). |
| Depth depended on released data; reading figures restored most of it (vector ≤ 0.5 pt, exact counts). | Read figures with readers' code, origins and calibrated uncertainty ([tab 2](02-audit.md)). |
| Reading Zhang's figures found 19 and 14 points where the legend says 25 and 22. | Points-to-P, n-from-error-bar and group-label checks ([tab 2](02-audit.md)). |
| Value comparisons all failed on context; the same thing was written in different words. | A controlled vocabulary; standing keys; *not comparable* named; direction comparisons first-class (tabs [3](03-vocabulary.md), [5](05-across-sources.md)). |
| A question written first biased extraction. | Fixed extraction rules; no questions inside LivingLit ([tab 2](02-audit.md)). |
| Composing shared claims was the hardest judgement; 15 of 20 claims had one source. | Dropped: claims are judged within their source only (next section). |
| 3 of 37 statuses typed by a reader broke the rules. | Statuses, counts and comparisons computed by code ([tab 7](07-building.md)). |
| Validation pilot: readers agreed with the table on 55 % of categorical cells but 100 % of yes/no flag cells. | Closed vocabularies, mapped once and checked, not free text compared at query time ([tab 3](03-vocabulary.md)). |
| Some groups sum both posts' deflections, doubling force (Ewoldt et al. 2025). | Derivations checked against a formula library ([tab 4](04-formulas.md)). |

### Why the discourse graph was dropped (2026-11-06)

The v4 design joined papers through LLM-written links (*same*, *narrower*, *opposes*, *supports*) and computed claim families from them. It is archived in `docs/archive/v4_discourse_graph/`. Three reasons:

1. **The weakest judgement sat at the centre.** Deciding that two papers' claims are the same assertion, at the same scope, was the hardest judgement in the trials, and every family, question and summary rested on it.
2. **The literature pointed the same way.** Recent evaluations found LLMs near expert accuracy at extracting single values but unreliable at combining evidence across studies (pooled estimates rarely reproduced), and deep-research agents' statements often unsupported by their own cited sources. Extraction is where agents are trustworthy; synthesis is where they are not.
3. **A claim is not a generalization.** A statement never becomes a general claim by being repeated; generalizing is a deliberate step, made by whoever uses the evidence, with its premises stated.

What replaced it: edges only through matched terms, comparisons computed under standing keys, and synthesis outside, on a release.

### First build: 10 papers (2026-11-07)

| Lesson | Decision |
| --- | --- |
| 10 papers (Mannhardt 2016, Ruan 2016, Mills 2017, Ulmer 2018, Ronaldson-Bouchard 2018, Saleem-U 2020, Tsan 2021, Zhang 2021, Bliley 2021, Shen 2022) became 331 units, 1,238 items, 426 claims and 35,804 values; every gate passed. | The pipeline worked end to end; the rules in tabs 2–7 were the ones that worked. |
| An independent check found 15/15 items printed correctly, 7/7 readings and 17,748 data cells correct; 6 of 10 sampled inconsistent items were real problems in the papers (n swapped between arms, fewer points than n, legend against data file). | Keep the independent check as a job ([tab 7](07-building.md)). |
| 4 of 10 inconsistent items were artefacts of the checks; direction verdicts parsed from words were mostly wrong. | Test-kind, unit and direction rules (tabs [2](02-audit.md), [5](05-across-sources.md)). |
| No value comparison and 49 direction comparisons out of 9,042 pairs; *derivation* and *method* blocked most. | Looser keys, measure qualifiers in keys, keys revisited at checkpoints ([tab 5](05-across-sources.md)). |
| 324 *several conditions* flags, mostly unit values naming both arms. | Groups, with contrasts computed by code ([tab 2](02-audit.md); decision 15). |
| Code matched 2 % of stated values. | Short stated values; details in qualifiers ([tab 3](03-vocabulary.md)). |
| Raster-only papers (Mannhardt, Mills, Saleem-U) stayed mostly *cannot check*. | Source data first; ask for it; the completeness list. |
| Item statuses: 334 consistent, 20 within reading, 16 close, 142 inconsistent, 726 cannot check. Claims: 175 overstated, 104 cannot judge, 56 does not follow, 41 follows. | — |
| The formula library had no statistical entries: statistics were hard-coded in the checks, and agents only propose what a paper derives. | Statistical entries written once by the build in a shared library; every check cites its entry ([tab 4](04-formulas.md)). |

### Rebuild: 10 papers (2026-11-07)

| Lesson | Decision |
| --- | --- |
| Groups made contrasts computable: 571 single-field contrasts, 48 factorial units; native tissue as a benchmark removed 44 of Ronaldson-Bouchard's 47 confounds. | Groups with kinds, linked and aliased fields ([tab 2](02-audit.md)). |
| Code matched 30 % of distinct stated values (first build 2.8 %). | Short values, synonyms, named states ([tab 3](03-vocabulary.md)). |
| An independent check found 15/15 items, 7/7 readings, 200/200 cells and 10/10 mappings right, and four code artefacts (value tolerance, post-hoc family, claim flags, suspect replicates). | Fixed test-first; the check stays a job after every build. |
| Unknown context blocked almost every cross-paper pair; requiring genotype left 2 value verdicts. | Open-world matching: conditional verdicts that name their assumptions (decision 28). |
| Post-hoc checks reproduced printed P but opened only ~20 items: families lacked points. | Source-data requests; unequal-variance alternatives (decision 31). |
| Two raster-only papers without data held half of the 971 *cannot check* items. | `source_data_requests.csv` leads each release. |

### Prototype: 4 force papers on field set 3 (2026-11-09)

| Lesson | Decision |
| --- | --- |
| All 4 records (Masumoto 2016, Leonard 2018, Tiburcy 2017, Shadrin 2017) passed all 16 gates, context anchors included, almost all on a first attempt; the runner held through a usage-limit interruption. | Keep the scripted runner and per-job gates ([tab 7](07-building.md)). |
| Only 13 % of the new items could be checked (predicted 30–45 %): most rest on ANOVA with Tukey post-hoc tests, which the checks verify only from points. | Source-data requests before reading (decision 46). Proposed, still open: pick papers for data by opening their files. |
| 75 figure jobs cost $83 of $147 and brought 6 items to readings depth; figures were chosen by missing values, not by whether a check could use them. | Figures read only for points a check can use (decision 49 as narrowed on 2026-11-10). |
| Twitch force was measured in all 14 papers, yet only 2 direction strata held items from two or more papers with nothing assumed. | The dataset before the verdicts (decision 45). |
| The first survey rule (stated in 3 of 29) made 47 fields; the narrowed rule made 3. | Decision 47 as revised ([tab 3](03-vocabulary.md)). |

### Add runs: 15 → 35 papers (2026-11-10 to 2026-11-12)

| Lesson | Decision |
| --- | --- |
| The first unattended `livinglit add` read one paper (2019_Zhao) with every gate passing on the first attempt; 16 of its 18 figure jobs found bars only. | The first look (decision 51). |
| The second batch added all 20 papers, none parked, with four stops at usage limits; about $404 in all (median $15.69 a paper). Strata with two or more papers went from 9 to 22. The first look ruled out 149 of 256 figure units for $0.97. | Keep `add` and the first look (decision 53). |
| Five older records failed their terms gate: later synonyms made a stored mapping redundant. | Re-gated; a standing fix is proposed (Open). |

### Add run: 35 → 50 papers (2026-11-12 to 2026-11-13)

| Lesson | Decision |
| --- | --- |
| All 15 papers, chosen for the meeting points they would add, passed all four gates, none parked; about $300 (median $11.87 a paper). Strata with two or more papers went from 22 to 42. | Pick papers by the strata they would join (decision 54). |
| 89 of 175 looked-at figures (51 %) were ruled out for $0.67; no looked-off unit was later found to need points. | Keep the first look; a sample audit is still proposed (Open). |
| Most of Garay's 164 inconsistent findings and all but one of deLange's 67 were artefacts of the checks; nine older records again failed their terms gate; two figure jobs passed their gate without reading anything; agents again wrote renders and extracted text to `/tmp`. | Re-gated and reread; the fixes are open proposals (Open). |

and who settled it. Numbers are stable; tabs cite them.

**Vocabulary**

1. **Identifier style.** Settled by Emma, by 2026-11-07. Readable ids (`field:slug`), not opaque ones (`PF-202`). An id never changes once made: a renamed term keeps its old slug, and its new label is what people see.
2. **Depth.** Settled by Emma, by 2026-11-07. Trees deepen only as distinctions that matter arrive.
3. **Source-level fields** (article type, study aim). Settled by Emma, by 2026-11-07. Left out: not the point of LivingLit.
4. **External ontologies.** Settled by Emma, by 2026-11-07. Standard ontologies are adopted wherever they cover a field (Cellosaurus, CL, ChEBI, MONDO, UO); own terms only where they are thin; every term shows its source ([tab 3](03-vocabulary.md)). Releases pinned by decision 18.
5. **When to re-map refinements.** Settled by Emma, by 2026-11-07. Every 10 papers, and once more before a release.
6. **Checkpoint size** for re-map agreement. Settled by Emma, 2026-11-07. Every 30 papers, as proposed; the key revision was also run after the first 10.

**Formulas**

*The library's name and kinds (unnumbered).* Settled by Emma, 2026-11-06. It is the formula library, with four kinds of entry (definition, model, bound, derived), because "law" overclaimed what most entries are.

7. **The principle wording** in [tab 4](04-formulas.md). Settled by Emma, 2026-11-07, as proposed.
8. **The share that makes a formula suspect** in the corpus sanity check. Settled by Emma, 2026-11-07: more than half of the papers that print all parts, as proposed.
9. **Scope of the first pass.** Settled by Emma, 2026-11-07. Calcium and electrophysiology from the start, not contractility only; the rebuild included them.

**First corpus**

10. **Rows or records first.** Settled by Emma, by 2026-11-07. Start fresh from records written by the new pipeline; the validation study's rows are not used.
11. **Both readers' rows, or one.** Settled by Emma, by 2026-11-07. No longer applies: starting fresh, one record per study.
12. **The new-terms-per-paper line.** Settled by Emma, by 2026-11-07. No fixed threshold: new terms per paper are plotted against paper order at each checkpoint, and the curve decides when the vocabulary has settled enough for a release.

**First build (2026-11-07)**

13. **Defaults with unit overrides.** Settled by Emma, 2026-11-07. A field may not sit in `default_context` while some units override it (the proposal had been yes). A field that differs between units is written in each unit. Code makes the repetition cheap: identical stated text within a paper is mapped once and reused, and copies of a value that differ only in wording are flagged back to the reader.
14. **`stated_direction`** for items with no values. Settled by Emma, 2026-11-07. Yes, flagged wherever it is used: the item shows "direction: stated, not computed", comparisons say "(stated)", and release tables carry `direction_origin` ([tab 5](05-across-sources.md)).
15. **Groups.** Settled by Emma, 2026-11-07. Groups are first-class parts of a unit, each with its full context. An item is a test between groups: two (a pair), several (an omnibus), sets of groups (a main effect), or an interaction. The reader never writes what varies: code compares the groups' contexts. One differing field gives a simple contrast; two in a pair give a confound flagged by code; two factors crossed in all combinations make a factorial design. Values, data rows and readings attach to groups. This superseded the factorial-contrast form first proposed for [tab 2](02-audit.md), per-arm context, and qualifier contrasts (16).
16. **Qualifier contrasts** (`condition_qualifiers` / `reference_qualifiers`). Settled by Emma, 2026-11-07: code compares the groups' numbers. Superseded the same day by groups (15), where each group's numbers are part of its context and no qualifier form is needed.
17. **What `derivation` and `method` mean in a key.** Settled by Emma, 2026-11-07. Required only for measures whose value depends on them (e.g. stress on how area is taken); values measured directly are compared without them, and an unstated method never blocks a direction comparison.
18. **Pinned ontology releases.** Settled by Emma, 2026-11-07. The build downloads the current releases of ChEBI, CL, MONDO, Cellosaurus and UO; versions and checksums are recorded in `fields/<field>/ontologies.yaml`, and the files stay out of git. Agents look terms up in these local copies (no web lookups); code checks every adopted id against them on every vocabulary edit, and an unknown or obsolete id fails the gate. Moving to a newer release is a logged event.
19. **Source-data requests.** Settled by Emma, 2026-11-07. Each release lists papers whose items stay *cannot check* for lack of per-sample data, ranked by how many items the data would open, and papers whose supplementary files are missing from their folder.

**Rebuild check-in (2026-11-07, after 5 papers)**

20. **Native tissue and other-study groups.** Settled by Emma, 2026-11-07. `Group.kind` (*engineered*, *native tissue*, *other study*); such a group resolves only its own context, and its pairs are *against benchmark*: value comparisons only, no contrast, no confound ([tab 2](02-audit.md)).
21. **Aliased and linked fields.** Settled by Emma, 2026-11-07. Aliased pairs stay confounds, labelled, compounded for factorial recognition and kept out of direction comparisons. Linked field pairs (`genotype ~ disease_model`) are declared in field content by a person and count as one contrast on the first field ([tab 2](02-audit.md)).
22. **Tests along x, between measures, and values over several groups.** Settled by Emma, 2026-11-07. One group per x level; a test between two measures is a derivation; `over: [groups]` for a value printed for several groups ([tab 2](02-audit.md)).
23. **Post-hoc tests and two-way ANOVA.** Settled by Emma, 2026-11-07. Given models, from points only, only when the unit's groups determine the family, each validated first against a consistent printed P ([tab 4](04-formulas.md)).
24. **Relative measures.** Settled by Emma, 2026-11-07. A base measure with qualifiers `expressed_as` and `normalised_to` from fixed lists; value keys require `level` and `expressed_as`, direction keys `level` (tabs [3](03-vocabulary.md), [5](05-across-sources.md)).
25. **New fields.** Settled by Emma, 2026-11-07. Added `mechanical_load`, `transgene`, `measurement_calcium_mM` (with `media_calcium_mM` renamed `culture_calcium_mM`) and `donor_age`; the `add_field` edit stayed open to agents ([tab 3](03-vocabulary.md)). Superseded for new fields by decision 47 (fields change only at checkpoints, by rule).
26. **Smaller defaults.** Settled by Emma, 2026-11-07. A named P state *significant, threshold not stated* (direction, no P check); several anchored P values per item, checked by code; `aggregation` alternatives for per-sample formulas against printed means.
27. **From the independent check.** Settled by Emma, 2026-11-07. Suspect cells run with and without; a claim judged *follows* against an opposite computed direction is flagged; pacing enters the keys of rates it can entrain; stated inputs carry their printed-precision interval in chains.

**Finalising the code (2026-11-07; settled by the building agent on Emma's instruction to use best judgement, for Emma's review)**

28. **Open-world matching.** A must-match field is known-same, known-different or unknown (*not stated*, *not yet read*, *not stated in this source*, *by reference*). Known-different blocks; unknowns do not: the verdict is computed and lists what it `assumes`, and confirmed verdicts (nothing assumed) are reported apart ([tab 5](05-across-sources.md)). Chosen over keeping unknowns as blocks, which left 2 value verdicts in 362,391 pairs, and over filling unknowns (inference).
29. **Field sets and *not yet read*.** A record names its field set; fields added later resolve to *not yet read* and are filled at checkpoints. The record gate requires only the record's own set. This replaced the earlier rule that every field resolves in every record, which forced a re-read of every paper for each new field (tabs [2](02-audit.md), [3](03-vocabulary.md)).
30. **Declared states on any field, and *healthy control line*.** States are field content for any kind of field; code matches them, and the gate refuses a mapping or flag for one; a state against a term is unknown. Genotype declares *healthy control line*, written only from the paper's own words ([tab 3](03-vocabulary.md)).
31. **Unequal variances.** Post-hoc pairs always run their unequal-variance form as a labelled alternative (Games–Howell beside Tukey, Welch beside the pooled t). Chosen over a fixed SD-ratio threshold, because the assumption is unstated in nearly every paper (tabs [2](02-audit.md), [4](04-formulas.md)).
32. **A value's own normalisation.** `expressed_as` and `normalised_to` on a value, from its legend, win over the mapping; a physical unit means *absolute* ([tab 2](02-audit.md)).
33. **Sets are complete per group; members are factors.** A group's stated set lists every member the paper gives, with absence written when stated; groups differing in members are factorial on them ([tab 2](02-audit.md)). Chosen over treating qualifiers as factors.
34. **New fields (field set 2):** `species` (own terms with NCBITaxon xrefs, checked against a pinned taxslim release), `time_point`, `measurement_medium`. Assay O₂ went to a `maturation_strategy` or `treatment` qualifier until it recurs ([tab 3](03-vocabulary.md)).
35. **Model and simulation outputs** are not evidence items or groups: derivations where the paper derives a step, otherwise left out and logged ([tab 2](02-audit.md)).
36. **Methods thresholds.** A significance threshold stated once in the Methods applies to the paper's asterisks ([tab 2](02-audit.md)).
37. **`asserts_direction` kept,** set only when every item a claim rests on is asserted to move the same way, in the direction of the printed numbers; it flags only up against down ([tab 2](02-audit.md)).
38. **Value comparisons within SDs,** from a stated SD, an SEM × √n, or the points; no spread gives *not available (no spread)* ([tab 5](05-across-sources.md)).
39. **Releases are CSV only** for now; Parquet and DuckDB wait for a larger corpus ([tab 6](06-releases.md)). **Dimensions are checked with sympy,** not pint ([tab 7](07-building.md)). **The Cellosaurus index keeps human lines;** rat and mouse cells are named in `species`.
40. **Jobs order.** The formula job may run before its paper's vocabulary job; it does not read terms ([tab 7](07-building.md)).
41. **Named states declared during the rebuild:** donor age (fetal, neonatal, newborn, infant, young, adult), confluency (confluent, confluence), time point (baseline).

**After the rebuild: how we work (proposed 2026-11-08 by the building agent; accepted by Emma 2026-11-09; built 2026-11-09)**

The rebuild met the first goal and fell short on the second. Records were right wherever an independent check looked (15/15 items, 7/7 readings, 200/200 cells, 10/10 mappings), and every paper had real problems the checks found. But 59 % of items could not be checked, mostly for lack of data, and papers rarely met: 2 confirmed value verdicts in 362,391 pairs. Most of the time went into adding checks and fields while agents ran, and each addition produced new artefacts. Decisions 42–49 shifted effort toward what moves the goals. All were built before the 2026-11-09 prototype (decision 52).

42. **Context is anchored.** Accepted by Emma, 2026-11-09. One quote per distinct stated context value; code checks the quote holds it ([tab 2](02-audit.md)). Inference in context was the agents' most common error, and the only one no gate saw.
43. **Findings, not item counts.** Accepted by Emma, 2026-11-09. Failing checks are grouped by cause into findings that lead each paper's page and the release ([tab 2](02-audit.md)).
44. **A gold set gates every check.** Accepted by Emma, 2026-11-09. No check enters or changes without reproducing every confirmed item ([tab 2](02-audit.md)).
45. **Strata, not pairs; the dataset before the verdicts.** Accepted by Emma, 2026-11-09. Comparisons are comparable sets per measure, and the main cross-paper product is the dataset with unknowns explicit ([tab 5](05-across-sources.md)).
46. **Depth comes from data.** Accepted by Emma, 2026-11-09. Source-data requests go out before the corpus run, and no new statistical check is added until requested data arrive or a gold item calls for it (principle 7). The building agent drafts the requests from `source_data_requests.csv`; Emma sends them.
47. **Fields are designed before the corpus** from a survey, then change only at checkpoints; a rule, not a person, decides the field list ([tab 3](03-vocabulary.md)). Accepted by Emma, 2026-11-09. Revised the same day after the first survey made 47 fields: a condition becomes a field when 3 or more surveyed papers vary it between groups or a third state it. The second survey (28 papers; 2020_Weng was left out after three safety stops) gave field set 3: `seeding_density` (varied in 3 papers), `dissociation_reagent` and `incubator_atmosphere` (each stated by more than a third).
48. **Agent reports are reviewed as a step, and the code is frozen during a run** ([tab 7](07-building.md)). Accepted by Emma, 2026-11-09.
49. **No needless compute.** Accepted by Emma, 2026-11-09. The rebuild cost about $15 of API time per paper (record jobs 17 %, figure jobs 24 %, reruns after mid-run changes 12 %, the orchestrating conversation 27 %). A figure is digitized only when an item needs its values and no printed or released numbers give them, one short job per figure; jobs run from a script that writes results and gate output to files, so the orchestrator reads summaries, not transcripts ([tab 7](07-building.md)). Narrowed by Emma on 2026-11-10, after the prototype: figures are read only for individual points, for items whose test a check can verify from them, and tables in the text and supplements are read first; bar means are no longer read for the dataset alone.

**After the prototype**

50. **All supplements read; data tables used.** Emma, 2026-11-10. Every file in a paper's folder is read and listed (`source.files`) or explained (`source.not_used`); every data or table file feeds values or says why not; code checks both ([tab 2](02-audit.md)).
51. **A first look before each figure job.** Emma, 2026-11-10. A small model looks at the legend's page and the page before and decides `no_points`; a figure job is skipped only on *no* with the page named ([tab 7](07-building.md)). Legend-text rules were tested and rejected (they skipped 8 % safely, or 42 % while losing a figure with points). Extended by the building agent on 2026-11-13 (test-first, during run 2026-11-12): when legends are batched, the page that carries a figure's heading is sent too.
52. **Decisions 42–49 built, and the prototype run.** Building agent, 2026-11-09. Context anchors, findings, the gold set, strata, the field survey, report review and the scripted runner were built test-first, then run on 4 force papers that share a measure (Trials and runs, *Prototype*). This closed the open item "build decisions 42–49, then a prototype run on 3–5 papers".
53. **Unattended runs: `livinglit add`.** Building agent, 2026-11-10. `livinglit add` runs every job for a paper from a script, gate by gate, resumes from the step it stopped at, and commits a paper only when all four gates pass; `livinglit site` builds the explorer from a release. The package moved to a src layout (`src/livinglit/`) the same day. Run 2026-11-10 used it for 2019_Zhao, then for 20 papers (15 → 35). After that run the runner was changed, test-first, to treat a record job that writes no record as a gate failure and save the attempt's cost (2026-11-12), and the explorer was republished at a new link (2026-11-12), closing proposals 1 and 3 of that run.
54. **Papers picked by meeting points.** Building agent, 2026-11-12, for run 2026-11-12. The 271 unread papers were ranked by the measure × contrast strata they would turn into meeting points in the last release; the top 15 were read, taking the corpus from 35 to 50 papers (`runs/2026-11-12_candidates/`). Run 2026-11-10 had ranked candidates by citation count × overlap with shared measures and contrasts.
55. **The Atlas in the release.** Building agent, 2026-11-12 to 2026-11-13; merged 2026-11-13. `livinglit release` writes the Atlas (an explorer by question, with the knowledge graph) from the release's own tables, standalone and as a page to publish ([tab 6](06-releases.md)). Its cover shows the whole-plan diagram and the review the corpus is drawn from, with citation and summary, from `fields/<field>/cover.yaml`, copied into each release. No field content is in code: the fields offered for highlighting and the graph's layers are chosen from the data.
56. **The agent command line is configuration.** Building agent, 2026-11-13. The runner and the first look read the agent's command line, model, environment and usage-limit pattern from `agent.yaml` (keys documented in `agent.example.yaml`), so no agent product is named in code. The same change added `tools/make_public.py`, which builds the public tree.
57. **The spec lives in the repository.** 2026-11-13. The spec's working copy moved from an online document to these files, which are now its single source; figures are drawn by a script in `figures/`.
58. **Six designed parts built.** Emma, 2026-11-13. Built, each test-first: comparisons use a value rebuilt from a failed derivation and name the rebuilt sides (tab 4, *Wrong derivations*); *same n along the chain* (tab 4); each release writes `changes.yaml` and `CHANGES.md` against the previous release and copies its logs into `logs/` (tab 6); `livinglit overlay` draws stored readings over their figure outside the repository (tab 2); every release re-checks adopted ids and xrefs against the pinned ontologies (tab 3); `formulas.csv` reports each entry's use and conflict share (tab 4).
59. **Two parts deferred by count, two designs changed.** Emma, 2026-11-13. Counted on release run-2026-11-12: carrying values stated by reference from a cited record in the corpus would serve 1 of 1,541 such values, and shared data and materials would touch 279 of 35,798 comparisons (same lab), none with a verdict; both stay designed and deferred. Changed: an entry is never marked *suspect* from its conflict share, which is reported instead (a field-wide conflict can be a finding); coverage trends, co-occurrence and unmeasured combinations are analysis outside the release (tabs 4 and 5).
60. **One page.** Emma, 2026-11-13. The explorer and the Atlas showed the same release twice. They are now one page, the explorer: the Atlas's views by question, with each result opening its own page (the old explorer's per-item detail), loaded from its paper's file (tab 6). The old explorer's run report, ambiguity logs and vocabulary-growth chart are left out: they describe the build, not the release.

## Open

### Still open

- **Scale.** The corpus holds 50 of the Ewoldt review's 300 studies.
- **Second reader.** All judgements are single-reader. Planned: one paper read by a second record reader and compared item by item, before 30 papers. The corpus passed 30 without it; Emma decides whether it still comes first.
- **Order sensitivity** of a vocabulary built one paper at a time. Planned: re-map the papers in a second seeded order and compare, before 30 papers. Not done; the same question as the second reader.
- **Settling of the vocabulary.** New terms per paper over the first 10 papers were 77, 18, 43, 41, 14, 45, 9, 46, 19, 37. The vocabulary had 883 terms at 35 papers and 1,076 at 50 (about 13 new terms per paper over the last 15). Not settled.
- **Hard figures and tables.** Uncalibrated figures (JPEGs, box plots, bars without points); raster figures with hidden markers (under mean lines, overlapping, axis breaks); image-only tables whose values cannot be anchored by text.
- **Evaluation.** Set aside for now ([tab 7](07-building.md)); benchmarks and the validation study will return later.

- **Designed, not yet built** (found when the spec was brought up to date, 2026-11-13; six built and two changed on the same day, decisions 58–59). Still open, each listed in its tab under *Designed, not yet built*: values stated by reference carried from a cited record in the corpus (tab 1; deferred by count); term groups, moving a field to an ontology as a logged edit (tab 3); which formula the numbers fit, a factor that differs between groups ("conclusion may change"), rebuilt values in claims against adult values (needs adult reference values), `applies_when` checked when entries are applied (tab 4); shared data and materials (tab 5; deferred by count).

### Open proposals (from run reports; not decisions)

- **Pick papers for data by opening their files** (prototype, 2026-11-09).
- **Printed-n parser** (run 2026-11-12, 1): do not take numbers that are part of a name (`PLZ/19004`); possibly take n only after "n =" up to the unit word.
- **n checks by unit** (run 2026-11-10, 7): tell the printed n's unit (batches, wells, tissues) from the plotted points before *n against readings or data* calls a value inconsistent (Huebsch, Ronaldson-Bouchard, Garay).
- **Labelled alternatives** (run 2026-11-12, 2): code evaluates a derivation's labelled alternatives and reports "consistent under the alternative" (deLange).
- **A figure job that writes nothing fails its gate** (run 2026-11-12, 3): each figure job's gate requires its unit in `figures` or `no_points`.
- **Re-gating as a standard step** (run 2026-11-10, 4; run 2026-11-12, 4): stale stored mappings appeared after each batch (5, then 9). Either `add` reruns the terms gate on every record at the end, or the vocabulary step drops mappings that code now matches, or the terms gate tolerates them.
- **A scratch folder per job** (run 2026-11-10, 2): created by the runner inside an allowed path and deleted after the gate, with a repo-rules check that no paper text or render is left behind. Agents wrote to `/tmp` in both runs; the files from run 2026-11-12 are not yet deleted (Emma decides).
- **Job folders named by run** (run 2026-11-10, 9): not by `date.today()`, so a run is in one folder and same-day reruns do not overwrite earlier attempts.
- **Number words and day shorthand** (run 2026-11-10, 5): read "Forty-eight hours" and "D0", or flag them as not parseable.
- **In vivo and native-tissue arms as contrasts; several doses in one value; log-scale expression** (run 2026-11-10, 8).
- **A sample audit of looked-off figures** (run 2026-11-10, 6): a stronger model rechecks about 10 looked-off units each run (about $5) to measure the miss rate.
