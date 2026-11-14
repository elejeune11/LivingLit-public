"""2021_Tsan helpers: raster scatter-with-mean-and-error-bar panels (GraphPad style, black on white).

Used only by this paper's figure scripts. Finds the y axis and its tick marks, the x tick of
each group, the group's mean line (the widest horizontal bar, several rows thick) and the caps
at the ends of the vertical error bar line. Markers overlap, so no points are returned.
"""
from __future__ import annotations

import numpy as np

from livinglit.figures.source import calibrate, dark_mask, RASTER_UNCERTAINTY_PX_300DPI

DPI = 300


def _runs(flags):
    """Centres of consecutive True runs: [(start, end)]."""
    out, start = [], None
    for i, f in enumerate(flags):
        if f and start is None:
            start = i
        if not f and start is not None:
            out.append((start, i - 1))
            start = None
    if start is not None:
        out.append((start, len(flags) - 1))
    return out


def axes(m):
    """y axis column band, x axis row band (long dark lines)."""
    H, W = m.shape
    cols = [x for x in range(W) if m[:, x].sum() > 0.6 * H]
    rows = [y for y in range(H) if m[y, :].sum() > 0.6 * W]
    return (min(cols), max(cols)), (min(rows), max(rows))


def y_ticks(m, ax_col, tick_len=(8, 16)):
    """Row centres of tick marks drawn left of the y axis."""
    strip = m[:, ax_col[0] - tick_len[1]:ax_col[0] - 1]
    return [(a + b) / 2 for a, b in _runs(strip.sum(1) >= tick_len[0])]


def x_ticks(m, ax_row, tick_len=(8, 16)):
    strip = m[ax_row[1] + 2:ax_row[1] + tick_len[1], :]
    return [(a + b) / 2 for a, b in _runs(strip.sum(0) >= tick_len[0])]


def run_at(m, y, x):
    """Left and right extent of the dark horizontal run through (x, y)."""
    if not m[y, x]:
        return 0, 0
    l = x
    while l > 0 and m[y, l - 1]:
        l -= 1
    r = x
    while r < m.shape[1] - 1 and m[y, r + 1]:
        r += 1
    return x - l, r - x


def group_bar(m, cx, top, bottom, mean_half=(28, 30), cap_half=(13, 26), band=4):
    """Mean row and the two cap rows of one group, in px.

    Mean: the first band of >= band rows whose run through the line column reaches mean_half on both sides.
    Caps: following the vertical error bar line up and down from the mean, the last row band whose run is
    cap-shaped (both halves within cap_half) before the line ends.
    """
    c = int(round(cx))
    cols = [c - 1, c, c + 1]
    line = int(max(cols, key=lambda x: m[top:bottom, x].sum()))
    full = [all(v >= h for v, h in zip(run_at(m, y, line), mean_half)) for y in range(m.shape[0])]
    bands = [(a, b) for a, b in _runs(full) if b - a + 1 >= band and top <= a and b <= bottom]
    if len(bands) != 1:
        raise ValueError(f"group at x={cx}: {len(bands)} mean-line bands")
    ma, mb = bands[0]
    mean_y = (ma + mb) / 2

    def cap(direction):
        """Walk the error bar line away from the mean; the cap is the farthest band of cap-shaped rows on it."""
        def capped(y):
            l, r = run_at(m, y, line)
            return cap_half[0] <= l <= cap_half[1] and cap_half[0] <= r <= cap_half[1]
        y = ma - 1 if direction < 0 else mb + 1
        hits = []
        while top <= y <= bottom and m[y, line]:
            if capped(y):
                hits.append(y)
            y += direction
        if not hits:
            raise ValueError(f"group at x={cx}: no cap {'above' if direction < 0 else 'below'}")
        far = hits[-1]
        ys = [h for h in hits if abs(h - far) <= 4]
        return (min(ys) + max(ys)) / 2

    return mean_y, cap(-1), cap(1)


def read_scatter(fig, groups, tick_values, unc_px=RASTER_UNCERTAINTY_PX_300DPI, **kw):
    """groups: labels left to right; tick_values: y tick values bottom to top. Bar mean and upper error end."""
    img, scale = fig.render(DPI)
    m = dark_mask(img, 128)
    ax_col, ax_row = axes(m)
    yt = sorted(y_ticks(m, ax_col), reverse=True)
    if len(yt) != len(tick_values):
        raise ValueError(f"found {len(yt)} y ticks, expected {len(tick_values)}")
    cal = calibrate(list(zip(yt, tick_values)))
    xt = x_ticks(m, ax_row)
    if len(xt) != len(groups):
        raise ValueError(f"found {len(xt)} x ticks, expected {len(groups)}")
    err = unc_px + abs(cal.residual / cal.slope) if cal.slope else unc_px
    out = {}
    for label, cx in zip(groups, xt):
        mean_y, up_y, lo_y = group_bar(m, cx, int(yt[-1]) + 3, ax_row[0] - 1, **kw)

        def val(y):
            v = cal.value(y)
            a, b = cal.interval(y, err)
            return [v, min(a, v), max(b, v)]

        out[label] = {"points": [], "countable": False,
                      "bar": {"mean": val(mean_y), "error": val(up_y)},
                      "_lower": val(lo_y)[0], "_at": fig.to_page(cx, mean_y, scale)}
    return out
