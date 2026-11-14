# 2020_Giacomelli

## Record reader

- **Which pairs an asterisk bracket joins.** Almost no values are printed in this paper: the bar graphs carry
  only brackets with asterisks, and the legends give one threshold for the whole panel. Where a bracket's two
  endpoints were unambiguous at high magnification I wrote one pair item per bracket (Figs 2F–H, 4C, 4D, 4F–H,
  4J, 5B, S1B, S1F, S1G). Where several brackets fan out over four or six bars and I could not attribute an
  asterisk to a specific pair (Fig. 5C, Fig. 6H/6I, Fig. S2A/S2B, Fig. S6F/S6G, Fig. S6I) I wrote one omnibus
  item per measure instead of inventing pairs. Fig. 7I has a third bracket at 2 Hz whose right-hand end I could
  not place; only the two clear pairs are recorded.
- **Direction of a pair.** The spec asks for condition first, reference second. For the five-group panels I made
  CMECFs the condition and CMECs, CMFs or CMEC SFs the reference, because the text words every comparison that
  way; for Fig. 4D and Fig. 5B the bracket fans from CMECs, so CMECs is the reference there.
- **`maturation_strategy` is left *not stated*.** The paper's maturation intervention is the cell combination
  itself (it applies no training, load or medium regime), and the combination is already carried by
  `cell_types`, `stromal_cell`, `endothelial_cell` and `composition`. Writing "co-culture" would have duplicated
  those fields, and the paper never uses the word. A vocabulary agent may want a term here.
- **Which fields set the groups apart.** The five microtissue groups differ in `cell_types`, `stromal_cell`,
  `endothelial_cell`, `composition` and `supplements` (VEGF for CMECs, FGF2 for CMFs, both for the three-cell
  groups), so all five sit in every group's context. The fibroblast identity is carried by `stromal_cell` alone;
  `cell_types` says "fibroblasts" for all three-cell groups so that CMECFs, CMEC ACFs and CMEC SFs do not differ
  in two fields for the same fact.
- **`donor_age` for the primary cells.** ACFs and SFs are adult primary cells, which the group's
  `stromal_cell` wording already says ("human adult cardiac fibroblasts"). I did not also write
  `donor_age: adult` for those groups, to avoid stating one fact in two fields; the ACM patient's age (37) is
  likewise only in the quoted clinical history, not in a context field.
- **Group kind.** The ACFs and SFs are primary human adult cells but the groups are engineered microtissues, so
  every group is `engineered`; no group is a native-tissue or other-study benchmark. The bulk RNA-seq comparison
  with Kuppusamy et al.'s fetal and adult heart samples (Fig. 3A) is a plot with no printed values, so it is not
  an item and no other-study group was needed.
- **Figure 3 and Figure 6A–6D.** The transcriptome panels (PCA, volcano, Spearman heatmaps, GO/KEGG dot plots,
  violin plots) and the proposed-mechanism schematic print no values and no tests, so they are not units. The
  numbers the text takes from them (ADCY5, GJA1, GUCY1A3, LDHA, LDHB, the DEG counts) are recorded as units
  ST2, ST4, ST5, S3E and F1.
- **Printed twice.** Three log2 fold changes are printed both in the Results text (1.78, 1.9, 2.37) and in the
  supplementary tables at machine precision; each is written twice under `_text` and `_table` names so code can
  check them against each other.
- **P for an omnibus item.** Where a legend gives a ladder of thresholds (`*P<0.01, **P<0.005, ***<P=0.0005,
  ****P<0.0001`) and I wrote an omnibus item, I put the first threshold of the ladder in `p`. This is the
  legend's convention, not a P for that item; the schema has no place for a threshold ladder.
- **Fig. 2G has no P in its legend**, although the panel is marked. I wrote the Methods' paper-wide threshold
  with its source (`*p < 0.05 (Methods)`), as the spec directs.
