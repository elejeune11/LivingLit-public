## Record reader

- **Which field holds the media.** The paper's contrast is SM against MM, a *medium* that is also the *maturation intervention*, and the drugs it applies during measurement are a second kind of exposure. `treatment` cannot hold both without colliding (the pharmacology units vary the drug inside a unit whose groups already differ in the medium). I put the pre-treatment media in `maturation_strategy` (value "Maturation Media" / "standard media", with glucose, galactose, oleic acid, palmitic acid and BSA as qualifiers) and left `treatment` for the drugs (isoproterenol, verapamil, flecainide, alfuzosin, ryanodine, thapsigargin, FCCP). `cm_medium` is "glucose free RPMI" everywhere, the base all media were made from. The field note for `cm_medium` says energy substrates go to "supplements or treatment", so this is a deliberate departure.
- **Where the screen's groups are.** In Extended Data Fig. 2b–f each plotted point is one *level* of one media component in an L9 orthogonal array (n = 9 MPS per point), not one medium; the groups of ED2BF are therefore levels (glucose 25/10/0 mM, …) and the printed ANOVA P values are recorded as omnibus items over the three glucose levels or the two printed BSA levels. The axes print three levels but only the ends are labelled, so the BSA items name two groups.
- **Context stated only inside a figure.** Media compositions for the screen levels and for M1–M4 are printed in tables drawn inside the figures, not in extractable text. I anchored those values to their unit (`kind: unit`) rather than leaving them *not stated*.
- **Brackets without named pairs.** Most P values are printed over brackets in figures. Where a bracket's ends were unambiguous I wrote a pair; where the Fig. 2e bracket runs from the MM MPS bar to a bar spanning *both* 2D groups I wrote one omnibus item instead of guessing a pair. The Fig. 8g verapamil and alfuzosin brackets span all three bars of their cluster; I read their ends as 2D SM and MPS maturation media and said so in a note.
- **Counts never stated.** `number_of_lines` is "not stated" everywhere except Extended Data Fig. 4 ("all four genotypes"), and `wnt_inhibition_days`, `insulin_day` and `cm_day_at_formation` are "not stated": each could be computed from protocol days, which the spec forbids.
- **Simulations left out.** Fig. 6d–l (simulated IKr, IK1, INa, ICaL, INaCaX, calcium buffer, RyR flux, diffusion, SERCA, each with a printed post-hoc Tukey P) are model outputs from an inversion of the measured waveforms, so by 02-audit they are neither groups nor items. Fourteen printed P values are therefore not in the record. The same holds for Extended Data Fig. 7 (representative traces only).
- **Conflicting printed numbers.** Glucose in MM is "0.5g/L (2.75mM)" in one sentence and "0.5 g l−1 (2.8 mM)" in another, and Table S1 says 2.75 mM; I kept the printed "0.5 g/l". Palmitate for Media 8, Media 9 and MM differs between Table S1 and the tables drawn under Extended Data Fig. 2g,h, and Extended Data Fig. 3's legend names MM as the reference for M2 and M3 while the brackets run from SM. Each is recorded as a `suspected_error`, nothing corrected.
- **Doses that look wrong.** "Saturating ryanodine (10 mM)", "10mM Thapsigargin" and the Supplementary Fig. 7 "1mM flecainide" (1 μM in the main text) are flagged, not changed.
- **No by-reference values.** Every protocol the paper cites ("as described previously") is also given in full in its Methods, so nothing resolved to `by_reference`.
- **Representative values.** The cAPD80 numbers inside the Fig. 2a–d traces (580, 300, 260, 300 ms) are one tissue each, not group means; they are recorded as `kind: value` with a note, since the figures reader cannot read them from points.
- **Purity percentages.** 98.0 / 99.7 / 85.5 % sit inside flow-cytometry quadrants of one representative batch while n = 3 and the SD belong to the time course in the next panel; I recorded the three percentages as an image-anchored item and noted the mismatch.
- **Schema gap.** There is no place to say that two groups of a unit are pooled in one bar (Extended Data Fig. 6c and Supplementary Fig. 3 plot WTC and SCVI20 points in the same bar). I wrote `cell_line: "WTC + SCVI20"` for those groups, which a vocabulary agent will have to split.

## Figures and data reader

### ED2GH (Extended Data Fig. 2g,h; journal_version.pdf p. 20)
- **No data.** The supplement .docx tables are media formulations, antibodies and primers; no released values for g,h. Read from the figure.
- **Raster.** The page is one embedded ~300 dpi image with no extractable text. Axes are calibrated from the tick marks found in the render, paired with the printed labels 0.8 to 0.0 (misfit < 0.0004).
- **One entry per item.** A figure group links to one item, and Standard Media serves three items (ED2G_m7, ED2G_m8, ED2H_mm). So there are three entries (`ED2G_m7`, `ED2G_m8`, `ED2H_mm`); the two g entries share a crop.
- **Standard Media (g and h): mean and SD only.** In g, the red squares make 11 blobs, one of them two touching squares (12 markers, n = 12 printed). In h they make 8 blobs, two of them pairs (10 markers against n = 12 printed: two SM tissues apparently gave no interval). Because markers touch, there are no points. Read: g mean 0.307, SD upper end 0.492; h mean 0.410, upper end 0.522. The lower ends (0.122; 0.299) are symmetric.
- **Upper caps hidden.** The upper SD caps of Standard Media (g) and Maturation Media (h) are partly hidden behind markers. They are read from the cap fragments either side of the marker.
- **Media 7: mean and SD only.** Its black squares lie on its black bar. Mean 0.015, upper end 0.041.
- **Media 8: nothing read.** Four touching black triangles at 0 cover the mean and SD lines. ED2G_m8/m8 has no reading.
- **Maturation Media (h): 9 points.** Each circle stands alone (n = 10 printed). The points give mean 0.203 and SD 0.096, against the bar's 0.203 and 0.094, so the 10th point is probably hidden near the mean.
- **Media tables disagree** (already logged by the record reader). The table under h prints Maturation Media palmitate 62.5, while the table under g prints 100.

