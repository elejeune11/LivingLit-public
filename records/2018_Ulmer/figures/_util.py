"""Helpers for 2018_Ulmer's figures (this paper's alone).

All figures in this paper are raster images (main text embedded at 300 dpi,
supplement at ~200 dpi). Tick labels are part of the image, so each script states
the printed tick values and code finds the tick marks they belong to; every bar
top and error-bar end is located by code. Pixel coordinates are of the crop
rendered at DPI.
"""
from __future__ import annotations

import numpy as np

from livinglit.figures.source import RASTER_UNCERTAINTY_PX_300DPI, calibrate

DPI = 300


def grey(img):
    return img.astype(int).mean(axis=2)


def nonwhite(img, thr=232):
    return img.astype(int).min(axis=2) < thr


def darkpx(img, thr=120):
    return grey(img) < thr


def y_axis(img, box, thr=120, min_len=40):
    """The y axis in box (x0, y0, x1, y1): the leftmost column holding a long vertical dark run.
    Returns (col, top, bottom) of that run, col = rightmost column of the axis stroke."""
    x0, y0, x1, y1 = box
    d = darkpx(img, thr)[y0:y1, x0:x1]
    best = []
    for c in range(d.shape[1]):
        col = d[:, c]
        run, start, longest = 0, 0, (0, 0, 0)
        for r, v in enumerate(col):
            if v:
                if run == 0:
                    start = r
                run += 1
                if run > longest[0]:
                    longest = (run, start, r)
            else:
                run = 0
        best.append(longest)
    lens = np.array([b[0] for b in best])
    if lens.max() < min_len:
        raise ValueError("no y axis found")
    cands = np.where(lens >= 0.8 * lens.max())[0]
    c = int(cands[0])
    while c + 1 < len(lens) and lens[c + 1] >= 0.8 * lens.max():  # axis stroke can be 2-3 px wide
        c += 1
    L, s, e = best[c]
    return x0 + c, y0 + s, y0 + e


def ticks(img, axis_col, top, bottom, near=2, far=4, frac=0.35, pad=4):
    """Tick marks left of the y axis, found from a darkness profile of the columns near..far pixels left of
    the axis stroke (a window that only major ticks reach selects majors). Returns tick centres (rows,
    darkness-weighted, sub-pixel), top to bottom."""
    dark = 255.0 - grey(img)
    span = slice(top, bottom)
    ref = dark[span, axis_col].mean()
    left = axis_col
    while left - 1 >= 0 and dark[span, left - 1].mean() > 0.4 * ref:
        left -= 1
    prof = dark[:, max(0, left - far):left - near + 1].mean(axis=1)
    r0, r1 = max(0, top - pad), min(len(prof), bottom + pad + 1)
    seg = prof[r0:r1]
    if seg.max() <= 0:
        raise ValueError("no ticks found")
    on = seg > frac * seg.max()
    out = []
    for a, b in runs(on):
        w = seg[a:b + 1]
        out.append(r0 + float((np.arange(a, b + 1) * w).sum() / w.sum()))
    if not out:
        raise ValueError("no ticks found")
    return out


def majors_from_minor_gaps(img, axis_col, top, bottom, base, thr=120):
    """For axes drawn with minor ticks only, the major ticks left as gaps: the axis top, the middle of
    each gap (a spacing about twice the minor spacing) and the baseline, top to bottom."""
    rows = ticks(img, axis_col, top, bottom, near=2, far=3)
    diffs = np.diff(rows)
    sp = float(np.median(diffs))
    out = [float(top)]
    for a, b, dd in zip(rows[:-1], rows[1:], diffs):
        if dd > 1.5 * sp:
            out.append((a + b) / 2)
    out.append(float(base))
    return out


def cal_from_ticks(rows, values):
    """Calibration from major tick rows (top to bottom) and the printed values (top to bottom)."""
    if len(rows) != len(values):
        raise ValueError(f"found {len(rows)} major ticks for {len(values)} printed labels")
    return calibrate(list(zip(rows, values)))


