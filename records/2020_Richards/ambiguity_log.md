# 2020_Richards

## Record reader

- **Venn-diagram circles (Fig. 2b, 4d, 5b, Supplementary Fig. 2a).** The counts are printed inside the figure image
  with no text label on each circle; only the colour key says which dataset is which. I read the five Fig. 2b Venns in
  the order of the sheet names of Supplementary Table 1 (mouse/human, porcine/human, organoid/mouse, organoid/porcine,
  organoid/human) and took the left circle as the first-named dataset. The unique counts therefore carry a group
  assignment I could not verify from the text; the shared counts (`between`) are unambiguous. The totals do not add up
  across Venns (mouse-unique is 734 against human ICM but 3,267 against the organoid), which is expected if each
  comparison uses its own platform intersection but would also be what a swapped circle looks like.
- **Compound treatment sets have no single quote.** A group that gets both the infarction protocol and an assay drug
  (noradrenaline + FCCP, noradrenaline + 2,3-butanedione monoxime, noradrenaline + DOX, noradrenaline + JQ1) has a
  treatment set whose members are stated in two different sentences, so no one quote holds every word of the value.
  I wrote those values as `ContextObj`s with an inline anchor on the sentence that states the added agent; the
  noradrenaline member is anchored on its own elsewhere in the record. A context value assembled from two sentences
  seems to be outside what *Context is anchored too* describes.
- **Edge against interior is not a field.** Fig. 1h, 5f and Supplementary Fig. 1b and 8 compare a region inside one
  organoid (edge/exterior against interior/centre). No context field holds it, so each such group carries an
  `other_conditions` entry ("Edge", "Interior", "exterior", "interior"). Code will see those pairs as differing in no
  field at all.
- **Fig. 1h prints two P for one plot.** The panel shows a bracket "P = 0.0014" and a separate "*" bracket, and the
  legend gives "*P < 0.001"; the brackets' endpoints are not legible. I wrote one omnibus item over the four groups
  with `P = 0.0014` and the legend's threshold under `p_values`, rather than guess which pairs the brackets span.
- **Control oxygen is never stated.** The infarct groups are "10% O2" as printed; for the control organoids the paper
  only writes "control" and "high O2" (Fig. 1d), and the 20% figure appears only as a boundary condition of the
  diffusion model. I wrote `incubator_atmosphere: not stated` for every control organoid group rather than carry 20%
  over from the model.
- **D10 against D11.** Every RNA-seq figure legend says the samples are D10 organoids; the Methods say total RNA was
  isolated on D11. I used "D11" for the RNA-seq units (it is the measurement) and recorded "D10" where the figures
  state it; the two are not flagged against each other because they sit in different units.
- **Transcriptomic analyses recorded at the level of the run, not the row.** Table 1 is one item per principal
  component holding every printed term's number of genes, enrichment score and q value, instead of 13 items per
  component, because the whole table is one GSEA run with one printed P ("0"). The 20-pathway and 20-GO-term tables in
  Supplementary Fig. 3 are images of tables inside the .docx and are *not* recorded term by term; the terms the main
  text and Table 1 print are.
- **Gene-set tables sampled.** Supplementary Tables 3, 4 and 6 hold a log-fold change per gene for hundreds of genes.
  I recorded only the genes the main text names as representative (LDHA, LDHB; ITGB3, COL1A1, TGFB1, MMP2; ATP2A2,
  CACNA1C, RYR2, SLC8A1), each anchored to its cell. The rest is unread.
- **Supplementary Table 5 holds a P per radial position** (dozens per comparison) for Fig. 4f, 6b and 7c. The items
  carry the figure's "P < 0.05" as their P and one or two table cells under `p_values`; the whole profile is not
  recorded. The four Fig. 7c items are anchored to their table cells so the file feeds values.
- **hADSCs have no field.** `stromal_cell` holds the cardiac fibroblasts; the adipose-derived stem cells appear only
  inside `cell_types`, because the sentence that names both of them is the composition sentence and `stromal_cell`
  would need its own quote holding both.
