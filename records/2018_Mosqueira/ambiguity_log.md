## Record reader

- **The supplement arrived as a zip.** `papers_dont_ever_commit/2018_Mosqueira/` held only `ehy249.pdf` and
  `ehy249_supp.zip`. No extractor in the build opens a zip, so nothing in the supplement could be anchored and the
  supplementary Methods hold almost all of the culture context. I extracted the archive's files beside the PDF (the
  folder is never committed, the zip is kept and listed in `source.not_used`, `Thumbs.db` was left out) and anchored
  against the extracted `.docx` and `.xlsx`. If the rebuild would rather readers never touch the paper folder, the
  gate needs to read inside archives instead.
- **Characters lost in extraction.** Both extractors render the paper's `+` as `þ` and `µ` as `l` or `m`
  (`1 µM nifedipine` → `1 lM nifedipine`, `α-actinin + cells` → `a-actinin þ cells`), and `≥` as `>_`. Quotes holding
  those characters are never found. I shortened quotes around them where I could. Where the value itself needs the
  character (`treatment.concentration: 1 µM`), I used an anchor of `kind: unit` with the legend's wording and said so
  in `where`. 02-audit calls a unit lost in extraction a suspected error, but gives no rule for a context value whose
  anchor cannot be matched; `kind: unit` was the only way through the gate.
- **Values assembled from several sentences.** `differentiation_factors` is BMP4 + Activin A (one sentence) and
  KY0211 + XAV939 (the next). One quote of 30 words cannot hold all four, and `context_anchors` requires the quote to
  hold every word. I gave the field an inline `anchor` (which the gate checks for existence, not for holding) and a
  note naming the second sentence. The schema has no way to anchor one value to two quotes.
- **`number_of_lines` per unit.** The paper states 3 lines paper-wide, but most figures use one. Putting 3 in
  `default_context` would leak it into AT1-only units, so I wrote `3` in the units that show all three lines and
  `not stated` in the rest, rather than counting lines from a legend.
- **Figure 3B and Supplementary Figure S4C–E are one unit.** They are the same BNP experiment shown for AT1 and for
  the other two lines, and the text's fold ranges span all three. Splitting them by figure would have left those
  ranges with no unit that holds their groups. The same for multi-nucleation (3D + S4F,G) and MYH7:MYH6 (7F,G + S9E).
- **Nifedipine time points as item context, not groups.** 02-audit makes a level of a number its own group, but the
  printed tests in Fig. 5H compare genotypes *at* a time, not times with each other, so the time sits in the item's
  context (anchored to its Supplementary Table 4 cell, the only place it is written). Pacing frequency in Fig. 6M and
  S8K, where the tests *are* between levels, is in the groups.
- **Omecamtiv panels compare genotypes, not drug against vehicle.** Fig. 6I–K and S8H–J plot change from each
  tissue's own baseline and the printed P compare lines. I made each group the drug-treated line and said in the
  unit's note that each group is its own control; code will see no treatment contrast in those pairs.
- **`treatment: none` for untreated units.** The paper never says "no drug", so this is my reading of an assay
  described without one; the alternative, `not stated`, would make every unit's treatment unknown.
- **What I left out.** Figure 7D/E and S9D/F/G (nanoString heat maps, sarcomeric gene bars) print no numbers and no
  P; I recorded only the directions the text states for 7D and 7E and left the heat-map cells unread. Supplementary
  Figure S5 is in-silico structure modelling (model output, not evidence). Figure 2A, 1A–D, 5A–B, S1–S2, S7 are
  schemas, gels and micrographs with no values.
- **Suspected errors recorded, not corrected:** Fig. 5J prints 0.0365 where Supplementary Table 4 gives 0.0312 for
  that panel; S8D prints 0.0001 where Table 4 gives <0.0001; Table 4 rows 30 and 43 name an "M/W+6W/f" line that does
  not exist; row 8 writes "AT1 K/K + AT1 W/W"; the S3C/D test is an F test in the legend and a 2-tailed t-test in
  Table 4; Fig. 6H says 2 Hz pacing where the Methods say 1.75 Hz for AT1.
- **n counts.** The Methods define N as biological replicates performed in triplicate; the EHT legends' n is almost
  certainly tissues. I wrote "engineered heart tissues" for the EHT units and "biological replicates" elsewhere,
  which is an interpretation the paper does not state outright.

## Figures and data reader