def unc_px(native_dpi=300, render_dpi=DPI):
    """Raster uncertainty in rendered pixels: 0.6 px at 300 dpi, i.e. 0.6 pixels of an image embedded at
    300 dpi; an image embedded at a lower resolution gets 0.6 of its own pixels."""
    return RASTER_UNCERTAINTY_PX_300DPI * (300.0 / native_dpi) * (render_dpi / 300.0)


def triple(cal, pos, native_dpi=300):
    """[value, lo, hi] at row pos, interval = raster uncertainty plus calibration misfit."""
    v = cal.value(pos)
    lo, hi = cal.interval(pos, unc_px(native_dpi))
    return [v, min(lo, v) - cal.residual, max(hi, v) + cal.residual]


def runs(mask_row, start=0, min_w=1, merge_gap=0):
    """Runs of True in a 1-D mask: [(a, b)] inclusive, offset by start."""
    out = []
    a = None
    for i, v in enumerate(mask_row):
        if v and a is None:
            a = i
        elif not v and a is not None:
            out.append([a, i - 1])
            a = None
    if a is not None:
        out.append([a, len(mask_row) - 1])
    merged = []
    for r in out:
        if merged and r[0] - merged[-1][1] - 1 <= merge_gap:
            merged[-1][1] = r[1]
        else:
            merged.append(r)
    return [(start + a, start + b) for a, b in merged if b - a + 1 >= min_w]


def bars_at_row(img, row, x0, x1, thr=232, min_w=8, merge_gap=0, band=None):
    """Bars crossing a row just above the baseline: runs of non-white columns. With band, a column counts
    when any pixel in the band rows above that row is non-white (hatched bars)."""
    if band:
        m = nonwhite(img, thr)[row - band:row + 1, x0:x1].any(axis=0)
    else:
        m = nonwhite(img, thr)[row, x0:x1]
    rr = runs(m, x0, 1, merge_gap)
    out, i = [], 0
    while i < len(rr):
        a, b = rr[i]
        if b - a + 1 <= 7 and i + 1 < len(rr) and rr[i + 1][1] - rr[i + 1][0] + 1 <= 7:
            out.append((a, rr[i + 1][1]))  # an outlined (white) bar: its two side strokes
            i += 2
            continue
        if b - a + 1 >= min_w:
            out.append((a, b))
        i += 1
    return out


def bar_top(img, bx0, bx1, base_row, thr=232, inset=1):
    """Top of a bar: climb from the baseline along a column just inside the left edge while pixels are
    non-white. A filled bar's value is its top edge; an outlined bar's (white inside) is the middle of its
    top stroke."""
    m = nonwhite(img, thr)
    c = bx0 + inset
    r = base_row
    while r - 1 >= 0 and m[r - 1, c]:
        r -= 1
    # an outlined bar (white inside): its value is the middle of the top stroke
    q = bx0 + (bx1 - bx0) // 4
    t = 0
    while r + t < base_row and m[r + t, q]:
        t += 1
    if r + t < base_row - 2:
        return r + t / 2.0
    return float(r)


