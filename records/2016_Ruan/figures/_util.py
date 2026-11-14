"""Helpers for 2016_Ruan's figure scripts (this paper's alone).

Every panel in this paper is a raster image (GraphPad Prism scatter plots with mean and
SEM bars, Excel line charts, and force traces). These helpers find, in a 300 dpi render of
a crop: the y axis and its tick marks, the long thin horizontal lines (mean and error-bar
caps) of one group column, and solid markers that stand alone. The scripts supply the
tick values, the column windows and the marker sizes.
"""
from __future__ import annotations

import numpy as np

from livinglit.figures.source import (RASTER_UNCERTAINTY_PX_300DPI, calibrate, dark_mask, blobs, point)

DPI = 300


def render(fig, threshold=128):
    img, scale = fig.render(DPI)
    return img, scale, dark_mask(img, threshold)


def runs(idx):
    """Consecutive runs of sorted integer indices -> list of (start, end) inclusive."""
    out = []
    for i in idx:
        if out and i == out[-1][1] + 1:
            out[-1][1] = i
        else:
            out.append([i, i])
    return [tuple(r) for r in out]


def y_axis(mask, x_lo, x_hi, y_lo=0, y_hi=None):
    """The vertical axis line: the run of columns in [x_lo, x_hi) with the most ink between y_lo and y_hi."""
    sub = mask[y_lo:y_hi, x_lo:x_hi].sum(0)
    best = sub.max()
    cols = [x_lo + i for i in np.nonzero(sub >= 0.85 * best)[0]]
    r = max(runs(cols), key=lambda t: t[1] - t[0])
    return r  # (left, right) px


def y_ticks(mask, axis_left, reach=(3, 7), y_lo=0, y_hi=None, min_rows=2, max_rows=None):
    """Tick marks to the left of the y axis: centres (px) of row runs fully inked over columns axis_left-reach."""
    a, b = axis_left - reach[1], axis_left - reach[0]
    seg = mask[y_lo:y_hi, a:b]
    rows = [y_lo + i for i in np.nonzero(seg.all(1))[0]]
    return [(s + e) / 2 for s, e in runs(rows) if e - s + 1 >= min_rows and (max_rows is None or e - s + 1 <= max_rows)]


def x_ticks(mask, axis_bottom, reach=(3, 7), x_lo=0, x_hi=None, min_cols=2):
    """Tick marks below an x axis: centres (px) of column runs fully inked over rows axis_bottom+reach."""
    a, b = axis_bottom + reach[0], axis_bottom + reach[1]
    seg = mask[a:b, x_lo:x_hi]
    cols = [x_lo + i for i in np.nonzero(seg.all(0))[0]]
    return [(s + e) / 2 for s, e in runs(cols) if e - s + 1 >= min_cols]


def fit(tick_px, values, log=False):
    """Calibration from matched tick positions (px) and their printed values; counts must agree."""
    if len(tick_px) != len(values):
        raise ValueError(f"found {len(tick_px)} ticks for {len(values)} printed values: {tick_px}")
    return calibrate(list(zip(tick_px, values)), log=log)


def misfit_px(cal):
    """Calibration misfit expressed in px."""
    return abs(cal.residual / cal.slope) if cal.slope else 0.0


