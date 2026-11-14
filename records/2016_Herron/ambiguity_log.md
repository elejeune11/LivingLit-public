## Record reader

- **Two versions of the paper.** The folder holds the journal PDF and the NIH author manuscript (`nihms772087.pdf`). The text and values are the same, but reference numbers shift by one after ref. 23. Both are listed in `source.files`. Anchors and citation labels follow the journal version, as noted in `source.version_note`.
- **Bracket reading in Fig. 2C/2D and Fig. 5D (raster).** No printed text says which pair each mark belongs to; I read the pairs from bracket positions. Fig. 2C: * = matrigel+PDMS vs fibronectin+glass and vs matrigel+glass, † = vs fibronectin+PDMS. Fig. 2D: ‡ = vs fibronectin+glass, § = vs fibronectin+PDMS and vs matrigel+glass. Fig. 5D: † = each of the three vs matrigel+PDMS, ‡ = fibronectin+PDMS vs fibronectin+glass and vs matrigel+glass, ns = matrigel+glass vs fibronectin+glass. The "ns" bracket over bars i–iii in Fig. 2C/2D is written as one omnibus item.
- **Fig. 7F ‡ "Significant difference from GLASS".** The legend does not name the glass group. I wrote it as PDMS 10 µmol/L vs glass 10 µmol/L, which is a guess. The glass groups come from Data Supplement Fig. VIIIC, so F7F is one unit that covers both panels.
- **Data Supplement Fig. IVC (E4031 effect, plastic vs PDMS)** compares the pre→post change between substrates. I recorded it as `test_of: interaction` over the four F4D groups and placed those items in unit F4D. The legend names no test.
- **Single marks without a bracket** (Data Supplement Fig. I C/D: ** and * over the matrigel bar; Fig. 8: marks over single groups, legend says "ANOVA") are recorded as omnibus items with the printed P, not as pairs.
- **Fig. 7A/7B asterisks.** The legend defines "*" only in its panel D sentence ("*Significant difference, t test, P<0.05"). I applied it to the asterisks in A and B.
- **Spread for supplement figures.** The legends of Data Supplement Figs. I, II and VIII and of Fig. 7F give no spread. I used the Data Supplement Statistics sentence "All data are presented as mean ± SEM" (`spread_source: methods`). Data Supplement Fig. VII states SD.
- **cm_day_at_formation for iCell.** The paper says the cells are "cryopreserved after 30 to 31 days of cardiac-directed differentiation" and later thawed and plated. The day of plating is not stated as such, so I wrote `not stated` and kept the sentence as an `other_condition`.
- **cm_medium for iCell.** Cells sit in EB20 (with 20% FBS and 10 µmol/L blebbistatin) for 24 h, then in RPMI + B27. The schema has one medium field, so I wrote `RPMI` with a note on EB20. A sequential-media structure would hold this better.
- **maturation_strategy left `not stated`.** The intervention is the substrate and coating, which already sit in `substrate` and `replating_coating`. Writing it again would copy one field's words into another.
- **Coating not stated** for Fig. 7A–E, Fig. 8 and Data Supplement Figs. VII/VIII. The text implies matrigel ("plating them on matrigel-coated PDMS coverslips"), but the experiments do not say it, so `replating_coating: not stated`. Fig. 8 also does not name the substrate.
- **Pre/post E4031 (F4D)** is the same monolayers before and after the drug. I encoded it only through `treatment` (none vs E4031), not also through `time_point`, to avoid an artificial aliased field. The legend says "Unpaired t test" for these paired recordings. Recorded as printed.
- **preparation wording.** For live monolayers I used the paper's word "monolayers", which also appears in `platform` ("monolayer"). There is no better printed wording for an intact preparation.
- **S3 V1/2 sentence.** It attaches −79.0 mV to PDMS+matrigel and −88.0 mV to the comparator, a right shift, while the text and figure say left-shifted. Recorded as printed with a `suspected_error`. The claim's direction is judged `cannot judge` with `asserts_direction: down`.
- **Cx43 Western (F5B).** The text says "≈3× greater when fibronectin+PDMS is compared with matrigel+PDMS", but the values make matrigel+PDMS higher. The ratio is recorded `between: [MP, FP]`.
- **Unit of replication in Fig. 3.** The legend gives N monolayers and n cells, and does not say which the t test used. I set replication to `cannot judge` on the AP claims.
- **n values printed inside bars** (Fig. 7F: 178, 207, 65) are image-only. They are written in `n.per_group` with a note; the schema has no anchor on `n`.
- **Not recorded:** the Fig. 6D human ventricle lane (qualitative positive control, no value; would be a native-tissue group with no item), representative traces and activation maps (Figs. 1A, 2B, 3A/F, 4A), flow gating (Data Supplement Fig. VI), and Data Supplement Fig. VB purification images (no values). Video I is not in the folder, but no item rests on it.
- **Cross-references.** Text "Figure 5B" for BJ purification (actually Data Supplement Fig. VB); Discussion "Figure 5" for IKr dependence (Fig. 4D); Fig. 7 legend "Figure 7 in the Data Supplement" and the text "Figure VII" for cell size (Data Supplement Fig. VIIIC); Data Supplement "supplemental figure 6B" for BJ purity (Fig. VB).

