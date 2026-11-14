## Record reader

- **Set value anchored across two sentences.** `differentiation_factors: CHIR99021 + IWP2`: the two molecules are stated 31 words apart (Methods 2.5/2.6), one word over the quote limit, so no single context anchor can hold both. I put the anchor on the value itself (CHIR99021 sentence) with a note quoting the IWP2 sentence. The schema has no way to anchor one set value with two quotes.
- **insulin_day left *not stated*.** The protocol switches from "RPMI/B27 without insulin" to "RPMI/B27" on day 7, but the paper never says that insulin is added. Reading day 7 as the insulin day would rely on what B27 contains, so I did not.
- **Fura-2 loading vs measurement bath (Fig. 3).** Methods 2.14 gives "incubated in Fura-2AM in 37 °C warm Tyrode's (1.8 mM CaCl2) for 30 min". That is the loading step; the recording bath is not stated. temperature, measurement_medium and measurement_calcium_mM are *not stated* for F3AB/TXT4/F3DE, and the loading is recorded under other_conditions. For the MEA (S4), "perfused with Tyrode's solution at 37 °C" is used. The composition of that Tyrode's is not restated, so its calcium is *not stated*.
- **Fields that vary between units, written per unit.** Because the hiPSC group (Fig. 2D) is undifferentiated and two kinds of platform exist (2D vs microisland; macrotissue/microsphere in Fig. 6), the differentiation fields, platform, substrate, seeding density, dissociation reagent and cm_day_at_formation sit in every unit's context (or group), not in the default. For the hiPSC group, platform, substrate and seeding are *not stated*: the paper does not say whether its hiPSC RNA came from encapsulated cells or from colonies on Matrigel.
- **cell_line where the text is silent.** IMR90-1 is used where the text, a legend or Table S1 ties the experiment to it (Fig. 2–5, S3–S6). For Fig. S2A (frequency over time), Fig. 6 and Fig. S7, no line is given, so cell_line is *not stated*. Table S1 says only that the 19-9-11 line had "video analysis".
- **dissociation_reagent** holds the hiPSC dissociation before encapsulation or seeding (Versene/Accutase). The later dissociation of tissues for replating (trypsin, collagenase) is under other_conditions. The field's scope covers both steps and allows one set.
- **"day 0 … day 5" (Fig. S1B).** The fourth x-axis label reads "Day 1", but the legend and text say day 5. I recorded this as a suspected error and named the groups by the legend's days.
- **Seeding density stated three ways.** Methods: 55 ± 8.5 × 10^6 hiPSCs/ml. Results: 55 ± 8.5 × 10^4 hiPSCs per tissue (10 µl per tissue, so consistent). Fig. S7 calls the "original" density 60 million/ml. The Methods value is used in BASE and S7's own values in S7; I did not flag a suspected error, because 60 is within the stated SD.
- **Pre/post drug designs (F3DE, F3F, S4B).** These are sequential in the same samples. I wrote treatment as the only differing field and left time_point *not applicable*, rather than also giving each condition a time, which would make every pair a confound. The washout group differs from baseline only by history, recorded as other_conditions "after washout".
- **Asterisk and hash thresholds.** Fig. 2 legend: "ANOVA P < 0.05, ** vs. 2D" and "# vs hiPSCs and day 0". I wrote p "P < 0.05". For "# vs hiPSCs and day 0", I wrote two pairs per marked bar (vs hiPSC, vs the same system's day 0); the legend does not say which day 0. In the author manuscript, the Fig. 3F legend omits "P < 0.05"; the journal version prints it, and I used that.
- **Similarity statements without tests.** "were similar for 2D and 3D cultured CMs" (Fig. 3A–B) and "decreased in response to increased pacing frequency" have no printed test or n. I recorded one pair per frequency (3D vs 2D) and 1.5 vs 0.5 Hz per system, each with stated_direction. By eye, the 3D bars look longer at 0.5 and 1.0 Hz, but I did not use eye readings.
- **Coincidence worth a second look.** The representative 3D flow plot (Fig. 2A) has Q4 = 26.6, which is also the printed Ki67 percentage of 2D cTnT+ cells (26.6 ± 0.5%). I did not flag it as an error.
- **Capture rate.** Day 14 CMs had a maximum 1:1 capture of 1.5 Hz (calcium imaging, paced 0.5–2.0 Hz), while day 20 MEA responded up to 3 Hz. These are different days and methods, so I logged it here rather than flagging it.
- **Representative flow quadrants** (Fig. 2A, S3A–B) are recorded as single-sample percentages from figure text (anchor kind unit). Table S1's yes/no columns (differentiation after encapsulation) and "characterization" text are not recorded; only "longest time reported" is a value. Other studies' rows are other-study groups, with substrate and species as printed.
- **Units with no unit.** Circularity, the length-to-width ratio and the TEM H-zone/I-band ratios are dimensionless; I wrote unit "".
- **Qualitative image results** (Fig. 1, 4A, 4D–E, 5, S1A/C/D, S5, S6, S7, 6) are measurement items without values. Where the text states a direction over time or between groups, they are pairs with stated_direction. Claims resting only on them are judged *cannot judge* on support and replication.
- **Movies S1–S6** are not in the folder; the claims of uniform contraction and suspension tissues maintained for months rest partly on them.

## Figures and data reader (S1B)
- Fig. S1B (NIHMS755756-supplement-8.tif, raster) shows bars with upper error bars only for both lines at four days; no individual points, so nothing was read (`no_points: S1B`). The paper releases no data files (.xlsx/.csv) holding these values.
- Day 5 means and SDs are printed (Results 3.1 and the Fig. S1 legend: 20.1 ± 8.0 %, 25.5 ± 8.0 %); day 0, 1 and 3 values appear only as bars.
- The day 0 bars have zero height but error bars reaching about 8 %, although growth is normalised to day 0; the fourth x-axis label reads 'Day 1' (already flagged in the record as day 5).

## Vocabulary agent

- **19-9-11 → CVCL_K054 (iPS-DF19-9-11T.H).** The paper names only "19-9-11" from WiCell; Cellosaurus has no exact
  "19-9-11" synonym. Mapped by synonym to the WiCell DF19-9-11T.H line already in the vocabulary; reasonably sure, not certain.
- **IMR90-1 → CVCL_C434** (IPS(IMR90)-1), adopted separately from the older own term `cell_line:imr90_ipsc`
  (clone not stated). The two now coexist; a person may want to say whether the own term should point to this id.
- **Platform formats.** Added `hydrogel_microisland`, `hydrogel_macrotissue`, `hydrogel_microsphere` directly under
  `engineered_3d` (no shared "cell-laden hydrogel" parent); near `cast_patch` and `cell_aggregate`, separated by scope notes.
- **PEG-fibrinogen** placed under `hydrogel`, not under `fibrin_hydrogel`; PEGylated fibrin (Geuss row) under `fibrin_hydrogel`.
  A judgement on whether PEG-fibrinogen "is" fibrin.
- **Table S1 is an image** (supplement-15.tif): no synonym can be anchored for "murine", "PEGylated fibrin hydrogels"
  etc., so these are per-paper mappings. "microcapsules" in two substrate values sent as split requests to `platform`.
- **Calcium transient duration "time to baseline 50/80%"** mapped to `calcium_transient_duration` with `level`; it could
  instead be a decay time (IonOptix time-to-baseline). "Spontaneous" left to the pacing context.
- **Gene expression** mapped with `normalised_to: GAPDH`, `expressed_as: normalised` (2^-ΔCt, Methods); if the figures plot
  fold vs hiPSC or day 0, the values should carry their own.
- **"normalized frequency of contraction"** (F3F): normalised to what is not stated; `expressed_as: normalised` only.
- **Flags (several measures, 6):** the two flow-cytometry quadrant items (four fractions each), "sarcomere alignment and
  nuclear size", "morphology and Caveolin 3 staining", "CM phenotype in tissue outgrowth" (sarcomeres + Cx43),
  "macrotissue dimensions" (thickness, width, length).
- **Record issues (not fixed):** F6_macro_onset holds both contraction onset (day 7) and uniform contraction (day 12) under
  one measure; S7 seeding density 60 million/ml vs Methods 55 ± 8.5 × 10^6/ml (already noted by the reader).
- "uniformity of contraction"/"uniform contraction" mapped to `beating_synchrony` (number of contracting areas and
  synchronicity); "microsphere diameter" to `tissue_width`; "cell number (darkening)" to `cell_number` with a new `proxy` qualifier.

## Formula agent

- **Nothing can be rebuilt.** 29 derivations (27 with a library formula, 2 without), all `cannot check`: no per-sample
  areas, counts, Ct values or readings exist (figures.yaml has no figure scripts; every bar chart is `no_points`). Readings
  of Fig. 3E (pre/post isoproterenol rate) would let code rebuild the printed 1.2-fold.
- **Tissue growth (S1B):** "normalized day 0 tissue surface area" beside a printed "expanded ... 20.1 %": written as the
  relative change (A5 − A0)/A0, with "ratio to day 0, minus 1" as an alternative (same number either way).
- **2^-ΔCt:** mapped to `ddct_relative_expression`, with its ΔΔCt variable taking ΔCt (no calibrator). There is no separate
  ΔCt entry; the form and the two efficiency assumptions are the same, so I did not propose one. Both assumptions are not stated.
- **Contraction frequency:** "number of contractions per minute" printed in Hz → `ratio_def` (count / time). The recording
  duration is not stated, so `t` is not stated (not a printed 1 min).
- **Fig. 3F "normalized frequency":** the reference is not stated (axis label only) → `no_formula`.
- **P4HB 5.24 %:** the text says "Of the remaining 3D-dhECT cells" (non-CM denominator); the Fig. S3 legend puts it beside
  72.5 % CMs as if of all cells. Written as labelled alternatives. Ki67 2.96 % is "of the remaining" too.
- **Circularity:** named, not written out ("ImageJ standard analysis plugins"); mapped to `circularity_def`. Its A input
  points at item F4B_area, which code reports holds 6 values for group cm (range and mean, text and legend): there is no
  per-sample input to point at. No bound entry covers circularity ≤ 1 (isoperimetric); `fraction_bounds` not used for it
  because circularity is not a part of a whole.
- **Bounds:** `fraction_bounds` on all flow percentages and quadrants and on the H-zone to sarcomere ratio (at most one
  H-zone per sarcomere): 22 values, all consistent. The I-band to Z-line ratio is not bounded by 1 (two I-bands border a Z-line).
- **Observations for code (not verdicts):** the representative quadrants sum to 100.06 % (Fig. 2A), 99.93 % and 99.98 %
  (Fig. S3), within rounding; no library entry checks a partition summing to 100 % without a printed total. The quadrant
  labels are not identified, so the representative plot cannot be tied to the 8.4 % Ki67-among-cTnT+ value.
  H-zone 0.257 × 101 = 25.96 and I-band 0.669 × 142 = 95.0 are both close to whole counts (26, 95); the counts are not printed.
