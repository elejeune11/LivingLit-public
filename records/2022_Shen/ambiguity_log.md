## Record reader

- **Fig. 1B P conflict.** The text ("Ca2+ p < 0.0001") and the figure label ("Calcium p < 0.0001") disagree with the legend ("two-way ANOVA p = n.s. (B and C)"). Recorded p < 0.0001 from the text and put a suspected_error on the item. Only one `p` per item, so a conflict between printed Ps cannot be stored as two values.
- **Figure text in main.pdf cannot be extracted** (neither extractor finds labels such as "Calcium p < 0.0001", "Pacing p = 0.004", "3-way ANOVA p < 0.0001" or the significance stars). Items resting only on those labels (F5_ttp_ffr, F5_rt50_ffr, F5_prp_pace, F5_prp_ca, F5_t80_pace, the F5A star pairs) use `kind: unit` anchors. Figure text in mmc1.pdf can be extracted and is anchored as text.
- **Fig. 5A star pairs** are printed only as brackets with no legend text. The legend gives thresholds for `**`, `***` and `****` only, so single-star pairs have p "not stated". I chose the condition side for each pair myself (the paced or high-Ca2+ group first).
- **Pairs with no control** (Fig. 5G "HC-NP vs. LC-RP"): neither group is a reference, so I kept the printed order. "HC-NP vs. HC-RP" is written HC_RP first (condition first).
- **Fig. 5 legend n mapping.** The legend gives "FURA data (M, N, and T–W)", but the FURA panels are L, M and S–V. I used the FURA n for L, M, U and V, and the ISO n for P, Q and R. Logged as a cross-reference.
- **Culture calcium vs measurement calcium.** `media_calcium_mM` holds the culture value (1.8 / 0.42 mM, as the paper names its groups). All measurements were made in Tyrode's solution with 1.8 mM Ca2+, and that sits only in `method`. The schema has one field for two calcium concentrations.
- **cm_medium and media_calcium_mM both differ** between HC and LC groups (DMEM vs RPMI). The paper itself says the media also differ in amino acids, vitamins, Na+ and Mg2+ (Table S1). I recorded both fields per group, so code will see a confound. This is the paper's real design, not a reader choice.
- **Training pacing vs measurement pacing.** I put ramp pacing (2–4 Hz, 2 weeks) in `maturation_strategy` and the stimulation during measurement in `pacing` (1 Hz, the 1–3 Hz staircase, or the post-rest protocol, set per item). Spontaneous beating rate has pacing "none".
- **Second cell line protocol.** The paper says the second line was "differentiated with 17.5 mM CHIR99021 on day 0. The same differentiation protocol was followed after day 0". I recorded IWP4, 48 h Wnt inhibition and lactate as stated by that sentence. The CHIR duration for this line is "not stated". `cm_day_at_formation` is "day 10" with the qualifier "after expansion" (seeding happened on day 10 after expansion).
- **pdftotext renders µ as "m"** ("15 mM CHIR99021", "1 mM ISO"). The page image shows µM, and qualifiers are written as µM.
- **Which cell line for the RNA-seq / western units (F4, S1, S2)**: the legend says "one separate differentiation batch of the same single cell". I took this to mean the first line (PGP1), since the second line is introduced only after these results.
- **S2 benchmarking groups from other studies** (Sim, Mills, Zhao) carry `citation` and group contexts for platform, cell_line, cm_medium, media_calcium_mM, maturation_strategy and preparation. The other paper-wide fields (substrate, cell_types, differentiation factors, B27…) still resolve from this paper's default and unit context for those groups, which is wrong for them. The schema has no way to set a group's context as "another study, fields not applicable". Sim's Fetal / Young / Adult groups differ only in donor age, and there is no field for age, so code will find no differing field between them.
- **Day of measurement, Fig. 1.** The text says "After 24 days in culture" and the schematic marks testing at day 25 post-seeding (suspected_error). Days are counted from seeding, not from differentiation, and are qualified "post-seeding".
- **TXT1** ("TTP of approximately 290 ms, RT50 at 120 ms") does not name a group or figure. It matches HC-RP in Fig. 2I/J, so I made it a text unit with one HC-RP group (first line). "approximately 290" is kept as printed.
- **Representative traces** (Fig. 2C; Fig. 1D, 2H, 3A/B, 5E and others) are not measurements. Only Fig. 2C is recorded (F2_ffr_repr), because the text draws a conclusion from it ("positive FFR behavior up to 2 Hz").
- **RNA-seq gene lists.** Each gene named with an arrow in the text became one item, with stated_direction and the threshold p < 0.05 given in the Results/Methods. The Discussion's "addition of both high Ca2+ and ramp pacing together shows additional upregulated … (ACTA1 …)" names no figure or comparison, so it got no items. Claim C19 rests on the matching Fig. 4E items.
- **Diastolic excess fraction is defined two ways**: in the text as diastolic force at 3 Hz relative to rest, and in Fig. 2K's legend as the ratio between 3 Hz and 1 Hz diastolic baselines. Both are recorded as `definition` on their items.
- **Fig. 5K "two-way ANOVA p < 0.0019"** is printed with "<" before a four-digit value. Kept as printed.
- **Methods statistics paragraph** names only t-tests and two-way RM ANOVA (Figs. 2–4), not Fig. 5's three-way and two-way ANOVAs. Tests are taken from each legend.
- **Discussion glucose** "(5.33 and 1.80 mM, respectively)" conflicts with Table S1 (glucose 25 mM). suspected_error on ST1_glc.
- **PCA**: PC1 61% + PC2 12% = 73%, but the panel title says "PC1-PC2: 76% Variation" (suspected_error).
- **Fig. 2 force unit**: panels D, K and L read "(nN)", while H and Figs. 1 and 5 read µN (suspected_error on F2_ffr_raw).
- **Missing files**: none. The RNA-seq data (GEO GSE201437) are named but no item rests on them as source data. mmc2.pdf is main.pdf followed by mmc1.pdf.

