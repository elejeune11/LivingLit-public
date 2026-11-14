# 2020_Feyen — ambiguity log

## Record reader

- **A set whose members sit in different sentences cannot be anchored.** `differentiation_factors` is CHIR99021 and
  C59, named in two sentences; a context anchor must be one contiguous quote of at most 30 words that holds every
  word of the value. I wrote `value: CHIR99021` with `qualifiers: {wnt_inhibitor: C59}`. The same problem forced the
  maturation medium's supplements into `value: "AlbuMAX + creatine + L-carnitine + taurine"` (the Introduction's
  wording) with the twelve components of the Methods formulation as qualifiers, and the EHT control medium into
  `value: "horse serum"` with penicillin/streptomycin, aprotinin and insulin as qualifiers. The schema has no way to
  carry a set whose members are stated in several places, each with its own anchor.
- **Media comparison: how many fields differ.** MM against RPMI/B27 differs in `cm_medium`, `supplements` and
  `maturation_strategy` ("directed metabolic maturation"). I wrote all three per group, so code will call every
  MM-vs-RPMI pair a confound. That is what the paper did (it changed base medium, calcium, glucose and several
  supplements at once, and states that no individual modification sufficed), but a reader could equally have left
  `maturation_strategy` out as a restatement of the medium.
- **Asterisks could not be counted.** Rendering figure pages was not permitted in this session, so I could not read
  how many asterisks each panel carries. Where the text or legend says a difference is significant I wrote
  `p: "p < 0.05 (Methods)"` (the Methods' paper-wide threshold, with its source); where no significance is stated I
  wrote `not stated`. Panels whose only statistics are the asterisks therefore carry the weakest stated threshold,
  not the printed one.
- **Figure 3 has no RPMI/B27 group.** The diastolic potential and upstroke velocity are measured in MM only; the
  comparison with RPMI/B27 is Figure S4A (IK1 and capacitance) and the representative traces of S4D. I kept F3B as a
  one-group unit plus an *other study* group for the adult ventricular values quoted from Chen et al. 2009, and
  judged the Figure 3 title's comparison dimension accordingly.
- **`preparation` for whole EHTs.** No sentence calls an EHT an intact tissue, so functional EHT units carry
  `preparation: not stated`; histology units carry "fixed" and 2D western blots "lysed" (from "lysed in RIPA
  buffer"). The field's declared vocabulary (intact tissue, dissociated cells, fixed, lysate) cannot be used without
  inventing the paper's wording.
- **`mechanical_load` for EHTs** is written "auxotonic" from the Discussion's general sentence about EHTs, not from a
  sentence about these tissues. It is the only place the word appears.
- **Cell line per experiment.** The Key Resources Table lists three healthy-donor SCVI lines, but almost no 2D
  experiment says which line it used, so `cell_line` is *not stated* for the 2D units; only the EHT lines and the
  counts ("two separate iPSC lines", "three HD lines") are stated per experiment.
- **Values printed without their groups.** The glycolytic-capacity ECAR ("17.4 ± 1.7 versus 10.2 ± 0.1") and the EHT
  sarcomere lengths ("1.68 ± 0.02 and 1.90 ± 0.025 µm, respectively") name no group in the sentence that prints them;
  I assigned them in the order of the preceding clause and noted that on the items.
- **Superscripts lost in extraction.** Seeding densities are written as the extracted text prints them ("2x106 per
  well", "2x104 hiPSC-CMs"), because a context anchor is checked against the extracted text.
- **µ extracted as m.** This paper's font extracts µ as m ("3.88 mM" for 3.88 µM, "1mM isoproterenol" for 1 µM). I
  wrote quotes and values with µ, which the matcher's µ→m variant finds; a reader who trusted the extraction would
  record the wrong units by a factor of a thousand.
- **Representative images and gene lists are not units.** Figures 1F, 2A–F (heatmaps), 2B (GO terms), S2C, S3D–G,
  S4D, S5A, S6C–E, 6E, 6F, 6H and the Table S1 primer list carry no measurement of a group; only the gene counts
  printed in the text (1,308 / 368 / 862) are recorded, as counts under F2. Figure S1A (the media composition table)
  and S1B (rationale) are images of a table; their numbers are not in the extracted text, so the culture calcium of
  MM is *not stated* rather than read.
- **`other_conditions`**: the non-failing human heart (positive control) and rat EHT (negative control) lanes of the
  S7G/S7H western blot are conditions of the unit, not groups: nothing is quantified for them, and a rat EHT is
  neither native tissue nor another study's engineered tissue, so no group kind fits.
- **Judging "improves".** Several assertive titles ("Improved Ca2+ Handling", "MM Improves ... EHTs", "MM Increases
  ... Diastolic Membrane Potential") assert a direction over measures whose printed directions differ (lower
  amplitude, lower diastolic calcium, longer time to peak, a more negative potential). I left `asserts_direction`
  unset for those and judged the direction dimension *cannot judge*, except Figure 3's title, where "Increases ...
  Diastolic Membrane Potential" contradicts the more negative value printed: that one is *does not follow*.

## Figures and data reader (unit S4A)

- **No released data**: the paper has no data files, so nothing goes in `data.yaml`. No table and no text prints the S4A values.
- **Fig. S4A read (raster, `figures/s4a.py`), bars only.** Both dot plots (IK1 at -140 mV, cell capacitance) have markers that overlap each other and the mean and error-bar lines, so they are not countable and give no points. The script reads each group's mean line and the upper end of its error bar: IK1 RPMI/B27 -3.83, MM -7.45 pA/pF; capacitance RPMI/B27 37.2, MM 52.6 pF. The legend does not say whether the bar is an SD or SEM, and it gives no n for either group. Axes are calibrated from the detected tick marks; the tick values were typed in from the printed labels. The image is embedded at about 458 dpi but read from a 300 dpi render, and raster uncertainty was measured only at 300 dpi.
- **Fig. S4B (item S4B_ik1_capacitance, MM) not readable.** The right panel (IK1 density against capacitance) has 26 lone markers and 3 pairs of overlapping markers. That makes 32 markers, which matches the printed n=32. Under the raster rule (every marker stands alone) it gives no points. Splitting each pair into two discs of the known marker size would recover all 32 (x, y) pairs; whether to allow that is a design question.
- **Record notes.** (1) S4B prints slope=0.00±0.03, r=0.023, p=0.902 in the panel, but the record has `p: not stated` for S4B_ik1_capacitance. (2) S4B has one MM cell at about 113 pF, but S4A's capacitance axis stops at 100 pF and its highest MM marker is about 75 pF. Either S4A leaves out that cell or the two panels show different cells.

## Figures and data reader (unit F4A)

- **No released data and no table** gives the Fig. 4A western-blot quantification; nothing goes in `data.yaml`.
- **Fig. 4A read (raster, `figures/f4a.py`), bars only.** Each bar (mean ± SEM, legend: "Data are presented as mean ± SEM") carries 3 batch dots (n = 3 batches). The dots are not countable under the raster rule: in SERCA2a and PLN RPMI/B27 the three dots overlap each other, and in the MM groups dots sit on the bar top (SERCA2a, CASQ2) or on the error-bar cap (JPH2). So the script reads bar tops and upper SEM caps only: SERCA2a RPMI/B27 1.00 (cap 1.08), MM 1.93 (2.07); PLN 1.00 (1.04), MM 2.11 (2.32); CASQ2 0.93 (1.11), MM 2.17 (2.48); JPH2 0.89 (1.16), MM 1.61 (1.73). No n can be checked.
- **Unsure:** the PLN RPMI/B27 cap is partly covered by dots; its reading (1.04) rests on the cap ends either side of them. The bar top is read on each bar's left edge columns, which no dot reaches.
- **Axis:** the y axis has no title or unit (ticks 0–3); RPMI/B27 means near 1 suggest values normalised to RPMI/B27, but this is not printed. The x label prints "CASLQ"; read as CASQ2 (item F4A_casq).- **Record note:** the four items print `p: p < 0.05 (Methods)`, but the panel marks SERCA2a ** and PLN ** (p < 0.005), CASQ * (p < 0.05) and JPH2 with no mark (not significant by the legend's convention), although the record's finding states JPH2 was higher in MM.

### Fig. 4C (figure job F4C)

- **No released data and no table** gives the Fig. 4C CTD values; nothing goes in `data.yaml`.
- **Fig. 4C read (raster, `figures/f4c.py`), bars only.** Two bar charts (siSERCA2a left, siPLN right), mean ± SEM, one marker per well (legend: n = 3 batches, n = 3 wells each, so 9 per group). Not countable under the raster rule: in every group read at least one marker touches the bar top, the error line or an SEM cap (black markers on black lines in MM bars). Read: MM siCtr 1.038 (cap 1.078) in the left chart, 1.040 (1.079) in the right; RPMI siSERCA2a 1.123 (1.157); MM siSERCA2a 1.238 (1.268); MM siPLN 0.782 (0.803). RPMI siCtr and RPMI siPLN are in no item and are not read. No n can be checked.
- **MM + siCtr is plotted twice** (once per chart, on different y scales); the two readings agree (1.038 vs 1.040), which suggests the same data were plotted again. Each item reads it from its own chart. MM + siSERCA2a is returned under two labels, one per item.
- **Unsure:** MM bars have a darker outline along the top; the script reads the bar's outer edge (as in Fig. 4A). The midpoint of the upper and lower SEM caps lies 0.35–0.6 px lower (≈ 0.003–0.005 units), about the reading interval, so the outline may be centred on the mean.
- **Axis:** "CTD75-25 normalized"; what it is normalized to is not printed.
- **Record notes:** the F4C unit's `note` ("ratio of the two media's decreases ... significance was calculated for each dose (Fig. 4B legend)") is the Fig. 4B note copied into F4C. The panel marks MM siSERCA2a vs RPMI siSERCA2a with * (p < 0.05), and MM siSERCA2a vs siCtr and MM siPLN vs siCtr with †† (p < 0.005); the items print only `p < 0.05 (Methods)`. The panel also marks siPLN RPMI vs MM ** (p < 0.005), and the record has no item for that comparison.

## Figures and data reader (unit F5C)

- **No released data** for Fig. 5C (no data files); read from the figure.
- **Fig. 5C read (raster, `figures/f5c.py`), points and bars.** Only the two maturation-media bars (RBM20-WT `mm_wt`, RBM20-R634Q `mm_mut`) are read, the groups `figures-needed` lists; the RPMI/B27 bars are not read (item F5C_media, which compares mm_mut with rpmi_mut, is not in the job).
- **Counted points vs printed n:** 3 dots per group, printed n = 3 batches. MM R634Q: 12.43, 8.237, 6.165 (their mean 8.94; bar 8.95; SEM from points 1.84, read upper SEM end 10.77, i.e. 1.82). MM WT: 0.897, 1.105, 1.024.
- **Unsure (countability):** the dots stand apart from each other, but touch lines: all three MM WT dots sit on the black band of the mean and SEM caps, and the middle MM R634Q dot sits on the vertical error line. The spec rule ("raster counts are used only when every marker stands alone") is read here as markers not overlapping each other; Figs. 4A and 4C were read more strictly (bars only when dots touch bar tops or caps). Dots are located from per-column chords 4-10 px long, which skip the 3-px band and caps and the > 30-px error line, so a line through a dot does not pull its centre. The R634Q check (points mean and SEM vs bar) agrees to within 0.02.
- **MM WT bar:** mean and both caps merge into one black band (~3.5 px); its mean is the band centre (0.972) with the band edges as interval (0.78-1.16); no error end read. The points' mean (1.009) lies inside.
- **Axis:** "Fold increase normalized to total TTN"; ticks 0, 5, 10, 15.
- **Record note:** the panel marks R634Q vs WT ** in both media (p < 0.005); the item prints only `p < 0.05 (Methods)`.

## Figures and data reader (unit F5I)

- **No released data and no table** gives the Fig. 5I baseline APD75 values; nothing goes in `data.yaml`.
- **Fig. 5I not read; recorded as `no_points`.** The panel is a raster bar chart (mean ± SEM) with one marker per well (journal_version.pdf p. 8, about x 430–538, y 222–272 pt). No compared group has markers that all stand alone: HD2 MM markers overlap each other in a chain; HD1 MM markers touch each other and the bar top; F1473C RPMI/B27 grey markers sit on same-grey SEM caps and the bar top; F1473C MM black markers sit on the black error line, caps and mean line. So neither item (mm_lqt vs mm_hd, mm_lqt vs rpmi_lqt) could get points on both sides, and bar readings feed no check.
- **Unsure:** F1473C MM shows 9 markers (6 circles, 3 triangles; consistent with 2 batches, 3–6 wells each), and per-column chords (as in Fig. 5C) might locate them despite the lines; not attempted, since its comparators are not countable.
- **Record note:** the figure plots the three HD lines as three separate bars (HD1, HD2, HD3 MM), while the record has one group `mm_hd`; points for `mm_hd` would pool three lines. The panel marks *** (p < 0.0005) for F1473C MM vs the others; the items print only `p < 0.05 (Methods)`.

## Figures and data reader (Fig. 5J)

- **No released data and no table** gives the Fig. 5J values; nothing goes in `data.yaml`.
- **Read: `f5j`** (raster, journal_version.pdf p. 8, crop 440–537 × 270–309 pt). F1473C MM only: 3 black triangles on the bar fill and 6 black circles below the bar stand alone; 9 points (legend: 2 batches, n = 3–6 wells each, so 3 + 6 fits). Bar mean −487.2 and upper SEM end −441.3 (the error bar's upper cap lies inside the bar). The points' mean (−488.4) and SEM (45.3) agree with the bar (−487.2, 45.9). Returned under two labels, one per item (F5J_lqt_vs_hd, F5J_lqt_media).
- **Not read:** HD1, HD2, HD3 (MM) and F1473C RPMI/B27. Their markers sit on the dotted zero line, the mean lines and the caps and touch each other, so they are not countable; no bars read (they would feed no check). So neither F5J item has points on both sides, and no check runs from this panel.
- **Unsure:** triangle positions are the middle of each marker's box; the triangle's centroid lies ~1 px lower (≈ 8 ms), and the interval covers both. The bar mean is the fill's bottom edge with 1 px added to its interval for the bar border. The y axis prints no unit; `ms` is from the legend ("APD75 shortening times (ms)").
- **Record note:** the record's `mm_hd` is three separate bars here (HD1–HD3), and the item's `rpmi_hd` group does not appear in Fig. 5J (only F1473C is shown in RPMI/B27).

## Figures and data reader (unit F6C)

- **No released data and no table** gives the Fig. 6C values (force normalized to ctr, spontaneous BPM); the text gives directions only. Nothing goes in `data.yaml`.
- **Not read (no_points):** Fig. 6C is a raster image (~300 dpi, journal_version.pdf p. 9) of two bar charts (mean ± SEM) with one marker per EHT (3 batches: circles, squares, triangles). In all four groups (force ctr/MM, BPM ctr/MM), some markers touch the mean line, the SEM caps, the vertical error line or each other (grey markers on same-grey lines in ctr; black on black in MM), so they are not countable under the raster rule. No script; recorded under `no_points.F6C` in `figures.yaml`.
- **Unsure:** I counted roughly 13–14 MM force markers by eye against printed n = 14–18; a marker hidden under the error line cannot be ruled out, which is part of why the panel is not countable. Mean and SEM bars were not read, since no check uses them.

## Figures and data reader (unit F6D)

- **No released data and no table** gives the Fig. 6D TTP80% values; the text and legend give the direction and the significance only. Nothing goes in `data.yaml`.
- **Not read (no_points):** the TTP80% chart in Fig. 6D is a raster image (~300 dpi, journal_version.pdf p. 9): bars (mean ± SEM) with one marker per EHT (3 batches). Control grey markers merge with the same-grey upper SEM cap. The black MM markers separate only at a strict darkness threshold: there is no fill-level gap between two stacked circles (~0.19 s), two stacked triangles (~0.147 s), or a triangle and the lower SEM cap (~0.168 s). That fails the standing-alone rule, so there is no script; the panel is recorded under `no_points.F6D` in `figures.yaml`.
- **Mismatch:** MM shows 10 markers (1 square, 4 circles, 5 triangles), counted from the pixel dump, against the printed n = 9 (legend "n = 9, 3 batches"). It is unclear whether n = 9 applies per group.
- **Unsure:** with a darkness threshold of 60 (as in the Fig. 5J script), all MM markers would come out as separate blobs. I judged abutting markers as not standing alone. MM-only points would not let a check verify the MM vs ctr test anyway.
- The RT80% chart (item F6D_rt) was not in this job's unit list and was not looked at for reading.

## Figures and data reader (unit S2B)

- **Released data / tables:** none gives the cTnT mean fluorescent intensity (item S2B_cTnT_mfi); the text and legend give the direction only. Nothing goes in `data.yaml`.
- **Read:** `figures/s2b.py`, the right chart of Fig. S2B (mmc1.pdf p. 4, raster: the whole page is one image). 4 circles per group, matching the printed n = 4 batches. Point means (29.8k RPMI/B27, 87.8k MM) agree with the bar tops (29.6k, 87.7k). Bar-to-cap distances (6.2k, 8.3k) equal the SEM of the points (5.9k, 8.2k), consistent with Methods (mean ± SEM).
- **Unsure:** in each group, one circle sits on the upper cap and one on the vertical error line or lower cap, in the same colour as the circle. I judged them countable as in F5C (the circles are apart from each other, and only lines cross them). The lines (2–5 px) are removed by a 9 px opening, and each centre is checked against the chords in the columns 4 px either side, outside the vertical line. The interval covers both estimates.
- **Unit:** the y axis has no unit ("cTnT mean fluo. intensity", arbitrary units).
- The left chart (% cTnT-positive, item S2B_purity) is not read: its values are printed in the Results.

## Figures and data reader (unit S2D)
- **Released data / tables:** none gives the ATP production values (item S2D_atp); the legend gives the direction only. Nothing goes in `data.yaml`.
- **Read:** `figures/s2d.py`, the ATP Production pair of the Fig. S2D bar chart (mmc1.pdf p. 4, raster). 4 markers per group, matching the printed n = 4 batches. Point means (54.3 RPMI/B27, 156.5 MM) agree with the bar tops (53.7, 155.6). Bar-to-cap distances (19.2, 11.3) equal the SEM of the points (18.7, 11.2), consistent with mean ± SEM.
- **Unsure:** markers touch error-bar lines in the same colour. RPMI/B27 has one square on the vertical line and lower cap. MM has one circle on the upper cap, one touching it, and two on the lower cap. I judged them countable as in S2B and F5C: the markers are apart from each other, and only lines cross them. The lines are removed by a 9 px opening, and a chord that runs into a line is skipped.
- **Calibration:** the y axis has no tick marks, so it is calibrated from the vertical centres of the six tick labels (1000–0). This may shift values by about 1–2 pmol/s*ml. The calibration misfit is inside the intervals.
- **Unit:** the bar chart's axis says "OCR (pmol/s*ml)". The time-course chart beside it says pmol/min. The record's item does not give a unit.
- **Not read:** basal respiration, maximal respiration and proton leak, because no record item rests on them. The legend sentence also claims higher respiration after uncoupling (maximal respiration), but the record has no item for that.

## Figures and data reader (unit S5D)
- **Released data / tables:** none gives diastolic calcium per group (item S5D_diastolic); the Fig. S5D and Fig. 4E legends give directions only. Nothing goes in `data.yaml`.
- **Not read (no_points):** the Diastolic Calcium chart of Fig. S5D (mmc1.pdf p. 10, raster: the whole figure is one image) is a bar (mean ± error bar) with a dense beeswarm of one marker per cell in each group, on the order of 90 markers per group. The markers touch and overlap each other and the same-colour error-bar lines, so the panel is not countable under the raster rule. There is no script; it is recorded under `no_points.S5D` in `figures.yaml`. No bar mean was read, since no check uses one.
- **Mismatch (count):** each swarm looks much larger than the printed "2 batches, n=39-48 cells each". Possibly n is per batch, but this was judged by eye and not counted.
- **Record problem (direction):** the chart puts RPMI/B27 above MM, with *** over the pair, and the Fig. 4E legend says "lowered ... diastolic Ca2+ levels in MM". Both contradict the S5D legend's "Diastolic calcium was significantly increased in MM" (stated_direction up). This supports the record's suspected_error. The direction was judged by eye and is not a result.
- The Non-SERCA Tau and SR Load charts in the same panel (items S5D_tau_nonserca, S5D_srload) were not in this job's unit list. They are the same kind of dense raster beeswarm.

## Figures and data reader (unit S6B)
- **Released data / tables:** none gives the adult/fetal SCN5a ratio (item S6B_scn5a); the legend and Results give the direction only. The paper has no data files. Nothing goes in `data.yaml`.
- **Read:** `figures/s6b.py`, Fig. S6B (mmc1.pdf p. 12, raster: the whole page is one image). 4 circles per group, matching the printed n=4 batches. Point means (5.42 RPMI/B27, 13.24 MM) agree with the bar tops (5.41, 13.24). The y axis is calibrated from its five tick marks (20–0).
- **Mismatch (error bar):** the bar-to-cap distances (2.81 RPMI/B27, 1.72 MM) equal the SD of the points (2.79, 1.74), not their SEM (1.39, 0.87). The Methods say data are mean ± SEM, and the S6 legend does not say. These bars look like SD; S2B and S2D matched SEM.
- **Unsure:** circles touch error-bar lines in the same colour. RPMI/B27 has one on the vertical line and one on the lower cap. MM has one touching the upper cap, one on the vertical line, and one at each end of the lower cap. I judged them countable as in S2B and S2D: the circles are apart from each other, and only lines cross them. The lines (~3 px at 300 dpi) are removed by a 9 px opening, and a chord that runs into a line is skipped.
- **Stats:** the chart shows ** over the pair (p < 0.005 by the Methods' key), while the record's stats give "p < 0.05 (Methods)". No test is named.

## Figures and data reader (unit S6F)
- **Released data / tables:** none gives absolute Gmax (item S6F_gmax). The legend gives only a non-significant elevation and prints no n. The paper has no data files, so nothing goes in `data.yaml`.
- **Read:** `figures/s6f.py`, Fig. S6F (mmc1.pdf p. 12, raster: the whole page is one image). 9 RPMI/B27 and 7 MM circles, one per cell; no printed n to check against. Point means (34.75 RPMI/B27, 50.85 MM) agree with the bar tops (34.75, 50.95). Bar-to-cap distances (6.48, 14.02) equal the SEM of the points (6.44, 13.99), as the S6 legend says (mean ± SEM). The y axis is calibrated from its four tick marks (150–0).
- **Unsure:** circles touch error-bar lines of their own colour. RPMI/B27 has one on the vertical line at the bar top, one at each end of the lower cap, and one touching the upper cap. MM has one on the vertical line, one where it meets the lower cap, and one touching the lower cap's right end. I judged them countable as in S6B, S2B and S2D: the circles are apart from each other, and only lines cross them. Each opened blob has the area of one circle, and the script fails on any blob over 140 px. The two MM circles near 37–38 nS sit side by side, 24 px apart.
- **Note on S6B:** the S6 legend (mmc1.pdf p. 13) ends "Data was presented as mean ±SEM". The S6B entry's "the S6 legend does not say" is therefore wrong, and its SD-like error bars disagree with the legend as well as the Methods.
- **Stats:** S6F prints no test or p value beyond "non-significant", and the chart has no bracket.

## Figures and data reader (unit S6G)
- **Released data / tables:** none gives capacitance per group for item S6G_cm. The paper has no data files, and the legend gives only the direction ("significantly higher"). The Methods' "Cell capacitance was 56.8 ± 3.1 pF (n = 44 cells)" belongs to the IK1 recordings and pools both groups, so it is not an S6G value. Nothing goes in `data.yaml`.
- **Not read (no_points):** Fig. S6G (mmc1.pdf p. 12, raster: the whole page is one image of about 280 dpi) is a bar chart (mean ± SEM per the S6 legend) with one filled circle per cell, and the legend prints no n. Under the raster rule the markers do not stand alone. RPMI/B27 grey circles merge with each other in pairs and triplets near 17 and 20 pF, and they crowd onto the same-grey mean line and caps near 5–13 pF. MM black circles touch in vertical pairs, below the lower cap and between the caps, and sit on both black caps. There is no script; the panel is recorded under `no_points.S6G` in `figures.yaml`.
- **Stats:** the chart shows ** over the pair (p < 0.005 by the legend's key), while the record's stats give "p < 0.05 (Methods)".
- **Correction:** the S6F entry says "~490 dpi" for this page image. The image is 2393 px across an 8.5 in page, about 280 dpi.

## Figures and data reader (unit S7C)
- **Released data / tables:** none gives mt-DNA content per group for item S7C_mtdna. The paper has no data files, and the legend gives only a direction ("significant tendency"). Nothing goes in `data.yaml`.
- **Read:** `figures/s7c.py`, Fig. S7C left panel (mt-DNA ND1/g-actin; mmc1.pdf p. 14, raster: the whole page is one image of about 400 dpi, rendered at 600 dpi). It finds 10 ctr and 9 MM markers, one per EHT, with shape marking the batch (circles, squares, triangles, diamonds). The legend prints no n to check against. Point means (200.7 ctr, 267.0 MM) agree with the bar tops (200.7, 266.7). Bar-to-cap distances (27.2, 46.6) are close to the SEM of the points (26.0, 46.2), as the S7 legend says (mean ± SEM). The y axis is calibrated from its five tick marks (800–0).
- **Unsure:** markers touch error-bar lines of their own colour. In ctr a diamond sits on the upper cap's right end and another on the lower cap's left end. In MM a diamond sits on the vertical line and a circle on the lower cap. I judged them countable as in S6B and S6F: no marker touches another, and the lines (~4 px at 600 dpi) are opened away with a 9 px disc, leaving one blob per marker. The script fails if an opened blob is larger than one marker. Earlier entries (F4A, F6C) treated markers on caps as not standing alone, so the shared rule is applied unevenly across this paper.
- **Unsure:** a marker's position is the middle of its vertical extent. For triangles that point differs from the area centroid by about a sixth of the marker's height (~3 units here), and each interval covers both.
- **Not read:** the right panel (mt-DNA ND2/g-actin). The record has one item, S7C_mtdna, covering ND1 and ND2, with groups mm/ctr only. Linking ND2 readings to the same groups would pool two measures into one set of points. Record problem: S7C should probably be split into ND1 and ND2 items (or the item should name ND1).
- **Note:** the MM top triangle (598.6) is far above the other MM points (160–371). It is kept as read and not marked suspect, because nothing suggests it is a stray symbol.

## Figures and data reader (unit S7E)
- **Released data / tables:** none gives average force per group for item S7E_force. The paper has no data files, and the legend and Results give only the direction. Nothing goes in `data.yaml`.
- **Not read (no_points):** Fig. S7E (mmc1.pdf p. 14, raster: the whole page is one image of about 400 dpi) has six bars, ctr and MM for each of batch1–3. Each bar shows mean ± error bar with one marker per EHT (legend n=3-8 EHTs). Under the raster rule the markers do not stand alone in batch1 MM (circles on the black mean line and cap), batch3 ctr (triangles overlapping each other on the same-grey lines) or batch3 MM (triangles on the caps, touching each other). The batch2 ctr squares also sit on the same-grey error line. The record's groups pool all batches (ctr, mm), so no group can be counted in full. There is no script; the panel is recorded under `no_points.S7E` in `figures.yaml`.
- **Unsure:** batch2 MM (6 squares, one on the error line) and batch1 ctr (3 circles) could be read on their own. A partial per-batch reading would not be the record's pooled group, so I left them unread. Compared with S7C (markers on caps judged countable after opening the lines), the line is drawn here because markers also touch each other.
- **Record problem:** the record's groups pool three batches whose force levels differ by about 3x (batch3 ~0.1 mN vs batch1–2 ~0.2–0.4 mN). Significance is marked per batch (** for batch1 and batch3 only; batch2 has no bracket), so "p < 0.05 (Methods)" for the pooled comparison is not what the chart shows.

## Figures and data reader (unit S7F)
- **Released data / tables:** none gives beat rate per group for item S7F_beatrate. The paper has no data files, and the text gives only the direction. Nothing goes in `data.yaml`.
- **Read:** Fig. S7F (mmc1.pdf p. 14, raster: the whole page is one image of about 406 dpi), script `figures/s7f.py`. It has six bars (ctr and MM for batch1–3), mean ± SEM, one marker per EHT. Each batch bar is its own label (`ctr_b1` … `mm_b3`) mapped to group ctr or mm, so each pooled group gets all of its points: ctr 3+8+7 = 18, MM 3+6+5 = 14. Each batch count is within the printed "n=3-8 EHTs"; no pooled n is printed.
- **Countable judgement:** at 600 dpi, no marker touches another marker. Some sit on error-bar lines of their own colour: ctr b1 circle on the upper cap, ctr b2 square on the vertical line, ctr b3 triangle on the lower cap, MM b2 square on the vertical line, and MM b3 two triangles at both cap ends. Those components are opened with a 7 px disc (lines are 2–3 px), as was done for S7C. S7E, on the same page, was judged not countable because its markers touch each other. In S7F they do not.
- **Checks:** for circles and squares (b1, b2), the point means agree with the bar tops within 0.1 BPM. In every bar, the SEM of the points agrees with the distance from bar top to cap (e.g. MM b2 7.77 vs 7.79; MM b3 0.95 vs 0.97).
- **Unsure:** for the triangles (b3), the point means sit about 0.5 BPM (about 2 px) below the bar top in both groups: ctr 42.05 vs 42.53, MM 26.52 vs 27.02. GraphPad probably anchors the triangle at or slightly above its box middle. The reading takes the midpoint between box middle and centroid, and its interval covers the box middle only just. I did not tune the reading to remove this.
- **Record problem:** significance is marked per batch (* batch2, ** batch3, none for batch1), but the record's groups pool all three batches and give "p < 0.05 (Methods)". The pooled comparison is not what the chart tests.

## Figures and data reader (unit S7H)
- **Released data / tables:** none gives β-MHC/cTnT per group for item S7H_bmhc. The paper has no data files, and the legend and Results give only the direction. Nothing goes in `data.yaml`.
- **Read:** Fig. S7H right panel (b-MHC/cTnT normalized to the mean of control EHTs per batch; mmc1.pdf p. 14, raster, whole page one image of about 406 dpi, rendered at 600 dpi), script `figures/s7h.py`. It finds 5 ctr and 5 MM circles. The legend prints "3 batches, n=2-4 EHT each" (per batch, both groups together). The S7G blot shows 2+1+2 lanes per group, which gives 5 per group and agrees with the count. All markers are circles, so the batch of each point cannot be recovered. The y axis is calibrated from its five tick marks (2.0–0.0).
- **Countable judgement:** no marker touches another marker. Three ctr circles sit on the grey error bar (upper cap, vertical line, lower cap) and two MM circles on the black one (upper cap, vertical line). Lines are about 8–9 px and circles about 24 px at 600 dpi, so those components are opened with a 15 px disc, the same approach as S7C and S7F. Where an opened blob is taller than the smallest stand-alone circle, the interval covers every centre such a circle could have.
- **Checks:** ctr point mean 0.999. This is 1.0 as the normalization implies (each batch's ctr mean is 1). MM point mean 1.351. Cap minus point mean (ctr 0.095, MM 0.120) equals the SEM of the points (0.094, 0.118).
- **Unsure / figure inconsistency:** in both bars the bar top is drawn about 5.5 px (about 0.017 units, 0.66 pt) below the midpoint of the two SEM caps. For ctr, the bar top is at row 396.8 and the caps' midpoint at 391.5. So the bar means read 0.981 (ctr) and 1.334 (MM), against point means 0.999 and 1.351. The error bars are centred on the point means, so the offset is in how the bars are drawn, not in the reading. I did not tune anything. The offset lowers the audit's "n implied by error bar" (3.5 and 3.8 from bar-to-cap, against 5 points).
- **Not read:** the left panel (a-MHC, item S7H_amhc) was not listed by `figures-needed` for this job.
- **Record note:** the audit parses the printed n "n=2-4 EHT each" as [2, 3]. The legend's n is per batch across both groups, not per group.

## Vocabulary agent

Vocabulary version 32; instructions terms_v4.

- **Flags (7).** *not a context* (3): preparation `monolayer` names the platform, not a preparation (it appears in 12 units; split request to platform). Treatment `EdU` and treatment `wheat germ agglutinin–Alexa Fluor 488 conjugate` are assay labels applied to every group, so they belong to the method. *placeholder* (3): day_of_measurement `last day of culture`, `last week of culture` and `after three weeks of culture` give no day of culture. *several measures* (1): `diastolic membrane potential and AP upstroke velocity of adult ventricular myocytes`.
- **Quantity values code accepts but that look wrong (not flagged; the gate cannot see them):** donor_age `two healthy female volunteers` gives sex and health, not an age. time_point `4h, 24h and at the time of re-feeding` names several time points (several conditions). number_of_lines `three HD lines` and `two separate iPSC lines` parse only because of the number word.
- **Cell line:** the methods print both `UKEi003-C/ERC018sv1634` (certificates) and `UKEi003-A/ERC018sv1634` (batch 2). In Cellosaurus, ERC018sv1634 is UKEi003-C (CVCL_A8PV); UKEi003-A is ERC018sv1583. I kept UKEi003-C. An own term `cell_line:erc018_ipsc` (ERC018, clone not stated) already exists from an earlier paper. It may be the same donor.
- **Unsure mappings:**
  - `diastolic membrane potential` became a synonym of *resting membrane potential*, not *maximum diastolic potential*. The paper measures it "just prior to the AP" in paced cells.
  - `slope of the decay phase of the calcium transient duration (CTD75-25)` is a thapsigargin-induced change. I mapped it to the new *calcium transient duration* with level CTD75-25 and did not add a slope term.
  - `maximum APD75 shortening by mexiletine` is a difference in ms from control wells. No `expressed_as` value fits a difference, so I left it to the values.
  - `fetal TTN isoform expression` (qRT-PCR) went to *gene expression*, not *isoform fraction*.
  - `adult/fetal SCN5a expression ratio` went to *gene expression* with `normalised_to` fetal isoform.
  - `phospho-PLN expression` went to *protein level*, because the paper does not say it is divided by total PLN.
  - `beating response to TTX` went to *presence of beating*. Its printed 100 µM is the highest dose tested, not a value.
  - `maximal contraction/relaxation rate` (nN/(µm s)) got new children of the force-rate terms because the dimension differs.
- **Platforms:** well plates, the XF96 well and coverslips map to *2D culture* with a new `format` qualifier, not to *monolayer*. Patch-clamp cells were plated at low density.
- **Ba2+:** mapped, not added as a synonym, because `+` is a field separator. The same applies to any ion written with a charge.
- **Spec gaps:** there is no flag kind for a quantity written in words relative to an unstated start ("after three weeks of culture"), so I used *placeholder*. adopt_own takes a `scope` (needed for root siblings), but the brief does not list it.

## Formula agent

- **"30% higher spare and maximal respiration":** one printed percentage covers two items. Both derivations point at the single value `F1C_spare.values.spare_pct`. Code rebuilds 39.8 % (spare) and 37.4 % (maximal) relative to RPMI/B27, so both come out inconsistent. Taken relative to MM they are 28.5 % and 27.2 %, which is still not 30 %. These are observations for code, not corrections.
- **"MM enhanced ECAR by 40%":** the printed means (12.3 against 6.3) give +95 % relative to RPMI/B27, or 49 % relative to MM. Neither reading gives 40 %. The 40 % may come from different values than the ones printed beside it.
- **Which medium is the reference** for "% higher" is not stated. I took RPMI/B27 as x0 and listed the other reading as a labelled alternative.
- **SR load/amplitude:** I took the denominator to be the paced transient amplitude, `F4E_amplitude`, from the same cells and figure. The paper does not say this.
- **Fold values (F4B 2-fold, S5B 3-fold):** these are ratios of two effects. The paper does not say how each effect was formed (a difference or a ratio to its control), so the inputs are not stated.
- **Normalised values with no printed output** (F6B, F6C, S7H, S7B, S6B, F5J, F4C): I wrote these where the methods state the operation, but none can be checked. S7H and F6C are normalised to the batch control mean, so the control mean should be 1 (`normalized_to_own_control`). The S7H control reading has a mean of 0.981. A derivation's `output` can only be a printed value, not a reading, so this check cannot be expressed. This is a spec gap.
- **F4C "CTD75-25 normalized"** and **F4A** (an axis with no title) name no reference, so I wrote no derivation for them. **S4A** IK1 density per group (the readings give capacitance but not the IK1 magnitude) is left out for the same reason: it cannot be rebuilt.
- **F5C:** the qPCR method gives TBP as the reference "unless stated otherwise", but the figure axis says normalised to total TTN. I used the ΔΔCt model and added a note.
- **DMFM tension and the Boltzmann Gmax fit** have no closed form, so they are marked `no_formula`.

## Figures and data reader (unit S4A, second job: S4B_ik1_capacitance/mm)

- **No released data and no table** gives the S4B per-cell values; nothing goes in `data.yaml`.
- **Fig. S4B not readable; unit S4A marked `no_points`.** I rechecked the earlier finding in memory, without writing any render: on a 300 dpi render, lone markers are blobs of ~54 px², and several blobs are merged pairs (~97–106 px², up to 14×14 px boxes). Not every marker stands alone, so under the raster rule there are no points, and the 32 markers cannot be counted against the printed n=32. The panel prints only its regression fit (slope=0.00±0.03, r=0.023, p=0.902). The record has `p: not stated` for this item (record note, repeated from above). Splitting merged pairs into two discs of the known marker size would recover all the points. That is still the open design question.
- `mark_no_points` re-dumped `figures.yaml`, so some notes were rewrapped. Their content did not change.

## Figures and data reader (unit F5J, second job: F5J_lqt_vs_hd/mm_hd, F5J_lqt_media/rpmi_lqt)

- **No released data and no table** gives the Fig. 5J values. Nothing goes in `data.yaml`.
- **The existing `f5j` reading is kept.** It is F1473C MM: 9 points, with the bar mean and the upper SEM end. It was rerun by the gate and still passes.
- **The remaining groups are not readable, so unit F5J is now marked `no_points`.** I checked pixel darkness in memory and wrote no render, because /tmp was not writable in this session.
  - RPMI/B27 F1473C: the grey markers (~130) sit in a light bar fill (~75) and touch the bar border, the dotted zero line and the bar-bottom line.
  - Only 2 triangles are visible against a printed 3–6 wells per batch, so at least one marker is hidden and the bar cannot be counted.
  - HD1–HD3: the markers merge with the dots of the zero line.
- **So neither F5J item has points on both sides, and no check runs from this panel.**
- **Record issue (repeated):** `mm_hd` is three separate bars (HD1, HD2, HD3) in the figure, not one group.

## Vocabulary agent (re-map against vocabulary v52)

- **The record has not changed since the first mapping (v32).** Every earlier mapping and edit still passes, so this re-map only removes what later versions made redundant.
- **Removed one stored mapping:** `extracellular acidification rate (ECAR)` is now matched by code to `measure:extracellular_acidification_rate`, and matches are never stored.
- **Checked later terms as refinements and applied none:**
  - `measure:contraction_displacement` (v43) is for lengths; F5D prints "contractile divergence", a unitless motion metric, so it stays on `measure:contraction_motion_amplitude`.
  - `measure:beating_construct_fraction` (v43) is a share of constructs; F1B describes whether one culture keeps beating under TTX, so it stays on `measure:beating_presence`.
  - The new 2D platforms (micropost array, Boyden chamber, muscular thin film, porous insert) and the new DMEM variants do not describe plates, coverslips or "DMEM without glucose".
  - `measure:glycolytic_rate` and `measure:ecar_time_course` do not fit the basal ECAR value in F1D.
- **`vocabulary_version` set to 52**, the version this re-map saw. The earlier edits are already logged; code appends only edits that are not yet in the log.

## Vocabulary agent (re-map against vocabulary v68)

- **Stored mapping removed:** `measurement_medium` "bath solution" is now matched by code (a later paper's synonym on `measurement_medium:extracellular_solution`), so the mapping is no longer stored.
- **Refined to a term added since v52:** "lactate production / glucose consumption ratio" now maps to `measure:lactate_glucose_yield` (2017_Correia), not `lactate_production` normalised to glucose consumption.
- **Qualifiers tidied:** fetal TTN and the adult/fetal SCN5A ratio now carry `gene: TTN` / `gene: SCN5A` with the isoform in `isoform`, so a "same gene" key can match them. I left the SCN5A ratio on `measure:gene_expression` (with `normalised_to`) rather than `measure:gene_expression_ratio`: that term is for two genes, and these are two splice isoforms of one gene. This choice is open to a later re-map.
- **New flags on values code reads as quantities only because they contain a number:**
  - `donor_age` "two healthy female volunteers" is flagged *not a context*. It gives a donor count and sex, not an age, so the reader should state the age or leave it not stated.
  - `time_point` "4h, 24h and at the time of re-feeding" (S7A) is flagged *several conditions*. It names three sampling times, and each value or group should carry its own.
- No library edits were needed. The earlier edits and standing keys are already logged, and `vocabulary_version` is set to 68.
