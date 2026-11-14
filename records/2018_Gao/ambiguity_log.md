## Record reader

- **What a pig heart is.** Most of this paper measures infarcted swine hearts, not engineered tissue. The spec's group
  kinds are *engineered*, *native tissue* and *other study*. I made every in-vivo group (Sham, MI, MI+OP, MI+hCMP in F4,
  F5, TXT1, F7be, F7gi, F8, ST2, and the proteomics replicates in S8) `kind: native tissue`, because that is what the
  measured tissue is: a pig's own ventricle. The cost is that code will label every in-vivo pair *against benchmark*,
  so the paper's main contrasts (hCMP vs open patch vs untreated) carry no contrast and no confound, even though they
  are the designed comparisons of a controlled animal study. A kind for *host tissue in an animal experiment*, or a way
  to mark a native-tissue group as the unit's own experimental arm, would fit this paper.
- **Transplantation as a `treatment`.** I put the in-vivo intervention in `treatment` ("two hCMPs", "two open fibrin
  patches", "none"), with immunosuppression as a qualifier. No field describes an implanted construct, and `platform`
  would say the measured object was engineered, which it was not.
- **A set that no single sentence states.** `differentiation_factors` and `purification` for the tri-lineage patches are
  unions over three differentiation protocols (CHIR99021, IWR-1, ascorbic acid, VEGF, SB431542, PDGF-BB, TGFβ1; lactate
  selection, FACS, CD34 bead selection), and each member is stated in its own sentence. A context anchor must hold every
  word of its value, so a combined value cannot be anchored. I wrote the first member as the value and the rest as
  qualifiers (`differentiation_factors: {value: CHIR99021, qualifiers: {wnt_inhibitor: IWR-1, ...}}`), which anchors
  cleanly but loses that the members are one set. The same shape is used for `purification`.
- **Stretch during a measurement has no field.** F3gh compares eight stretch levels (100–121 % of slack length) and the
  pacing-, isoproterenol- and BDM-units all state "stretched to 110 % of slack length". `mechanical_load` is defined as
  load *during culture*, so I put the stretch in `other_conditions` on the unit, and gave F3gh's eight groups labels with
  no distinguishing field. Code will therefore see eight identical groups in F3gh; it cannot compute the length contrast.
- **Which bar a bracket joins.** Significance brackets were read from 400-dpi renders of each panel (kept in /tmp,
  deleted). Where a panel prints two brackets over one gene or measure I recorded two pairwise items; in Supplemental
  Figure 2 the upper bracket joins hCMP day 1 with hCMP day 7 and the lower one monolayer day 7 with hCMP day 7.
- **Which test.** No figure legend names its test. The paper states paper-wide that two means were compared with
  Student's t test and multiple comparisons with ANOVA and a Tukey post hoc test. Following the convention the spec
  allows for paper-wide P thresholds, I wrote `test: "Student's t test (Statistical Analysis)"` for two-group units and
  `"ANOVA and the Tukey posthoc test (Statistical Analysis)"` elsewhere, naming the source. If that is too generous, the
  honest alternative is *not stated* everywhere.
- **"Not significant" with no P.** Fig. 3J and 3M, Fig. 8A and 8B, the remote-zone panels of Fig. 5E and 5G, and both
  arrhythmia items report "not significantly different" in words with no P and no mark. I wrote `p: "not stated"` with a
  note, rather than reading "n.s." into them.
- **n printed twice in Fig. 3.** The table inside Fig. 3D prints n=12 (CV), n=10 (APD) and n=5 (CaTD); the legend prints
  "n=4–5 in each group" for the whole figure. I recorded the figure's n per item and flagged the disagreement as a
  suspected error on each of the five items.
- **Values inside images.** The Fig. 3D table, the purity percentages in Supplemental Figure 1, the CV values in
  Supplemental Figure 8 and the calcium axis of Supplemental Figure 5 are not in the extracted text. Where the same
  number is also in a sentence I wrote it twice (`_text` and `_figure`); where it is not, I anchored the item to text
  that names the panel, or used `kind: unit` for the context anchor.
- **Which version to read.** The folder holds the journal version, the author manuscript and the author-manuscript
  supplement. Figure and table numbering differs (journal: Figures I–VIII; manuscript: Supplemental Figures 1–8). I used
  the manuscript's numbering and said so in `source.version_note`. One sentence differs in substance between the two
  versions ("CD31 and/or VE-cadherin" against "CD31 and vascular endothelial cadherin"); that is a suspected error on
  the item.
- **Not recorded.** Qualitative images with no quantification (Fig. 1 in full, Fig. 2B–2D, 2F, 2H, 2I, Fig. 4A–4C and
  4E–4F, Fig. 6B–6D, Supplemental Figures 1A, 3C, 7A); the voltage/current traces of Fig. 3E, whose only result is a
  stated phase alignment; the experimental and calculated molecular masses and ppm errors printed in Fig. 8 and
  Supplemental Figure 8, which identify protein forms rather than compare groups; Supplemental Table 1 (qPCR primers),
  which holds no measurement; Supplemental Videos 1–5, which are not in the folder and which no item rests on.
- **A citation that points at the wrong paper.** The Discussion attributes the cardiac-lineage hciPSCs to reference 16
  (Zhang D et al., an ESC patch paper); everywhere else the line is attributed to reference 17 (Zhang L et al.). There is
  no field for a mis-numbered citation, so it is logged here. The three swapped or over-wide panel citations I could
  record are in `cross_references`.

## Vocabulary agent

- **A quantity code cannot read.** `wnt_activation_days` "Forty-eight hours" is one context (48 h), but the quantity
  parser does not read the hyphenated number word. No flag kind fits; it is flagged *not a context* as a stand-in so the
  gate can pass. Fix in code (hyphenated number words) or the reader writes "48 hours".
- **Rocking is not a load.** `mechanical_load` "rocking" and "static" restate the culture regime already in
  `maturation_strategy` (dynamic rocking platform / static culture condition, both now code-matched). The paper states no
  anchoring or loading regime for the free hCMP, so both are flagged *not a context* rather than given a load term.
- **`time_point` "after incubation with BDM"** names the treatment but no time: flagged *not a context*.
- **"number of animals"** (Supplemental Table 2) is a sample size, not a measure: flagged.
- **Pacing in unit S4.** The unit's `pacing` is "pacing", but the item's measure is "spontaneous twitch force" and the
  finding says spontaneous transients. Possibly a reader error; not changed.
- **"pacing" mapped to electrical pacing without a synonym.** The legends say "electronic pacing". A bare "pacing"
  synonym would also cover optical pacing in other papers.
- **"hCMP" has no synonym.** The lab uses "hCMP" for other patch formats, so it is mapped to the new
  `platform:cast_patch` ("cast tissue patch, anchoring not stated") per paper. The methods give a mould and a dish but no
  frame or anchors.
- **Plates as platforms.** "4-well chamber slides", "24-well tissue culture plate" and "12-well plates" are vessels. They
  are mapped to the broader `platform:culture_2d` because the paper does not say "monolayer".
- **EGM 2-MV medium in `supplements`.** It is an EC medium kit with no field of its own (`cm_medium` is for
  cardiomyocytes and is "not applicable" in S7). Adopted as the own term `supplements:egm_2mv`. A medium field for
  non-myocyte cultures may be needed.
- **Purification of non-myocytes.** `purification` is scoped to cardiomyocyte enrichment, but the reader used it for SMC
  progenitors (CD34 immunomagnetic) and ECs (FACS). New terms were added; the field's scope may want widening.
- **Exosomes** are an own treatment term with qualifier `source` (hCMP, monolayers, co-cultures). Annexin V is adopted
  as ChEBI's "annexin a5" (CHEBI:758841). PBS is not in ChEBI (own term).
- **Species xrefs** NCBITaxon:9986 (rabbit) and NCBITaxon:9823 (pig) come from knowledge. NCBITaxon is not pinned, so
  they are unverified.
- **Ptotal** (mol phosphate per mol protein, summed over species) was added as a child of the phospho/total ratio
  because it can exceed one. Whether it is a kind of that ratio is a judgement.
- **Capture range.** "cycle lengths at which the hCMP could be paced" holds both 1000 ms and 450 ms. Only 450 ms is the
  capture limit (`measure:shortest_captured_cycle_length`).
- **Border-zone protein axis.** EPO/HGF/Ang1 read "Target Protein/GAPDH (% of MI)" while values run about 1–2.4, so
  `expressed_as` is left to the values.
- **In vivo time.** The reader put "week 4" in `day_of_measurement`. The in vivo keys from earlier papers (ejection
  fraction, engraftment) use `time_point`, so the new in vivo keys use `day_of_measurement`. The checkpoint should pick
  one field for time after surgery.

## Formula agent

- **2^-ΔCt mapped to `ddct_relative_expression`.** The library entry is stated for ΔΔCt against a calibrator; the paper
  uses 2^-ΔCt against GAPDH with no calibrator. Same equation, so I mapped `ddct → dct` and wrote the ΔCt step with
  `sum_of_parts`. If the library wants ΔCt and ΔΔCt kept apart, a separate entry is needed.
- **Named quantities without printed formulas.** Ejection fraction (QMASS) and systolic thickening fraction are given
  their textbook definitions (`relative_decrease`, `relative_change`) on the strength of the name alone. The paper
  doesn't print either formula. The spec covers named *operations* ("fold change"); whether named *measures* count
  too is my guess.
- **Wall stress.** Proposed `laplace_thin_wall_sphere` (model, σ = P·r/(2h)), matching the formula the paper prints. No
  radius or thickness is printed, so the thin-wall assumption is *not stated*. The remote-zone item covers three groups,
  but each LVSP item covers two, so its P input is `not_stated`.
- **Ptotal.** The printed formula ends in "+ …". I proposed a derived entry for forms with up to three phosphates
  (proved from `mean_def`) and kept higher forms as a labelled alternative.
- **Force per cardiomyocyte (Fig. 3N).** The CM count in the CM-only patches is not printed. The text says they held
  "the same total number of cells", so I built it from the printed 1 + 0.5 + 0.5 million. "1 million" is parsed as 1
  (code doesn't read the word "million"), so the counts are in 10^6 cells. This doesn't matter now, because the Fig.
  3M forces are not read, but it would matter if they were. The `nN/myocyte` unit is unknown to the unit parser.
- **LDH normalisation.** "Normalized to … PBS … expressed as percentage" is in the Exosome cytoprotection paragraph.
  I applied it to the Fig. 6E–H and 6I–J LDH items, but not to viability, whose normalisation isn't stated (the
  axes weren't read).
- **Border-zone proteins.** The Fig. 7 axis reads "Target/GAPDH (% of MI)", a second normalisation to MI that the
  legend doesn't state. I wrote only the GAPDH ratio.
- **Not derived.** APD/CaTD, CSA, LVSP, vessel and Ki67 counts per HPF are measured directly. Conduction velocity
  has no formula (the local-velocity method isn't stated). Impedance is stated only by citation.
- No derivation looks wrong. Nothing can be rebuilt because there are no readings or data, so every chain is *cannot
  check*. Only the bounds (purities, engraftment) give verdicts.
