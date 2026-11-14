# 2017_Mills · ambiguity log

## Record reader

- **Where glucose, palmitate and insulin belong.** The screens vary glucose, palmitate and insulin, which are
  medium components but also what each comparison varies. `supplements` is declared as "routine additions ... the
  same across compared groups", so I put the base additions (B27, GlutaMAX, ascorbic acid, Pen/Strep) in
  `supplements` and the varied substrates in `treatment` with qualifiers (`glucose`, `palmitate`, `insulin`).
  Insulin's presence or absence is a qualifier of `treatment` rather than a field of its own, so a reader looking
  for "±insulin" has to read the qualifier.
- **Paper-wide fields that one unit contradicts.** `default_context` may hold nothing a unit overrides, so
  `cm_medium`, `supplements` and `treatment` sit on every group of every unit (they are the CTRL-medium/MM
  contrast), and `cell_line`, `platform`, `substrate`, `preparation`, `pacing`, `temperature`,
  `day_of_measurement`, the two calcium fields, `mechanical_load`, `replating_coating` and `transgene` are
  repeated in every unit. That is a lot of repetition for a paper where one medium pair runs through 99 units.
- **`insulin_day`.** The SI states 3 d of mesoderm medium, then 3 d of IWP-4, "followed by another 7 d of RPMI
  B27+ (… with insulin)". No day is printed; I wrote `day 6`, which is arithmetic on the stated durations rather
  than a stated value. If that counts as filling a field from another field's text, it should be `not stated`.
- **`maturation_strategy`.** MM is the paper's maturation intervention, but it is already `cm_medium` plus
  `treatment`, and the posts are already `mechanical_load`. Writing "metabolic maturation" here would fill one
  field from another's words, so every unit says `not stated`.
- **Marks sitting between axis ticks.** In the dose–response panels (Fig. 2 B and C, Fig. S1 B and C) the
  asterisks sit over plotted points. Where a point is on a labelled tick I wrote a pair item with that dose as a
  group. For Fig. S1B calcium the two lower marks fall between labelled ticks; I read their x by eye (1.2 and
  1.6 mM) and wrote them as groups. Those two x values are not printed anywhere.
- **Counts that are not a group's value.** The GO-term panels (Fig. 3 F and G, Fig. S5D, Fig. 7K) print gene
  counts per term, and Fig. 4F prints fold differences per metabolite. A count of genes in a term is not a
  measurement of either group, so I wrote them as `between: [mm, ctrl]` values with the term or metabolite in
  `x`. `x` is documented for doses, frequencies and times; using it for a term name is a stretch.
- **Heat-map cells as groups.** Each screen is 16 (or 32) groups plus a CTRL-medium group, written one group per
  cell, with one measurement item carrying every printed cell and one pair item per printed asterisk. The record
  therefore has 482 groups, most of which exist only to hold two numbers.
- **"n (9 exp)" and friends.** Fig. 2 A, F and G and Fig. S3 A and D print n as a table row ("n (9 exp)", then a
  number per column). I put the row label in `n.printed` and the per-column numbers in `n.per_group`, so
  `printed` is not a sentence a reader would recognise.
- **Spreads without a label.** The SI Methods print "k = 14.2 ± 2.4 μN/μm (n = 10)" with no spread named; I wrote
  the 2.4 as a `sd` value with `spread: not stated` on the mean, which forces a kind the paper does not state.
- **P states the schema has no name for.** Fig. 5B prints "P < 0.09", Fig. 7C "P < 0.07", Fig. 1J "#P = 0.07" and
  several panels "NS" or "not significant". I wrote each exactly as printed; `NS` and `not significant` are not
  the named state `n.s.`, so code may treat them as unparsed rather than as P ≥ 0.05.
- **Two counts of the same analysis disagree.** The text says 3,856 differentially regulated transcripts while
  Fig. S5E prints 2220 down and 1436 up (3,656); the text and Fig. 7A say 2,120 down-regulated genes while
  Fig. S5E says 2220. Both are logged as `suspected_error` on the items that carry them, not corrected.
- **Neonatal rat cardiomyocytes as a group kind.** Fig. S8 A and B use primary neonatal rat ventricular
  cardiomyocytes. `native tissue` is the only kind that inherits nothing, so I used it, although the cells are
  dissociated primary cells in 2D rather than tissue.
- **Compound 6.28 as a group.** Fig. S9J is a kinase dose–response for the compound itself, with no hCO in it. I
  made it an `other study` group citing the patent (46) so the IC50 values have somewhere to live; it is really a
  reagent characterisation, not a group of this experiment.
