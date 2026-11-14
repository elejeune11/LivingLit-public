## Record reader

- **Two differentiation methods, none assigned to experiments.** Methods give a growth-factor (activin A + BMP4) and a small-molecule (CHIR99021 + Wnt-C59) protocol, with Percoll enrichment for growth-factor cultures under 70 % CMs, but never say which method produced the cells of which experiment. In F2–F7 I wrote `differentiation_factors` and `hipsc_medium` as stated alternatives ("… or …", which the vocabulary agent should flag as *alternatives*). I gave `wnt_activation_days`, `wnt_inhibition_days`, `insulin_day`, `confluency` and `purification` the one stated value, each with a note naming the method it belongs to. Treating these as *not stated* would also be defensible. In S1 the methods are separate groups.
- **`cm_day_at_formation` "day 16–20"** is printed only for the growth-factor harvest. Fig. 2A (image) shows "16/20" for both methods. I kept the value and added a note.
- **`maturation_strategy` left *not stated*.** The paper frames cell alignment as the maturation approach, but alignment comes only from the aligned scaffold (`platform` orientation qualifier). Writing "cell alignment" for the aligned group would alias two fields and turn aligned vs random into an aliased confound.
- **TCP vs scaffolds** differ in both `platform` (tissue culture polystyrene vs electrospun fibrous scaffold) and `substrate` (polystyrene vs PCL), so code will call those pairs confounds. That is real (material and format both change), but "tissue culture polystyrene" serves as the source of both values.
- **Empty `default_context`.** F1 (scaffold characterization, no cells) needs *not applicable* for every cell field, and the default may not be overridden. Every unit therefore carries its own full context.
- **Two replatings.** Cells sat on Matrigel-coated substrates for 2 weeks, then most assays replated them (96-well Matrigel plates, Matrigel coverslips, fibronectin MEA). `replating_coating` holds Matrigel, with the MEA surface as qualifier `measurement_surface: fibronectin`. `seeding_density` holds the substrate seeding density, with the second replating as qualifier `replating`. A field for "measurement surface" would help.
- **`day_of_measurement` "2 weeks"** is time on the substrates, not a differentiation day; the differentiation day is printed only in the Fig. 2A image ("16/20 +14"), so I did not compute it. Time after replating went to `time_point` ("48 h post-seeding", "3–7 days").
- **Fig. 6 doses** are printed only as figure labels and in Table S3, which is an image. Their context anchors are `kind: unit` quotes transcribed from Table S3. Baseline (0 dose) groups are `treatment: none`. The 5-min incubation is a unit `other_conditions`.
- **Heptanol concentration conflict:** Fig. 6D and its legend say 10 mM, while Table S3 says 10 µM. I recorded 10 mM with a `suspected_error`.
- **Fig. 6 significance dots** were read by eye from the figure (black dot vs white dot, one item per marked pair). There are 11 + 7 + 3 pairs. Random/carbamylcholine has no marks; it is recorded as a measurement item and opposes the "all substrates" carbamylcholine claims.
- **"Similar among three substrates (p > 0.05, two-way ANOVA post hoc Tukey)"** is one sentence covering every drug and dose. I wrote one omnibus item per drug × non-zero dose, over the three substrate groups at that dose (9 items), all from the same anchor. The schema has no way to say "the substrate factor of a two-way ANOVA across dose".
- **Fold ranges across genes** ("1.9–2.4 folds" over TNNT2, MYL7, MYH6, TTN; "1.8–2.8 fold" over five ion-channel genes) span several measures, not several groups. I wrote each as its own aligned-vs-TCP item with `between: [al, tcp]` lo/hi values. They are not attached to the per-gene items.
- **"up to 1.6–1.7 fold"** (and similar for phenylephrine and carbamylcholine) is attached `over` the highest-dose group of each substrate, because "up to" implies the maximal response. The paper does not name the dose.
- **Fig. 5 genes with no asterisk** (TNNI3, MYL2, MYH7, SLC8A1) are omnibus items with `p: not stated`. No P is printed; the absence of a mark is not an "n.s.". Unmarked pairs of starred genes are not recorded.
- **F7 peak amplitude "no statistically significant difference"** has `p: not stated`, because no P or "n.s." is printed.
- **Suspected errors:**
  - Beat-rate SE in the text (19 ± 10, 22 ± 14 bpm) is far larger than the Fig. 7D error bars.
  - The Fig. 7D peak-amplitude axis unit is "mV" for a ΔF/F0 fluorescence transient.
  - The Fig. 7 legend says "half rise to decay time", but the axis says "Half Rise to Peak Time".
  - For the small-molecule purity analysis, the Fig. S1 legend says day 18 but panel S1E says D20.