- **Suspected errors not corrected.** Fig. S4A's legend prints `*P>0.05` beside significance marks; Fig. 6's
  legend prints a stray `-n` in "sarcomere length in MTs from TEM (-n; n > 117". Both are labelled, not fixed.
  Fig. 6J's legend says "CMECFs generated from CTRL1 CMECFs", which reads circularly, and Fig. 6G calls the
  lentivirus-transduced SF tissues CTRL1 while Fig. S6F/S6G calls the same groups CTRL2; I recorded the main
  figure's line (CTRL1 for Fig. 6, CTRL2 for Fig. S6) and did not try to reconcile them.
- **`n` that is a bound.** Most n are printed as "n > 26", "N>9" and so on; they are written exactly as printed,
  so every check that needs an exact n will have to treat them as lower bounds.
- **No cross-reference error found.** I checked every "(Figure ...)" in the Results against the panel it names
  and found none pointing at a different experiment, so `cross_references` is empty.
- **Values left to the figures reader.** Every bar graph in this paper plots a mean with SEM and no individual
  points; the only printed numbers are in Fig. S5B (a table of metabolite release, recorded here), Fig. S3E (a
  table of DEG counts, recorded here) and the three fold changes in the text.

## Figures and data reader

- **F1 (Fig. 1C–F): no points.** Fig. 1C, the panel item F1C_qpcr rests on, is a raster heat map of qPCR values
  scaled per row; its colour bar is labelled only "row min" and "row max", so a colour gives no value in any
  unit, and the panel plots no individual replicates (legend n = 3). Marked `no_points` in `figures.yaml`; no
  script. The released data files (mmc3.xlsx, mmc5.csv, mmc6.xlsx) hold RNA-seq fold changes, not the Fig. 1C
  qPCR values, so no `data.yaml` rows were written for this unit.

- **F7D (Fig. 7D, PKP2 western blot densitometry): read, raster.** Fig. 7 is one embedded image (~300 dpi),
  so the tick labels are not text: `figures/f7d_pkp2.py` finds the tick marks in the raster and gives them
  their printed values in order. The y axis is broken (upper segment 1–5 for the EPI groups, lower 0.00–0.15
  for the CF groups); each segment has its own calibration. No released data hold these values.
  - CTRL-CFs: 2 squares (0.0821, 0.125); ACM-CFs: 3 squares (0.0815, 0.0622, 0.0731). Counts match the
    legend ("two and three independent differentiations") and the blot lanes. The right ACM-CF square sits on
    the end of the mean line but is drawn over it whole (red over black, full 13×13 px), so it was counted.
  - CTRL-EPI and ACM-EPI: the two circles of each group touch each other and the mean line is drawn across
    them, so per 02-audit no points were read (`countable: false`); line only: CTRL-EPI 4.29, ACM-EPI 1.85.
    The legend gives n = 2 for each (CTRL1 and CTRL2; two ACM differentiations), not checked against points.
  - The legend does not say what the horizontal line is. It is stored as the mean: for ACM-CFs the line
    (0.0723) equals the mean of the three squares (0.0723), not their median (0.0731).
  - The record's F7D unit context gives `printed: n > 10` / `counts: MTs per group` and a Chi-square test, which
    belong to the MT arrhythmia panel (Fig. 7I), not this monolayer western blot; flagged for the record reader.

### Fig. S7G (% SMA positive cells, CTRL- vs ACM-EPI)
- Read from mmc1.pdf p. 10 (one embedded ~300 dpi image) by `figures/s7g_sma_epi.py`; y ticks 0-5 found in the raster.
  No released data file holds these values (mmc3/mmc5/mmc6 are sequencing tables).
- CTRL: 3 standalone dots (2.056, 1.837, 0.326) = legend N=3; their mean (1.406) equals the line (1.406).
- ACM: both dots sit on the group line and merge with it into one blob, so ACM gives the line only (4.244,
  countable false, no points); legend N=2 is not checked against points. By eye both dots are at about the line.
- The legend does not say what the line is; it is stored as the mean (for CTRL it equals the mean of the dots).