### Fig. 2e (F2E_mps, F2E_platform)
- **Read as vector.** Every marker, bar, error bar and axis tick is a path; the y axis is calibrated from its five tick lines against the printed labels 0–0.8 (zero misfit). Two entries share one crop and one helper (`read_vector_groups` in `_util.py`), one per item.
- **Points counted:** SM MPS 12, MM MPS 13, SM 2D 16, MM 2D 11. The legend prints "n = 12–16 per group", so MM 2D falls one below the range. All eleven MM 2D circles are drawn as one compound path, and there is no duplicate circle in it.
- **Points reproduce the bars.** Mean and s.d. of the read points equal the drawn mean and s.d. to the third decimal place in all four groups (SM MPS 0.506/0.154, MM MPS 0.278/0.046, SM 2D 0.579/0.096, MM 2D 0.525/0.128). So the 11 MM 2D points are all the data behind that bar: the legend's range does not fit this group, and no marker is hidden.
- **Mean position.** The mean is read where the error bar's two halves meet; the bar's top edge sits 0.46 pt (half its line width) above it.
- **Audit's n check.** The audit compares 13 (MM MPS) and 16 (SM 2D) against "printed n [12]", although both lie within the printed 12–16. The range seems to be read as its lower bound only. This is for the code, not the readings.
- No source data file is in the folder, so there are no data.yaml rows.


### Unit F2F (Fig. 2f)
- **Panel read.** Fig. 2f (journal_version.pdf p. 4, crop [275, 175, 445, 315]), vector, APD80 (s) of SCVI20. One entry per item (F2F_mps, F2F_mm_vs_2dsm, F2F_2d), same crop, the helpers used for Fig. 2e.
- **Counts vs printed n.** SM MPS 35, MM MPS 29 (printed n = 29–35 per MPS group); SM 2D 15, MM 2D 16 (printed n = 15–16 per 2D group). All within the printed ranges.
- **Points reproduce the bars.** Mean and mean + s.d. of the points equal the drawn mean and upper cap within 0.0005 s in all four groups (SM MPS 0.324/0.430, MM MPS 0.434/0.523, SM 2D 0.316/0.360, MM 2D 0.403/0.489).
- **Audit's n check.** The audit marks F2F_mps and F2F_2d inconsistent on n: it reads "n = 29–35 per MPS group" as [29] and "n = 15–16 per 2D group" as [2, 15] (the "2" of "2D"). The counts lie inside the printed ranges; this is for the n parser, not the readings.
- Panels c,d are representative traces (item F2CD_trace, printed values); not read. No released data file covers Fig. 2f.

### Fig. 2g (unit F2GH)
- **Panel read.** Fig. 2g (journal_version.pdf p. 4, crop [80, 325, 180, 440]), vector, F/F0 of WTC MPS, SM vs MM (item F2G). Open bars at the mean with black s.d. bars; SM red squares, MM blue circles (a darker blue, 0.23/0.28/0.62, than panels e,f, so it is set in the script).
- **Counts vs printed n.** SM 16, MM 15 (printed n = 15–16 per group).
- **Points reproduce the bars.** Mean and mean + s.d. of the points equal the drawn mean and upper cap within 0.00003 (SM 0.0111/0.0200, MM 0.0234/0.0398).
- Panel h (item F2H, dF/dt on a log axis) is not in the figures-needed list and was not read. No released data file covers Fig. 2g; the supplement .docx holds no values for it.
- **Audit's n check.** The audit marks F2G inconsistent on n: it reads "n = 15–16 per group" as [15], so SM's 16 points look like a mismatch. 16 is inside the printed range; this is the n parser (as for Fig. 2f), not the reading.

### Fig. 2j (unit F2IJ)
- **Panel read.** Fig. 2j (journal_version.pdf p. 4, crop [393, 320, 500, 440]), vector, maximum Ca2+ upstroke velocity dF/dt (ms–1) of SCVI20 MPS, SM vs MM (item F2J). Log y axis: calibrated (log) from the four labelled decade ticks (0.00001–0.01); the unlabelled minor ticks are not used. Calibration is in the script (`F2J.py`), not `_util.py`, so `vector_axis` stays strict for linear panels.
- **Counts vs printed n.** SM 67, MM 67 (printed n = 67–70 per group), equal to the raw path counts (67 red fills, 67 red outlines, 67 blue circles), so no marker is lost to de-duplication.
- **Points reproduce the bars.** The arithmetic mean and mean + s.d. of the points (log axis, linear statistics) equal the drawn mean and upper cap within 0.3 % (SM 0.001058/0.001863 vs bar 0.001059/0.001865; MM 0.001482/0.002603 vs 0.001481/0.002607). The bars are mean ± s.d. on a linear scale.
- **Suspect points.** The lowest point of each group sits at the same page height (y = 399.385, 6.16e-05 ms–1), isolated 13 pt (SM) and 7 pt (MM) below the next point. This may be a floor or placeholder value, so both are marked `suspect` in readings.yaml. They are kept, and the bar means include them.
- Panel i (item F2I, n = 22–24) is not in the figures-needed list and was not read. No released data file covers Fig. 2j.
- **Audit.** "Points to P" cannot check because the panel has two groups but the stated test is Holm–Sidak after a one-way ANOVA (family not determined). This is a record/check matter, not the readings.

