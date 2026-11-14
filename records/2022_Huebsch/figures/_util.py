"""Helpers for 2022_Huebsch's raster scatter panels (journal_version.pdf, Extended Data Fig. 2g,h).

The page holds one embedded ~300 dpi image; text is not extractable, so axes are calibrated from
the tick marks found in the render, paired with the tick labels printed beside them.
"""
from __future__ import annotations

import numpy as np

from livinglit.figures.source import RASTER_UNCERTAINTY_PX_300DPI, blobs, calibrate, point

DPI = 300


def black(img, level=100):
    """Pixels of black ink (all channels dark), which excludes the red and blue markers."""
    return img.astype(int).max(axis=2) < level


def y_axis(img):
    """Column of the y axis line: the leftmost run of columns that are dark over most of the plot."""
    bk = black(img)
    cols = bk.sum(axis=0)
    tall = [i for i, v in enumerate(cols) if v > 0.6 * img.shape[0]]
    return min(tall)


def tick_rows(img, axis_col):
    """Row centres (darkness weighted) of the tick marks drawn left of the y axis line."""
    dark = 255 - img[:, axis_col - 12:axis_col - 2].astype(float).mean(axis=2)
    hit = (black(img)[:, axis_col - 12:axis_col - 2].sum(axis=1) >= 6)
    rows, cur = [], []
    for r in range(img.shape[0]):
        if hit[r]:
            cur.append(r)
        elif cur:
            rows.append(cur)
            cur = []
    if cur:
        rows.append(cur)
    out = []
    for run in rows:
        lo, hi = run[0] - 1, run[-1] + 2
        w = dark[lo:hi].sum(axis=1)
        out.append(float((np.arange(lo, hi) * w).sum() / w.sum()))
    return out


def axis(img, labels):
    """Calibration (render px row -> axis value) from tick marks, top to bottom, paired with labels;
    and the uncertainty in px: 0.6 px at 300 dpi plus the calibration misfit."""
    ax = y_axis(img)
    ticks = tick_rows(img, ax)
    if len(ticks) != len(labels):
        raise ValueError(f"found {len(ticks)} tick marks, expected {len(labels)}")
    cal = calibrate(list(zip(ticks, labels)))
    return cal, RASTER_UNCERTAINTY_PX_300DPI + cal.residual / abs(cal.slope), ax


def centre_column(img, near, half=14, top=None, bottom=None):
    """The vertical error-bar line of a group: the column near `near` with most black pixels."""
    bk = black(img)[top:bottom]
    lo, hi = near - half, near + half
    counts = bk[:, lo:hi].sum(axis=0)
    best = np.flatnonzero(counts >= counts.max() - 1)
    return float(lo + best.mean())


def bar_rows(img, col, bottom, through_centre=True, min_width=18, half=45):
    """Horizontal black strokes of a group's error bar, top to bottom, as (row, width): the caps and the mean line.
    through_centre: a stroke is the black run through the centre column (groups with black markers, which lie
    off the centre). Otherwise a stroke is the black ink within `half` px of the centre column, leaving out the
    vertical line (groups with coloured markers, which may hide the middle of a cap). Strokes that fill the
    whole window are significance brackets and are left out. Rows at or below `bottom` (the x axis) are ignored."""
    bk = black(img)
    ink = coloured(img, "red") | coloured(img, "blue")
    c = int(round(col))
    feats, cur = [], []
    for r in range(bottom):
        if through_centre:
            if not bk[r, c - 1:c + 2].any():
                width = 0
            else:
                x0 = c
                while x0 > 0 and bk[r, x0 - 1]:
                    x0 -= 1
                x1 = c
                while x1 < bk.shape[1] - 1 and bk[r, x1 + 1]:
                    x1 += 1
                width = x1 - x0 + 1
            bracket = width > 2 * half
        else:
            win = bk[r, c - half:c + half + 1].copy()
            win[half - 3:half + 4] = False
            width = int(win.sum())
            # a cap or mean line meets the vertical line (or a marker drawn over it) 5 rows above or below;
            # significance brackets and p-value text above the bars do not
            near = [rr for rr in (r - 5, r + 5) if 0 <= rr < bk.shape[0]]
            attached = any(bk[rr, c - 1:c + 2].any() or ink[rr, c - 1:c + 2].any() for rr in near)
            bracket = bool(win[0] and win[-1]) or not attached
        if width >= min_width and not bracket:
            cur.append((r, width))
        elif cur:
            feats.append(cur)
            cur = []
    if cur:
        feats.append(cur)
    return [(float(np.mean([r for r, _ in f])), max(w for _, w in f)) for f in feats]


def bar(cal, unc, fig, scale, col, rows):
    """{"mean", "error"}: the mean is the widest stroke, the error the topmost (upper end of the SD bar)."""
    mean_row = max(rows, key=lambda f: f[1])[0]
    top_row = rows[0][0]
    m = point(cal, mean_row, unc, fig.to_page(col, mean_row, scale))
    e = point(cal, top_row, unc, fig.to_page(col, top_row, scale))
    return {"mean": [m["value"], m["lo"], m["hi"]], "error": [e["value"], e["lo"], e["hi"]]}


def coloured(img, kind):
    """Mask of the red or blue marker fill."""
    r = img.astype(int)
    if kind == "red":
        return (r[:, :, 0] > 150) & (r[:, :, 1] < 120) & (r[:, :, 2] < 120)
    return (r[:, :, 2] > 100) & (r[:, :, 0] < 100) & (r[:, :, 2] - r[:, :, 0] > 50)


def markers(img, kind, x_lo, x_hi, single=(140, 300)):
    """Marker blobs of one colour between two columns; and whether every blob is one marker standing alone
    (area within the single-marker range)."""
    bs = [b for b in blobs(coloured(img, kind), min_area=5) if x_lo <= b["x"] <= x_hi]
    alone = all(single[0] <= b["area"] <= single[1] for b in bs)
    return sorted(bs, key=lambda b: b["y"]), alone


PDF_LABELS = [0.8, 0.6, 0.4, 0.2, 0.0]  # y tick labels of panels g and h, top to bottom
X_AXIS_ROW = 405  # render rows at and below this are the x axis and the media table under it
SINGLE = {"red": (240, 300), "blue": (150, 175)}  # area (px at 300 dpi) of one square / one circle marker


def read_group(fig, img, scale, cal, unc, near, colour=None):
    """One group of a scatter-with-mean±SD panel: its bar (mean, upper end of SD) and, when every marker of
    the group's colour stands alone, its points. Black markers lie on the black bar and are never counted."""
    col = centre_column(img, near, bottom=X_AXIS_ROW)
    rows = bar_rows(img, col, X_AXIS_ROW, through_centre=colour is None, min_width=18 if colour is None else 8)
    g = {"points": [], "countable": False, "bar": bar(cal, unc, fig, scale, col, rows)}
    if colour is not None:
        bs, alone = markers(img, colour, col - 60, col + 60, SINGLE[colour])
        if alone:
            g["countable"] = True
            g["points"] = [point(cal, b["y"], unc, fig.to_page(b["x"], b["y"], scale)) for b in bs]
    return g


# --- vector scatter-with-bar panels (journal_version.pdf, Fig. 2e) -------------------------------------------

RED, BLUE = (0.87, 0.16, 0.16), (0.25, 0.34, 0.65)  # Fig. 2: SM red squares, MM blue circles
BLACK = (0.0, 0.0, 0.0)


def _rgb(c):
    return tuple(round(v, 2) for v in c) if c else None


def _lines(d):
    """A path's straight segments as (x0, y0, x1, y1)."""
    return [(it[1].x, it[1].y, it[2].x, it[2].y) for it in d["items"] if it[0] == "l"]


