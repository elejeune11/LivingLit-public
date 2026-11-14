# 2017_Shadrin

## Record reader

- **Which bars a printed asterisk joins (Fig. 2g–j, Fig. 4a, b, e).** The legends print thresholds
  (`*p = 0.0026, **p = 0.0005, ***p < 0.0001`) but the bracket end points live only in the artwork, and I could not
  read them reliably from a page render. Where the legend names the reference explicitly (`#p < 0.001 vs. all other
  groups`, `vs. d0`, `vs. 1 week`, `vs. 1MM`) I wrote one pair item per printed pair. Where it does not (panels 2g and
  2i) I wrote one **omnibus** item over the four media groups with `p: not stated` and a note, rather than invent
  pairs. The figures reader can add the pairs. Fig. 4b's four genes carry one mark each, which I did read from the
  panel; Fig. 4a's per-gene marks I left out and kept only the ten per-gene linear-regression P values the legend
  states in words.
- **Fig. 4c and 4e carry marks with no P in their legend.** The Methods state a paper-wide threshold
  ("significance level set to α = 0.05"), so I wrote `significant at α = 0.05 (Methods)` rather than
  *significant, threshold not stated*. The brief's wording ("*P < 0.05 (Methods)") assumes the Methods print an
  operator; this paper prints a level instead.
- **`supplements` is incomplete on purpose.** Supplementary Table 1 gives the full composition of the three media
  (horse serum, B27, vitamin B12, ascorbate, 1-thioglycerol, pen/strep, NEAA, pyruvate, FBS), but it is a table whose
  rows I could not quote as one sentence holding a value's words, and the rule is that a group's set is read as
  complete. I wrote only `aminocaproic acid`, which the Methods state in a sentence. The set is therefore narrower
  than the paper's; a later pass with table-cell anchors should widen it.
- **The cell-free control in Fig. 6c.** A "blank (Cerex frame-only)" group is neither engineered tissue, native
  tissue nor another study, so it cannot inherit nothing the way a benchmark group does. I kept `kind: engineered`
  and wrote every cell-related field as *not applicable* in its own context, which forced the whole context block
  into the unit's four groups and left `units.F6c.context` empty. A fourth group kind (or a "no cells" state) would
  say this better.
- **Repeating the paper-wide block in every unit.** `default_context` may not be overridden by a unit or an
  engineered group, and this paper varies cell line (Fig. 2f), medium (Fig. 2g–j), density (Fig. 3), size (Fig. 5),
  culture (S10) and time (Fig. 1, 2, 4). So almost every field had to be repeated in all 37 units; only eight fields
  survived in `default_context`. This is the open decision in tab 8 and it costs about half of the record's lines.
- **Hes2 in Fig. 2f.** Hes2 cardiomyocytes were bought from VistaGen, so its differentiation, purification and
  dissociation are *not stated*, while H9 and RUES2 followed this paper's protocol. I wrote those fields per group
  rather than at the unit, which is correct but makes the three groups differ in ten fields; code will see confounds
  there that are really "we did not make these cells".
- **Supplementary-figure quotes.** Both extractors turn the "ti", "fi" and "fl" ligatures in the supplement into a
  period ("quantified" → "quan.fied"), so most supplementary legend sentences cannot be quoted. I anchored
  supplementary items on number-heavy fragments (`n=27/30 patches (1/0.5MM) from 9-10`), and in two places the
  printed n itself contains broken words, so the `n.printed` string carries them as extracted with the readable
  version in a note (S14).
- **Regressions (Supplementary Fig. 5C–E).** A regression of 2 Hz force against a 1 Hz twitch property is neither a
  measurement of groups nor a contrast between them. I wrote one item per regression over a single group
  ("cardiopatches"), with the printed equation as a value, R² as `statistic` and the printed P.
- **Statements that are two measures in the same samples.** Fig. 3e's "54% of cells in 71% volume" and the derived
  "~30% larger cells" are stated conclusions from two measurements; I recorded the printed numbers as values
  `between` the two density groups and left the arithmetic to the formula agent.
- **`preparation` wording.** The paper never says "intact tissue"; context anchors must hold their value's words, so
  the functional units use `cardiac tissue patch` and the western/qPCR units `lysis buffer`. A vocabulary agent will
  have to map both onto the intended preparation terms.
