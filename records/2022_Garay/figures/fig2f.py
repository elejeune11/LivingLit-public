"""Fig. 2F (% cTnT+MLC-2v+ cells: DMSO 30d, SP 30d, untreated 60d), main.pdf page 4.

Vector panel drawn like Fig. 2C (see fig2cd.py): each point is a translucent disc stored as flattened
pieces (pale where a disc stands alone, darker where discs overlap each other or a black stroke), so no
piece is a whole disc. Centres come from the arcs: every Bezier arc of a disc boundary gives the disc
centre as the meeting point of the normals at its two ends; arcs of the disc radius are clustered and one
cluster is one point. Columns come from the x-axis ticks (left to right DMSO, SP, 60d).

Tick labels are outlined glyphs (no text), so tick values are stated from the printed labels and matched
to the major tick strokes in order from the top. The axis is broken (0-20 below, 40-100 above); every
point lies above the break and only the upper segment is calibrated.

Means are the 11.2 pt horizontal strokes; the upper error-bar end is the upper 5.6 pt cap. The DMSO
error bar is drawn as a black filled outline (a stroke outlined), not as strokes: its upper cap is the
topmost pair of flat edges one stroke width (0.56 pt) apart.
"""
import math

import numpy as np

from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

TICKS = [100, 90, 80, 70, 60, 50]   # upper segment, major ticks from the top (40 sits at the break)
COLUMNS = ["DMSO", "SP", "60d"]
LABELS = {  # label -> column; the same column serves each pairwise item it is in
    "SP vs DMSO: SP": "SP", "SP vs DMSO: DMSO": "DMSO",
    "60d vs DMSO: 60d": "60d", "60d vs DMSO: DMSO": "DMSO",
    "SP vs 60d: SP": "SP", "SP vs 60d: 60d": "60d",
}


def _strokes(fig):
    """Single-line unfilled strokes: (x0, y0, x1, y1)."""
    out = []
    for d in fig.drawings():
        if d.get("fill") is None and len(d["items"]) == 1 and d["items"][0][0] == "l":
            a, b = d["items"][0][1], d["items"][0][2]
            out.append((min(a.x, b.x), min(a.y, b.y), max(a.x, b.x), max(a.y, b.y)))
    return out


def _axis(st):
    """Upper y-axis segment (x, top, bottom), its major tick ys, and the x-tick columns."""
    yaxes = [s for s in st if s[0] == s[2] and s[3] - s[1] > 50]
    if len(yaxes) != 1:
        raise ValueError(f"{len(yaxes)} long vertical axis strokes")
    ax, top, _, bottom = yaxes[0]
    major = sorted(s[1] for s in st if s[1] == s[3] and abs(s[2] - ax) < 0.05 and 3.5 < s[2] - s[0] < 5
                   and top - 0.05 <= s[1] <= bottom)
    xaxis = max(s[1] for s in st if s[1] == s[3] and s[2] - s[0] > 40)
    cols = sorted(s[0] for s in st if s[0] == s[2] and 3.5 < s[3] - s[1] < 5 and abs(s[1] - xaxis) < 0.05)
    return ax, bottom, major, cols


def _arc_centres(fig, x0, x1, y0, y1):
    """Centre and radius from every Bezier arc of a coloured (non-grey) filled piece in the box."""
    out = []
    for d in fig.drawings():
        f, r = d.get("fill"), d["rect"]
        if f is None or max(f) - min(f) < 0.1 or not (x0 <= r.x0 and r.x1 <= x1 and y0 <= r.y0 and r.y1 <= y1):
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
                out.append((c[0], c[1], (r0 + r1) / 2))
    return out


def _discs(arcs, radius, tol=0.25):
    """Cluster arc centres of the disc radius; one cluster per disc. Returns (x, y, votes)."""
    pts = [(x, y) for x, y, r in arcs if abs(r - radius) < 0.08]
    clusters = []
    for x, y in sorted(pts):
        for c in clusters:
            if math.hypot(c[0][0] - x, c[0][1] - y) < tol:
                c.append((x, y))
                break
        else:
            clusters.append([(x, y)])
    return [(float(np.median([p[0] for p in c])), float(np.median([p[1] for p in c])), len(c)) for c in clusters]