## Figures and data reader

- **No released data.** mmc1.pdf (supplement) and mmc2.pdf (article + supplement) hold no tabular source data. Table S1 is a printed table in the PDF, already recorded as printed values. No `data.yaml`.
- **All panels read are vector.** That is 43 panels in main.pdf, in 65 `figures.yaml` entries. Pairwise Fig. 5 items reuse their panel's script through small wrappers (`f5x__<item>.py`) that keep only the item's two groups. Bars: Fig. 1E/F/H/I, 2I/J/M/N/P/Q, 3C/D/E/H/I, 4A–C (6 panels), 5A/F/G/J/K/L/M/P/Q/R/U/V. Curves (mean markers only, each carrying x = frequency in Hz; error bars not read): Fig. 1B/C, 2D–G, 5B (both)/C/D.
- **Tick labels are not text.** They are glyph outlines with no text layer, so `fig.words()`/`tick_marks()` find nothing. Each script calibrates from the tick-mark line positions, paired bottom to top with the label values read from a render of the glyphs. The values are listed in the script, and the script fails if the count of tick marks differs from the count of values. Calibration misfit is 0 (to 1e-6) on every axis.
- **Bar means.** Taken from the vertex where the two-segment error stem meets (stroked style), or from the outer edge of the bar outline (Fig. 2, where every stroke is converted to a filled shape). Both agree with the mean of the read points to within 0.05 pt wherever all points are drawn.
- **Counted points vs printed n.** These match in Figs 1, 3, 4 and Fig. 5G/L/M/P/Q/R/U/V. Fig. 2 LC-RP: 6/6/11/11/6/6 (I/J/M/N/P/Q); Q's n is not stated in the record (the legend gives O–P n = 6). Mismatches:
  - Fig. 2 I, J, M, N, P, Q: **HC-RP points are not drawn** (bar and error bar only). They are returned with no points (`countable: false`).
  - Fig. 5F: LC-NP 13 points drawn against n = 14. The drawn points average 0.2445 s against a bar mean of 0.2515 s.
  - Fig. 5J: LC-NP 13 against 14; LC-RP 11 against 12.
  - Fig. 5K: HC-RP 12 against 13; LC-NP 12 against 14; LC-RP 10 against 12. The LC-NP and LC-RP drawn-point means fall below their bar means (0.244 vs 0.258; 0.261 vs 0.274).
  - Undrawn points may lie outside the plotted range, but this is not established. The values are recorded as drawn.
  - Fig. 5A (n not stated): 6 / 5 / 6 / 4 points (HC-NP / HC-RP / LC-NP / LC-RP).