- **`genotype` left *not stated*.** The paper calls the BJ fibroblast donor "a healthy male newborn" but never calls
  DU11 a healthy, wild-type or control line, so the declared state `healthy control line` did not apply; the donor
  statement went to `donor_age: newborn` instead.
- **Fig. 1a's day.** The text says d15–21, the legend "after 20 days of differentiation". I kept d15–21 (the text
  states it for the cells that were used) and did not record the legend's 20 days as a second context value.
- **Left out.** The uncropped blots (Supplementary Fig. 19), the representative images, movies and schematics carry
  no measurement; the arrhythmia table (Supplementary Fig. 18A) is a grid of per-attempt durations inside an image,
  of which I recorded only the counts the main text prints.

## Figures and data reader (F1g)
- No released data: the supplementary files are the reviewer file and the description of movie files, with no tables.
  Fig. 1g is read from the vector PDF (page 3).
- Fig. 1g is a bar chart (mean with only the upper SEM bar drawn) with no individual points, so it gives no counts
  (`countable: false`) and nothing to check against n = 8/11/12.
- Read means: w1 17.03, w2 11.63, w3 8.078 %. Upper SEM ends: 17.68, 12.90, 9.235, so SEM ≈ 0.65 / 1.27 / 1.16. These
  agree with the printed 17.0 ± 0.7 (w1) and 8.1 ± 1.1 (w3). No value is printed for w2.
- Each week's bar is returned under one label per comparison item it enters (six labels, three distinct bars),
  because a figures.yaml label links to one item.
- The pairwise Tukey P values stay unchecked: post hoc pairs are checked from points only, and the panel has none.

## Figures and data reader (F1i)
- No released data hold these values; Fig. 1i is read from the vector PDF (page 3). Panel h is images only.
- Fig. 1i is a grouped bar chart (orange MLC2a+2v, green MLC2v, matched to the legend squares by fill) of mean with
  only the upper SEM bar drawn; no individual points, so no counts (`countable: false`) and nothing to check against
  n = 7/5/4.
- Read means, MLC2v: w1 43.57, w2 89.45, w3 94.21 %; MLC2a+2v: w1 56.59, w2 10.71, w3 5.788 %. Each week's pair sums
  to 100 ± 0.2 %. MLC2v at w3 agrees with the printed 94%.
- The y tick labels are printed 33% and 67% on equally spaced ticks (i.e. thirds, rounded). I calibrated on the
  labels as printed; the resulting misfit (about 0.25 points) is added to every interval rather than replacing the
  labels with 33.3/66.7.
- The legend's single P (*p = 0.0002 vs. 1 week) is attached by the record to all four comparisons; the stars on the
  figure sit over both series at 2 and 3 weeks, consistent with that. Pairwise Tukey P values stay unchecked (no points).

## Figures and data reader (F2b)

- Fig. 2b (page 4) read as vector: two bar charts (max active force, mN; specific force, mN/mm2), 1/2/3 weeks,
  mean + upper SEM bar. No individual points, so no counts against the printed n = 6 patches; no released data
  (the supplementary files are PDFs only).
- Weeks are identified by fill colour matched to the legend squares (legend sits beside the specific-force chart
  and is taken to cover both charts, which use the same three fills).
- Readings agree with the printed text: force 1.17 (+0.26) vs 1.2 ± 0.3 mN at 1 week, 3.94 (+0.24) vs 3.9 ± 0.2 mN at
  3 weeks; specific force 2.92 (+0.57) vs 2.9 ± 0.6 and 13.34 (+0.99) vs 13.3 ± 1.0 mN/mm2. The 2-week values
  (3.28 mN, 10.1 mN/mm2) are not printed.
- Pairwise Tukey P values stay unchecked: the audit does not recheck post hoc pairs from bars alone.

## Figures and data reader (F2e)
- No released data: the supplementary files are PDFs, so Fig. 2e (CV at 1/2/3 weeks) is read from the vector chart
  (page 4, crop [317, 200, 410, 325]); mean bars and upper SEM caps only, no individual points, so no counts against
  n = 7/7/9.
- Error-bar caps are found by shape (thin stem + short cap, centred); the x axis' two end ticks form a drawing of
  the same item count and are kept out by that shape test.
- Readings agree with the printed text: 3 weeks 25.08 (+1.25) vs 25.1 ± 1.3 cm/s. The 1- and 2-week means (13.42,
  23.65 cm/s) are not printed in the text. Panel d's "CV=13/21/25 cm/s" belong to representative maps, not means,
  and are not read.