## Figures and data reader

- **S1 (Data Supplement Fig. I D, cTnI/GAPDH).** Supplement p. 13, vector panel: three filled bars (collagen, laminin, matrigel) with error bars, axis 0.00–0.08, a single "*" over matrigel. No individual points, so it is recorded as `no_points` with no script. The legend prints no means and no n for panel D, so S1D_ctni keeps only its printed P. No released data files.

## Vocabulary agent

- **No flags, no split requests.** Every unmapped value was one context.
- **Spontaneous activation rate (F2C)** was mapped to *calcium transient frequency*, because it was read from calcium optical mapping. The beating frequency in F4D, also read from calcium transients, is matched by code to *contraction frequency*. The two rates in this paper therefore sit under different measures. No synonym was added.
- **Interaction items (F4D)**: "E4031-induced reduction of spontaneous beating frequency" and "E4031-induced increase of CaTD80" were mapped to the base measures (*contraction frequency*; *calcium transient duration*, level CaTD80). The E4031 effect is left to the contrast. The reader's measure wording includes the treatment; consider writing only the measure.
- **preparation "monolayers" (F1)** was mapped to *live cells* without a synonym, because "monolayers" names the platform. The reader may want to write "live cells".
- **S5A "cell size"** has no numbers, so it was mapped to *cell size* (proxy: judged from immunostaining images) rather than *cell area*. It was a judgement call.
- **S5C "sarcomeric cTnI incorporation"** was mapped to *sarcomere organisation* (aspect: cTnI incorporation into sarcomeres). The ~2 µm value is a spacing, not a sarcomere length measurement.
- **Three cTnI wordings** ("cardiac troponin I protein expression (cTnI/GAPDH)", "… protein expression", "cardiac troponin I expression (cTnI/GAPDH)") name one measure. All map to *protein level* (cTnI / GAPDH). The reader could unify them.
- **F8 "relative to control"** was mapped as `expressed_as: fold`, `normalised_to: "GAPDH, relative to control"`. The F8 items carry no values, so this is inferred from the wording only.
- **Collagen coating (S1)** is collagen isolated from Matrigel (Sigma C0543). The paper does not state the type, so a new term *collagen, type not stated* was added in replating_coating.
- **Silanized glass (S2)**: two new substrate terms under *glass*. The supplement says both were made by coating with dimethyl siloxane, but they are named and reported apart.
- **Not in ontologies** (adopt_own): BJ-iPSC7 (Cellosaurus 57.0), FAK inhibitor-14 (Y15) (ChEBI), anti-integrin β1 blocking antibody MAB1951Z (ChEBI), MAB1969 activating α5β1 antibody (ChEBI). UM 22-2 was adopted as CVCL_E087 (UM22-2).
- **Possible record issue**: the anti-integrin β1 antibody is "MAB1951Z" in the supplement methods, while the activating antibody in Fig. 8 is "MAB1969". The record keeps them apart correctly; noted only because the catalogue numbers are close.

## Formula agent

- **Upper 95% CI of matrigel+PDMS CV (47.8 cm/s).** Rebuilt as mean + t(0.975, n−1)·SEM = 43.6 + 2.306·7.0 = 59.7 cm/s; code says inconsistent. Neither "7.0 is an SD" (49.0) nor the normal quantile (57.3) gives 47.8. Both are written as labelled alternatives, but code does not run alternatives with formulas yet. Proposed derived entry `ci95_upper_from_sem` (ci95_halfwidth + sem_def + sum_of_parts); until it is applied, library consistency reads "cannot check".
- **"reduced by ≈20%" (PDMS beating rate)** rebuilds to 23.5% from 1.02 → 0.78 Hz; code says close.
- **"increased ≈3X" / "≈1.34×" (CaTD80)** was read as a post/pre ratio, not as a relative increase. The ratio fits (3.09, 1.345); a relative-increase alternative is listed.
- **qPCR "fold of expression = 2^(−ΔCt)"** is printed as an image (supplement p. 7, not in the text layer). The anchor is the preceding words. It uses ΔCt with no calibrator, mapped to `ddct_relative_expression` with ddct := ΔCt. Strictly, 2^(−ΔCt) is expression relative to GAPDH, not a fold change between groups. The qPCR items carry no values, so nothing is rebuilt.
- **Conduction velocity:** every CV item (14) is "measured as described previously" (ref22), so it has no formula. I applied the main-text Methods anchor to the supplement CV items (S1C, S2) as well, because their legends give no method.
- **Ki67 percentage denominator** ("percentage of Ki67 positive binucleated iPSC-CMs"): binucleated cells or all gated cells is not stated.
- **Not written:** current densities (F3G, F4B: pA/pF, no values), cell area (measured in software), S1B confluence (no method in the S1 legend), Western items without values (F4C, F7D, F7E, F8, S1D, S8B), and the abstract's "≈2× faster than previously reported" (no comparator value printed).
- **Gate/spec:** `alternatives` with a formula are labels only, and code does not evaluate them. Agent field names (`model`, not `name`) are not stated in the brief.
