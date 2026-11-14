"""Helpers for this paper's raster bar charts (2018_Ronaldson-Bouchard only).

The Extended Data figures are embedded in the main PDF as 600-dpi images, so every
panel is read from a 600-dpi render of its crop. Tick values are the printed labels
(given by each script); their positions, bar ends and error-bar ends are found by code.
"""
from __future__ import annotations

import numpy as np

from livinglit.figures.source import calibrate, RASTER_UNCERTAINTY_PX_300DPI

DPI = 600
UNC_PT = RASTER_UNCERTAINTY_PX_300DPI * 72 / 300  # 0.6 px at 300 dpi, in page points


def load(fig):
    img, scale = fig.render(DPI)
    return img.astype(int), scale


def gray(img):
    return img.mean(axis=2)


def ink(img, thr=215):
    """Anything not near-white (bars, lines, text)."""
    return img.min(axis=2) < thr


def dark(img, thr=110):
    return gray(img) < thr


def runs(mask_1d, min_len=1):
    """(start, end_inclusive) of True runs in a 1-D mask."""
    out, s = [], None
    for i, v in enumerate(list(mask_1d) + [False]):
        if v and s is None:
            s = i
        elif not v and s is not None:
            if i - s >= min_len:
                out.append((s, i - 1))
            s = None
    return out


def axis_x(img, x_lo, x_hi, thr=110):
    """Column (px) in [x_lo, x_hi) holding the longest vertical dark run: the y axis."""
    d = dark(img, thr)
    best, bx = -1, None
    for x in range(max(0, x_lo), min(img.shape[1], x_hi)):
        r = runs(d[:, x])
        L = max((b - a for a, b in r), default=0)
        if L > best:
            best, bx = L, x
    # the axis line is several px wide: take the centre of the dark columns around bx with similar runs
    cols = [x for x in range(bx - 8, bx + 9) if 0 <= x < img.shape[1]
            and max((b - a for a, b in runs(d[:, x])), default=0) >= 0.8 * best]
    return (min(cols) + max(cols)) / 2.0, best


def axis_span(img, ax, thr=110):
    """(top, bottom) px of the longest dark run in the axis column."""
    d = dark(img, thr)
    r = runs(d[:, int(round(ax))])
    return max(r, key=lambda t: t[1] - t[0])


def ticks_left(img, ax, length_px=(8, 60), thr=110, span=None):
    """Row centres (px) of tick marks: short dark horizontal strokes ending at the axis line, on its left."""
    d = dark(img, thr)
    a = int(round(ax))
    # leftmost column of the axis line
    left = a
    while left > 0 and d[:, left - 1].sum() > 0.5 * d[:, a].sum():
        left -= 1
    lo, hi = length_px
    rows = []
    r0, r1 = span if span else (0, img.shape[0] - 1)
    r0, r1 = max(0, int(r0)), min(img.shape[0] - 1, int(r1))
    for y in range(r0, r1 + 1):
        x = left - 1
        n = 0
        while x >= 0 and d[y, x]:
            n += 1
            x -= 1
        if lo <= n <= hi:
            rows.append(y)
    return [(a + b) / 2.0 for a, b in runs(np.isin(np.arange(img.shape[0]), rows))]


def calib_rows(fig, scale, rows_px, values, log=False):
    """Calibration from tick rows (px in the crop) and their printed values, in page points."""
    if len(rows_px) != len(values):
        raise ValueError(f"found {len(rows_px)} ticks, expected {len(values)}: {rows_px}")
    marks = [(fig.crop[1] + r / scale, v) for r, v in zip(rows_px, values)]
    return calibrate(marks, log=log)


def resid_pt(cal):
    return abs(cal.residual / cal.slope) if cal.slope else 0.0


def reading(cal, y_px, scale, fig, extra_pt=0.0):
    """[value, lo, hi] for a page row given in crop px."""
    pos = fig.crop[1] + y_px / scale
    u = UNC_PT + resid_pt(cal) + extra_pt
    v = cal.value(pos)
    lo, hi = cal.interval(pos, u)
    return [v, min(lo, v), max(hi, v)]