- Pairwise Tukey P values stay unchecked (post hoc pairs are checked from points only); directions are now computed.

## Figures and data reader (F2gj)
- No released data (supplementary files are PDFs). Fig. 2g–j (page 4, crop [55, 335, 530, 525]) read as vector: four
  bar charts (max active force mN, specific force mN/mm2, CV cm/s, APD80 ms), mean + upper SEM bar, no individual
  points, so no counts against the printed n = 15/14/13/14 (force) and 15/15/14/15 (optical mapping).
- Groups are named from the rotated x-axis labels: the "(dN–21)" word aligned with each bar's right edge, and the
  word printed before it ("RB+" vs "FBS") separates 3D RB+ (d0–21) from 5% FBS (d0–21). Fill colours agree across
  panels but are not used.
- Readings agree with the printed text for 5% FBS (d7–21): 4.67 (+0.28) vs 4.7 ± 0.3 mN; 15.14 (+0.90) vs
  15.2 ± 0.9 mN/mm2; 25.85 (+0.76) vs 25.8 ± 0.8 cm/s. Other groups are not printed.
- Brackets the record left open (end points read from the bracket drawings, not stored as items): panel g, *** over
  3D RB+ – FBS d14, *** over FBS d14 – FBS d0, * over 3D RB+ – FBS d7; panel h, ** over FBS d14 – FBS d0 and # over
  3D RB+; panel i, *** over FBS d14 – d7, 3D RB+ – d7, FBS d14 – d0 and 3D RB+ – d0; panel j, # over 3D RB+.
  Panel g carries * and *** but not **, and panel h carries the ** bracket, so the legend's "*p = 0.0026,
  **p = 0.0005, ***p < 0.0001" spans panels g and h. These pairwise items are absent from the record (record
  reader to add if wanted).
- Panel g's FBS d14 bar (5.73 mN) is the highest force, not the d7 group the text singles out; read as drawn.

## Figures and data reader (F3bde)
- Read panel e (vector bar chart, Norm. cell number, mean + upper SEM bar): 0.5MM 0.544 (printed "54%"), 1MM
  0.9997 (the normalising group, drawn with its own SEM bar to 1.071). No individual points, so no counts against
  n = 13/16 patches; no released data (the supplementary files are PDFs).
- The axis is a fraction (0–1.2) while the record prints the result as a percent ("54"); unit_of_value is the
  axis label as printed.
- F3e_volume (71%) and F3e_cellsize (~30%) are not plotted in Fig. 3 (panel e shows cell number only), so they
  have no reading; both are text-only values without spread. Panels b and d were not read: their means ± SEM are
  printed in the Results.

## Figures and data reader (S9)

- Supplementary Fig. 9 (MOESM1 p. 9) is vector: panels B (relaxation time) and C (twitch duration) were read as
  bars of mean + upper SEM end; no individual points, so no counts against n=27/30. No released data exist.
- Panel A (rise time) was not read; its means and SEMs are printed in the Results. As a check (not stored), its bar
  tops calibrate to ~107.8 ms (orange, 1MM) and ~98.2 ms (blue, 0.5MM), which match the printed 107.6 and 98.0.
  This confirms the legend's colour-to-group mapping.
- Read values: relaxation 262.7 (1MM) vs 265.9 ms (0.5MM); duration 535.2 (1MM) vs 523.2 ms (0.5MM). The legend
  prints P only for panel A (*p=0.0055); B and C carry no asterisk and no P.
- Panel C's tick labels (0/200/400/600) are not exactly evenly spaced on the page (32.7/32.7/32.4 pt); the
  calibration misfit is added to every interval.
- The PDF's text layer appends "!" to tick labels, so the script parses them itself instead of using tick_marks.

## Figures and data reader (F4a)

- Fig. 4a (p. 6) is a vector bar chart on a log axis (0.0001–1.0000): 10 genes × d0/1wk/2wk/3wk = 40 bars, each read
  as mean + upper error-bar end (80 readings). No individual points, so no counts against n = 6 patches. The legend
  does not say whether the error bars are SD or SEM. No released data hold these values (the supplements are PDFs).