### Fig. S7I (% SMA positive cells, CTRL- vs ACM-CFs)
- Read from mmc1.pdf p. 10 (one embedded ~300 dpi image) by `figures/s7i_sma_cf.py`; y ticks 0-15 found in the raster.
  No released data file holds these values (mmc3/mmc5/mmc6 are sequencing tables).
- CTRL: 2 standalone dots (4.494, 2.275) = legend N=2; their mean (3.385) agrees with the line (3.391).
- ACM: 2 standalone dots (12.12, 9.253) = legend N=2; their mean (10.69) agrees with the line (10.68).
- The legend does not say what the line is; it is stored as the mean (with two points mean and median coincide).
- The audit still gives S7I_sma `cannot check` after the readings (N=2 per group, no test printed for this panel).

## Vocabulary agent

- **"ATP production" was matched by code to the wrong measure.** Fig. 5B's "ATP production" is the Seahorse
  oligomycin-sensitive OCR (`measure:atp_linked_respiration`), but code matches the label of `measure:atp_production`
  (ATP amounts calculated from substrate use). A stored mapping cannot override a code match, so the items F5B_atp_*
  currently land on the wrong term. The re-map checkpoint should resolve it (e.g. a scope note or a rename by a person).
- **Fibroblast origin as a qualifier.** hiPSC-derived CFs and primary adult CFs both map to CL:0002548; CL has no
  distinction, so the new qualifier `origin` (hiPSC-derived / primary adult) on CL:0002548, CL:0002620 and CL:0010008
  keeps CMECFs vs CMEC ACFs a contrast in `stromal_cell`. The bare "cardiac fibroblasts" (group cf) has no origin.
- **Arrhythmogenic cardiomyopathy.** MONDO has no umbrella ACM class, only ARVC (MONDO:0016587) and its numbered forms
  (PKP2: MONDO:0012180). Mapped to the broader MONDO:0004994 *cardiomyopathy* with `no_ontology_term`; choosing the PKP2
  form would have read `disease_model` from `genotype`.
- **dbcAMP.** ChEBI has both CHEBI:50095 *bucladesine* and CHEBI:197402 *dibutyryl-cAMP*; I adopted bucladesine (the
  established entry). Worth checking at the next ontology review.
- **Epicardial cells → CL:0011019 *mesothelial cell of epicardium*.** CL has no class named "epicardial cell".
- **LUMC0153iPKP → CVCL_ZA18.** The paper prints no clone number; Cellosaurus lists clone 03 (CVCL_ZA18) and its
  gene-corrected derivative. CTRL1/2/3 are mapped to their Cellosaurus ids without adding "CTRL1" etc. as synonyms,
  since other papers use those names for other lines.
- **`cm_medium: Fibroblast Growth Medium 3`** (units F1, S6K) is a fibroblast medium for units whose cells are not
  cardiomyocytes. I added it as a `cm_medium` term with a scope note saying so. The field's scope ("base medium for
  cardiomyocytes") has no place for a stromal-cell medium; a person may want a field for it.
