## Record reader

- **Two versions of the same paper in the folder.** `journal_version.pdf` (Science) and `nihms727908.pdf` (NIH author
  manuscript) are the same study. The schema has no field for "two renderings of one source", so both are in
  `source.files`, quotes are taken from whichever version prints the sentence, and `source.version_note` says so. Where
  the two differ I noted it on the item: Fig. 2H is "n>15 per genotype" (manuscript) and "n > 15 regions per genotype"
  (journal); Fig. 3E is "N>4" (manuscript) and "N ≥ 4 lanes" (journal). I recorded the manuscript wording in `n.printed`
  because every other quote of the record comes from that file.
- **Two unlabelled P in Fig. S2J.** The panel prints `p<0.002` and `p<0.001` over six isogenic groups; neither the
  legend nor the text says which bars they mark. I wrote one omnibus item over all six groups with the first P in `p`
  and the second in `p_values`, and a note. Picking two pairs would have invented comparisons.
- **Same problem in Fig. S3B and Fig. S3E.** S3B prints `p<10E-15` beside the I-band row and beside the all-TTN row;
  S3E prints one `p<0.03` over EGF/HGF/bFGF. I wrote omnibus items (S3B: one per segment; S3E: one extra item beside
  the three per-gene measurement items) with a note each, rather than attach a P to a gene the paper does not name.
- **A test that crosses two figure panels.** "cN22577fs+/− ... (2.19 μN) compared to isogenic cWT-CMTs (Fig. 1E,
  p<0.003), but not to the extent observed in pA22352fs+/− or pP22582fs+/− CMTs (0.767μN and 1.001μN, respectively,
  p<0.02)" compares groups of Fig. 1E with groups of Fig. 1D. Groups belong to one unit, so I made a text unit `TXT1`
  that re-declares the four groups and carries the three printed values and the two P; `F1D` and `F1E` keep their own
  items without those numbers.
- **Which pairs a panel tests.** Fig. 1D's title names the comparison ("compared to pWT"), so I wrote three pairs.
  Fig. 1E's legend names no comparison but the legend says significance was assessed by Student's t test for (D)–(H);
  I wrote five pairs against cWT. If that is too generous, those five items are the ones to drop.
- **Main-figure panels print no P.** Fig. 1 and Fig. 2 panels are images; no asterisk or threshold is extractable and
  the legends give only the test. Those items carry `p: not stated`, not `significant, threshold not stated`, because I
  could not verify that a mark of significance is shown. A figure job may see marks I could not.
- **`p<0.01` applied to seven items.** The Results sentence "significant attenuation (all p<0.01)" covers Fig. 3D–H
  without naming each measure. I put `p<0.01` on the five Fig. 3E and two Fig. 3G items with a note; the Fig. 3D RNAseq
  items (Bayesian P) kept `not stated`.
- **`disease_model` of the CRISPR lines.** The paper calls the CMTs "models of TTNtv", never models of DCM, and the
  I-band variant is described as tolerated. I wrote `disease_model: not stated` for every c-line and for
  pS6394fs+/− (a "benign variant"), `dilated cardiomyopathy` only for the three DCM patients' lines, `none` for pWT and
  cWT. Inheriting DCM from the paper's subject would have been the inference the spec warns about.
- **`preparation` of a microtissue.** No field value is printed for "what the sample is"; the nearest stated wording is
  "microtissue" ("For quantifying microtissue forces"), which repeats the platform's words. I used it rather than write
  an unstated "intact tissue".
- **`donor_age` of the patient lines.** Table S1A gives "age at diagnosis" (15, 31, 18 years), not the age at which
  blood was drawn, so `donor_age` stays *not stated* for the iPSC groups and the ages are evidence values of `T1A`.
- **Patients as groups.** Table S1A's three DCM patients and the two LV tissue samples are `kind: native tissue`;
  a patient's clinical phenotype is not tissue, but no other kind fits and the context must not be inherited.
