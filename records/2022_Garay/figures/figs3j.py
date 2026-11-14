"""Fig. S3J (% cTnT+MLC-2v+ cells, % cTnT+MLC-2a+ cells, MLC-2v+/MLC-2a+ ratio; flow cytometry, day 30), mmc1.pdf
page 4.

Three dot plots side by side, each with DMSO and SP columns for the inhibition windows days 15-20, 20-30 and
25-30. Every point is a whole vector circle (four Bezier arcs, 4.7 pt wide), so its centre is its rectangle centre;
discs drawn on top of each other are each kept. The plots are split at their y axes (one vertical axis line each).
In each plot the axis is calibrated from the printed tick labels matched to the major tick strokes; columns come
from the error bars (cap, stem, cap paths), left to right windows x (DMSO, SP); the x-axis window labels are checked
against WINDOWS and each disc's colour against its column (legend: yellow DMSO, purple SP). The mean is the long
horizontal stroke on each error bar; the error value is the upper cap. Fig. S3I is a timeline schematic (no values).
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

COLOURS = {"D30": (0.94, 0.72, 0.08), "SP30": (0.71, 0.44, 0.68)}
WINDOWS = ("15-20", "20-30", "25-30")
GROUPS = ("D30", "SP30")
MEASURES = ("MLC-2v", "MLC-2a", "ratio")
SHORT = {"D30": "DMSO", "SP30": "SP"}


def _plot(segs, single, words, discs, x0, x1):
    """One dot plot between page x0 and x1; returns {(window, group): column}."""
    vert = [s for s in single if abs(s[0] - s[2]) < 0.01 and abs(s[1] - s[3]) > 40 and x0 <= s[0] < x1]
    if len(vert) != 1:
        raise ValueError(f"{len(vert)} y axes in {x0:.0f}-{x1:.0f}")
    ax, bottom = vert[0][0], max(vert[0][1], vert[0][3])
    ticks = [s[1] for s in single if abs(s[1] - s[3]) < 0.01 and abs(max(s[0], s[2]) - ax) < 0.05
             and abs(s[2] - s[0]) > 3.5 and min(s[0], s[2]) < ax]
    marks = []
    for wx0, wy0, wx1, wy1, t in words:
        try:
            v = float(t)
        except ValueError:
            continue
        if ax - 15 < wx1 < ax:
            near = [y for y in ticks if abs(y - (wy0 + wy1) / 2) < 1.5]
            if len(near) == 1:
                marks.append((near[0], v))
    if len(marks) != len(ticks) or len(marks) < 3:
        raise ValueError(f"{len(marks)} labelled ticks of {len(ticks)} major ticks")
    cal = calibrate(marks)
    unc = VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)

    names = sorted((w for w in words if bottom < w[1] < bottom + 15 and ax < w[0] < x1 and w[4] in WINDOWS),
                   key=lambda w: w[0])
    if [w[4] for w in names] != list(WINDOWS):
        raise ValueError(f"x-axis labels {[w[4] for w in names]}")

    bars = [p for p in segs if len(p) == 3 and abs(p[0][1] - p[0][3]) < 0.01 and abs(p[1][0] - p[1][2]) < 0.01
            and abs(p[2][1] - p[2][3]) < 0.01 and abs(p[0][2] - p[0][0]) < 6.0 and ax < p[1][0] < x1]
    cols = sorted((p[1][0], p) for p in bars)
    keys = [(w, g) for w in WINDOWS for g in GROUPS]
    if len(cols) != len(keys):
        raise ValueError(f"{len(cols)} error bars")
    means = [s for s in single if abs(s[1] - s[3]) < 0.01 and 9.0 < abs(s[2] - s[0]) < 11.0 and ax < s[0] < x1]

    per = {k: [] for k in keys}
    for x, y, g in discs:
        if not ax < x < x1:
            continue
        i = min(range(len(cols)), key=lambda j: abs(cols[j][0] - x))
        if keys[i][1] != g or abs(cols[i][0] - x) > 5.0:
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


def read(fig):
    segs = []
    for d in fig.drawings():
        if d.get("fill") is None and all(it[0] == "l" for it in d["items"]):
            segs.append([(it[1].x, it[1].y, it[2].x, it[2].y) for it in d["items"]])
    single = [p[0] for p in segs if len(p) == 1]
    words = fig.words()

    discs = []
    for d in fig.drawings():
        f, r = d.get("fill"), d["rect"]
        if f is None or len(d["items"]) != 4 or not all(it[0] == "c" for it in d["items"]):
            continue
        if abs(r.width - r.height) > 0.01 or not 4.5 < r.width < 4.9:
            raise ValueError(f"unexpected filled shape {r}")
        g = [k for k, c in COLOURS.items() if max(abs(a - b) for a, b in zip(f, c)) < 0.02]
        if len(g) != 1:
            raise ValueError(f"unknown disc colour {f}")
        discs.append(((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2, g[0]))

    axes = sorted(s[0] for s in single if abs(s[0] - s[2]) < 0.01 and abs(s[1] - s[3]) > 40)
    if len(axes) != len(MEASURES):
        raise ValueError(f"{len(axes)} y axes")
    edges = [a - 1.0 for a in axes] + [float("inf")]

    groups = {}
    for measure, x0, x1 in zip(MEASURES, edges, edges[1:]):
        per = _plot(segs, single, words, discs, x0, x1)
        for w in WINDOWS:
            for g in GROUPS:
                groups[f"{measure} {w} SP vs DMSO: {SHORT[g]}"] = per[(w, g)]
    return {"groups": groups}
