"""Fig. 2g (journal_version.pdf p. 3): Vpara/Vortho ratio of laminar NRVM tissues by filament spacing.

Vector panel: grey bars (mean), one s.e.m. cap above each bar, open circles (individual tissues).
A green band and a dashed line at ratio 1 sit under the bars; they are not data.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

GREY = (0.2514, 0.2514, 0.2514)
SPACINGS = ["40", "60", "80", "100"]


def _close(a, b, tol=0.02):
    return a is not None and all(abs(x - y) <= tol for x, y in zip(a, b))


def read(fig):
    words = fig.words()
    draws = fig.drawings()

    # y axis: short horizontal tick strokes left of the axis, matched to the nearest numeric label
    labels = [((w[1] + w[3]) / 2, float(w[4])) for w in words if w[4] in {"0", "1", "2", "3"} and w[2] < 73]
    ticks = [d["rect"].y0 for d in draws if d["type"] == "s" and d["rect"].height == 0
             and d["rect"].width < 1.5 and d["rect"].x1 < 76]
    marks = []
    for y in ticks:
        ly, v = min(labels, key=lambda lv: abs(lv[0] - y))
        if abs(ly - y) < 2:
            marks.append((y, v))
    cal = calibrate(marks)
    unc = VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)

    # categories: x-axis labels under the axis
    cats = {w[4]: (w[0] + w[2]) / 2 for w in words if w[4] in SPACINGS and 395 < w[1] < 405}

    def cat(x):
        k = min(cats, key=lambda c: abs(cats[c] - x))
        return k if abs(cats[k] - x) < 4 else None

    groups = {c: {"points": [], "countable": True, "bar": {}} for c in SPACINGS}
    for d in draws:
        r = d["rect"]
        cx, cy = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
        c = cat(cx)
        if c is None:
            continue
        items = d["items"]
        if d["type"] == "s" and 1.2 < r.width < 2 and 1.2 < r.height < 2 and all(i[0] == "c" for i in items):
            groups[c]["points"].append(point(cal, cy, unc, (cx, cy)))
        elif d["type"] == "f" and _close(d.get("fill"), GREY) and items[0][0] == "re":
            groups[c]["bar"]["mean"] = list((cal.value(r.y0), *cal.interval(r.y0, unc)))
        elif d["type"] == "s" and r.height == 0 and 1 < r.width < 1.5 and r.y1 < 390:
            groups[c]["bar"]["error"] = list((cal.value(r.y0), *cal.interval(r.y0, unc)))
    for g in groups.values():
        g["points"].sort(key=lambda p: -p["value"])
    return {"groups": groups}
