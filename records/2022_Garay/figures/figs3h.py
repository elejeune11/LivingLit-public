"""Fig. S3H (% cTnT+MLC-2v+ cells, flow cytometry, day 30), mmc1.pdf page 4.

One bar-and-dot panel: three cell lines (MYL2, PLZ, 19004) x DMSO, S, P, SP. Every point is a whole vector circle
(four Bezier arcs, 2.5 pt wide), so its centre is its rectangle centre; discs drawn on top of each other are each
kept. Columns come from the error bars (a four-stroke path: two half stems meeting at the mean, two caps), left to
right lines x groups; the x-axis line labels are checked against LINES and each disc's colour against its column
(legend: yellow DMSO, blue S, green P, purple SP). The axis is calibrated from the printed tick labels matched to
the major tick strokes. The mean is where the two half stems meet (the bar top lies 0.28 pt lower, half the
outline stroke); the error value is the upper cap. Only the columns the record's items compare (DMSO, P, SP) are
returned; each DMSO column serves both pairwise items of its line.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

COLOURS = {"D30": (0.94, 0.72, 0.08), "S30": (0.24, 0.75, 0.92), "P30": (0.24, 0.65, 0.33),
           "SP30": (0.71, 0.44, 0.68)}
LINES = ("MYL2", "PLZ", "19004")
GROUPS = ("D30", "S30", "P30", "SP30")
SHORT = {"D30": "DMSO", "P30": "P", "SP30": "SP"}
PAIRS = [("P30", "D30"), ("SP30", "D30")]


def read(fig):
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
            v = float(t)
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

    names = sorted((w for w in fig.words() if bottom < w[1] < bottom + 15 and w[4] in LINES), key=lambda w: w[0])
    if [w[4] for w in names] != list(LINES):
        raise ValueError(f"x-axis labels {[w[4] for w in names]}")

    bars = []
    for p in segs:
        if len(p) != 4:
            continue
        stems = [s for s in p if abs(s[0] - s[2]) < 0.01]
        caps = [s for s in p if abs(s[1] - s[3]) < 0.01 and 2.5 < abs(s[2] - s[0]) < 4.0]
        if len(stems) == 2 and len(caps) == 2:
            mid = {round(s[3], 2) for s in stems}
            if len(mid) != 1:
                raise ValueError(f"half stems do not meet: {p}")
            bars.append((stems[0][0], stems[0][3], min(c[1] for c in caps)))
    bars.sort()
    keys = [(line, g) for line in LINES for g in GROUPS]
    if len(bars) != len(keys):
        raise ValueError(f"{len(bars)} error bars")

    per = {k: [] for k in keys}
    for d in fig.drawings():
        f, r = d.get("fill"), d["rect"]
        if f is None or len(d["items"]) != 4 or not all(it[0] == "c" for it in d["items"]):
            continue
        if abs(r.width - r.height) > 0.01 or not 2.3 < r.width < 2.7:
            raise ValueError(f"unexpected filled shape {r}")
        g = [k for k, c in COLOURS.items() if max(abs(a - b) for a, b in zip(f, c)) < 0.02]
        if len(g) != 1:
            raise ValueError(f"unknown disc colour {f}")
        x, y = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
        i = min(range(len(bars)), key=lambda j: abs(bars[j][0] - x))
        if keys[i][1] != g[0] or abs(bars[i][0] - x) > 3.5:
            raise ValueError(f"disc {g[0]} at {x:.2f},{y:.2f} not in its column")
        per[keys[i]].append((x, y))

    col = {}
    for k, (cx, m, upper) in zip(keys, bars):
        mean, err = point(cal, m, unc, (cx, m)), point(cal, upper, unc, (cx, upper))
        col[k] = {"points": [point(cal, y, unc, (x, y)) for x, y in sorted(per[k], key=lambda p: (p[1], p[0]))],
                  "countable": True,
                  "bar": {"mean": [mean["value"], mean["lo"], mean["hi"]],
                          "error": [err["value"], err["lo"], err["hi"]]}}

    groups = {}
    for line in LINES:
        for pair in PAIRS:
            for g in pair:
                groups[f"{line} {SHORT[pair[0]]} vs {SHORT[pair[1]]}: {SHORT[g]}"] = col[(line, g)]
    return {"groups": groups}