### Fig. 3c (unit F3C)
- **Panel read.** Fig. 3c (journal_version.pdf p. 5, crop [115, 160, 248, 272]), vector, MitoTracker Red intensity (raw RFU), WTC. There are two entries on the same crop, one per item: F3C_mps (SM MPS, MM MPS) and F3C_2d (SM 2D, MM 2D). The y axis line and each tick are separate paths, and the labels carry thousands commas, so the Fig. 2 `vector_axis` does not apply. I added `split_vector_axis`, `compound_markers` and `read_split_axis_groups` to `_util.py`, and the existing helpers are unchanged. The open 2D markers are compound paths: three rectangles in one path for SM 2D, and three circles in one path for MM 2D. The blue is the Fig. 3 blue (0.23/0.28/0.62).
- **Counts vs printed n.** All four groups have 3 points (printed n = 3 per group).
- **Points reproduce the bars.** For every group, the mean and mean + s.d. of the points equal the drawn mean and upper cap within about 1 RFU (SM MPS 1259/1575 vs 1260/1575; MM MPS 2440/2687 vs 2440/2688; SM 2D 564/≈590 vs 565/590; MM 2D 430/510 vs 430/510).
- No released data covers Fig. 3c (source data are listed as missing), and the supplement .docx holds no values for it.
- **Audit.** "Points to P" for F3C_mps cannot check: "family not determined: groups without points: d2_sm, d2_mm". The 2D points are stored under item F3C_2d, so the audit does not see them when it checks F3C_mps, even though the one-way ANOVA family is all four groups of the unit. This is a check/record matter (readings keyed by item), not the readings.

### Fig. 3d (unit F3D)
- **Panel read.** Fig. 3d (journal_version.pdf p. 5, crop [250, 160, 382, 272]), vector, MitoTracker Red intensity (raw RFU), SCVI20. Laid out exactly as Fig. 3c, so the two entries (F3D_mps: SM MPS, MM MPS; F3D_2d: SM 2D, MM 2D) reuse `read_split_axis_groups` from `_util.py` unchanged. Y axis 0–6,000 from four tick paths.
- **Counts vs printed n.** SM MPS 4, MM MPS 5, SM 2D 4 (one path of four rectangles), MM 2D 4 (one compound path of four circles); printed n = 4–5 per group. All within the range.
- **Points reproduce the bars.** MPS: mean and mean + s.d. of the points equal the drawn mean and upper cap within 5 RFU (SM 1550/1709 vs 1550/1710; MM 3282/4592 vs 3280/4595). 2D: the values are small against the axis (1 pt ≈ 68 RFU), and agree within the reading interval (SM 246/290 vs 245/290; MM 223/244 vs 220/245); the audit's (SD of points / bar)² of 0.7 for MM 2D comes from this resolution, not from a missing point.
- **Audit's n check.** F3D_mps is marked inconsistent because "n = 4–5 per group" is read as [4], so MM MPS's 5 points look like a mismatch. 5 is inside the printed range; this is the n parser (as for Fig. 2f, 2g), not the reading.
- No released data covers Fig. 3d, and the supplement .docx holds no values for it.

## Figures and data reader (F3E)

- **Panel read.** Fig. 3e (journal_version.pdf p. 5, crop [382, 160, 485, 292]), vector, MitoTracker Red intensity (raw RFU), G15.AO MPS only (no 2D groups). Read with `read_split_axis_groups`; y axis 0–4,000 from five tick paths. Two panel-specific differences: MM's blue is (0.16, 0.28, 0.52) (darker than panels c/d), and the s.d. caps are 8.35 pt wide, so `error_bars`/`read_split_axis_groups` gained an optional `cap_max` (default 8, unchanged for earlier panels; 9 here).
- **Counts vs printed n.** SM MPS 3 red squares, MM MPS 3 blue circles; printed n = 3 per group.
- **Points reproduce the bars.** SM mean 1533 and mean + s.d. ≈ 2176 from points vs drawn 1533/2177; MM 2750/≈3040 vs 2750/3040.
- No released data covers Fig. 3e, and the supplement .docx holds no values for it.

## Figures and data reader (F5A)

- **Panel read.** Fig. 5a (journal_version.pdf p. 7, crop [40, 55, 300, 200]), vector, log y axis (0.0001–1, calibrated from the five major ticks of the axis path; the minor ticks are shorter and not used). There are two entries on the same crop, one per item: F5A_cacnb2_mm (SM monolayer, MM monolayer) and F5A_cacnb2_adult (SM monolayer, Adult heart total RNA). I added `log_vector_axis`, `white_bars`, `triangle_markers` and `read_log_bars` to `_util.py`. Eight genes have three white bars each, and CACNB2 is bars 3–5. A marker belongs to the nearest bar. The adult triangles are a fill path plus an outline path, and only the fill is counted.
- **Counts vs printed n (n = 4 wells per condition).** For CACNB2, SM has **2** red squares drawn and MM has **3** blue circles. Adult heart has 6 triangles, but it is one commercial pooled RNA, so the triangles are not wells and no n is printed for it. The audit marks all three n checks inconsistent. No hidden markers were found: every path near the CACNB2 bars was listed, and there is nothing above the axis top.
- **Legend vs drawing.** The legend says "median ± s.d.". The drawn central values equal the **mean** of the drawn points: MM mean of 3 = 0.0410 vs 0.0410 drawn, and adult mean of 6 = 0.00895 vs 0.00895. MM's upper error (0.0597 − 0.0410 = 0.0187) equals the s.e.m. of its 3 points, not their s.d. (0.032). The SM bar (0.416, upper end 0.751) lies far above both drawn squares (0.102, 0.064), so the two SM values that are not drawn must be large (if it is a mean of 4, they sum to about 1.5). I stored the central value as kind `median`, as the legend names it, and corrected nothing.
- **Record.** F5A_cacnb2_mm brackets P < 0.0001 for SM vs MM. From the drawn points, a t-test gives p ≈ 0.18–0.29 (audit: inconsistent). This agrees with the legend's "none significant", which the record already notes as a suspected error.
- No released data covers Fig. 5a (source data are listed as missing), and the supplement .docx holds no values for it.

## Figures and data reader (F5B)

