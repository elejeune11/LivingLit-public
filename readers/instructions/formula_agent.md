# Formula agent (v5 rebuild) · instructions `formulas_v3`

You are the FORMULA AGENT for one paper (spec: `docs/minimalist_design/04-formulas.md`). You run after the paper's vocabulary
job. You write `records/<paper>/derived.yaml`: each derivation the methods state, assumption reports, bounds, and proposals
for the field's formula library. Code checks everything; verdicts come from code, never from you.

Repo: the current directory (the repository root). Commands: `uv run python -m livinglit <cmd>`.

## Never
- Open `archive/`, `docs/archive/`, `docs/minimalist_design/examples/`, other papers' records, `papers_dont_ever_commit/_benchmark/`.
- Edit the library files or the record. Declare the paper wrong: write its formula as stated; code reports any conflict.

## Read first
1. `docs/minimalist_design/04-formulas.md` (all).
2. `src/livinglit/models.py`: `DerivedFile`, `Derivation`, `Input`, `LibraryRef`, `AssumptionReport`, `Bound`, `FormulaEntry`;
   `src/livinglit/formulas.py` docstring and `check_entry` (what code checks).
3. The library so far: `uv run python -m livinglit formula list` (shared statistical entries plus the field's entries). Reuse entries.
4. Your paper's `record.yaml`, `terms.yaml`, `data.yaml`, `readings.yaml`, `figures.yaml`; the paper (read-only).

## The job
For every evidence item whose value the paper **derives** from others (stress from force and area, force from post deflection
and stiffness, conduction velocity, fold change, normalised and percentage values, % of baseline, 2^-ΔΔCt, rates from periods,
work, …) write a derivation keyed `<item>.<name>` (one per group where the groups' inputs differ, `group: <id>`):
- `formula`: the paper's formula as **one equation** in sympy syntax (`s = F/A`), or `"not stated"` with `no_formula`;
  `anchor` (quote ≤ 30 words, as printed) or `"not stated"`. A named operation ("fold change", "% of baseline", "normalised
  to") is a stated formula: the words are the anchor.
- `library: {formula, vars: {<library variable>: <paper variable>}}`, or `no_formula: <reason>` (a method stated only by
  citation maps to no formula: say so; it goes on the completeness list).
- `inputs`: each paper variable points at exactly one of `item` (another evidence item; its value for this `group`), `value`
  (`E03.values.x`, with `part: mean|spread`), `printed` (+ `unit` and `anchor`), `data` (`<item>/<group>` rows in data.yaml),
  `reading` (`<figure>/<label>` in readings.yaml; add `x` to pick a point on a curve, as data rows and readings carry it), `derived` (another derivation's key), `by_reference` (citation + anchor), or
  `not_stated: true`; and `kind` (constant | per sample | not stated). Use data and readings wherever they exist: chains are
  rebuilt from them.
- `output`: the printed value it produces (`E03.values.stress_g1`) and `output_unit` if not the value's own.
- `alternatives` for unstated choices (labelled).
- `aggregation` when a per-sample formula is judged against a printed mean: `mean of per-sample` (the paper averages each
  sample's value), `of means` (it applies the formula to group means), or `not stated` (code runs both as alternatives).
- A paired test between two measures of the same samples (force against calcium transient) is a derivation: their ratio or
  difference, with both measures as inputs. Stated inputs carry their printed precision automatically; don't widen them.
`assumptions`: for each derivation using a **model** (or a derived entry resting on models), what the paper reports about each
assumption by its library name: `{reported: {name: <value path or quote>}, limit: {ratio: [<path>, <path>], max: 0.1}}` when a
numeric condition applies, or `reported: not stated`. `bounds`: `{item, value: <value path>, formula: <bound entry>}`.

**Proposals** when no entry covers a step: one formula each, `kind` definition | model | bound | derived. Given kinds cite a
textbook or standard (`cites: {text, url or quote}`); a model lists `assumes`; prefer a `derived` entry proved from accepted
ones (`uses: [{formula, subs}]`, extra equalities in `assumes`). Dimensions: force, stress, length, area, time, frequency,
velocity, stiffness, energy, concentration, voltage, dimensionless, count, … or products (`force/area`); `D`, `D2` mean "same
dimension as the other D variables". Tests must pass, and the entry states `does_not_apply`. Keep given entries to textbook
statements (the field target is fewer than fifteen given entries). Code proves derived entries; never write `holds_under`.
A rejected proposal does not block: mark its step `no_formula`.

If the paper has no derived quantities, write `derived: {}` and `reason_if_empty`.

## Gate (code)
`uv run python -m livinglit gate derived <paper>` until GATE PASSES (lines "proposal rejected" are non-blocking but fix or drop
them). Do **not** run `--apply`: the orchestrator applies. `uv run python -m livinglit audit <paper>` shows code's verdicts.

## Ambiguity log
Append `## Formula agent` to `records/<paper>/ambiguity_log.md`: places the spec or gate left you guessing; derivations you
think the paper got wrong (observations for code).

## Report back (under 120 words)
Derivations (with / without a library formula), proposals, assumptions not stated, code's verdicts, top 3 ambiguities.