- **Cross-references:**
  - The text cites Fig. 4C for sarcomere length, which is Fig. 4D.
  - The supplement cites Fig. S1E for Percoll-enriched immunocytochemistry, which is Fig. S1D.
- **Citations that do not fit their sentence** (logged here because `Citation` has no `suspected_error`):
  - Bhagwati 2013 (a Chikungunya paper) is cited for hPSC culture.
  - Kuroda 2014 (RPE impurity detection) is cited for fiber-diameter analysis.
  - Ben-David 2013 (Claudin-6) is cited for O-rings.
  - Nori 2015 (spinal cord) is cited for GLOX buffer.
  - "(Chuva de Sousa Lopes et al.)" is inserted after "ultraviolet" in Methods 2.3, which looks like a reference-manager error; not recorded as a citation.
- **"c.a. 1.4 µm" and "c.a. 70 %"** are recorded as printed. The number parser does not treat "c.a." as an approximation word, so checks will judge them at full precision.
- **Image-printed values** (Fig. S1 quadrant labels 97.6 %, 70.4 %, 86.0 %) are in items anchored by their text sentence, with `_figure` value names and a note. A value can't carry its own `kind: unit` anchor.
- **Other-study groups in F4** (Li 1996 adult ventricular CM area; Bird 2003 sarcomere length) come from the Discussion. "At least 11 fold larger" and "about 1.5 fold" relate to hPSC-CMs in general, not to one group, so they are only notes.
- **Tables S1–S3** are methods tables (antibodies, primers, compounds) and not units. Only Table S3 feeds values: the context anchors for doses.
- **Qualitative units** (F2 alignment, F3 marker staining) have measurement items with no values. The claims resting on them are judged *cannot judge* on support.

## Vocabulary agent

- **Electrospun fibrous scaffold** is a new root platform term, not placed under 2D culture or engineered 3D. The abstract frames the mesh as "a 3D microenvironment", but the cells sit on a thin mesh. Fiber orientation (aligned/random) is a qualifier on it, so the aligned-vs-random contrast is a qualifier contrast. A later re-map could move it if a 2D/3D rule for scaffolds is settled.
- **TCP control**: platform 'tissue culture polystyrene' is mapped to the broader *2D culture* (the paper does not say monolayer for TCP), with a split request for 'polystyrene' → substrate. Substrate 'polystyrene' is mapped to *culture plate*. Bare 'polystyrene' is not a synonym because it is too broad.
- **Flags (alternatives)**: 'MEF-conditioned hPSC medium or Essential 8' (hipsc_medium) and 'activin A + BMP4 or CHIR99021 + Wnt-C59' (differentiation_factors, units F2–F7). The paper never says which protocol made the CMs of the main experiments, so the reader can't resolve the second one from the source either.
- **Flags (several measures)**: the two fold ranges over 4 and 5 genes (F5A_struct_fold, F5B_ion_fold).
- **Heptanol** is adopted as CHEBI:195607 'heptanol' (unspecified isomer), not heptan-1-ol, because the paper names no isomer. The record's suspected error (10 mM in Fig. 6 vs 10 µM in Table S3) stays with the record.
- **Calcium amplitude** gets `expressed_as: % change` from the record reader's note that Fig. 7C defines it as ΔF/F0 (an image I did not check). The Fig. 7D axis prints mV.
- **Gene expression** gets `normalised_to: GAPDH` (Methods 2.5: "normalized to the Ct value of housekeeping gene GAPDH"). The 2^−ΔΔCt calibrator group is not stated, so earlier papers that used normalised_to for the calibrator would not match.
- **'normalized beating rate'** (MEA) is mapped to contraction frequency with `expressed_as: fold` and no normalised_to. The reference (rate before the compound) is implied, not printed.
- **'cell alignment'** (qualitative, Fig. 2B) is mapped to *tissue anisotropy*, whose definition says "from histology". Here it comes from confocal images of cells on scaffolds.
- **'CM fraction after Percoll enrichment'** is given marker α-actinin from the supplement's Percoll section, with a split request for 'after Percoll enrichment' → purification (the group already holds it).
- **'sarcomeric organization level'**: a new child term *share of cells at sarcomeric organisation levels*, with `level: levels III and IV` (one item).
- **Possible record issue**: the F2 unit context holds 'activin A + BMP4 or CHIR99021 + Wnt-C59' and 'MEF-conditioned hPSC medium or Essential 8'. These are probably better as *not stated* for the main experiments, or the reader should check whether Methods 2.3 names the method used.