- **Panel read.** Fig. 5b (journal_version.pdf p. 7, crop [300, 55, 560, 200]) is vector with a log y axis (0.0001–1). Unlike 5a, its axis line and ticks are separate paths, so I added `split_log_vector_axis` to `_util.py` and an `axis` argument to `read_log_bars` (the default is unchanged, so F5A reads the same). There are two entries on the same crop, one per item: F5B_hcn4_sm (SM monolayer, Adult heart total RNA) and F5B_hcn4_mm (MM monolayer, Adult heart total RNA). Eight genes have three bars each, and HCN4 (the fourth label) is bars 9–11. The P < 0.0001 brackets join bar 9 to bar 11 (upper) and bar 10 to bar 11 (lower), as the record says. The error bars are also drawn a second time as one compound 5-line path. It duplicates the 4-line paths that are read and is not used.
- **Counts vs printed n (n = 4 wells per condition).** For HCN4, **6** red squares and **6** blue circles are drawn. The adult heart has 3 triangles, from one commercial RNA, so they are not wells. The audit marks the n checks inconsistent.
- **Legend vs drawing.** The legend says "median ± s.d.". The drawn central values equal the **mean** of the 6 drawn points: SM 0.1346 vs 0.1348 drawn, MM 0.1606 vs 0.1607. The upper error equals the **s.e.m.** of the 6 points (SM 0.0229 vs 0.0234, MM 0.0483 vs 0.0483), not their s.d. (0.057, 0.118). As in F5A, I stored the centre as `median`, the kind the legend names, and corrected nothing.
- **P.** From the drawn points, Welch's test gives p ≈ 0.002 (SM vs adult) and ≈ 0.02 (MM vs adult), against the printed P < 0.0001 (audit: inconsistent; the test is not stated).
- No released data covers Fig. 5b (source data are listed as missing), and the supplement .docx holds no values for it.

## Figures and data reader (F5E)

- **Panel read.** Fig. 5e (journal_version.pdf p. 7, crop [335, 200, 530, 348]), vector, log y axis 0.0001–10 (calibrated by `split_log_vector_axis`, misfit ~2e-5). One entry (F5E) covers all eight items, two groups each (SM red squares, MM blue circles). The bars here are black outlines, not white-filled rectangles, so `white_bars`/`read_log_bars` find nothing. I added `read_log_errorbar_groups` to `_util.py`: the 16 error bars, left to right, are the groups, and each marker belongs to the nearest one. The legend's red square sits inside the crop (it read as 8.28 for SLN SM), so markers level with a legend word "SM"/"MM" just to their right are left out. Existing helpers are unchanged.
- **Counts vs printed n (n = 4 per group).** Drawn points (SM/MM): SLN 3/2, HCN2 3/3, CACNB2 3/4, KCNIP2 3/2, MYH7 2/2, MYL2 3/3, KCND2 4/2, ALDH1A1 2/2. Only 2 of 16 groups show 4 points. Every red and blue path in the crop was counted (24 red fills = 23 data + 1 legend; blue circles are single fill+stroke paths). Only fill/outline pairs share a centre, so no markers are hidden. The audit marks the n checks inconsistent.
- **Legend vs drawing.** The legend says "mean ± s.e.m." In all 16 groups, the drawn centre equals the mean of the drawn points (within 0.3%), and upper error − centre equals the **s.d.** of the drawn points (within ~4%), not their s.e.m. For example, MYH7 SM: err 0.299, s.d. 0.299, s.e.m. 0.211. The bars appear to have been computed from the drawn 2–4 points. The centre is stored as `mean` and the upper end as `error`, as read. Nothing is corrected.
- No released data covers Fig. 5e (source data are listed as missing), and the supplement .docx holds no values for it.

## Figures and data reader (F5F)

- **Panel read.** Fig. 5f (journal_version.pdf p. 7, crop [335, 348, 530, 495]), vector, log y axis 0.0001–10, read with `read_log_errorbar_groups` from `_util.py` (unchanged). Only MYL2 (item F5F_MYL2, groups sm and mm) is returned: `figures-needed` lists no other group of this unit (F5F_CACNB1_SLN covers two genes; KCNJ2, KCND2, MYH7 carry no test a check needs). The SLN SM error bar runs down to the x axis and is drawn as separate paths (cap and line halves apart), so only 11 of 12 error bars are found as one path; that label is left out of the left-to-right pairing. MYL2 is unaffected.
- **Counts vs printed n (n = 4 per group).** MYL2 shows **5** red squares (SM) and **5** blue circles (MM), all separate vector markers. The audit marks both n checks inconsistent.
- **Legend vs drawing.** Here the bars agree with the legend: the centre equals the mean of the 5 drawn points (SM 2.661 vs 2.657, MM 0.699 vs 0.701), and upper end − centre equals their **s.e.m.** (SM 0.502 vs 0.498, MM 0.127 vs 0.124). In Fig. 5e the bars were s.d. instead. The audit's n-implied-by-error-bar check gives 4.8–4.9, so 5 points.
- The printed "P < 0.0001" uses a "two-way t-test, with Mann-Whitney correction method" and is not rechecked (audit: cannot check). No released data covers Fig. 5f, and the supplement .docx holds no values for it.

## Figures and data reader (F7)

- **Panels read.** Fig. 7g (crop [75, 315, 300, 450]) and 7h (crop [305, 315, 530, 450]), journal_version.pdf p. 11, vector. Log y axis 10^-1–10^5 calibrated from the seven major ticks (misfit < 5e-5); the tick labels extract as "10–1", "100", "101"…, so `_util.power_log_axis` reads them as powers of ten. One entry per item (8 entries, 17 item groups), all through `_util.read_drug_bars`; existing helpers unchanged. Category order Flecainide, Verapamil, Alfuzosin; within each, 2D SM (black triangles), MPS standard media (red squares), MPS maturation media (blue circles). Legend markers in the crop are left out.
- **No error bars are drawn** although the legend says "mean ± s.e.m."; only the bar (as `mean`) and the points are stored.
- **Bar value judgement.** The white fill's top is the centre of a 1.015 pt black outline stroke. Read there, every bar sat a constant ~7% (0.5 pt) below the arithmetic mean of its points; read at the stroke's outer edge (half a line width above), all 18 bars of g and h agree with the mean of their drawn points within 1.5%. The outer edge is stored.
- **Counts vs printed n.** Legend: n = 4 for verapamil, n = 3 for flecainide and alfuzosin. Drawn: verapamil 3/3/3 in g and h; flecainide 4/4/4 in g and 3/4/4 in h; alfuzosin 3/3/3 in both. The verapamil and flecainide counts look swapped relative to the legend. The audit's n check parses the verapamil n as [2, 4] (it seems to take the "2" of "(2D)"); flagged here, not changed.
- **Points vs printed P.** Two-sample t-tests on the drawn points (unadjusted) do not reproduce several printed P values: alfuzosin g SM vs MM printed 0.005, drawn points give 0.71 (log 0.79); alfuzosin h 2D vs SM printed 0.02, drawn give 0.78 (log 0.88); alfuzosin g 2D vs MM printed 0.008, drawn give 0.18 (log 0.07). Verapamil comparisons agree better on log values. The audit marks all seven P checks inconsistent. Nothing corrected.
- No released data covers Fig. 7 (source data are listed as missing), and the supplement .docx holds no values for it.

