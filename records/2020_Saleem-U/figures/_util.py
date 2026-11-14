"""Helpers for this paper's raster scatter/mean-line panels (2020_Saleem-U only).

All panels in this paper are embedded raster images. Tick labels are inside the
image, so axes are calibrated from the tick marks located by pixel (short dark
horizontal strokes left of the y-axis line); each script states the printed tick
values it assigns, top to bottom. Mean lines are short thick horizontal strokes of
one colour; the error bar (SEM) is the thin vertical stroke of the same colour
above the mean line, read only when it extends beyond the mean line.
"""
from __future__ import annotations

import numpy as np

from livinglit.figures.source import calibrate, colour_mask, dark_mask, RASTER_UNCERTAINTY_PX_300DPI

DPI = 300


def runs(v: np.ndarray):
    """(start, end) inclusive of True runs in a 1-D boolean array."""
    out, s = [], None
    for i, b in enumerate(v):
        if b and s is None:
            s = i
        elif not b and s is not None:
            out.append((s, i - 1))
            s = None
    if s is not None:
        out.append((s, len(v) - 1))
    return out


def y_axis(img, x_lo=0, x_hi=None, threshold=110):
    """Column index of the y-axis line (longest dark vertical run) within [x_lo, x_hi)."""
    d = dark_mask(img, threshold)
    x_hi = d.shape[1] if x_hi is None else x_hi
    best, bx, by = 0, None, None
    for x in range(x_lo, x_hi):
        for a, b in runs(d[:, x]):
            if b - a > best:
                best, bx, by = b - a, x, (a, b)
    return bx, by


def y_ticks(img, axis_x, span, threshold=110, min_len=4, max_len=30):
    """Pixel rows of tick marks: dark horizontal strokes ending at the axis line on its left."""
    d = dark_mask(img, threshold)
    # axis line may be 2-4 px wide: find its left edge on each row
    rows = []
    for y in range(span[0], span[1] + 1):
        x = axis_x
        while x > 0 and d[y, x - 1]:
            x -= 1
        # x is the left edge of the dark run containing the axis; tick if the run is long enough
        length = axis_x - x
        if min_len <= length <= max_len:
            rows.append(y)
    groups = runs(np.isin(np.arange(img.shape[0]), rows))
    return [(a + b) / 2 for a, b in groups]


def cal_from_ticks(img, values, x_lo=0, x_hi=None, threshold=110, min_len=4):
    """Calibration from tick marks matched top to bottom to `values` (None = tick skipped, e.g. above a break)."""
    ax, span = y_axis(img, x_lo, x_hi, threshold)
    ticks = y_ticks(img, ax, span, threshold, min_len=min_len)
    if len(ticks) != len(values):
        raise ValueError(f"found {len(ticks)} tick marks at rows {ticks}, expected {len(values)}")
    marks = [(t, v) for t, v in zip(ticks, values) if v is not None]
    return calibrate(marks), ax


def hue_mask(img, channel, thr=40):
    """Pixels where one RGB channel exceeds both others by thr (blue or red ink; grey dots excluded)."""
    a = img.astype(int)
    others = [a[:, :, i] for i in range(3) if i != channel]
    return a[:, :, channel] - np.maximum(*others) > thr


def ink_mask(img, ch, thr, sat=None):
    """hue_mask for ch 0/2 (with sat: the other two channels also below sat, i.e. saturated ink only,
    which drops pale dots of the same hue); for ch -1, black ink: every channel below thr."""
    if ch < 0:
        return img.max(axis=2) < thr
    m = hue_mask(img, ch, thr)
    if sat is not None:
        others = [i for i in range(3) if i != ch]
        m &= img[:, :, others].max(axis=2) < sat
    return m