- **Representative images are not items.** Panels that show staining without a quantification (Fig. 1g, 4g, 5h, 7d,
  7f, Supplementary Figs. 11a–c, 13c, 14b, 15) are not recorded as evidence; where the text states an outcome from
  such a panel (Supplementary Fig. 1d, the 0.1% O2 condition) I recorded an item with a `stated_direction`.
- **Model output left out, as the spec asks:** the finite-element oxygen-diffusion fields of Fig. 1b,c and their
  constants, and the PCA sample coordinates. The printed proportions of variance are recorded as values of an item
  with no group, which is a shape the schema allows but the spec does not describe.
- **Two reported-twice P** (Fig. 4i `P = 0.0025` against the text's `P < 0.0025`; Fig. 5g `P = 0.014` against
  `P < 0.014`) are recorded as `p` plus `p_values` and additionally labelled `suspected_error`, which may double up
  with the *reported twice* finding code computes.

## Figures and data reader

- **Fig. 1h (unit F1h), `f1h_nadh`.** Vector panel (journal_version.pdf p. 3). Read by script: 10, 10, 11, 11 dots for
  control edge, control interior, infarct edge and infarct interior, matching the legend's n = 10 control and n = 11
  infarct organoids (each organoid measured at edge and interior). Bar tops and upper s.d. ends read too; the means of the
  read dots agree with the bar tops to within 0.001. Axis calibrated on the four tick lines (0–1.5); no unit is printed
  (the index is a ratio to dead organoids), so `unit_of_value` is "NADH index".
- Group order taken from the panel: dark green = "Edge", light green = "Interior" in its key, "Control" and "Infarct"
  printed under each pair. No released data hold Fig. 1h values (Supplementary Tables 3–7 checked by sheet).
- Several dots overlap partly (e.g. control edge around 0.9–1.0) but each is its own vector path, so all are counted.

### Fig. 2c,d (unit F2cd)
- Both panels are raster images. Fig. 2d (PC3 vs PC4 sample scores) is read by `figures/f2d_pca.py`; each marker gives a
  `<group>_pc3` and a `<group>_pc4` point with the same index. Axes calibrated on the raster tick lines matched to the
  text tick labels (four per axis; the labels print negatives with an en dash, which `tick_marks()` does not parse, so
  the script reads the words itself).
- Counted points vs printed n: human ICM LV 8 (n = 8) and human non-failing LV 8 (n = 8); every blue marker stands alone.
- Not readable: control and infarct organoids (n = 3 each; the green markers of each group merge into one blob),
  mouse sham and mouse MI LV (n = 4 each; purple markers merge, three of four in each group). These return no points
  (countable: false). So the organoid groups, the only ones with values from this paper's own samples, get no figure values.
- Fig. 2c (PC1/PC2 strip plot) is not read: every group is a merged cluster.
- The item's own values (PC1–PC4 % of variance) are printed; the figure readings are sample scores, a different quantity,
  listed under the same item because it is the only item on unit F2cd. No released data hold PCA scores
  (Supplementary Tables 1–7 checked by sheet: GO terms, gene sets with LFC, vimentin/DOX values, Tukey p-values).

### Fig. 3c,d (unit F3cd)
- Fig. 3d is read by `figures/f3d_peak_ocr.py` (vector panel, journal_version.pdf p. 6). Each dot is its own vector
  path: 59 dark blue (control) and 59 orange (infarct), matching the legend's n = 59 organoids per group, although many
  dots overlap. Bar tops and upper s.d. caps read too (legend: mean ± s.d.). The read points give mean 198.5 / s.d. 64.5
  (control) and 132.0 / 35.3 (infarct); the bars read 198.3 (cap 262.8) and 132.3 (cap 167.2). Axis calibrated on six
  tick lines (0–500).
- Fig. 3c (OCR time course) plots only group means at each time point, so it is not read.
- No released data hold Seahorse values (Supplementary Tables 3–7 checked by sheet).
- The legend gives n = 59 organoids but also n = 3 wells per group; the dots are organoids.