## Figures and data reader (F8)

- **Panels read.** Fig. 8g (crop [75, 305, 305, 445]) and 8h (crop [305, 305, 545, 445]), journal_version.pdf p. 12, vector. Log y axis 10^-3–10^3, calibrated from the seven major ticks with `_util.power_log_axis` (misfit < 1e-4). There is one entry per item (5 entries, 10 item groups), all read through the new `_util.read_sem_drug_bars`; existing helpers are unchanged. Unlike Fig. 7, these bars are open outlines (one path per group holding its three drug bars), and s.e.m. bars are drawn (one path of five lines each). The crop holds no legend markers.
- **Bar value judgement.** As in F7, the value is the outline's outer edge (half the 0.987 pt line width above the top line). There, all 18 bars of g and h agree within 1.2% with both the arithmetic mean of their drawn points and the linear midpoint of their s.e.m. caps. At the line centre they sit about 7% lower. `error` is the upper cap line. Upper cap minus mean matches the s.e.m. of the drawn points (for example, g flecainide 2D: 0.128 vs 0.127), and the audit's n-from-error-bar checks agree with the drawn counts.
- **Counts vs printed n (n = 3–5 per group).** The drawn counts, as 2D/SM/MM, are: g flecainide 4/5/4, verapamil 4/6/5, alfuzosin 3/3/3; h flecainide 4/4/3, verapamil 4/3/5, alfuzosin 3/6/4. Two groups show 6, above the printed range: g verapamil SM (not an item group, not stored) and h alfuzosin SM (stored). Two verapamil 2D triangles in g sit at the same height (0.02213), at different x. Separately, the audit parses this n as [2, 3], apparently taking the "2" of "(2D)" (as also noted for F7). That is an audit parser issue; nothing was changed.
- **Points vs printed P.** On the drawn points, unadjusted Student t-tests reproduce flecainide g SM vs MM (printed 0.033, points give 0.0336) and verapamil g 2D vs MM (printed 0.045, points give 0.0454). They do not reproduce the alfuzosin P values: g 2D vs MM printed 0.046, points give 0.32 (log 0.66); h 2D vs SM printed < 0.0001, points give 0.011 (log 0.003); h 2D vs MM printed < 0.0001, points give 0.079 (log 0.13). Nothing was corrected.
- **Axis label vs legend.** Panel h's axis reads "Safety margin based on cAPD80", but the legend says APD80 (h), and so does the record's measure for F8H_* ("safety margin based on APD80"). `unit_of_value` follows the axis. This is for the record reader.
- No released data covers Fig. 8 (source data are listed as missing), and the supplement .docx holds no values for it.

## Figures and data reader (ED3EF)
- **Panel read.** Extended Data Fig. 3e (journal_version.pdf p. 22, a raster image at about 300 dpi; the NIHMS copy is more heavily compressed): `figures/ED3E_capd80.py`. Panel f (ED3F_ff0) was not in this job's list and was not read.
- **Bars.** Each group is an outlined bar (top edge = mean) with a mean + SD bar. Markers hide the middle of the bar tops and caps, so the script takes the bar top as the stroke whose ink (black or marker) spans the bar from side to side, and the SD end as the topmost stroke above it with ink on both sides of the centre line. MM: mean 375.3, SD upper end 474.3. SM: mean 243.5, SD upper end 313.7 msec. SM's lower cap is hidden by circles.
- **Counts vs printed n.** MM shows 10 red squares, each standing alone (area 320–326 px), and all 10 are stored as points. The legend prints MM n = 16, SM n = 10. SM's blue circles touch in four clusters: about 16 circles by blob area (1+2+1+3+1+2+5+1). Under the stand-alone rule, SM is mean and SD only (`countable: false`). The drawn counts (MM ≈ 10, SM ≈ 16) look like the legend's n with the two groups swapped. Nothing was changed; this is for the record reader.
- **Direction.** The plotted MM bar (375) lies above SM (244), so the figure shows MM *longer* cAPD80 in SCVI273. The record's item ED3E_capd80 states "MM shortens cAPD80 in SCVI273 MPS". The labels were read as printed (MM left, red; SM right, blue). This is for the record reader: either the labels or the finding is swapped.
- **Points vs bar.** The 10 MM points give mean 380.7 and SD 93.0. The bar gives mean 375.3 and SD 99.0. The audit's n-from-error-bar check reports "cannot check" (points 10, printed n 16).
- No released data covers this panel, and the supplement .docx has no SCVI273 or cAPD80 values.