def vector_axis(fig):
    """Calibration (page y -> axis value) from the y axis path's tick lines, each paired with the numeric label
    printed level with it just left of the axis; and the uncertainty in pt: 0.5 pt plus the calibration misfit."""
    from livinglit.figures.source import VECTOR_UNCERTAINTY_PT
    for d in fig.drawings():
        if _rgb(d.get("color")) != BLACK:
            continue
        ls = _lines(d)
        vert = [l for l in ls if abs(l[0] - l[2]) < 0.01 and abs(l[1] - l[3]) > 50]
        ticks = [l for l in ls if abs(l[1] - l[3]) < 0.01 and abs(l[0] - l[2]) < 4]
        if len(vert) == 1 and len(ticks) >= 2:
            break
    else:
        raise ValueError("no y axis path with tick lines found")
    ax = vert[0][0]
    labels = []
    for x0, y0, x1, y1, t in fig.words():
        try:
            v = float(t.replace("−", "-"))
        except ValueError:
            continue
        if 0 < ax - x1 < 12:
            labels.append(((y0 + y1) / 2, v))
    marks = []
    for l in ticks:
        pos, v = min(labels, key=lambda m: abs(m[0] - l[1]))
        if abs(pos - l[1]) > 1.5:
            raise ValueError(f"tick at y={l[1]} has no label level with it")
        marks.append((l[1], v))
    cal = calibrate(marks)
    return cal, VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)


def category_ticks(fig):
    """Page x of the x axis's category ticks (short vertical lines hanging from the long horizontal axis line)."""
    for d in fig.drawings():
        if _rgb(d.get("color")) != BLACK:
            continue
        ls = _lines(d)
        horiz = [l for l in ls if abs(l[1] - l[3]) < 0.01 and abs(l[0] - l[2]) > 50]
        ticks = [l for l in ls if abs(l[0] - l[2]) < 0.01 and 0 < abs(l[1] - l[3]) < 4]
        if len(horiz) == 1 and len(ticks) >= 2:
            return sorted(l[0] for l in ticks)
    raise ValueError("no x axis path with category ticks found")