- **Left out and logged.** Fig. 1A–C, 2A–C, 2G, S1, S5, S7 (schematics, representative images and gels with no
  quantification); Fig. 3A (Ingenuity upstream-regulator Z-scores — a computed enrichment, not a measurement of a
  group); Table S1C (2237 gene FPKM rows — a differential-expression list, feeding Fig. 3B–D, whose rows belong to the
  figures-and-data job rather than to printed values); the `%edited` column of Table S1B (stored as a raw float,
  16.666666666666664, whose printed precision I cannot know) — I recorded the four counts it is computed from.
- **Typos recorded as suspected errors, not corrected.** Fig. S2J's legend names cN2257fs and cT33520fs+/−; Fig. S4A
  names cT33520fs+/−; Fig. S4B names P22528fs+/−; Fig. S6G labels a group S22353fs+/−. The supplement itself prints the
  word "typo" over Fig. S6B.
- **`other_conditions`** was not needed: every stated condition fitted a field. Mitomycin C pre-treatment of the stromal
  cells is the one borderline case; it is a treatment of the hMSCs, not of a compared group, and I left it out.

## Figures and data reader

- **S2C (Supplement p. 6, panel C)**: not read. It holds two horizontal bars (Day 12 pre-selection, Day 60
  post-selection; x axis TnnT% 0–100) with one whisker each and no per-sample markers, so it is recorded under
  `no_points`. The legend's "N>4 samples" cannot be checked against counted points.
- No released data covers S2C: the Supplemental Table's sheets are DCM phenotypes, CRISPR Cas9, RNAseq CRISPR and
  Genotypes; none holds TnnT%.
- Record note: the item's groups are `pre`/`post`; the figure labels them "Day 12 Pre-selection" and "Day 60
  Post-selection", so the two bars also differ in day (12 vs 60), which the record's unit context does not state.
- **S2E (Supplement p. 6, panel E)**: not read. Five box plots (Exp 1–5, the five biological replicates of
  pP22582fs+/−; twitch force 0–6 µN) show median, quartile box and whiskers only, with no per-tissue markers, so it is
  recorded under `no_points`. The legend's "five different biological replicates" matches the five boxes; the number
  of tissues per box is not printed. No released data covers it (the Supplemental Table holds no force values).
- Record note: the item has one group (`pP22582fs`), but the panel shows five separate distributions (one per
  experiment); a reading would have to keep them apart, not pool them.
- **S2G (Supplement p. 6, panel G)**: not read. Six bars (pWT and pP22582fs+/− on Days 4, 5 and 6; twitch force
  0–10 µN) with error bars only; the vector objects hold bar rectangles, whiskers and axes and no per-CMT markers, so
  it is recorded under `no_points`. The legend's "N>4" cannot be checked against counted points. No released data
  covers it (the Supplemental Table holds no force values).
- Record note: the panel's x-axis group label prints "pP22582fs+/-" over a partly hidden "pP22583fs+/-" in the PDF
  text layer (the same overlap is in panel H); the record's groups use pP22582fs, which matches the visible label.
- **S2I (Supplement p. 6, panel I)**: not read. Two bars (pP22582fs+/− grey, pWT white; stress 0–0.8 kN/m2) with
  error bars only and no per-tissue markers, so it is recorded under `no_points`. The legend's "N>25 tissues" cannot be
  checked against counted points. No released data covers it (the Supplemental Table holds no stress values).
- **S4A (Supplement p. 8, panel A)**: not read. Three continuous 1D Fourier spectra (pWT, pP22582fs+/−,
  cT33520fs−/−; summed |F(u,v)| 0–1 against ω 0–3 µm⁻¹), one averaged curve per group with no per-myocyte markers,
  so it is recorded under `no_points`. The legend's "N>15 myocytes" cannot be checked against counted points. The
  item's definition (area under the first nonzero peak, normalized per condition) is not plotted as a value per cell.
  No released data covers it (the Supplemental Table holds no FFT values).
