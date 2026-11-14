"""Helpers for this paper's figure scripts (2022_Garay only).

Points in this paper's GraphPad panels are translucent discs stored as flattened pieces: no piece is a whole
disc. Every Bezier arc of a disc boundary gives the disc centre as the meeting point of the normals at its two
ends; arcs of the disc radius are clustered and one cluster is one disc.
"""
import math

import numpy as np


def arc_centres(fig, box, keep=lambda fill: True):
    """(cx, cy, r) from every Bezier arc of a filled piece inside box (x0, y0, x1, y1) whose fill passes keep."""
    x0, y0, x1, y1 = box
    out = []
    for d in fig.drawings():
        f, r = d.get("fill"), d["rect"]
        if f is None or not keep(f) or not (x0 <= r.x0 and r.x1 <= x1 and y0 <= r.y0 and r.y1 <= y1):
            continue
        for it in d["items"]:
            if it[0] != "c":
                continue
            p0, p1, p2, p3 = (np.array([q.x, q.y]) for q in it[1:5])
            t0, t1 = p1 - p0, p3 - p2
            if np.linalg.norm(p3 - p0) < 0.4 or np.linalg.norm(t0) < 1e-3 or np.linalg.norm(t1) < 1e-3:
                continue
            n0, n1 = np.array([-t0[1], t0[0]]), np.array([-t1[1], t1[0]])
            A = np.column_stack([n0, -n1])
            if abs(np.linalg.det(A)) < 1e-6 * np.linalg.norm(n0) * np.linalg.norm(n1) or \
                    abs(t0[0] * t1[1] - t0[1] * t1[0]) / (np.linalg.norm(t0) * np.linalg.norm(t1)) < 0.15:
                continue
            a, _ = np.linalg.solve(A, p3 - p0)
            c = p0 + a * n0
            r0, r1 = np.linalg.norm(c - p0), np.linalg.norm(c - p3)
            if abs(r0 - r1) < 0.05:
                out.append((float(c[0]), float(c[1]), float((r0 + r1) / 2)))
    return out


def discs(arcs, radius, rtol=0.08, tol=0.25):
    """Cluster arc centres of the disc radius; one cluster per disc. Returns (x, y, votes)."""
    pts = [(x, y) for x, y, r in arcs if abs(r - radius) < rtol]
    clusters = []
    for x, y in sorted(pts):
        for c in clusters:
            if math.hypot(c[0][0] - x, c[0][1] - y) < tol:
                c.append((x, y))
                break
        else:
            clusters.append([(x, y)])
    return [(float(np.median([p[0] for p in c])), float(np.median([p[1] for p in c])), len(c)) for c in clusters]


