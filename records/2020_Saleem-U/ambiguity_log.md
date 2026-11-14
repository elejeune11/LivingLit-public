## Record reader

- **Minus signs cannot be quoted.** In both extractors the printed minus of "−17%", "−85%" comes through as a control glyph that normalization drops, so a quote containing "−17%" is never found. I kept the printed minus in every `values.printed` string and anchored those items on a neighbouring sentence without a minus (e.g. the BDM items are anchored on "The reason for the BDM-induced reduction of CaT is not clear…"). Where the anchor sentence had to carry the number, I used the part of the sentence with the "+" values.

- **Multiplication signs likewise.** "7 × 10⁴" extracts as "7 3 104", so the MOI sentence cannot be quoted. The MOI items are anchored on the following clause, and the MOIs are written in the group context as "7x10^4" / "7x10^5" (a qualifier, not an anchored quote).

- **Force and CaT are two measures, not two groups.** Figures 1C/1D and S1A/S1B put "Force" and "CaT" side by side and the paired t-test compares a force parameter with a CaT parameter of the same tissues. Groups are experimental conditions, and `measure` is not a context field, so I gave these units one group and recorded the stated relations ("28% longer", "20% shorter") as their own items with measures such as "time-to-peak CaT relative to time-to-peak force". The schema has no way to say that one item compares two measures within a group.

- **Groups that differ only in repeat number.** In Figure S2F/S2G the three groups are measurement 1, 2 and 3, three hours apart. No context field in `field.yaml` carries "time of repeat", so those groups have empty contexts; code will find nothing varying between them.

- **The "10% decline" of CaT over three measurements** is stated for the series, not for a pair. `between` takes exactly two groups, so I attached it to [m3, m1]; the paper does not say which pair it means.

- **Transduction as `treatment`.** The vocabulary has no field for a viral vector, sensor or MOI, yet transduction (GCaMP5G, GCaMP6f, GFP, none, two MOIs) is what several units and groups vary. I wrote it into `treatment`, combined with the drug where both apply ("GCaMP6f transduction + isoprenaline"). The vocabulary agent may want to flag this as two fields in one.

- **Paper-wide values repeated per unit.** `platform` is "engineered heart tissue (EHT)" everywhere except Figure 2C (hollow PDMS posts), so by the rule it cannot sit in `default_context` and is repeated in all twenty units; the same for `pacing`, `media_calcium_mM`, `treatment` and `number_of_lines`. Identical things are written with identical wording.

- **"submaximal Ca²⁺" is not a number.** Figures 3, 4, 5, S3, S4 and S5 state the measurement calcium per cell line in one sentence. I wrote `media_calcium_mM: {value: "submaximal", qualifiers: {concentration: "<the sentence as printed>"}}` rather than pick one number.

- **Significance that lives only in a figure or a colour.** The concentration-response panels (S3, S4) mark significance with asterisks and Table S1 with green cell colour; neither is text. I recorded `p: "*p<0.05"` only where the Results state significance in words, and `"not stated"` otherwise, so some printed asterisks are not in the record. Table S1's items carry `test: "not stated"`, `p: "not stated"`.

- **Which concentrations get items.** The Results give the maximum effect per compound, usually at one concentration; the other concentrations are plotted only. I made one item per parameter at the stated concentration (values carry `x`), left the remaining concentrations as groups without items for the figures reader, and added one frequency item per compound unit for the right-hand panels.

- **"% of baseline" and "% change".** The plots are "Relative force [%]" (% of baseline); the text gives changes ("+96%", "−85%"). I used `unit: "% change"` for the text values, `"% longer"`/`"% shorter"`/`"% higher"` where the sentence words it that way, and left the plotted "% of baseline" axes to the figures reader.

- **Figure 1A/1B and the videos.** The 2D monolayer images (Figures 1A, 1B and Videos S1–S4) report no measurement, so they are not a unit; the videos are listed in `source.missing`.

