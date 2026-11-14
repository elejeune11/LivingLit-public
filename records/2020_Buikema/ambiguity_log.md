## Record reader

- **Passages and days as levels of a number.** Fig. 1B, 2C, 2E, 2H, 2J, S1D and S1E plot a quantity against
  passage number (P0–P5), and Fig. 3I–3K against day (D28–D49), with an asterisk over individual points.
  02-audit says a level of a number inside one experiment is its own group, but the passage and day labels sit
  only in the figure images (the text anchors P0, P2, P4 and P5 but not P1 or P3, and names no day for the
  qPCR time courses), so a group per level could not be anchored. I kept treatment groups and wrote one item
  per panel, with the per-point marks collapsed into the legend's thresholds (`p` plus `p_values`). The
  per-passage and per-day comparisons are therefore not separable in this record.
- **Asterisks the legend does not define.** The Fig. 1 legend defines only `*p < 0.05` and `****p < 0.001`,
  but Fig. 1D marks a pair `***` and Fig. 1F marks two pairs `**`. The Fig. 4B legend states
  `****p < 0.0001` while the panel marks `***`. I wrote the Methods' paper-wide threshold with its source
  (`P < 0.05 (Methods)`) for the undefined marks, and logged each mismatch as a `suspected_error` on the item
  rather than choosing a level.
- **Which pair an asterisk over a bar means.** In Fig. 3E, 5C, 5D, 5K and S3C/E/G an asterisk sits over a
  treatment bar with no bracket, in panels with one obvious control (CTR, or t=0 for the kinase array). I
  recorded those as pairs against that control; the paper never prints the pair. Where a mark spans a group
  cluster with no control (Fig. 3G, 3H, 4E, 4G) I used `test_of: omnibus` instead.
- **Fig. 3G/3H print two time points (D28, D42) in one panel with a single NS.** I recorded one omnibus item
  per measure at the unit's stated day (D42 from the Fig. 3F legend) and did not split the time points.
- **Fig. 3I–3K statistics.** The panels carry asterisks but the legend's test sentence (`unpaired t test`)
  does not say against which curve. I recorded these as measurement items over the three treatment groups and
  left the direction to the stated-direction sentence in the text, rather than inventing a reference curve.
- **Mitotic phases (Fig. 2L) and the 43-kinase screen (Fig. 5D, S4A).** Mitotic phase is not a context field
  and is not a level of a number; I recorded Fig. 2L as one measurement of "mitosis index" rather than five
  groups. For the screen I wrote one item per phospho-target that carries a mark and one measurement item per
  unmarked target, plus one item for the screen as a whole; the remaining ~35 kinases of Fig. S4A are not
  separately recorded because only the panel image names them.
- **`number_of_lines` where the paper does not count.** Supplementary Table 1 names the line(s) per panel but
  the text states a count only for the four-line experiment. Counting "one line" or "two lines" from the names
  would be a computed value, so single- and two-line units carry `number_of_lines: not stated`.
- **Cell density is split over two fields.** In Fig. 1B–1F the three conditions differ in `seeding_density`
  (100,000 / 10,000 / 500,000–1,000,000 cells/cm²); in Fig. 1J–1N and Fig. 4H–4K the same number of cells is
  plated in a 48-well or a 6-well plate, which I put in `platform` with `seeding_density` in the unit. There
  is no field for cell density as an experimental factor, so the two halves of the paper's central contrast
  are expressed differently and code will not see them as the same factor.
- **"w/o passaging" has no field.** Whether cells were passaged at all is stated but fits no field; it sits in
  `other_conditions` on the group, and the contrast between passaged and unpassaged is therefore invisible to
  code.
- **Action potentials.** The text reports no difference in spontaneous action potentials and the Methods
  describe sharp current-clamp recordings at room temperature, but no panel shows them. I recorded the
  statement as one item with `stated_direction: none` under the calcium unit (37 °C), so the room-temperature
  condition of the AP recordings is not represented.
- **mmc8.pdf** is "Document S2", the article and the supplement in one file; it duplicates the other two PDFs
  and is listed in `source.not_used`. The six videos the paper names are not in the folder (`source.missing`);
  no item rests on them, but Fig. 3E's force measurement cites Videos S2–S4.
- **Mouse groups.** The in vivo mouse experiments (Fig. S5) are recorded as `native tissue` groups, which
  inherit nothing; they carry only species, donor age, preparation and treatment. "CD1 mice" in the Methods
  and "C57BL/6J Mice" in the key resources table disagree; I did not record a strain and did not flag it as a
  suspected error on an item, because no item's value depends on it.
