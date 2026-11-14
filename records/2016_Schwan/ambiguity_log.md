## Record reader

- **Decimal commas (ST1, S5b).** Supplementary Table 1 prints every fold change with a decimal comma ("1,407"), and the S5b image table mixes "2,2 ± 0.76". I kept them as printed, but `numbers.parse_number` strips commas as thousands separators, so "1,407" would be read as 1407. The schema has no way to declare a decimal separator. Checks on ST1 and S5 values need this fixed in code (or a per-value flag) before they can be trusted.
- **ST1 split into two units and kept apart from Fig. 6.** ST1 holds the individual points behind Fig. 6b. I split it into `ST1_NRVM` and `ST1_iPSC` (two separate experiments, like a mixed figure) and recorded the points as per-group measurement items. The tests stay in `F6_NRVM` and `F6_iPSC`. Because they sit in different units, a points-to-P check cannot link them. A schema link between a table unit and the figure unit it backs would help.
- **Multi-sentence set values.** The differentiation factors (CHIR99021 + IWP4) are stated in two sentences that no ≤30-word quote spans. I used `ContextObj.anchor` on the CHIR sentence and a `note` quoting the IWP4 sentence. Because of that, the value has no `context_anchors` entry and its words are not checked by `holds`.
- **Fiber orientation (Fig. 5).** No field fits longitudinal vs transverse scaffold fiber angle. I wrote it as a `substrate` qualifier (`fiber orientation`) so that code sees the groups differ. The other option was `other_conditions`, but code would then see no difference between the groups.
- **F4c two printed P.** The text gives "p < 0.01" for the length-stress gain increasing with culture time; the legend gives "ANOVA, Tukey post hoc, *p < 0.05" with one bracket (Day9–Day23). I read the text P as the omnibus and the legend's as the Tukey pair, which gives two items. It could also be one test printed twice.
- **F4f P.** Legend "*p < 0.01", text "p < 0.001". I recorded both on each pair, legend first and text in `p_values`. S3 prints asterisks with no test or threshold, so its pairs use the text's p < 0.001.
- **S2b force-frequency.** I made 18 groups (3 days × 6 frequencies), and the "negative force-frequency response" is an omnibus item with `stated_direction: down`. No test is printed, and the paper does not say per day. Stretch is "8%" in the legend and "10%" in the Methods; both are in `other_conditions`.
- **Stretch during measurement.** Measurement stretch (8% or 10%) has no field and went to `other_conditions`. The F4b means (0.20, 0.49) do not state their stretch level.
- **Context values left not stated.** I did not compute these from the protocol:
  - `preparation` for mechanics and OCT: no wording such as "intact".
  - `cm_day_at_formation`: dissociation at differentiation day 14, but no seeding day is stated.
  - `wnt_inhibition_days`: IWP4 from day 3 to day 5, so the duration would have to be computed.
  - `insulin_day`.
  - The hiPSC `cell_line`: the new line is unnamed.
- **hiPSC maturation media.** T3, IGF-1 and dexamethasone are listed under `supplements` (routine for every hiPSC group). `maturation_strategy` is left not stated so the same fact does not sit in two fields, even though the paper calls them maturation factors.
- **Day for "two days after seeding" (F6, ST1).** I used the paper's wording; `time_point` is "2 hours" (the length of the loading). For the iPSC-CM experiments the Methods' general timing applies, and it is not restated for them.
- **`treatment` outside the T3 and isoproterenol units** is "not applicable". In those two units the controls are "none".
- **Benchmark groups.**
  - Fig. 7c (Milani-Nejad trace) and Fig. 7d (Mulieri gray bars) are `other study` groups.
  - The comparisons with them are items with `stated_direction` only, because no other-study values are printed.
  - The Discussion's Morgan and Raman kinetics are in `TXT3`.
  - The other literature values (8–9 and 42 mN/mm2 trabeculae; 0.1–4 mN/mm2 range) are recorded only as attributed or literature claims.
- **Left out.**
  - Fig. 1e (representative trace; its legend says 37 °C, the Methods 35 °C, which is logged as a suspected error on the F4ac temperature).
  - Fig. 2 (protocol images).
  - Fig. 4a/d and S5a representative traces.
  - S4b fiber-alignment polar plot (an image-processing output).
  - The peak stress panel of S2a, which repeats Fig. 4b.