- **What the figures-and-data reader still owes.** Every figure in this paper is raster, and almost all of the numbers are plotted only: Figures 1C–1F, 2A–2D, 3A–3E, 4A–4E, 5A–5D, S1–S5. Table S1 is a unit of its own (`T1`) and its values are extractable text, so they are recorded here.

- **Things that look wrong, recorded but not corrected:** the three different n for the reproducibility experiment (text N = 16 and N = 15, legend n = 14; 1; 1); Table S1's Bay K-8644 CaT entry (+2.4 at 300 nM) presented as the maximum change while the text reports +53% and +62% at lower concentrations; "RT80%,CaT" used in the isoprenaline sentence where the paper otherwise writes DT80%,CaT; "EMD-5733" in Figures S3E/S4E versus "EMD-57033" in the text and Table S1; and the same cited source credited with "to 25%" in the Results and "by 50%" in the Discussion (noted on the attributed claim). Table S1 also prints two entries at a precision the rest of the table does not use (−2.33, −50.16).

- **No code problem found.** The gate reported only problems in my record (one quote broken by a page break, which I re-quoted from the part after the break); nothing looked like a bug in `livinglit/`.

## Figures and data reader

- **Released data:** none. mmc6.pdf is a combined copy of the article and supplement (not tabular); no data.yaml.
- **All figures are embedded raster images** (main.pdf at 300 dpi, mmc1.pdf at ~220 dpi, rendered at 300 dpi). Tick labels are inside the images: each script locates the tick marks by pixel (short dark strokes left of the y-axis) and states the printed values it assigns, top to bottom. Shared parts used: `calibrate`, intervals; paper helpers in `figures/_util.py` (ink masks, mean-line finder, SEM-bar top).
- **Panels read (77 entries, 307 readings, bar means; SEM upper ends where the bar shows above the mean line):** Fig. S1A/B TTP and RT/DT (force blue, CaT red), S1D/S1E force and CaT; Fig. 2C and 2D right halves (force, fluorescence); Fig. S2F/S2G; Fig. S3A–E and S4A–E (force/CaT, TTP, RT/DT, frequency; concentration as x, BL = 0); Fig. 4A/4B (frequency, force/CaT, TTP, RT/DT; x = Hz); Fig. S5 frequency and force; Fig. 5A/5B rows 2–4 (baseline black and OM blue/red lines; one entry per item's frequency pair).
- **No points counted anywhere:** every scatter has overlapping dots or dots under the mean line, so all groups are `countable: false` (no n check, no P check from points).
- **Not read:** Fig. 1C–F, 2A/2B, 3, 4C–E, 5C/D (average traces and force–calcium loops; no means with error bars, markers overlap); Fig. 2C/2D TMC (left) halves (several lines per panel but the unit has one `tmc` group, so lines cannot be assigned without inferring); Fig. 5A/5B frequency rows (black dots fuse into horizontal runs indistinguishable from the black baseline mean lines); S4C DT80% at 100 and 300 nM (mean lines lie above the axis break, only one tick there); S3/S4 TTP/RT panels without an evidence item; S1A/B amplitude and frequency, S1D/E TTP/RT/DT (no items).
- **Mismatches found:** F1E_force: Fig. S1D mean lines read 0.077 mN (MOI 7x10^4) and 0.097 mN (7x10^5), printed 0.086 and 0.088 mN (audit: inconsistent). F1E_cat low MOI read 4,948 vs printed 5,192. F3C_dt_cat: text gives +74% at 300 nM, but the 300 nM mean line is drawn above the axis break (not readable). The S3E frequency panel shows four mean lines but only three x labels (BL, 3, 10); lines assigned by position to BL, 1, 3, 10 µM.
- **Units:** axes print "Relative ... [%]" (unit_of_value "%"), "Frequency [bpm]", "[s]", "[mN]", and "CaT [Fluorescence]" (unit_of_value "Fluorescence"; the text gives the same values in AU). F3A_rt_cat ("RT80%,CaT" in the text) is read from the S4A panel labelled DT80%.
- **Fig. 2C braces (force):** the mean line touches the x-axis and a marker; its centre (about 1%) is approximate.
- **Fig. S4 legend** says means only, but SEM-like bars are drawn on several groups; their tops are recorded as `error` as drawn.
- **Ratio items** (F1C/F1D_ttp_ratio, _dt_ratio) rest on the TTP and RT/DT readings of the same panels; no entry maps to them directly because force and CaT share one group.

## Vocabulary agent

- **Transduction in `treatment`.** I kept the reader's choice: one own term `treatment:viral_transduction` with qualifiers transgene, vector and MOI, combined as a set with the drug ("GCaMP6f transduction + isoprenaline" → {viral transduction, isoprenaline}). Not flagged *two fields in one*: no other field holds gene transfer and nothing contradicts. A future `reporter`/`transgene` field may suit it better (genotype's scope is gene variants for isogenic contrasts).
- **"EHT" on `platform`.** Mapped "engineered heart tissue (EHT)" to *tissue between two pillars* (the paper casts fibrin strips between pairs of PDMS posts) without adding "EHT" as a synonym, which would be broader than the term. The hollow-post variant carries a new `posts` qualifier.
- **Flags:** `media_calcium_mM` "submaximal" and "0.4–0.6 mM for hiPSC cell line 2, and 0.8 mM for hiPSC cell line 3" (*several conditions*: calcium differs by line; code would otherwise read the second as 0.4 mM); treatment "GCaMP5G or GCaMP6f transduction" (*alternatives*); three measures naming two or four measures (*several measures*).
- **"AAV6- and LV-GCaMP6f transduction"** pools two vectors in one unit; mapped with vector "AAV6 and LV (pooled)" rather than flagged, since the paper analyses them as one group. The orchestrator may prefer *several conditions*.
- **"spontaneous beating"** (F3B_stopped): the finding is that tissues stopped beating under electrical pacing; "spontaneous" looks wrong. Mapped to *presence of beating* without a mode.
- **Kinetic levels.** "TTP80%", "DT80%" and "RT80%" all map with `level: 80%`; I added a `level` qualifier to calcium transient rise and decay times. The existing standing keys of those two measures (written by 2018_Ronaldson-Bouchard) do not require `measure.level`; the re-map checkpoint should add it. "RT80%,CaT" is mapped to calcium transient decay time (same quantity as DT80%,CaT, per the figure panel).
- **"time to peak" vs "rise time".** TTP80%,CaT is mapped to *calcium transient rise time*; force got its own *time to peak force*, because no force-rise measure existed.
- **Ids not found:** EMD-57033 (own term), GFP/GCaMP and transduction (not chemicals), metal braces (mechanical). BDM is ChEBI's *diacetylmonoxime*.
- **Units, not measures.** "% change", "% of baseline", "% longer/shorter/higher" are units of the values; the measure terms carry no normalisation for them.

