"""Fig. S4A-D (sarcomere length, surface area, perimeter, length-to-width ratio per cell line), mmc1.pdf page 5.

Four GraphPad bar-and-dot panels, split by the page boxes in PANELS; each has its own y axis, calibrated from its
printed tick labels matched to the major tick strokes ending at the axis line (D is a log axis, 0.5-32). Each panel
has nine filled bars (three cell lines x DMSO 30d, SP 30d, Untreated 60d), identified by fill colour (yellow, purple,
red, the paper's legend colours, e.g. Fig. S4G and S5A) and ordered left to right; the x-axis line labels are checked
against LINES. The error bar is a four-stroke path (stem, cap, stem, cap) centred on the bar; its upper cap is the
upper end of the SEM and the mean is the average of the two cap values in axis units (on the log axis D this is
not the page midpoint). The drawn bar top lies about 0.3 pt below the cap midpoint (half its 0.72 pt outline,
inset), so it is used only as a check (within 0.5 pt); the point means agree with the cap-derived mean. Each point is one whole translucent dark disc (four Bezier arcs,
3.2 pt), so its centre is its rectangle centre; it is assigned to the nearest bar centre and must lie within
COLUMN_HALF of it.
"""
import math

from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

PANELS = {
    "A": ((40.0, 30.0, 226.0, 215.0), False),
    "B": ((226.0, 30.0, 401.0, 225.0), False),
    "C": ((401.0, 30.0, 600.0, 225.0), False),
    "D": ((40.0, 228.0, 258.0, 410.0), True),
}
LINES = ("PLZ", "19004", "MYL2")
GROUPS = ("D30", "SP30", "D60")
SHORT = {"D30": "DMSO", "SP30": "SP", "D60": "60d"}
BAR_COLOURS = {"D30": (0.943, 0.723, 0.082), "SP30": (0.597, 0.305, 0.607), "D60": (0.899, 0.178, 0.125)}
DISC_COLOUR = (0.171, 0.135, 0.089)
COLUMN_HALF = 5.8
# pairs marked in each panel (one label per item group); None: the line's three groups as one measurement
SP_D, D60_D, SP_D60 = ("SP30", "D30"), ("D60", "D30"), ("SP30", "D60")
COMPARED = {
    "A": {"PLZ": [SP_D, D60_D, SP_D60], "19004": [SP_D, D60_D, SP_D60], "MYL2": [SP_D, D60_D, SP_D60]},
    "B": {"PLZ": [SP_D, SP_D60], "19004": [SP_D, D60_D], "MYL2": [SP_D, SP_D60, D60_D]},
    "C": {"PLZ": [SP_D], "19004": [SP_D, D60_D], "MYL2": [SP_D, D60_D]},
    "D": {"PLZ": None, "19004": [SP_D, D60_D], "MYL2": [SP_D, D60_D]},
}


def _inside(r, box):
    return box[0] <= r[0] and r[2] <= box[2] and box[1] <= r[1] and r[3] <= box[3]


def _close(a, b, tol=0.02):
    return max(abs(x - y) for x, y in zip(a, b)) < tol


def _axis(single, words, log):
    """Calibration, its uncertainty (pt) and the axis bottom, from tick labels matched to major tick strokes."""
    vert = [s for s in single if abs(s[0] - s[2]) < 0.01 and abs(s[1] - s[3]) > 100]
    if len(vert) != 1:
        raise ValueError(f"{len(vert)} y axes")
    ax, bottom = vert[0][0], max(vert[0][1], vert[0][3])
    ticks = sorted({round(s[1], 3) for s in single if abs(s[1] - s[3]) < 0.01
                    and abs(max(s[0], s[2]) - ax) < 0.05 and min(s[0], s[2]) < ax - 4.0})
    marks = []
    for x0, y0, x1, y1, t in words:
        try:
            v = float(t.replace("−", "-"))
        except ValueError:
            continue
        if ax - 22 < x1 < ax:
            near = [y for y in ticks if abs(y - (y0 + y1) / 2) < 1.5]
            if len(near) != 1:
                raise ValueError(f"tick label {t}: {len(near)} ticks")
            marks.append((near[0], v))
    if len(marks) != len(ticks):
        raise ValueError(f"{len(marks)} labelled ticks of {len(ticks)} major ticks")
    cal = calibrate(marks, log=log)
    resid_pt = cal.residual / abs(cal.slope)
    return cal, VECTOR_UNCERTAINTY_PT + resid_pt, ax, bottom