- **Suspected errors.**
  - F5: 6 days in the text vs 9 days in the legend.
  - S2: TTP and RT50 axes labelled ms, values in s.
  - S4: a paired t-test with n = 6 vs 7.
  - Dexamethasone printed as 1 mM.
  - The Discussion's T3 day-15 values (59 and 83 ms, "2 Hz") vs the Results (63 and 77 ms; pacing 0.5 Hz).
  - The abstract's "by day 21" (the data are at day 23), judged in claim C02.
  - The Discussion's "shearing stretch tended to decrease BNP" vs the Results' "no expression change" (C34).
- **Cross-reference.** The Discussion cites Supplementary Fig. 2 for a force-frequency relation "in our rat and human EHTs"; Supplementary Fig. 2 shows NRVM EHTs only.

## Figures and data reader

Unit F4ac (Fig. 4a–c), job 2026-11-13.
- **Read:** Fig. 4c (`fig4c_gain`, vector, p. 5). Day9 11 points (printed n = 11), Day23 12 (n = 12), Day16 9 (printed n = 8). All markers are separate vector paths with no duplicates. The Day16 plotted mean (0.765) equals the mean of all 9 read points, so the ninth square is plotted data and not a stray symbol. Not marked suspect; the audit reports the count mismatch.
- **Means check:** the means of the read points match the plotted mean lines (Day9 0.324 vs 0.320; Day23 2.011 vs 2.014).
- **Calibration:** the tick labels are outlined glyphs with no text layer. The three tick lines were matched by eye to the labels 0, 3.25 and 6.5; the glyph centres sit within 1 pt of the ticks.
- **Unit of value:** the axis title "Length-Tension Gain" has no unit, so the unit was taken from the legend ("increase in mN/mm2 per unit engineering strain").
- **Day16 link:** Day16 is linked to F4c_gain_omnibus/d16, because F4c_gain_d23_d9 does not involve d16.
- **Not read:** Fig. 4b (F4b_stress/d16) plots means with error bars at each stretch level and no individual EHT points. The text gives no Day16 value.
- **Data:** no released data files.

Unit F5 (Fig. 5), job 2026-11-13.
- **Read:** Fig. 5c (`fig5c_twitch`, vector, p. 7), three stacked subpanels (peak stress, TTP, RT50), each with its own y axis. Long. 6 points and Trans. 7 points in every subpanel (printed n = 6 and 7). Some markers are drawn as a fill path plus a separate stroke path; the script uses the fills only and removes duplicate centres. Two RT50 Trans. squares share one y value (306.6 pt) at different x positions. Both are real markers.
- **Means check:** in every subpanel the mean of the read points equals the plotted mean line within 0.0005 (e.g. stress 1.154 vs 1.153 and 0.432 vs 0.433 mN/mm2).
- **Calibration:** the tick labels are outlined glyphs with no text layer. Each axis's three tick lines were matched by eye to the printed labels: 0/1/2 mN/mm2, 0.09/0.12/0.15 s and 0.07/0.09/0.11 s.
- **For the record reader (not corrected):** the readings do not reproduce the printed percentages. Long/Trans. peak stress is 1.153/0.433 = 2.66, i.e. about 166% greater, but the Results say 240% greater. Trans. is 38% of Long., but the Discussion says ~30%. Trans. TTP is 0.1246/0.1138 = 1.095, about 9.5% longer, but the Results say 11%. The audit does not check these percentages yet.
- **Data:** no released data files.

## Vocabulary agent

