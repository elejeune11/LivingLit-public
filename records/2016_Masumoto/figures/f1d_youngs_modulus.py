"""Fig. 1d: Young's modulus (kPa), one bar chart in a raster image.

The y axis is calibrated on its four tick marks (printed labels bottom to top: 0, 5, 10, 15 kPa). Bars are found by
their orange fill; left to right they are CM+EC, CM+MC, CM+EC+MC (printed under each bar). The error bar is drawn
upward only; its cap is the dark line above each bar. Bars only: no individual points are drawn, so nothing is
countable.
"""
import numpy as np

from livinglit.figures.source import RASTER_UNCERTAINTY_PX_300DPI, calibrate

DPI = 300
TICK_VALUES = [0, 5, 10, 15]  # bottom to top
FILL = (250, 147, 46)  # orange
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


def _axis(gray):
    """The y-axis line: the longest vertical dark run in the left half; its left column and row extent."""
    best = (None, 0, 0)
    for x in range(gray.shape[1] // 2):
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
    """Tick centres (px rows): dark runs two to three columns left of the axis line, within the axis extent."""
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
    left, top, bottom = _axis(gray)
    ticks = _ticks(gray, dark, left, top, bottom)
    if len(ticks) != len(TICK_VALUES):
        raise ValueError(f"found {len(ticks)} ticks, expected {len(TICK_VALUES)}")
    ticks_pt = [fig.to_page(0, y, scale)[1] for y in sorted(ticks, reverse=True)]
    cal = calibrate(list(zip(ticks_pt, TICK_VALUES)))
    unc = RASTER_UNCERTAINTY_PX_300DPI / scale + cal.residual / abs(cal.slope)

    x0 = left + 5
    m = _fill(img[:, x0:], FILL)
    m[:top - 6] = False
    m[bottom + 3:] = False
    runs = [r for r in _runs(np.where(m.sum(0) >= 4)[0]) if len(r) >= 15]
    if len(runs) != len(GROUPS):
        raise ValueError(f"expected {len(GROUPS)} bars, found {len(runs)}")
    groups = {}
    for grp, run in zip(GROUPS, runs):
        c0, c1 = run[0] + x0, run[-1] + x0
        # columns clear of the error-bar stem (white 4 rows above the fill)
        core = [c for c in range(c0 + 3, c1 - 2) if inten[np.where(m[:, c - x0])[0].min() - 4, c] > 230]
        top_px = float(np.median([_top_edge(inten, c, int(np.where(m[:, c - x0])[0].min())) for c in core]))
        # error cap: rows above the bar where the dark line spans at least a quarter of the bar width; the nearest
        # one above the bar (significance brackets lie higher)
        width = c1 - c0 + 1
        above = gray[:int(top_px), c0:c1 + 1].sum(1)
        cap_rows = [r for r in _runs(np.where(above >= width / 4)[0]) if r[-1] < top_px and r[0] > 1]
        if not cap_rows:
            raise ValueError(f"{grp}: no error cap")
        cap = cap_rows[-1]
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
        groups[grp] = {"points": [], "countable": False, "bar": vals}
    # the CM+EC bar is one group of two items (CM+MC vs CM+EC, CM+EC+MC vs CM+EC); a label links to one item, so the
    # same reading is returned again under a second label
    groups["ce_vs_cem"] = groups["ce"]
    return {"groups": groups}
