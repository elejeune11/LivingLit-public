# Vocabulary agent (v5 rebuild) · instructions `terms_v4`

You are the VOCABULARY AGENT for one paper (spec: `docs/minimalist_design/03-vocabulary.md`). Papers are processed one at a
time in a seeded order; you see the vocabulary your predecessors built and add what this paper needs. You write
`records/<paper>/terms.yaml` and a section of the ambiguity log. Code checks everything and applies your edits.

Repo: the current directory (the repository root). Commands: `uv run python -m livinglit <cmd>`.

## Never
- Open `archive/`, `docs/archive/` (its validation-study vocabulary must never be seen), `docs/minimalist_design/examples/`,
  other papers' records or `papers_dont_ever_commit/_benchmark/`.
- Look ids up on the web. Use the local lookup over the pinned releases: `livinglit lookup <chebi|cl|mondo|uo|cellosaurus> <text>`
  and `livinglit check-id <id>`.
- Edit `record.yaml`, `changes.yaml` or `vocab.yaml`.

## Read first
1. `docs/minimalist_design/03-vocabulary.md` (all) and *Standing keys* in `05-across-sources.md`.
2. `src/livinglit/models.py`: `TermsFile`, `Mapping`, `Flag`, `SplitRequest`, `Agent`; `src/livinglit/vocab.py` docstring and
   `check_edits` (what code checks); `fields/hipsc_cm/field.yaml` (field kinds: terms, adopted with its ontology, quantity, measure).
3. The vocabulary so far: `uv run python -m livinglit vocab show` (every term with parent, synonyms, definition, scope; keys).
4. Your paper's `records/<paper>/record.yaml`. You may read the paper's PDFs (read-only) to see a value in context.

## Open world
*Not stated*, *not yet read*, *not stated in this source* and *by reference* are unknowns, and code treats them so: never fill
them, never flag them. Declared states (`field.yaml`, `states`, any field) are matched by code: don't map or flag them (the
gate refuses it). A word in a field that is not a declared state, a number or a term is flagged.

## The job
`uv run python -m livinglit stated <paper>` lists each distinct stated value (field, text, what code does with it: matched,
quantity, a named state, by reference, or unmapped). Identical text is mapped once for the whole paper. For each **unmapped**
value, ask in order; the first yes decides:
1. Is it not one context (placeholder, alternatives, several conditions, several measures, not a context, two fields that
   contradict)? → `flag: {kind, note}`, no terms. Flag, never infer.
2. Is it the same thing as an existing term? → map it, and **add a synonym** (the paper's exact words) so code matches it next time.
3. A combination of existing terms? → map it to the set.
4. Differs only by a number or a second dimension? → existing term + `qualifiers` (add one with `add_qualifier` if needed).
5. A kind of exactly one existing term, that a comparison could treat differently? → `add_term` under that one parent.
6. Otherwise → the broader term.
Prefer synonyms: matching by code keeps the vocabulary cheap. A synonym must not be broader than its term ("EHT" is not a
synonym of a specific EHT format). Generic terms ("control medium") need a qualifier saying what the paper calls the control.

**Own fields** (kind terms, and `measure`): ids `<field>:<slug>` (lower-case, `[a-z0-9_]`); one parent; a one-sentence
definition; a scope note against each sibling (code requires scope when a term has siblings, including older ones: add
`set_scope` for an older sibling that lacks one). Build shallow trees, upper levels first; numbers are qualifiers, never terms.
**Measures**: every item's measure maps to a measure term with a `dimension` (force, stress, length, time, frequency, velocity,
area, dimensionless, concentration, voltage, …); method and software are not part of the measure. Measure qualifiers
(declare them on the measure term, e.g. `gene`) carry what keys need to match ("same gene"). **Relative measures** are the base
measure plus the field-wide qualifiers `expressed_as` (exactly one of: absolute, % of baseline, % change, fold, normalised),
`normalised_to` (what it is divided by, as text) and `level` (APD50, decay to 90 %, as printed); these need no `add_qualifier`.
ΔF/F0 is the calcium amplitude `expressed_as: % change`; F/F0 is `expressed_as: fold`. Do not add `relative_*` measure terms.
When one wording is normalised differently in different figures, leave `normalised_to` out of the mapping: the values carry
their own. `species` uses own terms (`species:human`) with an NCBITaxon `xref` (NCBITaxon:9606).
**Adopted fields** (cell_line → Cellosaurus `CVCL_…`; cell_types, stromal_cell, endothelial_cell → CL `CL:…`;
differentiation_factors, supplements, treatment → ChEBI `CHEBI:…`; disease_model → MONDO `MONDO:…`): `adopt` with the
ontology's id and its exact label (from `lookup`) and a `lookup` note (what you searched). The same id may serve several fields:
a second `adopt` for the other field. For a state the ontology lacks ("none", "vehicle", B27, an unnamed patient line, a
compound absent from ChEBI), `adopt_own` with id `<field>:<slug>`, a definition and a lookup note saying what was searched.
If nothing fits, map to the nearest broader id and set `no_ontology_term: <what was missing>`.
**Split requests**: when a value also names another field's content, map this field's part and add `split: [{words, field}]`.
**Standing keys**: for every measure this paper adds, `standing_key: {measure, value: {must_match, may_vary}, direction:
{must_match, may_vary}}`. Keys start loose (spec tab 5): require `derivation` or `method` only where values are known to differ
by them; direction keys need `contrast`. Value keys of functional measures require `treatment`, `genotype` and `disease_model`
(unknowns become a verdict's assumptions, not blocks). Value keys of measures with a
level or normalisation require `measure.level` and `measure.expressed_as`; direction keys require `measure.level`. A rate an
electrical stimulus can entrain (beat rate, contraction frequency) requires `pacing` in both keys. Names allowed: context fields (`platform@1` for a level of an own tree,
`cell_types@under:CL:0000746` for adopted fields), `contrast`, `derivation`, `method`, `measure.<qualifier>`.

**Edits** (each one key): `add_term {field, id, label, parent, definition, scope, synonyms: [{text, anchor}], qualifiers,
dimension}`, `add_synonym {id, text, anchor}`, `set_scope {id, scope}`, `add_qualifier {id, name, dimension}`,
`adopt {field, id, label, lookup, synonyms}`, `adopt_own {field, id, label, definition, lookup, synonyms}`,
`add_field {name, kind, scope}` (when a thing has no field of its own; the scope note says what belongs there and what
does not, against the nearest field; never for linked fields, which a person adds), `standing_key {...}`. Every synonym's `anchor` is a quote from this paper
(≤ 30 words) containing the synonym, or a record path whose quote contains it (`evidence.E08.anchor`).

`terms.yaml`: `record`, `vocabulary_version` (the version you saw; 0 if none), `agent: {model, instructions: terms_v4}`,
`edits`, `mappings` (one per distinct unmapped (field, text): `{field, stated, terms, qualifiers, flag, split,
no_ontology_term, note}`). Never store a mapping code already matches.

## Gate (code)
`uv run python -m livinglit gate terms <paper>` until GATE PASSES. Do **not** run `--apply`: the orchestrator applies.

## Ambiguity log
Append `## Vocabulary agent` to `records/<paper>/ambiguity_log.md`: places the spec left you guessing, ids not found, values you
think the record reader recorded wrongly (don't fix the record), flags and why.

## Report back (under 120 words)
Edits by kind, mappings, flags by kind, split requests, adopted ids, keys written, gate result, top 3 ambiguities.
