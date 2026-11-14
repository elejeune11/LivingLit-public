# 6 · Releases and use

A **release** is LivingLit's boundary: a tagged set of documented tables, generated from the files, that anyone (a person, a script, an agent) can query and cite. Everything inside it is anchored or computed; everything built on it lives outside.

## What a release holds

`livinglit release <tag>` audits every record and writes `releases/<tag>/`:

| File | One row per | Carries |
| --- | --- | --- |
| `papers.csv` | source | title, DOI, year, lab, kind, files, depth |
| `units.csv` | unit (one experiment as the paper presents it) | paper, where, title, status, depth, design |
| `groups.csv` | group (as the paper shows it, within a unit) | paper, unit, label, context terms |
| `items.csv` | evidence item | paper, unit, measure and its terms, n, test, P, finding, anchor, status, depth, computed contrast, direction and `direction_origin`, upstream flags, method, software |
| `values.csv` | value | see *Values as a dataset* below |
| `mappings.csv` | stated context (of a paper, unit or group) or measure | the stated text, its terms and qualifiers or flag, origin (matched, assigned, a named state…), vocabulary version |
| `derivations.csv` | derivation | formula as stated, the library formula and its kind, parameter kinds, inputs used, verdict, rebuilt value, flags |
| `checks.csv` | check run | check, target, library entry, basis, alternatives tried, verdict |
| `findings.csv` | finding | failing checks grouped by cause ([tab 2](02-audit.md)), with the items they affect |
| `claims.csv` | stated or attributed claim | quote, scope, the evidence it rests on, the judgement per dimension, the code's verdict |
| `strata.csv` | stratum | measure, part, key signature, items, papers, values with spreads, verdicts, unknowns, links ([tab 5](05-across-sources.md)) |
| `comparisons.csv` | pair of items with a computed verdict | measure, part, both items and units, verdict, `assumes`, blocking fields, relaxation, `direction_origin` |
| `coverage.csv` | field × term | sources, labs, mappings; per field, the count of each named state |
| `terms.csv` | vocabulary term | fields, label, parent, source, definition, scope, synonyms, the paper that added it |
| `formulas.csv` | library entry | kind, statement, equations, what it holds under, whether it is held as suspect |
| `completeness.csv` | cited paper not in the corpus | its citation and DOI, the records, fields and locations that depend on it (values stated by reference), and its rank by how many values it would complete |
| `refinements.csv` | earlier mapping a newer term may refine | paper, location, stated text, current term, the new term and the paper that added it |
| `source_data_requests.csv` | paper whose items stay *cannot check* for lack of per-sample data | items that cannot be checked, items in all |
| `missing_supplements.csv` | paper | source files the record names that the corpus lacks, or lists as missing |

Beside the tables: `summary.yaml` (vocabulary and formula library versions, per-paper counts, statuses, depths, mapping origins, directions, confirmed and conditional verdicts, the most assumed fields and the most common blockers, strata, completeness), `SCHEMA.md` (generated from the Pydantic models), `cover.yaml` (copied from the field), `logs/` (the vocabulary and formula logs the release was built from), `changes.yaml` and `CHANGES.md` (what changed since the previous release, below), and the pages below. `livinglit requests <folder>` drafts one source-data request per paper in `source_data_requests.csv`, for a person to send; nothing is sent.

**Values as a dataset.** For each record, code writes `records/<paper>/values.csv`: one row per value, with paper, unit, item, group, the group's label and its terms, kind (point, mean, sd, sem, n, p, …), value as printed, numeric value, unit of value, origin (stated, from data, read, derived by LivingLit), interval, x, measure terms, context terms per field and the item's computed contrast. The release joins these into one `values.csv` for the corpus, keyed by ids to the other tables. Filter `values.csv` by a measure term and you have the dataset for one question.

**Sizes.** Release run-2026-11-12 (50 papers, 2014–2022): 7,704 items, 2,641 claims, 95,825 values (`values.csv`, 131 MB), 35,798 comparisons (14 MB), 12,888 strata; vocabulary v69 (1,076 terms), formula library v33 (87 entries).

**Gaps are values, not blanks.** *Not stated*, *flagged*, *unmapped* and *cannot check* appear as values, so a reader or an agent never mistakes an absence for a negative.