## Formula agent

- **Force from post deflection.** The methods name the inputs ("EHT shortening and the elastic propensity and geometry of the PDMS posts") but no formula, stiffness, modulus or post dimension; the method is by citation (Hansen 2010 et al.). Mapped to the proposed model `hooke_spring` with `formula: not stated`; both assumptions (linear spring, small deflection) are not stated. Whether the EHT shortening is one post's deflection or shared between two flexible posts (a factor 2) is not said: written as labelled alternatives. Only the three items printed in mN get a force derivation; the relative-force items rest on the same unstated step.
- **"% of baseline" vs "% change".** Written as two steps per item: `pct_baseline` (ratio_def, per EHT, inputs not printed) and the printed % change (relative_change) rebuilt from the read bar means of treated and baseline. The paper normalises per EHT ("own baseline") but tests on data "normalized to the average baseline"; the read baseline bars sit near, not at, 100 %, so rebuilt changes carry reading error at the printed precision.
- **Unsigned decreases.** "20% shorter", "decreased by 21%", "10% decline", "declined by 10%–30%" are printed without sign; written with the proposed `relative_decrease` (derived from ratio_def) rather than relative_change.
- **Table S1 "maximum relative change".** The concentration per compound is not stated; the concentration of the matching Results sentence is used. Table S1 Bay K-8644 CaT (+2.4) does not match the 300 nM reading (−2.9 %): another concentration may have been used. Several Table S1 parameters (Bay K/digoxin TTP, EMD RT, Bay K DT) have no read panel.
- **S2FG CaT "10% decline".** Which measurements are compared is not stated; m3 vs m1 gives 8.9 %, m2 vs m1 gives 9.5 % (alternative).
- **F4 kinetics range "10%–30%".** Spans four parameters; the smallest read decline (TTP80%,force, 8.4 %) sits below the printed 10 %.
- **Signal-to-noise ratio.** Whether "background signal intensity" is a mean or an SD of the background is not stated (alternatives).
- Spec gap: a range output (S2C 20%–40%, F4 10%–30%) has no single output path; the F4 endpoints were written as two derivations.

