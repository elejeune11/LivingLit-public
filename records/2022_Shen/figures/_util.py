"""Helpers for 2022_Shen's figures (this paper's alone; 02-audit, Reading figures).

The panels are GraphPad Prism vector drawings, in two styles:
  * stroked (Figs 1, 3, 4, 5): axes, ticks, error bars and bar outlines are stroked
    line paths; markers are small filled paths.
  * filled (Fig 2): every stroke has been converted to a filled shape (thin
    rectangles for lines, a filled polygon for each bar outline).
Both are reduced here to the same primitives: segments (with a colour and a
thickness) and filled marker shapes.

Tick LABELS in main.pdf are drawn as glyph outlines, not text, so fig.words() and
fig.tick_marks() find nothing. Each script therefore calibrates from the tick-MARK
line positions found here, paired in order (bottom to top) with the label values
printed beside them, which the script lists as constants (read from a render of
the label glyphs). The number of tick marks found must equal the number of label
values, otherwise reading fails.

Bar means: in the stroked style Prism draws each error stem as two segments
meeting at the mean, and that vertex is used. Otherwise (the filled style of
Fig. 2, where stems are single rectangles) the outer edge of the bar outline is
used: Prism draws the outline inside the bar, so its outer edge (the filled
polygon's edge, or stroke centre + half the stroke width) is the mean. Where both
exist they agree within 0.05 pt.
"""
from __future__ import annotations

from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

BLACK_MAX = 0.12


def _is_black(c):
    return c is not None and max(c) <= BLACK_MAX


def _same(c, ref, tol=0.06):
    return c is not None and ref is not None and max(abs(a - b) for a, b in zip(c, ref)) <= tol


def drawings(fig):
    """Vector paths inside the crop. FigureSource.drawings() uses Rect.intersects, which is False
    for the zero-width (or zero-height) bounding box of a vertical (horizontal) stroked line, so
    axes, ticks and error stems would be lost; this tests the box's corners against the crop instead."""
    cached = getattr(fig, "_shen_drawings", None)
    if cached is not None:
        return cached
    R = fig.rect
    out = []
    for d in fig.page.get_drawings():
        r = d["rect"]
        if r.x1 >= R.x0 and r.x0 <= R.x1 and r.y1 >= R.y0 and r.y0 <= R.y1:
            out.append(d)
    fig._shen_drawings = out
    return out


def segments(fig):
    """Straight segments: (x0, y0, x1, y1, colour, thickness, drawing_index)."""
    out = []
    for k, d in enumerate(drawings(fig)):
        items = d["items"]
        if d.get("color") is not None and d.get("width"):
            for it in items:
                if it[0] == "l":
                    p, q = it[1], it[2]
                    out.append((p.x, p.y, q.x, q.y, tuple(d["color"]), float(d["width"]), k))
        if d.get("fill") is not None and all(it[0] == "re" for it in items):
            for it in items:
                r = it[1]
                if r.width < 0.9 and r.height > r.width:
                    cx = (r.x0 + r.x1) / 2
                    out.append((cx, r.y0, cx, r.y1, tuple(d["fill"]), r.width, k))
                elif r.height < 0.9 and r.width > r.height:
                    cy = (r.y0 + r.y1) / 2
                    out.append((r.x0, cy, r.x1, cy, tuple(d["fill"]), r.height, k))
    return out


def y_axis(fig, min_len=25):
    """The leftmost long black vertical segment: (x, y_top, y_bottom)."""
    v = [s for s in segments(fig) if _is_black(s[4]) and abs(s[0] - s[2]) < 0.05 and abs(s[1] - s[3]) >= min_len]
    if not v:
        raise ValueError("no y axis found")
    s = min(v, key=lambda s: s[0])
    return s[0], min(s[1], s[3]), max(s[1], s[3])


