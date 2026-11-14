"""Fig. 1c: active force (fold increase over 2 Hz) against pacing frequency, a line chart in a raster image.

The y axis is calibrated on its seven tick marks (printed labels bottom to top: 0-1.2 step 0.2). Three coloured lines
(blue CM+EC, green CM+MC, red CM+EC+MC, as in the legend) join the group means at 2, 2.5, 3 and 3.5 Hz; no markers are
drawn. Only the 3.5 Hz means are read (the items compare groups there). The 3.5 Hz category is the x of the black
error-bar stem at the right end of the lines; the 3 Hz stem bounds the last line segment on the left. Each line's centre
is fitted as a straight line over that segment (column centroids of its colour mask) and evaluated at the 3.5 Hz stem.
Blue runs under green where they meet, so only blue columns clear of green are fitted. Intervals add the fit's standard
error at 3.5 Hz to the raster uncertainty and the calibration misfit.

Error bars: CM+EC+MC has an upward bar whose cap is read (upper end). The CM+EC and CM+MC bars are drawn downward on one
shared stem with two caps; which cap belongs to which group cannot be told, so no error is returned for them. Means only:
no individual points are drawn, so nothing is countable.
"""
import numpy as np

from livinglit.figures.source import RASTER_UNCERTAINTY_PX_300DPI, calibrate

DPI = 300
TICK_VALUES = [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2]  # bottom to top
X_35HZ = 3.5


def _masks(img):
    a = img.astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    sat = a.max(2) - a.min(2)
    gray = (sat < 50) & (a.mean(2) < 140)
    red = (sat >= 50) & (r > g + 40) & (r > b + 40)
    green = (sat >= 50) & (g > r) & (g > b + 30)
    blue = (sat >= 50) & (b > r + 20) & (b > g)
    return gray, red, green, blue


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


def _vertical_lines(gray, min_len):
    """Columns holding a vertical dark run of at least min_len px, grouped; (centre x px, top row, bottom row) each."""
    cols = []
    for x in range(gray.shape[1]):
        best = max((r for r in _runs(np.where(gray[:, x])[0])), key=len, default=[])
        if len(best) >= min_len:
            cols.append((x, best[0], best[-1]))
    out = []
    for grp in _runs([c[0] for c in cols]):
        sel = [c for c in cols if c[0] in grp]
        out.append(((grp[0] + grp[-1] + 1) / 2, min(c[1] for c in sel), max(c[2] for c in sel)))
    return out


def _centre(dark, rows, cols):
    """Darkness-weighted centre (px, pixel centres at r + 0.5) of a horizontal line over rows (one past each end)."""
    rr = np.arange(rows[0] - 1, rows[-1] + 2)
    w = dark[rr][:, cols].sum(1)
    return float((w * (rr + 0.5)).sum() / w.sum())


def _fit_end(mask, cols, x_end, clear=None):
    """Fit a straight line to the centroid of the one mask run in each column; value and standard error at x_end."""
    xs, ys = [], []
    for c in cols:
        runs = [r for r in _runs(np.where(mask[:, c])[0]) if 2 <= len(r) <= 9]
        if len(runs) != 1:
            continue
        r = runs[0]
        if clear is not None and clear[max(r[0] - 2, 0):r[-1] + 3, c].any():
            continue  # touches the other line: its edge may be hidden
        xs.append(c + 0.5)
        ys.append((r[0] + r[-1] + 1) / 2)
    if len(xs) < 10:
        raise ValueError(f"only {len(xs)} clean columns to fit a line")
    xs, ys = np.array(xs), np.array(ys)
    A = np.vstack([xs, np.ones_like(xs)]).T
    coef, *_ = np.linalg.lstsq(A, ys, rcond=None)
    resid = ys - A @ coef
    s2 = float((resid ** 2).sum() / (len(xs) - 2))
    cov = s2 * np.linalg.inv(A.T @ A)
    v = np.array([x_end, 1.0])
    return float(v @ coef), float(np.sqrt(v @ cov @ v))