**Provenance.** Every row names its paper and, where it has one, its anchor. Each record file names the agent instructions that wrote it and the vocabulary or formula library version it was gated against; `summary.yaml` names the versions the release was built with. **Formats:** CSV, with a schema document generated from the Pydantic models; Parquet or DuckDB only when a corpus outgrows CSV. **Versions:** each release is tagged (e.g. `run-2026-11-12`) and written to its own folder; a later release never changes an earlier one.

## The explorer: the visualization step

Every release ends with one visualization step: code writes **the explorer**, one page built from the release's audits, tables, vocabulary and formula library. Nothing in it is written by an agent, and nothing on it is new: every number, verdict and link is one the release already holds. The page template (`livinglit/explorer_template.html`) holds layout and drawing code only, never field content (a test guards this); `livinglit/explorer.py` assembles the data it renders. Release text cannot break out of the page's script.

The explorer shows the release by question. It opens with a cover read from `fields/<field>/cover.yaml` through the release: the field's source review (citation and summary) beside the whole-plan diagram. Its views:

| View | What it shows |
| --- | --- |
| **Where do papers meet?** | measures shared by two or more papers, and the results under each |
| **How is it all connected?** | the knowledge graph: papers and the terms that link them, by kind of term |
| **How do reported values line up?** | reported values of one measure on one axis, highlighted by a context field |
| **Which comparisons hold?** | cross-paper verdicts and the context each sets aside |
| **Do the numbers check out?** | each paper's results by status, and the findings by check |
| **Do the claims follow?** | claims by verdict, and where they go further than their results |
| **What is missing?** | fields most often not stated, and cited works the corpus depends on |
| **Vocabulary**, **Formulas** | the terms with their use, and the formula library by kind |
| **Papers** | each paper and its results |
| **One result** | anchor, status and depth; measure and n; groups and contrast; points per group; values with origin and interval; every check code ran; derivations along the formula library; context resolved paper → unit → group → result, with each field's origin and terms |

Every result listed anywhere opens its own page. The context fields the page highlights and the graph's layers are chosen from the data, not listed in code. Unit conversions on its value axis are for display only and say so.

**Built to stay small.** The page holds what every view needs; each paper's result details go in their own file beside it (`explorer_data/items_<paper>.js`), loaded only when one of its results is opened. No file grows with the corpus. The page is written twice: `explorer.html`, a standalone page, and `explorer_artifact.html`, the same page without document tags, for embedding in a host page. `livinglit site <release> <folder>` writes it for a static host as `index.html`, with `explorer_data/` and `.nojekyll`, replacing what was there; the public repository serves this folder as `site/`. After each run the explorer is published at one fixed link, the new release replacing the old.

Overlays and page images stay outside the repository and outside the pages.

## Living

A new source, dataset, erratum, term or formula reruns everything downstream: the new source is audited and mapped; comparisons, strata and coverage are recomputed; nothing is overwritten, and an erratum is a new source. A release is cut after each run, and says **what changed since the previous one** (`changes.yaml`, `CHANGES.md`; `--since <tag>` names it, by default the latest other release): papers, terms and formulas added or removed, items whose status changed, and comparisons whose verdict changed, each with what changed in its row (a side now compared on a rebuilt value, the fields assumed). The corpus is drawn from the studies the field's source review cites (the explorer's cover); `refinements.csv` lists the earlier mappings a newer term may refine, for the next re-map checkpoint.

**Growing the corpus.** Each build ends with the completeness list ([tab 2](02-audit.md)): the cited papers not yet in the corpus that would complete the most records, with what each would complete. Adding one is a person's decision. Carrying its values into the citing records is designed, not built ([tab 1](01-goal.md)).

**Completeness counts once per field and paper.** A value stated by reference counts once per field and paper, not once per unit, so a reference repeated across many units does not inflate a citation's rank.

## Use from outside

Exploration is not part of LivingLit. A person or an agent queries a release, synthesizes, tests a claim against the corpus or forms hypotheses, and cites the release tag and the row ids it rests on. Recent evaluations favour exactly this split: agents extract single values well but combine evidence across studies unreliably, and an answer computed by a query over validated tables is tied to its evidence by construction. Nothing written outside enters a release; a missing term or a misread value is fixed the way everything else is, by the audit and the vocabulary agent when a source is read.