def mean_lines(m, x_lo, x_hi, min_width=15, min_thick=3, y_lo=0, y_hi=None, max_width=120):
    """Horizontal mean lines in mask m between columns x_lo..x_hi: list of (x_centre, y_top, y_bottom, x0, x1).

    A row belongs to a line when at least min_width consecutive pixels are in the mask.
    """
    y_hi = m.shape[0] if y_hi is None else y_hi
    rowruns = {}
    for y in range(y_lo, y_hi):
        for a, b in runs(m[y, x_lo:x_hi]):
            if b - a + 1 >= min_width:
                rowruns.setdefault(y, []).append((a + x_lo, b + x_lo))
    # group consecutive rows with overlapping runs
    lines = []
    for y in sorted(rowruns):
        for a, b in rowruns[y]:
            for L in lines:
                if L["y1"] == y - 1 and not (b < L["x0"] or a > L["x1"]):
                    L["y1"] = y
                    L["x0"], L["x1"] = min(L["x0"], a), max(L["x1"], b)
                    break
            else:
                lines.append({"y0": y, "y1": y, "x0": a, "x1": b})
    out = [L for L in lines if L["y1"] - L["y0"] + 1 >= min_thick and L["x1"] - L["x0"] + 1 <= max_width]
    return [((L["x0"] + L["x1"]) / 2, L["y0"], L["y1"], L["x0"], L["x1"]) for L in out]


def error_top(m, x_c, y_top, half=2, min_ext=3):
    """Top row of a thin vertical stroke in mask m rising from the mean line top at column x_c.

    Returns None when the stroke does not extend at least min_ext px above the line (SEM hidden by the line).
    """
    x0, x1 = int(round(x_c)) - half, int(round(x_c)) + half + 1
    y = y_top
    while y > 0 and m[y - 1, x0:x1].any():
        y -= 1
    return y if y_top - y >= min_ext else None


def reading(cal, ypx, unc=RASTER_UNCERTAINTY_PX_300DPI):
    v = cal.value(ypx)
    lo, hi = cal.interval(ypx, unc)
    return [v, min(lo, v) - cal.residual, max(hi, v) + cal.residual]


def bar_groups(fig, cal, m, lines, labels, read_error=True, err_mask=None):
    """Map mean lines (sorted left to right) to labels; returns read() groups with bar mean (and error when visible)."""
    lines = sorted(lines, key=lambda L: L[0])
    if len(lines) != len(labels):
        raise ValueError(f"found {len(lines)} mean lines at {[(round(L[0]), L[1]) for L in lines]}, expected {len(labels)}")
    groups = {}
    for L, lab in zip(lines, labels):
        if lab is None:
            continue
        xc, y0, y1 = L[0], L[1], L[2]
        bar = {"mean": reading(cal, (y0 + y1) / 2)}
        if read_error:
            et = error_top(m if err_mask is None else err_mask, xc, y0)
            if et is not None:
                # top row of the cap/stroke; its centre is ~0.5 px lower; thin anti-aliased strokes: 1 px uncertainty
                bar["error"] = reading(cal, et + 0.5, unc=1.0)
        groups[lab] = {"points": [], "countable": False, "bar": bar}
    return groups


def panel(fig, ticks, ch, labels, xs=None, keep=None, thr=40, min_width=15, read_error=True,
          axis_frac=3, x_from=None, x_to=None, sat=None, inks=None):
    """One scatter panel with mean lines: calibrate from tick marks, find mean lines, map them left to right.

    ticks: printed tick values top to bottom (None for a tick that is not used, e.g. above an axis break).
    ch: 0 red / 2 blue mean-line ink (grey dots excluded), or -1 for black lines (every channel below thr).
    labels: one per mean line, left to right (None = line found but not read, e.g. above an axis break).
    xs: optional x per label (concentration or frequency as printed). keep: labels to return.
    """
    img, _ = fig.render(DPI)
    groups = {}
    cal, ax = cal_from_ticks(img, ticks, 0, img.shape[1] // axis_frac)
    x0 = ax + 4 if x_from is None else x_from
    x1 = img.shape[1] if x_to is None else x_to
    # inks: several inks in one panel, each [(ch, thr, sat), labels, xs]; else the single ink given
    for (c, t, sa), labs, xx in (inks or [((ch, thr, sat), labels, xs)]):
        m = ink_mask(img, c, t, sa)
        lines = mean_lines(m, x0, x1, min_width=min_width)
        g = bar_groups(fig, cal, m, lines, labs, read_error=read_error)
        if xx is not None:
            for lab, x in zip(labs, xx):
                if lab in g and x is not None:
                    g[lab]["bar"]["x"] = x
        groups.update(g)
    if keep is not None:
        groups = {k: v for k, v in groups.items() if k in keep}
    return {"groups": groups}