def hlines(mask, x_lo, x_hi, y_lo, y_hi, min_len, max_thick=10, span_tol=4, merge_thick=None):
    """Thin horizontal lines in a window: rows whose longest ink run is >= min_len.

    Returns [{y: centre row, x0, x1, thick}] (px, full-image coordinates), one per line: consecutive rows
    whose runs start and end within span_tol of each other (so a line is kept apart from markers it crosses).
    """
    win = mask[y_lo:y_hi, x_lo:x_hi]
    found = []
    for i, row in enumerate(win):
        idx = np.nonzero(row)[0]
        best = None
        for s, e in runs(list(idx)):
            if e - s + 1 >= min_len and (best is None or e - s > best[1] - best[0]):
                best = (s, e)
        if best:
            found.append((y_lo + i, x_lo + best[0], x_lo + best[1]))
    lines = []
    for y, a, b in found:
        if lines and y == lines[-1]["rows"][-1] + 1 and abs(a - lines[-1]["spans"][-1][0]) <= span_tol \
                and abs(b - lines[-1]["spans"][-1][1]) <= span_tol:
            lines[-1]["rows"].append(y)
            lines[-1]["spans"].append((a, b))
        else:
            lines.append({"rows": [y], "x0": a, "spans": [(a, b)]})
    merge_thick = merge_thick or max_thick
    merged = []  # a line split by a marker touching one side: contiguous fragments over the same span
    for ln in lines:
        if merged:
            pv = merged[-1]
            a0, a1 = np.median([q[0] for q in pv["spans"]]), np.median([q[1] for q in pv["spans"]])
            b0, b1 = np.median([q[0] for q in ln["spans"]]), np.median([q[1] for q in ln["spans"]])
            tol = 0.12 * max(a1 - a0, b1 - b0)
            if ln["rows"][0] == pv["rows"][-1] + 1 and abs(a0 - b0) <= tol and abs(a1 - b1) <= tol \
                    and len(pv["rows"]) + len(ln["rows"]) <= merge_thick:
                pv["rows"] += ln["rows"]
                pv["spans"] += ln["spans"]
                continue
        merged.append(ln)
    out = []
    for ln in merged:
        rows = ln["rows"]
        if len(rows) > max_thick:
            continue
        x0 = int(np.median([s[0] for s in ln["spans"]]))
        x1 = int(np.median([s[1] for s in ln["spans"]]))
        out.append({"y": (rows[0] + rows[-1]) / 2, "x0": x0, "x1": x1, "thick": len(rows)})
    return out


def mean_and_upper_cap(lines, centre_tol=None):
    """The widest line is the mean; the upper error end is the nearest narrower line above it, centred on it."""
    if not lines:
        return None, None
    mean = max(lines, key=lambda l: l["x1"] - l["x0"])
    c = (mean["x0"] + mean["x1"]) / 2
    centre_tol = centre_tol or max(6, 0.1 * (mean["x1"] - mean["x0"]))
    mean_top = mean["y"] - (mean["thick"] - 1) / 2
    # a cap is apart from the mean line (not a fragment of it or of a marker on it) and about as thick
    caps = [l for l in lines if l is not mean and l["y"] + (l["thick"] - 1) / 2 < mean_top - 1
            and l["thick"] >= 0.5 * mean["thick"]
            and abs((l["x0"] + l["x1"]) / 2 - c) <= centre_tol and (l["x1"] - l["x0"]) < (mean["x1"] - mean["x0"])]
    cap = max(caps, key=lambda l: l["y"]) if caps else None
    return mean, cap


AREA_FACTOR = {"circle": 0.785, "square": 1.0, "triangle": 0.5, "diamond": 0.5}