- Bars are assigned to weeks by their order within each gene. The 2wk bars of MYL2 and MYOM2 are a different blue
  (0.26, 0.46, 0.89) from the legend's 2wk square (0.33, 0.56, 0.84), so the script only checks that they match
  none of the other three fills.
- Only the left section (structural genes) has y ticks. The middle and right sections' x-axis lines sit 0.40 pt
  below and 0.29 pt above the left one. Values use the left calibration, and intervals are widened by that offset.
- Two error bars (MYOM2 d0, CASQ2 3wk) are shorter than their caps are thick; they are read from the cap centre.
- The dashed "LV" line is drawn at about 0.83 on the axis, not at 1.0, although the axis is "Expression rel. to LV".
  It is not read as a value.
- Checks against printed text (not stored): 3-week/d0 ratios of the bar means run from 2.8 (CKM) to 111.5 (MYL2),
  median 23.9; the text prints 3- to 163-fold, median 23. MYL2 reads 111.5 vs printed 108 (close on a log axis).
  CASQ2 reads 80.5 vs printed 163-fold, a mismatch (the text also cites Supplementary Fig. 11A; not resolved here).
  PLN at 1–3 weeks reads 0.48–0.61 of LV vs printed "55–70% of adult heart levels" (0.58–0.73 if taken relative to
  the drawn LV line at 0.83).
- F4a_fold_range (groups w3, d0) pools all genes and has no single bar. It is linked to no reading, so it stays in
  `figures-needed`.

### F4b (Fig. 4b)
- Read from vectors: 8 bars (MYOM3, CASQ2, S100A1, COX6A2 × 0.5MM/1MM), mean + upper error bar; no points, so no
  counts (printed n = 6 patches from two differentiations). The panel legend names no error type (the figure legend
  says mean ± SEM only for other figures), so the error bar is stored as an upper end only.
- The 1MM reference bars read 0.9997 (all four) and carry their own error bars (upper ends 1.06–1.09).
- 0.5MM reads 1.41 (MYOM3), 1.68 (CASQ2), 1.70 (S100A1), 1.50 (COX6A2); no printed means to check against. The
  star placement in the figure (* MYOM3, *** CASQ2, ** S100A1, * COX6A2) agrees with the record's p strings.

### F4ce (Fig. 4c, e)
- Read from vectors: panel c (protein/DNA, 1MM and 0.5MM) and panel e (βMHC, SAA, Cx43, GAPDH relative to LamB1 ×
  1MM/0.5MM): 10 bars, mean + upper error bar (20 readings). No points, so no counts against printed n = 3/4
  (c) and 8/10 (e) patches. The panel legend names no error type.
- Panel c has no legend of its own. Its red and blue bars are named 1MM and 0.5MM from panel e's legend fills.
  The 1MM bar reads 1.00, which fits it being the reference.
- Panel e's d0 bars (white) enter no item and are not returned. Panel d (western blots) has no values. Its row labels
  repeat the protein names left of panel e and are excluded by x position.
- Checks against printed text (not stored): protein/DNA 0.5MM reads 1.122 vs printed 13% higher (12.2%). GAPDH reads
  1.331 vs 33%, SAA 1.715 vs 1.7-fold, βMHC 1.422 vs 1.4-fold and Cx43 1.300 vs 1.3-fold. All 1MM bars read 1.00.

## Figures and data reader (S11)

- Supplementary Fig. 11 (MOESM1 p. 11) is vector: two rows (A rel. to d0, B rel. to monolayer) of three grouped bar
  charts, 10 genes × 2 groups per row = 40 bars, each read as mean + upper SEM end (80 readings). No individual
  points, so no counts against n=6 cardiopatches/monolayers. No released data hold these values.
- The gene names under the bars are glyph outlines, not text, so code cannot read them. The script fixes the printed
  left-to-right order (TNNI3, MYL2, MYOM2, MYOM3 | CASQ2, S100A1, PLN | COX6A2, CKMT2, CKM; the order of
  Supplementary Tables 3–4) and asserts each axis has exactly that many category slots, each with one bar per group.
- Each item (S11_patch_vs_d0, S11_patch_vs_mono) covers all ten genes, so ten figure labels feed each (item, group).
  The shared checks keep one mean per group (the last label read), so the computed direction rests on one gene; all
  ten genes go the same way here, so the direction is not affected. Per-gene items would need the record reader.