def y_ticks(fig, axis=None):
    """Page y of the tick marks on the y axis, bottom to top."""
    ax, top, bot = axis or y_axis(fig)
    ys = []
    for s in segments(fig):
        if _is_black(s[4]) and abs(s[1] - s[3]) < 0.05 and 1.5 < abs(s[2] - s[0]) < 4.5:
            xr = max(s[0], s[2])
            if abs(xr - ax) < 0.6 and min(s[0], s[2]) < ax and top - 1 <= s[1] <= bot + 1:
                ys.append(round(s[1], 3))
    ys = sorted(set(ys), reverse=True)
    return ys


def x_axis_and_ticks(fig):
    """The bottom long black horizontal segment (y) and the x of its tick marks, left to right."""
    h = [s for s in segments(fig) if _is_black(s[4]) and abs(s[1] - s[3]) < 0.05 and abs(s[2] - s[0]) >= 25]
    if not h:
        raise ValueError("no x axis found")
    ay = max(s[1] for s in h)
    xs = []
    for s in segments(fig):
        if _is_black(s[4]) and abs(s[0] - s[2]) < 0.05 and 1.5 < abs(s[3] - s[1]) < 4.5:
            if abs(min(s[1], s[3]) - ay) < 0.6:
                xs.append(round(s[0], 3))
    return ay, sorted(set(xs))


def y_calibration(fig, values):
    """Calibrate the y axis from its tick marks paired with the printed label values (bottom to top)."""
    ys = y_ticks(fig)
    if len(ys) != len(values):
        raise ValueError(f"{len(ys)} y tick marks found for {len(values)} label values")
    return calibrate(list(zip(ys, values)))


