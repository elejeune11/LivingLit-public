## Record reader

- **Cell composition: one field or three.** The ECT groups differ in which hiPSC-derived lineages they contain (CM+EC, CM+MC, CM+EC+MC). `cell_types`, `endothelial_cell` and `stromal_cell` could each hold part of this. I put the complete set in `cell_types` for each group. `endothelial_cell` and `stromal_cell` are set to `not applicable` in `default_context`, so that the same fact is not stored in two fields and CM+EC+MC vs CM+EC stays a contrast on one field. A vocabulary checkpoint may prefer the other encoding.
- **Differentiation protocol per ECT group not stated.** CM+EC ECTs come from the CM+EC protocol. CM+MC and CM+EC+MC ECTs are made by "combin[ing] cells from these 3 induction protocols". The paper does not say which protocols feed which ECT class. ECT units therefore hold only the steps common to all protocols (`Activin A + Wnt3a + BMP4 + bFGF`, 24 hours Wnt activation), with `wnt_inhibition_days` and `insulin_day` as `not stated`, plus an `other_conditions` entry for the combining. In S1 (the protocols) the protocol-specific factors are qualifiers on `differentiation_factors` (VEGF165 from d5; Dkk1 d5 to 7), because no single quote of 30 words or fewer names all of a protocol's factors.
- **Supplementary Fig. 2 (Wnt3a dose).** The varied Wnt modulator (Wnt3a 50 or 100 ng/mL, Dkk1 100 ng/mL, control) is recorded as `treatment`. The unit's `differentiation_factors` is the rest of the protocol (`Activin A + BMP4 + bFGF`). The schema has no way to say "the differentiation set with one member swapped". Which protocol the S2 cells followed after day 1 is not stated. The concentrations appear only in the figure's group labels, so their anchors are `kind: unit`.
- **Fig. 1c bracket.** One *** bracket at 3.5 Hz runs from the CM+EC+MC point to the overlapping CM+EC and CM+MC points. I wrote two pairs (CM+EC+MC against each), with a note. Frequency levels are not groups, because no test runs along frequency. The 3.5 Hz pairs carry an item-level pacing override instead. The same applies to the day-14 pair in S4 and the 4-week pairs in Fig. 3.
- **Statistical test.** The Methods give "unpaired t-test" for two groups and "one-way or two-way repeated ANOVA followed by Tukey's test" for more than two. For three- and four-group units I wrote that Methods sentence. For the two-group comparisons in Fig. 3 (Tx vs sham at 4 weeks) and S4 (day 14), the test is `not stated`: the design is repeated over time and either sentence could apply.
- **Bounds not recorded as values.** "consistently greater than 240 bpm" (MCR), "reached over 17 kPa" (highest Young's modulus) and "thick (>800 μm)" are bounds. The Value schema has no bound kind, so they are in notes. The 240 bpm bound is also a suspected error, because Supplementary Fig. 6a plots CM+EC+MC ECTs at 3.5 Hz (210 bpm) and 4 Hz (240 bpm).
- **Implanted vs sham context.** In Fig. 3 and TXT3, the unit context describes the implanted ECTs (CM+EC+MC, collagen/Matrigel, etc.), and only `treatment` differs (`ECT implantation` vs `none`). Strictly, the ECT fields do not apply to sham rats. Writing them per group would alias every ECT field with treatment.
- **Species in vivo.** For histology of human grafts in rat hearts (Fig. 4, Fig. 5, S10) and for rat echocardiography, `species` is `rat`. The field holds one value, so "human graft in rat host" cannot be stated.
- **Purity.** The CM fractions (61.8% for the CM+EC protocol; 63.1/48.3/43.6% for the ECT mixtures) are recorded as evidence. `purity` is left `not stated` in context so the measured values are not stored twice.
- **2D group in Fig. 2a / S9.** The 2D samples were "cell/matrix mixture as the same density as used for ECT formation ... plated in 24-well plates, cultured for 14 days". Their medium and atmosphere are not stated, so they are `not stated` for that group rather than carried over from the ECTs. `seeding_density` is worded "same density as used for ECT formation" (no number is printed for 2D).
- **Pairs not printed.** In Fig. 2a, no mark is printed between 2D and 3D CM+EC, so no item was written for that pair. The claim that 3D gives greater alignment than 2D is judged scope `overstated`.
- **Representative values.** The S2a dot-plot gate percentages, the S7 representative-curve R2 and the S10 "= 42%" are single representative samples, printed in the figures. They are recorded as `kind: value` with image anchors (`kind: unit`) and named `_example`/`_figure`.
- **Fig. 2d enrichment.** Each GO process or pathway bar ("45 of 701") is one item: a measurement of groups [CM+EC+MC, CM+EC] with counts `between` them. It is not a `compares` item, because the enrichment P tests over-representation, not a direction between groups. The supplementary .xls files (s5–s10) are MetaCore exports for this comparison. They were listed as files and not used for values (left to the figures-and-data reader).
- **Model outputs left out.** The regression lines and equations in S6 are recorded as printed values (intercept, slope, R2), because the paper prints them. The spline-fitted Ca2+ curves (S8a) are left to the figures reader. EC50 is recorded only as printed ("around 1 mM", P=0.45).
- **Cross-references.** Three were recorded: the Fig. 2a legend cites "Supplementary Fig. 8" for whole images (they are in S9a); the Methods cite "Supplementary Fig. 2b and C" for the force set-up (S3b,c); and the main Methods cite "(Fig. 1)" for the three induction protocols (Supplementary Fig. 1).
- **Missing files.** Supplementary Videos 1–3 (s2–s4) are not in the folder. No item rests on them alone, so `missing` is empty and a `version_note` says so.

## Figures and data reader

### F1a (Fig. 1a, lower row): `figures/f1a_proportions.py`, raster
- Released data: s5–s10 are GO/MetaCore exports only; no cell proportions, so the panel is read from the figure.
- Three small bar charts (CM+EC, CM+MC, CM+EC+MC) in one raster image (p. 2), each calibrated on its own five tick marks
  (0–80 %, printed labels assigned bottom to top). Labels are `<ECT type>_<cell type>`; several labels share one group of
  F1a_proportions. Bars only (mean and upper end of the error bar); no points drawn, so nothing is countable and no n is read.
- Bar tops are taken at the half-intensity crossing above the fill (the bars have a dark anti-aliased outline); cap and tick
  centres are darkness-weighted. A first version that took the first fully coloured row read every bar ~1.5 px (~1.2 %) low.
- Check against printed CM ratios (Results): read 63.36 / 43.70 / 48.34 vs printed 63.1 ± 7.0 / 43.6 ± 4.7 / 48.3 ± 6.8;
  error-bar heights 6.7 / 4.6 / 7.0 vs printed SD 7.0 / 4.7 / 6.8.
- Not read: CM+EC MC bar (a few % at most; fill and error cap merge into one dark block, no edge to read); CM+MC EC (no bar
  drawn; not recorded as 0, since nothing is drawn to read).
- The proportions in each ECT do not sum to 100 % (e.g. CM+EC ≈ 63 + 17 + small MC); the remainder is not shown.
- Record note: F1a_proportions holds three cell-type proportions per group, but its groups are the ECT types only; the
  cell type lives in the figure label, not in the record.

### F1b (Fig. 1b): `figures/f1b_function.py`, raster
- Released data: none (s5–s10 are GO/MetaCore exports); read from the figure.
- Three bar charts in the same raster image as F1a (p. 2): maximum capture rate (ticks 0–6 Hz), relaxation time (0–250
  msec), excitation threshold (0–2 V/cm); each calibrated on its own tick marks (7 / 6 / 5, printed labels bottom to top).
  Bars left to right CM+EC, CM+MC, CM+EC+MC as printed under them. Same bar-top and cap method as F1a.
- Bars only (mean ± SD per Methods, upper error bar only); no points drawn, nothing countable, no n read (printed n = 8 / 7
  / 12 are in the record).
- Read means: MCR 3.43 / 3.29 / 4.58 Hz; RT 211 / 202 / 175 msec; ET 1.41 / 1.60 / 1.17 V/cm. No values are printed in the
  text to check against.
- Tick marks are read two to three columns left of the axis line: in the MCR chart the column right next to the line is
  grey all along (anti-aliasing) and merged every tick into one run.
- The CM+EC+MC bar is one group of both items of each measure (vs CM+EC, vs CM+MC). A figures.yaml label links to one item,
  so the same reading is returned under a second label `<measure>_cem_vs_cm`. The shared parts have no way to link one label
  to two items.
- Text: MCR in CM+EC+MC "consistently greater than 240 bpm" (4 Hz). The read mean is 4.58 Hz (275 bpm) and mean − SD is
  about 4.02 Hz, so the bar alone does not contradict it; the record's suspected error rests on Supplementary Fig. 6a.

### F1c (Fig. 1c): `figures/f1c_force_frequency.py`, raster
- Released data: none (s5–s10 are GO/MetaCore exports); read from the figure.
- Line chart in the same raster image (p. 2), active force (fold increase over 2 Hz) at 2, 2.5, 3, 3.5 Hz; y axis
  calibrated on its seven tick marks (0–1.2). Only the 3.5 Hz means are read (x = 3.5), as only the 3.5 Hz pairs are items.
- No markers: each mean is where its line meets the 3.5 Hz error-bar stem. The line centre is fitted straight over the
  3–3.5 Hz segment and evaluated at the stem; the fit's standard error is added to the interval. The blue (CM+EC) line runs
  under the green one where they meet near 3.5 Hz, so its value is extrapolated ~35 px from columns clear of green; the
  extrapolated row agrees with the blue tip visible just left of the stem (within ~1 px).
- Read means at 3.5 Hz: CM+EC 0.406, CM+MC 0.384, CM+EC+MC 0.748 (upper error end 0.838). Printed text: "approximately
  75%" (CM+EC+MC) and "approximately 40%" (CM+EC, CM+MC): consistent.
- Not read: the CM+EC and CM+MC error bars. Both are drawn downward on one shared stem with two caps (≈0.27 and ≈0.09);
  which cap belongs to which group cannot be told from the figure. The `error` kind is the upper end in any case.
- Means only, no points, nothing countable; no n read.
- Record note: F1c_force_frequency prints its values in % ("Approximately 75", unit %), while the figure axis is fold
  increase; the readings are in fold increase as printed on the axis.
- Same one-label-one-item limit as F1b: `cem_vs_cm` repeats the `cem` reading for the item against CM+MC.

### F1d (Fig. 1d): `figures/f1d_youngs_modulus.py`, raster
- Released data: none (s5–s10 are GO/MetaCore exports); read from the figure.
- One bar chart in the same raster image (p. 2), Young's modulus, y axis calibrated on its four tick marks (0–15 kPa).
  Bars left to right CM+EC, CM+MC, CM+EC+MC as printed under them. Same bar-top and cap method as F1b.
- Read means: CM+EC 3.56, CM+MC 9.94, CM+EC+MC 8.84 kPa; upper error ends 5.69 / 12.69 / 13.38. Printed text: CM+EC+MC
  "average of 8.8kPa": consistent. "The highest ... reached over 17 kPa" lies above the drawn axis (15) and is not checkable.
- Bars only (mean ± SD per Methods, upper error bar only); no points drawn, nothing countable, no n read.
- The CM+EC bar is one group of both items (CM+MC vs CM+EC, CM+EC+MC vs CM+EC); `ce_vs_cem` repeats the `ce` reading for
  the second item (same one-label-one-item limit as F1b, F1c).
- Record note: the panel's two brackets both carry "*"; the legend quote "NS, not significant" has no NS in this panel.

## Figures and data reader (F2a)

- **Data.** The supplementary .xls files (s5–s10) are MetaCore gene-list exports (Fig. 2d); none holds κ. No data rows.
- **Fig. 2a right (`f2a_kappa`, raster).** One bar chart, κ axis 0–8 calibrated on nine ticks. Four bars (2D CM+EC+MC,
  CM+EC, CM+MC, CM+EC+MC) found as saturated fill; mean and upper end of the upward error bar (SD per Methods) read
  for each. Bars only: no points drawn, so the legend's n = 3 (2D) and 5 (each 3D) cannot be counted.
- **Labels.** Each bar serves two items; it is returned again under `<group>_vs_<other>` so every item–group pair has
  its own link (same reading, same values).
- **Unit.** `unit_of_value` is "κ" (dimensionless; axis printed "Concentration parameter (κ)").
- The left half of Fig. 2a (orientation maps, colour bar −90 to 90 Deg) is representative imaging, not read.

## Figures and data reader (S9)

- **Data.** The supplementary .xls files (s5–s10) are MetaCore gene-list exports (Fig. 2d); none holds the circular
  standard deviation. No data rows.
- **Panel read.** Supplementary Fig. 9b (`figures/s9b_circular_sd.py`, raster, supplement p. 16, crop
  108,465–245,632 pt): one bar chart, y axis 0–70 "(Deg)" calibrated on eight tick marks. Read: 2D (CM+EC+MC) 57.65
  (error-bar end 64.14), CM+EC 37.59 (42.63), CM+MC 24.39 (25.86), CM+EC+MC 25.72 (29.57). No printed means to check
  against; the bar order (2D, CM+EC, CM+MC, CM+EC+MC) is taken from the labels printed under the bars.
- **Counts.** Bars only: no points drawn, so the legend's n = 3 (2D) and 5 (each 3D) cannot be counted.
- **Labels.** Five items share four bars; each bar is returned again under `<group>_vs_<other>` (twod ×3, ce ×3, cm ×2,
  cem ×2) so every item–group pair has its own link (same reading, same values).
- **Unit.** `unit_of_value` is "Deg", the axis label as printed.
- **Error bar.** Taken as SD from Methods; the legend does not say. The CM+MC error bar is short (about 1.5 Deg above
  the bar); its cap is resolved but its interval is relatively wide.
- **Not read.** Panel a (per-image nucleus and myofiber angle histograms with orientation maps) illustrates one image
  per group and no evidence item rests on it.

## Figures and data reader (F2d)

- **Panel read.** Fig. 2d (`figures/f2d_enrichment.py`, raster, p. 4, crop 300,228–555,362 pt): two horizontal bar
  charts of "-log(pValue)", axis on top. Left (GO processes, ticks 0–20 by 5): muscle structure 18.80, cardiovascular
  system 17.77, cardiac muscle tissue 13.56, heart 12.75, myofibril assembly 10.71, cardiac muscle cell 10.15, blood
  vessel 9.97, cardiac cell 9.97. Right (pathway maps / networks, ticks 0–6 by 1): muscle contraction 5.42,
  cytoskeleton remodeling 3.94, FGF/ErbB 2.16, Wnt/Notch/VEGF/IP3/integrin 1.80, BMP/TGF-β 1.20. Bar order checked
  against the labels printed beside the bars; it is the record's item order.
- **Value kind.** One -log p per bar, belonging to the comparison CM+EC+MC versus CM+EC. Stored as the bar's "mean"
  (readings have no p kind) and linked to group cem because a link needs one group. Nothing countable; no error bars.
- **Axis.** Tick marks in the raster are unevenly spaced (left spacings 11.6–13.3 pt per 5 units; right 10.4–13.3 pt per
  unit), so the calibration misfit (0.31 and 0.13 axis units) dominates the intervals.
- **Released data not used (shared parts).** srep29933-s5.xls ("GO Processes", MetaCore export for this comparison)
  holds the exact p of the eight GO items in column D: D9 muscle structure development 1.51e-19 (-log 18.82), D14
  cardiovascular system development 4.31e-19 (18.37), D24 cardiac muscle tissue development 2.61e-14 (13.58), D27
  heart development 5.99e-14 (13.22), D32 myofibril assembly 2.96e-13 (12.53), D37 cardiac muscle cell development
  1.53e-12 (11.82), D39 blood vessel development 1.82e-12 (11.74), D51 cardiac cell development 6.85e-12 (11.17);
  totals (col C) and in-data counts (col H) match the record's "N of M". The data reader cannot open legacy .xls
  (`livinglit/data.py` reads .xlsx/.xlsb/.csv only), so no `data.yaml` rows were written and the figure was read for
  all 13 items. Once .xls is supported these eight should be data rows (kind p).
- **Figure vs data mismatch.** The figure's bars agree with s5 for muscle structure, cardiac muscle tissue (±0.05) but
  are 0.5–1.8 lower for the other six (cardiovascular −0.6, heart −0.5, myofibril −1.8, cardiac muscle cell −1.7,
  blood vessel −1.8, cardiac cell −1.2); blood vessel and cardiac cell bars are drawn equal (9.97) where s5 gives 11.74
  and 11.17. Outside the reading intervals; not corrected. The figure may come from a different export than s5.
- **Pathway items.** s6–s10 are gene-list reports with no p, so the five right-chart values come from the figure only.
  Read values imply p ≈ 0.016 (Wnt/Notch) and ≈ 0.063 (BMP/TGF-β), above the Methods' P < 0.01 threshold the record
  quotes for every F2d item.

## Figures and data reader (F3)

- **Panel read.** Fig. 3d (`figures/f3d_echo.py`, raster, p. 5, crop 300,55–555,284 pt), four line charts, one per
  quadrant: cardiac output (mL/min), stroke volume and ejection fraction (fold increase to PreTx), LVAd (mm²). Means
  at PreTx / Tx2w / Tx4w, Tx then Sham: CO 119.6 / 141.2 / 127.8 and 115.2 / 110.3 / 99.4; SV 1.000 / 1.062 / 1.080 and
  1.000 / 0.925 / 0.826; LVAd 97.2 / 98.3 / 103.1 and 96.7 / 103.5 / 103.3; EF 1.000 / 1.029 / 0.956 and 1.000 / 0.843 /
  0.766. SV and EF at PreTx are 1 by construction and come back as 1.000 / 0.9995 / 0.9997, a check on the reading.
  Panel c (M-mode images) has no values; panels a and b are a timeline and photographs.
- **Released data.** None of the supplementary files (s5–s10, MetaCore exports) holds echo values; no data rows.
- **Time as x.** Course readings carry x = day of the echo after implantation printed in Fig. 3a (PreTx −1, Tx2w 14,
  Tx4w 28). The 4-week comparison labels repeat the Tx4w readings without x, since checks use only readings without x.
- **Error bars.** Tx bars point up, Sham bars down from a shared stem (CO, SV, EF); only the Tx upper ends are read
  (CO 130.1 / 178.3 / 150.7; SV 2w 1.256, 4w 1.311; EF 2w 1.160, 4w 1.074). That the upper cap is Tx's rests on the
  drawing convention, not a legend statement. Sham's lower ends are not stored: a reading has no lower-end kind
  (shared parts). LVAd lines cross and its caps cannot be assigned to a group, so no LVAd error is read. The spread
  (SD or SEM) is not stated for Fig. 3.
- **n.** No points drawn; the legend's n = 6 (Tx) and 5 (sham) cannot be counted.
- **Record problems (not edited).** Unit F3's `stats` (test "MetaCore enrichment analysis", p "P < 0.01 (Methods)")
  and note ("Values printed inside the figure bars (image); the -log p value is plotted only") appear copied from
  F2d. Its `other_conditions` lists cem/ce with `spread: none`, which reads as misplaced. `where` says "Fig. 3c,d";
  only 3d is quantitative.

## Figures and data reader (S1)

- **Panel read.** Supplementary Fig. 1 right (`figures/s1_protocol_populations.py`, raster, s1 p. 8, crop
  428,80–578,452 pt), three stacked bar charts with their own % axes. Read: CM+MC cTnT+ 45.76 (error top 51.14),
  CM+MC PDGFRβ+ 10.82 (13.66), MC-protocol cTnT+ 1.58 (3.30). SD per Methods.
- **Check against printed values (not stored).** The same code on the bars printed in the text gives CM+EC cTnT+ 61.80
  (printed 61.8), VE-cad+ 19.39 (19.4), MC-protocol PDGFRβ+ 74.54 (74.4). Error tops come back 70.72 / 28.13 / 82.92
  against mean + SD 69.8 / 28.5 / 82.8: caps drawn up to 0.9 off the printed SD, outside the 0.6 px intervals.
- **Not readable.** S1_vecad cmmc_p: no EC bar is drawn in the CM+MC chart (zero or not measured; the legend does not
  say). S1_vecad mc_p: only an error cap on the axis line, no fill to locate the mean. Both stay without values.
- **Thin bar.** The MC-protocol CM bar is one or two fill rows tall in the ~200 dpi embedded image and is split by its
  error stem; its mean (1.58, interval 1.35–1.81) rests on a sub-pixel edge, so the interval may be optimistic.
- **n.** Bars only; the legend's n = 5 (CM+MC) and 42 (MC protocol) cannot be counted.
- **Released data.** None (s5–s10 are MetaCore exports); no data rows.
- **Audit.** S1 items stay `cannot check` after the readings: they are measurements without a contrast.

## Figures and data reader (S2)

- **Panel read.** Supplementary Fig. 2b (`figures/s2b_wnt3a_induction.py`, raster, s1 p. 9, crop 60,268–412,428 pt),
  three bar charts side by side (CM, EC, MC), each on its own % axis, bars Dkk1 / Control / Wnt3a 50 / Wnt3a 100.
  Means (error tops): CM 17.91 (31.87), 41.07 (58.12), 46.65 (61.51), 53.64 (60.42); EC 6.153 (7.605), 10.55 (17.27),
  16.68 (24.56), 20.49 (25.44); MC 75.18 (82.74), 48.89 (80.14), 0.9738 (1.336), 1.103 (1.364). Every reading's order
  agrees with its item's printed finding. Each bar is returned under several labels, one per item it serves.
- **Thin bars.** The MC Wnt3a 50 and 100 bars are about 1 % tall: two fully coloured rows between the error cap and the
  axis line in the ~200 dpi embedded image. The cap (43 px wide at 300 dpi) lies over most of the bar (about 50 px), so
  the fill top is read only in the two to four antialiased edge columns clear of the cap. The cap sits directly on the
  fill. Their means and error tops rest on sub-pixel edges, and the standard 0.6 px interval may be optimistic.
- **n.** Bars only; the legend's n = 3-4 cannot be counted, and which groups have 3 and which 4 is not stated.
- **Error bars.** Taken as SD per Methods. The S2 legend itself does not name the spread.
- **Not read.** Panel a (representative dot plots): its gate percentages are printed in the image and are already
  recorded as values in S2_rep_ec / S2_rep_mc.
- **Released data.** None (s5–s10 are MetaCore exports); no data rows.

## Figures and data reader (S4)

- **Panel read.** Supplementary Fig. 4b (`figures/s4b_ect_area.py`, raster, page 11 of srep29933-s1.pdf): Day 14
  means of CM+EC (35.17 mm²) and CM+EC+MC (32.91 mm²). Each is a straight line fitted over the Day 6–14 segment and
  evaluated at the Day 14 error-bar stem. The upper end of the CM+EC bar is 37.57 mm². Calibrated on seven y ticks
  (0–120).
- **Error-bar assignment (judgement).** One stem at Day 14 carries a cap above both lines and one below both. I read
  the upper cap as CM+EC's upper end because at Days 2, 4 and 6 the upper series (CM+EC) is drawn upward and the
  lower one downward. If the caps were drawn the other way round, this error belongs to CM+EC+MC. The lower cap is a
  lower end only (not a reading kind), so CM+EC+MC has no error reading.
- **n.** No n is printed in the legend and no points are drawn, so nothing is countable. The spread is taken as SD per
  Methods; the S4 legend does not name it.
- **Not read.** Panel a (photographs) and the time course (`S4_area_course`, Days 0–6), which figures-needed did not
  list.
- **Released data.** None (s5–s10 are MetaCore exports); no data rows.

## Figures and data reader (S5)

- **Panel read.** Supplementary Fig. 5a (`figures/s5a_active_force.py`, raster, page 12 of srep29933-s1.pdf).
  Active force at Lmax, 2Hz/5V, mean (upper end of the error bar): CM+EC 0.520 (0.667) mN, CM+MC 0.464 (0.561),
  CM+EC+MC 0.372 (0.508). Calibrated on five y ticks (0–0.8). The cap nearest above each bar is read as the error
  bar's end; the N.S. bracket lies higher, near 0.78. The error is taken as SD per Methods; the S5 legend does not
  name the spread.
- **n.** Panel a draws bars only, so there is nothing to count. The force n in the Fig. 1 legend is 8 / 7 / 12.
- **Not read: panel b** (the same force plotted against CM ratio, coloured by ECT type). The markers do not all
  stand alone: two CM+EC near 0.71, two CM+EC+MC near 0.48, and CM+EC beside CM+EC+MC near 0.41 touch. Only six
  separate CM+MC markers are visible against n = 7; the blob near 0.45 is probably two markers. Rough check by eye,
  not a result: the eight CM+EC markers average about 0.52, which agrees with the bar. The item S5_force_cmratio_corr
  was not listed by figures-needed.
- **Released data.** None (s5–s10 are MetaCore exports); no data rows.

## Figures and data reader (S8a)

- **Panel read.** Supplementary Fig. 8a right (`figures/s8a_ec50.py`, raster, page 15 of srep29933-s1.pdf). Ca2+ EC50,
  mean (upper end of the error bar): CM+EC 1.010 (1.169) mM, CM+MC 0.887 (1.032), CM+EC+MC 1.047 (1.189). Calibrated
  on four y ticks (0–1.5). All three means are near 1 mM, as the Results text says ("around 1 mM").
- **Spread and n.** The error is taken as SD per Methods; the S8 legend does not name the spread. Bars only, no
  points and no n printed, so nothing is countable.
- **Not read: the left panel** (force against external Ca2+, item S8a_force_calcium); not listed by figures-needed.
- **Released data.** None (s5–s10 are MetaCore exports); no data rows.

## Figures and data reader (S8b)

- **Panel read.** Supplementary Fig. 8b right (`figures/s8b_caffeine.py`, raster, page 15 of srep29933-s1.pdf). Active
  force increase on 5 mM caffeine, mean (upper end of the error bar): CM+EC 26.89 (47.42) %, CM+MC 7.042 (12.33),
  CM+EC+MC 33.26 (57.07). Calibrated on seven y ticks (0–60 by 10). The wide, overlapping bars agree with the printed
  P=0.10.
- **Unit.** The y label says "fold increase" but the axis is printed "(%)"; recorded as % as printed.
- **Spread and n.** The error is taken as SD per Methods; the S8 legend does not name the spread. Bars only, no
  points and no n printed, so nothing is countable.
- **Not read: the left panel** (representative total-force trace, illustration).
- **Released data.** None (s5–s10 are MetaCore exports); no data rows.

## Vocabulary agent

- **Ids found and not found.** Adopted CVCL_A065 (201B6), MONDO:0005068 (myocardial infarction), CL:0000115
  (endothelial cell), CL:0008034 (mural cell), CHEBI:41218 (mercaptoethanol). ChEBI has no entry for Wnt3a or Dkk1
  (both own terms; Wnt3a twice, as a differentiation factor and as a treatment), nor for ECT implantation (own treatment
  term; arguably not a "treatment" in the ChEBI sense, but it is the exposure the Tx/sham comparison varies).
- **Stand-in flags (not reader errors).** `insulin_day` "d5": code's quantity parser does not read a 'd' prefix, while
  "d15" parses by accident. `donor_age` "pediatric" (TXT2, ref. 23): not a declared state; a person may add
  *pediatric* to donor_age's states.
- **Flags for the record reader.** `seeding_density` "same density as used for ECT formation" (placeholder: a pointer,
  not a density). Measures "proportion of CM, EC and MC" and "survival and tumor formation" (several measures each).
- **Split requests.** `cm_medium` "RPMI+B27" (B27) and "RPMI+10% FBS medium" (10% FBS) → supplements.
- **Guesses.** TissueTrain and its "nylon mesh anchors": the paper does not say whether the anchored ends yield, so new
  terms *linear tissue held between two end anchors* (platform) and *held between two end anchors, regime not stated*
  (mechanical_load) rather than isometric or auxotonic. "thin-coat matrigel" mapped to growth-factor-reduced Matrigel from
  the same quote ("growth factor reduced, 1:60 dilution"); "homogenized" (in Trizol) to RNA extract; "frozen" (OCT,
  for sectioning) to cryosection; "24-well plates" and "plates" to 2D culture (monolayer not stated). hbFGF in the hiPSC
  medium is a qualifier on MEF-conditioned medium: no field holds hiPSC-medium additions.
- **Measures.** Circular SD → angle dispersion (synonym added); κ of the von Mises fit is a new root measure. In vivo
  echo measures (cardiac output, stroke volume, LV end-diastolic area, ejection fraction) and engraftment (with area
  ratio and incidence as children) and vessel perfusion are new. "Increase ratio" (S8a) mapped as fold.
- **Possible record issues.** The F2d enrichment items hold gene counts ("45 of 701 genes") under measures named
  "enrichment of …"; the counts fit *number of genes in a GO term*, the wording fits *enrichment p-value* (mapped to
  the wording). The S6 correlation items hold R2 with the regression intercept and slope (Hz, Hz/%): two measures in
  one item. S8b legend says "fold increase" but values are % (expressed_as left to the values).

## Formula agent

- **Nothing rebuildable.** No force, CSA, diameter, strain, area or volume is printed and there is no data.yaml; every
  derivation is *cannot check*. The S5a force readings (per composition, mN) could not feed the 0.62 mN/mm2 mean stress
  because that value pools all ECTs (group `ect`) and no CSA is printed.
- **Young's modulus.** No library entry for sigma = E*eps, so I proposed `linear_elastic_stress_strain` (model; Gere &
  Goodno, Hooke's law). The field already has 15 given entries, so this goes over the "fewer than fifteen" target. I
  did not try a derived entry from `hooke_spring`, because that would need a strain definition (another given entry).
  The S7 average R2 is reported against "linear elastic material". Strain is described only as "lengths (up to 25%)
  from slack length", and its definition is not stated.
- **Aggregation.** I chose *mean of per-sample* for stress ("divided by the CSA of each specimen") and for E ("highest
  ... over 17 kPa (average of 8.8kPa)"). Everywhere else it is *not stated*.
- **"approximately 40%" covers CM+EC and CM+MC together**, so its derivation has no group.
- **Ejection fraction.** I mapped it to `relative_decrease` (EF = (EDV - ESV)/EDV) because "ejection fraction" is a
  named operation. The single-plane area-length volume step is named but not printed, so it goes on the completeness
  list. For cardiac output no formula is stated: no_formula.
- **S8b caffeine.** The axis reads "fold increase" in %, with means of 7 to 33 %. Read as a fold ratio, that would be a
  large decrease. I recorded the ratio, with relative change as a labelled alternative. Observation for code: the
  label and the values may not agree.
- **κ and circular SD.** Both are printed as equations (1) and (2) in the Supplementary Methods. They use Bessel
  functions and a complex mean resultant, which the allowed names cannot express, and pdftotext loses the symbols. Both
  are no_formula. EC50 is stated by citation only (spline): no_formula.
- **Engraftment / scar area.** The graft lies on the scar rather than inside it, so `fraction_bounds` was not applied.
  How the five sections per rat were combined is not stated (two labelled alternatives).
- **CM ratios (F1a).** They may have been computed from protocol purities and mixing proportions, but the paper does
  not say so; I treated them as measured fractions (bounds only).