## Formula agent

- **No data or readings.** Every Fig. 4–7 panel is bars only (figures.yaml `no_points`) and no readings were taken. So the qPCR (2^-ΔΔCt), normalised beat rate and circularity derivations have per-sample inputs marked not stated, and code can check only the formula, not the numbers. Reading the Fig. 4B stacked bars (levels III and IV per substrate) would let code rebuild the printed 75 % and 63 %.
- **Normalised beating rate (Fig. 6A–C): denominator not stated.** The legend says "normalized beating rates". The methods record 30 s at baseline and 5 min after each dose, so the baseline rate is the likely denominator, but the paper does not say so. Inputs are left not_stated; aggregation is not stated.
- **qPCR calibrator not stated.** "Fold of change was then calculated as 2−ΔΔCt", with GAPDH as the reference; the calibrator group (TCP by the figure layout) is not written. Amplification efficiencies are not reported (both assumptions of ddct_relative_expression are not stated).
- **Ranges over several genes or groups as outputs.** F5A "1.9–2.4 folds", F5B "1.8–2.8 fold" and F6A/B/C "up to x–y fold" are each one printed range over several genes or substrates. A derivation's output is one value, so no output is named. The spec gives no way to tie a range to a set of derivations.
- **Discussion folds not recorded as values (for the record reader).** "at least 11 fold larger than hPSC-CMs" and "about 1.5 fold of the value in hPSC-CMs" appear only in item notes, so F4_li1996_area.fold_vs_hpsc and F4_bird2003_sl.fold_vs_hpsc have no output. Code rebuilds 12,000/1053 = 11.4 (so "≥ 11" holds; against the aligned 864 it would be 13.9) and 2.2/1.4 = 1.57 (interval 1.48–1.67 holds 1.5).
- **Circularity.** The paper states only "circularity: 0 = line, 1 = circle" and ImageJ. I mapped it to circularity_def (the ImageJ form factor), with the ISO square-root form as a labelled alternative. No bound is applied to circularity: fraction_bounds is for a part of a whole, and I did not propose a [0, 1] bound for shape factors.
- **Not derived:** F7 calcium transient frequency (bpm) and the rise and decay times are read by Clampfit from traces. The flow-cytometry percentages are measured shares, bounded by fraction_bounds only.

### Re-map at vocabulary v68 (2026-11-13)

- **'circularity'** is now matched by code: 2021_Knight added it as a synonym of *cell circularity*. I had left it out at v55 as too broad (it could mean a nucleus or a colony). The stored mapping is removed, because matches are never stored.
- **platform:biomaterial_scaffold** (2021_Tsui) now sits next to *electrospun fibrous scaffold*. The scope notes keep the two apart, so the TCP and scaffold mappings stand.
- No other mapping changed. The edits from the first map (v56) are already in the log, and the gate skips them.