- **F3b (Fig. 3B; Supplementary Fig. S4C-E).** Not read. Fig. 3B plots stacked bars (% negative / medium / high BNP)
  with mean ± SD error bars per segment and no individual points; S4C-E are the same kind of stacked bars for the
  REBL-PAT and HUES7 lines and do not include the item's groups (AT1 M/M+6W/f, AT1 K/K). Recorded as `no_points`.
  Supplementary Table 4 holds only p-values (rows 11-26 for Fig. 3B), no group values, so no `data.yaml` rows.
  Item F3b_mm6_kk (no increase in BNP for M/M+6W/f and K/K) therefore rests on the printed text and the bars alone.
- **S6ad (Supplementary Fig. S6A-D, ehy249_Figure_S6.tif).** Not read. Panel A is a Seahorse time course of mean OCR
  with error bars per line; B (basal respiration), C (maximal respiration) and D (ATP production) are bars with upper
  error bars only; no individual points, so no script. Recorded as `no_points`. Supplementary Table 4 holds only the
  S6C p-values (rows 131-132), no group values, so no `data.yaml` rows. Item S6ad_basal_atp ("similar" basal
  respiration and ATP production, N=5) rests on the legend text and the bars alone.
- **S6gik (Supplementary Fig. S6F-K, ehy249_Figure_S6.tif).** Not read. F, H and J are representative flow-cytometry
  histograms (one sample per line, not per-replicate values); G (Mitotracker green), I (CellROX) and K (MitoSOX) are bars
  of median intensity relative to WT with upper error bars only; no individual points, so no script. Recorded as
  `no_points`. Supplementary Table 4 holds only the S6I p-value (row 134, 0.0412), no group values; Tables 1-3 hold
  nothing for S6. No `data.yaml` rows. Item S6gik_nodiff ("no differences", N=7) rests on the legend text and the bars.
- **S8k (Supplementary Fig. S8K, ehy249_Figure_S8.tif).** Not read. The force-frequency panel plots one mean marker
  with error bars per genotype (W/W circles, M/W squares, M/M triangles) at Unpaced, 1.5, 2 and 2.5 Hz, joined by
  dashed lines; no individual points, so no script. Recorded as `no_points`. Supplementary Table 4 has no S8K rows
  (S8 rows 135-146 cover B, D-F, H-J only) and Tables 1-3 hold sequences only, so no `data.yaml` rows. Item
  S8k_nodecline ("decline in force was not seen", no printed test) rests on the Results text and the plotted means.

## Vocabulary agent

- **"ATP production" was matched by code to `measure:atp_production`** (an amount of ATP from substrate use). Here it is
  the Seahorse Mito Stress parameter, i.e. oligomycin-sensitive OCR (`measure:atp_linked_respiration`). The label match is
  code's and cannot be overridden by a mapping; the re-map checkpoint should look at this label/synonym clash.
- **"basal respiration" made a synonym of `measure:basal_mitochondrial_respiration`**, on the Mito Stress Kit convention
  (non-mitochondrial OCR subtracted). The paper does not spell out the subtraction.
- **"XF base medium" made a synonym of `measurement_medium:seahorse_xf_dmem`.** Agilent #102353 (XF Base Medium) is the
  older DMEM-based unbuffered Seahorse medium, not literally "XF DMEM Basal Medium"; it fits that term's definition.
- **"percentage of cardiomyocytes, all categories"** is one wording for two different things: every BNP bin (Fig. 3B)
  and every nucleation class (Fig. 3D, S4F). Flagged *several measures*; the reader could split these items per bin or class.
- **Flagged *several measures*:** "bi- and multi-nucleated cardiomyocytes", "basal respiration, maximal respiration and
  ATP production", "basal respiration and ATP production", "mitochondrial content and ROS production", "mono- and
  bi-allelic targeting frequency". Each item holds two or three measures; one item per measure would let them map.
- **Flagged *several conditions*:** genotype "gene-edited" (the 11 edited lines carry different MYH7 genotypes) and platform
  "2D monolayers and 3D-engineered heart tissues" (the RNA-seq unit pools both formats).
- **Genotype variant qualifier R453C** was taken from the paper's design (title, legends: R453C-βMHC, 9123-MYH7) for the
  values "MYH7 heterozygote/homozygote (MUT/…)", which say only MUT. "homozygote + MYH6WT/fs" maps to the set {MYH7
  variant, MYH6 variant}; one mapping carries one qualifier set, so each qualifier names its gene.
- **AT1 and REBL-PAT are not in Cellosaurus** (AT1 there is SUP-B26, a leukaemia line): own terms. KY02111 is not in
  ChEBI: own term, with the paper's spelling "KY0211" as synonym (the reader noted the spelling).