- **Approximate and compound values.** "~2 million", "300 million to 900 million", "100- to 250-fold" and
  "~10-fold" are written as printed strings in the unit "cells" or "fold"; the ranges are two values each. The
  "8-, 8-, and 4-fold at each passage" values are written in the order printed, without assigning a passage,
  because the text does not name which passage is which.

## Figures and data reader

Unit F1BF (Fig. 1B–1F). No released data or table gives these values (the paper ships PDFs only).

- **Panels read.** Fig. 1D (Ki67+/TnT+ %) and Fig. 1F (pHH3+/TnT+ %), journal_version.pdf p. 4, both vector:
  `figures/f1d.py`, `figures/f1f.py` with the shared helper `figures/_util.py`. Each group gives 6 points (blue
  circles w/o PSG, red triangles Dense, green squares Sparse), the drawn mean and the upper SEM cap. Fig. 1B
  (fold change, a curve of means) was not listed by `figures-needed` and was not read.
- **Calibration.** Tick labels are outlined glyphs, not text, so `tick_marks()` finds nothing; the y axis is
  calibrated from the vector tick marks paired in order with the printed labels (1D: 0–50 by 10; 1F: 0–15 by 5).
  Fit residual is 0.
- **Counted points vs printed n.** 6 per group in both panels, matching "6 biological replicates". Point means
  agree with the drawn means (1D: 18.0 / 15.96 / 33.46; 1F: 1.09 / 1.35 / 5.79).
- **Groups shared by items.** Each panel group serves two pairwise items, so the same points are returned under
  one label per item/group (six labels per panel).
- **Text vs figure.** F1F_text prints the sparse mitotic fraction as 10%; the panel's sparse mean reads 5.79%
  (points 3.1–12.4). Nopsg and dense read 1.09% and 1.35%, matching the printed "1%". Not changed; for the
  record reader.
- The highest sparse point in 1F (12.35%) lies well above the others (3.1–6.9%); kept as read, not marked suspect.

Unit F1GI (Fig. 1G–1I). No released data or table gives these values.