### Fig. 3e,f (unit F3ef)
- Fig. 3f is read by `figures/f3f_peak_ecar.py` (vector panel, journal_version.pdf p. 6): 59 dark blue (control) and
  59 orange (infarct) dots, matching the printed n = 59 per group. The read points give mean 94.3 / s.d. 19.5 (control)
  and 136.5 / 27.8 (infarct); the bars read 94.1 (cap 113.8) and 136.5 (cap 164.3), so the caps match s.d. Axis
  calibrated on four tick lines (0–300).
- Unlike Fig. 3d, the error bars are upper-only and are drawn in the same stroked path as the bar outline.
- One infarct dot sits at 280 (the next highest at 209). It is kept as read and not marked suspect, because it is a
  plotted organoid.
- Fig. 3e (ECAR time course) plots only group means at each time point, so it is not read. No released data hold
  Seahorse values.

### Fig. 3g (unit F3g)
- Fig. 3g is read by `figures/f3g_lactate.py` (vector panel, journal_version.pdf p. 6). It finds 6 dark blue (control)
  and 6 orange (infarct) dots, matching the printed n = 6 wells per group. The read points give mean 1.000 / s.d. 0.149
  (control) and 1.352 / 0.12 (infarct). The bars read 1.000 (cap 1.149) and 1.352 (cap 1.472). The axis is calibrated
  on four tick lines (0–1.5); the unlabelled top tick is not used.
- The g legend does not state what the error bars are (the "mean ± s.d." sentences belong to panels f and h). The caps
  match the s.d. of the read points.
- No released data hold lactate values. Supplementary Tables 1–7 were searched for "lactate"; the only hit is a GO term
  name in Table 1.

### Fig. 3h (unit F3h)
- Fig. 3h is read by `figures/f3h_tpm_ratio.py` (vector, journal_version.pdf p. 6). It reads two stacked panels:
  LDHA/LDHB on top (axis 0–1.5) and SLC16A1/SLC16A3 below (axis 0–2.5). Each panel is calibrated on its own tick lines.
- Every group has 3 dots, which matches the record's n = 3 per group. The read point means (LDH: control 0.676,
  infarct 1.031; SLC16: control 1.982, infarct 1.278) match the bar tops. The caps sit at about one s.d. of the points,
  which is consistent with the legend's "mean ± s.d.".
- No released data hold TPM values. Supplementary Table 3 lists LDHA and LDHB, but only as gene-level values for the
  whole table, not as per-sample TPM for these groups.
- Record note (not edited): the F3h legend says "at D10", but the unit context has `day_of_measurement: D11`.

### Fig. 4h,i (unit F4hi)
- Fig. 4i read as vector (`f4i_modulus`, journal p. 7): 19 Control and 21 Infarct filled circles, matching the printed
  n = 19 and n = 21; every circle stands alone as its own path. Axis calibrated from the six ticks 0–5 kPa.
- The points' means (2.812 and 3.317 kPa) and s.d.s (0.474 and 0.509) match the bar tops (2.811 and 3.315) and the cap
  heights above them (0.474 and 0.511), consistent with "mean ± s.d.".
- Fig. 4h shows micrographs of the aspiration only (no values). No supplementary table holds the modulus values.
- The Fig. 4i "P = 0.0025" vs Results "P < 0.0025" is already recorded as a suspected error; the pooled t-test on the read
  points gives P between 0.0011 and 0.0055.

### Fig. 5f (unit F5f)
- Fig. 5f read as vector (`f5f_calcium`, journal p. 9): 32 Control, 47 Infarct-edge and 35 Infarct-interior filled
  circles, matching the legend's n = 32, 47 and 35 ROIs. Each circle is its own path, and the circles of each group share
  one fill colour. Axis calibrated from the five ticks 0–0.8. The error bars are two-sided; the upper caps are read.