## Figures and data reader (ED3GH)
- **Panels read.** Extended Data Fig. 3g and 3h (journal_version.pdf p. 22, raster at about 300 dpi). There is one entry per item: ED3G_mm, ED3G_m2, ED3G_m4 and ED3G_m1 (panel g), and ED3H_m2 (panel h). Each uses a 4-line script over `_util.read_ed3g` / `read_ed3h`. Group M3, and panel h's MM, M1, M3 and M4, are not read because no listed item involves them. ED3G_m1_sm was not in this job's list. Its groups (M1, SM) are read under other entries.
- **Coloured groups: bar only.** In panel g, SM's red squares touch (legend n = 12) and MM's blue circles touch (legend n = 13). In panel h, SM's red squares touch in pairs and are cut by the black error-bar strokes. All three are `countable: false`. MM's circles hide both SD caps, so MM gives its mean only (277.3, interval ±13 because the circles merge with the bar top). SM (g): mean 501.4, SD upper end 660.7. SM (h): mean 0.307, SD upper end 0.489.
- **Black markers counted (a judgement).** M1 (5 triangles), M2 in panel g (3 down triangles), M4 (4 circles) and M2 in panel h (4 down triangles, two straddling the x axis) are solid black, on top of the black bar outline and error-bar lines. They were counted as standing alone: after the lines are eroded away (square 7 px), each leaves its own core. Their centres are less certain than for free markers. A core merged with a line can sit off-centre by up to half the square, and a triangle may be plotted at its centroid or its box centre (3 px apart). Each interval is widened by both. Bar-mean evidence that GraphPad plots triangles at the box centre: M1's 5 points average 434.1 against a bar of 439.0, and 439.1 if box centres are used. The stored values stay at the core centroids. No n is printed for M1, M2 or M4, so there is no count to check.
- **M4 SD cap.** M4's upper SD cap merges with two circles that together span the bar's width. The script cannot tell it from a stroke across the bar, so M4 gives points and mean but no error.
- **Points vs bars.** M2 (g): points 295.6, 293.7, 167.3 (mean 252.2, SD ≈ 74) vs bar 242.0, SD upper end 319.2 (SD 77). M4: points mean 294.9 vs bar 289.6. M2 (h): points 0.065, 0.028, 0.008, 0.008 (mean 0.027) vs bar 0.017. The two lowest triangles straddle the axis, so their cores are pulled up by the bar lines. Their intervals reach below 0.
- **Checks.** Points-to-P cannot run: the Holm–Bonferroni family needs points for every group, and SM and MM have none (markers touch). The audit computes directions from the read means for all five items: MM, M2 and M4 are below SM, M1 is above MM, and M2 is below SM in beating prevalence.
- **Record note (already flagged).** The legend says M2 and M3 had APD80 "significantly less than MM", but the printed brackets run from SM. The readings agree with the brackets: M2 (242) is below SM (501), but only slightly below MM (277), and M3 (≈381) is above MM.
- No released data covers these panels. The supplement .docx has no values for the media screen.

## Figures and data reader (ED4)

- **Panels read.** Extended Data Fig. 4a (cAPD80, msec) and 4b (spontaneous beating frequency, Hz), journal_version.pdf p. 23, one raster image (about 300 dpi; the NIHMS copy is raster too). Entries ED4A and ED4B, one group per genotype and medium; helper `_util.read_ed4`.
- **Points.** Read only where every marker of the group stands alone: a: SCVI273 SM 10, G15A0 SM 8, G15A0 MM 8; b: WTC MM 5, G15A0 SM 8, G15A0 MM 8. All other groups (WTC SM/MM and SCVI20 SM/MM in a; WTC SM, SCVI20 SM/MM, SCVI273 SM/MM in b) have touching markers: bar only. No n is printed (the legend says "randomly selected subset" / "representative set"), so counts cannot be checked. Coincident markers would hide one another and cannot be detected.
- **Bars.** The mean is the bar top found at the bar corners. Markers cover both corners of SCVI20 SM (a) and WTC SM (b), so those give no mean. The upper cap is left out where markers hide it. The legend does not say whether the error bar is SD or s.e.m.
- **Checks.** Points-to-P runs for ED4A_g15 and ED4B_g15 (both consistent). The other items, and both variability items, lack points for at least one side.
- **Shared-part note.** `blobs()` drops regions over its default max_area (10,000 px). A dense cluster of circles (b, SCVI20 MM) vanished, so the group looked like one single marker. The ED4 reader passes a max_area covering the whole image. Earlier raster readers on this paper that use `_util.markers` (default max_area) may have the same blind spot.
- No released data: the folder has no source data file.

## Figures and data reader (ED5FG)
- **Panels read.** Extended Data Fig. 5f (reserve OCR) and 5g (ATP capacity), journal_version.pdf p. 24, raster (one ~300 dpi image). Scripts `ED5F.py` and `ED5G.py`, helper `_util.read_ed5`. Axes are calibrated from 4 (f) and 6 (g) tick marks. No table or released data holds these values (the supplement .docx has no OCR/ATP table).
- **Points vs printed n (4 wells per group).** f MM: 4 blue circles. f SM: 3 blobs, because the two lowest red squares overlap (one blob two markers tall), so bar only. g SM: 4 red squares. g MM: 4 blue circles.
- **Occluded rings.** In g the black error-bar line and caps cross several open markers and cut them into pieces. Pieces are joined while their joint box stays within one marker (20–24 px), and every joined box is one marker. Each point is its box centre.
- **Error bars.** The legend does not name them. From the points, f MM's bar matches s.e.m. (implied n ≈ 4.1), but g's bars match SD (implied n ≈ 1.0), so the two panels seem to use different error bars. The audit's n check is therefore `cannot check` for ED5G_atp.
- **Means.** The mean of the points matches the bar top (f MM 50.4 vs 50.7; g SM 21.1 vs 21.0; g MM 32.3 vs 32.2).

## Figures and data reader (Supplementary Fig. 4)

- **Panels read.** Supplementary Fig. 4b (normalized F/F0), 4c (normalized cτ75) and 4d (normalized upstroke duration), Supplementary_Figures.pdf p. 5, vector. Scripts `S4B_ff0.py`, `S4C_tau75.py`, `S4D_upstroke.py`, helper `_util.read_supp_groups`. Every axis, tick, bar side, error-bar half and cap is its own one-line path in a near-black ink (0.14, 0.12, 0.13), so the Fig. 2–3 helpers (which expect black paths with several lines) did not apply. Panel A (beat rate) was not asked for.
- **No table or data.** The supplement .docx has no Supplementary Fig. 4 values, and no data file is released for it.
- **Points vs printed n.** b: SM 3, MM 6. c: SM 3, MM 4. d: SM 3, MM 4. All match the legend. Panel d's legend names the second group "SCVI20", but its x axis reads MM. Read as MM, as the record has it.
- **Means and error bars.** Mean of points = where the error bar's halves meet, to within 0.004. Mean + SD of the points = the upper cap, which matches the legend's "mean and standard deviation".
- **P values from the points (my check, not stored).** Welch t-test on the read points: c 0.0059 (printed p=0.0059), d 0.045 (printed p=0.044), b 0.016 (printed p=0.0015). Panel b's printed P is about ten times smaller than the points give, so it may be a misprint of 0.015. The audit does not recheck these, because it treats "2-way t-test with Welch's correction" as a test it cannot rerun. "2-way" here most likely means two-tailed.