def vector_markers(fig, colours, max_size=6.0):
    """Centres of markers drawn in any of `colours` (stroke or fill): small rectangles, and circles of four
    Bezier curves, including several circles drawn as one compound path. A fill and an outline drawn as two
    paths at the same centre are one marker."""
    out = []
    for d in fig.drawings():
        if _rgb(d.get("color")) not in colours and _rgb(d.get("fill")) not in colours:
            continue
        items = d["items"]
        if items and all(it[0] == "c" for it in items) and len(items) % 4 == 0:
            for k in range(0, len(items), 4):
                pts = [q for it in items[k:k + 4] for q in it[1:]]
                xs, ys = [q.x for q in pts], [q.y for q in pts]
                if max(xs) - min(xs) <= max_size:
                    out.append(((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2))
        elif len(items) == 1 and items[0][0] == "re":
            r = items[0][1]
            if r.width <= max_size and r.height <= max_size:
                out.append(((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2))
    uniq = []
    for p in sorted(out):
        if not any(abs(p[0] - q[0]) < 0.05 and abs(p[1] - q[1]) < 0.05 for q in uniq):
            uniq.append(p)
    return uniq


def error_bars(fig, cap_max=8):
    """Black mean ± s.d. bars: [(x, mean y, upper cap y)]. Each is one path of two caps (narrower than `cap_max` pt)
    and a vertical line drawn in two halves that meet at the mean (the bar's top edge sits half a line width above it)."""
    out = []
    for d in fig.drawings():
        ls = _lines(d)
        if _rgb(d.get("color")) != BLACK or len(ls) != 4 or len(d["items"]) != 4:
            continue
        caps = [l for l in ls if abs(l[1] - l[3]) < 0.01 and abs(l[0] - l[2]) < cap_max]
        vert = [l for l in ls if abs(l[0] - l[2]) < 0.01]
        if len(caps) != 2 or len(vert) != 2:
            continue
        a, b = {vert[0][1], vert[0][3]}, {vert[1][1], vert[1][3]}
        joint = [y for y in a if any(abs(y - z) < 0.01 for z in b)]
        if len(joint) != 1:
            continue
        out.append((vert[0][0], joint[0], min(c[1] for c in caps)))
    return out


def read_vector_groups(fig, groups):
    """groups: {label: (category index, marker colours)}. Markers and error bars belong to the nearest category
    tick. Returns read() groups: every point (top to bottom), the mean and the upper end of the s.d. bar."""
    cal, unc = vector_axis(fig)
    cats = category_ticks(fig)
    near = lambda x: min(range(len(cats)), key=lambda i: abs(cats[i] - x))
    bars = error_bars(fig)
    res = {}
    for label, (ci, colours) in groups.items():
        pts = sorted((p for p in vector_markers(fig, colours) if near(p[0]) == ci), key=lambda p: p[1])
        (bx, my, ty), = [b for b in bars if near(b[0]) == ci]
        m, e = point(cal, my, unc, (bx, my)), point(cal, ty, unc, (bx, ty))
        res[label] = {"points": [point(cal, p[1], unc, p) for p in pts], "countable": True,
                      "bar": {"mean": [m["value"], m["lo"], m["hi"]], "error": [e["value"], e["lo"], e["hi"]]}}
    return res


# --- vector scatter-with-bar panels with split axis paths (journal_version.pdf, Fig. 3c) ---------------------

BLUE3 = (0.23, 0.28, 0.62)  # Fig. 3 blue (Fig. 2's is BLUE)


def split_vector_axis(fig, n_ticks):
    """Calibration (page y -> axis value) when the y axis line and each tick are separate paths: the short horizontal
    lines ending at the axis line, each paired with the numeric label (thousands commas removed) printed level with it
    just left of the axis; and the uncertainty in pt: 0.5 pt plus the calibration misfit."""
    from livinglit.figures.source import VECTOR_UNCERTAINTY_PT
    lines = [l for d in fig.drawings() if _rgb(d.get("color")) == BLACK for l in _lines(d)]
    ax = min(l[0] for l in lines if abs(l[0] - l[2]) < 0.01 and abs(l[1] - l[3]) > 50)  # leftmost (bar sides are long too)
    ticks = [l for l in lines if abs(l[1] - l[3]) < 0.01 and abs(max(l[0], l[2]) - ax) < 0.05
             and 0 < abs(l[0] - l[2]) < 4]
    labels = []
    for x0, y0, x1, y1, t in fig.words():
        try:
            v = float(t.replace("−", "-").replace(",", ""))
        except ValueError:
            continue
        if 0 < ax - x1 < 12:
            labels.append(((y0 + y1) / 2, v))
    marks = []
    for l in ticks:
        pos, v = min(labels, key=lambda m: abs(m[0] - l[1]))
        if abs(pos - l[1]) > 1.5:
            raise ValueError(f"tick at y={l[1]} has no label level with it")
        marks.append((l[1], v))
    if len(marks) != n_ticks:
        raise ValueError(f"expected {n_ticks} y ticks, found {len(marks)}")
    cal = calibrate(marks)
    return cal, VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)


def compound_markers(fig, colour, max_size=6.0):
    """Centres of markers in `colour`: every rectangle of a path of rectangles (one or several), and circles of four
    Bezier curves (one or several per path). A fill and an outline drawn as two paths at the same centre are one."""
    out = []
    for d in fig.drawings():
        if _rgb(d.get("color")) != colour and _rgb(d.get("fill")) != colour:
            continue
        items = d["items"]
        if items and all(it[0] == "re" for it in items):
            for it in items:
                r = it[1]
                if r.width <= max_size and r.height <= max_size:
                    out.append(((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2))
        elif items and all(it[0] == "c" for it in items) and len(items) % 4 == 0:
            for k in range(0, len(items), 4):
                pts = [q for it in items[k:k + 4] for q in it[1:]]
                xs, ys = [q.x for q in pts], [q.y for q in pts]
                if max(xs) - min(xs) <= max_size:
                    out.append(((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2))
    uniq = []
    for p in sorted(out):
        if not any(abs(p[0] - q[0]) < 0.05 and abs(p[1] - q[1]) < 0.05 for q in uniq):
            uniq.append(p)
    return uniq


def read_split_axis_groups(fig, groups, n_ticks, cap_max=8):
    """groups: {label: (category index, marker colour)}. As read_vector_groups, for panels whose axis ticks are
    separate paths and whose open markers are compound paths."""
    cal, unc = split_vector_axis(fig, n_ticks)
    cats = category_ticks(fig)
    near = lambda x: min(range(len(cats)), key=lambda i: abs(cats[i] - x))
    bars = error_bars(fig, cap_max)
    res = {}
    for label, (ci, colour) in groups.items():
        pts = sorted((p for p in compound_markers(fig, colour) if near(p[0]) == ci), key=lambda p: p[1])
        (bx, my, ty), = [b for b in bars if near(b[0]) == ci]
        m, e = point(cal, my, unc, (bx, my)), point(cal, ty, unc, (bx, ty))
        res[label] = {"points": [point(cal, p[1], unc, p) for p in pts], "countable": True,
                      "bar": {"mean": [m["value"], m["lo"], m["hi"]], "error": [e["value"], e["lo"], e["hi"]]}}
    return res


# --- vector log-axis bars with points (journal_version.pdf, Fig. 5a,b) ---------------------------------------

GREEN5 = (0.17, 0.7, 0.29)  # Fig. 5 adult heart triangles


def log_vector_axis(fig):
    """Calibration (page y -> axis value, log scale) from the y axis path's major ticks (its longest tick lines; the
    minor ticks are shorter), each paired with the numeric label printed level with it just left of the axis; and the
    uncertainty in pt: 0.5 pt plus the calibration misfit."""
    from livinglit.figures.source import VECTOR_UNCERTAINTY_PT
    for d in fig.drawings():
        if _rgb(d.get("color")) != BLACK:
            continue
        ls = _lines(d)
        vert = [l for l in ls if abs(l[0] - l[2]) < 0.01 and abs(l[1] - l[3]) > 50]
        ticks = [l for l in ls if abs(l[1] - l[3]) < 0.01 and 0 < abs(l[0] - l[2]) < 4]
        if len(vert) == 1 and len(ticks) >= 2:
            break
    else:
        raise ValueError("no y axis path with tick lines found")
    ax = vert[0][0]
    longest = max(abs(l[0] - l[2]) for l in ticks)
    major = [l for l in ticks if abs(l[0] - l[2]) > longest - 0.1]
    labels = []
    for x0, y0, x1, y1, t in fig.words():
        try:
            v = float(t.replace("−", "-"))
        except ValueError:
            continue
        if 0 < ax - x1 < 12 and v > 0:
            labels.append(((y0 + y1) / 2, v))
    marks = []
    for l in major:
        pos, v = min(labels, key=lambda m: abs(m[0] - l[1]))
        if abs(pos - l[1]) > 1.5:
            raise ValueError(f"tick at y={l[1]} has no label level with it")
        marks.append((l[1], v))
    cal = calibrate(marks, log=True)
    return cal, VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)


def split_log_vector_axis(fig):
    """As log_vector_axis, when the y axis line and each tick are separate paths (Fig. 5b): the major ticks are the
    longest short horizontal lines ending at the axis line (the minor ticks are shorter)."""
    from livinglit.figures.source import VECTOR_UNCERTAINTY_PT
    lines = [l for d in fig.drawings() if _rgb(d.get("color")) == BLACK for l in _lines(d)]
    ax = min(l[0] for l in lines if abs(l[0] - l[2]) < 0.01 and abs(l[1] - l[3]) > 50)
    ticks = [l for l in lines if abs(l[1] - l[3]) < 0.01 and abs(max(l[0], l[2]) - ax) < 0.05
             and 0 < abs(l[0] - l[2]) < 4]
    longest = max(abs(l[0] - l[2]) for l in ticks)
    major = [l for l in ticks if abs(l[0] - l[2]) > longest - 0.1]
    labels = []
    for x0, y0, x1, y1, t in fig.words():
        try:
            v = float(t.replace("−", "-"))
        except ValueError:
            continue
        if 0 < ax - x1 < 12 and v > 0:
            labels.append(((y0 + y1) / 2, v))
    marks = []
    for l in major:
        pos, v = min(labels, key=lambda m: abs(m[0] - l[1]))
        if abs(pos - l[1]) > 1.5:
            raise ValueError(f"tick at y={l[1]} has no label level with it")
        marks.append((l[1], v))
    cal = calibrate(marks, log=True)
    return cal, VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)


def white_bars(fig):
    """Bars: narrow white-filled rectangles, as x centres, left to right."""
    out = []
    for d in fig.drawings():
        items = d["items"]
        if _rgb(d.get("fill")) == (1.0, 1.0, 1.0) and len(items) == 1 and items[0][0] == "re":
            r = items[0][1]
            if 2 < r.width < 8 and r.height > 0.1:
                out.append((r.x0 + r.x1) / 2)
    return sorted(out)


def triangle_markers(fig, colour, max_size=4.0):
    """Centres (bounding-box centres) of triangle markers: filled paths of two lines in `colour` (each also has an
    outline path of three lines, not counted again)."""
    out = []
    for d in fig.drawings():
        r = d["rect"]
        if _rgb(d.get("fill")) == colour and [it[0] for it in d["items"]] == ["l", "l"] \
                and r.width <= max_size and r.height <= max_size:
            out.append(((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2))
    return sorted(out)


def read_log_bars(fig, groups, centre_kind, axis=log_vector_axis):
    """groups: {label: (bar index, left to right; marker shape "square" red, "circle" blue or "triangle" green)}.
    A marker belongs to the bar nearest it in x. Returns read() groups: every point (top to bottom); the bar's central
    value (where the error bar's two halves meet) under `centre_kind`, as the legend names it; and the upper end of the
    error bar. `axis` calibrates the y axis (log_vector_axis or split_log_vector_axis)."""
    cal, unc = axis(fig)
    bars = white_bars(fig)
    marks = {"square": compound_markers(fig, RED), "circle": compound_markers(fig, BLUE3),
             "triangle": triangle_markers(fig, GREEN5)}
    nearest = lambda x: min(range(len(bars)), key=lambda i: abs(bars[i] - x))
    ebars = error_bars(fig)
    res = {}
    for label, (bi, shape) in groups.items():
        pts = sorted((p for p in marks[shape] if nearest(p[0]) == bi), key=lambda p: p[1])
        (ex, my, ty), = [b for b in ebars if nearest(b[0]) == bi]
        m, e = point(cal, my, unc, (ex, my)), point(cal, ty, unc, (ex, ty))
        res[label] = {"points": [point(cal, p[1], unc, p) for p in pts], "countable": True,
                      "bar": {centre_kind: [m["value"], m["lo"], m["hi"]], "error": [e["value"], e["lo"], e["hi"]]}}
    return res


def read_log_errorbar_groups(fig, labels, axis=split_log_vector_axis):
    """labels: [(label, marker shape "square" red or "circle" blue)], one per error bar, left to right (Fig. 5e, whose
    bars are outlines, not white-filled rectangles). A marker belongs to the error bar nearest it in x. Returns read()
    groups as read_log_bars, with the error bar's central value stored as mean. Legend markers (level with a word "SM"
    or "MM" printed just right of them) are left out."""
    cal, unc = axis(fig)
    ebars = sorted(error_bars(fig))
    if len(ebars) != len(labels):
        raise ValueError(f"found {len(ebars)} error bars, expected {len(labels)}")
    legend = [(x0, (y0 + y1) / 2) for x0, y0, x1, y1, t in fig.words() if t in ("SM", "MM")]
    in_legend = lambda p: any(0 < wx - p[0] < 8 and abs(wy - p[1]) < 2 for wx, wy in legend)
    marks = {"square": [p for p in compound_markers(fig, RED) if not in_legend(p)],
             "circle": [p for p in compound_markers(fig, BLUE3) if not in_legend(p)]}
    nearest = lambda x: min(range(len(ebars)), key=lambda i: abs(ebars[i][0] - x))
    res = {}
    for bi, (label, shape) in enumerate(labels):
        pts = sorted((p for p in marks[shape] if nearest(p[0]) == bi), key=lambda p: p[1])
        ex, my, ty = ebars[bi]
        m, e = point(cal, my, unc, (ex, my)), point(cal, ty, unc, (ex, ty))
        res[label] = {"points": [point(cal, p[1], unc, p) for p in pts], "countable": True,
                      "bar": {"mean": [m["value"], m["lo"], m["hi"]], "error": [e["value"], e["lo"], e["hi"]]}}
    return res


# --- vector log-axis bars with points, no error bars drawn (journal_version.pdf, Fig. 7g,h) ------------------

F7_GROUPS = {"2D SM": 0, "MPS standard media": 1, "MPS maturation media": 2}  # bar order within each drug


def _power_label(t):
    """A tick label printed as 10 with a superscript exponent flattened into the word ("10–1", "100", "105")."""
    if not t.startswith("10") or len(t) < 3:
        return None
    try:
        return 10.0 ** int(t[2:].replace("–", "-").replace("−", "-"))
    except ValueError:
        return None


def power_log_axis(fig):
    """Calibration (page y -> axis value, log scale) when the y axis line and each tick are separate paths and the
    labels are powers of ten whose exponents extraction flattens into the word: the major ticks are the longest short
    horizontal lines ending at the axis line, each paired with the label level with it; and the uncertainty in pt:
    0.5 pt plus the calibration misfit."""
    from livinglit.figures.source import VECTOR_UNCERTAINTY_PT
    lines = [l for d in fig.drawings() if _rgb(d.get("color")) == BLACK for l in _lines(d)]
    ax = min(l[0] for l in lines if abs(l[0] - l[2]) < 0.01 and abs(l[1] - l[3]) > 50)
    ticks = [l for l in lines if abs(l[1] - l[3]) < 0.01 and abs(max(l[0], l[2]) - ax) < 0.05
             and 0 < abs(l[0] - l[2]) < 4]
    longest = max(abs(l[0] - l[2]) for l in ticks)
    major = [l for l in ticks if abs(l[0] - l[2]) > longest - 0.1]
    labels = []
    for x0, y0, x1, y1, t in fig.words():
        v = _power_label(t)
        if v is not None and 0 < ax - x1 < 12:
            labels.append(((y0 + y1) / 2, v))
    marks = []
    for l in major:
        pos, v = min(labels, key=lambda m: abs(m[0] - l[1]))
        if abs(pos - l[1]) > 1.5:
            raise ValueError(f"tick at y={l[1]} has no label level with it")
        marks.append((l[1], v))
    cal = calibrate(marks, log=True)
    return cal, VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)


def white_bar_tops(fig, min_width=6, max_width=12):
    """Bars: white-filled rectangles, as (x centre, value y), left to right. Each has a black outline path whose top
    line is centred on the fill's top edge; the bar's value is the outline's outer edge, half its line width above
    (in Fig. 7g,h the arithmetic mean of a bar's points lies there, not at the fill's edge, in all 18 bars)."""
    ds = fig.drawings()
    outlines = [d for d in ds if _rgb(d.get("color")) == BLACK and d.get("width") and len(_lines(d)) == 5]
    out = []
    for d in ds:
        items = d["items"]
        if _rgb(d.get("fill")) == (1.0, 1.0, 1.0) and len(items) == 1 and items[0][0] == "re":
            r = items[0][1]
            if min_width < r.width < max_width:
                o, = [o for o in outlines if abs(o["rect"].y0 - r.y0) < 0.01 and o["rect"].x0 < r.x0 < o["rect"].x1]
                out.append(((r.x0 + r.x1) / 2, r.y0 - o["width"] / 2))
    return sorted(out)


def read_drug_bars(fig, drug, labels):
    """Fig. 7g,h: three drugs (category ticks left to right Flecainide, Verapamil, Alfuzosin), three bars each
    (2D SM black triangles, MPS standard media red squares, MPS maturation media blue circles). `drug` is the category
    index, `labels` the groups to return. A marker belongs to the bar nearest it in x; legend markers (level with a word
    "2D" or "MPS" printed just right of them) are left out. No error bars are drawn, so each group gives its points and
    the bar's top (as mean, the legend's "mean ± s.e.m.")."""
    cal, unc = power_log_axis(fig)
    bars = white_bar_tops(fig)
    if len(bars) != 9:
        raise ValueError(f"found {len(bars)} bars, expected 9")
    legend = [(x0, (y0 + y1) / 2) for x0, y0, x1, y1, t in fig.words() if t in ("2D", "MPS")]
    in_legend = lambda p: any(0 < wx - p[0] < 8 and abs(wy - p[1]) < 2 for wx, wy in legend)
    marks = {0: triangle_markers(fig, BLACK, max_size=4.5), 1: compound_markers(fig, RED),
             2: compound_markers(fig, BLUE)}
    nearest = lambda x: min(range(len(bars)), key=lambda i: abs(bars[i][0] - x))
    res = {}
    for label in labels:
        k = F7_GROUPS[label]
        bi = 3 * drug + k
        pts = sorted((p for p in marks[k] if not in_legend(p) and nearest(p[0]) == bi), key=lambda p: p[1])
        bx, by = bars[bi]
        m = point(cal, by, unc, (bx, by))
        res[label] = {"points": [point(cal, p[1], unc, p) for p in pts], "countable": True,
                      "bar": {"mean": [m["value"], m["lo"], m["hi"]]}}
    return res


# --- vector log-axis bars with points and s.e.m. bars (journal_version.pdf, Fig. 8g,h) -----------------------

def open_bar_tops(fig):
    """Bars drawn as open outlines (no fill): each outline path of one group holds the group's three bars, five lines
    each (left side, top, right side). Returns (x centre, value y), left to right; the value is the outline's outer
    edge, half its line width above the top line (as in white_bar_tops)."""
    out = []
    for d in fig.drawings():
        ls = _lines(d)
        if _rgb(d.get("color")) == BLACK and (d.get("width") or 0) > 0.8 and len(ls) == 15:
            for k in range(0, 15, 5):
                seg = ls[k:k + 5]
                out.append(((seg[0][0] + seg[4][0]) / 2, seg[2][1] - d["width"] / 2))
    return sorted(out)


def sem_bars(fig):
    """Error bars drawn as paths of five thin lines each (cap, half cap, vertical line, half cap, cap):
    (x, upper cap y), left to right."""
    out = []
    for d in fig.drawings():
        ls = _lines(d)
        if _rgb(d.get("color")) == BLACK and (d.get("width") or 1) < 0.8 and len(ls) % 5 == 0 and len(ls) >= 5:
            for k in range(0, len(ls), 5):
                v = ls[k + 2]
                if abs(v[0] - v[2]) < 0.01 and abs(v[1] - v[3]) > 0.1:
                    out.append((v[0], min(v[1], v[3])))
    return sorted(out)


def read_sem_drug_bars(fig, drug, labels):
    """Fig. 8g,h: three drugs (Flecainide, Verapamil, Alfuzosin left to right), three open bars each (2D SM black
    triangles, MPS standard media red squares, MPS maturation media blue circles) with s.e.m. bars. `drug` is the
    category index, `labels` the groups to return. A marker belongs to the bar nearest it in x. Each group gives its
    points, the bar's top (mean) and the upper cap of its error bar."""
    cal, unc = power_log_axis(fig)
    bars, caps = open_bar_tops(fig), sem_bars(fig)
    if len(bars) != 9 or len(caps) != 9:
        raise ValueError(f"found {len(bars)} bars and {len(caps)} error bars, expected 9 each")
    marks = {0: triangle_markers(fig, BLACK, max_size=4.5), 1: compound_markers(fig, RED),
             2: compound_markers(fig, BLUE)}
    nearest = lambda x: min(range(len(bars)), key=lambda i: abs(bars[i][0] - x))
    res = {}
    for label in labels:
        k = F7_GROUPS[label]
        bi = 3 * drug + k
        pts = sorted((p for p in marks[k] if nearest(p[0]) == bi), key=lambda p: p[1])
        bx, by = bars[bi]
        (cx, cy), = [c for c in caps if nearest(c[0]) == bi]
        m, e = point(cal, by, unc, (bx, by)), point(cal, cy, unc, (cx, cy))
        res[label] = {"points": [point(cal, p[1], unc, p) for p in pts], "countable": True,
                      "bar": {"mean": [m["value"], m["lo"], m["hi"]], "error": [e["value"], e["lo"], e["hi"]]}}
    return res


# --- raster bars with black or coloured markers on them (journal_version.pdf, Extended Data Fig. 3g,h) ----------
# Markers sit on the bar outlines and error bars, so strokes are found as runs of ink through the error-bar line and
# told apart by width and by what continues below them. A stroke whose run of rows is thicker than one line (a marker
# merged with it) gets an interval covering every place the line could lie within the run.

def outline(img, near, row, half=32):
    """Outer columns of a bar's two side lines at a row inside the bar, and the line width (px)."""
    bk = black(img)[row]
    runs, s = [], None
    for c in range(near - half, near + half + 2):
        if bk[c] and s is None:
            s = c
        elif not bk[c] and s is not None:
            runs.append((s, c - 1))
            s = None
    (a0, a1), (b0, b1) = runs[0], runs[-1]
    return a0, b1, (a1 - a0 + b1 - b0 + 2) / 2


def strokes_through(img, col, bottom, ink):
    """Horizontal runs of `ink` through the error-bar column, grouped into strokes over consecutive rows of width
    >= 15 px: (first row, last row, widest run, (run start, run end) on the widest row)."""
    c = int(round(col))
    feats, cur = [], []
    for r in range(bottom):
        x0 = x1 = c
        if ink[r, c]:
            while x0 > 0 and ink[r, x0 - 1]:
                x0 -= 1
            while x1 < ink.shape[1] - 1 and ink[r, x1 + 1]:
                x1 += 1
        if ink[r, c] and x1 - x0 + 1 >= 15:
            cur.append((r, x1 - x0 + 1, x0, x1))
        elif cur:
            feats.append(cur)
            cur = []
    if cur:
        feats.append(cur)
    out = []
    for f in feats:
        w = max(f, key=lambda t: t[1])
        out.append((f[0][0], f[-1][0], w[1], (w[2], w[3])))
    return out


def line_in_run(cal, unc, fig, scale, col, first, last, lw):
    """A line of width lw lying somewhere in rows first..last: value at the middle of the places it can lie,
    interval covering all of them (plus unc)."""
    a, b = first + (lw - 1) / 2, last - (lw - 1) / 2
    if b < a:
        a = b = (first + last) / 2
    mid = (a + b) / 2
    return point(cal, mid, unc + (b - a) / 2, fig.to_page(col, mid, scale))


def bar_and_cap(img, cal, unc, fig, scale, near, x_axis, ink, lw=None):
    """A bar's mean (top line of the open bar) and the upper end of its error bar. The bar top is the topmost
    stroke through the centre spanning the bar from side to side whose side lines continue below it; the cap is
    the topmost black stroke above it at least 20 px wide, narrower than the bar and attached to the error-bar line
    below (brackets are not; a run of marker colour is not a cap). Side lines may run under markers, so `ink`
    counts for them. `lw` overrides the line width where markers cover the bar's sides near the x axis.
    Returns (bar dict, centre column, side columns, line width); the error is left out when no cap shows."""
    bk = black(img)
    col = centre_column(img, near, bottom=x_axis - 5)
    x0, x1, side_lw = outline(img, near, x_axis - 5)
    lw = lw or side_lw
    width = x1 - x0 + 1
    fs = strokes_through(img, col, x_axis - 5, ink)

    def sides_go_on(last):
        below = range(last + 2, min(last + 17, x_axis - 3))
        return len(below) > 0 and all(ink[r, x0:x0 + 3].any() and ink[r, x1 - 2:x1 + 1].any() for r in below)

    def on_bar(f):
        return f[2] >= 0.85 * width and abs(f[3][0] - x0) <= 3 and abs(f[3][1] - x1) <= 3

    top = [f for f in fs if on_bar(f) and sides_go_on(f[1])][0]
    m = line_in_run(cal, unc, fig, scale, col, top[0], top[1], lw)
    bar = {"mean": [m["value"], m["lo"], m["hi"]]}
    c = int(round(col))
    caps = [f for f in strokes_through(img, col, x_axis - 5, bk)
            if f[1] + 6 < top[0] and 20 <= f[2] < 0.85 * width and bk[f[1] + 4:f[1] + 7, c - 1:c + 2].any()]
    if caps:
        e = line_in_run(cal, unc, fig, scale, col, caps[0][0], caps[0][1], lw)
        bar["error"] = [e["value"], e["lo"], e["hi"]]
    return bar, col, (x0, x1), lw


def black_markers(img, x0, x1, top, bottom, lw):
    """Solid black markers between two columns: cores left when black ink is eroded by a square wider than any
    line (lines vanish, markers shrink about their centre). Returns the cores' blobs, top to bottom, and the
    square's side (px)."""
    import cv2
    k = int(round(lw)) + 3
    core = cv2.erode(black(img).astype(np.uint8), np.ones((k, k), np.uint8)).astype(bool)
    bs = [b for b in blobs(core, min_area=3) if x0 <= b["x"] <= x1 and top <= b["y"] <= bottom]
    return sorted(bs, key=lambda b: b["y"]), k


TRIANGLE_H = 19  # height (px at 300 dpi) of one Extended Data Fig. 3g,h triangle marker, from one free of all lines


def coloured_group(img, cal, unc, fig, scale, near, x_axis, ink, colour, single, lw=None):
    """A group of red or blue markers on an open bar: its bar, and its points only when every marker stands alone."""
    bar, col, _, lw = bar_and_cap(img, cal, unc, fig, scale, near, x_axis, ink, lw)
    g = {"points": [], "countable": False, "bar": bar}
    bs, alone = markers(img, colour, col - 40, col + 40, single)
    if alone:
        g["countable"] = True
        g["points"] = [point(cal, b["y"], unc, fig.to_page(b["x"], b["y"], scale)) for b in bs]
    return g, lw


def black_group(img, cal, unc, fig, scale, near, x_axis, ink, shape, lw=None):
    """A group of solid black markers on an open bar: its bar and one point per marker core. A core merged with a
    line may lie up to half the eroding square off the marker's centre, and a triangle's plotted position may be
    its centroid (the core's centre) or its box centre, TRIANGLE_H / 6 apart: both widen the interval."""
    bar, col, (x0, x1), lw = bar_and_cap(img, cal, unc, fig, scale, near, x_axis, ink, lw)
    cores, k = black_markers(img, x0, x1, 0, x_axis, lw)
    extra = k / 2 + (TRIANGLE_H / 6 if shape == "triangle" else 0)
    pts = [point(cal, b["y"], unc + extra, fig.to_page(b["x"], b["y"], scale)) for b in cores]
    return {"points": pts, "countable": True, "bar": bar}


def _ed3_setup(fig, labels):
    img, scale = fig.render(DPI)
    cal, unc, _ = axis(img, labels)
    x_axis = int(round(-cal.intercept / cal.slope))  # render row of the value 0
    ink = black(img) | coloured(img, "red") | coloured(img, "blue")
    return img, scale, cal, unc, x_axis, ink


def read_ed3g(fig, labels):
    """Extended Data Fig. 3g (p. 22): cAPD80 (msec), SM, MM, M1-M4 open bars with mean + SD. SM's red squares and MM's
    blue circles touch each other: bar only (MM's circles hide both SD caps: mean only). M1 (triangles), M2 (down
    triangles) and M4 (circles) are solid black markers on the black bar and error-bar lines, each found as the core
    left when lines are eroded away; each core is one marker apart from the others. Returns the groups in `labels`."""
    img, scale, cal, unc, x_axis, ink = _ed3_setup(fig, [800, 600, 400, 200, 0])
    single = {"red": (340, 420), "blue": (330, 420)}  # area (px at 300 dpi) of one square / one circle
    near = {"SM": 145, "MM": 222, "M1": 298, "M2": 375, "M4": 528}  # columns near each group's centre
    out = {}
    for label in labels:
        if label in ("SM", "MM"):
            colour = "red" if label == "SM" else "blue"
            out[label], _ = coloured_group(img, cal, unc, fig, scale, near[label], x_axis, ink, colour, single[colour])
        else:
            shape = "circle" if label == "M4" else "triangle"
            out[label] = black_group(img, cal, unc, fig, scale, near[label], x_axis, ink, shape)
    return out


def read_ed3h(fig):
    """Extended Data Fig. 3h (p. 22): prevalence of beating (1 Hz pacing), SM and M2 only (no item involves the other
    groups). SM's red squares touch in pairs and are cut by the black error-bar strokes: bar only. M2's four solid black
    down triangles lie on its short bar, error bar and the x axis (two straddle the axis line), each apart from the
    others. Triangles cover M2's side lines near the axis, so its line width is taken from SM's bar."""
    img, scale, cal, unc, x_axis, ink = _ed3_setup(fig, [0.8, 0.6, 0.4, 0.2, 0.0])
    sm, lw = coloured_group(img, cal, unc, fig, scale, 296, x_axis, ink, "red", (300, 360))
    return {"SM": sm, "M2": black_group(img, cal, unc, fig, scale, 527, x_axis, ink, "triangle", lw)}


# --- raster bars with red and blue markers spread across the bar (journal_version.pdf, Extended Data Fig. 4a,b) ---

ED4_SINGLE = {"red": (880, 990), "blue": (640, 720)}  # area (px at 300 dpi) of one square / one circle marker
ED4_HALF = 80  # half the window (px) about a group's centre holding its bar sides and its markers


ED4_CORNER = 15  # length (px) of top line and side line that make a bar's top corner


def ed4_bar(img, cal, unc, fig, scale, near, x_axis):
    """A bar's mean and the upper end of its error bar. Markers cover the middle of many bar tops, so the top line is
    found at the bar's corners: rows where black runs ED4_CORNER px inward from a side line along the row and the side
    line runs ED4_CORNER px down from it (error-bar caps are narrower than the bar and touch no side). Rows found at
    either corner are pooled. The cap is as in bar_and_cap: the topmost black stroke through the error-bar line above
    the top, at least 20 px wide, narrower than the bar and attached to the line below; left out when none shows."""
    bk = black(img)
    x0, x1, lw = outline(img, near, x_axis - 5, ED4_HALF)
    col = centre_column(img, near, bottom=x_axis - 5)
    k, w = ED4_CORNER, int(round(lw))
    rows = [r for r in range(x_axis - k)  # the side line's inner columns (its edge columns are anti-aliased)
            if (bk[r, x0:x0 + k].all() and bk[r:r + k, x0 + 1:x0 + w - 1].all())
            or (bk[r, x1 - k + 1:x1 + 1].all() and bk[r:r + k, x1 - w + 2:x1].all())]
    if not rows:
        return {}, col  # markers cover both corners: no mean
    if rows[-1] - rows[0] > 2 * lw:
        raise ValueError(f"bar near column {near}: top corners not found as one line (rows {rows})")
    m = line_in_run(cal, unc, fig, scale, col, rows[0], rows[-1], lw)
    bar = {"mean": [m["value"], m["lo"], m["hi"]]}
    c = int(round(col))
    caps = [f for f in strokes_through(img, col, x_axis - 5, bk)
            if f[1] + 6 < rows[0] and 20 <= f[2] < 0.85 * (x1 - x0 + 1) and bk[f[1] + 4:f[1] + 7, c - 1:c + 2].any()]
    if caps:
        e = line_in_run(cal, unc, fig, scale, col, caps[0][0], caps[0][1], lw)
        bar["error"] = [e["value"], e["lo"], e["hi"]]
    return bar, col


def read_ed4(fig, labels, near):
    """Extended Data Fig. 4a or b (p. 23): open bars with an error bar to the mean + error (the legend does not name
    the error) and red squares (SM) or blue circles (MM) spread across each bar. labels: y tick labels top to bottom;
    near: {group label: (column near the group's centre, marker colour)}. Each group gives its bar (mean, and the upper
    end of the error bar when its cap shows), and its points only when every marker of its colour in its window stands
    alone."""
    img, scale = fig.render(DPI)
    cal, unc, _ = axis(img, labels)
    x_axis = int(round(-cal.intercept / cal.slope))  # render row of the value 0
    out = {}
    for label, (c, colour) in near.items():
        bar, col = ed4_bar(img, cal, unc, fig, scale, c, x_axis)
        g = {"points": [], "countable": False, "bar": bar}
        # every blob of the colour, however large (a cluster of touching markers can exceed blobs' default max_area)
        bs = sorted((b for b in blobs(coloured(img, colour), min_area=5, max_area=img.shape[0] * img.shape[1])
                     if col - ED4_HALF <= b["x"] <= col + ED4_HALF), key=lambda b: b["y"])
        lo, hi = ED4_SINGLE[colour]
        if bs and all(lo <= b["area"] <= hi for b in bs):
            g["countable"] = True
            g["points"] = [point(cal, b["y"], unc, fig.to_page(b["x"], b["y"], scale)) for b in bs]
        out[label] = g
    return out


# --- Extended Data Fig. 5f,g (journal_version.pdf p. 24) ------------------------------------------------------

ED5_MARKER = (20, 24)  # side (px at 300 dpi) of one open square / circle marker's bounding box
ED5_HALF = 60  # half width (px) of a group's marker window around its error-bar line


def marker_boxes(img, colour, x_lo, x_hi):
    """Open markers of one colour between two columns, as bounding boxes (x0, y0, x1, y1). Black bar outlines and
    error-bar lines drawn over a ring cut it into pieces; pieces are joined while their joint box stays within one
    marker's size. A box larger than one marker is two or more touching markers."""
    bs = sorted((b for b in blobs(coloured(img, colour), min_area=5, max_area=img.shape[0] * img.shape[1])
                 if x_lo <= b["x"] <= x_hi), key=lambda b: b["box"][1])
    boxes = []
    for b in bs:
        x0, y0, w, h = b["box"]
        x1, y1 = x0 + w, y0 + h
        for i, (a0, b0, a1, b1) in enumerate(boxes):
            j = (min(a0, x0), min(b0, y0), max(a1, x1), max(b1, y1))
            if j[2] - j[0] <= ED5_MARKER[1] and j[3] - j[1] <= ED5_MARKER[1]:
                boxes[i] = j
                break
        else:
            boxes.append((x0, y0, x1, y1))
    return boxes


def read_ed5(fig, labels, near):
    """Extended Data Fig. 5f or g: open bars with an error bar (not named in the legend), red open squares (SM) and
    blue open circles (MM). labels: y tick labels top to bottom; near: {group label: (column near the group's
    error-bar line, marker colour)}. Each group gives its bar (mean = bar top, error = upper cap) and, when every
    marker box is one marker, its points (box centres)."""
    img, scale = fig.render(DPI)
    cal, unc, _ = axis(img, labels)
    bk = black(img)
    x_axis = min(r for r in range(bk.shape[0]) if bk[r].sum() > 0.35 * bk.shape[1])
    out = {}
    for label, (c, colour) in near.items():
        col = centre_column(img, c, bottom=x_axis)
        rows = bar_rows(img, col, x_axis, through_centre=False, min_width=8, half=45)
        g = {"points": [], "countable": False, "bar": bar(cal, unc, fig, scale, col, rows)}
        boxes = marker_boxes(img, colour, col - ED5_HALF, col + ED5_HALF)
        lo, hi = ED5_MARKER
        if boxes and all(lo <= x1 - x0 <= hi and lo <= y1 - y0 <= hi for x0, y0, x1, y1 in boxes):
            g["countable"] = True
            g["points"] = [point(cal, (y0 + y1) / 2, unc, fig.to_page((x0 + x1) / 2, (y0 + y1) / 2, scale))
                           for x0, y0, x1, y1 in boxes]
        out[label] = g
    return out


# --- vector bars with points, every line a separate path (Supplementary_Figures.pdf, Supplementary Fig. 4) ------

SUPP_INK = (0.14, 0.12, 0.13)  # near-black of axes, ticks, bars and error bars
SUPP_RED, SUPP_BLUE = (0.92, 0.13, 0.15), (0.2, 0.25, 0.6)  # SM filled squares, MM filled circles


def _ink_lines(fig, ink):
    """Straight segments of the one-line paths drawn in `ink`."""
    return [l for d in fig.drawings() if _rgb(d.get("color")) == ink and len(d["items"]) == 1 for l in _lines(d)]


def _num(t):
    try:
        return float(t.replace("−", "-").replace(",", ""))
    except ValueError:
        return None


def supp_axis(fig, n_ticks, ink=SUPP_INK):
    """Calibration (page y -> axis value) when the y axis line and each tick are separate one-line paths: the short
    horizontal lines ending at the leftmost long vertical line, each paired with the numeric label printed level with
    it just left of the axis; and the uncertainty in pt: 0.5 pt plus the calibration misfit."""
    from livinglit.figures.source import VECTOR_UNCERTAINTY_PT
    lines = _ink_lines(fig, ink)
    ax = min(l[0] for l in lines if abs(l[0] - l[2]) < 0.01 and abs(l[1] - l[3]) > 50)
    ticks = [l for l in lines if abs(l[1] - l[3]) < 0.01 and abs(max(l[0], l[2]) - ax) < 0.05
             and 0 < abs(l[0] - l[2]) < 6]
    labels = [((w[1] + w[3]) / 2, _num(w[4])) for w in fig.words() if _num(w[4]) is not None and 0 < ax - w[2] < 12]
    marks = []
    for l in ticks:
        pos, v = min(labels, key=lambda m: abs(m[0] - l[1]))
        if abs(pos - l[1]) > 1.5:
            raise ValueError(f"tick at y={l[1]} has no label level with it")
        marks.append((l[1], v))
    if len(marks) != n_ticks:
        raise ValueError(f"expected {n_ticks} y ticks, found {len(marks)}")
    cal = calibrate(marks)
    return cal, VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)