## Record reader (re-read v3)

- **Calcium is the measurement bath, not the medium.** Every stated calcium in this paper is the Tyrode's
  solution during the recording ("Measurements were done in modified Tyrode's solution at 1.8 mM Ca2+";
  "submaximal Ca2+"), so all of them moved from `culture_calcium_mM` to `measurement_calcium_mM`. The calcium of
  the EHT culture medium is never stated: `culture_calcium_mM: "not stated"` sits in `default_context`.
  The 0.6 / 1.8 mM groups of F1F are measurement-bath groups for the same reason.
- **Transduction moved to `transgene`.** Every "GCaMP5G / GCaMP6f / GFP transduction" left `treatment`
  ("GCaMP6f (lentiviral)", "GFP (lentiviral)", "none" for non-transduced EHTs and for S5), with the two MOIs of F1E
  as a `MOI` qualifier of the transgene instead of the treatment. `treatment` now holds only the drugs
  (isoprenaline, nifedipine, Bay K-8644, digoxin, EMD-57033, BDM, ivabradine, omecamtiv mecarbil), and the
  baseline group of each drug unit states `treatment: "none"`. Which vector carried GCaMP6f in the follow-up
  experiments is not stated per figure (Methods name AAV6 at MOI 1x10^6 and lentivirus at MOI 0.3), so those units
  say "GCaMP6f" without a vector; only F1E (AAV6) and F1F ("AAV6 and LV") are stated.
- **Metal braces are a mechanical load, not a treatment.** F2C's braces stiffen the flexible PDMS posts
  ("contraction-abrogating afterload enhancement"), so its four groups state `mechanical_load`
  ("flexible PDMS posts" / "stiffened PDMS posts (metal braces)") and their treatment is the unit's "none".
  Every other unit carries `mechanical_load: "flexible PDMS posts"` in its unit context — the paper's own words
  for the load (EHTs cast between two flexible posts, force computed from their deflection); it never writes
  "auxotonic" of its own tissues, so that word is not used. Because F2C's groups state the field, it cannot sit
  in `default_context` and is repeated per unit, like `platform`.
- **`donor_age` is not stated** anywhere (no line age, no native tissue): default context.
- **The "10 % decline" now carries `over`.** S2FG_cat's decline is stated for the series of three measurements,
  so it is `over: [m1, m2, m3]` instead of the pair [m3, m1] the first read picked.