def _read_panel(fig, name):
    box, log = PANELS[name]
    draws = [d for d in fig.drawings() if _inside(tuple(d["rect"]), box)]
    words = [w for w in fig.words() if _inside(w[:4], box)]
    strokes = [[(it[1].x, it[1].y, it[2].x, it[2].y) for it in d["items"]] for d in draws
               if "s" in d["type"] and all(it[0] == "l" for it in d["items"])]
    single = [p[0] for p in strokes if len(p) == 1]
    cal, unc, ax, bottom = _axis(single, words, log)

    labels = sorted((w for w in words if w[1] > bottom and any(w[4].startswith(k) for k in LINES)),
                    key=lambda w: w[0])
    if [next(k for k in LINES if w[4].startswith(k)) for w in labels] != list(LINES):
        raise ValueError(f"{name}: x-axis labels {[w[4] for w in labels]}")

    bars = {}
    for d in draws:
        f = d.get("fill")
        if f is None or not all(it[0] == "l" for it in d["items"]) or len(d["items"]) != 3:
            continue
        g = [k for k, c in BAR_COLOURS.items() if _close(f, c)]
        if not g:
            continue
        r = d["rect"]
        if abs(r.y1 - bottom) > 0.05:
            raise ValueError(f"{name}: bar not on the axis {r}")
        bars[round((r.x0 + r.x1) / 2, 2)] = (g[0], r.y0)
    cols = sorted(bars.items())
    keys = [(line, g) for line in LINES for g in GROUPS]
    if [c[1][0] for c in cols] != [k[1] for k in keys]:
        raise ValueError(f"{name}: bar colours left to right {[c[1][0] for c in cols]}")

    errs = [p for p in strokes if len(p) == 4 and all(abs(s[0] - s[2]) < 0.01 for s in (p[0], p[2]))
            and all(abs(s[1] - s[3]) < 0.01 for s in (p[1], p[3]))]

    discs = []
    for d in draws:
        f, r = d.get("fill"), d["rect"]
        if f is None or len(d["items"]) != 4 or not all(it[0] == "c" for it in d["items"]):
            continue
        if abs(r.width - r.height) > 0.01 or not 3.0 < r.width < 3.4 or not _close(f, DISC_COLOUR):
            raise ValueError(f"{name}: unexpected filled shape {r} {f}")
        discs.append(((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2))
    per = {k: [] for k in keys}
    for x, y in discs:
        i = min(range(len(cols)), key=lambda j: abs(cols[j][0] - x))
        if abs(cols[i][0] - x) > COLUMN_HALF:
            raise ValueError(f"{name}: disc at {x:.2f},{y:.2f} in no column")
        per[keys[i]].append((x, y))

    out = {}
    for k, (cx, (g, top)) in zip(keys, cols):
        e = [p for p in errs if abs(p[0][0] - cx) < 0.2]
        if len(e) != 1:
            raise ValueError(f"{name} {k}: {len(e)} error bars")
        upper, lower = sorted((e[0][1][1], e[0][3][1]))
        mid_value = (cal.value(upper) + cal.value(lower)) / 2  # mean +- SEM is symmetric in axis units
        mid = ((math.log10(mid_value) if log else mid_value) - cal.intercept) / cal.slope
        if abs(mid - top) > 0.5:
            raise ValueError(f"{name} {k}: error bar centre {mid:.2f} far from bar top {top:.2f}")
        mean, err = point(cal, mid, unc, (cx, mid)), point(cal, upper, unc, (cx, upper))
        out[k] = {"points": [point(cal, y, unc, (x, y)) for x, y in sorted(per[k], key=lambda p: (p[1], p[0]))],
                  "countable": True,
                  "bar": {"mean": [mean["value"], mean["lo"], mean["hi"]],
                          "error": [err["value"], err["lo"], err["hi"]]}}
    return out


def read(fig):
    groups = {}
    for name in PANELS:
        per = _read_panel(fig, name)
        for line, pairs in COMPARED[name].items():
            if pairs is None:
                for g in GROUPS:
                    groups[f"{name} {line}: {SHORT[g]}"] = per[(line, g)]
                continue
            for pair in pairs:
                for g in pair:
                    groups[f"{name} {line} {SHORT[pair[0]]} vs {SHORT[pair[1]]}: {SHORT[g]}"] = per[(line, g)]
    return {"groups": groups}
