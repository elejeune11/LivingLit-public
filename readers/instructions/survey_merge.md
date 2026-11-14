# Survey merge agent · instructions `survey_merge_v1`

You read every `survey/<paper>.yaml` and name each condition tagged `no field`, so that code can count how many papers state
the same condition (spec: `docs/minimalist_design/03-vocabulary.md`, *Fields are designed from the corpus*). This is the one
judgement in the survey: which wordings are the same condition. Code counts and applies the rule; you decide nothing else.

Write `survey/merge.yaml`:
```yaml
names:
  <paper>: {<index of the condition in that paper's list>: "<condition name>"}
```
- Give the same name to conditions that are the same kind of experimental setting (e.g. "cyclic stretch" for "stretched
  cyclically by 10 %" and "uniaxial cyclic strain"); the values stay in the papers.
- A name is a short noun phrase for the setting, not its value ("assay oxygen", not "5 % O2").
- Every `no field` condition gets a name; `livinglit survey tally` fails otherwise.
- Never open `records/`, `archive/`, `docs/archive/` or `papers_dont_ever_commit/_benchmark/`.

Report back in under 10 lines: how many names, and the names you were least sure of.