def bar_spans(img, row, min_w, thr=215, x_lo=0, x_hi=None):
    """(x0, x1) px of ink runs at least min_w wide along one row: the bars crossing it."""
    m = ink(img, thr)[int(round(row)), x_lo:x_hi]
    return [(a + x_lo, b + x_lo) for a, b in runs(m, min_w)]


def bar_end(img, span, base_row, direction=-1, thr=215):
    """Row (px) of the far edge of a bar: walking from base_row (direction -1 = up) along a column a third of
    the way into the bar (clear of the error-bar line), the last ink row. If the edge is an outline darker than
    the fill, the outline's centre is taken (outlines are drawn on the boundary)."""
    x0, x1 = span
    cols = [int(x0 + (x1 - x0) * f) for f in np.linspace(0.15, 0.85, 15)]
    ends = []
    for c in cols:
        m = ink(img, thr)[:, c]
        y = int(round(base_row))
        while 0 <= y + direction < img.shape[0] and m[y + direction]:
            y += direction
        # y is the last ink row; an outline is a dark run at the edge, clearly darker than the fill
        g = gray(img)[:, c]
        fill = float(np.median(g[sorted([int(round(base_row)), y])[0]:sorted([int(round(base_row)), y])[1] + 1]))
        k = y
        while 0 <= k - direction < img.shape[0] and g[k - direction] < min(90, fill - 40) and abs(k - y) < 12:
            k -= direction
        if g[y] < min(90, fill - 40) and abs(k - y) >= 1:
            ends.append((y + k) / 2.0)
        else:
            ends.append(y + direction * 0.5)  # the fill's edge lies half a pixel beyond the last ink row
    ends = np.array(sorted(ends))
    q1, q3 = np.percentile(ends, [25, 75])   # columns crossing an error line or a label are outliers
    return float(np.median(ends)), float(q3 - q1)


def error_end(img, span, edge_row, direction=-1, thr=215, max_gap=1):
    """Row (px) of the far end of an error bar drawn from the bar edge: the error line is the darkest column near
    the bar centre; walk outward along it through ink (gaps up to max_gap px) and return the centre of the cap."""
    x0, x1 = span
    xc = (x0 + x1) / 2.0
    g = gray(img)
    m = ink(img, thr)
    e = int(round(edge_row))
    probe = [e + direction * k for k in range(3, 12)]
    probe = [p for p in probe if 0 <= p < img.shape[0]]
    best, bc = None, None
    W = img.shape[1]
    for c in range(int(xc - (x1 - x0) * 0.25), int(xc + (x1 - x0) * 0.25) + 1):
        if c - 9 < 0 or c + 9 >= W:
            continue
        line = float(np.median([g[p, c] for p in probe]))
        side = float(np.median([min(g[p, c - 9], g[p, c + 9]) for p in probe]))
        if side < 200:          # an error line stands alone: white on both sides
            continue
        if best is None or line < best:
            best, bc = line, c
    if best is None or best > 200:   # no error line beyond the bar edge
        return None, bc
    y, gap, last = e, 0, e
    while 0 <= y + direction < img.shape[0]:
        y += direction
        if m[y, bc - 1:bc + 2].any():
            last, gap = y, 0
        else:
            gap += 1
            if gap > max_gap:
                break
    # cap: the run of rows near `last` where ink extends sideways from the line
    cap = []
    for k in range(0, 15):
        yy = last - direction * k
        w = m[yy, bc - 15:bc + 16].sum()
        if w >= 22:
            cap.append(yy)
        elif cap:
            break
    end = (min(cap) + max(cap)) / 2.0 if cap else float(last)
    if (end - edge_row) * direction < 4:   # no error bar standing clear of the bar edge (cap merged with the edge)
        return None, bc
    return end, bc


def bar_group(fig, cal, scale, img, span, base_row, direction=-1, err_direction=None, err=True):
    """{"points": [], "countable": False, "bar": {"mean": [...], "error": [...]}} for one bar."""
    edge, spread_px = bar_end(img, span, base_row, direction)
    out = {"points": [], "countable": False, "bar": {"mean": reading(cal, edge, scale, fig, spread_px / scale / 2)}}
    if err:
        ed = err_direction if err_direction is not None else direction
        end, _ = error_end(img, span, edge, ed)
        if end is not None:
            out["bar"]["error"] = reading(cal, end, scale, fig)
    return out


