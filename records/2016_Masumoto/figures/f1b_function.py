"""Fig. 1b: maximum capture rate (Hz), relaxation time (msec) and excitation threshold (V/cm), three bar charts in a
raster image.

Each chart has its own y axis, calibrated on its own tick marks (printed labels bottom to top: 0-6 Hz step 1;
0-250 msec step 50; 0-2 V/cm step 0.5). Bars are found by fill colour (maroon, red, green); left to right they are
CM+EC, CM+MC, CM+EC+MC (printed under each bar). The error bar is drawn upward only; its cap is the dark line above
each bar. Bars only: no individual points are drawn, so nothing is countable.
"""
import numpy as np

from livinglit.figures.source import RASTER_UNCERTAINTY_PX_300DPI, calibrate

DPI = 300
# measure, axis-line search columns, bar columns (px at 300 dpi within the crop), tick values bottom to top, fill
CHARTS = [
    ("mcr", (90, 115), (105, 440), [0, 1, 2, 3, 4, 5, 6], (152, 48, 88)),
    ("rt", (455, 475), (468, 790), [0, 50, 100, 150, 200, 250], (232, 48, 40)),
    ("et", (825, 845), (838, 1085), [0, 0.5, 1, 1.5, 2], (144, 192, 56)),
]
GROUPS = ["ce", "cm", "cem"]  # bar order left to right, as printed under the bars


def _gray(img):
    a = img.astype(int)
    return (a.max(2) - a.min(2) < 40) & (a.mean(2) < 120)


def _fill(img, rgb, tol=45):
    return np.abs(img.astype(int) - np.array(rgb)).max(2) <= tol


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


def _axis(gray, x0, x1):
    """The y-axis line: the longest vertical dark run in the search columns; its left column and row extent."""
    best = (None, 0, 0)
    for x in range(x0, x1):
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
    """Tick centres (px rows): dark runs left of the axis line, within the axis extent. The column right next to the
    line is skipped: in the first chart it is grey all along from anti-aliasing."""
    rows = np.where(gray[top - 3:bottom + 3, left - 3:left - 1].any(1))[0] + top - 3
    return [_centre(dark, r, [left - 3, left - 2]) for r in _runs(rows) if 2 <= len(r) <= 6]


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
    for measure, (a0, a1), (x0, x1), tick_values, rgb in CHARTS:
        left, top, bottom = _axis(gray, a0, a1)
        ticks = _ticks(gray, dark, left, top, bottom)
        if len(ticks) != len(tick_values):
            raise ValueError(f"{measure}: found {len(ticks)} ticks, expected {len(tick_values)}")
        ticks_pt = [fig.to_page(0, y, scale)[1] for y in sorted(ticks, reverse=True)]
        cal = calibrate(list(zip(ticks_pt, tick_values)))
        unc = unc_px / scale + cal.residual / abs(cal.slope)
        m = _fill(img[:, x0:x1], rgb)
        m[:top - 6] = False
        m[bottom + 3:] = False
        cols = np.where(m.sum(0) >= 4)[0]
        runs = [r for r in _runs(cols) if len(r) >= 15]
        if len(runs) != len(GROUPS):
            raise ValueError(f"{measure}: expected {len(GROUPS)} bars, found {len(runs)}")
        for grp, run in zip(GROUPS, runs):
            c0, c1 = run[0] + x0, run[-1] + x0
            # columns clear of the error-bar stem (white 4 rows above the fill)
            core = [c for c in range(c0 + 3, c1 - 2) if inten[np.where(m[:, c - x0])[0].min() - 4, c] > 230]
            top_px = float(np.median([_top_edge(inten, c, int(np.where(m[:, c - x0])[0].min())) for c in core]))
            # error cap: rows above the bar where the dark line spans at least a quarter of the bar width
            width = c1 - c0 + 1
            above = gray[:int(top_px), c0:c1 + 1].sum(1)
            cap_rows = [r for r in _runs(np.where(above >= width / 4)[0]) if r[-1] < top_px and r[0] > top - 6]
            if not cap_rows:
                raise ValueError(f"{measure} {grp}: no error cap")
            cap = cap_rows[-1]  # the nearest above the bar (significance lines lie higher, above the axis top)
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
            groups[f"{measure}_{grp}"] = {"points": [], "countable": False, "bar": vals}
        # the CM+EC+MC bar is one group of two items (vs CM+EC and vs CM+MC); a label links to one item, so the same
        # reading is returned again under a second label
        groups[f"{measure}_cem_vs_cm"] = groups[f"{measure}_cem"]
    return {"groups": groups}