- **P states.** Every legend in this paper prints its threshold ("*p<0.05"), so no item needed
  `significant, threshold not stated`. One asterisk was missing from the record: Fig. 2D marks the TMC force
  bar, which the text words as "force decreased by 21%" — `F2D_tmc_force` now carries `p: "*p < 0.05"`.
  Panels whose bars carry no asterisk (S2F force, F2C TMCs, Bay K-8644 CaT at 300 nM, OM at 2.5 Hz, every
  frequency row) keep `p: "not stated"`. No item has several different printed P, so no `p_values` were added:
  where an item rests on a main and a supplemental panel, both legends print the same "*p<0.05".
  Table S1 marks significance by green cell colour with no threshold and cell by cell, while each T1 item spans
  five compounds under one `stats` block; one P state cannot express that, so those items stay "not stated".
- **`asserts_direction`.** Added to every stated claim: `up` for the force-frequency claims (c_title,
  c_abstract_ffr, c_abstract_positive_ffr, c_finding4, c_unmasked), `down` for the two claims that CaT peaks
  before force (c_abstract_sequence, c_finding1, read as the shorter time-to-peak of the CaT) and for the
  photo-bleaching claim (c_repetitive), `none` for the rest. Left off c_finding5 and c_om_confirm (the reverse
  frequency dependency of OM): they assert *up* at low frequency and *no effect* at high frequency of the same
  three items, which one direction cannot say.
- **Repeat measurements are still groups without a context.** S2FG's three measurements, 3 h apart on one day,
  are levels of time, but no field carries a time within a day (`day_of_measurement` is a day, and it is in
  `default_context` as "day 20–70"), so the three groups still state nothing and code will find nothing varying.
- **Force and CaT in F1C/F1D stay two measures of one group**, as v3 asks: each parameter is its own measurement
  item, and the printed relation ("28% longer", "20% shorter") is kept as its own item with the paired t-test in
  its `stats`, for the formula agent to write as a derivation. No group was added for them.
- No native-tissue or other-study groups: this paper reports no benchmark data of its own, only literature in
  the Discussion.

## Vocabulary agent (re-map v3)

- **Mappings dropped.** The 2 `culture_calcium_mM` flags and the 17 `treatment` transduction mappings were for stated
  text the re-read removed (the calcium is now `measurement_calcium_mM`; sensor and braces moved to `transgene` and
  `mechanical_load`). The two calcium values are flagged again under `measurement_calcium_mM` (several conditions):
  "submaximal" (per-line concentrations in the qualifier) and "0.4–0.6 mM for hiPSC cell line 2, and 0.8 mM for
  hiPSC cell line 3", which code would otherwise read as one quantity. Both are real flags; none was removed as
  code-handled.
- **Superseded terms.** `treatment:viral_transduction` and `treatment:metal_braces` (from my first map) are no longer
  used by this record; `transgene` and `mechanical_load` now carry them. Agents cannot retire terms; a person may.
- **`transgene` tree.** Two roots (`calcium_indicator`, `fluorescent_reporter`), children GCaMP5G, GCaMP6f, GFP;
  vector and MOI are qualifiers. "GCaMP6f (AAV6 and lentiviral)" is mapped to one transgene with the pooled vectors
  in the qualifier (one sensor, two vectors analysed together); "GCaMP5G or GCaMP6f (lentiviral)" is flagged
  (alternatives).
- **`mechanical_load`.** "flexible PDMS posts" → `auxotonic` with a `posts` qualifier (not a synonym: it names the
  device, not the load); metal braces → new `isometric` (braces abrogate EHT movement). Whether braced posts are
  truly isometric or just much stiffer auxotonic is a judgement.
- **expressed_as is per measure text, but this paper prints one measure text in two forms.** "CaT amplitude",
  "force amplitude", "contraction force", "time-to-peak CaT (TTP80%,CaT)", "time-to-peak force (TTP80%,force)",
  "decay time of the CaT (DT80%,CaT)" and "relaxation time for force (RT80%,force)" have items in AU/mN/s and items
  in "% change" from own baseline. A paper-wide `expressed_as` would be wrong for one set, so none is given, and
  these items cannot meet keys that require `measure.expressed_as`. Texts used only as % change (Table S1 rows,
  RT80%,CaT) carry `expressed_as: % change, normalised_to: own baseline`; DT80% (Fig. 1C, s only) is `absolute`.
  Suggest code take `expressed_as` from an item's unit when the unit is one of the fixed values.
