# Independent check (v5 rebuild) · instructions `check_v3`

You are the INDEPENDENT CHECKER after a build (spec: `docs/minimalist_design/07-building.md`, *Jobs*). Every gate has passed;
your job is to find what gates cannot: values attached to the wrong comparison, misread figures, check artefacts, wrong groups.
You write a report only: `runs/<run>/INDEPENDENT_CHECK.md`. You change nothing else.

Repo: the current directory (the repository root). The release is in `releases/<tag>/` (items.csv, checks.csv, values.csv, comparisons.csv,
derivations.csv, mappings.csv); per-paper `records/<paper>/audit.yaml`.

## Never
Open `archive/`, `docs/archive/`, `papers_dont_ever_commit/_benchmark/`. Edit records, code or the vocabulary.

## Sample (seed 7: use `python3 -c "import random; random.seed(7); ..."` to draw)
1. 15 evidence items across the papers: compare value, n, P, test, groups and anchor with the PDF as printed.
2. 7 figure readings: render the panel in /tmp (deleted afterwards) and check counts and a few values against the figure.
3. 200 released-data cells: re-open the file and compare.
4. Up to 10 items with status *inconsistent*: decide for each whether it is a real problem in the paper or an artefact of the
   checks (test kind, ANOVA kind, units, spread, groups, n), with the evidence.
5. Every computed contrast flagged as a confound or an unbalanced main effect, and every factorial unit: is the design as the
   paper describes it?
6. Every direction comparison with a verdict, and 10 not-comparable rows: is the verdict right, and is the blocking field real?
7. 10 mappings (5 assigned, 5 matched): is the term right for what the paper means?
8. Up to 10 post-hoc and two-way ANOVA checks (`checks.csv`, "points to P" with a post-hoc or two_way_anova_f entry): is the
   family the paper's (whole unit, or within a factor's level), the test the one it names, and the error term right?
9. Up to 10 *against benchmark* and 5 *linked* contrasts: is the group kind right, and does a benchmark group state only
   what the paper says about it?
10. Every `suspect` cell or reading: a real slip, and handled as labelled alternatives?
11. Every claim flag (judged direction against computed direction): real, or an artefact of `asserts_direction`?
12. 10 confirmed and 10 conditional comparisons (`comparisons.csv`, `assumes`): same quantity under comparable conditions?
    Is each assumption really unstated in the paper (not a field the reader missed)? Is the verdict computed right?

## Report
Ranked list of problems (most consequential first), each with paper, item or row id, what is wrong, evidence (page, panel,
cell), and whether it is a code artefact (say which rule), a record error, a mapping error, or a real problem in the paper.
Then counts per sample. Under 1,500 words.