def error_top(img, bx0, bx1, top_row, thr=200, max_gap=2, cap_min=4):
    """Upper end of an error bar drawn from the bar top: climb the bar's centre column (±1 px)
    through non-white pixels, allowing small gaps; the end is the centre of the cap stroke.
    Returns None when nothing rises above the bar."""
    m = grey(img) < thr
    cx = (bx0 + bx1) // 2
    cols = slice(max(0, cx - 1), cx + 2)
    r = int(top_row) - 1
    last = None
    gap = 0
    while r >= 0:
        if m[r, cols].any():
            last = r
            gap = 0
        else:
            gap += 1
            if gap > max_gap:
                break
        r -= 1
    if last is None or int(top_row) - last < 3:
        return None
    # cap stroke: rows from the top where the dark run around the centre is wider than the whisker
    def width(rr):
        row = m[rr]
        if not row[cx]:
            return 0
        a = cx
        while a - 1 >= 0 and row[a - 1]:
            a -= 1
        b = cx
        while b + 1 < len(row) and row[b + 1]:
            b += 1
        return b - a + 1
    whisker = width((last + int(top_row)) // 2)
    cap = []
    for rr in range(last, int(top_row)):
        if width(rr) >= max(cap_min, whisker + 3):
            cap.append(rr)
        elif cap:
            break
    if cap:
        return float(np.mean(cap)) + 0.5
    return float(last) + 0.5


def find_baseline(img, axis_col, bottom, thr=120, search=12):
    """The x axis row near the axis bottom: the row with the longest dark run to the right of the axis."""
    d = darkpx(img, thr)
    best, br = -1, bottom
    for r in range(max(0, bottom - search), min(d.shape[0], bottom + search)):
        c, n = axis_col + 1, 0
        while c < d.shape[1] and d[r, c]:
            n += 1
            c += 1
        if n > best:
            best, br = n, r
    # top row of the baseline stroke, antialiased rows included
    g = grey(img)
    while br - 1 >= 0 and g[br - 1, axis_col + 5] < 200:
        br -= 1
    return br


def baseline_centre(img, axis_col, base):
    g = grey(img)
    t = 0
    while base + t < g.shape[0] and g[base + t, axis_col + 5] < 200:
        t += 1
    return base + (t - 1) / 2.0


def panel(img, box, values, thr=120, stroke=6, gaps=False, tick_win=(2, 4), zero_at_base=False, top_at_end=False):
    """Axis, calibration and baseline of one plot inside box (gaps: majors left as gaps among minor ticks)."""
    col, top, bottom = y_axis(img, box, thr)
    base = find_baseline(img, col, bottom, thr)
    if gaps:
        rows = majors_from_minor_gaps(img, col, top, bottom, base, thr)
    else:
        rows = ticks(img, col, top, bottom, *tick_win)
        if zero_at_base and values[-1] == 0:  # the 0 tick hidden in the x axis: the baseline's centre
            bc = baseline_centre(img, col, base)
            rows = [r for r in rows if abs(r - bc) > 3] + [bc]
        if top_at_end:  # the top tick not drawn: the axis line's top end
            rows = [float(top)] + [r for r in rows if abs(r - top) > 3]
    cal = cal_from_ticks(rows, values)
    return col, top, bottom, base, cal


def read_bars(img, box, values, labels, native_dpi=300, thr=120, bar_thr=232, row_off=2, min_w=8, merge_gap=0,
              err_thr=200, x_end=None, expect=None, gaps=False, tick_win=(2, 4), band=None, zero_at_base=False,
              top_at_end=False):
    """Bars of one plot: {label: {"points": [], "countable": False, "bar": {...}}} for labels in left-to-right order.
    A label of None skips that bar."""
    col, top, bottom, base, cal = panel(img, box, values, thr, gaps=gaps, tick_win=tick_win, zero_at_base=zero_at_base,
                                        top_at_end=top_at_end)
    x1 = x_end if x_end is not None else box[2]
    bars = bars_at_row(img, base - row_off, col + 4, x1, bar_thr, min_w, merge_gap, band)
    n = expect if expect is not None else len(labels)
    if len(bars) != n:
        raise ValueError(f"found {len(bars)} bars, expected {n}: {bars}")
    out = {}
    for lab, (a, b) in zip(labels, bars):
        if lab is None:
            continue
        t = bar_top(img, a, b, base - row_off, bar_thr)
        g = {"points": [], "countable": False, "bar": {"mean": triple(cal, t, native_dpi)}}
        e = error_top(img, a, b, t, err_thr)
        if e is not None:
            g["bar"]["error"] = triple(cal, e, native_dpi)
        out[lab] = g
    return out


def alias(groups, names):
    """The same bar read once and listed under a second label, for a bar that several evidence items share
    (figures.yaml links each label to one item)."""
    for new, old in names.items():
        groups[new] = groups[old]
    return groups