- **Keys revised.** `contraction_time_to_peak` value adds `measure.expressed_as`; `force_calcium_relation` value
  swaps `culture_calcium_mM` for `measurement_calcium_mM`; `fluorescence_peak_amplitude` value adds
  `measurement_calcium_mM`. Others of this paper needed no change (no level/normalisation, no rate); keys of shared
  measures were already revised by the previous paper. `mechanical_load` is in no force key yet; post stiffness
  changes force, so a later checkpoint may want it in `twitch_force`.
- F1F pacing qualifier "1.5 Hz for N = 17 and 2.0 Hz for N = 4" pools two frequencies inside a matched pacing value;
  not flaggable from the qualifier, noted for the record reader.

## Formula agent (v3 follow-up)

- **Force against CaT is a derivation.** The four F1C/F1D relations ("28% longer", "99% longer", "20% shorter",
  "16% longer") are written as relative differences of the CaT parameter against the force parameter of the same
  EHTs, with both measures as inputs. Inputs now come from the S1A/S1B readings (CaT red, force blue bars) instead
  of the printed means; the printed means are kept in the input notes. The note names the paired t-test
  (*p<0.05) the relation rests on. Code: all four consistent (F1C TTP consistent within reading, 28.7% from the
  read bars vs 28.4% from the printed means).
- **Aggregation.** Every derivation judged against a printed value with per-sample inputs (83) now carries
  `aggregation: not stated`: no legend or method says whether % changes, ratios or forces are of group means or
  means of per-EHT values. Only "normalized to own baseline" is per EHT, and that step (`pct_baseline`) has no
  printed output. No scatter is countable, so code reports the mean-of-per-sample alternative as unavailable.
- **S2FG decline over three measurements.** The record now states `over: [m1, m2, m3]`; the derivation still
  needs one pair, kept as m3 vs m1 (8.9%) with m2 vs m1 (9.5%) as the alternative; Dunnett's post-test is vs
  measurement 1, so both pairs use m1. Spec gap: a value stated `over` a series has no formula form for
  "decline across the series" (max drop, last vs first, trend).
- **Transgene and measurement calcium.** No derivation referred to the transduction, the treatment field or the
  calcium field; groups (moi_low/moi_high, ca06/ca18, gcamp5g/gcamp6f, drug groups) are unchanged and every input
  path still resolves.
- The audit.yaml present before this run was stale (F1F_cat.higher showed "close"; with printed-digit intervals
  it is consistent); no verdict changed through this edit apart from the F1C TTP basis.

## Vocabulary agent (key checkpoint)

Re-map checkpoint after 10 papers (03-vocabulary, Earlier papers; 05-across-sources, Standing keys), after the independent check of release v5-rebuild-10. 6 standing_key edits revise the keys of the measures this paper first added.

- Value keys now require treatment, genotype and disease_model for every measure whose value a drug, variant or disease can change. Left unchanged: method, device, design and yield measures (analysis time, required sample size, micropattern yield, usable constructs, post spring constant, applied load, strip bending force, between-sample variability, identified protein count, PCA variance, medium composition, signal-to-noise, embryoid body diameter, cardiomyocyte yield, beating onset).
- Direction keys of force and beat-rate measures now require pacing (paced against spontaneous), so a spontaneous and a paced isoprenaline response do not meet.
- Guess: kinetic times (twitch duration, relaxation and calcium decay times) are also rate dependent, but their direction keys were not given pacing; the request named rate and force only.
- Concern for a person: genotype and disease_model are 'not stated' for most healthy lines, and an unstated must-match field blocks a value comparison. A dry run of the revised keys leaves 2 cross-paper value agree/differ verdicts of 104 (44 with treatment alone). The relaxation report will name genotype; whether an unstated genotype of a healthy line should count as wild type is a design decision.