def supp_axis_base(fig, ink=SUPP_INK):
    """Page y of the x axis line: the lowest long horizontal one-line path."""
    return max(l[1] for l in _ink_lines(fig, ink) if abs(l[1] - l[3]) < 0.01 and abs(l[0] - l[2]) > 50)


def supp_categories(fig, ink=SUPP_INK):
    """Page x of the category ticks, left to right: short vertical one-line paths hanging from the x axis line."""
    base = supp_axis_base(fig, ink)
    return sorted(l[0] for l in _ink_lines(fig, ink) if abs(l[0] - l[2]) < 0.01
                  and abs(min(l[1], l[3]) - base) < 0.05 and 0 < abs(l[1] - l[3]) < 6)


def supp_error_bar(fig, x, ink=SUPP_INK, cap_max=12):
    """(mean y, upper cap y) of the error bar on category x: its vertical line is two one-line halves at x, above the
    x axis, that meet at the mean; its caps are short horizontal lines centred on x."""
    lines = _ink_lines(fig, ink)
    base = supp_axis_base(fig, ink)
    halves = [l for l in lines if abs(l[0] - x) < 0.05 and abs(l[2] - x) < 0.05 and abs(l[1] - l[3]) > 0.1
              and max(l[1], l[3]) < base - 0.05]
    caps = [l for l in lines if abs(l[1] - l[3]) < 0.01 and abs((l[0] + l[2]) / 2 - x) < 0.1
            and 0 < abs(l[0] - l[2]) < cap_max]
    if len(halves) != 2 or len(caps) != 2:
        raise ValueError(f"error bar at x={x}: {len(halves)} halves, {len(caps)} caps")
    a, b = {halves[0][1], halves[0][3]}, {halves[1][1], halves[1][3]}
    joint = [y for y in a if any(abs(y - z) < 0.01 for z in b)]
    if len(joint) != 1:
        raise ValueError(f"error bar at x={x}: its halves do not meet")
    return joint[0], min(c[1] for c in caps)


