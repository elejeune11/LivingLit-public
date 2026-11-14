"""Fig. 4f: bone TRAP activity (absorbance normalized to chamber volume), day 0 and day 28 (vector).

Vertical bars: y axis -0.5 to 1.0, major ticks every 0.5 with labels. One bar pair per condition
(Multi-organ, Mixed, Isolated from left); the black bar (left) is Day 0, the pink bar (right) Day 28.
Points: black filled circles (Day 0) and pink filled squares (Day 28), six per bar. Error bar: a full
whisker (mean - s.d. to mean + s.d.) drawn as one 5-segment path (drawn three times); its upper cap is
the upper end and its midpoint the mean. The bar outline ends about 0.4 pt short of the whisker
midpoint (stroke inset), so the mean interval spans both. The legend markers sit left of the words "Day".
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

PINK = (0.898, 0.122, 0.4)
BLACK = (0.0, 0.0, 0.0)
CONDITIONS = {"Multi-organ": "mo", "Mixed": "mix", "Isolated": "iso"}


def _close(c, ref, tol=0.08):
    return c is not None and max(abs(a - b) for a, b in zip(c, ref)) <= tol


def read(fig):
    words = fig.words()
    draws = fig.drawings()

    # y axis: the vertical axis line, its major ticks (longest left ticks) matched to numeric labels
    axis = next(d["rect"] for d in draws if d["rect"].width == 0 and d["rect"].height > 40)
    ticks = sorted({round(d["rect"].y0, 3) for d in draws
                    if d["rect"].height == 0 and abs(d["rect"].x1 - axis.x0) < 0.1 and d["rect"].width > 2})
    def num(t):
        t = t.replace("–", "-").replace("−", "-")
        return float(t) if t.replace(".", "").lstrip("-").isdigit() else None

    labels = [((w[1] + w[3]) / 2, num(w[4])) for w in words
              if w[2] < axis.x0 and axis.x0 - w[2] < 6 and num(w[4]) is not None]
    marks = []
    for pos, v in labels:
        t = min(ticks, key=lambda t: abs(t - pos))
        if abs(t - pos) < 1.5:
            marks.append((t, v))
    cal = calibrate(marks)
    unc = VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)
    zero = min(ticks, key=lambda t: abs(cal.value(t)))

    legend = [(w[0], (w[1] + w[3]) / 2) for w in words if w[4] == "Day"]

    def in_legend(x, y):
        return any(0 < lx - x < 4 and abs(ly - y) < 2 for lx, ly in legend)

    # bars: unfilled outlines (4-5 segments) with one edge on the zero line, width ~7 pt
    cond_x = {CONDITIONS[w[4]]: (w[0] + w[2]) / 2 for w in words if w[4] in CONDITIONS and w[1] > axis.y1}
    rows = {}
    for d in draws:
        r = d["rect"]
        if d.get("fill") is None and len(d["items"]) in (4, 5) and 6 < r.width < 8 \
                and (abs(r.y1 - zero) < 0.1 or abs(r.y0 - zero) < 0.1):
            col = "d28" if _close(d.get("color"), PINK) else "d0" if _close(d.get("color"), BLACK) else None
            if col is None:
                continue
            xc = (r.x0 + r.x1) / 2
            rows[(xc, col)] = r.y0 if abs(r.y1 - zero) < 0.1 else r.y1  # the bar's far end
    pairs = sorted({round(xc, 1) for xc, _ in rows})
    labels_for = {}
    for xc, col in rows:
        c = min(cond_x, key=lambda k: abs(cond_x[k] - xc))
        labels_for[(xc, col)] = f"{c}_{col}"
    bars = {labels_for[k]: {"x": k[0], "col": k[1], "end": v} for k, v in rows.items()}
    assert len(bars) == 6 and len(pairs) == 6, bars

    # whiskers: 5-segment paths ~3.4 pt wide centred on a bar
    whisk = {}
    for d in draws:
        r = d["rect"]
        if d.get("fill") is None and len(d["items"]) == 5 and 3 < r.width < 4 and r.height > 1:
            xc = (r.x0 + r.x1) / 2
            lab = min(bars, key=lambda k: abs(bars[k]["x"] - xc))
            if abs(bars[lab]["x"] - xc) < 0.5:
                whisk[lab] = (r.y0, r.y1)

    # markers: black circles (curves) and pink squares (re)
    pts = {k: set() for k in bars}
    for d in draws:
        r = d["rect"]
        f = d.get("fill")
        if f is None or not (1.5 < r.width < 3.5 and 1.5 < r.height < 3.5):
            continue
        kinds = {it[0] for it in d["items"]}
        col = "d0" if kinds == {"c"} and _close(f, BLACK) else "d28" if kinds == {"re"} and _close(f, PINK) else None
        if col is None:
            continue
        x, y = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
        if in_legend(x, y):
            continue
        cands = [k for k in bars if bars[k]["col"] == col]
        lab = min(cands, key=lambda k: abs(bars[k]["x"] - x))
        if abs(bars[lab]["x"] - x) < 4:
            pts[lab].add((round(x, 3), round(y, 3)))

    groups = {}
    for lab, b in bars.items():
        g = {"points": [point(cal, y, unc, (x, y)) for x, y in sorted(pts[lab])], "countable": True}
        if lab in whisk:
            top, bottom = whisk[lab]
            mid = (top + bottom) / 2
            m = sorted([cal.value(mid), *cal.interval(min(mid, b["end"]) - unc, 0), *cal.interval(max(mid, b["end"]) + unc, 0)])
            e_lo, e_hi = cal.interval(top, unc)
            g["bar"] = {"mean": [cal.value(mid), m[0], m[-1]], "error": [cal.value(top), e_lo, e_hi]}
        groups[lab] = g
    return {"groups": groups}