def row_of(cal, fig, scale, value):
    """Crop px row where the axis reads `value` (linear axes)."""
    return ((value - cal.intercept) / cal.slope - fig.crop[1]) * scale


def bar_panel(fig, axis_pt, tick_values, bar_row_pt, labels, direction=-1, min_w_pt=3.0, err=True,
              x_range_pt=None, tick_len=(8, 60), thr=110, ticks="marks", band_px=(10, 90)):
    """Read a bar chart whose bars cross the row bar_row_pt: labels name the bars left to right.
    The script gives the axis search range (page x), the printed tick values (top to bottom) and the labels."""
    img, s = load(fig)
    ax, _ = axis_x(img, int((axis_pt[0] - fig.crop[0]) * s), int((axis_pt[1] - fig.crop[0]) * s), thr)
    rows = find_ticks(img, ax, thr, tick_len, ticks, band_px)
    cal = calib_rows(fig, s, rows, tick_values)
    base = row_of(cal, fig, s, 0.0)
    row = (bar_row_pt - fig.crop[1]) * s
    xlo = int(ax + 3) if x_range_pt is None else int((x_range_pt[0] - fig.crop[0]) * s)
    xhi = None if x_range_pt is None else int((x_range_pt[1] - fig.crop[0]) * s)
    spans = bar_spans(img, row, int(min_w_pt * s), x_lo=xlo, x_hi=xhi)
    if len(spans) != len(labels):
        raise ValueError(f"found {len(spans)} bars, expected {len(labels)}")
    groups = {}
    for lab, span in zip(labels, spans):
        g = bar_group(fig, cal, s, img, span, base, direction, err=err)
        groups[lab] = g
    return groups


def expand(groups, links):
    """One label per (item, group) link, "<item>/<group>", so each reading is tied to every item over its group."""
    out = {}
    for item, gids in links.items():
        for g in gids:
            out[f"{item}/{g}"] = groups[g]
    return out


def colour_spans(img, row, colours, min_w, x_lo=0, x_hi=None, white=(255, 255, 255)):
    """Bars crossing one row, segmented by colour: each pixel goes to the nearest of `colours` (name -> RGB) or
    white; runs of one colour at least min_w px wide. Returns [(name, (x0, x1))] left to right."""
    seg = img[int(round(row)), x_lo:x_hi].astype(int)
    names = ["_white"] + list(colours)
    refs = np.array([white] + [colours[n] for n in colours], int)
    d = np.abs(seg[:, None, :] - refs[None, :, :]).sum(axis=2)
    cls = d.argmin(axis=1)
    out = []
    for i, n in enumerate(names):
        if n == "_white":
            continue
        for a, b in runs(cls == i, min_w):
            out.append((a + x_lo, (n, (a + x_lo, b + x_lo))))
    return [t for _, t in sorted(out)]


def colour_bar_panel(fig, axis_pt, tick_values, bar_row_pt, colours, labels, min_w_pt=3.0, err=True,
                     x_range_pt=None, tick_len=(8, 60), thr=110, direction=-1, expect=None,
                     ticks="marks", band_px=(10, 90)):
    """Like bar_panel, but bars that touch are told apart by colour; labels name the bars left to right;
    `expect` (optional) is the colour name sequence the script expects, checked against what is found."""
    img, s = load(fig)
    ax, _ = axis_x(img, int((axis_pt[0] - fig.crop[0]) * s), int((axis_pt[1] - fig.crop[0]) * s), thr)
    rows = find_ticks(img, ax, thr, tick_len, ticks, band_px)
    cal = calib_rows(fig, s, rows, tick_values)
    base = row_of(cal, fig, s, 0.0)
    row = (bar_row_pt - fig.crop[1]) * s
    xlo = int(ax + 3) if x_range_pt is None else int((x_range_pt[0] - fig.crop[0]) * s)
    xhi = None if x_range_pt is None else int((x_range_pt[1] - fig.crop[0]) * s)
    found = colour_spans(img, row, colours, int(min_w_pt * s), xlo, xhi)
    if len(found) != len(labels):
        raise ValueError(f"found {len(found)} bars {[n for n, _ in found]}, expected {len(labels)}")
    if expect is not None and [n for n, _ in found] != list(expect):
        raise ValueError(f"bar colours {[n for n, _ in found]} differ from {list(expect)}")
    cls, names = classify(img, colours)
    groups = {}
    for lab, (name, span) in zip(labels, found):
        edge, spr = colour_bar_end(img, cls, names, name, span, base, direction)
        g = {"points": [], "countable": False, "bar": {"mean": reading(cal, edge, s, fig, spr / s / 2)}}
        if err:
            end, _ = error_end(img, span, edge, direction)
            if end is not None:
                g["bar"]["error"] = reading(cal, end, s, fig)
        groups[lab] = g
    return groups