- The points' means (0.2876, 0.3344, 0.1596) and s.d.s (0.1203, 0.1450, 0.1125) match the bar tops (0.2878, 0.3344,
  0.1591) and the cap heights (0.1198, 0.1450, 0.1122), which is consistent with "mean ± s.d.".
- The interior group is compared in two items (F5f_int_vs_edge, F5f_int_vs_ctrl), and figures.yaml links one item per
  label. Its reading is therefore returned under two labels (`infarct_interior`, `infarct_interior_vs_control`), with
  the same points.
- No released data hold Fig. 5f values (the sheets of Supplementary Table 5 cover Figs. 4f, 6b and 7c only).
- Record note (not edited): the quote says interior CMs were lower "in contrast to the infarct and control edge CMs", but
  the panel shows no edge/interior split for the control. The control group is the whole-organoid control ROIs.

### Fig. 5g (unit F5g)
- Fig. 5g read as vector (`f5g_contraction`, journal p. 9): 30 Control and 30 Infarct dots, matching the printed
  n = 30 organoids per group. Each dot is drawn as two concentric filled shapes of one colour (4 and 48 path items); the
  48-item shape is taken as the dot, and the script checks that the inner shapes number the same. Axis calibrated from
  the five ticks 0–0.04.
- The points' means (0.00831, 0.00496) match the bar tops (0.00830, 0.00500). The error bars are one-sided (upper) and
  end 0.0067 and 0.0025 above the bars, equal to the points' s.d.s (0.0067, 0.0026). This is consistent with s.d.,
  though the legend does not state the error type.
- A two-sided Student's t-test on the read points gives P = 0.0136, consistent with the printed P = 0.014.
- No released data or table holds Fig. 5g values.

### Fig. 7b (unit F7b)
- Read `f7b_tunel` (vector, journal p. 11): only the 1.0 µM DOX pair (c1, i1), the only pair an item (F7b_tunel)
  compares. The other doses (0, 0.1, 10.0 µM) also plot individual points, but no item uses them.
- Counted points equal the printed n: 12 control and 14 infarct organoids at 1.0 µM. (At 0 µM only 9 control dots are
  drawn against a printed n = 10, probably because one overlaps another; not read.)
- The points' means (0.934, 0.762) match the bar tops (0.933, 0.763).
- The legend says "Data are mean ± s.d.", but the error bars' half-lengths (0.017, 0.032) match the points' s.e.m.
  (s.d. ≈ 0.055 and 0.12 divided by √12 and √14), not their s.d. The stated error type looks wrong for this panel.
- The printed test is a two-way ANOVA with post hoc Tukey test over all 8 groups. Only 2 groups are read, so the printed
  P cannot be rebuilt from these readings alone.
- No released data or table holds Fig. 7b values (Supplementary Table 5 covers Figs 4f, 6b and 7c only).

### Supplementary Fig. 1a,b (unit S1ab)
- Read `s1b_tunel` (raster). The panel exists only as a raster TIFF (word/media/image1.tiff, 220 dpi, transparent
  background) inside the supplement .docx; no PDF holds it. PyMuPDF opens the .docx, but its layout drops the images, so
  the script reads the TIFF from the archive in memory (helper `figures/_util.py`). `page` is unused, and `crop` is the
  panel box in the image's pixels, not PDF points. A shared part that opens images embedded in a .docx would remove this
  workaround. Panel a is micrographs only.
- Only the norepinephrine interior dots each stand alone: 7 dots, matching the printed n = 7. Their mean (0.878) matches
  the bar (0.877), and their s.d. matches the error bar (audit ratio 1.0), so the bar is s.d. as the legend says.
- 10% O2 exterior (n = 17), NE exterior (n = 7) and 10% O2 interior (n = 17) give bars only (countable: false). The
  exterior dots merge into clumps at about 0.95–1.0. The 10% O2 interior shows 17 dots by eye, matching n, but several
  touch, so under the stand-alone rule no points are stored for it. With touching dots resolved, S1b_hypoxia could be
  checked from points.
