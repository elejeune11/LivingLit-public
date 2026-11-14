# Survey agent · instructions `survey_v2`

You survey one paper for the field survey (spec: `docs/minimalist_design/03-vocabulary.md`, *Fields are designed from the
corpus, before it is read*). You write `survey/<paper>.yaml`. You do not write a record.

## Never
- Open `archive/`, `docs/archive/`, `docs/minimalist_design/examples/`, any `records/`, or `papers_dont_ever_commit/_benchmark/`.
- Write paper text anywhere. Read PDFs with `pdftotext -layout <file> - | sed -n '…'` (piped, never saved).

## What to write
Read the methods section and every figure legend (nothing else). List every experimental condition the paper states: how
cells were made, matured, cultured, loaded, stimulated, treated and measured (e.g. "paced at 1 Hz from day 7", "Tyrode's
solution with 1.8 mM Ca", "37 °C", "cyclic stretch 10 %").

Not conditions, and not listed: how data were analysed or reported (statistics, normalisation, inclusion criteria,
replicate counts, software, analysis methods), reagent sources and catalogue numbers, and instrument makes unless the
paper compares them.

```yaml
paper: <paper>
conditions:
  - text: "paced at 1 Hz"          # short, worded from the quote: every word and number must be in it
    field: pacing                   # a field of fields/hipsc_cm/field.yaml, or "no field"
    varied: true                    # true when the paper's groups differ in this condition; false when all share it
    anchor: {quote: "...paced at 1 Hz...", where: "Methods, Electrical stimulation"}
```
Before tagging `no field`, read the scope of every field in `field.yaml`: a condition belongs to a field whose scope holds
it, including as a qualifier (an assay oxygen level under `maturation_strategy` or `treatment`, drug concentrations under
`treatment`). Tag `no field` only when no scope holds it. Never invent a field name. `varied` is true only when the paper
compares groups that differ in this condition (two O2 levels, paced vs unpaced); a setting all groups share is false. One
entry per distinct condition; at most 30 words per quote.

## Gate (code)
`livinglit survey gate <paper>` until it passes (quotes found, quotes hold the text, tags are fields or `no field`).

## Report back (under 10 lines)
How many conditions, how many tagged `no field`, how many varied, and any condition you could not place.
