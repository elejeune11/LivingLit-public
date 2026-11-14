"""Fig. 4i: elastic modulus (kPa), bars (mean ± s.d.) with individual organoids as filled dots.

Vector panel. Left bar Control (light blue fill, dark blue dots), right bar Infarct (light orange fill,
orange dots); "Control" and "Infarct" printed under the bars.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

LABELS = ["control", "infarct"]


def read(fig):
    draws = fig.drawings()

    # y-axis path: the stroked path holding the short horizontal tick lines left of the axis
    ticks = []
    for d in draws:
        if d.get("type") == "s" and len(d["items"]) >= 6:
            for it in d["items"]:
                if it[0] == "l":
                    p, q = it[1], it[2]
                    if abs(p.y - q.y) < 0.05 and 1 < abs(p.x - q.x) < 4:
                        ticks.append(p.y)
    assert len(ticks) == 6, ticks
    labels = [(pos, v) for pos, v in fig.tick_marks("y") if v in (0, 1, 2, 3, 4, 5)]
    marks = []
    for pos, v in labels:
        y = min(ticks, key=lambda t: abs(t - pos))
        assert abs(y - pos) < 2.0, (pos, v, y)
        marks.append((y, v))
    assert len(marks) == 6, marks
    cal = calibrate(marks)
    unc = VECTOR_UNCERTAINTY_PT + abs(cal.residual / cal.slope)

    bars = sorted([d for d in draws if d.get("type") == "f" and d["rect"].height > 15 and 20 < d["rect"].width < 30],
                  key=lambda d: d["rect"].x0)
    assert len(bars) == 2, len(bars)
    # error bars: stroked paths of 4 lines (two stems and two caps), narrow
    errs = [d for d in draws if d.get("type") == "s" and len(d["items"]) == 4 and d["rect"].width < 8]
    dots = [d for d in draws if d.get("type") == "fs" and d["rect"].width < 4 and d["rect"].height < 4]

    out = {}
    for label, b in zip(LABELS, bars):
        r = b["rect"]
        mine = [d["rect"] for d in dots if r.x0 - 3 <= (d["rect"].x0 + d["rect"].x1) / 2 <= r.x1 + 3]
        pts = [point(cal, (q.y0 + q.y1) / 2, unc, ((q.x0 + q.x1) / 2, (q.y0 + q.y1) / 2))
               for q in sorted(mine, key=lambda q: (q.y0, q.x0))]
        eb = [d["rect"] for d in errs if r.x0 <= (d["rect"].x0 + d["rect"].x1) / 2 <= r.x1]
        assert len(eb) == 1, (label, len(eb))
        mean = point(cal, r.y0, unc, (r.x0, r.y0))
        top = point(cal, eb[0].y0, unc, (eb[0].x0, eb[0].y0))
        out[label] = {"points": pts, "countable": True,
                      "bar": {"mean": [mean["value"], mean["lo"], mean["hi"]],
                              "error": [top["value"], top["lo"], top["hi"]]}}
    assert sum(len(g["points"]) for g in out.values()) == len(dots), "a dot was not assigned to a bar"
    return {"groups": out}