def markers(fig, colour, size=(1.2, 3.2), tol=0.06):
    """Centres of small filled shapes of one colour; duplicate drawings of the same marker
    (a fill plus its outline, within 0.06 pt) count once."""
    pts = []
    for d in drawings(fig):
        r = d["rect"]
        f = d.get("fill")
        if f is None or not _same(f, colour, tol):
            continue
        if not (size[0] <= r.width <= size[1] and size[0] <= r.height <= size[1]):
            continue
        if abs(r.width - r.height) > 0.3:
            continue
        c = ((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)
        if not fig.rect.contains(c):
            continue
        if any(abs(c[0] - p[0]) < 0.06 and abs(c[1] - p[1]) < 0.06 for p in pts):
            continue
        pts.append(c)
    return pts


def bar(fig, colour, tol=0.06):
    """A bar outline of one colour: (x0, x1, base_y, mean_y). Stroked: a 3-segment path; filled: a polygon."""
    found = []
    for d in drawings(fig):
        r = d["rect"]
        if r.width < 5 or r.width > 20:
            continue
        items = d["items"]
        if d.get("color") is not None and _same(d["color"], colour, tol) and d.get("fill") is None \
                and len(items) == 3 and all(it[0] == "l" for it in items):
            base = items[0][1].y
            end = items[1][1].y
            hw = float(d["width"]) / 2
            mean = end - hw if end < base else end + hw
            found.append((r.x0 - hw, r.x1 + hw, base, mean))
        elif d.get("color") is not None and _same(d["color"], colour, tol) and d.get("fill") is None \
                and len(items) == 1 and items[0][0] == "l" and abs(items[0][1].y - items[0][2].y) < 0.01 \
                and float(d["width"]) >= 0.8:
            # a bar shorter than its outline's stroke width is drawn as one horizontal line
            y = items[0][1].y
            hw = float(d["width"]) / 2
            found.append((r.x0 - hw, r.x1 + hw, None, y))
        elif d.get("fill") is not None and _same(d["fill"], colour, tol) and d.get("color") is None \
                and len(items) >= 8 and all(it[0] == "l" for it in items):
            base = items[0][1].y
            mean = r.y0 if abs(r.y1 - base) < abs(r.y0 - base) else r.y1
            found.append((r.x0, r.x1, base, mean))
    found = [f for f in found if fig.rect.contains(((f[0] + f[1]) / 2, f[3]))]
    if len(found) != 1:
        raise ValueError(f"{len(found)} bars of colour {colour}")
    return found[0]


def error_top(fig, colour, x0, x1, tol=0.06):
    """Page y of the upper end of the error bar drawn in a bar's colour between x0 and x1 (None if none)."""
    ys = []
    for s in segments(fig):
        if not _same(s[4], colour, tol) or s[5] > 0.5:
            continue
        if x0 <= min(s[0], s[2]) and max(s[0], s[2]) <= x1:
            ys += [s[1], s[3]]
    return min(ys) if ys else None


def stem_middle(fig, colour, x0, x1, tol=0.06):
    """Page y of the shared vertex of a two-segment vertical error stem (Prism draws it from the
    mean outwards, so the vertex is the mean); None if the stem is not drawn that way."""
    for d in drawings(fig):
        c = d.get("color")
        items = d["items"]
        if c is None or not _same(c, colour, tol) or d.get("fill") is not None or len(items) != 2:
            continue
        if not all(it[0] == "l" and abs(it[1].x - it[2].x) < 0.01 for it in items):
            continue
        if not (x0 <= items[0][1].x <= x1):
            continue
        a, b = items[0][2], items[1][1]
        if abs(a.y - b.y) < 0.01:
            return a.y
    return None


def _widen(d, cal):
    d["lo"] -= cal.residual
    d["hi"] += cal.residual
    return d


def read_bars(fig, y_values, groups, points_hidden=()):
    """A bar-and-points panel. groups: [(label, colour)]; points_hidden: labels whose points
    are not drawn (bar only). Returns read()'s dict."""
    cal = y_calibration(fig, y_values)
    u = VECTOR_UNCERTAINTY_PT
    out = {}
    for label, colour in groups:
        x0, x1, base, mean_y = bar(fig, colour)
        mid = stem_middle(fig, colour, x0, x1)
        if mid is not None:
            mean_y = mid
        cx = (x0 + x1) / 2
        g = {"points": [], "countable": label not in points_hidden}
        if label not in points_hidden:
            pts = [p for p in markers(fig, colour) if x0 - 3 <= p[0] <= x1 + 3]
            pts.sort(key=lambda p: (p[1], p[0]))
            g["points"] = [_widen(point(cal, p[1], u, p), cal) for p in pts]
        m = _widen(point(cal, mean_y, u, (cx, mean_y)), cal)
        g["bar"] = {"mean": [m["value"], m["lo"], m["hi"]]}
        ey = error_top(fig, colour, x0, x1)
        if ey is not None:
            e = _widen(point(cal, ey, u, (cx, ey)), cal)
            g["bar"]["error"] = [e["value"], e["lo"], e["hi"]]
        out[label] = g
    return {"groups": out}


def read_curve(fig, y_values, x_values, groups, exclude=()):
    """A curve of mean markers against frequency. groups: [(label, colour)]; exclude: page rects
    (x0, y0, x1, y1) to ignore (the legend). Each marker takes the printed x of the x tick it sits on."""
    cal = y_calibration(fig, y_values)
    _, xt = x_axis_and_ticks(fig)
    if len(xt) != len(x_values):
        raise ValueError(f"{len(xt)} x tick marks found for {len(x_values)} label values")
    u = VECTOR_UNCERTAINTY_PT
    out = {}
    for label, colour in groups:
        pts = [p for p in markers(fig, colour)
               if not any(e[0] <= p[0] <= e[2] and e[1] <= p[1] <= e[3] for e in exclude)]
        got = {}
        for p in pts:
            k = min(range(len(xt)), key=lambda i: abs(xt[i] - p[0]))
            if abs(xt[k] - p[0]) > 0.6:
                raise ValueError(f"{label}: marker at x={p[0]:.2f} is on no x tick")
            if k in got:
                raise ValueError(f"{label}: two markers at x tick {x_values[k]}")
            got[k] = p
        out[label] = {"points": [_widen(point(cal, got[k][1], u, got[k], x=x_values[k]), cal) for k in sorted(got)],
                      "countable": False}
    return {"groups": out}