- Reference bars: d0 reads 0.95–1.25 and monolayer 1.00–1.02 (normalised to 1, read on 0–140/0–250/0–40 and 0–12/
  0–4.5/0–4 axes). Several d0 error bars have zero-length stems (SEM below drawing precision).
- Checks against printed text (not stored): MYOM2 patch/monolayer reads 10.3 vs printed 10-fold; the other nine
  genes read 2.77–3.83 (mean 3.14) vs printed "average 3-fold". CASQ2 patch/d0 reads 162.9, which matches the 163-fold
  that the text gives for CASQ2 and attributes to Supplementary Fig. 11A. This explains the F4a mismatch noted above:
  the 163-fold is relative to d0 in this figure, not taken from Fig. 4a.

## Figures and data reader (S12)

- Supplementary Fig. 12B (MOESM1 p. 12) is vector: one grouped bar chart, 3 proteins × 2 groups = 6 bars, each read
  as mean + upper SEM end (12 readings). No individual points, so no counts against n=4 cardiopatches per group. No
  released data hold these values. Panel A (blots) has no values.
- The protein names under the bars are glyph outlines, not text; the script fixes the printed order (Akt, mTOR,
  AMPK, seen on a render and matching the legend's "Akt, mTOR, and AMPK") and asserts three category slots.
- Read values: Akt 1.336 (0.5MM) vs 0.999 (1MM); mTOR 0.991 vs 0.999; AMPK 1.066 vs 0.999. The 1MM reference bars
  sit on the "1" tick line; they read 0.9989 because the tick lines are not evenly spaced (23.2–23.6 pt) and the
  least-squares misfit (~0.004) shifts them; that misfit is added to every interval.
- Only Akt carries an asterisk; the record gives mTOR and AMPK p "not stated", so the audit computes a direction
  for S12_Akt only.

## Figures and data reader (S14)
- No released data for this unit (the supplementary files are PDFs); Supplementary Fig. 14B is read as a vector
  grouped bar chart (mean + upper SEM bar, no points, so no counts against n=5 patches / n=2 d0). Panels A (blots),
  C and D (images) have no values.
- The d0 bars and legend square are unfilled outlines and the patch ones blue fills; the script tells them apart by
  whether a fill is drawn at the same rectangle, and names categories from the JPH2/Cav3 words under the slots.
- Read values: JPH2 0.817 (patch) vs 0.167 (d0); Cav3 0.392 vs 0.021. Cav3 d0 is a 1.6 pt high bar with a 0.65 pt
  error stem, so its value is close to the 0.5 pt interval.
- No printed means to check against; the main text cites the figure only for upregulation. Both bars carry "**",
  matching the record's p for both items.

## Figures and data reader (S5b)
- Panel read: Supplementary Fig. 5B (supplement p. 5), vector line plot of mean force normalised to 1 Hz at 1, 1.5
  and 2 Hz, mean ± SEM error bars at 1.5 and 2 Hz. No individual points, so no counts against N=61; no released
  data for this panel (MOESM2/3 not used for it).
- Means are the vertices of the single black polyline, assigned by the frequency label under each slot; the upper
  cap of each error bar is the error reading. The 1 Hz point has no error bar (normalisation reference); its read
  mean is 0.999, the calibration's misfit around the printed 1 tick.
- Read vs printed: 1.5 Hz 0.952 (printed 95%), SEM from the upper cap 0.0066 (printed 0.8%); 2 Hz 0.829 (printed
  83%), SEM 0.0192 (printed 2.0%). The axis is a fraction; the record prints %.
- The error bars are not quite symmetric about the mean (1.5 Hz: 0.65 pt above, 0.85 pt below), so the upper cap
  gives a SEM a little smaller than printed; nothing adjusted.
- The x labels are printed "1Hz", "1.5hz", "2Hz" (lower-case h at 1.5).
- Panels A (traces) and C–E (2 Hz force vs twitch timing scatter, units S5ce…) are not part of this job.

## Figures and data reader (F5ef)
- No released data hold these values (the supplementary files are PDFs), so they are read from the figure.
- Fig. 5e (CV) and 5f (APD80), p. 7: vector bar charts of mean ± SEM (upper bar only drawn); no individual
  points, so no counts against n = 11 (ctrl). Only the Ctrl bars are read: CV 27.26 cm/s (SEM cap 27.98), APD80
  466.1 ms (cap 489.4). No ctrl value is printed in the text to check against.
- Check of the calibration (not stored): the hatched Mega/Giga bars measured the same way read about 27.15/28.86
  cm/s and 447.7/471.3 ms, which agree with the printed 27.2 ± 1.1 / 28.9 ± 1.8 cm/s and 447 ± 22 / 471 ± 31 ms.
- The record gives n = 11/6/7 for CV and 11/6/5 for APD; the figure prints no n of its own.
- Panel d (activation maps with colour bars) holds representative patches only and enters no item.

## Figures and data reader (F5hi)
- No released data hold these values (the supplementary files are PDFs), so they are read from the figure.
- Fig. 5h (max active force, norm.) and 5i (specific force, norm), p. 7: vector bar charts of mean ± SEM (upper
  bar only drawn), normalised to Ctrl; no individual points, so no counts against n = 10/6/10. Read means (SEM
  cap): h Ctrl 1.001 (1.049), Mega 1.785 (1.876), Giga 4.373 (5.088); i Ctrl 1.000 (1.050), Mega 0.926 (0.972),
  Giga 0.963 (1.119). Ctrl reading 1 in both panels checks the calibration.
- Mega and Giga bars are hatched outlines; their tops are taken as the centre of the outline's top stroke (half
  stroke measured from the solid Ctrl bar). The stroke is 0.72 pt, within the interval.
