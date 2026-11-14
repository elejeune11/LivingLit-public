"""Supplementary Fig. 4b: ECT area (mm2) during pre-culture, a line chart in a raster image.

The y axis is calibrated on its seven tick marks (printed labels bottom to top: 0-120 step 20). Two coloured lines (blue
CM+EC, red CM+EC+MC, as in the legend) join the group means at Day 0, 2, 4, 6 and 14; no markers are drawn. Only the
Day 14 means are read (the item compares the groups there). The Day 14 category is the x of the black error-bar stem at
the right end of the lines (the long vertical further right is the *** bracket); the Day 6 stem bounds the last line
segment on the left. Each line's centre is fitted as a straight line over that segment (column centroids of its colour
mask, columns where the two lines touch skipped) and evaluated at the Day 14 stem. Intervals add the fit's standard error
there to the raster uncertainty and the calibration misfit.

Error bars: the Day 14 stem is shared and carries two caps, one above both lines and one below both. As at Days 2, 4 and
6, the upper series (CM+EC) is drawn with its bar upward and the lower (CM+EC+MC) downward, so the upper cap is read as
the upper end of the CM+EC bar. The lower cap is a lower end only, not a reading kind, so CM+EC+MC gets no error. Means
only: no individual points are drawn, so nothing is countable.
"""
import numpy as np

from livinglit.figures.source import RASTER_UNCERTAINTY_PX_300DPI, calibrate

DPI = 300
TICK_VALUES = [0, 20, 40, 60, 80, 100, 120]  # bottom to top
X_DAY14 = 14


def _masks(img):
    a = img.astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    sat = a.max(2) - a.min(2)
    gray = (sat < 50) & (a.mean(2) < 140)
    red = (sat >= 50) & (r > g + 40) & (r > b + 40)
    blue = (sat >= 50) & (b > r + 20) & (b > g)
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


def _fit_end(mask, cols, x_end, clear):
    """Fit a straight line to the centroid of the one mask run in each column; value and standard error at x_end."""
    xs, ys = [], []
    for c in cols:
        runs = [r for r in _runs(np.where(mask[:, c])[0]) if 2 <= len(r) <= 9]
        if len(runs) != 1:
            continue
        r = runs[0]
        if clear[max(r[0] - 2, 0):r[-1] + 3, c].any():
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
    gray, red, blue = _masks(img)
    dark = 255.0 - img.astype(float).mean(2)

    # y axis: the longest vertical dark line in the left third; ticks are short dark runs just left of it
    left_third = gray[:, : gray.shape[1] // 3]
    axis = max(_vertical_lines(left_third, 200), key=lambda a: a[2] - a[1])
    ax_left, mid = int(axis[0]), (axis[1] + axis[2]) // 2
    while gray[mid, ax_left - 1]:
        ax_left -= 1
    tick_cols = list(range(ax_left - 5, ax_left - 1))
    tick_rows = np.where(gray[axis[1] - 3:axis[2] + 3, tick_cols].all(1))[0] + axis[1] - 3
    ticks = [_centre(dark, r, tick_cols) for r in _runs(tick_rows) if 2 <= len(r) <= 8]
    if len(ticks) != len(TICK_VALUES):
        raise ValueError(f"found {len(ticks)} y ticks, expected {len(TICK_VALUES)}")
    ticks_pt = [fig.to_page(0, y, scale)[1] for y in sorted(ticks, reverse=True)]
    cal = calibrate(list(zip(ticks_pt, TICK_VALUES)))

    # error-bar stems: columns with a long dark run within WINDOW px of the red line (legend letters, the *** and the
    # bracket share columns with the stems but lie outside that window, or beyond the line's end). Where the stem hides
    # the line, the line row of the nearest column showing it is used. Day 14 is the rightmost stem, Day 6 the next.
    window = 60
    red_row = {}
    for c in range(int(axis[0]) + 10, gray.shape[1]):
        runs = [r for r in _runs(np.where(red[axis[1]:axis[2], c])[0] + axis[1]) if 2 <= len(r) <= 9]
        if len(runs) == 1:
            red_row[c] = (runs[0][0] + runs[0][-1]) // 2
    known = np.array(sorted(red_row))
    line_end = int(known.max())
    stem_cols = []
    for c in range(int(axis[0]) + 10, line_end + 8):
        row = red_row[int(known[np.argmin(abs(known - c))])]
        band = gray[row - window:row + window, c]
        if len(band) and max((len(r) for r in _runs(np.where(band)[0])), default=0) >= 12:
            stem_cols.append(c)
    stems = []
    for grp in _runs(stem_cols):
        if len(grp) <= 8:  # a stem is a few px wide; caps are wide but only a few rows tall, so they fail the run test
            row = red_row[int(known[np.argmin(abs(known - grp[0]))])]
            sub = gray[row - window:row + window, grp[0]:grp[-1] + 1].any(1)
            r = max(_runs(np.where(sub)[0]), key=len)
            stems.append(((grp[0] + grp[-1] + 1) / 2, row - window + r[0], row - window + r[-1]))
    if len(stems) < 2:
        raise ValueError(f"found {len(stems)} error-bar stems, expected at least two")
    x14, stem_top, stem_bottom = stems[-1]
    x6 = stems[-2][0]
    if line_end > x14 + 3:
        raise ValueError("the red line runs past the last stem")
    # clear of the error caps (about 18 px either side of each stem at 300 dpi)
    seg = range(int(x6) + 25, int(x14) - 22)

    unc_base = RASTER_UNCERTAINTY_PX_300DPI / scale + cal.residual / abs(cal.slope)

    def value(y_px, extra_px=0.0):
        ypt = fig.to_page(x14, y_px, scale)[1]
        v = cal.value(ypt)
        lo, hi = cal.interval(ypt, unc_base + extra_px / scale)
        return [v, min(lo, v), max(hi, v)]

    groups = {}
    fits = {}
    for label, mask, clear in (("ce", blue, red), ("cem", red, blue)):
        y, se = _fit_end(mask, seg, x14, clear)
        fits[label] = y
        groups[label] = {"points": [], "countable": False, "bar": {"mean": value(y, se), "x": X_DAY14}}
    if not fits["ce"] < fits["cem"]:
        raise ValueError("CM+EC line is not above CM+EC+MC at Day 14; cap assignment would not hold")

    # caps: dark horizontal runs across the Day 14 stem; the one above the CM+EC (upper) line is its upper end
    c0, c1 = int(x14) - 12, int(x14) + 12
    rows = np.where(gray[stem_top - 3:int(fits["ce"]) - 3, c0:c1].sum(1) >= 12)[0] + stem_top - 3
    caps = _runs(rows)
    if len(caps) != 1:
        raise ValueError(f"expected one cap above the CM+EC Day 14 mean, found {len(caps)}")
    cap = caps[0]
    cap_cols = [c for c in range(c0, c1) if gray[cap[0]:cap[-1] + 1, c].any() and abs(c + 0.5 - x14) > 3]
    groups["ce"]["bar"]["error"] = value(_centre(dark, cap, cap_cols))
    return {"groups": groups}