## Figures and data reader (Supplementary Fig. 5)
- **Panels read.** Supplementary Fig. 5a (normalized beat rate), 5c (normalized cτ75) and 5d (normalized upstroke duration), Supplementary_Figures.pdf p. 6, vector. Scripts `S5A_rate.py`, `S5C_tau75.py`, `S5D_upstroke.py`. The layout is the same as Supplementary Fig. 4, so each script reuses `_util.read_supp_groups` and only the tick count changes. Panel b was not asked for. Panel d's y axis starts at 1.4, not 0.
- **No table or data.** The supplement .docx has no Supplementary Fig. 5 values, and no data file is released for it.
- **Points vs printed n.** Every group has 5 points (SM and MM, in all three panels), which matches the legend's n = 5.
- **Means and error bars.** Mean of points = bar mean, to within 0.001.
- **P value from the points (my check, not stored).** Welch t-test on 5c's points gives 0.0102 (printed p=0.01).
- **Record note.** The unit's `anchor` and `n` (p=0.044, "SM: n=3, SCVI20: n=4", "Supplementary Fig. 4d") appear to be copied from S4. Supplementary Fig. 5 prints only p=0.01 (panel c) and n = 5 per group. The record reader should check this.

## Figures and data reader (Supplementary Fig. 7)
- **Panels read.** Supplementary Fig. 7a (normalized Ca2+ upstroke), 7b (normalized Ca2+ τ75) and 7c (normalized Ca2+ amplitude), Supplementary_Figures.pdf p. 8. Unlike Supplementary Figs. 4 and 5, this page is one embedded image (~320 dpi), so it is read as raster. Scripts `S7A_upstroke.py`, `S7B_tau75.py`, `S7C_amplitude.py`, helper `_util.read_s7`. In 7c only the 1uM groups are read, because S7C_amplitude compares only those two. Panels D and E are traces with no item.
- **No table or data.** No data file is released, and the supplement .docx holds no Supplementary Fig. 7 values.
- **Separating markers.** The black lines cut most touching markers apart in the colour masks. Two cases stay joined. In 7b, two pairs of red squares are stacked in one column (SM 100nM, SM 1uM). Each pair is split at half a side from the box's top and bottom, with 1 px added to the interval. MM 1uM's error bar is drawn in blue in 7a and 7b and joins some of its circles. Those circles are found by eroding the blob with a 7 px square (blue lines are 3–4 px), which adds 3.5 px to their intervals. Any other blob shape stops the script with an error.
- **Points vs printed n (SM n=5-6, MM n=3-5).** 7a: SM 100nM 6, MM 100nM 4, SM 1uM 5, MM 1uM 4. 7b: 6, 3, 5, 3. 7c: SM 1uM 6, MM 1uM 4. All fall within the printed ranges. A marker exactly hidden behind another cannot be detected.
- **Means and error bars.** Mean + SD of the points matches the upper cap to within 0.01 (legend: mean and SD). The mean of the points sits 0.01–0.03 above the bar top in most groups (about 1–2 px), and in 7c SM 1uM it sits 0.02 below. No reading was adjusted.
- **7c lowest SM 1uM point.** It reads 0.004, on the x axis line (amplitude ≈ 0 relative to vehicle). Kept as read.
- **P value from the points (my check, not stored).** 7c MM 1uM vs SM 1uM: Welch t-test gives p = 0.107 and Student's pooled t-test gives p = 0.031. The printed p=0.03 matches the pooled test, not the Welch test the legend names.
- **Main text vs points.** "almost 3-fold" vs a bar mean of 3.12 (3.15 from the points).
- **Record notes.** (1) The audit's n check uses printed n [3, 5] for sm_1, but the legend gives SM n=5-6. S7's items carry no per-group n, so the record reader should add `per_group`. (2) The x-axis label reads 1µM, which matches the main text against the legend's 1mM, as the record's suspected_error notes.
- **Renders.** Renders and probe scripts were written to `/tmp/livinglit_2022_Huebsch_S7_*` because no folder could be created. Deleting them needed a permission this session lacked, so they are still there. Nothing was written to the repo or the papers folder.

## Vocabulary agent

Vocabulary version 39, instructions terms_v4.

**Flags (4).**
- `preparation` "live" (*not a context*): the paper writes "live" for MPS microtissues and for 2D monolayers alike ("Live MPS and monolayer were incubated with Mitotracker"). The vocabulary has *intact tissue* and *live cells*, and picking one per group would mean reading the platform field. Please write the preparation per group. This flag blocks preparation matching for most functional items in this paper, so it is the most useful re-read.
- `day_of_measurement` "immediately after lactate treatment" (*not a context*): a moment relative to purification, not a number or a declared state. "six days" and "180 days" in the same unit also count from purification, not from the start of culture. They may belong in `time_point`.
- `measure` "expression of ion channel and sarcomere transcripts relative to GAPDH" and "CACNB1 and SLN expression relative to GAPDH" (*several measures*): several genes in one value.

