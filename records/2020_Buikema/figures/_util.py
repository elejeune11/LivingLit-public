"""Helpers for 2020_Buikema Fig. 1D and 1F (vector dot plots with mean ± SEM).

Tick labels are outlined glyphs, not text, so the y axis is calibrated from the
vector tick lines on the axis, paired in order with the tick values as printed.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point


def _black(c, tol=0.1):
    return c is not None and max(c) < tol


def read_dot_panel(fig, tick_values, groups, ytick_max=3, marker_max=4, error_bars=True):
    """groups: list of labels in x-axis order. Returns {label: {points, countable, bar}}.

    error_bars=False: the panel draws a mean line only (no error bar objects); the bar gives the mean alone.
    """
    ds = fig.drawings()
    hlines, vticks = [], []
    for d in ds:
        r = d["rect"]
        if d.get("fill") is None and _black(d.get("color")) and [i[0] for i in d["items"]] == ["l"]:
            if r.height < 0.01 and r.width < ytick_max:
                hlines.append(r)            # y tick mark
            elif r.width < 0.01 and r.height < 4:
                vticks.append(r)            # x tick mark
    # y ticks: the short horizontal marks left of the y axis, bottom to top
    yt = sorted(hlines, key=lambda r: -r.y0)
    if len(yt) != len(tick_values):
        raise ValueError(f"found {len(yt)} y tick marks, expected {len(tick_values)}")
    cal = calibrate([(r.y0, v) for r, v in zip(yt, tick_values)])
    unc = VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)
    xs = sorted(r.x0 for r in vticks)
    if len(xs) != len(groups):
        raise ValueError(f"found {len(xs)} x tick marks, expected {len(groups)}")
    out = {g: {"points": [], "countable": True, "lines": []} for g in groups}

    def nearest(x):
        i = min(range(len(xs)), key=lambda k: abs(xs[k] - x))
        return groups[i] if abs(xs[i] - x) < 6 else None

    for d in ds:
        r = d["rect"]
        f, c = d.get("fill"), d.get("color")
        if f is not None and not _black(f) and r.width < marker_max and r.height < marker_max:
            g = nearest((r.x0 + r.x1) / 2)
            if g:
                cy = (r.y0 + r.y1) / 2
                out[g]["points"].append(point(cal, cy, unc, ((r.x0 + r.x1) / 2, cy)))
        elif f is None and c is not None and not _black(c) and r.height < 0.01:
            g = nearest((r.x0 + r.x1) / 2)
            if g:
                out[g]["lines"].append(r)
    res = {}
    for g, v in out.items():
        lines = sorted(v["lines"], key=lambda r: -r.width)
        v["points"].sort(key=lambda p: p["value"])
        if not error_bars:
            if len(lines) != 1:
                raise ValueError(f"{g}: expected a mean line only, found {len(lines)} lines")
            lo, hi = cal.interval(lines[0].y0, unc)
            res[g] = {"points": v["points"], "countable": True, "bar": {"mean": [cal.value(lines[0].y0), lo, hi]}}
            continue
        if len(lines) != 3:
            raise ValueError(f"{g}: expected mean line and two caps, found {len(lines)} lines")
        mean, caps = lines[0], lines[1:]
        top = min(caps, key=lambda r: r.y0)
        lo, hi = cal.interval(mean.y0, unc)
        elo, ehi = cal.interval(top.y0, unc)
        v["points"].sort(key=lambda p: p["value"])
        res[g] = {"points": v["points"], "countable": True,
                  "bar": {"mean": [cal.value(mean.y0), lo, hi], "error": [cal.value(top.y0), elo, ehi]}}
    return res


def fan_out(panel, links):
    """links: {figure label: panel group}; the same panel group serves every item that compares it."""
    return {"groups": {label: panel[g] for label, g in links.items()}}


def read_glyph_axis_triangles(fig, tick_values, groups, marker_max=5):
    """Fig. 5A/5B-style dot plots with no y tick marks: the y axis is calibrated from the vertical centres of the
    outlined tick-label glyph rows left of the axis line, paired bottom to top with tick_values. Markers are filled
    triangles (three-segment paths) in one x column per group, left to right in `groups`; the mean is a short black
    horizontal line per column (no error bars drawn). Returns {label: {points, countable, bar}}."""
    ds = fig.drawings()
    axis = [d["rect"] for d in ds if d.get("fill") is None and _black(d.get("color"))
            and d["rect"].width < 0.01 and d["rect"].height > 30]
    if len(axis) != 1:
        raise ValueError(f"found {len(axis)} y axis lines, expected 1")
    ax = axis[0].x0
    glyphs = sorted((d["rect"] for d in ds if _black(d.get("fill")) and d["rect"].x1 < ax - 2
                     and d["rect"].height > 3), key=lambda r: r.y0)   # decimal points are < 1 pt high
    rows = []
    for r in glyphs:
        if rows and abs(rows[-1][0].y0 - r.y0) < 1.0:
            rows[-1].append(r)
        else:
            rows.append([r])
    centres = sorted(((min(g.y0 for g in rs) + max(g.y1 for g in rs)) / 2 for rs in rows), reverse=True)
    if len(centres) != len(tick_values):
        raise ValueError(f"found {len(centres)} tick-label rows, expected {len(tick_values)}")
    cal = calibrate(list(zip(centres, tick_values)))
    unc = VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)
    marks = [d["rect"] for d in ds if d.get("fill") is not None and [i[0] for i in d["items"]] == ["l", "l", "l"]
             and d["rect"].x0 > ax and d["rect"].width < marker_max and d["rect"].height < marker_max]
    cols = sorted({round((r.x0 + r.x1) / 2, 1) for r in marks})
    if len(cols) != len(groups):
        raise ValueError(f"found {len(cols)} marker columns, expected {len(groups)}")
    means = [d["rect"] for d in ds if d.get("fill") is None and _black(d.get("color")) and d["rect"].height < 0.01
             and d["rect"].x0 > ax + 0.5 and d["rect"].width < 9]
    res = {}
    for g, cx in zip(groups, cols):
        pts = []
        for r in marks:
            if abs((r.x0 + r.x1) / 2 - cx) < 0.5:
                cy = (r.y0 + r.y1) / 2
                pts.append(point(cal, cy, unc, (cx, cy)))
        pts.sort(key=lambda p: p["value"])
        ml = [r for r in means if abs((r.x0 + r.x1) / 2 - cx) < 1.5]
        if len(ml) != 1:
            raise ValueError(f"{g}: expected one mean line, found {len(ml)}")
        lo, hi = cal.interval(ml[0].y0, unc)
        res[g] = {"points": pts, "countable": True, "bar": {"mean": [cal.value(ml[0].y0), lo, hi]}}
    return res


def _hidden(d, whites):
    """True when a white fill drawn later covers the whole object (Fig. 5H-5J carry a stale chart layer hidden this way)."""
    r = d["rect"]
    return any(w["seqno"] > d["seqno"] and w["rect"].x0 <= r.x0 and w["rect"].x1 >= r.x1
               and w["rect"].y0 <= r.y0 and w["rect"].y1 >= r.y1 for w in whites)


def read_glyph_axis_colours(fig, tick_values, groups, marker_max=5, colour_tol=0.03):
    """Fig. 5H-5J-style dot plots: filled triangles, one colour per group, a black mean line per column and no error
    bars or y tick marks. The y axis is calibrated from the vertical centres of the outlined tick-label glyph rows just
    left of the axis line, paired bottom to top with tick_values. Objects covered by a later white fill are skipped.
    groups: {label: fill RGB 0-1}. Returns {label: {points, countable, bar}}."""
    ds = fig.drawings()
    whites = [d for d in ds if d.get("fill") is not None and min(d["fill"]) > 0.99 and d["rect"].width > 10]
    ds = [d for d in ds if not _hidden(d, whites)]
    axis = [d["rect"] for d in ds if d.get("fill") is None and _black(d.get("color"))
            and d["rect"].width < 0.01 and d["rect"].height > 30]
    if len(axis) != 1:
        raise ValueError(f"found {len(axis)} y axis lines, expected 1")
    ax, top, bottom = axis[0].x0, axis[0].y0, axis[0].y1
    glyphs = sorted((d["rect"] for d in ds if _black(d.get("fill")) and ax - 12 < d["rect"].x0
                     and d["rect"].x1 < ax - 2 and d["rect"].height > 3), key=lambda r: r.y0)
    rows = []
    for r in glyphs:
        if rows and abs(rows[-1][0].y0 - r.y0) < 1.0:
            rows[-1].append(r)
        else:
            rows.append([r])
    centres = sorted(((min(g.y0 for g in rs) + max(g.y1 for g in rs)) / 2 for rs in rows), reverse=True)
    if len(centres) != len(tick_values):
        raise ValueError(f"found {len(centres)} tick-label rows, expected {len(tick_values)}")
    cal = calibrate(list(zip(centres, tick_values)))
    unc = VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)
    means = [d["rect"] for d in ds if d.get("fill") is None and _black(d.get("color")) and d["rect"].height < 0.01
             and d["rect"].x0 > ax + 0.5 and d["rect"].width < 9 and (d.get("width") or 0) > 0.8]
    res = {}
    for g, rgb in groups.items():
        marks = [d["rect"] for d in ds if d.get("fill") is not None and [i[0] for i in d["items"]] == ["l", "l", "l"]
                 and max(abs(a - b) for a, b in zip(d["fill"], rgb)) < colour_tol
                 and d["rect"].x0 > ax and d["rect"].width < marker_max and d["rect"].height < marker_max
                 and top - 3 < (d["rect"].y0 + d["rect"].y1) / 2 < bottom + 3]
        cols = {round((r.x0 + r.x1) / 2, 1) for r in marks}
        if len(cols) != 1:
            raise ValueError(f"{g}: markers in {len(cols)} columns, expected 1")
        cx = cols.pop()
        pts = []
        for r in marks:
            cy = (r.y0 + r.y1) / 2
            pts.append(point(cal, cy, unc, (cx, cy)))
        pts.sort(key=lambda p: p["value"])
        ml = [r for r in means if abs((r.x0 + r.x1) / 2 - cx) < 1.5]
        if len(ml) != 1:
            raise ValueError(f"{g}: expected one mean line, found {len(ml)}")
        lo, hi = cal.interval(ml[0].y0, unc)
        res[g] = {"points": pts, "countable": True, "bar": {"mean": [cal.value(ml[0].y0), lo, hi]}}
    return res


def read_text_axis_triangles(fig, box, tick_values, groups, marker_max=15):
    """Fig. S3C/E/G-style dot plots inside box (page x0, y0, x1, y1): filled triangles in one x column per group
    (left to right in `groups`), a thick black mean line per column, no error bars and no y tick marks. A stale chart
    layer is covered by a later white fill and skipped. The y tick labels are text, printed twice (the stale layer's
    set sits at the same x); for each value the label nearest the visible y axis line's span is used, and the axis is
    calibrated from those label centres. The gap between the fitted 0 and the visible x axis line is added to the
    interval. Returns {group: {points, countable, bar}}."""
    bx0, by0, bx1, by1 = box

    def inside(r):
        return bx0 <= r.x0 and r.x1 <= bx1 and by0 <= r.y0 and r.y1 <= by1

    every = fig.drawings()
    whites = [d for d in every if d.get("fill") is not None and min(d["fill"]) > 0.99 and 10 < d["rect"].width < 400]
    ds = [d for d in every if inside(d["rect"]) and not _hidden(d, whites)]
    axis = [d["rect"] for d in ds if d.get("fill") is None and _black(d.get("color"))
            and d["rect"].width < 0.01 and d["rect"].height > 30]
    if len(axis) != 1:
        raise ValueError(f"found {len(axis)} y axis lines, expected 1")
    ax, top, bottom = axis[0].x0, axis[0].y0, axis[0].y1
    # the x axis line meets the y axis at its bottom (S3C's stale x axis pokes 1.4 pt out of its white box)
    xaxis = [d["rect"] for d in ds if d.get("fill") is None and _black(d.get("color")) and d["rect"].height < 0.01
             and d["rect"].width > 30 and (d.get("width") or 0) < 1.5 and abs(d["rect"].y0 - bottom) < 0.01]
    if len(xaxis) != 1:
        raise ValueError(f"found {len(xaxis)} x axis lines at the y axis foot, expected 1")
    labels = []
    for x0, y0, x1, y1, t in fig.words():
        if ax - 45 < x0 and x1 < ax and by0 <= y0 and y1 <= by1:
            try:
                labels.append(((y0 + y1) / 2, float(t)))
            except ValueError:
                pass
    lo_v, hi_v = min(tick_values), max(tick_values)
    marks = []
    for v in tick_values:
        guess = bottom + (top - bottom) * (v - lo_v) / (hi_v - lo_v)
        cands = [pos for pos, lv in labels if lv == v]
        if not cands:
            raise ValueError(f"no tick label {v}")
        marks.append((min(cands, key=lambda p: abs(p - guess)), v))
    cal = calibrate(marks)
    offset = abs(xaxis[0].y0 - (0 - cal.intercept) / cal.slope)   # pt between the fitted 0 and the x axis line
    unc = VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope) + offset
    tris = [d["rect"] for d in ds if d.get("fill") is not None and [i[0] for i in d["items"]] == ["l", "l", "l"]
            and d["rect"].x0 > ax and d["rect"].width < marker_max and d["rect"].height < marker_max]
    cols = sorted({round((r.x0 + r.x1) / 2, 1) for r in tris})
    if len(cols) != len(groups):
        raise ValueError(f"found {len(cols)} marker columns, expected {len(groups)}")
    means = [d["rect"] for d in ds if d.get("fill") is None and _black(d.get("color")) and d["rect"].height < 0.01
             and d["rect"].x0 > ax + 0.5 and d["rect"].width < 30 and (d.get("width") or 0) > 2]
    res = {}
    for g, cx in zip(groups, cols):
        pts = []
        for r in tris:
            if abs((r.x0 + r.x1) / 2 - cx) < 0.5:
                cy = (r.y0 + r.y1) / 2
                pts.append(point(cal, cy, unc, (cx, cy)))
        pts.sort(key=lambda p: p["value"])
        ml = [r for r in means if abs((r.x0 + r.x1) / 2 - cx) < 3]
        if len(ml) != 1:
            raise ValueError(f"{g}: expected one mean line, found {len(ml)}")
        lo, hi = cal.interval(ml[0].y0, unc)
        res[g] = {"points": pts, "countable": True, "bar": {"mean": [cal.value(ml[0].y0), lo, hi]}}
    return res
