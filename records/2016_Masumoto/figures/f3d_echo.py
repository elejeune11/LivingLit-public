"""Fig. 3d: echocardiography of Tx and sham rats at PreTx, Tx2w and Tx4w, four line charts in one raster image.

Panels (quadrants of the crop): cardiac output (mL/min, ticks 0-200 step 50) top left, stroke volume (fold increase
to PreTx, ticks 0.6-1.4 step 0.2) top right, LVAd (mm2, ticks 0-120 step 20) bottom left, ejection fraction (fold
increase to PreTx, ticks 0.5-1.3 step 0.2) bottom right. Each panel's y axis is calibrated on its tick marks (short dark
runs left of the axis line; the bottom tick is the x axis' left overhang). The three categories are centred between
the x-axis tick marks (the y axis is the first boundary). Two coloured lines (blue Sham, red Tx, as in the legend)
join the group means; no markers or points are drawn, so nothing is countable.

Each mean is the vertex of its line at a category centre: every line segment between two centres is fitted as a
straight line (column centroids of its colour mask, columns near the error-bar stems and columns where the other line
is within 2 px left out) and evaluated at the centres it joins. An inner vertex takes the mean of the two segments'
values; their half-difference and the fits' standard errors are added to the raster uncertainty and the calibration
misfit.

Error bars: in cardiac output, stroke volume and ejection fraction the Tx bars point up and the Sham bars down from a
shared stem; the upper end of each Tx bar (the topmost cap above the Tx mean) is read. Sham bars show only their lower
end, which is not a reading kind, so no Sham error is returned. In LVAd the lines cross and the caps cannot be told
apart, so no error is returned. Stroke volume and ejection fraction are 1 at PreTx by construction and have no bar
there.

Labels: <measure>_<group>_<pre|2w|4w> carry x = day of the echo after implantation as printed in Fig. 3a (-1, 14, 28)
and link to the time-course item; <measure>_<group> repeat the Tx4w reading without x and link to the 4-week
comparison.
"""
import numpy as np

from livinglit.figures.source import RASTER_UNCERTAINTY_PX_300DPI, calibrate

DPI = 300
PANELS = {  # quadrant (row, col): measure, tick values bottom to top, Tx error bars read
    (0, 0): ("co", [0, 50, 100, 150, 200], True),
    (0, 1): ("sv", [0.6, 0.8, 1.0, 1.2, 1.4], True),
    (1, 0): ("lvad", [0, 20, 40, 60, 80, 100, 120], False),
    (1, 1): ("ef", [0.5, 0.7, 0.9, 1.1, 1.3], True),
}
TIMES = [("pre", -1), ("2w", 14), ("4w", 28)]  # days after implantation of the echo (Fig. 3a)


def _masks(img):
    a = img.astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    sat = a.max(2) - a.min(2)
    gray = (sat < 50) & (a.mean(2) < 140)
    red = (sat >= 50) & (r > g + 40) & (r > b + 40)
    blue = (sat >= 50) & (b > r + 30) & (b > g)
    return gray, red, blue


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


def _longest(line):
    return max(_runs(np.where(line)[0]), key=len, default=[])


def _centre(dark, rows, cols):
    """Darkness-weighted centre (px, pixel centres at r + 0.5) of a horizontal line over rows (one past each end)."""
    rr = np.arange(rows[0] - 1, rows[-1] + 2)
    w = dark[rr][:, cols].sum(1)
    return float((w * (rr + 0.5)).sum() / w.sum())


def _centre_x(dark, cols, rows):
    """Darkness-weighted centre (px) of a vertical line over cols (one past each end)."""
    cc = np.arange(cols[0] - 1, cols[-1] + 2)
    w = dark[rows][:, cc].sum(0)
    return float((w * (cc + 0.5)).sum() / w.sum())


def _fit(mask, other, cols, rows):
    """Straight line through the centroid of the one mask run per column (rows limited); returns fit function."""
    xs, ys = [], []
    for c in cols:
        runs = [r for r in _runs(np.where(mask[rows[0]:rows[1], c])[0] + rows[0]) if 2 <= len(r) <= 9]
        if len(runs) != 1:
            continue
        r = runs[0]
        if other[max(r[0] - 2, 0):r[-1] + 3, c].any():
            continue  # touches the other line: its edge may be hidden
        xs.append(c + 0.5)
        ys.append((r[0] + r[-1] + 1) / 2)
    if len(xs) < 10:
        raise ValueError(f"only {len(xs)} clean columns to fit a segment")
    xs, ys = np.array(xs), np.array(ys)
    A = np.vstack([xs, np.ones_like(xs)]).T
    coef, *_ = np.linalg.lstsq(A, ys, rcond=None)
    s2 = float(((ys - A @ coef) ** 2).sum() / (len(xs) - 2))
    cov = s2 * np.linalg.inv(A.T @ A)

    def at(x):
        v = np.array([x, 1.0])
        return float(v @ coef), float(np.sqrt(v @ cov @ v))
    return at