def read(fig):
    img, scale = fig.render(DPI)
    gray, red, green, blue = _masks(img)
    dark = 255.0 - img.astype(float).mean(2)

    # y axis: the longest vertical dark line in the left third; ticks are short dark runs just left of it
    left_third = gray[:, : gray.shape[1] // 3]
    axis = max(_vertical_lines(left_third, 200), key=lambda a: a[2] - a[1])
    ax_left, mid = int(axis[0]), (axis[1] + axis[2]) // 2
    while gray[mid, ax_left - 1]:
        ax_left -= 1
    tick_cols = list(range(ax_left - 5, ax_left - 1))
    tick_rows = np.where(gray[axis[1] - 3:axis[2] + 3, tick_cols].all(1))[0] + axis[1] - 3
    ticks = [_centre(dark, r, tick_cols) for r in _runs(tick_rows) if 2 <= len(r) <= 6]
    if len(ticks) != len(TICK_VALUES):
        raise ValueError(f"found {len(ticks)} y ticks, expected {len(TICK_VALUES)}")
    ticks_pt = [fig.to_page(0, y, scale)[1] for y in sorted(ticks, reverse=True)]
    cal = calibrate(list(zip(ticks_pt, TICK_VALUES)))

    # error-bar stems right of the axis. 3.5 Hz: a long stem (>= 60 px) where the red line ends (red just left of it;
    # the other long vertical is the significance bracket). 3 Hz: the nearest vertical run (>= 30 px) left of it; the
    # 3 Hz stem is broken by the lines, so it is shorter. Shorter runs are legend letters.
    off = int(axis[0]) + 10

    def verticals(min_len):
        return [(x + off, t, b) for x, t, b in _vertical_lines(gray[:, off:], min_len)
                if t > axis[1] - 3 and b < axis[2] - 5]

    ends = [s for s in verticals(60)
            if red[:, int(s[0]) - 8:int(s[0]) - 2].any() and not red[:, int(s[0]) + 3:int(s[0]) + 9].any()]
    if len(ends) != 1:
        raise ValueError(f"expected one 3.5 Hz stem, found {len(ends)}")
    x35 = ends[0][0]
    x3 = max(s[0] for s in verticals(30) if s[0] < x35 - 20)
    seg = range(int(x3) + 8, int(x35) - 5)

    unc_base = RASTER_UNCERTAINTY_PX_300DPI / scale + cal.residual / abs(cal.slope)

    def bar_value(y_px, extra_px=0.0):
        ypt = fig.to_page(x35, y_px, scale)[1]
        v = cal.value(ypt)
        lo, hi = cal.interval(ypt, unc_base + extra_px / scale)
        return [v, min(lo, v), max(hi, v)]

    groups = {}
    for label, mask, clear in (("ce", blue, green), ("cm", green, None), ("cem", red, None)):
        y, se = _fit_end(mask, seg, x35, clear)
        groups[label] = {"points": [], "countable": False, "bar": {"mean": bar_value(y, se), "x": X_35HZ}}

    # CM+EC+MC error cap: the dark horizontal run on the 3.5 Hz stem above the red mean
    red_px, _ = _fit_end(red, seg, x35)
    c0, c1 = int(x35) - 12, int(x35) + 12
    rows = np.where(gray[: int(red_px) - 3, c0:c1].sum(1) >= 12)[0]
    caps = [r for r in _runs(rows) if r[0] > axis[1] - 3]
    if not caps:
        raise ValueError("no CM+EC+MC error cap above the 3.5 Hz mean")
    cap = caps[-1]
    cap_cols = [c for c in range(c0, c1) if gray[cap[0]:cap[-1] + 1, c].any() and abs(c + 0.5 - x35) > 3]
    groups["cem"]["bar"]["error"] = bar_value(_centre(dark, cap, cap_cols))

    # the CM+EC+MC mean is one group of two items (vs CM+EC and vs CM+MC); a label links to one item, so the same
    # reading is returned again under a second label
    groups["cem_vs_cm"] = groups["cem"]
    return {"groups": groups}
