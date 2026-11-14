"""Fig. 4c (bottom): TEER of the endothelial barrier under each tissue, day 0 and day 14 (vector).

Horizontal bars: x axis unit area resistance (Ohms x cm2), 0-20. One row pair per tissue
(Skin, Bone, Heart, Liver from top); the pink row (above) is Day 14, the black row (below) Day 0.
Points: black filled circles (Day 0), pink filled squares (Day 14), each drawn once or twice
(fill and stroke); duplicates share a centre. Error bar: a full whisker (mean - s.d. to mean + s.d.)
drawn as one 5-segment path; its right cap is the upper end and its midpoint the mean. The bar's
own outline ends about 0.46 pt left of the whisker midpoint (stroke inset), so the mean interval
spans both.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

PINK = (0.898, 0.122, 0.4)
BLACK = (0.0, 0.0, 0.0)
TISSUES = {"Liver": "liver", "Heart": "heart", "Bone": "bone", "Skin": "skin"}


def _close(c, ref, tol=0.08):
    return c is not None and max(abs(a - b) for a, b in zip(c, ref)) <= tol


def read(fig):
    words = fig.words()
    draws = fig.drawings()

    # x axis: major tick lines (vertical, below the axis) matched to their numeric labels
    axis_y = max(d["rect"].y0 for d in draws if d["rect"].height == 0 and d["rect"].width > 40)
    ticks = sorted({round(d["rect"].x0, 3) for d in draws
                    if d["rect"].width == 0 and abs(d["rect"].y0 - axis_y) < 0.1 and d["rect"].height > 2})
    labels = [((w[0] + w[2]) / 2, float(w[4])) for w in words
              if w[4].isdigit() and w[1] > axis_y and w[1] < axis_y + 8]
    marks = []
    for pos, v in labels:
        t = min(ticks, key=lambda t: abs(t - pos))
        if abs(t - pos) < 1.0:
            marks.append((t, v))
    cal = calibrate(marks)
    unc = VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)

    # legend markers sit just left of the words "Day"
    legend = [((w[0]), (w[1] + w[3]) / 2) for w in words if w[4] == "Day"]

    def in_legend(x, y):
        return any(0 < lx - x < 4 and abs(ly - y) < 2 for lx, ly in legend)

    # bars: 5-segment outlines starting at the y axis; row centre and colour give the group
    bars = {}
    for d in draws:
        r = d["rect"]
        if len(d["items"]) == 5 and r.height > 4 and abs(r.x0 - ticks[0]) < 0.1 and d.get("fill") is None:
            col = "d14" if _close(d.get("color"), PINK) else "d0" if _close(d.get("color"), BLACK) else None
            if col:
                bars[(round((r.y0 + r.y1) / 2, 2), col)] = r.x1
    tissue_y = {TISSUES[w[4]]: (w[1] + w[3]) / 2 for w in words if w[4] in TISSUES}

    def label_for(yc, col):
        t = min(tissue_y, key=lambda k: abs(tissue_y[k] - yc))
        return f"{t}_{col}"

    rows = {}
    for (yc, col), x1 in bars.items():
        rows[label_for(yc, col)] = {"y": yc, "col": col, "bar_end": x1}

    # whiskers: 5-segment paths, height ~2.4 pt, centred on a bar row
    whisk = {}
    for d in draws:
        r = d["rect"]
        if len(d["items"]) == 5 and 2 < r.height < 3 and d.get("fill") is None:
            yc = (r.y0 + r.y1) / 2
            lab = min(rows, key=lambda k: abs(rows[k]["y"] - yc))
            if abs(rows[lab]["y"] - yc) < 1.0:
                whisk[lab] = (r.x0, r.x1)

    # markers: small filled shapes, circles (curves) black, squares (re) pink
    pts = {k: set() for k in rows}
    for d in draws:
        r = d["rect"]
        f = d.get("fill")
        if f is None or not (1.5 < r.width < 3.5 and 1.5 < r.height < 3.5):
            continue
        kinds = {it[0] for it in d["items"]}
        col = "d0" if kinds == {"c"} and _close(f, BLACK) else "d14" if kinds == {"re"} and _close(f, PINK) else None
        if col is None:
            continue
        x, y = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
        if in_legend(x, y):
            continue
        cands = [k for k in rows if rows[k]["col"] == col]
        lab = min(cands, key=lambda k: abs(rows[k]["y"] - y))
        if abs(rows[lab]["y"] - y) < 3.5:
            pts[lab].add((round(x, 3), round(y, 3)))

    groups = {}
    for lab, row in rows.items():
        g = {"points": [point(cal, x, unc, (x, y)) for x, y in sorted(pts[lab])], "countable": True}
        if lab in whisk:
            lo_x, hi_x = whisk[lab]
            mid = (lo_x + hi_x) / 2
            m_lo, m_hi = cal.interval(min(mid, row["bar_end"]) - unc, 0)[0], cal.interval(max(mid, row["bar_end"]) + unc, 0)[1]
            e_lo, e_hi = cal.interval(hi_x, unc)
            g["bar"] = {"mean": [cal.value(mid), min(m_lo, cal.value(mid)), max(m_hi, cal.value(mid))],
                        "error": [cal.value(hi_x), e_lo, e_hi]}
        groups[lab] = g
    return {"groups": groups}
