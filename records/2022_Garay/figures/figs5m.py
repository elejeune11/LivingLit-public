"""Fig. S5M (AP maximum upstroke velocity dV/dtmax, V/s; PLZ, DMSO vs SP), mmc1.pdf page 6.

One GraphPad dot panel, two columns (DMSO, SP). Every point is a whole vector circle (four Bezier arcs, centre =
rectangle centre); colours follow the column (yellow DMSO, purple SP, as in the S5N key). Columns are the x-axis
tick strokes, left to right DMSO, SP (checked against the x-axis labels). The axis is calibrated from the printed
tick labels matched to the major tick strokes. Means are the 11.5 pt horizontal strokes; the upper error-bar end is
the upper cap of the cap-stem-cap path (5.75 pt caps); the ns bracket (a longer path) is not an error bar.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

COLOURS = {"DMSO": (0.94, 0.72, 0.08), "SP": (0.71, 0.44, 0.68)}
COLUMNS = ["DMSO", "SP"]


def read(fig):
    paths = [[(it[1].x, it[1].y, it[2].x, it[2].y) for it in d["items"]] for d in fig.drawings()
             if d.get("fill") is None and all(it[0] == "l" for it in d["items"])]
    single = [p[0] for p in paths if len(p) == 1]
    yaxes = [s for s in single if abs(s[0] - s[2]) < 0.01 and abs(s[1] - s[3]) > 40]
    xaxes = [s for s in single if abs(s[1] - s[3]) < 0.01 and abs(s[2] - s[0]) > 30]
    if len(yaxes) != 1 or len(xaxes) != 1:
        raise ValueError(f"{len(yaxes)} y axes, {len(xaxes)} x axes")
    ax, base = yaxes[0][0], xaxes[0][1]
    ticks = [s[1] for s in single if abs(s[1] - s[3]) < 0.01 and abs(max(s[0], s[2]) - ax) < 0.05
             and 3.5 < abs(s[2] - s[0]) < 4.5]
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
    cal = calibrate(marks)
    unc = VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)

    cols = sorted(s[0] for s in single if abs(s[0] - s[2]) < 0.01 and abs(min(s[1], s[3]) - base) < 0.05
                  and 3.5 < abs(s[3] - s[1]) < 4.5)
    names = sorted((w for w in fig.words() if w[1] > base and w[4] in COLUMNS), key=lambda w: w[0])
    if len(cols) != len(COLUMNS) or [w[4] for w in names] != COLUMNS:
        raise ValueError(f"{len(cols)} x ticks, labels {[w[4] for w in names]}")

    discs = {c: [] for c in COLUMNS}
    for d in fig.drawings():
        f, r = d.get("fill"), d["rect"]
        if f is None:
            continue
        if len(d["items"]) != 4 or not all(it[0] == "c" for it in d["items"]) or abs(r.width - r.height) > 0.01:
            raise ValueError(f"unexpected filled shape {r}")
        g = [k for k, c in COLOURS.items() if max(abs(a - b) for a, b in zip(f, c)) < 0.02]
        if len(g) != 1:
            raise ValueError(f"unknown disc colour {f}")
        x, y = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
        i = min(range(len(cols)), key=lambda j: abs(cols[j] - x))
        if COLUMNS[i] != g[0] or abs(cols[i] - x) > 8:
            raise ValueError(f"disc {g[0]} at {x:.2f},{y:.2f} not in its column")
        discs[g[0]].append((x, y))

    bars = [p for p in paths if len(p) == 3 and abs(p[0][1] - p[0][3]) < 0.01 and abs(p[1][0] - p[1][2]) < 0.01
            and abs(p[2][1] - p[2][3]) < 0.01 and 5.0 < abs(p[0][2] - p[0][0]) < 6.5]
    means = [s for s in single if abs(s[1] - s[3]) < 0.01 and 10.5 < abs(s[2] - s[0]) < 12.5]
    groups = {}
    for label, cx in zip(COLUMNS, cols):
        b = [p for p in bars if abs(p[1][0] - cx) < 0.5]
        m = [s[1] for s in means if abs((s[0] + s[2]) / 2 - cx) < 0.5]
        if len(b) != 1 or len(m) != 1:
            raise ValueError(f"{label}: {len(b)} error bars, {len(m)} mean strokes")
        upper = min(b[0][0][1], b[0][2][1])
        mean, err = point(cal, m[0], unc, (cx, m[0])), point(cal, upper, unc, (cx, upper))
        groups[label] = {"points": [point(cal, y, unc, (x, y)) for x, y in sorted(discs[label], key=lambda p: (p[1], p[0]))],
                         "countable": True,
                         "bar": {"mean": [mean["value"], mean["lo"], mean["hi"]],
                                 "error": [err["value"], err["lo"], err["hi"]]}}
    return {"groups": groups}