- **"dissociated hPSC-CMs" made a synonym of `preparation:dissociated_cells`.** In F4gik (flow cytometry) and F2bc this is
  right; in F5df/F5gh/F5ij the dissociated cells were replated in dishes and imaged as cultured cells (`live_cells` would fit
  better). Possible reader fix: a different preparation value for the line-scan units.
- **Ca2+/Mg2+-rich HBSS (F4gik)** is the dye-loading medium; the cells were resuspended in PBS for flow cytometry. The reader
  may want `measurement_medium` to say PBS. Mapped as stated (HBSS, formulation with Ca2+/Mg2+).
- **S3a_mlc2v** holds an `mlc2a_panel` value (MLC2v/MLC2a ratio) under the measure "MLC2v positive cardiomyocytes"; that
  value is a different ratio and may belong in its own item.
- **vehicle**: "vehicle (0.1% DMSO)" maps to DMSO (concentration 0.1%); the ranolazine "vehicle" names no solvent, so it maps
  to an own term `treatment:vehicle_not_stated`. Whether a vehicle should be its own term or its solvent is a spec gap.
- **Relative measures**: existing `relative_*` terms were not used; the base measures carry `expressed_as`/`normalised_to`
  as tab 3 says. "Mitotracker/CellROX/MitoSox intensity" take `expressed_as: normalised` to wild-type from the reader's method text.
- **Not used for this paper, but noted:** "median" (F2bc) has no qualifier on `cell_volume`; noted in the mapping only.

## Formula agent

- **Nothing to rebuild from.** There is no data.yaml or readings.yaml (bars without points; Supplementary Table 4 holds P values
  only), so 175 of 176 derivations have no inputs. One rebuild exists: F3f kk/ww = 56.4/14.0 = 4.03, but code cannot read the
  printed "four-fold" as a number ("output has no single value"). Observation for code: word numbers (four-, ten-fold) could be parsed.
- **Force (F6eg, F6lm, S8df, S8k):** the Methods name the inputs ("post deflection", "the known mechanical properties of the
  silicone posts") and cite Mannhardt 2016, but print no relation. Recorded as `no_formula` with Hooke (F = k*x) as a labelled
  alternative instead of mapping to hooke_spring. As a result no linear-spring/small-deflection assumption report is made. Either
  reading is defensible.
- **Percentages of counted cells** (F3b, F3d, F3f, purity, MLC2v, ventricular share, targeting frequency) are written as
  count/total ratios with unstated counts. I am not sure the spec wants these: they add about 60 derivations that cannot be checked.
  For F3d and the % of baseline items (F5gh, F5ij), "%" is in the raster axis only, so the anchor is "not stated".
- **Ambiguous wording, run as alternatives:** "n-fold higher/increase" (ratio vs relative change); "ten-fold lower" (WT/KO vs KO/WT);
  F3d "increase in bi- and multi-nucleation (1.9–3.6% and 1.1–1.9%) relative to WT/WT" (percentage-point difference, relative
  change, or the WT/MUT level itself); "changes from baseline" on OM (relative vs absolute; the record's measure says % change);
  "ratio of MUT: WT alleles" (MUT/WT vs MUT/(MUT+WT)).
- **Printed-formula typo:** S3 legend and main text print "(APD80-APD70)/APD40-APD30)" with an unmatched parenthesis; written as
  (APD80-APD70)/(APD40-APD30), as the record's measure reads it.
- **Mean vs median:** the Methods say "Mean signal fluorescence intensities" (F4gik). The record's method says median.
- **Ranges over lines** (F2bc 12–51 %, F3b folds, F7fg 5–15-fold, S8df 0.04–0.06 mN, F3d) name no line per end, so no output is
  named for them. F4bd's 3/2.75/3-fold name no genotype. They have outputs, but their inputs are unknown.
- **Unstated steps** (no derivation written): basal/maximal/ATP-linked OCR from the Mito Stress trace ("manufacturer's
  instructions"), the FSC-to-diameter calibration curve (Fig. 2A, form not printed), nanoString housekeeping normalisation, and
  beat rate from peaks. These are noted in the derivations' input notes.
- **Proposals:** sphere_volume (model, CRC tables) and its derived diameter form (the paper prints V = π/6 × diameter³ as an
  equation object), ratio_of_differences, and difference_from_reference. The first try of ratio_of_differences used the variable
  names a1, a2, b1, b2. It then had the same variable set as ratio_of_products and was rejected as "contradicting" it. Renaming the
  variables fixed it, but the contradiction check keyed on variable names looks fragile.