- Record note: the figure's own legend prints "cT33520fs-/-", agreeing with the main text; only the caption says
  cT33520fs+/− (the record's suspected error stands).
- **S4B (Supplement p. 8, panel B)**: not read. Two continuous 1D Fourier spectra (WT LV solid black,
  P22582fs+/− LV grey dashed; summed |F(u,v)| 0–1 against ω 0–2 µm⁻¹), each one averaged curve drawn as a vector
  Bézier path (126 segments) with no per-myocyte markers, so it is recorded under `no_points`. The legend's
  "N>15 myocytes" cannot be checked against counted points; the item's definition (area under the first nonzero peak,
  normalized per condition) is not plotted as a value per cell. No released data covers it (the Supplemental Table's
  sheets are DCM phenotypes, CRISPR Cas9, RNAseq CRISPR and Genotypes).
- Record note: the figure's own legend prints "P22582fs+/- LV", agreeing with the main text; only the caption prints
  P22528fs+/− (the record's suspected error stands).
- Fig. S6C (Supplemental_text_and_figures.pdf p. 10): not read. Grouped bars (P22582fs+/- n=4, WT n=6, Adult LV n=8)
  for four titin species with error bars only; no per-sample markers, so S6C_T2 (and S6C_fetal, S6C_N2B, S6C_T3) get
  no points. The Supplemental Table holds no titin densitometry. Record note: the S6C unit lists an `LV_adult` group,
  but no S6C item compares it (legend: adult tissue was not included in the statistics).
- Fig. S6G (Supplemental_text_and_figures.pdf p. 12): not read. Grouped bars (S6394fs+/- n=6, S22353fs+/- n=3,
  P22582fs+/- n=8, WT n=9) for four titin species (fetal Ttn/N2BA, N2B, T2/trunc Ttn, T3; titin expression normalized
  to obscurin, 0-300) with error bars only. The vector objects hold bar rectangles, 16 whisker paths, axes and legend
  swatches and no per-sample markers, so S6G_fetal, S6G_N2B, S6G_T2 and S6G_T3 get no points. The printed n cannot be
  checked against counted points. The Supplemental Table holds no titin values. Record notes: (1) the panel's legend
  labels the dark-grey group S22353fs+/- (the record's suspected error stands). (2) The record's `n.printed` reads
  "n = 6, n = 3, n = 8, n = 9", and its per_group map gives pWT 9 and pP22582fs 8. That agrees with the panel's legend
  order (S6394fs, S22353fs, P22582fs, WT). (3) Two N2B bars (S22353fs, P22582fs) are at or near zero.

## Vocabulary agent

- **Unparseable quantities.** `wnt_activation_days` "D0-D1" and `wnt_inhibition_days` "D3-D5" cannot be read by code as
  quantities, and a quantity field takes no terms. No flag kind fits well, so I flagged both *not a context* and asked the
  reader to write "day 0-1" and "day 3-5". The spec could add a flag kind for "a quantity printed in a form code cannot read".
- **donor_age "adult human donor hearts"**: flagged *not a context*. It holds the declared state *adult* plus species and
  tissue words; split request: "donor hearts" → platform. The reader should write "adult".
- **cell_line "patient-derived iPS-CMs"**: flagged *several conditions*. It names no line, and at unit level it spans groups
  from different patients (pWT, pW976R, pA22352fs, pP22582fs). Groups should carry their own line names. Only the S2F clones
  name lines, so I added two own terms (pWT, pP22582fs) with `clone` as a qualifier, following the precedent of other
  studies' unnamed lines. The other patient lines got no terms because no value names them.
- **hipsc_medium "feeder-free conditions"**: flagged *not a context*. It is a culture condition, not a medium.
  **purity_method "FACS analysis or by morphology"**: flagged *alternatives*.
- **measure "growth factor transcript level"** (S3E_p003): flagged *alternatives*. The single p<0.03 marks one of EGF, HGF
  or bFGF, and the source does not say which.
- **Possible record or paper inconsistency:** genotypes A22352fs+/− (Fig. 1, Table S1A) and A22353fs+/− (Fig. S6, Results
  text) may be one line printed two ways. I mapped them as written, as two TTN variants.
- **Platform "cardiac microtissue"**: mapped to a new µTUG term under *tissue between two pillars*. I added no synonym
  because the phrase is broader than this format. The mechanical_load values "cantilever", "flexible cantilever", "rigid
  cantilever" and "microposts" all map to *auxotonic*. The reader's qualifier "spring constant" on "microposts" is a
  stiffness, but the record names it differently from the `stiffness` qualifier used elsewhere.
- **Judgement calls on measures:**
  - "sarcomere organization (ɛ)" → *sarcomere alignment index* with `normalised_to` "maximum value observed for each
    condition". The paper's ε uses a different denominator from the term's definition.
  - "static force" → *passive tension*, with stretch not stated. "Static force" in µTUGs may include cell prestress.
  - "tissue stress" → *twitch stress*, based on the methods' definition.
  - "strain energy" → *contractile work*, with a synonym added.
  - PSI values → *transcript isoform fraction*, as its scope note says.
  - Gene qualifiers use HGNC symbols (TGFB1, VEGFA, FGF2 for bFGF).
- **No ontology term:** CL has no iPS-cell class, so "iPS cells" maps to CL:0002248 *pluripotent stem cell*. ChEBI has no
  VEGF or TGF-β proteins, so both are own terms marked "isoform not stated".
- **Transgene:** STEMCCA (an integrating lentivirus; the paper reports no excision) got a new *reprogramming factor vector*
  branch.

## Formula agent

- **No data or readings:** the record has no `data.yaml` or `readings.yaml`, so almost no chain can be rebuilt. Code
  rebuilt only three derivations from printed values: TXT3 fold, T1D mutant share and the S6F 100 % index.
- **Force formula not stated:** "Displacement values were run through a custom MATLAB script". The 25 force derivations
  are `no_formula`, with Hooke's law on one cantilever as a labelled alternative. Which stiffness (0.20 or 0.45 µN/µm) was
  used outside Fig. 1F is not stated.
- **"greater than four-fold more than that produced by pP22582fs+/−" (F1F_high):** this could mean the ratio of forces at
  high load (the record's reading, used here) or the ratio of the load-induced increases (the Δ in Fig. 1F). The second
  reading is given as an alternative. The "two-fold" and "four-fold" values have no numeral, so code cannot judge them.
- **TXT3 "5-fold":** ">80" is a lower bound, but code parses it as 80, so 80/18 = 4.44. Code judged it consistent with
  "5-fold" through the printed-precision interval. A true value above 80 % only raises the ratio.
- **T1D "Ratio" 0.53/0.47:** this is read as the mutant and WT shares of 177 and 160 reads (part_of_whole). The column
  header says "Ratio", but the plain 177/160 ratio is 1.11. Code reads only the first number of the printed pair.
- **Strain energy (S2D):** the energy is computed "on each attached micro-post", but the figure plots it per cell. How
  posts are combined is not stated. I proposed `spring_strain_energy` (model, U = k x²/2). No post displacement is printed,
  so both assumptions are not stated.
- **Stress (S2I/J):** the cross-sectional area and its measurement are not stated. Which force items share the tissues is
  also not stated: S2I has N>25, against N=5 in Fig. 1D.
- **Possible issues in the paper, not in the record (for code or the reader):** Table S1(B) prints a derived "%edited"
  row (edited/screened × 100), which is not a record value. Edited clones ≠ homozygous + heterozygous for cN22577fs
  (15 vs 2+12) and cV6382fs (62 vs 56+4), but they are equal for cT33520fs. The partition is not stated, so no derivation
  was written. In Table S1(C) the column "CRISPR WT/avg TTN mutant" matches avg(mutants)/WT, not WT/avg (7SK row:
  3.71/10.79 = 0.34). That column is not in the record.
- **FPKM (17 items):** a named normalisation with no library entry. I did not propose one: no inputs are printed, and the
  given-entry count is already above target.