- **Panels with no numbers and no test.** Several panels are images only (Fig. S2 E and F, Fig. S4 A–C and E–J,
  Fig. S6, Fig. S8 A, D, F, J and K, Fig. S9 A and I). They are not units here, because no item would rest on
  them; the schema has no place for "shown but not measured".

## Orchestrator
- `insulin_day`: set to `not stated`. "day 6" was arithmetic on stated durations (3 d + 3 d), not a printed value; flag, never infer (CONTRIBUTING, Fixed rules).

## Figures and data reader

- **No released data** (no .xlsx/.csv), so no `data.yaml`. Every value comes from figures.
- **62 figure entries, 478 readings, all bars or markers (mean and upper error-bar end); no points.** Every
  panel is a bar chart or marker curve without individual points, so no n is counted and no points-to-P check is
  possible; readings feed directions and printed-value comparisons only.
- **Raster panels (60):** Fig. 1H, K, L; 2B, 2C, 2E (force, duration); 3H, 3I; 4B–E; 5A, B, C, E, H–K; 6B, C;
  7B–J; S1D, S1K; S2A; S4D; S5G (four panels); S7A–C; S8B, S8E (two), S8G, S8H, S8I; S9B–G, S9H (two);
  S10B, S10C (two). All are images embedded at ~200 dpi with tick labels drawn into the image (no words, no OCR
  available), so each script types the tick values it sees and code finds tick marks, bar tops, caps and markers.
  The raster interval is widened for the resolution: 0.6 px × 300/200 = 0.9 px at 300 dpi, plus calibration misfit.
- **Vector panels (2):** Fig. S1F and S1L (bar outlines and error paths; axis from tick rects matched to tick words).
- **Checks against printed values:** bars normalised to CTRL read 0.99–1.02 (Fig. 1H, 1K, 3I, 7H, 7I, S2A, S7A,
  S7B, S9F, S10C); Fig. 7I MM reads 1.10 against the printed 11 ± 2.5% increase; Fig. S4D reads 2.37 and 2.25 μm
  against "~2.3 μm"; Fig. S8G reads 98.1% against ">98%". Fig. 1K MM/CTRL reads 0.21/1.00 (≈4.8-fold) against the
  text's "fourfold".
- **Groups a figure entry links to:** a group compared in two items (e.g. a baseline or DMSO bar) is repeated under
  a second label (e.g. "d0 (vs 30 μM)") so that each item gets it. Bars in a panel that no item compares (SF bars of
  Fig. S1L; NRG1, SCR, miR bars of S8H/S8I; AAV6-GFP (1X) of S9H, which is no group of the record) are located so
  the others are named right, but not returned. The left S9H panel's GFP control is "(1X)" while the record's
  `gfp` group is "(2X)"; only the right panel's GFP bar is linked to it.
- **Curve points carry no `x`:** each dose of Fig. 2B/2C is its own group in the record, so the readings are per
  group; an `x` would make code skip them.
- **Suspect readings (6):** Fig. 2B CTRL at 10^-8 to 10^-5 M, where MM markers and error bars cover the CTRL markers
  or whiskers.
- **Error bar equal to the mean:** where no whisker leaves the bar top (e.g. Fig. 4B CTRL, Fig. 1L MM nearly), the
  error reading equals the mean (SEM below reading resolution).
- **Not read:**
  - Fig. 2D: the figure plots seven calcium concentrations per curve (about 0.2, 0.4, 0.8, 1.2, 1.6, 2 and 3 mM,
    from marker spacing), but the record's groups are 0.3, 0.6, 1, 1.5, 2 and 3 mM; markers cannot be assigned to
    the record's groups. Record problem for the record reader. Several MM markers are also hidden under CTRL ones.
  - Fig. S1B (doxorubicin, calcium, nifidipine) and S1C (E-4031, cisapride): black markers on black fitted curves
    with black error bars at ~200 dpi; opening the mask cannot separate markers from curves and axis ticks, so the
    shared parts cannot locate them reliably. The doxorubicin panel also seems to show two markers near 10^-5 M
    for one group.
  - Fig. 2C: only MM at 10^-6 M is read (the one compared group); its baseline is not plotted (normalised), and the
    MM marker at 10^-10 M lies under the CTRL one.
  - Fig. S8E scramble bars: they lie on the axis line and are not found; only the miR bars are read.
  - Fig. 3A (PCA) and Fig. 5F (146-point scatter): overlapping markers, and points of 5F cannot be assigned to groups.
  - Fig. S3C (stacked proportions: three categories per group, no single value per group), Fig. 7K, 3F/3G, S5D
    (GO-term statistics, not group values; 3F/3G counts are printed), Fig. S9J (kinase inhibition curves for the
    IC50s, not group values), heat maps with printed numbers (Fig. 1F/G/I/J, S1E/H/I/J), tables (Fig. 2A/F/G,
    S3A/D) and histograms with printed values (S2C/D).