- The Results print absolute forces 4.6 ± 0.6, 9.4 ± 1.0 and 17.5 ± 1.1 mN (ctrl/Mega/Giga), whose ratios
  (2.04, 3.80) differ from the normalised bars (1.79, 4.37). Not an error by itself: the bars are presumably
  normalised per differentiation or per batch, which the legend does not say; noted for whoever compares them.

## Figures and data reader (F6c)
- No released data hold these values (the supplementary files are PDFs), so they are read from the figure.
- Fig. 6c (BVD, A.U.), p. 8: vector line plot of mean ± SEM (both caps drawn), cardiopatch (square) and blank
  (diamond) at d7 and d14; no individual points, so no counts against n = 15 patches / 3 blanks. Read means
  (SEM upper end): patch d7 0.267 (0.279), d14 0.409 (0.421); blank d7 0.262 (0.277), d14 0.317 (0.344).
  The y axis starts at 0.2, not 0.
- The two d7 error bars overlap at the same x; each is given to the marker nearest its midpoint (both bars are
  symmetric about their marker to < 0.1 pt).
- Mismatch: the Results print a "1.6-fold increase" in BVD from d7 to d14; the plotted patch means give
  0.409 / 0.267 = 1.53. Possibly a mean of per-patch ratios, which the text does not say; not corrected.
- The items' tests (repeated measures ANOVA, Tukey post hoc) cannot be rechecked without points.
- Panel b (images) holds no values.

## Figures and data reader (F6h)
- No released data for Fig. 6h (the three supplementary PDFs hold no tables); read from the vector figure.
- Panel h (figures/F6h.py): two mean markers (green diamonds) ± SEM, d7 1.001 (error top 1.134), d14 1.264
  (error top 1.413), axis "dF/F (norm.)". No individual points, so no counts against the printed n = 12 patches.
- The axis is normalised but the legend does not say to what; d7 sits at 1.00, so d7 is likely the reference, yet it
  carries its own SEM bar. Read as printed; not reinterpreted.
- The record's finding says amplitude was "stable" (p = 0.2, ns); the plotted d14 mean is ~26% above d7. Not a
  contradiction (ns), noted only.
- The paired t-test cannot be rechecked from group means and SEMs (pairing unknown); the audit reports cannot check.
- Panel g (images, time trace) has no group values.

## Figures and data reader (F7f)
- No released data hold these values (the ESM files are PDFs). Panel f is a vector bar chart of mean ± SEM, upper bar
  only, no points: 6 bars read (CV and APD80 × Ctrl/Under/Away), no counts (printed n = 6/3/3 hearts).
- One y axis serves both measures, printed "CV (cm/s) or APD80 (ms)"; CV is recorded in cm/s and APD in ms. The x-axis
  word is "APD" while the axis label says APD80; the record's measure says "action potential duration".
- The Under/Away hatched fills are embedded images. Bars are named by matching each bar's hatch diagonal to the legend
  swatches on a render (a check only; no value comes from the raster).
