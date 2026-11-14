# 7 · How it is built

A few fixed requirements, because the results can only be trusted if the checking code and the readers are.

## Test-driven development

- A new or changed rule starts as a failing test; code is written until it passes.
- Each test names, in one sentence, the rule and where it comes from in these documents; collection fails otherwise.
- Tests run on small synthetic fixtures with known answers; tests that need the real papers are marked and skipped without them. Nothing ships red.

## Jobs

| Job | Unit | Writes | Gate |
| --- | --- | --- | --- |
| **Record** | one source | `record.yaml` | code: anchors, schema, plan validates, units, context resolution |
| **Figures and data** | one figure that needs reading, after its record | `data.yaml`, `figures.yaml`, `figures/*.py`, `readings.yaml` | code: every script and cell reproduces what is stored |
| **Vocabulary** | one source, one at a time (each sees its predecessors' vocabulary) | `terms.yaml`, vocabulary edits | code: mapping complete, edits anchored and checked |
| **Formula** | one source with derived measures or statistics to chain, after its record, figures and data | `derived.yaml` (derivations, assumption reports), formula proposals | code: derivations anchored, formulas checked (kind, citation or proof, dimensions, tests) |
| **Re-read** | one flagged field or split request | the field, in `record.yaml` | as the record job |
| **Survey and merge** | one paper's methods and legends; then the untagged conditions of all surveyed papers | `survey/<paper>.yaml`, `survey/merge.yaml` | code: schema, known fields, quotes found; code counts and decides which conditions become fields ([tab 3](03-vocabulary.md)) |
| **Independent check** | a sample, after a build | a report | none: a second agent samples items, readings, inconsistent items and comparisons against the papers, and reports problems ranked |
| **Build** | all sources | audits, comparisons, coverage, the release | tests |

**Order of jobs per paper:** record; then one figure job per figure that needs reading; then vocabulary; then formula. The formula job needs the record, figures and data but not the paper's terms. Library edits are applied in the order they are gated, and only by the orchestrator's own run of the gate.

**Changing field content without a re-run:** a new field goes into a new field set (*not yet read* in earlier records); a declared state is matched by code at once; a rename is a logged event; a key is revised as a logged edit at a checkpoint. Records are re-read only at checkpoints.

**Each agent keeps scratch in its own folder** (`/tmp/livinglit_<paper>/`), because agents run at the same time and one must never run another's script. Scratch is deleted when the job ends; nothing extracted from a paper is kept.

**The agent is configuration.** A job is one run of a headless LLM coding agent: it takes a prompt and its brief (`readers/instructions/`), reads and writes files in the repository, runs `livinglit gate` as a tool, and prints one JSON object as its last line (`result`, and optionally `session_id`, `total_cost_usd`, `num_turns`). Which agent runs, and how its command line is spelled, is set in `agent.yaml` (git-ignored; keys documented in `agent.example.yaml`; code in `livinglit/agent.py`). The configuration also names the folders a job may not read (the archives, the curated table, other papers' records), the read-only command for the first look, and the output that means a usage limit.

**The runner.** `livinglit run <job> <paper>` runs one job: the agent writes its files and a short report; code runs the report review and the job's gate, writes both beside the report (`runs/<date>_jobs/<paper>/`), and resumes the agent with the gate's problems until the gate passes or three attempts are spent. `livinglit add <paper> …` adds papers: record, figures, vocabulary, formula, each to a passing gate. A step whose gate already passes is skipped, so adding is safe to repeat. A paper whose gate keeps failing is *parked* for a person; at a usage limit `add` stops and, run again, resumes at the step it stopped at. The orchestrator reads reports and gate results, never transcripts.

**Gates are code, never part of an agent.** A gate decides whether an agent's output is well-formed and grounded (schema, anchors found, fields of the record's field set filled or *not stated*, mapping complete, edits valid), and everything downstream relies on it, so it must give the same answer every time, under any agent. Each gate is also given to its agent as a tool (`livinglit gate …`) so it can fix problems before handing in; that run saves round trips but is not trusted, and the orchestrator always reruns the gate itself. A gate does not judge whether the agent read the paper correctly (a quote can exist and still be attached to the wrong comparison); that stays with the agent's brief and the independent check.

**Reviewing agent reports.** Before a record's gate, code reviews the agent's output against failure patterns seen in the trials (`livinglit review`, `review.py`): an id silently removed in a re-read blocks the gate; one stated wording in two fields of one context is listed for a person to review. Patterns no rule can decide (a value computed rather than read; one of two conflicting printed values chosen; a group's kind set to avoid inheriting context; a flag written for what code already matches) are examples in the agents' briefs. A new pattern becomes a rule where a rule can decide it.

**The code is frozen during a corpus run.** Between checkpoints the code changes only to fix an artefact, test first, and only when the fix reproduces the whole gold set (`tests/gold/`, [tab 2](02-audit.md)); design changes wait for a checkpoint. Otherwise a new field fails every earlier record's gate and no two builds can be compared.

**No needless compute.** A figure job is made only for a figure some item needs: one whose values no printed text, table or released dataset gives, and whose item's test a check can verify from individual points (`readings_use`). Each such figure is its own short job, which first looks for the points and stops, recording `no_points`, when the figure plots none. Before each figure job, a **first look** (`first_look.py`) shows a small model, read-only, the page where code finds the figure's legend, the page before it, and the page carrying the figure's heading when legends are collected elsewhere, and asks whether the figure plots one marker per sample. The job is skipped only on *no* with the page named, recording `no_points` marked *first look* with the page. A unit naming more than one figure, or whose legend code finds in no file or in more than three, gets no look and its job runs. In a study on 93 recorded units and 319 panels of 28 unread papers, the look missed none of 82 units with points and ruled out 98 % of the rest, at about $0.004 a look against $0.47 for a figure job that finds bars (`runs/2026-11-10_figure_first_look/`).

## Adding papers unattended

A batch of papers is added without a person, in this order:

1. Work on a run branch; the tests are green before the start, and the code is frozen for the run.
2. Write the batch's predictions (papers added, parked, cost, findings, new strata) before any job runs.
3. Run `livinglit add <paper>` for each paper. A paper whose gate keeps failing is parked and the batch goes on; after a usage limit the batch resumes where it stopped.
4. Build the release (`livinglit release <tag>`), which also writes the explorer.
5. Write a run report against the predictions.
6. Ask a person only design questions. A change to a check, field, brief, key or the code is written in the report as a proposal, not made.

## Readers and agents

- Readers and agents make judgements; code decides anything a rule can (in the trials, statuses typed by a reader drifted from the rules).
- Each job's instructions are a versioned brief in `readers/instructions/`.
- One reader per job, labelled single-reader. Target: two readers from different models, working independently, disagreements kept.
- Readers never see the curated table, the validation study's files, other papers' records or hand-built answers: the runner denies those folders to every job.

## Evaluation

The checks code runs on every build (gates, report review, edit checks, the formula library, and the vocabulary measures in [tab 3](03-vocabulary.md)), the gold set, the independent check and each run report against its predictions are the quality signals. Benchmarks for the agents and a validation study against the curated table are not run.

## Files, not a database

| Path | What |
| --- | --- |
| `records/<paper>/` | `record.yaml`, `figures.yaml` + `figures/*.py`, `readings.yaml`, `data.yaml`, `terms.yaml`, `derived.yaml`, `ambiguity_log.md`; `audit.yaml` and `values.csv` generated |
| `fields/<field>/` | `field.yaml` (fields and field sets), `vocab.yaml` (rebuilt from its log), `changes.yaml`, `formulas/`, `ontologies.yaml`, `cover.yaml` |
| `fields/_shared/formulas/` | statistical entries shared by every field |
| `readers/instructions/` | the agents' briefs |
| `src/livinglit/` | generic code: schema, validate, checks, figures, vocabulary, formulas, matching, jobs, release, explorer |
| `runs/` | job reports, gate outputs, run plans and run reports |
| `releases/<tag>/` | generated tables, schema and explorer; git-ignored or published separately |
| `papers_dont_ever_commit/` | sources; never committed |

Everything is rebuilt from files under version control. Papers, figures and overlays stay outside any repository.

**One stated exception to "never store a value a rule computes":** values read from figures and taken from released data are stored in `readings.yaml` and `data.yaml` as a checked cache. Every audit reruns them and fails on any difference ([tab 2](02-audit.md)).

## What the first build taught about the code

- **Pydantic models forbid unknown keys**, so every improvised key fails. Agents still put structure in free `note` fields, so a needed field shows up first as notes in the ambiguity logs: they are read after each run.
- **Agents may generate YAML with scripts** in their scratch folder. The record is the product; the script is not kept.
- **Re-running a gate after its apply** checks the mappings against the current vocabulary and the derivations against the current library, not the applied edits again.
- **An apply with nothing new** does not add a version.
- **Statistics parsing and test kinds** have their own tests with printed strings from real legends ([tab 2](02-audit.md)).
- **Ambiguity logs** are read and acted on after each checkpoint; the tables in [tab 8](08-trials-and-decisions.md) come from them.

## Build order

Each step ended with passing tests on synthetic fixtures before any real paper was touched. All are built:

0. **The record schema** with units, groups, contrasts computed from groups, value paths, the quote matcher, statistics parsing and test kinds ([tab 2](02-audit.md)).
1. **Vocabulary format and rules:** ids, one parent, synonym uniqueness, definitions and scope, append-only log, rebuild from the log.
2. **Matching and comparing on terms:** sets, ancestry, the seven results, qualifiers, *unmapped* and *flagged*.
3. **The vocabulary agent's job:** `terms.yaml` schema, flags, edit checks, the refinement list.
4. **Formulas:** the four kinds, proof and dimension checks (sympy, dimensions as base symbols), assumptions carried from premises; the shared statistical entries ([tab 4](04-formulas.md)), which the checks of [tab 2](02-audit.md) call.
5. **The formula agent's job:** `derived.yaml` with assumption reports, formula proposals and their checks.
6. **Chains:** carrying data and readings, cross-item formulas, alternatives, upstream flags.
7. **Standing keys and comparisons** on terms, with relaxation; the independent check as a standing job.
8. **The runner:** jobs, report review, the first look, `livinglit add`, the agent as configuration.
9. **The release** export, the **explorer**, rebuilt by code from the release ([tab 6](06-releases.md)); a person looks at them before a release is reported.

The first corpus is in progress ([tab 9](09-first-corpus.md)). How the build order and the code changed after the first build is logged in [tab 8](08-trials-and-decisions.md).
