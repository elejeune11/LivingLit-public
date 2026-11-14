"""Fig. S3P (western blot: relative ssTnI (fetal) and cTnI (adult) expression, DMSO vs SP), mmc1.pdf page 4.

Two paired dot panels side by side, split by the page boxes in PANELS; each has its own y axis, calibrated from its
printed tick labels matched to the major tick strokes ending at the axis line. Each point is a whole vector circle
(four Bezier arcs, 4.74 pt) in its legend colour, DMSO left and SP right; no mean or error bar is drawn.
Each straight stroke between the two columns joins one DMSO disc centre to one SP disc centre (one pair); the script
checks every disc ends exactly one stroke, and returns the points of both groups in pair order (index i of DMSO is
paired with index i of SP), pairs ordered by the DMSO value from the top of the axis down.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

PANELS = {"ssTnI": (466.5, 600.0, 520.0, 760.0), "cTnI": (520.0, 600.0, 580.0, 760.0)}
GROUPS = ("D30", "SP30")
SHORT = {"D30": "DMSO", "SP30": "SP"}
DISC_COLOURS = {"D30": (0.943, 0.723, 0.08), "SP30": (0.714, 0.444, 0.68)}


def _inside(r, box):
    return box[0] <= r[0] and r[2] <= box[2] and box[1] <= r[1] and r[3] <= box[3]


def _close(a, b, tol=0.02):
    return max(abs(x - y) for x, y in zip(a, b)) < tol


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


def _read_panel(fig, name):
    box = PANELS[name]
    draws = [d for d in fig.drawings() if _inside(tuple(d["rect"]), box)]
    words = [w for w in fig.words() if _inside(w[:4], box)]
    lines = [[(it[1].x, it[1].y, it[2].x, it[2].y) for it in d["items"]] for d in draws
             if d.get("fill") is None and all(it[0] == "l" for it in d["items"])]
    cal, unc, bottom = _axis(lines, words)
    labels = sorted((w for w in words if w[1] > bottom and w[4] in SHORT.values()), key=lambda w: w[0])
    if [w[4] for w in labels] != [SHORT[g] for g in GROUPS]:
        raise ValueError(f"{name}: x-axis labels {[w[4] for w in labels]}")
    discs = {g: [] for g in GROUPS}
    for d in draws:
        f, r = d.get("fill"), d["rect"]
        if f is None or len(d["items"]) != 4 or not all(it[0] == "c" for it in d["items"]):
            continue
        if abs(r.width - r.height) > 0.01 or not 4.5 < r.width < 4.9:
            raise ValueError(f"{name}: unexpected filled shape {r}")
        g = [k for k, c in DISC_COLOURS.items() if _close(f, c)]
        if len(g) != 1:
            raise ValueError(f"{name}: unknown disc colour {f}")
        discs[g[0]].append(((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2))
    xs = {g: sorted({round(p[0], 2) for p in discs[g]}) for g in GROUPS}
    if any(len(v) != 1 for v in xs.values()) or not xs["D30"][0] < xs["SP30"][0]:
        raise ValueError(f"{name}: disc columns {xs}")
    # pair strokes: one straight segment from the DMSO column to the SP column
    strokes = [p[0] for p in lines if len(p) == 1 and abs(p[0][0] - p[0][2]) > 5
               and {round(p[0][0], 2), round(p[0][2], 2)} == {xs["D30"][0], xs["SP30"][0]}]
    used = {g: set() for g in GROUPS}
    pairs = []
    for x0, y0, x1, y1 in strokes:
        ends = {round(x0, 2): y0, round(x1, 2): y1}
        idx = {}
        for g in GROUPS:
            y = ends[xs[g][0]]
            near = [i for i, p in enumerate(discs[g]) if abs(p[1] - y) < 0.05]
            if len(near) != 1 or near[0] in used[g]:
                raise ValueError(f"{name}: stroke end {g} at y={y:.2f} meets {len(near)} free discs")
            used[g].add(near[0])
            idx[g] = near[0]
        pairs.append(idx)
    for g in GROUPS:
        if len(used[g]) != len(discs[g]):
            raise ValueError(f"{name}: {len(discs[g]) - len(used[g])} {g} discs in no pair")
    pairs.sort(key=lambda idx: discs["D30"][idx["D30"]][1])
    out = {}
    for g in GROUPS:
        pts = [discs[g][idx[g]] for idx in pairs]
        out[g] = {"points": [point(cal, py, unc, (px, py)) for px, py in pts], "countable": True}
    return out


def read(fig):
    groups = {}
    for name in PANELS:
        for g, v in _read_panel(fig, name).items():
            groups[f"{name}: {SHORT[g]}"] = v
    return {"groups": groups}