def read_supp_groups(fig, groups, n_ticks):
    """groups: {label: (category index, marker colour)}. A marker belongs to the nearest category tick. Returns read()
    groups: every point (top to bottom), the mean (where the error bar's two halves meet; the open bar's top line lies
    half a line width below it) and the upper end of the error bar."""
    cal, unc = supp_axis(fig, n_ticks)
    cats = supp_categories(fig)
    near = lambda x: min(range(len(cats)), key=lambda i: abs(cats[i] - x))
    res = {}
    for label, (ci, colour) in groups.items():
        pts = sorted((p for p in compound_markers(fig, colour) if near(p[0]) == ci), key=lambda p: p[1])
        bx = cats[ci]
        my, ty = supp_error_bar(fig, bx)
        m, e = point(cal, my, unc, (bx, my)), point(cal, ty, unc, (bx, ty))
        res[label] = {"points": [point(cal, p[1], unc, p) for p in pts], "countable": True,
                      "bar": {"mean": [m["value"], m["lo"], m["hi"]], "error": [e["value"], e["lo"], e["hi"]]}}
    return res


# --- Supplementary Fig. 7a-c (Supplementary_Figures.pdf p. 8): one embedded ~320 dpi image, open bars, mean + SD ---

S7_SQUARE = (290, 330)  # area (px at 300 dpi) of one red square (SM), side 17-19 px
S7_CIRCLE = (220, 245)  # area (px at 300 dpi) of one blue circle (MM), diameter 17-18 px
S7_SIDE = 18  # side (px) of one red square
S7_HALF = 70  # half the window (px) about a group's centre holding its markers (groups are ~149 px apart)
S7_LINE = 4  # widest blue error-bar stroke (px): the vertical line is 3 px, the caps 3-4 px