- The upper cap of the 10% O2 exterior error bar is hidden under its dots (only the lower cap shows), so no error is read
  for that group. The tops of the two exterior bars are taken where the bar's side outlines begin, because dots cover the
  top line.
- No released data or table holds Supplementary Fig. 1 values (Supplementary Tables 1–7 hold GO and gene tables, the data
  for Figs 4f, 6b and 7c, and Tukey P values).

### Supplementary Fig. 1c (unit S1c)
- Not read: the panel (raster TIFF word/media/image1.tiff in the supplement .docx) shows bars (mean ± s.d.) with dot swarms,
  but no group's dots stand alone. Control and infarct dots merge into horizontal rows at repeated beat rates (7 colour
  blobs each for n = 37 and 39); the metoprolol dots touch in pairs and clusters (9 blobs for n = 15). Recorded as
  `no_points` in figures.yaml; no script. No released data or table holds these beat rates.

## Figures and data reader (S1d)

- **Supplementary Fig. 1d has no points.** The legend calls it representative z-stack confocal images
  (αSA/vimentin, TUNEL; 26, 27 and 4 images); it plots no values, so `S1d_asa` rests on its `stated_direction` only.
  Recorded under `no_points`; no script and no readings. No released data table holds an αSA measure for the 0.1% O2
  group. The panel was judged from its legend and the record reader's note; no render was viewed (the session could
  not write to /tmp).

## Figures and data reader (S4)

- **Supplementary Fig. 4 has points, but none can be counted.** The panel is a 150 dpi raster TIFF in the supplement .docx
  (word/media/image4.tif): bars (legend: mean ± s.d.) with one dot per organoid, n = 10 control and 10 infarct. Colour-mask
  blobs: the control (blue) dots merge into one clump; of the infarct (orange) dots, four stand alone and the other six
  merge into two clumps (blob areas about 2× and 4× a single dot, 4 + 2 + 4 = 10, consistent with n). Raster counts are
  used only when every marker stands alone, so no group gives points. Recorded under `no_points`; no script. A bars-only
  script was not written because no check uses a mean or error bar read from a bar.
- No released data hold S4 values: Supplementary Tables 1–7 hold GO terms, gene sets with LFC, vimentin/DOX values and
  Tukey p-values, no αSMA area. The record's dataset-cell anchors to Supplementary Table 4 are fibrosis-gene LFCs, not S4.

## Figures and data reader (S5)

- **Supplementary Fig. 5 has points, but none can be counted.** The panel is a 150 dpi raster TIFF in the supplement .docx
  (word/media/image5.tif): individual circles only, no bars or means; y axis "Elastic modulus (kPa)", ticks 0–8 at 54.25 px
  per kPa, circle diameter 23 px. Non-white blobs per column: CM spheroid one clump of five open circles (85 px tall);
  FB spheroid 1 alone + 1 clump (49 px, 4 circles); cardiac organoid 1 alone + 1 clump (45 px, 5 circles); organoid+FB
  1 alone + 1 clump of 3 circles whose outlines overlap (65 px < 3 × 23). Clump sizes agree with the legend's n (5, 5, 6, 4).
  Raster counts are used only when every marker stands alone, so no group gives points. Recorded under `no_points`; no script.