def dot_panel_9(fig, colours, lines_order, groups_order, cap_max=4.0, mean_width=(5.0, 7.0), disc_width=(3.4, 3.7)):
    """One GraphPad dot panel of three cell lines x three groups (Fig. S5C-G kind) drawn as whole vector discs.

    Each point is one whole filled circle (four Bezier arcs), so its centre is its rectangle centre; discs drawn
    on top of each other are each kept. Columns come from the error bars (cap, stem, cap paths), left to right
    lines_order x groups_order; the x-axis line labels are checked against lines_order and each disc's colour
    against its column. The axis is calibrated from the printed tick labels matched to the major tick strokes.
    cap_max (widest error-bar cap, pt), mean_width (mean stroke length range, pt) and disc_width (disc diameter
    range, pt) default to the S5C-G style.
    Returns {(line, group): {"points", "countable", "bar"}}.
    """
    from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

    segs = []
    for d in fig.drawings():
        if d.get("fill") is None and all(it[0] == "l" for it in d["items"]):
            segs.append([(it[1].x, it[1].y, it[2].x, it[2].y) for it in d["items"]])
    single = [p[0] for p in segs if len(p) == 1]
    vert = [s for s in single if abs(s[0] - s[2]) < 0.01 and abs(s[1] - s[3]) > 40]
    if len(vert) != 1:
        raise ValueError(f"{len(vert)} y axes")
    ax, bottom = vert[0][0], max(vert[0][1], vert[0][3])
    ticks = [s[1] for s in single if abs(s[1] - s[3]) < 0.01 and abs(max(s[0], s[2]) - ax) < 0.05
             and abs(s[2] - s[0]) > 3.5 and min(s[0], s[2]) < ax]
    marks = []
    for x0, y0, x1, y1, t in fig.words():
        try:
            v = float(t.replace("−", "-"))
        except ValueError:
            continue
        if ax - 15 < x1 < ax:
            near = [y for y in ticks if abs(y - (y0 + y1) / 2) < 1.5]
            if len(near) == 1:
                marks.append((near[0], v))
    if len(marks) != len(ticks):
        raise ValueError(f"{len(marks)} labelled ticks of {len(ticks)} major ticks")
    cal = calibrate(marks)
    unc = VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)

    names = sorted((w for w in fig.words() if w[1] > bottom and w[4] in lines_order), key=lambda w: w[0])
    if [w[4] for w in names] != list(lines_order):
        raise ValueError(f"x-axis labels {[w[4] for w in names]}")

    bars = [p for p in segs if len(p) == 3 and abs(p[0][1] - p[0][3]) < 0.01 and abs(p[1][0] - p[1][2]) < 0.01
            and abs(p[2][1] - p[2][3]) < 0.01 and abs(p[0][2] - p[0][0]) < cap_max]
    cols = sorted((p[1][0], p) for p in bars)
    if len(cols) != len(lines_order) * len(groups_order):
        raise ValueError(f"{len(cols)} error bars")
    means = [s for s in single if abs(s[1] - s[3]) < 0.01 and mean_width[0] < abs(s[2] - s[0]) < mean_width[1]]

    discs = []
    for d in fig.drawings():
        f, r = d.get("fill"), d["rect"]
        if f is None or len(d["items"]) != 4 or not all(it[0] == "c" for it in d["items"]):
            continue
        if abs(r.width - r.height) > 0.01 or not disc_width[0] < r.width < disc_width[1]:
            raise ValueError(f"unexpected filled shape {r}")
        g = [k for k, c in colours.items() if max(abs(a - b) for a, b in zip(f, c)) < 0.02]
        if len(g) != 1:
            raise ValueError(f"unknown disc colour {f}")
        discs.append(((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2, g[0]))

    keys = [(line, g) for line in lines_order for g in groups_order]
    per = {k: [] for k in keys}
    for x, y, g in discs:
        i = min(range(len(cols)), key=lambda j: abs(cols[j][0] - x))
        if keys[i][1] != g or abs(cols[i][0] - x) > 4.5:
            raise ValueError(f"disc {g} at {x:.2f},{y:.2f} not in its column")
        per[keys[i]].append((x, y))

    out = {}
    for k, (cx, path) in zip(keys, cols):
        m = [s[1] for s in means if abs((s[0] + s[2]) / 2 - cx) < 0.5]
        if len(m) != 1:
            raise ValueError(f"{k}: {len(m)} mean strokes")
        upper = min(path[0][1], path[2][1])
        mean, err = point(cal, m[0], unc, (cx, m[0])), point(cal, upper, unc, (cx, upper))
        out[k] = {"points": [point(cal, y, unc, (x, y)) for x, y in sorted(per[k], key=lambda p: (p[1], p[0]))],
                  "countable": True,
                  "bar": {"mean": [mean["value"], mean["lo"], mean["hi"]],
                          "error": [err["value"], err["lo"], err["hi"]]}}
    return out


def dot_panel_2(fig, colours, columns, cap_width, mean_width, disc_width, log=False):
    """One GraphPad dot panel of two columns (Fig. S5L, S5P-Q kind) drawn as whole vector discs.

    Each point is one whole filled circle (four Bezier arcs), so its centre is its rectangle centre; discs drawn on
    top of each other are each kept. Columns are the x-axis tick strokes, left to right `columns`, checked against
    the x-axis labels; each disc's colour (colours: column -> fill) is checked against its column. The axis is
    calibrated from the printed tick labels matched to the major tick strokes. Means are horizontal strokes of
    mean_width (pt range); the upper error-bar end is the upper cap of the cap-stem-cap path whose caps are
    cap_width (pt range) wide; the significance bracket (a path drawn vertical first) is not an error bar.
    Any number of columns; log=True calibrates a log10 axis (Fig. S6B).
    Returns {column: {"points", "countable", "bar"}}.
    """
    from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

    paths = [[(it[1].x, it[1].y, it[2].x, it[2].y) for it in d["items"]] for d in fig.drawings()
             if d.get("fill") is None and all(it[0] == "l" for it in d["items"])]
    single = [p[0] for p in paths if len(p) == 1]
    yaxes = [s for s in single if abs(s[0] - s[2]) < 0.01 and abs(s[1] - s[3]) > 40]
    xaxes = [s for s in single if abs(s[1] - s[3]) < 0.01 and abs(s[2] - s[0]) > 30]
    if len(yaxes) != 1 or len(xaxes) != 1:
        raise ValueError(f"{len(yaxes)} y axes, {len(xaxes)} x axes")
    ax, base = yaxes[0][0], xaxes[0][1]
    ticks = [s[1] for s in single if abs(s[1] - s[3]) < 0.01 and abs(max(s[0], s[2]) - ax) < 0.05
             and 3.5 < abs(s[2] - s[0]) < 6.0]
    marks = []
    for x0, y0, x1, y1, t in fig.words():
        try:
            v = float(t.replace("−", "-"))
        except ValueError:
            continue
        if ax - 15 < x1 < ax:
            near = [y for y in ticks if abs(y - (y0 + y1) / 2) < 1.5]
            if len(near) == 1:
                marks.append((near[0], v))
    if len(marks) != len(ticks) or len(marks) < 3:
        raise ValueError(f"{len(marks)} labelled ticks of {len(ticks)} major ticks")
    cal = calibrate(marks, log=log)
    unc = VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)

    cols = sorted(s[0] for s in single if abs(s[0] - s[2]) < 0.01 and abs(min(s[1], s[3]) - base) < 0.05
                  and 3.5 < abs(s[3] - s[1]) < 6.0)
    names = sorted((w for w in fig.words() if w[1] > base and w[4] in columns), key=lambda w: w[0])
    if len(cols) != len(columns) or [w[4] for w in names] != list(columns):
        raise ValueError(f"{len(cols)} x ticks, labels {[w[4] for w in names]}")

    per = {c: [] for c in columns}
    for d in fig.drawings():
        f, r = d.get("fill"), d["rect"]
        if f is None or len(d["items"]) != 4 or not all(it[0] == "c" for it in d["items"]):
            continue
        if abs(r.width - r.height) > 0.01 or not disc_width[0] < r.width < disc_width[1]:
            raise ValueError(f"unexpected filled shape {r}")
        g = [k for k, c in colours.items() if max(abs(a - b) for a, b in zip(f, c)) < 0.02]
        if len(g) != 1:
            raise ValueError(f"unknown disc colour {f}")
        x, y = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
        i = min(range(len(cols)), key=lambda j: abs(cols[j] - x))
        if columns[i] != g[0] or abs(cols[i] - x) > 8:
            raise ValueError(f"disc {g[0]} at {x:.2f},{y:.2f} not in its column")
        per[g[0]].append((x, y))

    bars = [p for p in paths if len(p) == 3 and abs(p[0][1] - p[0][3]) < 0.01 and abs(p[1][0] - p[1][2]) < 0.01
            and abs(p[2][1] - p[2][3]) < 0.01 and cap_width[0] < abs(p[0][2] - p[0][0]) < cap_width[1]]
    means = [s for s in single if abs(s[1] - s[3]) < 0.01 and mean_width[0] < abs(s[2] - s[0]) < mean_width[1]]
    out = {}
    for label, cx in zip(columns, cols):
        b = [p for p in bars if abs(p[1][0] - cx) < 0.5]
        m = [s[1] for s in means if abs((s[0] + s[2]) / 2 - cx) < 0.5]
        if len(b) != 1 or len(m) != 1:
            raise ValueError(f"{label}: {len(b)} error bars, {len(m)} mean strokes")
        upper = min(b[0][0][1], b[0][2][1])
        mean, err = point(cal, m[0], unc, (cx, m[0])), point(cal, upper, unc, (cx, upper))
        out[label] = {"points": [point(cal, y, unc, (x, y)) for x, y in sorted(per[label], key=lambda p: (p[1], p[0]))],
                      "countable": True,
                      "bar": {"mean": [mean["value"], mean["lo"], mean["hi"]],
                              "error": [err["value"], err["lo"], err["hi"]]}}
    return out
