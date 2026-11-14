"""Fig. 5f: calcium transient amplitude (dF/F0) of single-CM ROIs, bars (mean ± s.d.) with one dot per ROI.

Vector panel. Bars left to right: Control organoid (light blue fill, dark blue dots), Infarct organoid-edge
(light orange fill, dark orange dots), Infarct organoid-interior (pale orange fill, orange dots); the labels
are printed under the bars. Error bars are two-sided with caps at both ends.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

LABELS = ["control", "infarct_edge", "infarct_interior"]


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
    labels = [(pos, v) for pos, v in fig.tick_marks("y") if v in (0, 0.2, 0.4, 0.6, 0.8)]
    marks = []
    for pos, v in labels:
        y = min(ticks, key=lambda t: abs(t - pos))
        assert abs(y - pos) < 2.0, (pos, v, y)
        marks.append((y, v))
    assert len(marks) == 5, marks
    cal = calibrate(marks)
    unc = VECTOR_UNCERTAINTY_PT + abs(cal.residual / cal.slope)

    # bar outlines: stroked paths of three lines (left side, top, right side)
    bars = []
    for d in draws:
        ls = _lines(d)
        if d.get("type") == "s" and len(ls) == 3 and 15 < d["rect"].width < 30:
            top = [p.y for p, q in ls if abs(p.y - q.y) < 0.05][0]
            bars.append((d["rect"], top))
    bars.sort(key=lambda b: b[0].x0)
    assert len(bars) == 3, len(bars)

    # error bars: stroked paths of four lines (two stems, two caps), narrow
    errs = [d["rect"] for d in draws if d.get("type") == "s" and len(d["items"]) == 4 and d["rect"].width < 12
            and d["rect"].height > 5]
    dots = [d for d in draws if d.get("type") == "fs" and d["rect"].width < 4 and d["rect"].height < 4]
    centres = [(b[0].x0 + b[0].x1) / 2 for b in bars]

    out = {}
    for i, (label, (r, top)) in enumerate(zip(LABELS, bars)):
        mine = [d for d in dots
                if min(range(3), key=lambda k: abs((d["rect"].x0 + d["rect"].x1) / 2 - centres[k])) == i]
        fills = {tuple(round(c, 2) for c in d["fill"]) for d in mine}
        assert len(fills) == 1, (label, fills)  # each group's dots share one colour
        rects = sorted((d["rect"] for d in mine), key=lambda q: (q.y0, q.x0))
        pts = [point(cal, (q.y0 + q.y1) / 2, unc, ((q.x0 + q.x1) / 2, (q.y0 + q.y1) / 2)) for q in rects]
        eb = [e for e in errs if r.x0 <= (e.x0 + e.x1) / 2 <= r.x1]
        assert len(eb) == 1, (label, len(eb))
        mean = point(cal, top, unc, ((r.x0 + r.x1) / 2, top))
        upper = point(cal, eb[0].y0, unc, ((eb[0].x0 + eb[0].x1) / 2, eb[0].y0))
        out[label] = {"points": pts, "countable": True,
                      "bar": {"mean": [mean["value"], mean["lo"], mean["hi"]],
                              "error": [upper["value"], upper["lo"], upper["hi"]]}}
    assert sum(len(g["points"]) for g in out.values()) == len(dots), "a dot was not assigned to a bar"
    # the interior group is compared in two items (vs edge, vs control); figures.yaml links one item per label,
    # so the same reading is returned under a second label for the second item
    out["infarct_interior_vs_control"] = out["infarct_interior"]
    return {"groups": out}