def _square_discs(fig, radius, x0, x1, y0, y1):
    """Discs stored as a coloured filled rectangle exactly one disc diameter square (no arcs): centres."""
    out = []
    for d in fig.drawings():
        f, r = d.get("fill"), d["rect"]
        if f is None or max(f) - min(f) < 0.1 or [it[0] for it in d["items"]] != ["re"]:
            continue
        if abs(r.width - 2 * radius) < 0.05 and abs(r.height - 2 * radius) < 0.05 and \
                x0 <= r.x0 and r.x1 <= x1 and y0 <= r.y0 and r.y1 <= y1:
            out.append(((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2, 0))
    return out


def _mean_and_cap(fig, st, cx):
    """Mean line y and upper error-bar end y for the column at cx."""
    near = [s for s in st if s[1] == s[3] and abs((s[0] + s[2]) / 2 - cx) < 1.0]
    mean = [s[1] for s in near if 10.8 < s[2] - s[0] < 11.5]
    caps = [s[1] for s in near if 5.2 < s[2] - s[0] < 6.0]
    if len(mean) != 1:
        raise ValueError(f"column at {cx}: {len(mean)} mean lines")
    if caps:
        return mean[0], min(caps)
    # error bar drawn as a black filled outline: upper cap = topmost pair of flat edges 0.56 pt apart
    ys = []
    for d in fig.drawings():
        f, r = d.get("fill"), d["rect"]
        if f is None or max(f) > 0.1 or abs((r.x0 + r.x1) / 2 - cx) > 1.0 or not r.y0 < mean[0] < r.y1:
            continue
        ys += [it[1].y for it in d["items"] if it[0] == "l" and abs(it[1].y - it[2].y) < 1e-3]
    ys = sorted(set(round(y, 3) for y in ys))
    for i in range(len(ys) - 1):
        if abs(ys[i + 1] - ys[i] - 0.56) < 0.03 and ys[i + 1] < mean[0]:
            return mean[0], (ys[i] + ys[i + 1]) / 2
    raise ValueError(f"column at {cx}: no error-bar cap found")


def read(fig):
    st = _strokes(fig)
    ax, bottom, major, cols = _axis(st)
    if len(major) != len(TICKS) or len(cols) != len(COLUMNS):
        raise ValueError(f"{len(major)} major ticks, {len(cols)} columns")
    cal = calibrate(list(zip(major, TICKS)))
    unc = VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)
    if abs(cal.value(bottom) - 40) > 0.1:
        raise ValueError("upper axis segment does not end at 40")
    box = (ax, cols[-1] + 10, major[0] - 15, bottom + 5)
    arcs = _arc_centres(fig, *box)
    radii = [round(r, 2) for _, _, r in arcs]
    radius = max(set(radii), key=radii.count)
    discs = _discs(arcs, radius)
    for sq in _square_discs(fig, radius, *box):
        if any(math.hypot(sq[0] - d[0], sq[1] - d[1]) < 0.25 for d in discs):
            raise ValueError("a square disc coincides with an arc disc")
        discs.append(sq)
    per_col = {}
    for label, cx in zip(COLUMNS, cols):
        mine = sorted((d for d in discs if abs(d[0] - cx) < 7.5), key=lambda d: d[1])
        if any(d[1] > bottom for d in mine):
            raise ValueError("a point lies below the calibrated segment")
        mean_y, err_y = _mean_and_cap(fig, st, cx)
        m, e = point(cal, mean_y, unc, (cx, mean_y)), point(cal, err_y, unc, (cx, err_y))
        per_col[label] = {
            "points": [point(cal, y, unc, (x, y)) for x, y, _ in mine],
            "countable": True,
            "bar": {"mean": [m["value"], m["lo"], m["hi"]], "error": [e["value"], e["lo"], e["hi"]]},
        }
    if sum(len(g["points"]) for g in per_col.values()) != len(discs):
        raise ValueError("a disc lies outside every column")
    return {"groups": {label: per_col[col] for label, col in LABELS.items()}}