- **Units as printed on the axes.** Fig. 2D (F2_ffr_raw) reads "nN", while Figs 1B and 5B read µN (see the record reader's suspected_error). Panels whose axis prints no unit are given `unit_of_value: no unit printed`.
- **Not read:**
  - Representative traces (Fig. 1D/G, 2C/H/K/L/O, 3A/B/F/G, 5E/H/I/N/O/S/T). These are not measurements; F2_ffr_repr rests on Fig. 2C traces.
  - Fig. 4D heat map (F4_heatmap). Its cells are per gene and per sample, while the item holds no per-group value.
  - Fig. 4E–H volcano plots (F4E_*–F4H_*). Each labelled point is a contrast's fold change and P, not a group value, so it cannot be linked to one group.
  - mmc1 Figure S1 (volcanoes, pathway maps) and Figure S2 (PCA scatter, contrast heat map), for the same reasons.
- **LivingLit issues (reported, not edited):**
  1. `FigureSource.drawings()` filters with `Rect.intersects`, which is False for the zero-width or zero-height box of a vertical or horizontal stroked line. Axes, ticks and error stems are therefore dropped. `_util.drawings()` works around this.
  2. In `checks.py` "points to P" (readings basis), each end of the P interval is judged separately. An interval that brackets the printed P is called "inconsistent": F3_force has P interval [0.000925, 0.001549] against p = 0.0012, and F4_pln has [0.0396, 0.0576] against p = 0.0477. Affected (pooled-t interval brackets the printed P): F3_force, F3_ttp, F3_ca_amp, F3_t80 and F4_pln are called inconsistent, and F4_serca is called close.

## Vocabulary agent

- **Relative measures.** Percentage changes on isoproterenol (force, TTP, RT50, Ca2+ transient intensity, t80) and the normalized FFR got child terms (`relative_*`) under their base measures, carrying `normalised_to` and `expressed_as`, because they are dimensionless and differ from the base quantity. The spec does not say whether a change-from-baseline should be a child term, a qualifier or a derivation (tab 4); a re-map may fold them into one pattern.
- **Qualifiers not filled from method.** Western blots are normalised to total protein and Ca2+ amplitudes are Fura-2 F340/F380, but both are stated only in `method`; `protein_level.normalised_to` and `calcium_transient_amplitude.normalisation` are left empty (no field filled from another field's text). Value keys that require them will block; the reader could write them as measure qualifiers.
- **Normalized FFR reference not stated** ("normalized systolic peak forces"): `normalised_to` left empty.
- **Flags (several measures, 3):** "RNA expression of genes of interest" (heat map over many genes), "log2 fold change of 50 cardiac genes" (S2C), "time to peak and time to 50% relaxation" (TXT1). Each needs one item per measure or per gene.
- **"time to peak"** mapped to time to peak force without a synonym: alone it is broader (could be a calcium transient).
- **"engineered heart tissue"** mapped to the broad `3D engineered tissue` (synonym added): the format (tissue on a decellularized myocardium slice) is in `substrate`, and the platform is not filled from it. A format term under engineered_3d may be wanted once another scaffold-slice paper appears.
- **"human ventricular samples"** (Sim et al.) is one text for fetal, young and adult groups, so it maps to `native heart tissue`; donor age lives only in the group labels, not in a context field.
- **"rapid pacing"** (Zhao et al.) maps to the broad electrical stimulation: the paper does not say the rate was ramped. "ramp pacing" is a synonym of intensity training (frequency raised over culture, as in Ronaldson-Bouchard's regime).
- **"Akt expression"** is a KEGG pathway node, not a named gene (AKT1/2/3); mapped as gene expression with gene "Akt".
- **Second line** has no name or accession: own term in cell_line, no synonym (the phrase "second healthy control line" would mis-match other papers).

## Formula agent

- Normalised FFR (F1/F2/F5_ffr_norm): the text names the normalisation but not its reference. I took the 1 Hz force as F1
  because each normalised curve reads 1.00 at 1 Hz; derivations at 3 Hz per group, from the raw-curve readings. No value is
  printed, so `output` is empty and code gives no verdict; the rebuilt ratio of group means (e.g. F5 HC-NP 0.26) can be set
  against the normalised curve (f5b_norm HC-NP 0.31 at 3 Hz). A difference is expected if each EHT was normalised to its own
  1 Hz force (ratio of means vs mean of ratios); the spec has no way to point a derivation's output at a reading.
- Diastolic excess fraction: Fig. 2K legend says "ratio between 3 Hz and 1Hz diastolic baselines"; the Results say
  "relationship between the diastolic force at 3 Hz and at rest". Written as the stated ratio; "excess over baseline"
  ((D3 - D1)/D1) and the rest reference are labelled alternatives.
- p-PLN/PLN and p-cTnI/cTnI are named only in the Discussion; no item records them. I rebuilt them (ratio of group means of
  the content panels, keyed on F4_ppln / F4_pctni) without an output. Rebuilt p-PLN/PLN: HC-RP 0.22, LC-RP 0.46, matching the
  Discussion's direction.
- ISO percentage changes and PRP/DEF/western normalisations: before/after and per-lane values are not given, so these
  check symbolically only.
- Fura-2 F340/F380 (record method) is not found in the paper text, so no ratio derivation was written for Ca2+ amplitude.
- S1 DEG totals (341 = 182 + 159; 653 = 335 + 318) are consistent sums but no formula is stated; not derived.
- PCA: proposed `cumulative_variance_explained_two` (definition, Jolliffe 2002). Code finds PC1-PC2 76% inconsistent with
  61% + 12% = 73% (the reader's suspected error); PC1-PC3 67% consistent.

## Record reader (re-read v3)

- **Other-study groups (S2).** SIM_FETAL/YOUNG/ADULT, MILLS_MM/CTRL and ZHAO_RP/CTRL are now `kind: other study` with their citation and a group anchor (the Discussion sentence that describes them). Their context holds only what Shen states: Sim `platform: human ventricular samples` with `donor_age` fetal / young / adult; Mills `platform: engineered three-dimensional tissues` (MM also `maturation_strategy: maturation media`); Zhao `platform: engineered tissues` (RP also `maturation_strategy: rapid pacing`). The controls' maturation strategy is not stated by Shen ("control/least mature group"), so it is left out. Kept `other study` rather than `native tissue` for Sim because the data are another study's.
- **Gate gap: benchmark groups.** `gate_record.check_record` resolves a benchmark group to its own context but still demands every field, and `BENCHMARK_STATE` ("not stated in this source") is never filled in by code. To pass the gate I wrote `not stated in this source` explicitly for every unstated field of the seven other-study groups. Once the gate fills that state itself, these lines can be removed.
- **S2 engineered groups.** Platform, cell line and preparation are the same for HC-RP and LC-NP, so they moved from the groups to the S2 unit context. The engineered-group rules no longer count the benchmark groups.
- **measurement_calcium_mM.** `1.8 mM` (qualifier Tyrode's solution, anchored to the Discussion's "characterized in the same Tyrode's solution (1.8 mM Ca2+)") is set in F1, F2, F3, F5 and TXT1. "(1.8 mM CaCl2)" is removed from every `method`. The F5A spontaneous beating rate items say `not stated`, because the rate is reported "after ramp completion" and no bath is named. Lysate units (F4ac, F4d, F4eh, S1, S2) and ST1 are `not applicable`. No measurement was made at several bath calcium levels, so no calcium-level groups were added.
- **mechanical_load.** `isometric` in every tissue unit, anchored to the Introduction ("EHT grown under isometric conditions"). Guess: this describes culture, because tissues sit on PTFE holders throughout. The 10% stretch at testing stays in `method`. ST1 is `not applicable`.
- **donor_age.** F5 is `adult` (qualifier: healthy adult male, as stated for the second line). For PGP1 units it is `not stated`, and for ST1 `not applicable`. **transgene:** `none` in default_context. Nothing is introduced, but the paper never says so; I chose `none` to match `endothelial_cell: none`.
- **Several printed P.** F1_ffr_raw: `p` is the text's "p < 0.0001", and `p_values` holds the legend's "p = n.s." and the Fig. 1B label "Calcium p < 0.0001" (unit anchor). The old suspected_error was replaced by a note, since code now reports the disagreement. F5_ca_amp: the Discussion's p < 0.0001, plus the Fig. 5L label "Calcium p < 0.0001" in `p_values`. All the other figure stars in Figs 2–5 agree with the legend Ps, so they were not added.
- **Unthresholded stars.** The Fig. 5 legend defines only `**`, `***` and `****`, so the single-star pairs F5_beat_LC_RP_LC_NP and F5_beat_HC_RP_LC_RP get `significant, threshold not stated`. The Methods sentence "A p value of <0.05 was used for all analysis to be considered significant" is a significance criterion, not a star legend, so I did not use it as the threshold.
- **Levels of a number.** The FFR staircases (F1B/C, F2D–G, F5B–D) print only effects between culture groups across 1–3 Hz, and no test along frequency within a group. Frequency therefore stays as `x` on curve values, not as frequency groups, which keeps the readings' group ids stable. No dose or time levels exist.
- **over.** ST1_k and ST1_glc `both_text` (one Discussion number for both media) now carry `over: [DMEM, RPMI]`.
- **Renamed or split.** TXT1_kin became TXT1_ttp and TXT1_rt50 (one measure each; vocabulary flag "several measures"), and claims C3 and C16 now rest on both. C29 is split into C29 (higher post-rest potentiation, F2_prp) and the new C31 (smaller diastolic excess fraction, F2_def).
- **asserts_direction** is given only where every item a claim rests on goes the same way: up for C2, C4, C6, C7, C11, C14, C15, C18, C19, C20 and C29; down for C3, C21 (HC is the condition, and low Ca2+ is higher) and C30; none for C8 and C28. Mixed claims (C1, C5, C9, C10, C12, C13, C22–C24) and claims that are not comparisons (C16, C27) have none.
- The YAML anchors (&id) are expanded in the file (re-dumped without aliases). The content is otherwise unchanged.

## Vocabulary agent (re-map v3)

- **Relative measures moved to base terms.** "normalized peak force" is now `twitch_force` `expressed_as: normalised` (the Normalized FFR's reference force is not printed, so no `normalised_to`). The five isoproterenol items ("... in percentage", Fig. 3C-G) are now `twitch_force`, `contraction_time_to_peak`, `relaxation_time` (level 50%), `calcium_transient_amplitude` and `calcium_transient_decay_time` (level 80%), each `expressed_as: % change`, `normalised_to: before isoproterenol`. The `relative_*` terms this paper added earlier stay in the vocabulary (edits only add) and their keys are left as they were; no mapping uses them.
- **Keys.** The base keys for those five measures now require `measure.expressed_as` and `measure.normalised_to` in the value key: a % change from before a drug and a ΔF/F0 are both `% change` and differ only in what they are divided by. Calcium timing, relaxation and time to peak already required `measure.level`; contraction frequency already required `pacing` in both keys. `diastolic_excess_fraction` and `force_frequency_relationship` required `culture_calcium_mM`; both are measured in the 1.8 mM Tyrode's bath, so their value keys now require `measurement_calcium_mM` (culture calcium is this paper's contrast, not a matching condition).
- **`mechanical_load` "isometric"** matched by a new synonym on `mechanical_load:isometric` ("EHT grown under isometric conditions").
- **`donor_age` "adult", "young", "fetal" flagged (spec gap).** `donor_age` is a quantity field with no named states, and an agent cannot add a state or a term to a quantity field, so these age classes (printed as such: Sim et al.'s Fetal/Young/Adult groups; the second control line from "a healthy adult male") can only be flagged. The flag list has no kind for "a word where a quantity field expects a number", so `not a context` stands in; it is not a reader error. Suggest declaring age-class states for `donor_age` (fetal, young, adult) in field content, or making it a terms field. Until then the S2 other-study groups cannot be compared on donor age.
- **Dropped:** the mapping and flag for "time to peak and time to 50% relaxation" (no longer stated). Kept: the two *several measures* flags ("RNA expression of genes of interest", "log2 fold change of 50 cardiac genes"), which still name many genes in one item.

## Vocabulary agent (key checkpoint)

Re-map checkpoint after 10 papers (03-vocabulary, Earlier papers; 05-across-sources, Standing keys), after the independent check of release v5-rebuild-10. 8 standing_key edits revise the keys of the measures this paper first added.

- Value keys now require treatment, genotype and disease_model for every measure whose value a drug, variant or disease can change. Left unchanged: method, device, design and yield measures (analysis time, required sample size, micropattern yield, usable constructs, post spring constant, applied load, strip bending force, between-sample variability, identified protein count, PCA variance, medium composition, signal-to-noise, embryoid body diameter, cardiomyocyte yield, beating onset).
- Direction keys of force and beat-rate measures now require pacing (paced against spontaneous), so a spontaneous and a paced isoprenaline response do not meet.
- Guess: kinetic times (twitch duration, relaxation and calcium decay times) are also rate dependent, but their direction keys were not given pacing; the request named rate and force only.
- Concern for a person: genotype and disease_model are 'not stated' for most healthy lines, and an unstated must-match field blocks a value comparison. A dry run of the revised keys leaves 2 cross-paper value agree/differ verdicts of 104 (44 with treatment alone). The relaxation report will name genotype; whether an unstated genotype of a healthy line should count as wild type is a design decision.