- **Flags.** `supplements: Pluricyte medium` (F6E) is flagged *two fields in one*: it is a base medium, and the
  unit's `cm_medium` says BPEL medium, which disagrees with the Methods ("cultured for 72 hr either in Pluricyte
  medium (NCardia) (CTRL) or in medium containing 0.5 mM dbcAMP"). `measure: relative mRNA expression of
  fibroblast and epicardial genes` (F1C) is flagged *several measures* (eight genes in one item).
- **Split requests.** "MTs" in `pacing: paced MTs` and "in MTs" in `cell_types: CFs in MTs / CMs in MTs` → platform;
  "ACM" in `cell_line: ACM hiPSC line LUMC0153iPKP` → disease_model. None of them contradicts the other field.
- **`pacing: paced at 1, 2 or 3 Hz`** names three frequencies, but every F7I group also carries its own `frequency`
  qualifier, so I mapped it to *electrical pacing* with no frequency rather than flagging *several conditions*. A
  shorter value ("paced") would be cleaner.
- **Values I think the record reader recorded wrongly (not fixed).** S6K (CF monolayer qPCR) has `preparation: lysed
  MTs`, but the cells are CFs in 2D, not microtissues. "scramble shRNA" is a GFP-expressing virus (pLV-CMV-GFP) by the
  Methods, which the paper calls the scramble control; I mapped it to the new *non-targeting shRNA control*.
  F4B uses "1 Hz" for a patch-clamp stimulation (current clamp), but identical text is mapped once, so it shares
  *electrical pacing* with the 1 Hz field-paced MTs.
- **Generic wordings kept off the synonyms:** "contraction amplitude" (an image-motion amplitude here, a force elsewhere)
  and "time to peak" (Ca2+ transient here). "log2 fold change" is mapped as `expressed_as: fold`; the fixed list has no
  log2 value, so the log transform is only in the values' unit.
- **Guesses.** "normalized relaxation time" (S4I) has no stated normaliser, so `normalised_to` is left out.
  "basal oxygen consumption" and "basal glycolysis" stay on the parent OCR/ECAR terms, following the existing scope note.
  `measure:construct_cost` (dimension currency) holds the paper's cost per MT; it is not a biological measure.

## Formula agent

- **Almost nothing can be rebuilt.** The only printed inputs are the S5B metabolite values (outputs whose inputs are not
  printed), F7F's CTRL at 1.00, and counts. There is no data.yaml, and the readings (F7D, S7G, S7I) are of normalised
  values or percentages, not their parts. So 73 of 74 derivations are *cannot check*; their use is the symbolic library
  check and the completeness list. Only `F7F_cx43.norm_ctrl_cmecf` rebuilds (1.00, consistent).
- **CTRL normalised to itself written as `y = m_ctrl/m_ctrl`** against `normalized_to_own_control`. That is the
  "of means" form; the paper may have normalised each CTRL batch to the CTRL mean, which gives the same mean (1) but a
  non-zero SEM. The spec has no cleaner way to state "the control divided by its own mean".
- **Bounds cannot target readings.** S7G/S7I (% SMA+ cells), F4B, F7I and the alignment index are fractions of a whole,
  where `fraction_bounds` would apply, but `bounds:` takes only a record value path and these have no printed values.
- **DCt method mapped to `ddct_relative_expression`** with `ddct` := ΔCt (no calibrator is named). The equation is the
  same (2^-x); S6K normalises to two reference genes (HARP and RPL37A), and how they are combined is not stated.
  Amplification efficiencies: not stated.
- **Normalised contraction duration (Fig. 4G) is Bazett's correction** (`ncd = cd/sqrt(ibi)`); proposed
  `bazett_rate_correction` (definition, dimension time^(1/2), i.e. with durations in seconds as in Bazett's convention).
  It also covers corrected field-potential duration in MEA papers. The unit of IBI inside the square root is not stated.
- **Not proposed: ellipsoid volume** (S1G nuclear volume "calculated from the semi-axis distance"). The formula is only
  implied, and given entries are already above the field's fifteen; marked `no_formula`.
- **Caffeine response (S4G):** the methods give a ratio (first peak / mean of four), the legend a "percentage, relative to
  amplitude at baseline"; whether the plotted value is ratio ×100 or the increase over baseline is a labelled alternative.
- **Seahorse parameters (F5B/F5C):** only the normalisation to DNA is stated. ATP production, spare capacity, proton
  leak and glycolytic reserve (= capacity − basal glycolysis) are differences of injection phases the paper never
  states; with readings of F5C, glycolytic reserve vs capacity − basal would be a checkable chain.
- **Not derivations here:** TXT_* log2 fold changes are rounded copies of the Table S2–S5 values (same quantity, not
  a formula); edgeR log2FC, MUSCLEMOTION/vector-flow velocities and Vmax are software outputs with no closed form.
- **S1C percentages and S4I "Norm. Relaxation"** state no numerator, denominator or normaliser: `no_formula`.
- No derivation in this paper looks wrong to me.
