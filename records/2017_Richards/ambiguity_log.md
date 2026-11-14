## Record reader

- **hADSCs in later organoids.** Fig. 3B and Results 2.2 define organoids with hADSCs (50/29/14/7 %). Later legends (Figs 3G, 5–7, S9–S12) say only "developing stage cell ratio". S5 gives "the organoid ratio of cell types" as 50/29/14/7 including hADSCs, and S8 says "with hADSCs". I gave every organoid group after Fig. 3 the hADSC composition. The text never says outright that Figs 5–7 used hADSCs. S3 (media screening, before hADSCs) and Fig. 2 use the 5:4:1 composition without hADSCs.
- **Supplementary legends are in docx text boxes.** python-docx `paragraphs` do not reach them, so the gate's extractor cannot see them. Items anchored only to S-legends (S3, S5, S9, S12) and the S3 FBS levels use `kind: unit` with `file:` set to the docx. Assertive S-figure titles (S2, S8) were not recorded as claims, because a claim quote cannot be unit-anchored.
- **Fig. 3C significance lines.** There are three lines and two asterisks. At the printed resolution I could not tell which D0 bar each long line starts from. I recorded −ADSC D10 vs D0, +ADSC D10 vs D0, and +ADSC vs −ADSC at D10.
- **Fig. 7E VEGFA.** There are two lines under one asterisk. I recorded only organoid ischemia vs control, which the text supports. The partner of the second line is unresolved.
- **Fig. S3.** A single asterisk is labelled "significant difference with control", but no control is named. I wrote it as a main effect: ratiometric against the three DMEM/F12 groups.
- **Fig. S5 asterisks.** "*" means "higher than remaining" and "**" means "different than remaining". I wrote the pairs the legend's sentences name rather than every implied pair.
- **Test per item not stated.** Methods list Student's t-test, matched pairs, one-way ANOVA and two-way ANOVA with Tukey without assigning them to figures. Every `test` is `not stated`. The P is the legend's "*p<0.05", or "p<0.05 (Methods)" where only the text says "significantly".
- **"insignificant increase" / "did not change significantly"** are written as `p: not significant` so code reads them as n.s. The exact wording is kept in notes.
- **Verapamil dose.** Results say 500 μM. Methods and the Fig. 7A label say 0.5 μM. The context holds 0.5 μM with a suspected_error, and item F7A_arrhythmia also carries it.
- **Cross-reference.** Methods say the media screening is "shown in Figure S1", but it is in Figure S3. The S9 legend also says "used for media screening", which looks like a copy from S3. It is logged here only.
- **cell_types / stromal_cell / endothelial_cell overlap.** cell_types lists every cell type in the construct, and stromal/endothelial list the subsets, following each field's scope. In S8 the HAMEC group has no quote listing its full cell set, so the unit's cell_types is `not stated` and only endothelial_cell differs.
- **Medium of single-cell-type spheroids.** Written "cell-specific media" (Methods' wording). I did not infer DMEM/F12, FGM-3 or EGM-2 per type. Fig. 2 organoids predate the media screening, so their medium is `not stated`.
- **Ischemia** is split across cm_medium (low glucose DMEM, 1 g/L), supplements (serum-free), incubator_atmosphere (1% O2) and treatment ("ischemic stimulus", 6 hrs). Controls are "normoxia" with treatment none.
- **F3G(i) groups** differ in both the oxygen window and the measurement day (D10 vs D20). Code will see the confound. The claim's "TUNEL increase" is the opposite sign of the item's viability index, so asserts_direction is unset.
- **Left out:** Fig. 1 (mouse embryo H&E, qualitative), Fig. S1 (timeline), Fig. 4A (images summarised by 4B), S6/S7/S10B–C (images behind units F3Gi, F3Gii, F6CD), Fig. 2D (representative traces), and the S5 "theoretical organoid" (a model output computed from the single-type values).
- **Fig. 2A** is literature data (refs 45–47) shown as two other-study groups with no printed numbers. Their donor_age is "developing stage" / "adult".
- **Values printed only inside images** are recorded twice with source suffixes: the Fig. S10A table (13/19, 1/10) and the Fig. 2E labels (100%, ~50%). The S11 ± spread is unlabelled (`not stated`). The Fig. 2E legend says SEM, but no Fig. 2E values are printed.

## Figures and data reader (F3Gi)
- Fig. 3G(i) (journal_version.pdf p. 4; the whole Fig. 3 is one raster image) plots four bars with error bars (10% O2 D0-D10, D10-D20; 21% O2 D10, D20) and no individual organoid markers, so it is recorded under `no_points`; no script was written. Printed n=4-7 organoids cannot be checked against counted points.
- The supplement .docx has no tables; its Fig. S6 legend describes images and gives no values. No released data file covers these groups.

## Figures and data reader (F3Gii)
- Fig. 3G(ii) (journal_version.pdf p. 4) has no quantitative panel: it shows a schematic of macrotissue assembly and three confocal images (TUNEL/DAPI, vWF/DAPI, merge). Fig. S7 (supplement .docx) is images too, and its legend says only "minimal TUNEL-positive apoptotic nuclei" and "extensive" vWF networks. The unit is recorded under `no_points`, and no script was written.
- Items F3Gii_tunel and F3Gii_vwf have no printed, tabulated, plotted or released values, so printed n=3 macrotissues cannot be checked. F3Gii_tunel's "no significant changes" has no plotted reference group (already noted by the record reader).

## Figures and data reader (S5)
- Fig. S5 (NIHMS894081-supplement.docx, raster image) shows (A) VEGFA and (B) VEGFR2 mRNA as open bars with error bars for hiPSC-CM, cFB, HUVEC, hADSC and organoid, plus a hatched "theoretical organoid" bar. No individual experiment markers are drawn, so the unit is recorded under `no_points` and no script was written. Printed n=3 experiments cannot be checked against counted points.
- The supplement .docx has no tables, and no released data file covers these groups. The legend does not say whether error bars are SD or SEM.

## Figures and data reader (Fig. S9)
- Fig. S9 (supplement .docx, raster image9.jpg) plots laminin-positive fraction area for spheroids and organoids at D0 and D10 as bars with error bars only (no individual microtissue markers), so it is recorded under `no_points` and no script was written. The error-bar type (SD or SEM) is not visible in the image.
- The supplement .docx holds no tables, and the paper releases no data files, so no `data.yaml` rows give these groups.
- Points could not be checked against the printed n (n=3-6 microtissues) because the figure plots none.

## Figures and data reader (F6CD)
- Fig. 6C–D (journal_version.pdf p. 7, raster) plots cTnI/α-SA and MLC-2v/α-SA fraction area as one open (spheroid) and one filled (organoid) bar each with error bars; no individual microtissue markers, so it is recorded under `no_points` and no script was written. Error-bar type (SD or SEM) is not stated in the Fig. 6 legend.
- Fig. S10B–C (supplement .docx, image10.jpg) shows immunofluorescence images only; S10A's table holds Z-line counts for another item, not these groups.
- No released data files exist, so no `data.yaml` rows; points could not be checked against the printed n=3 microtissues.

## Figures and data reader (S12)
- Fig. S12 (supplement .docx, raster image12.jpg) plots VEGFA (A) and IL6 (B) mRNA expression as paired open (control) and filled (ischemia) bars with error bars for hiPSC-CM, cFB, HUVEC, hADSC and organoid. It has no individual experiment markers, so it is recorded under `no_points` and no script was written.
- Panel B prints "NA" for hiPSC-CM and HUVEC IL6, so those groups have no bar at all.
- The supplement holds no tables, and the paper releases no data files, so there are no `data.yaml` rows. Points could not be checked against the printed n=3 experiments.

## Vocabulary agent
- **`D0` (day_of_measurement) flagged as a placeholder, but the real cause is code.** `quantity_value` requires a digit not preceded by a letter, so "D0" fails; "D10"/"D20" pass only because their second digit follows a digit, and they parse with no unit. A parser fix (read "D<n>" as day n) would clear it; otherwise the reader can write "Day 0", which the paper prints.
- **Flags (placeholder):** donor_age "developing stage" (no age; the cited studies' stage is unread); composition "developing stage cell ratio" (S8; a ratio printed elsewhere); cm_medium "cell-specific media" (a different named medium per group: Methods name iCell Maintenance Medium / DMEM/F12 + 10% FBS, FGM-3, EGM-2); incubator_atmosphere "normoxia" (a word in a quantity field; Fig. 3G gives 21% O2 for its controls).
- **Probable record issues (not fixed):** "whole spheroid" maps to intact (live) tissue, which suits the beating and calcium videos, but S4 is fixed, immunostained whole-mount confocal, so its preparation should be fixed. Unit S8 has cell_types *not stated*, but its stromal_cell is cFBs + hADSCs and its composition is the developing-stage ratio (no hADSCs). F2A (literature ratios) carries preparation "cryosection" and the organoid platform although its values come from other studies.
- **Judgements:** "time to 50% calcium decay" is defined from the start of the transient to the half-decay, so I mapped it to calcium transient duration (level "50% decay"), not decay time. "time to peak calcium" is rise time, level "start to peak". "contraction amplitude" is fractional area change, as the paper equates them. TNNI3/TNNI1 and MYL2/MYL7 ratios are gene expression with the ratio in the `gene` qualifier, not isoform fraction. TUNEL index is cell viability. I left `normalised_to` out of gene expression (the F7E/S12 plots may be fold vs control) and out of normalized beat rate (unstated).
- **New terms:** platform organoid aggregate macrotissue (under cell aggregate); DMEM/F12 sits under DMEM as a sibling of Advanced DMEM/F12, because edits cannot move Advanced under it. cell type fraction by number is a sibling, not a child, of proportion of cells assigned to a cell type, whose definition limits it to single-cell classification.
- **Ids:** HAMECs → CL:2000072 adipose microvascular endothelial cell. CL:0002570 is adopted for stromal_cell as well (hADSCs). No ChEBI entry exists for ischemia or for serum-free, so both are own terms.

## Formula agent
- **Nothing can be rebuilt.** No readings or data exist (every figure is under `no_points`), and the only printed derived values are S11 amplitude/bpm and F2E % beating, whose inputs are not printed. All 63 derivations are therefore *cannot check*. The library-form check still runs: 55 are consistent, 5 wait on the proposal, and 3 have no formula.
- **Contraction amplitude** ("percent change in fractional area change amplitude between contraction and relaxation") is ambiguous. I mapped it to relative_decrease (x0 = relaxed area) and listed alternatives: signed change, relative to the contracted area, and percentage-point difference.
- **dCt "to the geometric mean of GAPDH and ACTB"** could be the geometric mean of the Ct values (as literally written) or the arithmetic mean of Ct (the usual geometric mean of quantities). Both are alternatives. I mapped 2^(-dCt) to ddct_relative_expression with ddct := dCt, because there is no calibrator. Whether F7E/S12 bars are also normalised to control is not stated.
- **Not recorded:** the S5 "theoretical organoid" bar (0.50·CM + 0.29·cFB + 0.14·HUVEC + 0.07·hADSC, a stated weighted sum) has no evidence item, so no derivation could be keyed to it. F7D "normalized beat rate" states neither its normalisation nor its reference (no_formula). S11B bpm method is not stated (no_formula).
- **Viability index** 1 − TUNEL/DAPI needs the proposal complement_of_ratio (derived from ratio_def + complement_fraction). It assumes the TUNEL-positive area lies within the DAPI area. The gate accepted it.
- **F7A–C normalized F/F0:** the baseline groups are 1 by construction (normalised to their own pre-treatment transient), so a test against baseline compares with a group of SD 0 (normalized_to_own_control). I did not check what the bars show.
- **Spec gap:** the gate cannot see supplement (docx text-box) text, so no derivation is anchored to an S-legend. S5/S12 items reuse the Methods qPCR anchor.