- The Under-patch APD bar's outline is inside an embedded image; its top is the bottom of its vector error stem, which
  sits within 0.1 pt of the outline midline on the five vector bars; a dark outline row on the render is required there.
- Reads: CV 54.5 / 58.7 / 51.2 cm/s, APD 77.1 / 84.9 / 86.9 ms (Ctrl/Under/Away). No test or p is stated, so the
  audit has nothing to check against ("cannot check").

## Vocabulary agent

- **Quantity parser gap (code, not the reader).** `matching.quantity_value` does not read a day printed as `d3`, `d7`
  or `d0` (its look-behind refuses a digit after a letter); `d15–21` and `d14 post implantation` parse only because
  a later digit follows a non-letter. A quantity field takes no terms, so the only way through the gate was a flag:
  `wnt_inhibition_days 'd3'`, `insulin_day 'd7'`, `day_of_measurement 'd0'` and `time_point 'd7 post implantation'`
  are flagged *not a context* as stand-ins. They are valid values; fix the parser, then drop these four flags.
- `time_point 'pre-implantation'` is flagged: a word that is neither a number nor the declared state *baseline*. The
  reader may restate it as *baseline* if the paper means the measurement before implantation (Fig. 7e).
- `hipsc_medium 'TeSR-E8 or mTeSR'` flagged *alternatives* (the paper used E8 for one protocol, mTeSR for the other).
- `cm_medium 'cardiac medium'` flagged *placeholder*: the paper's generic name for whichever medium of Supplementary
  Table 1 was used. The reader should state the regime (most units are probably the 1-week 3D RB+ then 2-week 5% FBS
  regime chosen after Fig. 2g–j, but the value does not say so).
- `cm_medium` regimes: '1 week 3D RB+, 2 weeks 5% FBS' (TXT1) and '3D RB+ d0–7, 5% FBS d7–21' (S11) are the same
  regime in two wordings; code's wording-copies check may send them back. '5% FBS (d14–21)' and '(d7–21)' name only
  the FBS period; the 3D RB+ period before it is not in the value. 3D RB+ mapped to RPMI 1640 and 5% FBS medium to
  low-glucose DMEM from Supplementary Table 1 (qualifiers `formulation`, `glucose`, new `days`).
- Measure flags (*several measures*): the three ten-gene summaries ('maturation gene expression relative to d0',
  '... d0 hiPSC-CMs', '... age-matched 2D monolayers') and 'cardiomyocytes with M-bands or T-tubule-like structures'
  (two features; the printed <5% is M-bands only).
- Suspected record mismatch: `F4a_MYL2` and `F4a_CASQ2` carry the measure 'expression relative to adult human left
  ventricle' but their printed values (108-fold, 163-fold) are fold changes against d0. I left `normalised_to` out of
  those two mappings so the values carry their own.
- `F2f_*` items use the plain wordings 'maximum active force', 'specific force', 'conduction velocity' but their
  values are % of the hiPSC-CM cardiopatches; the values should carry `normalised_to`, which the wording cannot.
- `twitch force relaxation time` was matched by code as two measures (twitch force + relaxation time); I stored a
  mapping to relaxation time (level 10 to 90% relaxation). The rise time (10 to 90% activation) went to *time to peak
  force* with that level; neither existing rise term fits a 10–90% window exactly.
- 'cell size' (inferred from cell number and tissue volume) mapped to the new *cell volume*; the paper never says volume.
- 'H9, iPSC' (Supplementary Fig. 5B) mapped to {WA09, DU11}: the paper states that all experiments except Fig. 2f
  used DU11 hiPSCs.
- 'host epicardial action potential duration': the level (APD50/80/90) is not stated, so the mapping has none.
- 'Cerex frame only' mapped to *cell-free control*; 'lysis buffer' (a reagent) mapped to *lysate*; 'implanted
  cardiopatch' mapped to the new *implanted tissue*, with a split request for 'cardiopatch' → platform.
- `F1a` preparation 'dissociated cardiomyocytes': the methods say the dissociated cells were fixed before flow
  cytometry; the value says only dissociated, and I mapped only what it says.
- `pacing 'point stimulation'` carries an occurrence qualifier `rate` ('1–4 Hz'); the pacing tree's qualifier is
  `frequency`. I did not add `rate`.