def classify(img, colours, white=(255, 255, 255)):
    """Per-pixel index of the nearest of [white] + colours (name -> RGB); returns (index array, names)."""
    names = ["_white"] + list(colours)
    refs = np.array([white] + [colours[n] for n in colours], int)
    d = np.abs(img[:, :, None, :].astype(int) - refs[None, None, :, :]).sum(axis=3)
    return d.argmin(axis=2), names


def colour_bar_end(img, cls, names, name, span, base_row, direction=-1, max_dark=14):
    """Far edge of a bar of colour `name`: per column (15 across the middle 70%), walk from base_row through the
    bar's colour, crossing dark runs (error lines, caps) of at most max_dark px when the colour resumes beyond them;
    a dark outline run at the end is taken at its centre. Median over columns, and IQR."""
    k = names.index(name)
    g = gray(img)
    x0, x1 = span
    H = img.shape[0]
    ends = []
    for c in [int(x0 + (x1 - x0) * f) for f in np.linspace(0.15, 0.85, 15)]:
        y = int(round(base_row))
        while not cls[y, c] == k and abs(y - base_row) < 40:   # start inside the bar
            y += direction
        while True:
            if 0 <= y + direction < H and cls[y + direction, c] == k:
                y += direction
                continue
            j = y   # a run of other ink (error line, cap, anti-aliasing) beyond y, after which the colour resumes?
            while 0 <= j + direction < H and cls[j + direction, c] not in (0, k) and abs(j - y) < max_dark:
                j += direction
            if j != y and 0 <= j + direction < H and cls[j + direction, c] == k:
                y = j + direction
                continue
            break
        j = y   # a dark outline at the end
        while 0 <= j + direction < H and g[j + direction, c] < 90 and abs(j - y) < max_dark:
            j += direction
        if j != y and name_is_light(img, cls, k):
            ends.append((y + direction + j) / 2.0)
        else:
            ends.append(y + direction * 0.5)
    ends = np.array(sorted(ends))
    q1, q3 = np.percentile(ends, [25, 75])
    return float(np.median(ends)), float(q3 - q1)


def name_is_light(img, cls, k):
    """Whether bars of class k are clearly lighter than a dark outline (so an outline can be told from the fill)."""
    sel = cls == k
    return bool(sel.any() and gray(img)[sel].mean() > 80)


def label_rows(img, ax, band_px=(10, 90), thr=110, span=None, min_h=8):
    """Row centres (px) of the tick labels left of the axis, for axes drawn without tick marks: runs of rows with
    dark ink in a band left of the axis line (digit glyphs share one height, so a run's middle is the label's)."""
    d = dark(img, thr)
    a = int(round(ax))
    lo, hi = band_px
    band = d[:, max(0, a - hi):max(0, a - lo)].any(axis=1)
    if span:
        band[:max(0, span[0])] = False
        band[span[1] + 1:] = False
    return [(r0 + r1) / 2.0 for r0, r1 in runs(band, min_h)]


def find_ticks(img, ax, thr, tick_len, mode="marks", band_px=(10, 90)):
    sp = axis_span(img, ax, thr)
    if mode == "labels":
        return label_rows(img, ax, band_px, thr, span=(sp[0] - 40, sp[1] + 40))
    if mode == "marks_right":
        return ticks_right(img, ax, span=(sp[0] - 6, sp[1] + 6), length_px=tick_len, thr=thr)
    return ticks_left(img, ax, span=(sp[0] - 6, sp[1] + 6), length_px=tick_len, thr=thr)