def solid_markers(mask, x_lo, x_hi, y_lo, y_hi, size_px, shape="circle", area_tol=0.45, kernel_px=None,
                  tri_kernel_px=None):
    """Markers in a window after removing lines thinner than the marker (morphological opening).

    Returns (markers, all_alone): markers are dicts with centroid and bbox centre (px, full image);
    all_alone is False when any blob is larger than one marker (overlap) or smaller (clipped).
    """
    import cv2
    win = mask[y_lo:y_hi, x_lo:x_hi].astype(np.uint8)
    # wider than the lines, narrower than a marker (a triangle's inscribed circle is small)
    if shape == "triangle":
        k = (tri_kernel_px or max(3, int(size_px * 0.5))) | 1
    else:
        k = (kernel_px or max(3, int(size_px * 0.75))) | 1
    opened = cv2.morphologyEx(win, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    bl = blobs(opened.astype(bool), min_area=int(0.15 * size_px * size_px))
    if not bl:
        return [], True
    areas = np.array([b["area"] for b in bl], float)
    single = AREA_FACTOR[shape] * size_px * size_px  # one marker's area
    alone = bool(np.all(np.abs(areas - single) <= area_tol * single))
    out = []
    for b in bl:
        bx, by, bw, bh = b["box"]
        out.append({"x": x_lo + b["x"], "y": y_lo + b["y"], "cy_box": y_lo + by + (bh - 1) / 2,
                    "cx_box": x_lo + bx + (bw - 1) / 2, "area": b["area"]})
    return out, alone


def vertical_extent(mask, x, y):
    """Rows (top, bottom) of the ink run through column x that contains row y (centre column +-1 px)."""
    col = mask[:, int(round(x)) - 1:int(round(x)) + 2].any(1)
    y = int(round(y))
    a = b = y
    while a > 0 and col[a - 1]:
        a -= 1
    while b < len(col) - 1 and col[b + 1]:
        b += 1
    return a, b


def unc(cal, extra_px=0.0, native_dpi=DPI):
    """0.6 px at 300 dpi; an image embedded at a lower resolution gets 0.6 of its own pixels."""
    return RASTER_UNCERTAINTY_PX_300DPI * max(1.0, DPI / native_dpi) + misfit_px(cal) + extra_px


def to_point(fig, cal, scale, px_x, px_y, extra_px=0.0, x=None, native_dpi=DPI):
    """A reading at pixel (px_x, px_y) on a y-calibrated axis (calibration in px)."""
    return point(cal, px_y, unc(cal, extra_px, native_dpi), fig.to_page(px_x, px_y, scale), x=x)


def bar(cal, px_y, extra_px=0.0, native_dpi=DPI):
    v = cal.value(px_y)
    lo, hi = cal.interval(px_y, unc(cal, extra_px, native_dpi))
    return [v, min(lo, v), max(hi, v)]


def scatter_group(fig, mask, scale, cal, x_lo, x_hi, y_lo, y_hi, marker_px, line_min_px, shape="circle",
                  native_dpi=DPI, kernel_px=None, max_thick=10, tri_kernel_px=None):
    """One column of a Prism scatter: points (if every marker stands alone), mean, and upper SEM end."""
    lines = hlines(mask, x_lo, x_hi, y_lo, y_hi, line_min_px, max_thick)
    mean, cap = mean_and_upper_cap(lines)
    marks, alone = solid_markers(mask, x_lo, x_hi, y_lo, y_hi, marker_px, shape, kernel_px=kernel_px,
                                 tri_kernel_px=tri_kernel_px)
    g = {"points": [], "countable": alone, "bar": {}}
    if alone and shape == "triangle":
        # Prism centres a triangle on its bounding box, not its centroid; opening rounds the apex, so the box
        # is taken from the raw ink in the centroid's column (apex to base)
        ext = [vertical_extent(mask, m["x"], m["y"]) for m in marks]
        hs = [b - a + 1 for a, b in ext]
        if max(hs) > 1.25 * float(np.median(hs)):  # a bar or another marker runs through the column
            g["countable"] = False
        else:
            for m, (a, b) in zip(marks, ext):
                g["points"].append(to_point(fig, cal, scale, m["x"], (a + b) / 2, native_dpi=native_dpi))
    elif alone:
        for m in marks:
            g["points"].append(to_point(fig, cal, scale, m["x"], m["y"], native_dpi=native_dpi))
    if mean:
        g["bar"]["mean"] = bar(cal, mean["y"], native_dpi=native_dpi)
    if cap:
        g["bar"]["error"] = bar(cal, cap["y"], native_dpi=native_dpi)
    return g


def scatter_panel(fig, axis_x, tick_values_top_down, y_lo, y_hi, columns, marker_px, line_min_px,
                  no_error=(), threshold=128, tick_reach=(3, 7), log=False, native_dpi=DPI,
                  kernel_px=None, max_thick=10, tri_kernel_px=None):
    """A Prism scatter panel: calibrate the y axis from its tick marks, then read each group column.

    columns: {group: (x_lo, x_hi, shape[, y_lo])} in px of the 300 dpi crop (a column's own y_lo keeps
    significance bars out). no_error: groups whose error-bar caps
    are hidden by markers (the upper SEM end is not read for them).
    """
    img, scale, m = render(fig, threshold)
    left, _ = y_axis(m, *axis_x)
    cal = fit(y_ticks(m, left, tick_reach), tick_values_top_down, log=log)
    out = {}
    for g, (a, b, shape, *own) in columns.items():
        r = scatter_group(fig, m, scale, cal, a, b, own[0] if own else y_lo, y_hi, marker_px, line_min_px, shape,
                          native_dpi, kernel_px, max_thick, tri_kernel_px)
        if g in no_error:
            r["bar"].pop("error", None)
        out[g] = r
    return out


def per_item(read, items):
    """The same column readings under one label per evidence item: '<item>: <group>'."""
    return {"groups": {f"{it}: {g}": read[g] for it, gs in items.items() for g in gs}}


def grey_marker_columns(img, x_lo, x_hi, y_lo, y_hi, light=215, dark=100, max_sat=40, min_cols=4):
    """Grey markers drawn over a black axis line: columns holding grey ink grouped into markers; each
    marker's centre is the middle of its grey rows (the axis may hide its middle). Returns [(x, y)] px."""
    sub = img[y_lo:y_hi, x_lo:x_hi].astype(int)
    mean, sat = sub.mean(2), sub.max(2) - sub.min(2)
    grey = (mean < light) & (mean >= dark) & (sat <= max_sat)
    # a marker column has grey ink above and below the axis band; a plain axis column does not
    cols = [c for c in range(grey.shape[1]) if grey[:, c].sum() >= 3 and not grey[:, c].all()]
    out = []
    for s, e in runs(cols):
        if e - s + 1 < min_cols:
            continue
        w = e - s + 1  # the middle third of the marker's columns holds its apexes (edges may touch ticks)
        rows = np.nonzero(grey[:, s + w // 3:e + 1 - w // 3].any(1))[0]
        # drop the anti-aliased edge rows of the axis band that span the whole window
        full = grey.all(1)
        rows = [r for r in rows if not full[r]]
        if rows:
            out.append((x_lo + (s + e) / 2, y_lo + (min(rows) + max(rows)) / 2))
    return out


def frame(mask, min_frac=0.6):
    """The box drawn around a trace panel: {left: (x0, x1), right: (x0, x1), top: (y0, y1), bottom: (y0, y1)}
    px runs of its four lines."""
    h, w = mask.shape
    cols = [x for x in range(w) if mask[:, x].sum() >= min_frac * h * 0.6]
    rows = [y for y in range(h) if mask[y, :].sum() >= min_frac * w * 0.6]
    cr, rr = runs(cols), runs(rows)
    return {"left": cr[0], "right": cr[-1], "top": rr[0], "bottom": rr[-1]}


def trace_panel(fig, y_values_top_down, x_values, threshold=128, prominence=0.3, tick_reach=(1, 4),
                title_rows=0, min_sep_px=20, tick_threshold=200, native_dpi=DPI):
    """A force trace in a framed panel: y from the tick marks left of the frame, time from the tick marks
    below it. Returns {'peaks': [...], 'troughs': [...]} as points carrying x = time (s): each twitch's
    highest point and the lowest point between twitches, read on the centre line of the trace."""
    img, scale, m = render(fig, threshold)
    fr = frame(m)
    left, right, top, bottom = fr["left"][1], fr["right"][0], fr["top"][1], fr["bottom"][0]
    light = dark_mask(img, tick_threshold)  # tick marks are thin and anti-aliased
    cal = fit(y_ticks(light, fr["left"][0], tick_reach, y_lo=top, y_hi=bottom + 4, min_rows=1, max_rows=6),
              y_values_top_down)
    calx = fit(x_ticks(light, fr["bottom"][1], tick_reach, x_lo=fr["left"][0] - 4, x_hi=fr["right"][1] + 5,
                       min_cols=1), x_values)
    inner = m[top + 3 + title_rows:bottom - 2, left + 3:right - 2]
    import cv2
    n, lab, stats, _ = cv2.connectedComponentsWithStats(inner.astype(np.uint8), connectivity=8)
    trace = lab == (1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA])))  # the trace is the largest piece of ink
    y0, x0 = top + 3 + title_rows, left + 3
    cols = [c for c in range(trace.shape[1]) if trace[:, c].any()]
    up = np.array([np.nonzero(trace[:, c])[0][0] for c in cols], float)
    dn = np.array([np.nonzero(trace[:, c])[0][-1] for c in cols], float)
    # line half-thickness from the flat parts (the thinnest vertical extents)
    half = float(np.percentile(dn - up + 1, 10)) / 2
    need = prominence * abs(1 / cal.slope) * (y_values_top_down[0] - y_values_top_down[-1])
    peaks, troughs = [], []
    # peaks: columns that are the highest within +-min_sep_px and rise >= need above the lowest within a twitch width
    for i in range(len(cols)):
        a, b = max(0, i - min_sep_px), min(len(cols), i + min_sep_px + 1)
        if up[i] == up[a:b].min() and (i == 0 or up[i] < up[i - 1] or up[i] <= up[a:b].min()):
            lo_side = dn[max(0, i - 6 * min_sep_px):min(len(cols), i + 6 * min_sep_px + 1)].max()
            if lo_side - up[i] >= need and (not peaks or i - peaks[-1] > min_sep_px):
                peaks.append(i)
    for p, q in zip(peaks, peaks[1:]):
        j = p + int(np.argmax(dn[p:q]))
        troughs.append(j)
    out = {"peaks": [], "troughs": []}
    for i in peaks:
        px, py = x0 + cols[i], y0 + up[i] + half
        out["peaks"].append(to_point(fig, cal, scale, px, py, half / 2, native_dpi=native_dpi, x=float(round(calx.value(px), 2))))
    for j in troughs:
        px, py = x0 + cols[j], y0 + dn[j] - half
        out["troughs"].append(to_point(fig, cal, scale, px, py, half / 2, native_dpi=native_dpi, x=float(round(calx.value(px), 2))))
    out["_max"] = to_point(fig, cal, scale, x0 + cols[int(np.argmin(up))], y0 + up.min() + half, half / 2,
                           native_dpi=native_dpi,
                           x=float(round(calx.value(x0 + cols[int(np.argmin(up))]), 2)))
    return out


