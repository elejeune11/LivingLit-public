"""Supplementary Fig. 2b: flow cytometry proportions (%) of CM, EC and MC after Dkk1, control or Wnt3a, three bar charts.

The charts sit side by side (CM, EC, MC), each with its own y axis (printed ticks 0-70 by 10, 0-30 by 5, 0-100 by 20)
and calibrated on its own tick marks. Each chart has four bars, left to right Dkk1 100ng/mL, Control, Wnt3a 50ng/mL,
Wnt3a 100ng/mL; bars are found as coloured (saturated) fill, the only colour in the crop. The error bar is the dark cap
above each bar. In the two near-zero MC bars the cap lies just above the fill and is narrower than the bar, so the fill
top is read in the bar columns clear of the cap (as in every bar). Bars only: no individual points, nothing countable.
Each bar serves several items, so it is returned under every label linked to it (see LINKS).
"""
import numpy as np

from livinglit.figures.source import RASTER_UNCERTAINTY_PX_300DPI, calibrate

DPI = 300
# chart column ranges (px at 300 dpi within the crop), the cell type each shows and its printed ticks, bottom to top
CHARTS = [("cm", 0, 470, [0, 10, 20, 30, 40, 50, 60, 70]),
          ("ec", 470, 960, [0, 5, 10, 15, 20, 25, 30]),
          ("mc", 960, 1467, [0, 20, 40, 60, 80, 100])]
BARS = ["dkk1", "ctrl", "w50", "w100"]  # left to right, as labelled under each chart
# label -> group whose bar it returns; labels beyond <cell>_<group> link the same bar to a further item
LINKS = {
    "cm": {"cm_w100": "w100", "cm_dkk1": "dkk1", "cm_w50": "w50", "cm_dkk1_vs_w50": "dkk1",
           "cm_w100_vs_ctrl": "w100", "cm_ctrl": "ctrl"},
    "ec": {"ec_w100": "w100", "ec_dkk1": "dkk1", "ec_w50": "w50", "ec_dkk1_vs_w50": "dkk1",
           "ec_w100_vs_ctrl": "w100", "ec_ctrl": "ctrl"},
    "mc": {"mc_w100": "w100", "mc_dkk1": "dkk1", "mc_w50": "w50", "mc_dkk1_vs_w50": "dkk1",
           "mc_w100_vs_ctrl": "w100", "mc_ctrl": "ctrl", "mc_w50_vs_ctrl": "w50", "mc_ctrl_vs_w50": "ctrl"},
}


def _gray(img):
    a = img.astype(int)
    return (a.max(2) - a.min(2) < 40) & (a.mean(2) < 120)


def _fill(img):
    """Coloured pixels: the bar fills (red, blue, green); text, axes and error bars are black or gray."""
    a = img.astype(int)
    return a.max(2) - a.min(2) > 60


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


def _axis(gray, c0, c1):
    """The y-axis line: the longest vertical dark run in the chart's columns; returns its left column and row extent."""
    best = (None, 0, 0)
    for x in range(c0, c1):
        for r in _runs(np.where(gray[:, x])[0]):
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
    return [_centre(dark, r, [left - 2, left - 1]) for r in _runs(rows) if 2 <= len(r) <= 7]


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
    fill = _fill(img)
    inten = img.astype(float).mean(2)
    dark = 255.0 - inten
    unc_px = RASTER_UNCERTAINTY_PX_300DPI  # rendered at 300 dpi
    groups = {}
    for cell, k0, k1, tick_values in CHARTS:
        left, top, bottom = _axis(gray, k0, k1)
        ticks = _ticks(gray, dark, left, top, bottom)
        if len(ticks) != len(tick_values):
            raise ValueError(f"{cell}: found {len(ticks)} ticks, expected {len(tick_values)}")
        ticks_pt = [fig.to_page(0, y, scale)[1] for y in sorted(ticks, reverse=True)]
        cal = calibrate(list(zip(ticks_pt, tick_values)))
        unc = unc_px / scale + cal.residual / abs(cal.slope)
        m = fill.copy()
        m[:, :max(k0, left + 3)] = False  # only this chart's plot area
        m[:, k1:] = False
        m[bottom + 3:] = False
        # the two near-zero MC bars show only two fully coloured rows between the cap and the axis line
        runs = [r for r in _runs(np.where(m.sum(0) >= 2)[0]) if len(r) >= 15]
        if len(runs) != len(BARS):
            raise ValueError(f"{cell}: expected {len(BARS)} bars, found {len(runs)}")
        bars = {}
        for grp, run in zip(BARS, runs):
            c0, c1 = run[0], run[-1]
            # error cap: the lowest run of rows above the fill where the dark line spans at least a quarter of the bar
            # width (significance lines lie higher and span several bars)
            fill_top = int(min(np.where(m[:, c])[0].min() for c in range(c0, c1 + 1)))
            width = c1 - c0 + 1
            above = gray[:fill_top + 1, c0:c1 + 1].sum(1)
            cap_rows = [r for r in _runs(np.where(above >= width / 4)[0]) if r[0] > top - 6]
            if not cap_rows:
                raise ValueError(f"{cell} {grp}: no error cap")
            cap = cap_rows[-1]
            cap_cols = np.where(gray[cap[0]:cap[-1] + 1, c0:c1 + 1].any(0))[0] + c0
            # bar columns clear of the cap and stem (white 4 rows above the fill top); in the near-zero MC bars these are
            # only the two or three columns at one edge of the bar
            core = [c for c in range(c0 + 1, c1)
                    if inten[np.where(m[:, c])[0].min() - 4, c] > 230 and c not in set(cap_cols)]
            if len(core) < 2:
                raise ValueError(f"{cell} {grp}: no bar columns clear of the error bar")
            top_px = float(np.median([_top_edge(inten, c, int(np.where(m[:, c])[0].min())) for c in core]))
            stem = set(np.where(gray[cap[-1] + 3, c0:c1 + 1])[0] + c0) if cap[-1] + 3 < top_px else set()
            ends = [c for c in cap_cols if not ({c - 1, c, c + 1} & stem)] or list(cap_cols)
            cap_y = _centre(dark, cap, ends)
            xc = (c0 + c1 + 1) / 2
            vals = {}
            for kind, y in (("mean", top_px), ("error", cap_y)):
                ypt = fig.to_page(xc, y, scale)[1]
                v = cal.value(ypt)
                lo, hi = cal.interval(ypt, unc)
                vals[kind] = [v, min(lo, v), max(hi, v)]
            bars[grp] = vals
        for label, grp in LINKS[cell].items():
            groups[label] = {"points": [], "countable": False, "bar": bars[grp]}
    return {"groups": groups}
