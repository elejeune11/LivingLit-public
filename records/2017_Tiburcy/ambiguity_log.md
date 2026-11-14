## Record reader

- **Asterisk pairs in Suppl. Fig. 7 and 8a not listed one by one.** Each gene panel has asterisks against 2D D22 and § brackets that a raster figure only shows as marks. I recorded one omnibus item per gene (18 + 9) with the legend's P wording. I did not record each starred pair, which the spec asks for when pairs are printed. A figures reader could add them.
- **Brackets with one asterisk** (Fig. 2c, Suppl. Fig. 6c, Fig. 4a): I could not read which pairs the marks belong to, so each is an omnibus item. For Suppl. Fig. 1c (right), a bracket spanning both curves is recorded as a main effect of the protocol. For Fig. 2d and Suppl. Fig. 10a, a bracket at 3 Hz is recorded as a pair at 3 Hz.
- **Cell line naming.** Legends say "HES2" (Fig. 2c, 2f, Suppl. Fig. 2, 8c) and "HES3" (Fig. 2f), while Supplementary Table 1 maps the same panels to HES2-RFP and HES3-ENVY. I used the Supplementary Table 1 lines, and so their differentiation protocols, and noted this on the units. Suppl. Video 2 names iCell CM for the comparison in Fig. 1d; Supplementary Table 1 says HES2-RFP. I used HES2-RFP and noted the conflict.
- **30-word quote limit against complete sets.** The monolayer differentiation factors (Activin A, BMP4, CHIR99021, FGF-2, then IWP4) are not all in one sentence of 30 words or fewer. I wrote IWP4 as a qualifier (`wnt_inhibitor`) of `differentiation_factors`. The base additions shared by every EHM medium (non-essential amino acids, glutamine, penicillin/streptomycin, and β-mercaptoethanol or ascorbic acid, which differ between protocols) are left out of `supplements`, because no quote of 30 words or fewer holds them together with the serum/B27/growth factors. So the sets list only the protocol-defining members. The schema could use multi-quote anchors for set values.
- **Growth factors: supplements or treatment.** In the Serum-free Protocol and Suppl. Fig. 3f,g the growth factors are part of the medium (`supplements`). In Suppl. Fig. 3e and 3d they are what is compared (`treatment`), as the field scopes say. This puts one stated fact in different fields in different units.
- **Undefined/defined vs protocol.** Suppl. Fig. 1 and 2 compare "undefined" vs "defined" EHM without saying which serum protocol was used. Only composition, purification and HFF are filled there; the serum fields are not stated. The Fig. 4 colour-coded EHM have no stated protocol either.
- **Sarcomere lengths** "1.93±0.01 vs. 1.81±0.01 vs. 1.84±0.01 μm; n>120 sarcomeres from 12/8/10 cardiomyocytes": I assigned 1.81 to 2D and 1.84 to the Starting Protocol by order of mention. n per group is not assigned.
- **Heart failure as disease_model.** NE-induced "heart failure" is recorded only as `treatment` (NE, concentration, 7 days). `disease_model` stays not stated paper-wide, to avoid aliasing it with the treatment.
- **Benchmark pacing** (infant "at 1 Hz", adult "at ~1.5 Hz") is written as a plain `pacing` value. The source does not say "electrical stimulation" for those studies.
- **seeding_density** holds the EHM input cells (1.5×10⁶ cells/500 μl, from the Fig. 5b legend and Supplementary Table 1). The PSC plating density before differentiation (5×10⁴–1×10⁵ cells/cm²) is not recorded, because one field cannot hold both.
- **Preparation wording.** No sentence says "intact tissue". Force items use "organ bath" (from "isometric conditions in organ baths"). Patch FAC uses "recorded using a camera".
- **Suppl. Fig. 3d** is a semi-quantitative image table (+/o/−). I recorded it as one item per read-out, with one value per factor carrying `between: [factor, its comparison medium]`. These are not statistical tests.
- **Matrix Protocol reference** in Suppl. Fig. 3e–g (dashed lines) is a group of its own. Its n is not stated, and its growth-factor treatment is written as "none" (Table 1 lists no growth factors for it).
- **Fig. 4f** prints an asterisk over NE 1 but its legend names no test. Recorded as "significant, threshold not stated".
- **Fig. 2f** cell classes (ventricular, pacemaker) are the paper's classification of recorded cells. No field holds this, so it is in `other_conditions` from figure text. The table values are figure-only (`kind: unit`), with spread taken as SEM from the Methods.
- **Model outputs:** fitted calcium curves (Fig. 1f, 2c, 4a, Suppl. Fig. 4b, 6c) and the EC50 fit are the paper's. Only the printed EC50 is recorded.
- **Supplementary Tables 3–5** (gene lists with RPKM per gene) are not recorded as items: thousands of values with no test.
- **Discussion claim "similar to fetal human heart at 13 weeks of gestation"**: nothing in the paper shows this analysis, and the fetal sample's age is not given. Recorded as a claim with `presence: does not follow`.
- **Cross-references:** the text cites Supplementary Figure 4b/4c for the electron micrographs and M-band/MLC2V/n-cadherin staining, which are Suppl. Fig. 5b,c in the corrected supplement. Supplementary Table 1 cites "Figure 3a-f", but Fig. 3 has panels a–e.
- **Missing:** Supplementary Videos 1–5. The claim "EHM patches and loops contracted similarly" rests on Video 5 alone.

## Figures and data reader