def trace_groups(o, items, group, twitches=True):
    """Labels '<item>: <group> peaks' / 'troughs' (or 'max', the highest point of a trace without twitches)."""
    out = {}
    for it in items:
        if twitches:
            out[f"{it}: {group} peaks"] = {"points": o["peaks"], "countable": True}
            out[f"{it}: {group} troughs"] = {"points": o["troughs"], "countable": True}
        else:
            out[f"{it}: {group} max"] = {"points": [o["_max"]], "countable": True}
    return {"groups": out}


def excel_trace(fig, grid_value, x_values, min_sep_s, prominence=0.4, native_dpi=DPI, black=80, grey=225):
    """A thick force trace in an Excel chart framed black at top and right, grey axes at left and bottom,
    one grey gridline at grid_value. y from the gridline and the bottom axis (0); time from the tick marks
    below the axis. Returns {'peaks': [...]} as points with x = time (s): each twitch's highest point on the
    upper edge of the trace plus half the trace's thickness on its flat parts."""
    import cv2
    img, scale = fig.render(DPI)
    g = img.astype(int).mean(2)
    ink = g < grey
    h, w = g.shape
    long_rows = [y for y in range(h) if ink[y].sum() > 0.8 * w]
    groups = runs(long_rows)
    top_frame, axis = groups[0], groups[-1]
    grid = [r for r in groups[1:-1]]
    if len(grid) != 1:
        raise ValueError(f"expected one gridline, found {grid}")
    y_axis0 = (axis[0] + axis[1]) / 2
    cal = calibrate([((grid[0][0] + grid[0][1]) / 2, grid_value), (y_axis0, 0.0)])
    left = [x for x in range(w) if ink[:, x].sum() > 0.6 * h]
    lc = runs(left)
    x_lo, x_hi = lc[0][1] + 2, lc[-1][0] - 2
    light = (g < grey) & (g >= black)
    xt = x_ticks(light | (g < black), axis[1], reach=(1, 4), x_lo=lc[0][0] - 3, x_hi=lc[-1][1] + 4, min_cols=1)
    calx = fit(xt, x_values)
    dark = (g < black)
    dark[:top_frame[1] + 2, :] = False
    dark[:, :x_lo] = False
    dark[:, x_hi:] = False
    n, lab, stats, _ = cv2.connectedComponentsWithStats(dark.astype(np.uint8), connectivity=8)
    trace = lab == (1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA])))
    cols = [c for c in range(w) if trace[:, c].any()]
    up = np.array([np.nonzero(trace[:, c])[0][0] for c in cols], float)
    dn = np.array([np.nonzero(trace[:, c])[0][-1] for c in cols], float)
    flat = dn - up + 1
    half = float(np.percentile(flat, 10)) / 2
    sep = abs(min_sep_s / calx.slope)
    need = prominence * abs(grid_value / cal.slope)
    peaks = []
    order = np.argsort(up, kind="stable")
    taken = np.zeros(len(cols), bool)
    for i in order:  # highest first; each peak claims +-sep columns
        if taken[i]:
            continue
        a, b = max(0, i - int(sep)), min(len(cols), i + int(sep) + 1)
        edge = i < sep / 3 or i > len(cols) - 1 - sep / 3  # a twitch cut by the plot edge
        if not edge and dn[a:b].max() - up[i] >= need:  # rises from the lowest point within +-sep
            peaks.append(i)
        taken[a:b] = True
    peaks.sort()
    pts = []
    for i in peaks:
        px, py = cols[i], up[i] + half
        pts.append(to_point(fig, cal, scale, px, py, half / 2, native_dpi=native_dpi, x=float(round(calx.value(px), 2))))
    return {"peaks": pts}
