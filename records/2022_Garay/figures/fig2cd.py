"""Fig. 2C (% cTnT+MLC-2v+ cells) and 2D (MLC-2v+/MLC-2a+ ratio, log2 axis), main.pdf page 4.

Vector panels. Each point is a translucent disc that the PDF stores flattened: pale pieces where a disc
stands alone and darker pieces where discs overlap, all cut by the mean and error-bar strokes. No piece is
a whole disc, so centres are found from the arcs: every Bezier arc of a disc boundary gives the disc
centre as the meeting point of the normals at its two ends. Arcs of the disc radius are clustered; one
cluster is one point. Columns come from the x-axis ticks (left to right DMSO, S, P, SP).

Tick labels are outlined glyphs (no text), so the tick values below are stated from the printed labels and
matched to the major tick strokes in order from the top. Panel C has a broken axis (0-20 below, 40-100
above); every point lies above the break and only the upper segment is calibrated. Panel D is log scale
(0.5, 1, 2, 4, 8).

Means are the 6.3 pt horizontal strokes; the upper error-bar end is the upper 3.2 pt cap. The DMSO error
bar in panel C is drawn in the group colour as a filled shape (a stroke outlined), not a black stroke.
"""
import math

import numpy as np

from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

C_TICKS = [100, 90, 80, 70, 60, 50]       # upper segment, major ticks from the top (40 sits at the break)
D_TICKS = [8, 4, 2, 1, 0.5]
COLUMNS = ["DMSO", "S", "P", "SP"]

LABELS = {  # label -> (panel, column)
    "C S vs DMSO: S": ("C", "S"), "C S vs DMSO: DMSO": ("C", "DMSO"),
    "C P vs DMSO: P": ("C", "P"), "C P vs DMSO: DMSO": ("C", "DMSO"),
    "C SP vs DMSO: SP": ("C", "SP"), "C SP vs DMSO: DMSO": ("C", "DMSO"),
    "D SP vs DMSO: SP": ("D", "SP"), "D SP vs DMSO: DMSO": ("D", "DMSO"),
}


def _strokes(fig):
    """Horizontal and vertical single-line strokes: (x0, y0, x1, y1)."""
    out = []
    for d in fig.drawings():
        if d.get("fill") is None and len(d["items"]) == 1 and d["items"][0][0] == "l":
            a, b = d["items"][0][1], d["items"][0][2]
            out.append((min(a.x, b.x), min(a.y, b.y), max(a.x, b.x), max(a.y, b.y)))
    return out


def _panels(fig):
    """For each panel: y axis line x, the major-tick y positions, the x-tick columns."""
    st = _strokes(fig)
    yaxes = sorted((s for s in st if s[0] == s[2] and s[3] - s[1] > 50), key=lambda s: s[0])
    xticks = sorted(s[0] for s in st if s[0] == s[2] and 3.5 < s[3] - s[1] < 5)
    out = {}
    for name, (ax, ytop, _, ybottom) in zip("CD", yaxes):
        major = sorted(s[1] for s in st if s[1] == s[3] and abs(s[2] - ax) < 0.05 and 3.5 < s[2] - s[0] < 5)
        cols = [x for x in xticks if ax < x < ax + 45]
        out[name] = {"axis": ax, "major": major, "cols": cols, "strokes": st, "axis_bottom": ybottom}
    return out


def _cal(major, values, log):
    cal = calibrate(list(zip(major[:len(values)], values)), log=log)
    misfit_pt = cal.residual / abs(cal.slope)
    return cal, misfit_pt


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
                out.append((c[0], c[1], (r0 + r1) / 2, tuple(round(v, 2) for v in f)))
    return out


def _discs(arcs, radius, tol=0.25):
    """Cluster arc centres of the disc radius; one cluster per disc. Returns (x, y, votes)."""
    pts = [(x, y) for x, y, r, _ in arcs if abs(r - radius) < 0.08]
    clusters = []
    for x, y in sorted(pts):
        for c in clusters:
            if math.hypot(c[0][0] - x, c[0][1] - y) < tol:
                c.append((x, y))
                break
        else:
            clusters.append([(x, y)])
    return [(float(np.median([p[0] for p in c])), float(np.median([p[1] for p in c])), len(c)) for c in clusters]


def _cap_and_mean(panel, col_x, fig, colour_box):
    """Mean line y and upper error-bar end y for the column at col_x."""
    st = panel["strokes"]
    near = [s for s in st if s[1] == s[3] and abs((s[0] + s[2]) / 2 - col_x) < 1.0]
    mean = [s[1] for s in near if 6.0 < s[2] - s[0] < 6.6]
    caps = [s[1] for s in near if 3.0 < s[2] - s[0] < 3.4]
    if len(mean) != 1:
        raise ValueError(f"column at {col_x}: {len(mean)} mean lines")
    if caps:
        return mean[0], min(caps)
    # error bar drawn as a filled outline in the group colour: its cap is the widest flat run at the top
    x0, x1, y0, y1 = colour_box
    tops = []
    for d in fig.drawings():
        f = d.get("fill")
        if f is None or max(f) - min(f) < 0.1:
            continue
        for it in d["items"]:
            if it[0] == "l":
                a, b = it[1], it[2]
                if abs(a.y - b.y) < 1e-3 and abs((a.x + b.x) / 2 - col_x) < 2.5 and y0 < a.y < mean[0]:
                    tops.append(a.y)
    ys = sorted(set(round(y, 3) for y in tops))
    # the cap is a 0.56 pt thick bar: the pair of flat edges just below each other nearest the top
    for i in range(len(ys) - 1):
        if abs(ys[i + 1] - ys[i] - 0.56) < 0.03:
            return mean[0], (ys[i] + ys[i + 1]) / 2
    raise ValueError(f"column at {col_x}: no error-bar cap found")


def read(fig):
    panels = _panels(fig)
    groups = {}
    per_panel = {}
    for name, panel in panels.items():
        ticks, log = (C_TICKS, False) if name == "C" else (D_TICKS, True)
        cal, misfit_pt = _cal(panel["major"], ticks, log)
        unc = VECTOR_UNCERTAINTY_PT + misfit_pt
        top = panel["major"][0] - 15
        bottom = panel["axis_bottom"]  # panel C: the end of the upper axis segment, at the break (40)
        if name == "C" and abs(cal.value(bottom) - 40) > 0.1:
            raise ValueError("panel C upper segment does not end at 40")
        arcs = _arc_centres(fig, panel["axis"], panel["axis"] + 45, top, bottom + 5)
        radii = [round(r, 2) for _, _, r, _ in arcs]
        radius = max(set(radii), key=radii.count)
        discs = _discs(arcs, radius)
        cols = {}
        for label, cx in zip(COLUMNS, panel["cols"]):
            mine = sorted((d for d in discs if abs(d[0] - cx) < 4.85), key=lambda d: d[1])
            if name == "C" and any(d[1] > bottom for d in mine):
                raise ValueError("a panel C point lies below the calibrated segment")
            mean_y, err_y = _cap_and_mean(panel, cx, fig, (cx - 2.5, cx + 2.5, top, bottom))
            m, e = point(cal, mean_y, unc, (cx, mean_y)), point(cal, err_y, unc, (cx, err_y))
            cols[label] = {
                "points": [point(cal, y, unc, (x, y)) for x, y, _ in mine],
                "countable": True,
                "bar": {"mean": [m["value"], m["lo"], m["hi"]], "error": [e["value"], e["lo"], e["hi"]]},
            }
        per_panel[name] = cols
    for label, (pn, col) in LABELS.items():
        groups[label] = per_panel[pn][col]
    return {"groups": groups}