- **Code gap, flagged:** `wnt_activation_days` 'twenty-four hours' cannot be read as a quantity, because `matching.NUMBER_WORDS` stops at "twelve". The spec says a quantity printed in words is a quantity, so this is a code limit and not a vocabulary one. A quantity field takes no terms, so it is flagged *not a context* and the reader is asked to write '24 hours'. Two more problems remain: the field counts days, and a 24 h exposure fits it poorly.
- **Static stretch and shear (new terms `mechanical_load:static_stretch`, `mechanical_load:static_shear`):** both are 10 % deformations imposed once and held for 2 h. They are two root terms rather than children of *isometric* or *cyclic stretch*, so that the paper's stretch-vs-shear contrast reads *differ*, not *narrower/broader*. A tissue held stretched also contracts isometrically, so placing them under *isometric* was a close alternative. The control 'original culture length' maps to *isometric*. 'stretch loading' got no synonym because the phrase also covers cyclic regimes.
- **Native tissue:** RV trabecula, LV muscle strips and thin rat trabeculae map to `platform:native_tissue` with `region` and a new qualifier `format`. I did not add trabecula as a term: a term under *native heart tissue* would sit beside *adult/fetal heart tissue*, which split by age, a second dimension.
- **Purity method:** 'cardiac troponin T staining of a test aliquot' does not say whether the cells were imaged or run through flow cytometry. It maps to a new root term, *marker staining, read-out not stated*, because neither existing term is broader than the other.
- **Levels:** 'time to 50% relaxation' maps to `relaxation_time`, level 'RT50' (the paper's abbreviation). I don't know how earlier papers spelled `level`. 'time to peak stress' became a synonym of *time to peak force* with no level: the paper defines it from the stimulus.
- **'maximum twitch stress'** maps to *twitch stress* with no synonym, because "maximum" may mean the highest value over stretch levels.
- **'pluripotency markers'** (OCT4, SSEA-4, NANOG, TRA-1-60, alkaline phosphatase) goes to a new term under *protein staining*. SSEA-4 and alkaline phosphatase are not proteins as stained, so a single `protein` qualifier did not fit.
- **CL has no induced pluripotent stem cell:** mapped to CL:0002248 *pluripotent stem cell*, with `no_ontology_term`.
- **Split requests:** NRVM / 'neonatal rat ventricular myocytes' → species (rat) and donor_age (neonatal). The TXT3 Morgan group has neither filled, and the TXT1 values agree. 'thin native rat trabeculae' → species (its group already says rat). 'RPMI/B27' → supplements (B27 is missing from those units' supplements).
- **Flag:** 'twitch kinetics (RT50, TTP)' (TXT3) is *several measures*. Each measure needs its own evidence item.
- **Possible reader issues (not fixed):** the matched treatment 'thyroid hormone T3' gives two ids, CHEBI:18258 (T3) and CHEBI:60311 (thyroid hormone), because the label 'thyroid hormone' matches too. The hiPSC units have T3 in `supplements` while the F4df groups have T3 as a `treatment`. Both are consistent with the paper, but a cross-field duplicate is something to check at re-map.

## Formula agent

- **Group ids across items:** F4b stress (groups d9/d23) points at the area item F3c_csa, whose groups are c9/c16/c23 for the same EHT ages. An `item` input takes "its value for this group", so code finds nothing. The spec gives no way to map a group onto another unit's group. F3c also prints only ~0.1 mm2 (day 16), so nothing would be rebuilt anyway.
- **'240% greater' (F5c):** mapped to relative_change, (long − trans)/trans, with 'X times' as a labelled alternative. Code finds 167% from the Fig. 5c reading means: inconsistent. The 2.4× reading would give 267%, which does not fit either. The Discussion's '~30%' (trans/long) gives 37% from the readings: also inconsistent. The two printed statements agree with each other (1/(1+2.4) = 29%) but not with the plotted means. The Fig. 5c tick labels were matched by eye (figures.yaml note), so a calibration slip in fig5c_twitch is possible. Observation for code, not a correction.
- **'11% longer' TTP:** code finds 9.6% from the readings: close.
- **Length-stress gain:** "slope of the stretch-peak stress relationship". The library has no regression-slope entry and the fitting method is not stated, so I gave no_formula and no proposal. The engineering strain step (6.6 mm on 6 mm = 10%) maps to relative_change. The printed '10%' is not a record value, so it has no output.
- **S5 baseline = Fig. 7d hiPSC EHTs:** the same 2.2 ± 0.76, RT50 168 and TTP 181, so I took F7d_force as the baseline force. That is a judgement; the paper does not say they are the same measurements.
- **Stretch level:** the Methods give the force-frequency relationship "at 10% stretch"; the Supplementary Fig. 2 legend says "at 8% stretch".
- **Diameter versus area:** "circular cross-section of approximately 250 μm in diameter" gives π·0.125² ≈ 0.049 mm2, against the Discussion's ~0.1 mm2 at day 16. The paper never derives one from the other, so this is not a derivation, only an observation.
- **ddCt:** "delta-delta CT method" (cited to Livak) is treated as a named operation and mapped to ddct_relative_expression. Ct values, calibrator and efficiencies are not stated.