**Judgements I was unsure of.**
- "hESC-Qualified Matrix (Corning)": I took this to be Corning's hESC-qualified Matrigel and added it under *Matrigel*. The paper does not say "Matrigel" here.
- "cardiac MPS": I added a new platform term under *3D engineered tissue*, not under *tissue between two pillars*. The MPS has no hydrogel, and the tissue self-assembles in a fluid-fed microchamber with anchoring posts. I added no synonym, because "cardiac MPS" is broader than this chip format.
- "standard media": I added *standard medium control* (qualifier `called`) as the control arm of maturation_strategy. The alternative was the state "none".
- Rate-corrected measures (cAPD80, FWHMc, cτ75) became child terms of the uncorrected measures, so they are never compared with uncorrected values. The correction formula (Fridericia, given only for ED3E) is not a qualifier.
- "MitoTracker Red intensity" maps to *mitochondrial membrane potential* because the paper says so ("Mitochondrial inner transmembrane potential, as measured with MitoTracker Red"). I added no synonym, because other sources use MitoTracker for mitochondrial mass.
- "ATP capacity" is a new term under OCR. The paper never says how it was calculated.
- "sarcomere power score" is a new term. Its FFT formula is only cited (ref. 61), so it may turn out to be the *sarcomere alignment index*.
- The IC50 key (from an earlier paper) requires `measure.target`. I added the `response` qualifier but did not change that key. The re-map agent should revisit it.
- `calcium_transient_rise_rate` now has a `statistic` qualifier ("maximum"). Its existing key does not require it.
- S4/S5 "normalized …" wordings: `normalised_to` is left out because it is not stated. The S7 wordings carry "the same MPS treated with vehicle".
- "B-27" already matches *B27* after normalisation. "B-27 + L-ascorbic acid" was unmapped only because L-ascorbic acid (CHEBI:29073) had not been adopted yet.

**Ids not found.** SCVI20 is not in Cellosaurus (the nearest are SCVI-202 and SCVI-2020), so I added it as an own term, `cell_line:scvi20`. Values recorded as "G15.AO" match Cellosaurus CVCL_V192 exactly, but the methods print "G15.AO48".

**Values the reader may have recorded wrongly.**
- F5A/F5B "Adult heart total RNA" has `preparation` "lysis buffer". The source was commercial polyA RNA, so *RNA extract* fits better.
- `cm_medium` "glucose free RPMI" is the powder that all media were made from. Standard media then has 25 mM glucose added, so the culture glucose sits in the maturation qualifiers, not here.
- "peak twitch stress" is not printed in the text; the paper says "peak twitch force" and "contractile stress".

**Re-map (2026-11-13, vocabulary version 69, terms_v4).**
- "peak twitch stress" now matches *twitch stress* by code, so I removed its stored mapping. No other mapping is matched yet, and every term it uses still exists.
- EC50 mappings: I changed `agonist` to `compound`, the qualifier `measure:ec50` has had since 2016_Lind. Alfuzosin and flecainide are not agonists, and Lind writes `compound: isoproterenol`. Extracellular calcium is under `compound` too, for one spelling. Hinson still uses `agonist`, so the re-map checkpoint should merge the two.
- The flags stand. "live" is still the one to re-read, because *live cells* (2D) and *intact tissue* (MPS) both exist now.
- Still open: the IC50 key requires `measure.target`, which this paper's IC50s do not carry (they carry `response`).

## Formula agent

**Where the spec or gate left me guessing.**
- **Safety margins (Fig. 7G,H; 8G,H).** These are the paper's clearest stated formula (IC50/ETPC). But no margin is printed as a value, only drawn as bars, and a derivation's `output` must be a record value. So every margin derivation has no output and can't be checked. The verapamil IC50s are printed (971 nM MM, 90 nM SM), so the bar readings could check them if a reading were allowed as an output, or if the formula were rearranged (IC50 = SM·ETPC). I kept the formula as stated.
- **ETPC.** Only flecainide's is printed (1.5 μM). Verapamil and alfuzosin are "obtained from the literature" with no value and no citation, so I recorded them as `not_stated` rather than `by_reference`.
- **Flecainide APD80 margin in SCVI20.** "in vitro EC50 was less than the clinically reported ETPC" (5.5 nM / 1.5 μM ≈ 0.004) has no evidence item, so it isn't recorded.
- **Aggregation.** The margin bars are mean ± SEM per MPS, while the printed IC50 is one fitted value per group. I wrote `aggregation: not stated`.
- **Fridericia.** The methods apply it "for spontaneously beating cells". cAPD80 (Fig. 2a,b; ED3, ED4) and FWHMc (ED2e, 1 Hz paced) are called rate-corrected, but the pacing is often unstated or 1 Hz, where RR = 1 s and the correction does nothing. Fig. 2a,b has the alternative "paced at 1 Hz" written in.
- **Variable names.** The Fridericia proposal was first rejected as "contradicts bazett_rate_correction on its own test values". Code compares entries that share their whole set of variable names, so two different rate corrections with names (dc, d, RR) count as a contradiction. I renamed them (dcf, dur, RR). The check may be too strict for alternative definitions of one quantity.
- **Pillar force.** The paper names the uniform-load cantilever formula and its variables (q, L, E, I, R) but prints no equation, and no pillar radius or height. I wrote F = 8EI·d/L³ with F = qL as the total load. Whether "contraction force F" is qL or q is my reading.
- **Stress.** The area that turns force into mN/mm² is never stated. Stress = F/A is written from the named quantity and its unit.
- **qPCR "relative to GAPDH".** No quantification method (ΔCt, 2^-ΔCt, ΔΔCt or standard curve) is stated, so these are `no_formula` with labelled alternatives. The four F5A/F5B items have no anchor.
- **ΔF/F0 vs F/F0.** The text says ΔF/F0 (relative change) for Fig. 2g,i, but the axes and brackets say F/F0 (a ratio). ED3f's legend says F/F0 while the Results sentence on it says ΔF/F0. Both are recorded as alternatives; they differ by exactly 1.
- **S7C "almost 3-fold".** This is the same quantity as the bar of S7C_amplitude, group "MM 1uM" (read mean ≈ 3.1). The library has no identity entry to compare a printed value with a reading of itself, so it is `cannot check`.

**Observations for code (not verdicts).**
- τ75 is defined two ways: "maximum to 25% of maximum" in the Methods and "maximum value to 30% of the maximum value" in the Fig. S7 legend.
- The S7 legend gives the flecainide dose as 1 mM; the Results give 1 μM (already flagged by the reader).
