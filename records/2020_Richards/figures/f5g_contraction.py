"""Fig. 5g: contraction amplitude (fractional area change) at D10, bars with one dot per organoid.

Vector panel. Bars left to right: Control organoid (light blue fill, dark blue dots), Infarct organoid
(light orange fill, orange dots); the labels are printed under the bars. Each bar is one stroked path of six
lines: the bar outline (left side, top, right side) and a one-sided upper error bar (cap and stem). Each dot is
drawn twice, as two concentric filled shapes of the same colour (4 and 48 path items); the 48-item shape is
taken as the dot.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

LABELS = ["control", "infarct"]


def _lines(d):
    return [(it[1], it[2]) for it in d["items"] if it[0] == "l"]


def read(fig):
    draws = fig.drawings()
    x0c, _, x1c, _ = fig.crop

    # y-axis path: one stroked path holding the vertical axis line and short horizontal ticks to its left
    ticks = []
    for d in draws:
        if d.get("type") != "s":
            continue
        for p, q in _lines(d):
            if abs(p.y - q.y) < 0.05 and 1 < abs(p.x - q.x) < 4 and x0c <= min(p.x, q.x) and max(p.x, q.x) <= x1c:
                ticks.append(p.y)
    labels = [(pos, v) for pos, v in fig.tick_marks("y") if v in (0, 0.01, 0.02, 0.03, 0.04)]
    marks = []
    for pos, v in labels:
        y = min(ticks, key=lambda t: abs(t - pos))
        assert abs(y - pos) < 2.0, (pos, v, y)
        marks.append((y, v))
    assert len(marks) == 5, marks
    cal = calibrate(marks)
    unc = VECTOR_UNCERTAINTY_PT + abs(cal.residual / cal.slope)

    # bar + error bar paths: stroked, six lines, bar-wide
    bars = []
    for d in draws:
        ls = _lines(d)
        if d.get("type") == "s" and len(ls) == 6 and 15 < d["rect"].width < 30:
            hor = sorted({round(p.y, 2) for p, q in ls if abs(p.y - q.y) < 0.05})
            assert len(hor) == 2, hor  # cap (upper) and bar top
            bars.append((d["rect"], hor[1], hor[0]))
    bars.sort(key=lambda b: b[0].x0)
    assert len(bars) == 2, len(bars)

    dots = [d for d in draws if d.get("type") == "f" and len(d["items"]) == 48
            and d["rect"].width < 4 and d["rect"].height < 4]
    inner = [d for d in draws if d.get("type") == "f" and len(d["items"]) == 4
             and d["rect"].width < 2 and d["rect"].height < 2]
    assert len(inner) == len(dots), (len(inner), len(dots))  # every dot has its concentric twin
    centres = [(b[0].x0 + b[0].x1) / 2 for b in bars]

    out = {}
    for i, (label, (r, top, cap)) in enumerate(zip(LABELS, bars)):
        mine = [d for d in dots
                if min(range(2), key=lambda k: abs((d["rect"].x0 + d["rect"].x1) / 2 - centres[k])) == i]
        fills = {tuple(round(c, 2) for c in d["fill"]) for d in mine}
        assert len(fills) == 1, (label, fills)  # each group's dots share one colour
        rects = sorted((d["rect"] for d in mine), key=lambda q: (q.y0, q.x0))
        pts = [point(cal, (q.y0 + q.y1) / 2, unc, ((q.x0 + q.x1) / 2, (q.y0 + q.y1) / 2)) for q in rects]
        cx = (r.x0 + r.x1) / 2
        mean = point(cal, top, unc, (cx, top))
        upper = point(cal, cap, unc, (cx, cap))
        out[label] = {"points": pts, "countable": True,
                      "bar": {"mean": [mean["value"], mean["lo"], mean["hi"]],
                              "error": [upper["value"], upper["lo"], upper["hi"]]}}
    assert sum(len(g["points"]) for g in out.values()) == len(dots), "a dot was not assigned to a bar"
    return {"groups": out}
