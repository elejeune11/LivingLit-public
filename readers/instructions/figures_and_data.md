# Figures and data reader (v5 rebuild) · instructions `figures_v6`

You are the FIGURES-AND-DATA READER for one paper (spec: `docs/minimalist_design/02-audit.md`, *Reading figures* and
*Readings and data are stored as a checked cache*). The record reader wrote `records/<paper>/record.yaml`. You add the numbers
behind its evidence items: values from released data (`data.yaml`) and values read from figures by code you write
(`figures.yaml`, `figures/*.py`, `readings.yaml`). Every audit reruns all of it; a stored value that does not come back exactly
fails.

Repo: the current directory (the repository root). Commands: `uv run python -m livinglit <cmd>`.

## Every data table is used
Every data or table file the record lists (.xlsx, .xls, .xlsb, .csv, .docx) must feed values: write `data.yaml` rows for every group value it holds for the record's items (`livinglit cells` reads .xlsx, .xls, .xlsb and .csv), or, if it holds none, add it to the record's `source.not_used` with what it holds. Your gate fails on a data or table file that does neither.

## One figure per job, points only
The runner gives you one figure unit (`--figure`), chosen by `livinglit figures-needed <paper>`: the item groups listed there
are the only ones no printed text, table or released data gives, and whose test a check can verify from individual points.
No check uses a mean and error bar read from a bar, so figures are read only for their individual points.

1. **Tables and data first.** If a table (main text or supplement: PDF, .docx, .xlsx) or a released data file gives the
   listed groups' values, write `data.yaml` rows for data files, or report the table so the record can be corrected; write
   no script.
2. **Points or nothing.** Look at the figure. If it plots no individual points for the listed groups (bars, box plots or
   means with error bars only), write `no_points: {<unit>: "<what it shows instead>"}` in `figures.yaml`, write no script,
   and stop. This takes a minute, not a job.
3. Otherwise read the individual points (and the means and error bars beside them) with one script, its readings and a
   report.

## Never
- Open `archive/`, `docs/archive/`, `docs/minimalist_design/examples/`, other papers' records, `papers_dont_ever_commit/_benchmark/`.
- Write page images, crops, overlays or extracted text into the repo or the papers folder. A render you look at goes in
  `/tmp/livinglit_<paper>/` and is deleted when you finish. Values judged by eye are never results.
- Put figure-specific code in `src/livinglit/` (a test guards this). Helpers go in `records/<paper>/figures/_util.py`.
- Edit `record.yaml` (note record problems in the ambiguity log instead).

## Read first
- The two spec sections; `src/livinglit/models.py` (`FigureEntry`, `GroupLink`, `Reading`, `DataValue`);
  `src/livinglit/figures/run.py` (what `read(fig)` returns); `src/livinglit/figures/source.py` (FigureSource: `drawings()`, `words()`,
  `markers()`, `tick_marks()`, `render(dpi)`, `to_page()`; `calibrate()`, `point()`, `colour_mask()`, `dark_mask()`, `blobs()`).
- Your paper's `record.yaml`: units, groups, items and the groups each item involves.

## 1. Released data first
For each item whose numbers are in the paper's data files (.xlsx, .csv), write rows in `records/<paper>/data.yaml`:
`{item, group, kind: point|mean|sd|sem|n|p, x (optional: dose, frequency, time as printed), file, sheet, cell, value, unit}`.
`value` is exactly what the cell holds (list with `uv run python -m livinglit cells <paper> <file> "<sheet>" A1:H40`; copy the
right side of `=` exactly). `group` is a group id of the item's unit. One row per cell. Use data for every item it covers before
reading any figure. A cell that looks wrong (68 among values 0.9–3.9; a unit slip) is kept as it is and marked
`suspect: {why}`; code runs every mean, direction and check with and without it. Never drop or correct a cell. A generator script under `/tmp/livinglit_<paper>/` (your own folder: other agents run at the same time) is fine; the rows are the product.

## 2. Figures for items whose points are not in data
Cover **every quantitative panel an evidence item rests on** that has no released data (points, bars, box plots, curves,
heat maps with a colour bar). For each panel:
- Find page and crop (PDF points: x0, top, x1, bottom) with PyMuPDF; look at a render in /tmp if needed.
- Write `records/<paper>/figures/<name>.py` defining `read(fig)` (fig is a FigureSource of the crop). Calibrate the axis from
  tick labels (`fig.tick_marks`, `calibrate`), locate markers (vector objects first: `fig.drawings()`/`fig.markers()`; raster
  masks and blobs only if the panel is an image), and return
  `{"groups": {label: {"points": [point(cal, pos, unc, at, x=...)...], "countable": bool,
  "bar": {"mean": [v, lo, hi], "error": [upper_end, lo, hi]}}}}`. Intervals: 0.5 pt (vector) or 0.6 px at 300 dpi (raster)
  plus the calibration misfit. `error` is the upper end of the error bar in axis units. Points on a curve carry `x`.
- Raster counts are used only when every marker stands alone; otherwise return the bar only and set `countable: false`
  (no points). Box plots give median/q1/q3. Bars without points give no n.
- Add the entry to `records/<paper>/figures.yaml`: `figures: {<name>: {file, page, crop, script: figures/<name>.py, unit,
  kind: vector|raster|heat map, groups: {<label>: {item, group, unit_of_value}}, note}}`. `unit_of_value` is the axis unit as
  printed ("mN", "% of baseline", "ms"); labels equal the labels `read()` returns.
- `uv run python -m livinglit figure <paper> <name>` prints what the script reads (check counts against the legend's n and
  means against printed values); `--store` writes its rows into `readings.yaml`. Never adjust a reading to make a check pass. A reading that looks wrong
  (a marker that may be a stray symbol) may be marked `suspect: {why}` in `readings.yaml` after storing.

## Gate (code)
`uv run python -m livinglit gate figures <paper>` until GATE PASSES (it reruns every script and re-reads every data cell).
Then `uv run python -m livinglit audit <paper>` shows the statuses your numbers enable.

## Ambiguity log
Append `## Figures and data reader` to `records/<paper>/ambiguity_log.md`: panels read; panels not readable and why; counted
points vs printed n; data groups vs figure groups; anything the shared parts could not do.

## Report back (under 120 words)
Data rows (items covered), figures read (vector/raster, points), panels not readable, mismatches found, gate result.
