# Contributing

LivingLit is specified in [`docs/minimalist_design/`](docs/minimalist_design/README.md) (README plus tabs 01–09). Read
it before changing behaviour; the build order is in tab 07 and open and settled decisions are in tab 08.

## Fixed rules

The code and tests enforce these. Tests cite them as `(CONTRIBUTING, Fixed rules)`.

- **Never commit papers, figures or figure overlays.** Records hold anchors, extracted values and short quotes only.
  Anything with `dont_commit` in its name stays out of git. No paper text is cached anywhere in the repository. A
  repo-rules test guards this.
- **Test-driven.** Every rule starts as a failing test that names the rule and the document it comes from. Nothing
  ships red.
- **Code decides anything a rule can decide** (statuses, depth, counts, matches, comparisons, verdicts). LLM agents
  only make judgements, and their output must validate against the schema. Never store a value a rule computes.
  Exception: values read from figures and taken from released data are stored in `readings.yaml` and `data.yaml` as a
  checked cache; every audit reruns them and fails on any difference.
- **Gates are code.** An agent may run its gate as a tool while it works, but only the orchestrator's own run of the
  gate counts.
- **Record what was stated.** Values as printed (strings, never floats), verdicts at printed precision; nothing
  corrected, suspected errors labelled. Rebuilt values are labelled *derived by LivingLit*.
- **Flag, never infer.** A stated value that is not one context gets no term; it is flagged back to the record reader.
  No field is filled from another field's text.
- **Papers meet only through matched terms.** No reader or agent writes a link between sources.
- **Libraries grow only through checked edits.** Every synonym is found in a source's text; one parent per term; every
  formula has a kind, given ones are cited and derived ones are proved by code; edits are appended to a log and the
  library is rebuilt from it. Nothing is seeded from an existing curated table.
- **Everything is rebuildable from files.** Records, mappings, derivations, vocabulary and formulas are YAML under
  version control, not a database.
- **Generic core.** Nothing field-specific in code; field content (vocabulary, formulas, standing keys) lives in
  `fields/<field>/`.
- **Figure digitization is bespoke to each figure.** A reader writes the code that reads a figure; it is kept in the
  record (`records/<paper>/figures/*.py`, indexed by `figures.yaml`) and every audit reruns it.
  `src/livinglit/figures/` offers shared parts only (vector objects, raster masks and blobs, axis calibration,
  intervals, overlays) and never holds a crop, page, colour, group label or axis range (a test guards this). Values
  read by eye are never results.

## Working here

- Every test function needs a docstring that states its rule in one sentence and cites its source, e.g.
  `(02-audit, Anchors and origins)`, `(03-vocabulary, Mapping, and flags)` or `(CONTRIBUTING, Fixed rules)`;
  collection fails otherwise.
- Tests that need the papers are marked `@pytest.mark.papers` and skipped when `papers_dont_ever_commit/` is absent.
  Logic is tested on synthetic fixtures that contain no paper content.
- Text is extracted from PDFs with poppler's `pdftotext`, from .docx with python-docx; datasets (.xlsx) are read with
  openpyxl. Nothing extracted is written to disk.
- A field's source review or curated table is never shown to the agents, and nothing from it enters `fields/`.
- Paths under `runs/` and `archive/` in the design documents refer to working notes that are not part of this
  repository.