- DU11 is not in Cellosaurus (pinned): own term `cell_line:du11`. 'non-CMs' has no CL class: own term
  `cell_types:non_cardiomyocyte`. 'aminocaproic acid' adopted as CHEBI:16586 (6-aminohexanoic acid); the pinned
  ChEBI does not list the drug name, so I added it as our synonym.

### Re-map against vocabulary v52 (2026-11-12)

- The stored mappings for 'lysis buffer' (preparation) and 'protein/DNA ratio' (measure) are dropped: code matches
  both now (the first through an earlier synonym, the second through a new synonym anchored in the Methods heading).
- 'maximum active force relative to Ctrl cardiopatch' and 'specific force relative to Ctrl cardiopatch' now carry
  `expressed_as: normalised` (Fig. 5h,i legend: "normalized active/specific force"); 'fold' or '% of baseline' would
  read more into the axis than is printed.
- Still open: the `d3`/`d7`/`d0`/`d7 post implantation` stand-in flags (the quantity parser still leaves these
  unmapped); 'RUES2 hESC' and 'spontaneous contraction rate' get no synonym because neither wording is in the paper's
  text as printed (the paper writes "RUES2 and H9 hESCs"; the rate wording is the reader's).
- 'H9, iPSC' → {WA09, DU11} is still a reading of the paper's own statement that every experiment but Fig. 2f used
  DU11; if that counts as filling the field from elsewhere, the reader should write the line name instead.

## Formula agent

- **Force per input CM (Fig. 3g) does not rebuild from seeded cells.** Force over the seeded cell count (Methods:
  1 × 10^6 / 0.5 × 10^6) gives 5.8 and 10.4 nN against printed 6.7 and 11.9. Both printed values are about 1/0.863
  of the rebuilt ones, i.e. N × the cTnT+ fraction (86.3 %, F1a). The definition is by citation (ref 24), so I wrote
  F/N as stated and that reading as a labelled alternative. Code flags mm05 inconsistent; mm1 passes only because
  the printed "1 × 10^6" carries a wide interval.
- **CASQ2 163-fold (Fig. 4a, Suppl. Fig. 11A).** The anchor cites both panels. The Fig. 4a bars (relative to LV)
  give w3/d0 ≈ 80; the Suppl. Fig. 11A patch bar alone reads 163. MYL2 agrees in both (≈ 111–113 vs 108). I wrote
  one derivation per panel. The S11 d0 bars do not read 1 (0.95, 1.25), and one has a read interval that crosses
  zero (rebuilt interval [-593, 130]). That looks like a log-axis reading problem for the figures reader.
- **Specific force (8 groups) and stiffness have no printed area.** The Methods say only "cross-sectional area of the
  patch". A is `not_stated`, per sample, so code cannot check any of them. Stiffness is a slope of tension against
  strain divided by area. I did not map it to stress_def (a slope is not a force). It is `no_formula`, and I proposed
  no tangent-modulus entry.
- **Relative volume (71 %) is a thickness ratio** only if both patch sizes have equal area (both 7 × 7 mm molds). The
  paper does not say how volume was obtained. Recorded as an alternative.
- **Relative cell number (Fig. 3e).** n = 13/16 differs from the thickness (22/25) and count sets. Whether thickness ×
  cells was formed per patch or from group means is not stated. aggregation: not stated; only of-means can run.
  Proposed `ratio_of_products` (derived from ratio_def) for it.
- **Fig. 5h, i vs TXT2.** The TXT2 means (4.6/9.4/17.5 mN) are "for this set of experiments". Fig. 5h, i are from
  patches "derived from the same input cells". 17.5/4.6 = 3.8 against a read 4.37, so I did not chain TXT2 into
  the normalised panels. Their inputs are not stated.
- **"In 75% of attempts … in both"**: pooled (76/102 = 74.5 %) or per group (74.1 %, 75.0 %). Pooled was written;
  per group is the alternative.
- **Median, range and "average 3-fold over 9 of 10 genes"** have no library reduction (median, min/max, mean over a
  subset). They are `no_formula`; the S11 readings reproduce them (median 22.7, mean of nine ≈ 3.1).
- Conduction velocity is computed by cited software (ref 66), so it is `no_formula` and goes on the completeness
  list. For the in vivo / ex vivo CVs (F7e, F7f) the computation is not stated at all.
- Gate: the spec says an input from a reading on a curve names `x`. S5b's readings carry no x even though the panel
  is a force–frequency curve: the reader keyed the groups by frequency instead.