def s7_axis(img, labels):
    """Calibration (render row -> value) from the tick marks left of the y axis line (the leftmost column that is
    black over at least 90% of the tallest black column), top to bottom, paired with labels; the uncertainty in px;
    and the x axis row (the row holding most black ink)."""
    bk = black(img)
    cols = bk.sum(axis=0)
    ax = min(i for i, v in enumerate(cols) if v >= 0.9 * cols.max())
    ticks = tick_rows(img, ax)
    if len(ticks) != len(labels):
        raise ValueError(f"found {len(ticks)} tick marks, expected {len(labels)}")
    cal = calibrate(list(zip(ticks, labels)))
    return cal, RASTER_UNCERTAINTY_PX_300DPI + cal.residual / abs(cal.slope), int(np.argmax(bk.sum(axis=1)))


def s7_markers(img, colour, x_lo, x_hi):
    """Markers of one colour between two columns as (x, y, extra px of uncertainty), top to bottom. A blob of one
    marker's area is one marker (its centroid). Black bar and error-bar lines cut touching markers apart in the colour
    mask; what stays joined is read only in two known shapes, and anything else raises:
    - red: two squares stacked in one column (box one square wide and two tall, twice a square's area): centres half a
      side in from the box's top and bottom, 1 px extra for the 17-19 px side;
    - blue: circles joined by MM's blue error bar: the blob is eroded by a square wider than any blue line (lines
      vanish, circles shrink about their centres) and each core is one circle; a core may sit up to half the square
      off its circle's centre where a line widens the circle, which widens the interval."""
    import cv2
    mask = coloured(img, colour)
    out = []
    for b in blobs(mask, min_area=5, max_area=mask.size):
        if not x_lo <= b["x"] <= x_hi:
            continue
        x0, y0, w, h = b["box"]
        lo, hi = S7_SQUARE if colour == "red" else S7_CIRCLE
        if lo <= b["area"] <= hi:
            out.append((b["x"], b["y"], 0.0))
        elif (colour == "red" and w <= S7_SIDE + 1 and 2 * lo <= b["area"] <= 2 * hi
              and 2 * S7_SIDE - 2 <= h <= 2 * S7_SIDE + 2):
            c = (S7_SIDE - 1) / 2
            out += [(b["x"], y0 + c, 1.0), (b["x"], y0 + h - 1 - c, 1.0)]
        elif colour == "blue" and b["area"] > hi:
            k = S7_LINE + 3
            _, lab = cv2.connectedComponents(mask.astype(np.uint8), connectivity=8)
            ids, n = np.unique(lab[y0:y0 + h, x0:x0 + w], return_counts=True)
            own = ids[np.argmax(np.where(ids == 0, -1, n))]  # the blob's own component, the largest in its box
            core = cv2.erode((lab == own).astype(np.uint8), np.ones((k, k), np.uint8)).astype(bool)
            for c in blobs(core, min_area=3, max_area=mask.size):
                if max(c["box"][2], c["box"][3]) > 18 - k + 4:  # wider than one eroded circle: circles merged
                    raise ValueError(f"blue blob at ({b['x']:.0f}, {b['y']:.0f}): a core is not one circle")
                out.append((c["x"], c["y"], k / 2))
        else:
            raise ValueError(f"{colour} blob at ({b['x']:.0f}, {b['y']:.0f}), area {b['area']}, box {b['box']}: "
                             "not a known marker shape")
    return sorted(out, key=lambda m: m[1])