def ticks_right(img, ax, length_px=(8, 60), thr=110, span=None):
    """Row centres (px) of tick marks drawn inside the plot: short dark strokes leaving the axis line to the right."""
    d = dark(img, thr)
    a = int(round(ax))
    right = a
    while right < img.shape[1] - 1 and d[:, right + 1].sum() > 0.5 * d[:, a].sum():
        right += 1
    lo, hi = length_px
    rows = []
    r0, r1 = span if span else (0, img.shape[0] - 1)
    r0, r1 = max(0, int(r0)), min(img.shape[0] - 1, int(r1))
    for y in range(r0, r1 + 1):
        x, n = right + 1, 0
        while x < img.shape[1] and d[y, x]:
            n += 1
            x += 1
        if lo <= n <= hi:
            rows.append(y)
    return [(a + b) / 2.0 for a, b in runs(np.isin(np.arange(img.shape[0]), rows))]


def gridlines(img, fig, scale, x_pts, y_range_pt, drop=8, min_px=2, max_px=12):
    """Rows (crop px, sub-pixel) of faint horizontal gridlines: in each probe column (page x), runs of rows darker
    than the local background by `drop`, centred on their darkness; rows found in every column are kept."""
    g = gray(img)
    y0 = int((y_range_pt[0] - fig.crop[1]) * scale)
    y1 = int((y_range_pt[1] - fig.crop[1]) * scale)
    per = []
    for xp in x_pts:
        c = int((xp - fig.crop[0]) * scale)
        col = g[y0:y1, c]
        bg = float(np.median(col))
        w = np.clip(bg - col, 0, None)
        found = []
        for a, b in runs(w > drop):
            if min_px <= b - a + 1 <= max_px:
                seg = w[a:b + 1]
                found.append(y0 + a + float((seg * np.arange(len(seg))).sum() / seg.sum()))
        per.append(found)
    base = per[0]
    keep = []
    for r in base:
        ms = [min(f, key=lambda t: abs(t - r)) for f in per[1:] if f]
        if all(abs(m - r) < 3 for m in ms) and len(ms) == len(per) - 1:
            keep.append(float(np.mean([r] + ms)))
    return keep


def grid_bar_panel(fig, grid_x_pt, grid_y_pt, tick_values, bar_row_pt, colours, labels, min_w_pt=3.0, err=True,
                   x_range_pt=None, direction=-1, expect=None):
    """Bar chart drawn without an axis line but with gridlines at its tick values: calibrated on the gridlines."""
    img, s = load(fig)
    rows = gridlines(img, fig, s, grid_x_pt, grid_y_pt)
    cal = calib_rows(fig, s, rows, tick_values)
    base = row_of(cal, fig, s, 0.0)
    row = (bar_row_pt - fig.crop[1]) * s
    xlo = 0 if x_range_pt is None else int((x_range_pt[0] - fig.crop[0]) * s)
    xhi = None if x_range_pt is None else int((x_range_pt[1] - fig.crop[0]) * s)
    found = colour_spans(img, row, colours, int(min_w_pt * s), xlo, xhi)
    if len(found) != len(labels):
        raise ValueError(f"found {len(found)} bars {[n for n, _ in found]}, expected {len(labels)}")
    if expect is not None and [n for n, _ in found] != list(expect):
        raise ValueError(f"bar colours {[n for n, _ in found]} differ from {list(expect)}")
    cls, names = classify(img, colours)
    groups = {}
    for lab, (name, span) in zip(labels, found):
        edge, spr = colour_bar_end(img, cls, names, name, span, base, direction)
        g = {"points": [], "countable": False, "bar": {"mean": reading(cal, edge, s, fig, spr / s / 2)}}
        if err:
            end, _ = error_end(img, span, edge, direction)
            if end is not None:
                g["bar"]["error"] = reading(cal, end, s, fig)
        groups[lab] = g
    return groups