- **F1c (F1c_purity):** no released data; read from the raster panel in the author manuscript (nihms862055.pdf p. 18; the journal version is a lower-resolution raster). Markers overlap in both columns (before: two markers near 60 % nearly coincide; after: six of eight merge into one blob), so pairs are not counted from marker blobs. They are resolved from the eight connecting lines, which stand apart between the columns: a constrained Hough search from each before-marker blob finds 8 lines = printed n=8 (two from the bottom blob). The isolated after marker sits at 88.21 % by its blob and 88.27 % by its line end. The two bottom before values share one blob centre (60.36 %, interval covering the blob, 59.98–60.61). Y ticks are raster; their values (50–100) are assigned from the printed labels in order. Not checked against a printed mean (none printed).
- **F1d (F1d_condense, F1d_rounded):** not readable as numbers. Fig. 1d (nihms862055.pdf p. 18, one raster image for the whole of Fig. 1) is a macroscopic photograph of CM EHM and CM+HFF EHM and two immunostaining micrographs (actinin, f-actin, nuclei). It has no axes, bars, points or colour scale, and the paper releases no data files, so no figures.yaml entry, script or data.yaml row is written. Both items stay qualitative: condensation and rounded morphology are shown only as images (and in Suppl. Video 2, which is missing). No count of rounded cells is printed.
- **F1e (F1e_cmpct, F1e_force; script F1e_ratio):** no released data; read from the raster scatter in the author manuscript (nihms862055.pdf p. 18, ~300 dpi; journal version is ~200 dpi). Each marker is one EHM with x = output CM percentage (labels *_cmpct) and y = force per CM (labels *_force); the two lists share index order. Legend gives no n ("each circle represents one individual EHM"), so counts are the only n: blue 90/10 = 6, black 70/30 = 8. Red 50/50 is bar only (countable false): two red markers near 4.5 and 4.8 nN overlap; 7 red markers are visible but not counted. Judgements: (1) "stands alone" taken within a colour; the blue marker at ~4.4 nN is partly covered by the black one at ~4.5 nN (different colours), and both groups are still counted. (2) Marker centres are circle fits to edges bordering white paper, so the fitted curve and overlapping markers do not pull them. (3) The blue and black upper y caps touch a filled marker, so their upper error ends mirror the lower caps (error bars taken as symmetric; red's two clean caps agree within 1 px, and so do all three x bar pairs). (4) Mean = median of the open marker's hole centre and the bar segments on either side of it. Checks: SD of points over bar length gives implied n 6.0/6.1 (blue) and 7.9/8.0 (black), so the bars are SEM. **Mismatch:** plotted x means (blue 64.87 %, black 47.52 %) sit 1.4 and 1.1 points to the right of the point means (63.46, 46.42). The y means agree (3.40 vs 3.37; 7.34 vs 7.31). Not adjusted. A hidden marker or different data behind the means could explain it. Fig. 1e prints no mean values to check against. F1e_ratio (~1:1) has no figure group of its own. The plotted black x mean of 47.5 % CM corresponds to ~0.9:1.
- **F1f (F1f_foc; script F1f_foc):** no released data; read from the raster panel in the author manuscript (nihms862055.pdf p. 18, ~300 dpi, rendered at 600 dpi). Each marker is a group mean (filled Starting, open Serum-free) at one calcium concentration with a vertical error bar; no single EHM is drawn, so all 20 labels (`start_<mM>`, `sf_<mM>`) are bar only (countable false). Printed n=19/59 cannot be checked by counting. The x of each bar is the calibrated marker position rounded to 0.1 mM (all within 0.005 mM of 0.2, 0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 4.0). The steps are not printed (Methods: "0.2–4 mmol/L"), so the rounding is a judgement. Judgements: (1) markers are found by matching a synthetic disc and ring. Their radius is measured from the filled plot markers, and the ring width is fixed at 0.4 R as drawn in the plot, because the legend circles are larger with a thinner ring and misclassify the plot rings. Filled and open are told apart by inner-disc darkness (1.0 vs ≤ 0.6). (2) Error end missing for start 0.2–1.2 mM and sf 0.2–0.4 mM: both caps merge with the marker or the steep curve, so no clean cap. (3) Where the top cap merges with the marker edge (sf 0.8, start 1.6 and start 2.8 mM), the bottom cap is mirrored about the mean. Where both caps are clean they agree within 1 px. The error type is not stated in the legend. Not checked against printed values (none printed). The fitted curves are the paper's model output and are not read. The audit gives "cannot check" because there are no points and checks skip readings with x.
- **S1ab (S1a_force_cm, S1b_actinin; script S1ab):** no released data; both panels are vector (supplement p. 40) and are read in one crop. Counted markers equal the printed n in all four groups (undef 10, def 9 in a and b). Each group's mean line and upper whisker cap are read as the bar. Judgement: panel b's defined group uses triangles. The vertex centroid sits 0.87 pt below the bounding-box centre and puts the point mean 0.67 MFI below the drawn mean line (64.82 vs 65.49). The box centre puts it on the line (65.48), so the box centre is used. Checks: point means agree with the drawn means within 0.02 (5.236/5.234, 10.431/10.43, 35.695/35.68). The bar half-lengths equal the SEM of the points (1.338 vs 1.341, 0.72 vs 0.725, 5.24 vs 5.246), so the bars are SEM; the legend does not say this. Actinin MFI has no printed unit (stored as "MFI"). No values are printed in the text to compare against.
- **S1c (all 9 S1c items; script S1c):** no released data. Both panels (FOC, mN; T2-50, ms) are vector (supplement p. 40) and are read in one crop. Each marker is a group mean (circles Undef. EHM, squares Def. EHM, as the legend draws them) with a vertical error bar. No single EHM is drawn, so all six groups per panel are bar only (countable false), and printed n (10 undef / 9 def) cannot be checked by counting. Mean = the joint of the bar's two vertical segments (marker box centre within 0.03 pt of it; the connecting lines' vertices fall on it too). 'error' = top end of the upper segment. Columns are named from the Iso/Carb rows under the axis (base, iso, carb). Judgements: (1) in the T2-50 Def. Iso+Carb bar the cap is drawn 0.29 pt above the segment end; the segment end is kept (inside the 0.5 pt interval). (2) One curve point serves several items (e.g. def_iso is in S1c_foc_def_iso and S1c_foc_def_carb), and a figures.yaml label links to one item, so labels are `<item>/<group>` and repeat the same bar (44 readings for 12 bars). The legend does not say whether the bars are SD or SEM. No values are printed to compare against. Read means: FOC undef 0.487/0.586/0.549, def 0.553/0.815/0.702 mN; T2-50 undef 81.6/76.0/76.4, def 100.0/84.0/100.8 ms (base/iso/carb). P checks stay "cannot check" (2-way RM ANOVA not in the library); the audit now computes directions from these means.
- **S1e (all 5 S1e items; script S1e):** no released data. Vector stacked bars (supplement p. 40), one per group (Input cells, Undef. EHM, Def. EHM), segments MLC2V (magenta, base), MLC2A+V (grey), MLC2A (green, top) with colours matched to the legend swatches. No cell pool is drawn, so all labels are bar only (countable false), and printed n=3-4 cannot be checked. Judgements: (1) segments are drawn as overlapping shapes (up to 0.85 pt), so each boundary is the midpoint of the two edges and half the gap is added to the interval. (2) Each error bar is a T drawn upward from its segment's top. 'error' = segment mean + T length, i.e. the bar's upper end in units of that segment's own fraction, not its position on the stacked axis. T bases sit within 0.7 pt of the boundaries. (3) Undef. MLC2A's bar is 0.46 pt long (error 6.54 vs mean 6.11). Read means (input/undef/def, % of CM): MLC2A 21.7/6.1/13.1; MLC2A+V 59.7/44.3/21.2; MLC2V 18.5/49.5/65.6. Each stack sums to 99.9 % (the green top is drawn 0.12 pt below the 100 tick). The legend does not say whether the bars are SD or SEM. P checks stay "cannot check" (Tukey post hoc, no points). Record note: one p<0.05 label is printed over three brackets.
- **S2a (S2a_NANOG, _POU5F1, _ZFP42, _FGF4, _TERT; script S2a):** no released data. Vector bar chart (supplement p. 42) with a split y axis: each segment (0–0.4 and 0.8–1.2) is calibrated from its own tick stubs. Bars are group means with upward-only error bars; no sample is drawn, so every label is bar only (countable false), and printed n=3-6 cannot be checked. Judgements: (1) groups are assigned by slot in legend order (PSC, fibroblasts, undefined, defined), anchored on the black PSC bar. The undefined bars are grey 0.50, but the legend swatch is 0.38; the defined bars match their swatch (0.83). (2) **Not readable:** the fibroblast slot holds no drawing in any gene, so S2a_TERT/hff has no reading. Zero, below one stroke, or not measured cannot be told apart. (3) Defined POU5F1 and ZFP42 bars are 0.2–0.3 pt tall and have no drawn error bar, so they get a mean only. Their 0.5 pt interval reaches below 0. Read means (undef/def): NANOG 0.318/0.0029, POU5F1 0.088/0.0007, ZFP42 0.092/0.0011, FGF4 0.039/0.0057, TERT 0.0136/0.0064; TERT PSC 0.999 (normalised to 1, which checks the upper segment's calibration). The legend does not say whether the bars are SD or SEM. P checks stay "cannot check".
- **S2cd (S2c_def_input, S2c_def_undef, S2d_def_input, S2d_def_undef; script S2cd):** no released data. Two vector bar charts (supplement p. 42, one crop): c Ki67+ cells (%) among cardiomyocytes (ticks 0–15), d among non-myocytes (ticks 0–30), each calibrated from its own axis stubs. One open bar per group with an upward error bar (cap = 'error'). No sample is drawn, so every label is bar only (countable false), and printed n=3-6 cannot be checked by counting. Each bar is drawn twice (filled path and stroked rectangle, tops ≤0.05 pt apart); the midpoint is used and half the gap is added to the interval. Labels are `<item>/<group>` and repeat a bar used by two items. Read means (input/undef/def): c 11.27/11.87/5.68 %, d 23.74/17.47/6.53 %. The drawn significance brackets (Input–Def and Undef–Def, one * each, in both panels) match the record's items. The legend does not say whether the bars are SD or SEM. No values are printed to compare against.

## Figures and data reader (S3a)
- Suppl. Fig. 3a (supplement p. 44) read from vector objects (`figures/S3a.py`): two open bars (rat, bovine collagen
  + Matrigel), each a group mean with an upward error bar. No single EHM is drawn, so no points and no count against
  the printed n (rat 12, bovine 14); both groups are bar only (countable false).
- Read: rat mean 1.00 (error cap 1.066), bovine mean 1.15 (cap 1.27). The rat bar at exactly 1.0 suggests
  normalization to the rat-collagen mean; the legend does not say so.
- The legend for 3a does not say whether bars are SD or SEM (SEM is named only for the dashed lines of panels e-g).
- No released data file covers this panel.

## Figures and data reader (S3b)
- Suppl. Fig. 3b (supplement p. 44) read from vector objects (`figures/S3b.py`): two open bars (Starting Protocol,
  Defined-Matrix Protocol), each a group mean with an upward error bar. Starting 1 (error cap 1.074), Matrix 0.9487
  (cap 1.126). No single EHM is drawn, so the printed n (12, 9) cannot be checked by counting; both groups are bar only.
- No released data file; the figure is the only source.
- The Starting bar sits at 1.0, so FOC is presumably normalized to the Starting Protocol mean (not stated).
- The x label reads 'Defined-Matrix Protocol'; the legend and record say 'Matrix Protocol'. Taken as the same group.
- The legend does not say whether the error bars are SD or SEM.

## Figures and data reader (S3c)
- Suppl. Fig. 3c read as vector (supplement p. 44): three open bars (group means) with upward error caps; no single
  EHM drawn, so bar only (countable false, printed n=4/group not checkable). No released data.
- Group order: 'Bovine collagen' heads a rule over all three bars; '+ Fibronectin' and '+ Laminin' label the middle
  and right bars, so the unlabelled left bar is taken as collagen only (matches the legend's order). It reads 1.00,
  so FOC appears normalized to the collagen-only mean (not stated).
- The fibronectin bar's error bar is very short (cap 0.015 above the mean). The legend does not say SD or SEM.

## Figures and data reader (S3d)
- Nothing to read. Suppl. Fig. 3d (supplement p. 44) is a table of semi-quantitative symbols (+ increased, o no
  change, - decreased), not a plotted panel: no axis, markers, bars or colour scale. No released data. No script, no
  figures.yaml entry and no readings were written.
- The symbols are vector text, not an image (the record note says "(image)"). All 70 cells (14 factors x 5 columns:
  Viability, CM actinin content, CM size, NM size, CM/NM ratio) were extracted by row and column position and compared
  with the record's `*_table` values: 0 mismatches.
- `figures-needed` lists all 80 S3d groups because these values name their groups under `between`, which it does not
  count as printed; the reference groups (ref_serum, ctrl_gf) only ever appear there. Every group is in fact covered by
  a printed value.

## Figures and data reader (S3e)

- No released data for Suppl. Fig. 3e; read from the vector panel (`figures/S3e.py`, supplement p. 44). Seven open bars
  (No GF, IGF, FGF, VEGF, TGFβ1 d0-10, ALL, TGFβ1 d0-3), each a mean with one upward error bar; no single EHM is drawn,
  so all groups are bar only (countable false) and no n can be counted against the legend's n.
- `matrix_ref` (Matrix Protocol EHM) is read from the black dashed line (1.00) and its 'error' from the upper of the two
  grey dashed lines (1.15; the lower is 0.85, symmetric). The legend does not say what the grey band is (SD, SEM or a
  range), nor whether the bar errors are SD or SEM.
- The legend's n string ("n=10; n=3; n=3; n=6; n=16; No GF, n=6") lists six n for seven bars, so the record's
  per-group n (igf 10, vegf 3, tgfb1 6) depends on a mapping the legend does not make explicit; tgfb1_d03 has no n.
- FGF d0-10 is drawn (≈0.31) but no item uses it; it is not stored. Tukey pairs cannot be rechecked from bars alone.

## Figures and data reader (S3f)

- No released data for Suppl. Fig. 3f; read from the vector panel (`figures/S3f.py`, supplement p. 44, crop
  [260, 655, 430, 841]). Four open bars (2% B27 0.41, 4% B27 0.72, 4% B27 -AO, 4% B27 -insulin 1.06), each a mean with
  one upward error bar; no single EHM is drawn, so all groups are bar only (countable false) and the printed n (9, 16,
  5, 6) cannot be counted.
- `matrix_ref` is read from the dark dashed line (1.00) and its 'error' from the upper grey dashed line (1.05; the
  lower mirrors it). The (e-g) legend says the dashed lines are mean (black) and SEM (grey); it does not say whether
  the bar errors are SD or SEM. (The S3e entry above says the legend does not name the grey band; it does.)
- The error-bar paths draw the cap as two collinear segments (across, then back to the centre); the script accepts
  that form.
- 4% B27 -AO is drawn but no item uses it; it is not stored. Four comparison brackets are drawn above the bars but only
  two '§' symbols, and their positions do not sit clearly over single brackets, so which pairs are significant is not
  rechecked from the drawing.

## Figures and data reader (S3g)
- Read Suppl. Fig. 3g (supplement p. 44, vector): normalized FOC of RPMI EHM and the Matrix Protocol EHM reference
  (dashed line, grey band) for S3g_rpmi_matrix. No released data; bar only (no single EHM drawn), so the printed n=9 for
  RPMI cannot be checked by count. RPMI mean 0.213 (error cap 0.276); reference 0.999 (upper band 1.134).
- The legend does not say whether the bars are SD or SEM, nor what the grey band is in this panel.
- The FOC of IMDM, αMEM and RPMI+calcium is drawn and read for bar naming only; no item uses it (S3g_calcium holds the
  bracketed calcium values, which the script checks against each bar).
- The y axis line leans ~0.1 pt; the αMEM label's α is a Symbol-font glyph (U+F061). Both handled in the script.

## Figures and data reader (S4)
- No released data for Suppl. Fig. 4; read from the vector panel b (`figures/S4.py`, supplement p. 46, crop
  [30, 60, 570, 570], which takes in the panel-a table). Nine FOC-calcium series at W4, each with 10 markers at
  0.2, 0.4, 0.8, 1.2 ... 3.2, 4.0 mmol/L (the steps are not printed; x is rounded to 0.1 from the calibrated axis).
  Each marker is a group mean with a symmetric error bar; no single EHM is drawn, so every group is bar only and the
  table's n (24, 8, 7, 3, 18, 11, 4, 10, 4) cannot be counted. 100 labels (g1_sf serves two items), 188 readings.
- Marker classes (shape x filled/half/open) are mapped to groups from the table itself (row word, column header), so
  the legend mapping is checked, not typed in. Plateau means at 4.0 mmol/L: iCell SF 1.66, H7 SF 1.60, G1 SF 1.46,
  HES2 SF 1.36; G1 Matrix 0.72, H7 Matrix 0.60, G1 Starting 0.46, HES2 Starting 0.32, iCell Matrix 0.15 mN.
- Error bars smaller than the marker are not drawn, so no error end for all of icell_matrix, nor hes2_start and
  icell_sf at 0.2 mmol/L. The legend does not say SD or SEM.
- The drawing holds leftovers of a HES2 Matrix series, which the table marks n.d.: one half-filled square at
  0.2 mmol/L (about 0.07 mN) and error-bar lines at 0.4-4.0 with no markers (centred about 0.43 mN at 4.0). The plot
  has 9 fitted curves. Not read; worth knowing that a removed series sits under the figure.
- Bar lines start at the centre of filled markers and at the edge (centre ± half the marker width) of open and half
  filled ones; where another series' line meets a marker the symmetric pair is taken. The hexagon outline is flatter
  than its marker box.
- The asterisks are per protocol pair over the whole curve (2-way ANOVA); each S4 item compares two curves, so the
  audit has a mean per calcium step, not one mean per group, and computes no direction.

## Figures and data reader (S5c)
- **S5c (S5c_mband, S5c_mlc2v, S5c_ncad; groups ehm, cm2d): not readable as numbers.** Suppl. Fig. 5c (supplement
  p. 47, lower half) is six pairs of immunostaining micrographs (myomesin, MLC2V, n-cadherin, each single channel and
  merged) for 2D CM and EHM CM, with 20 µm scale bars. The text layer holds only the panel labels. The panel has no
  axes, bars, points or colour scale, and the legend gives no n, test or score. The paper releases no data files, so
  no figures.yaml entry, script, reading or data.yaml row is written. All three items stay qualitative: M-band,
  MLC2V and intercalated-disc organisation are shown only as images (same case as F1d). The text cites this panel as
  "Supplementary Figure 4c"; see the cross-reference note above.

## Figures and data reader (F2c)
- **Fig. 2c read as raster** (author manuscript p. 20, 300 dpi; the journal version is a lower-resolution raster):
  script figures/F2c_foc_csa.py, 53 bars (means, 34 with an upper error end) of 60 markers, as <group>_<calcium>.
  No single EHM is drawn, so there are no points and no counts against the printed n (12/14/8 and 7/10/8).
- **Not read: 7 markers merged at low calcium.** HES2 all three weeks at 0.2 mM, HES2 Week 4 and Week 6 at 0.4 mM,
  hiPS-G1 Week 2 and Week 4 at 0.2 mM.
- **Series assignment.** Within a calcium column the components are assigned bottom to top (Week 2 < 4 < 6/8), since
  the curves never cross. Triangle against circle/square is checked by area; circle against square is not checked.
- **Marker centre.** The mean is the midpoint of the two SEM caps where both are clean. For squares this agrees with
  the box centre within 0.5 px. The opened triangle's box centre lies about 3 px (~0.03 mN/mm2) below the cap
  midpoint (the apex is cut). Triangles without both caps (HES2 Week 6 at 0.8 mM, hiPS-G1 Week 8 at 0.2 and
  0.4 mM) take the median offset, and its spread is added to the interval. HES2 Week 4 at 0.8 mM and hiPS-G1 Week 2
  at 4 mM have both caps fused to the marker; the midpoint of the component's flat ends gives the mean and no error
  end is read.
- **Check against text:** hiPS-G1 Week 8 at 4 mM reads 6.15 mN/mm2, upper end 6.98 (SEM about 0.83). Results print
  6.2 +/- 0.8 mN/mm2 (F2c_g1w8_infant/adult). This agrees.
- Week 2 error bars are mostly hidden inside the markers (no error end). The legend does not say SEM; Methods do.
- Figure labels for g1_w8 point to item F2c_g1_time only. F2c_g1w8_infant/adult use the same group, but their values
  are printed, so the figure is not needed for them.
- The audit cannot check either time item: the printed test is a 2-way ANOVA, and omnibus P is rechecked only for a
  one-way ANOVA.

## Figures and data reader (Suppl. Fig. 6)

- No released data for S6; all six panels read from the vector page (supplement p. 49) by `figures/S6.py`.
- (a) CM number and (b) CSA: three bars per cell line, mean and upper error end each; no single EHM drawn, so no
  points and no n. The legend does not say whether the bars are SEM or SD.
- (c) FOC against calcium: 3 series × 10 calcium steps per cell line (0.2–4 mM; steps are not printed, taken from the
  calibrated marker positions at 0.1 mM). 54 of 60 markers have an error end; six have their bar hidden inside the
  marker (HES2 Week 2 at 0.2 and 0.4 mM, HES2 Week 6 at 0.2 mM, hiPS-G1 Week 2 at 0.2 and 0.4 mM, hiPS-G1 Week 4 at
  0.2 mM). All 108 bar halves on the page meet a marker centre.
- Printed n differ between panels for the same groups: HES2 n=12/10/3 in (a), 12/10/8 in (b), 12/14/8 in (c);
  hiPS-G1 n=4/7/6 in (a), 7/10/8 in (b, c). Nothing to count against them.
- The record's S6b_g1_w8_g1_w2 per_group gives g1_w8 '8' (from panel b) — consistent with the legend; noted only
  because panel a gives 6 for the same group.

## Figures and data reader (F2d)

- No released data for Fig. 2d; read from the raster panel (author manuscript p. 20, 300 dpi) by `figures/F2d_ffr.py`.
- Groups read: sf1, sf2, sf3 (black circles) and sp3 (red square), each a mean and upper SEM end, bar only (no
  single EHM drawn, no n to count). sp1 and sp2 are drawn but are in no item, so they are not read.
- Read values agree with the Results text: sf2 118.9 (SEM 4.6) vs printed +19±5%; sf3 122.0 (SEM 5.6) vs +22±6%;
  sf1 99.9 (normalised to 100 by definition). sp3 92.2 (SEM 3.1).
- At 1 Hz the red square (sp1) lies under the black circle; the black caps (106.2 / 93.7) are separated from the red
  ones by colour, so sf1 is clean. The '*' bracket right of 3 Hz is outside the column window.
- Record note: the n=21/n=8 in the legend are per protocol, and the curves are % of each EHM's own 1 Hz force, so
  sf1 vs sf2/sf3 are within-EHM (repeated) comparisons; the item's per_group n treats them as two groups of 21.

## Figures and data reader (F3ce)

- No released data (only PDFs). Fig. 3d read from the raster panel (author manuscript p. 22, ~300 dpi) by
  `figures/F3d_hist.py`: EHM (red) and 2D D60 (blue) frequency polygons as curve samples with x; 2D D22 (grey) is
  in no item and not read. 73 EHM and 30 D60 points; EHM peak 49.7 genes, D60 peak 61.3 genes.
- The x axis 'Expression level (RPKM)' has no numeric scale, so x is the offset from the dashed 'Fetal heart' line
  in page points (1 pt steps). It is a page position, not RPKM; points carry x, so no mean or n check uses them.
- Curves are told apart by the fill on each side of a black outline. Right of the fetal line, the D60 and D22
  outlines run inside the red fill and cross at about +5 pt; past the crossing which is which is not determined
  (slope continuity suggests D60 is the steep line reaching 0 near +12 pt, but that is a judgement), so D60's
  Fetal-Adult tail is not read. Every outline inside red lies below the EHM outline right of the line.
- The legend gives no n of genes per curve; the Results text says n=346 maturation genes. Area under each curve was
  not computed, so the total is not checked against 346.
- F3e_go: Fig. 3e is a Venn diagram with gene lists; nothing about GO:0055010 is quantitative there (no enrichment
  value, fold change or P). Not readable. Its Venn counts (56/27/9) are printed values already in F3e_venn.
- F3d_hist stays *cannot check*: it has no printed value or test, and curve samples with x feed no check.

## Figures and data reader (S7)
- No released data; read from the vector page (supplement p. 51) by `figures/S7.py`: 18 genes x 7 groups = 126 bars,
  each a mean with an upper error end (119) or a mean only (7). No samples drawn: bars only, no n (printed n=3-4/group).
  No printed means to check against.
- Log y axis 'RPKM'. In the Calcium handling panel the '10^n' labels sit up to 3.5 pt off their (evenly spaced) stubs;
  the stubs are the calibration.
- Seven bars hang below 10^0 (SCN2B D22, D60, EHM serum W2; KCNJ4 D22, D60; KCNJ12 D22, D60); their error bar is
  drawn downward, so the upper end is not drawn and only the mean is stored. The upper end was not rebuilt.
- Groups are taken by slot order within each gene cluster (legend order), checked against the legend fills. Two bars
  break the fill pattern: TNNT1 EHM serum-free W6 is filled grey (0.628, the 2D D60 fill) instead of white, and SCN2B
  EHM serum W2 is an unfilled outline. Both are taken by position (judgement: a drawing slip, not a reordered cluster).
  EHM serum-free W2 and Fetal heart share one fill (0.376), so only order separates them.
- All of MYOM2 (bars and error paths) is drawn twice; one copy of its EHM serum-free W6 bar is grey, the other white.
  Duplicates are kept once.
- CKM EHM serum-free W2 has a cap with no stem (error end 0.3 pt above the bar top); taken as its error end.
- The asterisks and § brackets are not read (the record does not enumerate starred pairs).

## Figures and data reader (S8a)
- No released data; read from the vector page (supplement p. 53) by `figures/S8a.py`: 9 adrenoceptor genes x 7 groups
  = 63 slots giving 62 means and 63 upper error ends (125 readings). No samples drawn: bars only, no n
  (printed n=3-4/group). No printed means to check against.
- Log y axis 'RPKM' (10^-2 to 10^2), calibrated from the axis path's five stubs and their '10' labels with exponents.
  The axis path is as narrow as a bar (4.08 pt); it is told apart by its 6 segments (bars have 4).
- ADRB3 adult heart has no bar, only an error path standing on the 10^-2 floor: the mean is below the axis and is not
  stored; only the upper error end (about 0.0105 RPKM) is stored.
- Groups are taken by slot order within each gene cluster (legend order), with every fill checked against its legend
  swatch; all match.
- The asterisks and § brackets are not read (the record does not enumerate starred pairs). The record's item note
  calls the figure raster, but the page is vector.

## Figures and data reader (F4)

- No released data for Fig. 4; all values read from the raster figure (author manuscript p. 23, ~300 dpi) by
  `figures/F4.py` (one script for panels a, b, d, e, f; 80 readings stored).
- Panels b, d, e, f: bar only (mean = top outline, error = cap of the upward bar). No single EHM is drawn, so no
  counts against the printed n (8–10 / 4 / 3 per group) and no points-based checks.
- Panel e (stacked): the CM value is the red bar's top. The fibroblast value is the green segment's height (stack
  top minus CM top). Its error end assumes the stack's error bar is the SEM of the fibroblast segment (GraphPad
  stacked-bar convention), drawn above the stack: fib + (cap − stack top). If that bar is the SEM of the total cell
  number instead, only the size of the error changes, not the mean.
- Panel a: means only, at 1.2, 2.0, 2.4 and 2.8 mM for Control, NE 0.001, NE 0.01 and NE 0.1, where those markers
  stand apart (order and shape-area checks in the script). The NE 1 diamonds lie under the grey ET-1 stars at every
  calcium, so neither is readable. Error bars interleave and are not read. Other calcium columns merge markers
  or stacked caps. Triangle means carry +2 px uncertainty because the opening cuts off the apex. Readings carry x
  (calcium), so they do not feed the item checks.
- Groups not compared in any item (b, d, e non-asterisked bars) are linked to that panel's item for completeness.
  The control bars of d and e are repeated under "<label> for <item>" to feed each comparison item.
- Fig. 4d: the y axis starts at 0.8 (fold). Values are read from the calibrated axis, not from bar length.

## Figures and data reader (F4g)

- Fig. 4g (author manuscript p. 23, raster ~300 dpi, crop of panel g only): no released data exist for this paper
  (PDFs only), so the six compared bars were read by `figures/F4g.py`: NE in FOC, ISO, CM viability and CM size;
  NE+Phen in ISO; NE+Met in CM size. Bar only (mean, upper error end); no single EHM is drawn, so no points and no
  n to compare with the printed "n=4–10/group". The six NE+Met/NE+Phen bars not compared in any item were not read.
- Control is the dashed line (no bar, no error bar); its mean (0.9995) is the line read from the figure, repeated
  as "<x>_ctr for <item>" for each comparison item. It is 1 by normalisation, so it carries no spread.
- The raster is blurred: line rows never reach full darkness. Bar tops and caps are half-maximum upper edges moved
  down by the centre-minus-edge offset measured on the isolated caps (FOC, ISO and viability NE); +0.5 px for that.
  The CM size caps (NE, NE+Met) touch their bar tops and the ISO NE+Phen cap sits 3 px above its outline, so their
  error ends rest on edges only; error bars there are ~0.01–0.02 fold, about two to three times the interval.
- The y axis title is printed "Fold of ctontrol" [sic]. The Fig. 4g legend does not name the error type; Methods
  state data are mean ± SEM.

## Figures and data reader (S8bc)

- Suppl. Fig. 8b,c (supplement p. 53) read as vector bars, `figures/S8bc.py`: two panels, y axis 'FOC (% change)'
  calibrated from six stubs (0-100). Bar means / upper error ends (% change): hiPS-G1 start 56.85/63, matrix
  53.59/68.66, serum-free 89.66/96.07; HES2 start 37.09/40.67, matrix 25.99/31, serum-free 77.58/83.83. Each
  serum-free bar is repeated under both items of its line. No released data cover these panels.
- Bars only, no single EHM drawn: no points, no counts, so the legend n (11/20, 11/32, 15/18) cannot be checked
  against the figure, and the Tukey pairs cannot be rechecked (audit: cannot check).
- Error type is not named in the legend; only an upper error bar is drawn.
- Record concern (not edited): each panel has two nested brackets, a long one Starting–Serum-free and a shorter
  one Matrix–Serum-free under it, with a single '*' centred over the long bracket only (b: '*' at x≈177, long
  bracket centre ≈180, short ≈212; c: '*' at x≈461, long ≈464, short ≈496). The record gives '*p<0.05' to both
  sf-vs-matrix items as well; whether the one star covers both brackets is not stated. Flag to the record reader.
- n strings '(n=11/20)' etc. are read in the record as hiPS-G1/HES2 per protocol; that reading is the record's.

## Figures and data reader (S8e)

- Suppl. Fig. 8e (supplement p. 53) read as vector bars, `figures/S8e.py`: y axis 'Normalized FOC (%)' calibrated
  from seven stubs (-25 to 125); treatment of each bar read from the +/- rows under it. Bar means / error ends (%):
  isoprenaline alone 100.6/107.9, + CGP-20712A 66.26/72.12, + ICI-118551 31.88/37.89. No released data cover the panel.
- Bars only, no single EHM drawn: no points, so legend n (11, 7, 7, 5) cannot be checked against the figure and the
  CGP-vs-ICI t-test cannot be rechecked from points. The legend does not name the error type.
- The 'both blockers' bar (mean just below 0, downward error bar) belongs to no item and is not returned.
- Record concern (not edited): item S8e_adrb1 links the printed 32 ± 6 % (ADRB1 share) to iso_cgp vs iso. The figure's
  iso + ICI bar (beta2 blocked, so the beta1-mediated remainder) reads 31.88 with error end 37.89 (≈ 32 ± 6), while the
  iso + CGP bar reads 66.26 (100 - 66 ≈ 34). The 32 % appears to be the ICI bar, i.e. groups iso_ici vs iso. Flag to
  the record reader.
- Record note: the unit gives every group 'concentration: 100 nmol/L' (the isoprenaline dose); the legend gives the
  blockers as CGP 300 nmol/L and ICI 50 nmol/L.

## Figures and data reader (S10a)

- Suppl. Fig. 10a (supplement p. 57), left (Serum-free protocol) plot read as vector, `figures/S10a.py`: y axis
  '% of FOC at 1 Hz' calibrated from three stubs (50, 100, 150). Means / upper error ends at 3 Hz: Untreated
  131.9/145.2, 1 umol/L NE 97.87/102.4. No released data cover the panel.
- Markers are group means with error bars (legend does not name SD or SEM); no single EHM is drawn, so bars only and
  the legend n=4 cannot be checked against the figure.
- Only the 3 Hz groups the item compares are read; the 1 and 2 Hz points (both curves start at 100 % at 1 Hz) and the
  Starting protocol plot (no item group needed) are not returned.
- The asterisk bracket at 3 Hz joins the two serum-free curves, consistent with the item's *p<0.05.

## Figures and data reader (S10b)
- Suppl. Fig. 10b (supplement p. 57) read as a vector bar chart by `figures/S10b.py`: six bars (FOC, ISO, CM size ×
  Starting/black, Serum-free/grey), means and error caps. No released data hold these values.
- Bars are group means with one-sided error bars drawn away from zero; the legend does not say SD or SEM. No single
  EHM is drawn, so bars only (countable false) and the legend n=8 / n=11 cannot be checked against the figure.
- 'error' is the cap, the far end of the error bar: below the mean for the negative FOC and ISO bars, above it for
  CM size. It is not always the upper end.
- Read means (% change): FOC sp -46.3, sf -57.9; ISO sp -39.3, sf -57.8; CM size sp 2.4, sf 11.5. Asterisks stand
  over the serum-free ISO and CM size bars and not over FOC, matching the items' p entries.
- Record note (not edited): S10b_iso context has `measurement_calcium_mM: EC50`, which reads as a measure word, not a
  calcium concentration.

## Vocabulary agent

Vocabulary v30, instructions terms_v4. 146 values mapped or flagged in terms.yaml; the rest match by code once the edits apply.

**Judgements I was unsure of**
- `mechanical_load: mechanical load` (T1, F1b): Fig. 1a shows flexible PDMS holders (elastic, so auxotonic), but the
  supplement's Starting Protocol mentions "static or dynamic stretch devices". I did not infer auxotonic; I added
  `mechanical_load:load_regime_not_stated` with "mechanical load" as its synonym.
- Bovine collagen: the source never gives its type ("medical grade bovine collagen"), so I added
  `substrate:collagen_type_not_stated` instead of using collagen I. Rat collagen is "collagen type I from rat tails" →
  collagen I hydrogel. Source (rat tail / bovine) is the new qualifier `collagen_source`.
- "ALL growth factors" (S3e–g supplements) is mapped to IGF-1 + FGF-2 + VEGF165 + TGF-β1, as the Suppl. Fig. 3 legend
  defines ALL. The reader could write the four factors out instead.
- HES2-RFP has no Cellosaurus entry: mapped to HES-2 (CVCL_D093) with `no_ontology_term` and a split request (RFP →
  transgene). So HES2 and HES2-RFP groups have the same cell_line term and differ only in transgene.
- PDGF-BB → CHEBI:749433 *becaplermin* (recombinant human PDGF-BB). It is the same protein, but the ChEBI entry is the drug.
- No ChEBI entries for TGF-β1/β2, VEGF165, EGF, cardiotrophin-1, CGP-20712A or chick embryo extract, and the TGF inhibitor
  is unnamed: all became own terms. TGF-β1 and VEGF165 have separate own terms in supplements and treatment, because
  own ids carry their field.
- Isoprenaline response measures: I added `measure:inotropic_response` (qualifier agonist) instead of twitch force with
  `% change`, because "response to ISO (fold of control)" normalises a change, not a force. "% change in FOC" items
  therefore sit under inotropic_response.
- RPKM values were mapped to `gene_expression` with `expressed_as: normalised` and `normalised_to: RPKM`. The term's
  definition says "fold change against a reference", which RPKM is not. A separate transcript-abundance term may be better.
- Flow-cytometry size (RFP MFI, FSC, semi-quantitative grade) went to a new `measure:cell_size` (arbitrary units), apart
  from cell area or volume.
- `spontaneous frequency` (Fig. 2f, impaling electrodes) is mapped to `contraction_frequency`, although it is an
  electrical rate.
- `preparation: organ bath` and `cardiomyocytes in EHMs` → intact tissue without a synonym (a set-up, not a preparation).

**Flags**
- placeholder: cell_line "different ESC and iPSC lines" (pooled lines not named); measurement_calcium_mM "EC50" (a word in a
  quantity field; code passes it as a quantity).
- alternatives: hipsc_medium "HFF-conditioned medium or TeSR-E8"; dissociation_reagent "collagenase I and/or trypsin/EDTA".
- not a context: composition "undefined/defined cell composition" (descriptors in a quantity field); preparation
  "recorded using a camera" (a method).
- several measures: "RPKM of the 29 most abundantly expressed transcripts"; "EHM patch size" (mm and cell count).

**Possible record issues (not edited)**
- F2ab has unit-level `preparation: isolated cardiomyocyte`, but its panel B is electron microscopy of whole EHM.
- F1e "output cardiomyocyte percentage" names no marker; Fig. 1b says actinin+. I left the marker out.
- Existing keys for cell_volume, cell_viability and cell_number do not require the new `measure.cell_type` qualifier. They
  should, at the next re-map.

**Re-map at vocabulary v68 (2026-11-13)**
- Another paper has since added "viability" as a synonym of `measure:cell_viability`, so code now matches S3d_viab. I removed
  the stored mapping (same term; the qualifier-free mapping is unchanged). I had refused that synonym at v30 as broader
  than cell viability; a tissue-viability term (`measure:tissue_viability`) now exists, so the bare word can mislead.
- I checked terms added since v30 under the parents my mappings use. None is a clear refinement: the benchmark pacing
  ("1 Hz", "~1.5 Hz") states no stimulus type, EHM condensation is an image, not a compaction %, and normalised forces stay
  `twitch_force` + `expressed_as` (the brief forbids `relative_*` measures, though `measure:relative_twitch_force` now
  exists in the vocabulary). Edits were not re-reviewed one by one; the gate accepts them against v68.

## Formula agent

**Where the spec or gate left me guessing**
- S8e_adrb1 (32±6% "mediated via ADRB1"): the paper does not say which antagonist the share comes from. I wrote two
  derivations: CGP-sensitive share `(E - Ec)/E` (the record pairs iso_cgp with iso) and ICI-resistant share `Ei/E`.
  Code: CGP 34.2% is inconsistent with 32, ICI 31.7% is consistent. The `alternatives` field is not run by chains.py, so a
  second derivation with the same output was the only way to get the alternative checked.
- F2c_g1w8 (6.2 mN/mm² "average maximal FOC"): I took FOC at 4 mmol/L calcium (where the week-8 curve peaks) over the
  week-8 CSA. Means of the Suppl. Fig. 6 readings give 5.94 (inconsistent). Per-EHM values are not available, so the
  mean of per-EHM ratios cannot be run. Fig. 2c's own reading at 4 mmol/L is 6.15. The gap is plausibly ratio of means
  vs mean of ratios; code cannot tell them apart.
- TXT1_aspect (7.6): rebuilt as length/width from the printed means (92/13 = 7.08; inconsistent). The same caveat applies
  (per-cell ratios), and length and width carry no n of their own.
- Derivations with no printed output (F2c per group, the normalised/fold/% change items) give rebuilt values or nothing.
  Code does not compare a rebuilt value with the item's own readings (e.g. the Fig. 2c reading at 4 mmol/L). If it did,
  the six per-group FOC/CSA rebuilds would check Fig. 2c against Suppl. Fig. 6b/c. Rebuilt vs Fig. 2c reading:
  hes2 w2 0.90/0.91, w4 2.23/2.00, w6 3.45/3.43; g1 w2 0.67/0.77, w4 2.74/2.88, w8 5.94/6.15.
- F1e_ratio (~1:1 output CM:fibroblast): this needed a new entry, `ratio_from_fraction` (r = f/(1 - f), derived from
  part_of_whole and ratio_def). It assumes every non-myocyte is a fibroblast. Until the entry is applied, the library
  verdict is "cannot check".
- Not written as derivations: counted percentages (F1c, F1e_cmpct, S1e, S2c/d, S9a). Their counts are never reported, so
  each is a measurement, not a chain. Bounds were added where a value is printed (S9a, S8e_adrb1, R² values).
- The F4d and F4g "fold" and the F4b "% change" come from raster axis labels the readers recorded; the legends do not
  name the operation. I anchored the legend wording.
- No assumption reports: no derivation uses a model. How CSA was measured is not stated (circular or elliptical area
  model unknown); qPCR 2^-ddCt is listed as a labelled alternative for S2a only.

**Observations for code (not verdicts)**
- 218 + 128 + 431 = 777: the three trajectory clusters account exactly for the cardiomyocyte transcriptome.
