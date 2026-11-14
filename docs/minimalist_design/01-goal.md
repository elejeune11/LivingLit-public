# 1 · The goal

LivingLit audits each paper against itself and lets papers meet only where code can say they match. It checks **consistency**.

## The problem

**Checking a paper against itself.** Claims rest on results and results on statistics, but the links are made in prose. An abstract can claim an effect its own test does not support; a legend can give an n its data do not have; a force can be derived by a formula that doubles it. A full check of one paper takes hours of expert time, so it is rarely done for a literature.

**Comparing papers.** Papers describe the same thing in different words ("3D CMT", "cardiac microtissue on a micropillar array") and different things in the same words (two "forces" built two ways). Reviews compare them by reading, and Ewoldt et al. (2025) found most values in their 300 studies could not be compared at all. An LLM can read the papers, but what it writes when it compares them is text, not a check: recent evaluations find LLMs near expert accuracy at extracting single values, and unreliable at combining evidence across studies and at citing it faithfully.

## What we build

1. **The audit**, one source at a time: a reader writes an anchored record, and code that reads values from figures where no data were released; code checks both; the reader judges each stated claim against its own evidence.
2. **Mapping and derivations**, in two short jobs per source: a vocabulary agent ties each stated context (of a unit or a group) to terms of a controlled vocabulary and extends the vocabulary when nothing fits; a formula agent writes each derived quantity's derivation, reports what the paper says about each model's assumptions, and extends the formula library when nothing fits. Code checks every edit.
3. **Matching**, by code only: items meet when their terms match under a standing key, and code computes comparisons, coverage and independence.
4. **A release:** versioned, documented tables. Whatever is built on them (search, synthesis, hypotheses) is built outside and cites them.

## Three kinds of statement

Kept apart, so that software never mistakes one for another:

| Kind | In LivingLit | World | Example |
| --- | --- | --- | --- |
| **Formulas** (the theory) | the formula library (definitions, models, bounds, derived formulas); the vocabulary's hierarchy | general, tested against records | tension in a two-post tissue equals the force on one post |
| **Statements with evidence** | evidence items and stated claims: the printed value (cannot be wrong) and its interpretation (can be: measure, context, contrast, condition) | open: what one source reports; what it does not state is unknown | "twitch stress 12 ± 3 mN/mm² at 1 Hz", anchored, mapped to terms |
| **Constraints** | gates on records: anchors found, fields of the record's field set filled or *not stated*, mappings complete, edits valid | closed: the record as it stands | every value has an origin |

A statement never becomes a formula by being repeated. A formula is checked against statements; a statement is checked against its own source and the formulas; a constraint is checked against the record.

## Principles

1. **The audit is the product.** Each source parsed and checked well is the contribution; everything else is computed from it. Units (usually one figure each) let a single figure stand alone as a contribution.
2. **Record what was stated.** Claims quoted, values as printed; a suspected error is labelled, never an edit.
3. **Everything anchored, every value with an origin:** *stated*, *from data*, *read* (with method and uncertainty), or *derived by LivingLit*. Context values too: each distinct stated value carries one quote.
4. **Three kinds of statement, kept apart:** formulas, statements with evidence, constraints.
5. **Never blur who said what:** stated, read, derived, matched by code, assigned by an agent, flagged; each labelled wherever it appears.
6. **Recompute, don't trust,** at printed precision or within reading uncertainty.
7. **Say how deep the check went.** Every item reports its status and depth. Depth is limited by released data far more than by checks: asking for data comes before adding checks.
8. **Papers meet only through matched terms.** Code makes every edge; no LLM decides that two sources are related.
9. **Compare only what is comparable;** *not comparable* is a result, with the field that differs named.
10. **Flag, never infer.** A value that is not one context goes back to its reader; completeness is a named premise, never assumed.
11. **Open world for statements, closed world for constraints.** What a source does not state is unknown, never false: *not stated*, *not yet read*, *not stated in this source* and *by reference* are unknowns. A comparison that depends on an unknown is still computed, and names what it assumes; a field known to differ makes a pair *not comparable*. Gates stay closed-world over the record as it stands.
12. **Disagreement is a result,** recorded and shown, never edited away.
13. **Everything can be rebuilt; nothing is overwritten.** Files under version control; releases tagged.
14. **Nothing about a field is built in;** fields add vocabularies and formulas.
15. **LLMs assert, code checks.** What a rule can decide, code decides. Agreement between readers is not correctness.
16. **Exploration lives outside.** Search, synthesis and hypotheses are built on a release and cite it; nothing written there enters it.

## Who asserts, who checks

| Step | Asserted by | Checked by |
| --- | --- | --- |
| Record from a source | reader | code: every quote and value found at its anchor |
| A value stated only by citation | reader marks it by reference, with the citation | code: resolves the citation and lists a cited paper outside the corpus as needed for completeness |
| Values read from figures | reader, by code it writes for each figure | code: reruns the script on every audit; uncertainty calibrated on panels with known data |
| Statistics, repeated values, values against data or readings | computed | code |
| Status and depth | computed by rule | code |
| Stated claim against its own evidence | reader, dimension by dimension | code: the verdict is the worst dimension; a judged direction opposite to the computed one is flagged |
| Context of units and groups as terms | code (synonym match), else the vocabulary agent | code: terms exist, flags respected; re-map agreement at checkpoints |
| New terms and synonyms | vocabulary agent | code: anchored in the source, no collision, one parent |
| Derivations | formula agent writes the paper's formula and reports its models' assumptions | code: checked against the formula library, recomputed, dimensions |
| New formulas | formula agent | code: a kind; cited if given, proved if derived; tests, no contradiction, corpus sanity |
| Comparisons, coverage, independence | computed | code, under standing keys |

## Where things belong

| If it is… | It belongs in |
| --- | --- |
| the same in any field | LivingLit's rules (code) |
| what one source reports, or a check of it | its record |
| a field's terms, standing keys and formulas | `fields/<field>/` |
| a comparison, a coverage count, an independence check | computed from records, in a release |
| a synthesis, a hypothesis, an answer to a question | outside, citing a release |

## Designed, not yet built

The design keeps these; the code does not do them yet (open item in [tab 8](08-trials-and-decisions.md)).

- Values stated *by reference* are carried from the cited record when that paper is in the corpus (today code resolves the citation and lists cited papers outside the corpus). Deferred: in release run-2026-11-12, 1 of 1,541 values stated by reference cites a paper in the corpus; they cite protocol papers outside it, which the completeness list ranks.
