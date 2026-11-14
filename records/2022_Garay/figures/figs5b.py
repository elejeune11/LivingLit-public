"""Fig. S5B (contraction force, µN), mmc1.pdf page 6.

Vector panel with a broken y axis: a lower segment 0-0.5 and an upper segment from the break (0.8) to 1.5,
labelled 1.0, 1.2, 1.4. Each segment is calibrated on its own from the printed tick labels matched to the
major tick strokes beside them; a point is read on the segment whose span holds it.

Every point is a whole filled circle (four Bezier arcs, 3.54 pt across), so its centre is the centre of its
rectangle. Colours follow the legend under panel A: yellow DMSO (30d), purple SP (30d), red Untreated (60d).
Columns are the three bracket ends of each cell line, left to right DMSO, SP, 60d (PLZ, then MYL2); a point
belongs to the column whose x it lies nearest.

The mean is the 10.2 pt horizontal stroke of each column; the error bar is a three-part path (cap, stem,
cap) and its upper end is the upper cap.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

COLOURS = {"D30": (0.94, 0.72, 0.08), "SP30": (0.71, 0.44, 0.68), "D60": (0.9, 0.15, 0.17)}
COLUMNS = [("PLZ", "D30"), ("PLZ", "SP30"), ("PLZ", "D60"), ("MYL2", "D30"), ("MYL2", "SP30"), ("MYL2", "D60")]
SHORT = {"D30": "DMSO", "SP30": "SP", "D60": "60d"}
PAIRS = [("SP30", "D30"), ("D60", "D30"), ("SP30", "D60")]


def _label(line, pair, g):
    return f"{line} {SHORT[pair[0]]} vs {SHORT[pair[1]]}: {SHORT[g]}"


def _lines(fig):
    """Unfilled line paths as lists of segments (x0, y0, x1, y1)."""
    out = []
    for d in fig.drawings():
        if d.get("fill") is None and all(it[0] == "l" for it in d["items"]):
            out.append([(it[1].x, it[1].y, it[2].x, it[2].y) for it in d["items"]])
    return out


def _axis(fig, lines):
    """Two calibrations (lower, upper) and the y span of each axis segment."""
    single = [p[0] for p in lines if len(p) == 1]
    yaxes = sorted((s for s in single if abs(s[0] - s[2]) < 0.01 and abs(s[3] - s[1]) > 20), key=lambda s: min(s[1], s[3]))
    if len(yaxes) != 2:
        raise ValueError(f"{len(yaxes)} y-axis segments, expected 2")
    ax = yaxes[0][0]
    ticks = [s[1] for s in single if s[1] == s[3] and abs(max(s[0], s[2]) - ax) < 0.05 and abs(s[2] - s[0]) > 3.5
             and min(s[0], s[2]) < ax]
    labels = [(y, v) for (x0, y0, x1, y1, t) in fig.words() for y, v in [((y0 + y1) / 2, _num(t))]
              if v is not None and x1 < ax]
    cals = []
    for seg in yaxes:
        top, bottom = min(seg[1], seg[3]), max(seg[1], seg[3])
        marks = []
        for y, v in labels:
            near = [t for t in ticks if abs(t - y) < 1.5 and top - 0.1 <= t <= bottom + 0.1]
            if near:
                marks.append((min(near, key=lambda t: abs(t - y)), v))
        cal = calibrate(marks)
        cals.append((cal, top, bottom, cal.residual / abs(cal.slope), marks))
    return ax, cals


def _num(t):
    try:
        return float(t)
    except ValueError:
        return None


def read(fig):
    lines = _lines(fig)
    ax, cals = _axis(fig, lines)

    def cal_for(y):
        for cal, top, bottom, misfit, _ in cals:
            if top - 2.5 <= y <= bottom + 0.1:   # a disc may stand up to its radius above the segment end
                return cal, misfit
        raise ValueError(f"y {y} lies in the axis break")

    # one error bar per column; its stem x is the column x
    bars = [p for p in lines if len(p) == 3 and p[0][1] == p[0][3] and p[1][0] == p[1][2] and p[2][1] == p[2][3]]
    cols = sorted((p[1][0], p) for p in bars)
    if len(cols) != 6:
        raise ValueError(f"{len(cols)} error bars, expected 6")
    means = [p[0] for p in lines if len(p) == 1 and p[0][1] == p[0][3] and 10.0 < abs(p[0][2] - p[0][0]) < 10.4]

    discs = []
    for d in fig.drawings():
        f, r = d.get("fill"), d["rect"]
        if f is None or not all(it[0] == "c" for it in d["items"]) or len(d["items"]) != 4:
            continue
        if abs(r.width - r.height) > 0.01 or not 3.4 < r.width < 3.7:
            raise ValueError(f"unexpected filled shape {r}")
        g = [k for k, c in COLOURS.items() if max(abs(a - b) for a, b in zip(f, c)) < 0.02]
        if len(g) != 1:
            raise ValueError(f"unknown disc colour {f}")
        discs.append(((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2, g[0]))

    per = {}
    for (line, g), (cx, path) in zip(COLUMNS, cols):
        mine = [(x, y) for x, y, c in discs if min(cols, key=lambda k: abs(k[0] - x))[0] == cx]
        if any(c != g for x, y, c in discs if min(cols, key=lambda k: abs(k[0] - x))[0] == cx):
            raise ValueError(f"{line} {g}: column holds discs of another colour")
        m = [s[1] for s in means if abs((s[0] + s[2]) / 2 - cx) < 0.5]
        if len(m) != 1:
            raise ValueError(f"{line} {g}: {len(m)} mean strokes")
        upper = min(path[0][1], path[2][1])
        cal, misfit = cal_for(m[0])
        unc = VECTOR_UNCERTAINTY_PT + misfit
        mean = point(cal, m[0], unc, (cx, m[0]))
        cal_e, misfit_e = cal_for(upper)
        err = point(cal_e, upper, VECTOR_UNCERTAINTY_PT + misfit_e, (cx, upper))
        pts = []
        for x, y in sorted(mine, key=lambda p: p[1]):
            c, mf = cal_for(y)
            pts.append(point(c, y, VECTOR_UNCERTAINTY_PT + mf, (x, y)))
        per[(line, g)] = {"points": pts, "countable": True,
                          "bar": {"mean": [mean["value"], mean["lo"], mean["hi"]],
                                  "error": [err["value"], err["lo"], err["hi"]]}}
    if len(discs) != sum(len(v["points"]) for v in per.values()):
        raise ValueError("a disc was not assigned to a column")

    groups = {}
    for line in ("PLZ", "MYL2"):
        for pair in PAIRS:
            for g in pair:
                groups[_label(line, pair, g)] = per[(line, g)]
    return {"groups": groups}