def _panel(fig, scale, gray, red, blue, dark, y0, y1, x0, x1, ticks_v, read_err, measure):
    sub = gray[y0:y1, x0:x1]
    # y axis: the longest vertical dark line in the left third; x axis: the longest horizontal dark line
    best = max(((c, _longest(sub[:, c])) for c in range(sub.shape[1] // 3)), key=lambda t: len(t[1]))
    axis_rows = (best[1][0] + y0, best[1][-1] + y0)
    ax_cols = [c + x0 for c in range(sub.shape[1] // 3) if len(_longest(sub[:, c])) >= len(best[1]) - 5]
    ax_left = min(ax_cols)
    besth = max(((r, _longest(sub[r, :])) for r in range(sub.shape[0])), key=lambda t: len(t[1]))
    xax_rows = [r + y0 for r in range(sub.shape[0]) if len(_longest(sub[r, :])) >= len(besth[1]) - 5]
    xax_bottom, xax_top = max(xax_rows), min(xax_rows)
    xax_right = besth[1][-1] + x0

    # y ticks: rows dark across the 4 columns just left of the axis line
    tick_cols = list(range(ax_left - 5, ax_left - 1))
    rows = np.where(gray[axis_rows[0] - 3:axis_rows[1] + 3, tick_cols].all(1))[0] + axis_rows[0] - 3
    ticks = [_centre(dark, r, tick_cols) for r in _runs(rows) if 2 <= len(r) <= 6]
    if len(ticks) != len(ticks_v):
        raise ValueError(f"{measure}: found {len(ticks)} y ticks, expected {len(ticks_v)}")
    ticks_pt = [fig.to_page(0, y, scale)[1] for y in sorted(ticks, reverse=True)]
    cal = calibrate(list(zip(ticks_pt, ticks_v)))

    # x ticks: columns dark over the 4 rows just below the x axis, right of the y axis
    xrows = list(range(xax_bottom + 2, xax_bottom + 6))
    cols = np.where(gray[xrows][:, max(ax_cols) + 3:xax_right + 1].all(0))[0] + max(ax_cols) + 3
    xt = [_centre_x(dark, r, xrows) for r in _runs(cols) if 2 <= len(r) <= 6]
    bounds = [float(np.mean(ax_cols)) + 0.5] + xt
    if len(bounds) != 4:
        raise ValueError(f"{measure}: found {len(xt)} x ticks, expected 3")
    centres = [(bounds[i] + bounds[i + 1]) / 2 for i in range(3)]

    unc_base = RASTER_UNCERTAINTY_PX_300DPI / scale + cal.residual / abs(cal.slope)
    plot_rows = (axis_rows[0] - 3, xax_top - 1)

    def value(xpx, ypx, extra_px=0.0):
        ypt = fig.to_page(xpx, ypx, scale)[1]
        v = cal.value(ypt)
        lo, hi = cal.interval(ypt, unc_base + extra_px / scale)
        return [v, min(lo, v), max(hi, v)]

    means = {}
    for g, mask, other in (("tx", red, blue), ("sham", blue, red)):
        segs = [_fit(mask, other, range(int(centres[i]) + 8, int(centres[i + 1]) - 8), plot_rows) for i in range(2)]
        ends = [[segs[0](centres[0])], [segs[0](centres[1]), segs[1](centres[1])], [segs[1](centres[2])]]
        means[g] = []
        for i, vals in enumerate(ends):
            ys = [v for v, _ in vals]
            y = float(np.mean(ys))
            extra = max(se for _, se in vals) + (max(ys) - min(ys)) / 2
            means[g].append((y, extra))

    groups = {}
    for g in ("tx", "sham"):
        for i, (t, day) in enumerate(TIMES):
            y, extra = means[g][i]
            groups[f"{measure}_{g}_{t}"] = {"points": [], "countable": False,
                                            "bar": {"mean": value(centres[i], y, extra), "x": day}}

    if read_err:
        for i, (t, _) in enumerate(TIMES):
            c = centres[i]
            c0, c1 = int(c) - 12, int(c) + 12
            ytx = means["tx"][i][0]
            rows = np.where(gray[plot_rows[0]:int(ytx) - 3, c0:c1].sum(1) >= 12)[0] + plot_rows[0]
            caps = _runs(rows)
            if not caps:
                continue  # no bar (PreTx of a fold-change panel)
            cap = caps[0]  # topmost
            cap_cols = [k for k in range(c0, c1) if gray[cap[0]:cap[-1] + 1, k].any() and abs(k + 0.5 - c) > 3]
            groups[f"{measure}_tx_{t}"]["bar"]["error"] = value(c, _centre(dark, cap, cap_cols))

    for g in ("tx", "sham"):  # the Tx4w readings again, without x, for the 4-week comparison
        b = groups[f"{measure}_{g}_4w"]["bar"]
        groups[f"{measure}_{g}"] = {"points": [], "countable": False,
                                    "bar": {k: v for k, v in b.items() if k != "x"}}
    return groups


def read(fig):
    img, scale = fig.render(DPI)
    gray, red, blue = _masks(img)
    dark = 255.0 - img.astype(float).mean(2)
    h, w = gray.shape
    groups = {}
    for (r, c), (measure, ticks_v, read_err) in PANELS.items():
        y0, y1 = (0, h // 2) if r == 0 else (h // 2, h)
        x0, x1 = (0, w // 2) if c == 0 else (w // 2, w)
        groups.update(_panel(fig, scale, gray, red, blue, dark, y0, y1, x0, x1, ticks_v, read_err, measure))
    return {"groups": groups}
