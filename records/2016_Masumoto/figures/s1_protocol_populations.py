"""Supplementary Fig. 1 (right): flow cytometry proportions (%) of CM, EC and MC per protocol, three bar charts in a raster.

The charts are stacked top to bottom (CM+EC, CM+MC, MC protocol), each with its own y axis (printed ticks 0-80 by 20,
0-60 by 20, 0-100 by 20) and calibrated on its own tick marks. Bars are found by fill colour (CM red, EC blue, MC dark
green); the error bar is the dark cap above each bar. Only the bars the record needs from the figure are read (CM+EC
values are printed in the text). Bars only: no individual points are drawn, so nothing is countable.
"""
import numpy as np

from livinglit.figures.source import RASTER_UNCERTAINTY_PX_300DPI, calibrate

DPI = 300
# chart row ranges (px at 300 dpi within the crop), the protocol each shows and its printed ticks, bottom to top
CHARTS = [("ce", 0, 420, [0, 20, 40, 60, 80]),
          ("cmmc", 420, 1000, [0, 20, 40, 60]),
          ("mc", 1000, 1551, [0, 20, 40, 60, 80, 100])]
FILLS = {"CM": (237, 52, 47), "EC": (0, 163, 222), "MC": (38, 95, 55)}
# read: CM+MC CM and MC bars, MC-protocol CM bar. Not read: CM+MC EC (no bar drawn); MC-protocol EC (only a cap on the
# axis line, no fill to find); MC-protocol MC and all CM+EC bars (printed in the text)
READ = {("cmmc", "CM"), ("cmmc", "MC"), ("mc", "CM")}
# the MC-protocol CM bar is one or two fill rows tall, cut in two by the error-bar stem
MIN_ROWS = {("mc", "CM"): 1}
STEM_GAP = 8  # px: fill runs this close are one bar split by the stem


def _gray(img):
    a = img.astype(int)
    return (a.max(2) - a.min(2) < 40) & (a.mean(2) < 120)


def _fill(img, rgb, tol=45):
    """Pixels near the fill colour and coloured (not the gray error-bar stems, which sit within tol of dark green)."""
    a = img.astype(int)
    return (np.abs(a - np.array(rgb)).max(2) <= tol) & (a.max(2) - a.min(2) > 30)


def _runs(idx):
    out, cur = [], []
    for i in idx:
        if cur and i != cur[-1] + 1:
            out.append(cur)
            cur = []
        cur.append(int(i))
    if cur:
        out.append(cur)
    return out


def _axis(gray, r0, r1):
    """Column of the y-axis line: the longest vertical dark run in the chart rows; returns its left column and row extent."""
    best = (None, 0, 0)
    for x in range(gray.shape[1] // 2):
        for r in _runs(np.where(gray[r0:r1, x])[0] + r0):
            if len(r) > best[1]:
                best = (x, len(r), r[0])
    x, n, top = best
    left = x
    while gray[top + n // 2, left - 1]:
        left -= 1
    return left, top, top + n


def _centre(dark, rows, cols):
    """Darkness-weighted centre (px, pixel centres at r + 0.5) of a horizontal line over rows (one past each end)."""
    rr = np.arange(rows[0] - 1, rows[-1] + 2)
    w = dark[rr][:, cols].sum(1)
    return float((w * (rr + 0.5)).sum() / w.sum())


def _ticks(gray, dark, left, top, bottom):
    """Tick centres (px rows): dark runs just left of the axis line, within the axis extent."""
    rows = np.where(gray[top - 3:bottom + 3, left - 2:left].any(1))[0] + top - 3
    return [_centre(dark, r, [left - 2, left - 1]) for r in _runs(rows) if 2 <= len(r) <= 6]


def _top_edge(inten, col, t):
    """Sub-pixel top edge of a bar in one column: where intensity crosses halfway from white to the bar edge."""
    level = (255.0 + inten[t, col]) / 2
    r = t - 1
    while inten[r, col] <= level:
        r -= 1
    return (r + 0.5) + (inten[r, col] - level) / (inten[r, col] - inten[r + 1, col])


def read(fig):
    img, scale = fig.render(DPI)
    gray = _gray(img)
    inten = img.astype(float).mean(2)
    dark = 255.0 - inten
    unc_px = RASTER_UNCERTAINTY_PX_300DPI  # rendered at 300 dpi
    groups = {}
    for prot, r0, r1, tick_values in CHARTS:
        left, top, bottom = _axis(gray, r0, r1)
        ticks = _ticks(gray, dark, left, top, bottom)
        if len(ticks) != len(tick_values):
            raise ValueError(f"{prot}: found {len(ticks)} ticks, expected {len(tick_values)}")
        ticks_pt = [fig.to_page(0, y, scale)[1] for y in sorted(ticks, reverse=True)]
        cal = calibrate(list(zip(ticks_pt, tick_values)))
        unc = unc_px / scale + cal.residual / abs(cal.slope)
        for cell, rgb in FILLS.items():
            if (prot, cell) not in READ:
                continue
            m = _fill(img, rgb)
            m[:top - 6] = False  # only this chart's plot area
            m[bottom + 3:] = False
            m[:, :left + 3] = False
            cols = np.where(m.sum(0) >= MIN_ROWS.get((prot, cell), 4))[0]
            runs = []
            for r in _runs(cols):
                if runs and r[0] - runs[-1][-1] <= STEM_GAP:
                    runs[-1] = runs[-1] + r
                else:
                    runs.append(r)
            runs = [r for r in runs if len(r) >= 15]
            if len(runs) != 1:
                raise ValueError(f"{prot} {cell}: expected one bar, found {len(runs)}")
            c0, c1 = runs[0][0], runs[0][-1]
            # columns clear of the error-bar stem (white 4 rows above the fill)
            core = [c for c in range(c0 + 3, c1 - 2) if m[:, c].any() and inten[np.where(m[:, c])[0].min() - 4, c] > 230]
            top_px = float(np.median([_top_edge(inten, c, int(np.where(m[:, c])[0].min())) for c in core]))
            # error cap: rows above the bar where the dark line spans at least a quarter of the bar width
            width = c1 - c0 + 1
            above = gray[:int(top_px), c0:c1 + 1].sum(1)
            cap_rows = [r for r in _runs(np.where(above >= width / 4)[0]) if r[-1] < top_px and r[0] > top - 6]
            if not cap_rows:
                raise ValueError(f"{prot} {cell}: no error cap")
            cap = cap_rows[0]
            cap_cols = np.where(gray[cap[0]:cap[-1] + 1, c0:c1 + 1].any(0))[0] + c0
            stem = set(np.where(gray[cap[-1] + 3, c0:c1 + 1])[0] + c0)
            ends = [c for c in cap_cols if not ({c - 1, c, c + 1} & stem)] or list(cap_cols)
            cap_y = _centre(dark, cap, ends)
            xc = (c0 + c1 + 1) / 2
            vals = {}
            for kind, y in (("mean", top_px), ("error", cap_y)):
                ypt = fig.to_page(xc, y, scale)[1]
                v = cal.value(ypt)
                lo, hi = cal.interval(ypt, unc)
                vals[kind] = [v, min(lo, v), max(hi, v)]
            groups[f"{prot}_{cell}"] = {"points": [], "countable": False, "bar": vals}
    return {"groups": groups}