- **Panel read.** Fig. 1I (Ki67+/TnT+ %), journal_version.pdf p. 4, vector: `figures/f1i.py` with the shared
  helper (its y-tick width limit is now a parameter; 1I's tick marks are 4 pt long, 1D/1F keep the old limit).
  Fig. 1G (schematic) and 1H (images) hold no values.
- **Calibration.** Outlined-glyph labels 0–80 by 20 paired with the five vector tick marks.
- **Counted points vs printed n.** 4 per group (Fresh, 1X, 0.1X, 0.01X), matching "4 biological replicates"
  (the 2 technical replicates are not plotted separately). Point means agree with the drawn means
  (33.17/33.13, 35.13/35.13, 23.25/23.27, 31.2/31.2).
- **Marker centres.** Points are bounding-box centres; for the triangles (0.01X) and diamonds (1X) this is the
  symbol's box centre, not its centroid. The 0.01X triangles overlap the mean line but each is a separate
  vector object, so the count is exact.

Unit F1JN (Fig. 1J–1N). No released data or table gives these values.

- **Panels read.** Fig. 1L (Ki67+/TnT+ %) and Fig. 1N (pHH3+/TnT+ %), journal_version.pdf p. 4, both vector:
  `figures/f1l.py` and `figures/f1n.py` with the shared helper. Fig. 1J (schematic) and 1K/1M (images) hold no values.
- **Calibration.** Outlined-glyph labels 0–40 by 10 (1L) and 0–15 by 5 (1N) paired with the vector tick marks.
- **Helper change.** 1N's Dense circles are drawn 3.7 x 4.0 pt, above the helper's 4 pt marker limit, so only one was
  found; the limit is now a parameter (`marker_max`, default 4 keeps 1D/1F/1I unchanged; 1N uses 4.5).
- **Counted points vs printed n.** 1L: 3 per group, matching "3 biological replicates". 1N: 6 per group, matching
  "6 biological replicates". Point means vs drawn means: 1L 16.18/16.17 and 33.92/33.93; 1N Sparse 5.38/5.38,
  Dense 0.718/0.664 (the six Dense circles overlap near zero, and their 4.0 pt boxes are taller than wide, so the
  box centres may sit slightly off; not adjusted).
- **Statuses.** F1L: close (pooled t p 0.006–0.008 against **p < 0.01; Welch above 0.01). F1N: consistent within reading.
- **F2L (Fig. 2K and 2L).** No points. Panel L shows five vector bars (Interphase to Telophase, mitosis index, CHIR
  only) with mean ± SD error bars, so `no_points` is recorded and no script is written. Panel K is images. Neither
  mmc1.pdf nor the main text has a table of these values, and the paper releases no data file. Item F2L names only the
  chir group, and its finding (cells found at every phase) compares phases rather than groups. The record has no
  per-phase groups, so the bars would have nothing to attach to even if they could be read.

Unit F3BE (Fig. 3B–3E). No released data or table gives these values.

- **Panel read.** Fig. 3E (contraction force nN, contraction velocity um/s, relaxation velocity um/s, contraction
  duration s), journal_version.pdf p. 7, vector: `figures/f3e.py`. One triangle per point (grey CTR, yellow CHIR,
  black CHIR>C59) and a black mean line; no error bars. CHIR>C59 is not read because no item compares it.
- **Not read.** Fig. 3D plots, per sarcomere angle, the mean percent of sarcomere area with SD bars (n = 10 cells):
  no individual cells are plotted, so items F3D/ctr, F3D/chir, F3D/chir_c59 get no readings. 3B and 3C are images.
- **Calibration.** The panels have no tick marks and their labels are outlined glyphs, so each axis is calibrated
  from the vertical centres of its label rows (the label column is separated from the rotated axis title by a
  per-panel x limit). Label centres sit about 0.2 pt above the axis-line ends for 0 and the maximum, consistently.
- **Counted points vs printed n.** 15 per group in every panel (CHIR>C59 has 16 in the force panel), against the
  record's printed n "20 biological replicates, 60 cells analyzed"; the audit flags n as inconsistent. The legend
  says dot plots are biological replicates.
- **Point means vs drawn means.** Force CTR 198.2/193.6, CHIR 101.1/93.9; contraction velocity 18.63/18.55,
  10.40/10.06; relaxation velocity 10.76/10.29, 4.77/4.93; duration 0.139/0.141, 0.150/0.156. The differences go
  both ways (up to about 1 pt), so they are not a marker-centre offset; the drawn mean may be over more cells than
  the 15 dots plotted (consistent with the n mismatch). Not adjusted.

### Fig. 4A–4B (unit F4AB)
- **Read:** Fig. 4B (`f4b`, vector), YAP nuclear/cytoplasmic ratio. Panel A is images. No table or data file gives the values (Table S1 lists replicates only; no .xlsx released).
- **Counts:** 7 red circles (Dense) and 7 green squares (Sparse), which matches the printed 7 biological replicates. Point means 1.905 and 7.317 match the drawn mean lines (1.900 and 7.313).
- **Dense SEM bar:** the caps are about 0.5 pt apart (SEM ≈ 0.05), so the implied n (5.2 against 7) is within reading resolution of a bar this small.
- **P value:** a pooled t test from the points gives p ≈ 0.0002–0.0004, and Welch gives ≈ 0.002. Both are above the legend's ****p < 0.0001 and fit the panel's *** mark (the record already flags *** against ****). Not adjusted.

### Fig. 4H–4K (unit F4HK)
- **Read:** Fig. 4I (`f4i`, vector), YAP nuclear/cytoplasmic ratio, and Fig. 4K (`f4k`, vector), Ki67+/TnT+ (%). Panels H and J are images. No table or data file gives the values.
- **4I has no error bars as objects:** each group has a mean line but no SEM caps or stems (the legend says mean ± SEM), so the bar gives the mean only. An `error_bars=False` option was added to `_util.read_dot_panel` for this; the earlier panels keep the default.
- **Counts 4I:** Dense - DMSO 3; Sparse - DMSO, 0.1uM, 1 uM and 10 uM 4 each. The printed n is "3-4 biological replicates". The audit's n check reads this as [3] and marks the 4-point groups inconsistent; that comes from parsing the range, not from the figure.
- **Mean line vs points, 4I Sparse - DMSO:** the drawn mean, 3.488, sits 0.07 (about 1 pt) below the mean of the 4 points, 3.558. Dense - DMSO (1.437 vs 1.445) and 10 uM (2.592 vs 2.604) agree within reading. No hidden marker object was found. Not adjusted.
- **Counts 4K:** Sparse - DMSO has 5 red squares against the printed "6 biological replicates". The 5-point mean (33.87) equals the drawn mean line, so no marker is missing from the drawing. 10 uM has 6 points (n = 6). Dense - DMSO has 4 points; no item links it.
- **Record note (not edited):** the record gives the vp01/vp1/vp10 concentrations as "0.1 mM / 1 mM / 10 mM". The axis labels and legend print uM / µM ("1.0 or 10 µM"), so this is likely a µ→m glyph slip.

### Fig. 5A–5C (unit F5AC)
- **Read:** Fig. 5A (`f5a`, vector), normalized LEF/TCF luciferase expression, and Fig. 5B (`f5b`, vector), relative TnT+ cell number. Each draws filled triangles and a black mean line. There are no error bars and no y tick marks, so the axis is calibrated from the centres of the outlined tick-label rows (0–1.4). A new helper, `_util.read_glyph_axis_triangles`, does this. No table or data file gives the values.
- **Not read: 5C (qPCR; F5C_AXIN2, LEF1, CCND2, MYL2, MYH7, MYOM1).** It shows bars with mean ± SD and plots no individual points. `no_points` is kept per unit, and this unit has points in 5A/5B, so 5C cannot be marked there. `figures-needed` will keep listing its 12 groups.
- **Counts 5A:** CHIR has 6 triangles, which matches the printed n of 6. CTR has 8 and CHIR + PNU74654 has 8 (the latter is not linked to any item). All of them overlap near 0, and their y positions are quantized in 0.31 pt steps, so equal positions can be distinct values. Taking every drawn object, the CTR count does not match the printed n of 6, and the audit marks F5A inconsistent. Not adjusted.
- **Mean line vs points, 5A CTR:** the mean line reads 0.0245, but the 8 triangle centres read 0.053–0.075. That is about 1.8 pt below every marker, so the mean line cannot be the mean of the drawn markers. For CHIR, the line reads 0.973 against a point mean of 0.986.
- **Counts 5B:** 4 triangles per group, which matches the printed 4 biological replicates. The mean lines run 0.01–0.03 below the point means: CTR 0.275 vs 0.280, CHIR 0.971 vs 0.984, and CHIR + PNU 0.505 vs 0.534, which is about 1 pt. This could be because the marker's anchor is its centroid rather than its bounding-box centre. The bounding-box centre is used as in the earlier panels.
- **5B vs text:** the text says PNU74654 cut the CHIR increase "only by 50%". From the drawn means, (0.505−0.275)/(0.971−0.275) leaves 33% of the increase, a 67% drop. From the point means it leaves 39%. This is computed here only as a note; the record's check decides.

### Fig. 5D and Fig. S4A (unit F5D)
- **Not read: no points.** Fig. 5D (journal_version.pdf p. 10) shows vector bars for CTR, CHIR t=10min and CHIR t=100min, with error bars, for eight phospho-kinases and b-Catenin total. Fig. S4A (mmc1.pdf p. 9) shows horizontal bars for T0, T10 and T100 for 43 kinases, with no error bars. Neither plots individual points, and no table or data file gives the values, so the unit is entered in `no_points` and no script was written.
- **Record note (not edited):** the printed n is 1 biological replicate with 2 technical replicates, yet t tests are marked (*, **) against CTR. CTR is normalised to 1 but has a visible error bar on some kinases (e.g. pGSK3).

### Fig. 5G–5K (unit F5GK)
- **Read:** 5H (`f5h`), 5I (`f5i`) and 5J (`f5j`). All are vector filled triangles (grey CTR, yellow CHIR, dark yellow CHIR + MK2206, black MK2206) with a black mean line and no error bars or y tick marks. Each y axis is calibrated from the centres of its outlined tick-label rows. MK2206 alone is not read because no item compares it.
- **Hidden layer:** each panel also holds a stale chart layer: 8 grey, 5 yellow, 6 dark yellow and 8 black triangles stacked at the plot top, plus '**' glyphs. A white box drawn later covers it. The helper (`read_glyph_axis_colours`) skips any object that a later white fill covers. These triangle counts equal 5J's visible counts, so the layer looks like a leftover copy of 5J.
- **Counts vs printed n:** 5H and 5I have 4/4/4 points, which matches 4 biological replicates. 5J has 8 CTR, 5 CHIR and 6 CHIR + MK2206 points against the same printed "4 biological replicates, 2 technical replicates". The CTR count fits 4 × 2. The CHIR and CHIR + MK2206 counts fit no stated n. The audit flags all three as inconsistent.
- **Point means vs drawn mean lines:** in every column the mean of the read points differs from the drawn mean line. Examples: 5H CHIR 3.78 vs 3.90; 5I CHIR + MK2206 2.51 vs 2.14; 5J CTR 0.84 vs 0.71. The sign varies, so this is not a marker-anchor offset. The plotted points may not be the values that were averaged.
- **Below zero:** one 5I CTR point reads −0.074, a fold increase below 0. The marker sits on the x axis line. Kept as read.
- **Not read: 5K.** Panel K is vector bars (CTR, CHIR, CHIR+MK2206 for AXIN2, LEF1, CCND2, MYL2, MYH7, MYOM1) with mean ± SD and no points. Its eight items get no figure values, and F5GK is entered in `no_points` for the panel K groups only. No data file exists for this unit.

### Fig. 5M and 5N (unit F5MN)
- **Read:** 5N (`f5n`), vector filled triangles (grey CTR, yellow CHIR, dark yellow CHIR + MK2206, black CHIR + PNU74654) with a black mean line and no error bars or y tick marks; y axis calibrated from the centres of the four outlined tick-label rows (0–60). Panel M is images. No table or data file gives the values.
- **Legend triangle:** the legend's CHIR + PNU74654 marker is a black triangle like the data markers; the crop starts at y = 464 pt, below the legend, so it is not read.
- **Counts vs printed n:** 4/4/4/4 points, which matches 4 biological replicates (2 technical replicates and 955 cells are also printed). Two CHIR + PNU74654 triangles overlap exactly (both read 14.53); both are kept.
- **Point means vs drawn mean lines:** CTR 7.75 vs 5.66 (the line sits below three of the four points), CHIR 41.55 vs 40.24, CHIR + MK2206 31.59 vs 30.17, CHIR + PNU74654 16.72 vs 16.60. As in 5A–5J, the drawn means are not the means of the drawn points.

### Fig. 5O and 5P (unit F5OP)
- **Read:** 5P (`f5p`), vector filled triangles (yellow CHIR, black CHIR + Palbociclib) with a black mean line and no error bars or y tick marks; y axis calibrated from the centres of the six outlined tick-label rows, read as 0, 2, 4, 6, 8, 10 (five single-glyph rows and a two-glyph top row, evenly spaced; the labels are glyphs, not text, so the values are a reading of their shapes). Panel O is images. No table or data file gives the values.
- **Counts vs printed n:** 4/4 points, which matches 4 biological replicates (2 technical replicates and 1368 cells are also printed).
- **Below zero:** one CHIR + Palbociclib triangle reads −0.07 (its centre sits just under the x axis line, within the interval); it is kept as read.
- **Point means vs drawn mean lines:** CHIR 6.29 vs 6.08, CHIR + Palbociclib 0.37 vs 0.09. As in 5A–5N, the drawn means are not the means of the drawn points.

### Fig. 6C–6G (unit F6CG)
- **Read:** 6G (`f6g`), six vector plots (beating rate, force, time to peak, relaxation time, resting length, contraction velocity): grey Non-Expanded and yellow P4 CHIR>CTR bars (bar top = mean) with an upper error bar only, and one filled circle per tissue coloured by line (blue CVI-111, orange CVI-273). Both line colours are pooled into the bar they sit on (the record's groups are treatments, not lines). Each circle is a fill path followed by a stroke-only copy of the same outline; only the fills are counted. Y axes calibrated from each plot's vector tick marks (labels are outlined glyphs).
- **Not read:** 6F (three time courses, day 5–20) plots one mean marker per day joined by a line, with error bars; no individual tissues, so its groups are listed under `no_points: F6CG`. C–E are images. Table S1 (replicates) is not text in mmc1.pdf. No released data.
- **Counts vs printed n:** 13 Non-Expanded and 21 P4 CHIR>CTR circles in every plot, against a printed '12-20 biological replicates'. 13 is inside the range; 21 is one above it. The point means match the bar tops (e.g. rate 38.54 vs 38.52, 23.71 vs 23.71), and (SD of points / error bar)² gives 12.5 and 21.0, so the error bars are SEM of the drawn points (the legend says bars are mean ± SD but dot plots mean ± SEM).
- **Audit parsing:** the audit reports the printed n as [1, 12] for '12-20 biological replicates, 1 technical replicate', so it flags the 13-point groups as inconsistent too; that looks like an n-parsing problem in code, not a reading problem.
- **Units:** time to peak prints no unit on the axis or in the legend ('time to peak [T1]'); `unit_of_value: not printed`. Beating rate's axis title is 'Beats/minute'.
- **Item wording:** the unit F6CG's title/anchor/method describe 6C (bright-field images) and qPCR, while its items are contraction measures from 6F/6G; noted for the record reader.
- **Fig. S1A (unit S1A):** not read. The panel is smoothed vector curves of normalized gene expression (six genes, D0–D14; dashed CHIR lines only for D12–D14) with no markers, no error bars and no replicates (printed n: 3 biological, 2 technical replicates). Listed under `no_points: S1A`. No table or data file holds the values; mmc8.pdf is already in `not_used`. Item S1A has no `compares` and no test, so nothing is lost for a check.
- **Fig. S1B and S1C (unit S1BC):** not read. Each graph is two vector bars (grey CTR, yellow CHIR) with one error bar each (legend: mean ± SD) and 'NS'; no individual points, so S1B and S1C are listed under `no_points: S1BC`. The rest of the panels is images. No table or data file holds the values (the paper releases no data files; Table S1 lists replicates only).
- **Fig. S1D (unit S1D):** not read. The panel is two vector line series (Freshly differentiated, Cryopreserved) of fold increase in cell number at P1–P4, one mean marker per passage with an error bar (the legend does not say SD or SEM), 'NS' at each passage. The 2 biological replicates per group (printed n) are not plotted, so S1D is listed under `no_points: S1D`. No table or data file holds the values.
- **Fig. S1E (unit S1E):** not read. The panel is two vector line series (grey CTR, yellow CHIR) of Percent Ki67+ cells at P0–P5: one filled circle per passage (the mean) joined by a line, with an error bar per marker (Fig. S1 legend: mean ± SD), and '*' at P1–P5. No individual replicates are plotted, so S1E is listed under `no_points: S1E`. Table S1 gives replicate counts only; no table or data file holds the values. Item S1E's printed p (4.42E-05) is a single value for a multi-passage series; the record does not say which passage or test it belongs to (noted for the record reader).
- **Fig. S1F and S1G (unit S1FG):** not read. S1F is images. S1G (% Annilin-eGFP+ nuclei, as spelled on the axis, D0–D10) is bars with error bars (legend: mean ± SEM, n=1): one white D0 bar, then grey CTR and black CHIR bars at D3, D5 and D10, with '*' over D10. No individual points are plotted, so the unit is listed under `no_points: S1FG`. No table or data file holds the values. Item S1G does not say which day it compares (its finding names D10); noted for the record reader.
- **Fig. S1H and S1I (unit S1HI):** not read. Each graph is three vector bars (grey CTR, yellow CHIR, black CHIR>C59) with one error bar per bar (legend: mean ± SD) and '*' over CHIR; no individual points are plotted, so the unit is listed under `no_points: S1HI`. No table or data file holds the values. The text layer under S1I's x labels holds both 'CHIR>CTR' and 'CHIR>C59' at the same place (only 'CHIR>C59' is visible); the record's third group (chir_c59) follows the visible label and the legend.

### Fig. S3 (unit S3)
- **Read:** S3C (fold increase TnT+ cells), S3E (% Ki67+/TnT+) and S3G (% pHH3+/TnT+), mmc1.pdf p. 8, all vector, one script (`s3`) with a new helper `_util.read_text_axis_triangles`. Filled triangles (grey CTR, green Wnt ligands, yellow CHIR) and a black mean line; no error bars, no y tick marks. A, B, D and F are a schematic and images. No table or data file gives the values (Table S1 lists replicates only).
- **Hidden layer:** each panel holds a stale bar-and-error-bar chart (with its own axis lines and a second set of text tick labels, offset 15–16 pt) under a later white box; it is skipped. In S3C the stale x axis line pokes 1.4 pt out past the white box (the dot at the right end of the axis in the render), so the x axis is taken as the line meeting the visible y axis foot.
- **Calibration:** the tick labels here are text. For each printed value, the label copy nearest the visible y axis span is used, and the axis is fitted to the label centres. Label centres sit about 0.75 pt above the axis line ends, and this gap is added to every interval (about ±1.3 pt in total).
- **Counts vs printed n:** 4 points in every group of every panel, which matches "4 biological replicates" (2 technical replicates and 5098 cells are also printed). Two S3C RSPO triangles overlap exactly (both read 0.88); both are kept.
- **Point means vs drawn mean lines:** S3C CTR 0.93 vs 0.56 (the line sits about 6 pt below all four points), RSPO 1.04 vs 0.98, scFv-DKK1c 1.69 vs 1.45, Wnt3A 4.05 vs 3.84, scFv-DKK1c + RSPO 8.07 vs 7.95, CHIR 8.82 vs 8.72. S3E CTR 24.85 vs 23.60, Wnt3A 39.13 vs 38.15. S3G Wnt3A 6.12 vs 5.79. As in Fig. 5, the drawn means are not the means of the drawn points; most lines sit below them. Not adjusted.
- **Record notes (not edited):** the record's S3C item for RSPO/scFv-DKK1c has no stats, while the panel prints no asterisk over them. A fold increase CTR whose points average 0.93 (not 1) suggests normalisation to something other than the CTR mean.

### Fig. S5A–S5E (s5, mmc1.pdf p. 10)
- **Panels read:** S5B (Relative pHH3+/TnT+ Cells, 0–2) and S5C (%pHH3+ Cells, 0–1.4), vector filled triangles (grey CTR, yellow CHIR) with a thick black mean line and no error bars; read with the same helper as Fig. S3 (text tick labels, no y tick marks; the ~0.75 pt gap between the fitted 0 and the x axis line is added to every interval). The legend triangles above each panel are outside the panel boxes. No stale layer here.
- **Not readable:** S5E (cell size) is two vector bars with one error bar each and "P=0.4"; no points, so its groups stay open (`no_points: S5AE`). A and D are images.
- **Counts vs printed n:** 4 points per group in B and C, matching "4 biological replicates" (2 technical replicates and 112162 cells also printed). S5C CTR points overlap partly but are separate vector objects.
- **Point means vs drawn mean lines:** S5B CTR 1.009 vs 0.984, CHIR 1.728 vs 1.713; S5C CTR 0.830 vs 0.805, CHIR 1.246 vs 1.229. The lines sit slightly below the point means (as in Fig. 5 and S3); not adjusted. Point positions are triangle bounding-box centres.
- **Printed fold:** the record's S5B fold "1.8" vs 1.71 (point means) or 1.74 (drawn lines); the axis is about 1.7 pt per 0.01, so the gap is larger than reading error and may be rounding or a different normalisation. Not adjusted.
- **Stray text:** each of S5B, S5C and S5G carries an x-axis label set "0 2 4" (text) below the axis, not part of the visible chart.

### Fig. S5F and S5G (s5g, mmc1.pdf p. 10)
- **Panel read:** S5G (Relative pHH3+/TnT+ Cells, 0–2, P10 mouse myocardium), vector filled triangles (grey CTR, yellow CHIR) with a thick black mean line and no error bars; read with `_util.read_text_axis_triangles` as in S5B/C. The crop bottom (1010.5) keeps the "0" tick label in and the stray "0 2 4" x labels out. S5F is images. No table or data file gives the values.
- **Counts vs printed n:** 3 points per group, matching "3 biological replicates" (4 technical replicates and 157280 cells also printed).
- **Point means vs drawn mean lines:** CTR 0.994 vs 0.968, CHIR 1.394 vs 1.366; the lines sit about 0.027 below the point means, as in S5B/C; not adjusted.
- **Record notes (not edited):** the unit's shared context (cell_line CVI-111, cm_day_at_formation day 12, treatment CHIR99021 2.0 mM) describes the in vitro hiPSC-CM work, not P10 mice injected with CHIR 50 mg/kg; S5G's printed test is "not stated" with P=0.07.

## Vocabulary agent

- **Cell lines:** the paper writes CVI-111/113/202/273; Cellosaurus has the Stanford lines as SCVI-111 (CVCL_C6U9), SCVI-113 (CVCL_A8QC), SCVI-202 (CVCL_C6UA) and SCVI-273 (CVCL_A5GC, already adopted). Mapped as synonyms on the assumption that the dropped "S" is the paper's spelling (the methods cite Matsa et al., 2016 for these lines). The eGFP-anillin reporter line is mapped to its parent iLB-C1-30 m-r12 (CVCL_W566 Ctrl1-12); the reporter goes to `transgene` (new term eGFP-anillin fusion).
- **Not in ChEBI:** thiazovivin (printed "Thiozovivin"), R-spondin 1, scFv-DKK1c and concentrated conditioned medium were added with `adopt_own`. The control "media alone" became an own term with the paper's name as a qualifier; it is not a vehicle control.
- **Split requests (3):** B27 is in `cm_medium` ("RPMI 1640 + B27") and in a treatment value, but `supplements` holds only KOSR and thiazovivin; TrypLE Select is in a `preparation` value ("dispersed with TrypLE Select Enzyme"); "micro-patterned" is in `replating_coating`.
- **Flags (5, all *several measures*):** F3FH_text (AP, calcium transients, beat rate and amplitude), F3IK_text (seven genes), F3L_capture (three sequencing counts), S1A (six genes in one item), S4A (43 kinases in one item).
- **Possible record errors (not edited):** F3IK preparation "cell lysate" is not in the paper; the item is qPCR on extracted RNA. Unit S5AE/S5FG: the reader's own note already says the unit's shared context (cell_line, cm_day_at_formation, the in vitro CHIR treatment) describes the in vitro work, not the mice. The F6 "contraction velocity (mN/s)" is a force rate, so it maps to the maximal rate of force rise. The array spot printed "pAkt1/2/3 T473" is presumably S473; mapped as printed.
- **Judgements:** "Engineered Heart Tissues" maps to generic 3D engineered tissue because the paper cites Hansen et al. 2010 but names no posts. "micropatterned surfaces" maps to micropatterned single cell (no synonym, because the wording is generic). "heart sections" maps to cryosection (OCT cryo-sectioning in the methods; no synonym). The YAP nuclear/cytoplasmic ratio is protein fluorescence intensity in the nucleus, normalised to the cytoplasm, not a new term. Fig. 2L "mitosis index" (cells per mitotic phase, by imaging) got a new child term under cell cycle phase fraction. "total culture surface" got a new root measure, culture surface area. For "relative TnT+ cell number" and "relative pHH3+/TnT+ cells", `expressed_as` is left to the values, because their printed units differ (fold, % change).

## Formula agent

- **Single-cell force (F3E_force):** the methods give F = (deformation / 112 um) x surface area (1800 um^2) x Young's modulus (10 kPa). Mapped to a new derived entry `force_from_strain_modulus_area` (stress_def + linear_elastic_stress_strain, strain = d/L). Observation for code: E is the hydrogel substrate's modulus and A the patterned planform area, not a cross-section carrying the force, so the entry's does_not_apply ("an area other than the one carrying the force; a modulus of a body other than the one strained") may cover this use. No force or deformation is printed, so nothing is rebuilt; both model assumptions are not stated.
- **Anchors:** L = 112 um sits in a typeset equation that pdftotext garbles ("(112 mmÞ"); its anchor is the words beside it. "1800 mm2" in extracted text is 1800 um^2 in the PDF (micro sign lost); recorded as um^2.
- **"50%" drops (F5B_pnu_chir, F5H_mk):** rebuilt from readings as relative decreases of group means (45.7 % and 52.8 %); code judges a printed "50" at unit precision. The 50 % reads as a rounded statement, but the record does not mark it approximate.
- **F1B_sparse 241-fold:** taken as the product of the three per-passage folds (8 x 8 x 4 = 256 at printed precision, 241 consistent within it); new derived entry `product_of_three_ratios`.
- **Ca2+ amplitude:** methods say DF/F0 (relative_change); the Fig. 3F legend says traces are F/F0. Mapped to DF/F0 for F3H_amp.
- **Percentages and folds with no stated reference:** many measures are named only on figure axes (images for the main figures; F1D, F4K anchored "not stated") or with a legend that says "number of" while the axis is a percent (F5N, F5P: no_formula). Fold items in Fig. 5B/5H/5I and S3C never state their reference (start count or CTR). Luciferase "normalized" values (F5A, F5J) state no normaliser: no_formula.
- **qPCR:** no quantification method, reference gene or calibrator is stated anywhere; 2^-ddCt is a labelled alternative only.
- **Not recorded:** F2E_text (2 million to 300-900 million) implies 150-450-fold expansion, but no fold is printed for it; F2GH_text (100-250-fold vs CTR) is a range over lines and time points with no inputs printed, so it has no output. F1F_text's 1 %/1 %/10 % restate figure means; checking them against readings is a record check, not a derivation.
