# Adding papers

A batch of papers can be added without a person. The orchestrator (a person, a script, or an agent session following
these steps) starts jobs, reads their short reports and gate results, and keeps going. It does not read transcripts or
papers, and does not change code, checks, fields or briefs during a run. Design: [tab 7](minimalist_design/07-building.md).

## Before starting

1. The working tree is clean and you are on a run branch (`run-<date>`).
2. `uv run pytest -q` passes. Never start a run on red.
3. Each paper's files are in `papers_dont_ever_commit/<year>_<Author>/` (PDFs, supplements, released datasets).
4. `agent.yaml` names the agent to run (copy `agent.example.yaml`).
5. Write `runs/<date>_add/PLAN.md` with the papers and predictions for the batch (records passing all gates, share of
   items checkable, findings per paper, cost per paper), so the run report can be compared with them.

## The run

For each paper, one at a time (the vocabulary and formula jobs share the field libraries):

```bash
uv run livinglit add <paper>
```

`add` runs the record job, then for each figure that needs reading a first look and a figure job unless the look ruled
it out, then the vocabulary job and the formula job, each to a passing gate. It skips any step whose gate already
passes. It prints one JSON line:

- `added`: go on to the next paper.
- `parked`: a gate kept failing. Note the paper, the step and the problems in the run report, and go on.
- `usage limit`: stop and commit what is done. Rerunning `livinglit add` with the same papers continues from that step.

After each paper, read `runs/<date>_jobs/<paper>/*.report.md` and `*.json` for `for_review` items and the agents'
unsure judgements, and note them in the report. Commit after each added paper.

## After the papers

1. `uv run pytest -q` passes, and so does every gate for each paper added:
   `uv run livinglit gate record|figures|terms|derived <paper>`.
2. Build the release: `uv run livinglit release run-<date>`. It writes the tables and `explorer.html`.
3. Update the hosted page: `uv run livinglit site run-<date> site/` (the explorer as `index.html`), then commit
   `site/`.
4. Write `runs/<date>_add/REPORT.md` against the plan's predictions: papers added and parked, cost, findings, items for
   review, and any proposed change to a check, field, brief, key or the code (proposed only, never made during a run).