- Design question (not acted on): the circles have one known diameter, and the CM spheroid circles are open, so each full
  outline is visible; a fixed-radius circle fit to the outlines could resolve the CM spheroid and organoid+FB centres. The
  stand-alone rule (and run.py's check) forbids raster points that do not stand alone, so this was not done.
- No released data hold S5 values: Supplementary Tables 1–7 contain no elastic modulus, kPa or spheroid values.

## Figures and data reader (S9)
- Panel read: Supplementary Fig. 9 PCA scatter, raster TIFF in the supplement .docx (word/media/image9.tif, 150 dpi),
  script `figures/s9_pca.py`. Each marker gives a PC1 and a PC2 reading (same index = same marker).
- No released data hold the PCA scores: Supplementary Tables 1–7 hold GO terms, gene lists and p values only.
- Counted vs printed n: Donor B control 3/3 (open rings; the two upper rings nearly touch but are separate blobs) and
  Donor B infarct 3/3 stand alone and are read. Donor A control: one ring alone and two touching (n = 3); Donor A
  infarct: the three dots merge into one blob (n = 3). Donor A gives no points (countable: false).
- The plot has no means or error bars. Tick values are taken from the printed tick labels (raster, no text layer);
  tick positions are located in the image. The record's S9_pca values (52.6%, 10.5%) are printed in the axis titles and
  agree with the record.
- The item's measure is "proportion of total variance"; the readings are per-sample PC coordinates (unit_of_value
  "PC1 coordinate" / "PC2 coordinate"), which the item's test (donor separation on PC1, infarct on PC2) rests on.

## Figures and data reader (S10)

- Supplementary Fig. 10b read (`s10_pca`): raster TIFF (word/media/image10.tif, 150 dpi) in the supplement .docx; PC3 (x)
  vs PC4 (y) sample scores. Human ICM LV (filled blue) 8 points and human non-failing LV (open blue) 8 points, each
  marker alone; counts match the legend (n = 8 each).
- Not readable: Donor B control rings and infarct dots (n = 3 each) each merge into one blob of three; mouse sham rings
  (n = 4) merge into one blob; mouse MI dots (n = 4) show as a double blob plus one dot (one marker hidden). These groups
  return countable: false. Panel a (PC1/PC2 strip plot) is all merged clusters and is not read. Panels c-d are printed
  GSEA tables (not used by S10_pca).
- The y tick at -20 has no printed label; calibration uses the five labelled y ticks and four labelled x ticks.
- Axis titles print PC3 2.6% and PC4 1.6%, panel a PC1 49.3% and PC2 31.2%; all agree with the record. As for S9, the
  item's measure is "proportion of total variance" while the readings are per-sample PC coordinates.
- No released data hold these scores.

## Figures and data reader (S11d)

- **Supplementary Fig. 11d has points, but they cannot be counted.** It is panel d of a 220 dpi raster TIFF in the supplement
  .docx (word/media/image11.tiff). It shows individual open circles only, with no bars or means. The y axis is "Elastic
  modulus (kPa)", ticks 0–7 at about 50 px per kPa, circle diameter 19 px. Non-white blobs: the infarct column has 2 circles alone
  and 2 clumps of 2 overlapping circles (33–38 px tall), n = 6. The control column has 1 circle alone and 1 clump of 4 overlapping
  circles (52 px tall), n = 5. The clump sizes agree with the legend's n. Raster counts are used only when every marker
  stands alone, so neither group gives points. Recorded under `no_points` with no script, as for S5.
- Same design question as S5: the circles are open, have one known diameter, and each outline is mostly visible. A
  fixed-radius circle fit could resolve the clumps (except the two lowest control circles, about 4 px apart). This was not done.
- No released data hold S11d values. Supplementary Tables 1–7 hold GO terms, gene lists and p values; they hold no elastic
  modulus values.

### Supplementary Fig. 12 (unit S12)
- The figure (supplement .docx, word/media/image12.tiff) shows representative 2PLSM images of one control and one infarct
  organoid, each with calcium traces for two CM ROIs. It has no per-video markers, no axis values (scale bars only) and no
  summary bars. Recorded under `no_points` with no script.
- Synchronization (S12_sync) is shown only by how the traces line up. The n of 5 videos per group is printed but not plotted.
  Supplementary Tables 1–7 hold no calcium or synchronization values.

## Figures and data reader (S13)

- Supplementary Fig. 13b read (`s13b_xtt`): raster TIFF (word/media/image13.tiff, 220 dpi) in the supplement .docx; bars
  (mean ± s.d.) with one dot per well, y axis "Normalized absorbance (relative to 0 µM dose)", ticks 0.0–2.0. Only the
  1 and 10 µM bars (the item groups c1, i1, c10, i10) are read.