S7_BAR_HALF = 60  # half the window (px) about a group's centre holding its bar's side lines (bars are ~97 px wide)
S7_CAP = 25  # least width (px) of an SD cap's run through the error-bar line: wider than any marker (17-19 px)


def s7_bar(img, cal, unc, fig, scale, near, x_axis, blue_error):
    """A group's bar, as in bar_and_cap: mean = the open bar's top line (the topmost stroke through the error-bar line
    spanning the bar between its side lines, which continue below it); error = the upper SD cap (the topmost run of
    the error bar's ink through its line, at least S7_CAP px wide, narrower than the bar, above the bar top and
    attached to the line below; brackets span more than the bar). The error bar's ink is black, or blue where MM's
    error bar is drawn in blue (its caps are S7_LINE px thick). Returns the bar and the error-bar column."""
    bk, bl = black(img), coloured(img, "blue")
    ink = img.astype(int).min(axis=2) < 180  # any ink: lines, markers and the anti-aliased seams between them
    line = bl if blue_error else bk
    counts = line[:x_axis - 5, near - 14:near + 14].sum(axis=0)
    col = float(near - 14 + np.flatnonzero(counts >= counts.max() - 1).mean())
    c = int(round(col))
    x0, x1, lw = outline(img, c, x_axis - 5, S7_BAR_HALF)
    width = x1 - x0 + 1

    def sides_go_on(last):
        below = range(last + 2, min(last + 17, x_axis - 3))
        return len(below) > 0 and all(ink[r, x0:x0 + 3].any() and ink[r, x1 - 2:x1 + 1].any() for r in below)

    tops = [f for f in strokes_through(img, col, x_axis - 5, ink)
            if f[2] >= 0.85 * width and abs(f[3][0] - x0) <= 3 and abs(f[3][1] - x1) <= 3 and sides_go_on(f[1])]
    if not tops:
        raise ValueError(f"bar near column {near}: no top line")
    top = tops[0]
    m = line_in_run(cal, unc, fig, scale, col, top[0], top[1], lw)
    # runs and attachment are taken through all ink, as a marker drawn over or just under a cap hides the error bar's
    # own ink at the line; a cap's rows must hold its own ink (at least S7_CAP px of it near the line)
    caps = [f for f in strokes_through(img, col, x_axis - 5, ink)
            if f[1] + 6 < top[0] and S7_CAP <= f[2] < 0.85 * width and ink[f[1] + 4:f[1] + 7, c - 1:c + 2].any()
            and line[f[0]:f[1] + 1, c - 40:c + 41].sum(axis=1).max() >= S7_CAP]
    if not caps:
        raise ValueError(f"bar near column {near}: no upper cap")
    # a marker on the cap widens its run over more rows than the cap: keep only the rows at least S7_CAP wide
    first, last = caps[0][0], caps[0][1]
    wide = [r for r in range(first, last + 1) if s7_run(ink, r, c) >= S7_CAP]
    e = line_in_run(cal, unc, fig, scale, col, wide[0], wide[-1], S7_LINE if blue_error else lw)
    return {"mean": [m["value"], m["lo"], m["hi"]], "error": [e["value"], e["lo"], e["hi"]]}, col


def s7_run(mask, r, c):
    """Length of the run of mask through column c on row r (0 when c is off)."""
    if not mask[r, c]:
        return 0
    x0 = x1 = c
    while x0 > 0 and mask[r, x0 - 1]:
        x0 -= 1
    while x1 < mask.shape[1] - 1 and mask[r, x1 + 1]:
        x1 += 1
    return x1 - x0 + 1


def read_s7(fig, labels, near, blue_error=()):
    """Supplementary Fig. 7a, b or c. labels: y tick labels top to bottom; near: {group label: (render column near the
    group's error-bar line, marker colour)}; blue_error: labels whose error bar is drawn in blue. Every group gives its
    bar and all its markers (each read alone or split as in s7_markers)."""
    img, scale = fig.render(DPI)
    cal, unc, x_axis = s7_axis(img, labels)
    out = {}
    for label, (c, colour) in near.items():
        bar_, col = s7_bar(img, cal, unc, fig, scale, c, x_axis, label in blue_error)
        ms = s7_markers(img, colour, col - S7_HALF, col + S7_HALF)
        out[label] = {"points": [point(cal, y, unc + e, fig.to_page(x, y, scale)) for x, y, e in ms],
                      "countable": True, "bar": bar_}
    return out
