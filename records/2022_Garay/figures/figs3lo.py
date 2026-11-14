"""Fig. S3L-O (immunofluorescence: % cTnT+ cells by MLC-2a/MLC-2v pattern; % cTnT+MLC-2v+; % cTnT+MLC-2a+;
MLC-2v+/MLC-2a+ ratio), mmc1.pdf page 4.

Four panels side by side, split by the page boxes in PANELS; each has its own y axis, calibrated from its printed
tick labels matched to the major tick strokes ending at the axis line.
L: grouped bars (MLC-2a+2v-, MLC-2a+2v+, MLC-2a-2v+ x DMSO 30d, SP 30d, 60d), bar colours as in the legend. Each
   point is a whole dark vector circle (four Bezier arcs, 2.5 pt) put in the column of the nearest bar; the mean is
   where the two half stems of the error bar meet (0.28 pt above the stroked bar top), the error value the upper cap.
   The middle cluster (MLC-2a+2v+) is read but not returned (its item is an omnibus statement, not asked for).
M-O: dot panels DMSO, SP, 60d; each point a whole vector circle (4.7 pt) in its legend colour; columns from the
   error bars (cap, stem, cap paths), the mean the long horizontal stroke on each error bar, the error the upper cap.
Each column serves every pairwise item it is in.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

PANELS = {"L": (36.0, 630.0, 200.0, 735.0), "M": (205.0, 604.0, 297.0, 760.0),
          "N": (297.0, 604.0, 384.0, 760.0), "O": (384.0, 604.0, 466.5, 760.0)}
GROUPS = ("D30", "SP30", "D60")
SHORT = {"D30": "DMSO", "SP30": "SP", "D60": "60d"}
BAR_COLOURS = {"D30": (0.94, 0.72, 0.08), "SP30": (0.6, 0.31, 0.61), "D60": (0.9, 0.18, 0.13)}
DISC_COLOURS = {"D30": (0.96, 0.77, 0.1), "SP30": (0.71, 0.44, 0.68), "D60": (0.9, 0.18, 0.13)}
L_CLUSTERS = ("2a only", "2a2v", "2v only")
L_PAIRS = [("SP30", "D30"), ("D60", "D30")]
MNO_PAIRS = [("SP30", "D30"), ("D60", "D30"), ("SP30", "D60")]


def _inside(r, box):
    return box[0] <= r[0] and r[2] <= box[2] and box[1] <= r[1] and r[3] <= box[3]


def _close(a, b, tol=0.02):
    return max(abs(x - y) for x, y in zip(a, b)) < tol


def _panel(fig, box):
    """Drawings, single-line segments and words of one panel box."""
    draws = [d for d in fig.drawings() if _inside(tuple(d["rect"]), box)]
    words = [w for w in fig.words() if _inside(w[:4], box)]
    lines = []
    for d in draws:
        if d.get("fill") is None and all(it[0] == "l" for it in d["items"]):
            lines.append([(it[1].x, it[1].y, it[2].x, it[2].y) for it in d["items"]])
    return draws, lines, words


def _axis(lines, words):
    """Calibration, its uncertainty (pt) and the axis bottom, from tick labels matched to major tick strokes."""
    single = [p[0] for p in lines if len(p) == 1]
    vert = [s for s in single if abs(s[0] - s[2]) < 0.01 and abs(s[1] - s[3]) > 60]
    if len(vert) != 1:
        raise ValueError(f"{len(vert)} y axes")
    ax, bottom = vert[0][0], max(vert[0][1], vert[0][3])
    ticks = [s[1] for s in single if abs(s[1] - s[3]) < 0.01 and abs(max(s[0], s[2]) - ax) < 0.05
             and min(s[0], s[2]) < ax - 3.5]
    marks = []
    for x0, y0, x1, y1, t in words:
        try:
            v = float(t.replace("−", "-"))
        except ValueError:
            continue
        if ax - 15 < x1 < ax:
            near = [y for y in ticks if abs(y - (y0 + y1) / 2) < 1.5]
            if len(near) != 1:
                raise ValueError(f"tick label {t}: {len(near)} ticks")
            marks.append((near[0], v))
    if len(marks) != len(ticks):
        raise ValueError(f"{len(marks)} labelled ticks of {len(ticks)} major ticks")
    cal = calibrate(marks)
    return cal, VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope), bottom


def _entry(cal, unc, pts, x, mean_y, upper_y):
    m, e = point(cal, mean_y, unc, (x, mean_y)), point(cal, upper_y, unc, (x, upper_y))
    return {"points": [point(cal, py, unc, (px, py)) for px, py in sorted(pts, key=lambda p: (p[1], p[0]))],
            "countable": True,
            "bar": {"mean": [m["value"], m["lo"], m["hi"]], "error": [e["value"], e["lo"], e["hi"]]}}


def _read_l(fig):
    draws, lines, words = _panel(fig, PANELS["L"])
    cal, unc, _ = _axis(lines, words)
    bars = []
    for d in draws:
        f = d.get("fill")
        if f is None or d["items"][0][0] != "l" or len(d["items"]) != 3:
            continue
        g = [k for k, c in BAR_COLOURS.items() if _close(f, c)]
        if len(g) != 1:
            raise ValueError(f"unknown bar colour {f}")
        bars.append(((d["rect"].x0 + d["rect"].x1) / 2, g[0]))
    bars.sort()
    keys = [(c, g) for c in L_CLUSTERS for g in GROUPS]
    if [b[1] for b in bars] != [k[1] for k in keys]:
        raise ValueError(f"bar order {[b[1] for b in bars]}")
    errs = {}
    for p in lines:
        if len(p) == 4 and all(abs(s[0] - s[2]) < 0.01 for s in (p[0], p[2])):
            cx = p[0][0]
            i = min(range(len(bars)), key=lambda j: abs(bars[j][0] - cx))
            if abs(bars[i][0] - cx) > 0.5 or i in errs:
                raise ValueError(f"error bar at {cx:.2f}")
            errs[i] = (p[0][3], min(min(s[1], s[3]) for s in p))
    if len(errs) != len(bars):
        raise ValueError(f"{len(errs)} error bars of {len(bars)} bars")
    per = {i: [] for i in range(len(bars))}
    for d in draws:
        r = d["rect"]
        if d.get("fill") is None or len(d["items"]) != 4 or not all(it[0] == "c" for it in d["items"]):
            continue
        if not (2.3 < r.width < 2.7 and abs(r.width - r.height) < 0.01):
            raise ValueError(f"unexpected disc {r}")
        x, y = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
        i = min(range(len(bars)), key=lambda j: abs(bars[j][0] - x))
        if abs(bars[i][0] - x) > 4.5:
            raise ValueError(f"disc at {x:.2f},{y:.2f} not in a column")
        per[i].append((x, y))
    return {keys[i]: _entry(cal, unc, per[i], bars[i][0], errs[i][0], errs[i][1]) for i in range(len(bars))}


def _read_dots(fig, name):
    draws, lines, words = _panel(fig, PANELS[name])
    cal, unc, bottom = _axis(lines, words)
    labels = sorted((w for w in words if w[1] > bottom and w[4] in SHORT.values()), key=lambda w: w[0])
    if [w[4] for w in labels] != [SHORT[g] for g in GROUPS]:
        raise ValueError(f"{name}: x-axis labels {[w[4] for w in labels]}")
    bars = sorted((p[1][0], p) for p in lines if len(p) == 3 and abs(p[0][1] - p[0][3]) < 0.01
                  and abs(p[1][0] - p[1][2]) < 0.01 and abs(p[2][1] - p[2][3]) < 0.01 and abs(p[0][2] - p[0][0]) < 6)
    if len(bars) != len(GROUPS):
        raise ValueError(f"{name}: {len(bars)} error bars")
    means = [p[0] for p in lines if len(p) == 1 and abs(p[0][1] - p[0][3]) < 0.01 and 9 < abs(p[0][2] - p[0][0]) < 12]
    per = {g: [] for g in GROUPS}
    for d in draws:
        f, r = d.get("fill"), d["rect"]
        if f is None or len(d["items"]) != 4 or not all(it[0] == "c" for it in d["items"]):
            continue
        if abs(r.width - r.height) > 0.01 or not 4.5 < r.width < 4.9:
            raise ValueError(f"{name}: unexpected filled shape {r}")
        g = [k for k, c in DISC_COLOURS.items() if _close(f, c)]
        if len(g) != 1:
            raise ValueError(f"{name}: unknown disc colour {f}")
        x, y = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
        i = min(range(len(bars)), key=lambda j: abs(bars[j][0] - x))
        if GROUPS[i] != g[0] or abs(bars[i][0] - x) > 4.5:
            raise ValueError(f"{name}: disc {g[0]} at {x:.2f},{y:.2f} not in its column")
        per[g[0]].append((x, y))
    out = {}
    for g, (cx, path) in zip(GROUPS, bars):
        m = [s[1] for s in means if abs((s[0] + s[2]) / 2 - cx) < 0.5]
        if len(m) != 1:
            raise ValueError(f"{name} {g}: {len(m)} mean strokes")
        out[g] = _entry(cal, unc, per[g], cx, m[0], min(path[0][1], path[2][1]))
    return out


def read(fig):
    groups = {}
    l = _read_l(fig)
    for cluster in ("2a only", "2v only"):
        for pair in L_PAIRS:
            for g in pair:
                groups[f"L {cluster} {SHORT[pair[0]]} vs {SHORT[pair[1]]}: {SHORT[g]}"] = l[(cluster, g)]
    for name in ("M", "N", "O"):
        per = _read_dots(fig, name)
        for pair in MNO_PAIRS:
            for g in pair:
                groups[f"{name} {SHORT[pair[0]]} vs {SHORT[pair[1]]}: {SHORT[g]}"] = per[g]
    return {"groups": groups}