- Points: infarct 1 µM 5 and control 10 µM 5, each dot alone (n = 5 wells printed). Their means (0.583, 0.558) agree
  with the bar tops read (0.587, 0.556), and mean + s.d. of the points agrees with the upper caps (0.758 vs 0.758,
  0.785 vs 0.782), so the error bars are s.d. as the legend says.
- Not countable: control 1 µM has two dots merged into one blob (3 alone + 1 double; 5 in all); infarct 10 µM is one clump
  of about 5 overlapping dots on the 0.0 line. Both give bars only (control 1 µM mean 1.161, cap 1.419; infarct 10 µM
  mean 0.039, cap hidden under the dots and not read). A fixed-radius circle split of the double blob was not attempted.
- Bar means come from the top of each bar's side strokes plus half the stroke width (dots hide the top stroke of the
  infarct bars); on bars whose top stroke is visible the two agree within 1 px.
- The 0, 0.1 µM bars are not read (no item uses them). The audit's points-to-P check cannot run in any case, because the
  Bonferroni family's groups lack points (c1 and i10 cannot be counted).
- No released data hold these values: Supplementary Tables 1–7 hold GO terms, gene lists, radial-position p values
  (Table 5) and organoid DOX ANOVA p values (Table 7, Fig. 7), none for the 2D XTT assay.

## Figures and data reader (S14a)

- Supplementary Fig. 14a (supplement .docx, word/media/image14.tif) shows only two representative bright-field
  micrographs (organoid media vs cardiomyocyte media, 1% O2 + 1 µM NE). It has no plot and no per-image values for the
  4 images per group, so the unit goes under `no_points` and no script was written.
- Item S14a_death's only value ("Almost 100%" death, cm_med) is stated in the text. Nothing is printed for org_med.
  None of the released tables (Supplementary Tables 1–7) holds cell-death values, so there are no data.yaml rows.
- Record note: the legend says the cells were cultured "for 2 days", but the record's anchor quote (Results) says
  "after 4 d". The record's time_point / day_of_measurement are "not stated". This is left to the record reader.

## Vocabulary agent

Vocabulary v37, instructions terms_v4.

- **Day 'D0' is flagged, but no flag kind fits.** `quantity_value('D0')` returns None: the regex wants a digit not preceded by a letter, and 'D10' only passes because its '0' follows '1'. So D0 is neither a quantity nor mappable to a term. It is flagged *not a context* so the reader can write 'Day 0', as at units.S5. This is a code issue: either `quantity_value` should read 'D<n>', or there should be a flag kind for a value that does not parse.
- **Doses in multi-drug treatments.** A mapping's qualifiers are one dict, so a value naming two drugs cannot give each one a `concentration`. I declared per-drug qualifiers (`noradrenaline_concentration`, `doxorubicin_concentration`, `bdm_concentration`, `jq1_concentration`, `metoprolol_concentration`). The spec doesn't say how to qualify a set; a convention is needed (for example qualifiers keyed by term id).
- **The percentages in supplements are not recorded as qualifiers.** '10% FBS + 1% glutamine + 1% non-essential amino acids' is mapped to the three terms with no percentages, for the same reason as above.
- **'0 µM DOX' is mapped to doxorubicin at 0 µM**, not to a vehicle state, so the dose series stays one contrast on a number.
- **'cardiac organoid' is mapped to platform:cell_aggregate with no synonym added.** Elsewhere, 'cardiac organoid' also names self-organising organoids differentiated in place. 'spheroid' was added as a synonym; in this paper organoid and spheroid differ only in cell_types.
- **'non-adhesive agarose hydrogel molds' (replating_coating)** is really the mold the microtissues self-assemble in, not a coating. I added replating_coating:non_adhesive_agarose. The reader may prefer substrate or platform qualifiers.
- **cell_types 'FBs'** is mapped to cardiac ventricle fibroblast (CL:2000066) because the paper defines the abbreviation that way. 'FBs' was not added as a synonym because it is broader than the term. The hADSCs (CL:0002570) are in cell_types but not in stromal_cell. Is that a reader omission?
- **No MONDO class for ischaemic cardiomyopathy.** I mapped it to {myocardial ischemia MONDO:0024644, cardiomyopathy MONDO:0004994} with `no_ontology_term`. 'non-failing' has no MONDO term, so I used adopt_own disease_model:non_failing_heart.
- **Log-fold changes use the new gene_expression qualifier `scale: log`.** The gene_expression standing key does not require `measure.scale`, so a log fold change could be compared with a linear one. The key needs revising at the next checkpoint.
- **TPM values are `expressed_as: absolute`.** TPM ratios (LDHA/LDHB) are `normalised` to the second gene's TPM.
- **Peak OCR and peak ECAR are normalised to 'non-mitochondrial respiration'.** This comes from the record's method; the figure axis wasn't checked. 'change in elastic modulus relative to control' leaves expressed_as to the printed unit.
- **'cell death' (S14a) has a new measure term, not cell_viability.** It is the complement, and mapping it there would invert directions.
- **The pathway and GO 'enrichment' items are mapped to enrichment_p_value**, because their stated stats are P values.
- **Split request:** for 'gelatin-coated 96-well plates', '96-well plates' goes to platform.