## Vocabulary agent

Vocabulary v13, instructions `terms_v3`. 153 values were unmapped; after the edits code matches 26 of them and 127 are
stored mappings (3 flags).

- **Flags (3).** `replating_coating` "Matrigel or laminin" is *alternatives* (the paper prints "Matrigel or laminin
  (Sigma)coated coverslips"). `cell_types` "human adult heart" and "human fetal ventricle" are *not a context*: they name
  a tissue, not a cell type, and those groups' platform already says native tissue. Each carries a split request to
  `platform`.
- **Split requests (3 values).** `cm_medium` "α-MEM with 10% FBS": FBS goes to `supplements`. `treatment`
  "Ad-YAP1(S112A)": an adenoviral construct, which goes to `transgene` (mapped meanwhile to
  `treatment:viral_transduction` with transgene and vector qualifiers; `transgene:yap1_s112a` added for the re-read).
- **Record-reader problems (not fixed).**
  - Unit S8B (neonatal rat cardiomyocytes in 2D) inherits `cell_line: HES3`, `substrate: collagen I + Matrigel`,
    `mechanical_load: auxotonic` and the Heart-Dyno post stiffness from its unit context; none applies to rat cells
    on coverslips. `cell_types` was mapped (CL:2000046, species rat), and the contradiction is left for the reader.
  - "intact cells" (S8B) was mapped to `preparation:live_cells`, but the measure is pH3 immunostaining, so the cells
    were fixed. The record uses "intact tissue" in the same way for whole-mount immunostaining (F1G, F1H, F5…), which
    the term's definition ("without dissociation or fixation") excludes. The reader should say `fixed` where cells
    were stained.
  - `supplements` varies across groups in F1H and F5 (B27 with or without insulin), while the field's scope says
    supplements are the same across compared groups; insulin is also a treatment qualifier there. Kept as stated.
    The insulin in "B27 with insulin" is mapped as the B27 qualifier `insulin`, not as a separate CHEBI:145810.
  - "nifidipine" (read from the Fig. S1B image) is mapped to nifedipine (CHEBI:7565). It is not in the extracted text,
    so no synonym was added.
- **Relative measures.** I read "relative to <group>" (RNA-seq, proteomics, qPCR, immunostaining intensity, LDH) as
  `expressed_as: fold` with `normalised_to` the reference group; log2(CPM) as `normalised` to library size; "relative
  DNA intensity" as `normalised` with no stated divisor. Where one stated measure text covers panels with different
  references ("Ki-67 relative intensity": CTRL medium in Fig. 1, the 0 mM glucose / 0 μM palmitate condition in
  Fig. 5; "MLC2v expression"), `normalised_to` is left out because one mapping serves all of them. The spec does not
  say whether a ratio to a control group is *fold* or *normalised*.
- **Measures with one value per x label** (F3F GO terms, F4F metabolites, S9J IC50 targets) are mapped once; the
  go_term, metabolite or target qualifier comes from each value's `x`, not from the mapping.
- **Ratios of two genes** ("MYH7/6", "TNNI3/1", "MYL2/MYL7", "TTN/N2B") are `gene_expression` with the printed pair
  as the gene qualifier. A key on `measure.gene` will compare them only with the same printed pair.
- **"maximum depolarisation"** (positive mV, 38 mV CTRL) is read as the action potential's peak potential, a new
  term under `action_potential`, distinct from the amplitude (S3D, ~100 mV).
- **New measures that are not cell properties:** `post_spring_constant` (the Heart-Dyno pole) and `ic50` (compound
  6.28 against purified kinases). Their keys require platform or treatment and target.
- **Ids.** H9 had three exact Cellosaurus hits. WA09 (CVCL_9773) was chosen because the paper says hESC from WiCell.
  Palmitate is ChEBI hexadecanoate (CHEBI:7896), with "palmitate" as a synonym. These are own terms because no
  ChEBI entry was found: TGFβ-1, neuregulin-1 (only a named recombinant fragment exists), the miR-199a-3p and
  miR-590-3p mimics, the scramble control and compound 6.28. L-ascorbic acid 2-phosphate (CHEBI:167162) is the parent
  acid of the sesquimagnesium salt the paper used.
- **Quantity fields.** Every quantity value parsed with a number (day_of_measurement phrases such as "9 d of culture in
  CTRL medium or MM", donor_age "1- to 2-d-old neonatal rats"), so none was flagged. The words around the numbers
  are kept as printed.

## Record reader (S8B re-read)

Instructions `record_v3`; re-read of SI Methods (*Neonatal Rat Ventricular Cardiomyocytes*, *Mitogen Screening*,
*hPSC-CM Dissociation for Single-Cell Electrophysiology*) and the Fig. S8 legend. Ids unchanged.

- **S8B (neonatal rat cardiomyocytes).** Groups are `engineered` (cultured primary cells, not tissue taken from a heart),
  so they inherit default → unit. Every default field whose value differs for the rat cells (differentiation, hiPSC medium
  and coating, Wnt days, insulin day, confluency, purification, purity method and purity, cell types, stromal and
  endothelial cells, composition, day at formation, donor age) moved out of `default_context` into every unit's context
  (02-audit, Context per unit); only genotype and disease_model stay paper-wide. S8B's unit context states: cell line,
  number of lines and the hPSC differentiation fields not applicable, neonatal rat ventricular cardiomyocytes, 1- to 2-d-old
  rats, 2D culture on gelatin-coated glass coverslips, load, pacing, temperature and culture calcium not stated, the hCO CTRL
  medium (same recipe in the SI), preparation fixed (pH3/α-actinin staining; was "intact cells"), 48 h of culture. Its
  groups hold only treatment and transgene. Purification is "not stated" with a note: the myocytes were "separated with
  Percoll gradients", and the vocabulary has no density-gradient term (a new term is needed).
- **Ad-YAP1(S112A)** moved from `treatment` to `transgene` (MOI 10 as a qualifier), as the vocabulary agent asked; that
  group's treatment is none.
- **S8B CTRL group.** The methods name three controls (DMSO, scramble miR, CMV-GFP) but the figure shows one "CTRL"; which
  one is not stated, so its `treatment` and `transgene` are `not stated` (were none).
- **Same problem elsewhere.** F2F, F2G, S3C: the starting-population (SP) group (2D hPSC-CMs at day 15, never in a
  Heart-Dyno) inherited the hCO `substrate` (collagen I + Matrigel) and `day_of_measurement` (9 d after switching to MM).
  Both are now group fields: SP substrate not stated (seeded on gelatin-coated coverslips, already its
  `replating_coating`), SP day "15 d of differentiation" with a note that it was analysed the following day.
- **Native heart groups** (F3A, F3B, F3C, S5A, S5B, S5D): `cell_types` "human adult heart" / "human fetal ventricle"
  (flagged *not a context*) are dropped (cell types not stated) and the words moved to `platform`, replacing "native
  tissue" (mapped to `platform:adult_heart_tissue` / `platform:fetal_heart_tissue`).
- Not changed: "intact tissue" for whole-mount immunostaining of hCOs (F1G, F1H, F5…), which the vocabulary agent says
  should be `fixed`; outside this re-read.

## Formula agent

Instructions `formulas_v3`, formula library v8; 125 derivations (91 with a library formula, 34 `no_formula`), 48
assumption reports, 17 bounds, 2 proposals.

- **Pole stiffness (SIM1_k).** The SI states eqs. S1–S4: tip deflection of a cantilever loaded at height x, I = bh³/12,
  and F = kδ with k = 14 μN/μm. The library had only the tip-load cantilever, so I proposed
  `cantilever_point_load_stiffness` (model, Gere and Goodno Table G-1) and `cantilever_point_load_stiffness_rect`
  (derived from it and `rect_second_moment`; matches eq. S3). Code rebuilds k = 13.99 μN/μm from the printed geometry.
  The methods' "k = 14 μN/μm" is not a record value, so the derivation has no output; the measured 14.2 ± 2.4 μN/μm is
  an independent validation, not the derivation's output. The pole is L/h = 0.7/0.2 = 3.5, short for slender-beam
  theory; reported as quotes (code can only test a ratio limit on value paths).
- **Force (38 items).** F = kδ (`hooke_spring`) with k one constant and δ per sample, not printed or plotted, so nothing
  is rebuilt; the library check and constant scaling apply. "Linear spring" is reported through the force-transducer
  validation; small deflection is not stated.
- **Normalised values.** Only MLC2v ("relative to control serum-free conditions"), Ki-67 in Fig. 1 ("relative to
  CTRL"), Figs. 5C/5E ("normalized to the 0 mM glucose, 0 μM palmitate condition") and the Fig. 4F metabolites state
  their divisor in text. The others (Ki-67 in Figs. 5, 7, S1, S7, S9; DNA intensity; RNA-seq/proteomics relative to CTRL;
  OCR % of baseline; LDH relative to −VE; F/F0; miR qPCR; S9E BIRC5) show it only on axis labels that are not in the
  extracted text: `no_formula`. The MLC2v reference conditions printed as 1.00 are checked with
  `normalized_to_own_control`.
- **2^-ΔΔCt** for the HRPT1-normalised qPCR genes only; the miR assays (RNU6B) and mtDNA (ND1/RNA18S5) do not name a
  calculation. Amplification efficiencies are not stated.
- **Counts.** `sum_of_parts` (library v8). Code: 410 + 445 = 855 proteins (consistent);
  2,220 + 1,436 = 3,656 transcripts against the text's 3,856 (inconsistent). The volcano percentages agree with 3,656
  (11.9 % and 7.7 % of about 18,650). The denominators of the volcano percentages are not printed.
- **Given-entry count.** The one given proposal (the cantilever model) brings the field's given entries up by one, close to the "fewer than fifteen" target.
- "fourfold" (F1K) has no number for code to parse; the rebuilt CTRL/MM ratio from readings is 4.8.
- Not written: the calcium EC50 (F2D; no fit formula stated), Pearson r (F3B, F3C) and PCA (F3A), which have no
  per-sample inputs, and the calcium-transient rising slope (no formula stated).

## Orchestrator (S8B)
- S8B purification restored to the stated "Percoll gradients" (it had been set to "not stated" for want of a term); the term `purification:density_gradient_separation` was added as a re-map edit with that synonym. Groups in S8B are engineered (cultured primary rat cells are not native tissue); paper-wide fields moved into each unit so S8B states its own.
- **Insulin (F1H, F5C, F5E, F5F, F5H, S7C and every serum-free group).** Insulin was recorded twice: "B27 with/without
  insulin" in `supplements` and the `insulin` qualifier of `treatment`. It is the compared factor, so it is now recorded
  once, in `treatment`; `supplements` reads "4% B27 + GlutaMAX + L-ascorbic acid 2 phosphate + Penicillin/Streptomycin"
  (326 contexts).

## Vocabulary agent (key checkpoint)

Re-map checkpoint after 10 papers (03-vocabulary, Earlier papers; 05-across-sources, Standing keys), after the independent check of release v5-rebuild-10. 21 standing_key edits revise the keys of the measures this paper first added.

- Value keys now require treatment, genotype and disease_model for every measure whose value a drug, variant or disease can change. Left unchanged: method, device, design and yield measures (analysis time, required sample size, micropattern yield, usable constructs, post spring constant, applied load, strip bending force, between-sample variability, identified protein count, PCA variance, medium composition, signal-to-noise, embryoid body diameter, cardiomyocyte yield, beating onset).
- Direction keys of force and beat-rate measures now require pacing (paced against spontaneous), so a spontaneous and a paced isoprenaline response do not meet.
- Guess: kinetic times (twitch duration, relaxation and calcium decay times) are also rate dependent, but their direction keys were not given pacing; the request named rate and force only.
- Concern for a person: genotype and disease_model are 'not stated' for most healthy lines, and an unstated must-match field blocks a value comparison. A dry run of the revised keys leaves 2 cross-paper value agree/differ verdicts of 104 (44 with treatment alone). The relaxation report will name genotype; whether an unstated genotype of a healthy line should count as wild type is a design decision.

## Vocabulary agent (re-map, terms_v4, vocabulary v68)

- `substrate` "glass coverslips" is now matched by code (a later paper's synonym), so its stored mapping was removed (matches are never stored). No other mapping or edit changed; the edits already in the log are skipped by code.
- `measure:relative_calcium_transient_decay_time` (set_scope in this paper's edits, term added earlier) is a `relative_*` measure term that terms_v4 would not add; edits only add, so it stays. Nothing in this paper maps to it.
- "calcium transient rising slope" is matched by code, but the stored mapping carries `expressed_as: fold` (printed in F/F0/s); the gate accepts it. Unsure whether a matched value's stored qualifiers count as a stored match.
- Still open from the first pass: "Matrigel or laminin" (replating_coating) flagged *alternatives*; "α-MEM with 10% FBS" split request (10% FBS → supplements); "nifidipine" (as printed in Fig. S1B image) mapped to nifedipine with no synonym; "CD90+ stromal cell" mapped to CL stromal cell with no_ontology_term.