## Formula agent

- **~30 % ECAR increase (F3e) is wired to the Fig. 3f readings.** Code finds it inconsistent: the rebuilt value is 44.7 %. Fig. 3f is normalised to each group's non-mitochondrial respiration. The text cites Fig. 3e,f, and the raw ECAR time course (Fig. 3e) was not read. So the ~30 % may refer to raw ECAR, and the inconsistency may come from the choice of input rather than from the paper.
- **'Approximately twofold' OCR after FCCP (F3c) has an unstated baseline.** The record says OCR before FCCP; Fig. 3c was not read, so the inputs are not stated. The control peak in Fig. 3d is ~198 % of non-mitochondrial respiration, which is also about twofold. The text doesn't say which baseline it means.
- **The S2a Venn diagram is checked against the DE count.** I treated the Venn diagram as stating the partition, so the organoid circle is unique + shared (4,047 + 1,628 = 5,675 = F2a; code says consistent). The Fig. 2b Venn circles for the organoid set give other totals (2,832, 2,290, 4,157), because the Methods exclude genes that are not common to both platforms. No derivation was written for them.
- **Micropipette modulus: proposed a model, `micropipette_aspiration_half_space` (Theret 1988).** It is one more given entry, so the field's count of given entries grows. Nothing is rebuildable: L is not printed, the inner radius is printed only as a diameter range ("approximately 70–80 µm"), and Φ is by reference. It gives a symbolic check and assumption reports. Incompressibility and small aspirated length are not stated.
- **Contraction amplitude (F5g):** the Methods say 'percentage change', but the figure plots fractions (~0.008). I mapped it to relative_decrease, with a ×100 alternative.
- **LFC (Supplementary Tables 3, 4, 6): no formula.** These are software estimates: DESeq2 for the organoids, GEO2R/limma for the mouse. The log base is not stated in the tables, so I wrote 20 derivations marked no_formula. An observation, not a derivation: 2^(LFC_LDHA − LFC_LDHB) = 1.51, which agrees to about 1 % with the ratio of the Fig. 3h LDHA:LDHB TPM-ratio readings (1.031/0.677 = 1.52).
- **Normalisations with no stated reference:** the radial-density intensities (F1f, F4f, F6b, F7c), the TUNEL index (S1b, F7b), and whether 'vehicle control' means a group mean or a per-organoid value. 'Change in elastic modulus relative to the control' (F6c) may be a ratio or a relative difference; both are written, the ratio as an alternative.
- **Spec/gate:** an `output` must be a printed value. Items whose values exist only as figure readings (most of this paper) cannot be judged even when all the inputs are read. The F7e rows (28 items, one measure) each got the same derivation.
