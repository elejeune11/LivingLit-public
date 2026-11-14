"""Fig. 1h (right): NADH index, bars (mean ± s.d.) with individual organoids as black dots.

Vector panel. Bars left to right: Control Edge, Control Interior, Infarct Edge, Infarct Interior
(dark green = Edge, light green = Interior, per the panel's key; "Control" and "Infarct" printed under each pair).
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

LABELS = ["control_edge", "control_interior", "infarct_edge", "infarct_interior"]


def read(fig):
    draws = fig.drawings()

    # tick lines: short horizontal segments of the axis path, left of the plot's y axis
    ticks = []
    for d in draws:
        if d.get("fill") is None and len(d["items"]) >= 5:
            for it in d["items"]:
                if it[0] == "l":
                    p, q = it[1], it[2]
                    if abs(p.y - q.y) < 0.05 and abs(p.x - q.x) < 4:
                        ticks.append(p.y)
    labels = [(pos, v) for pos, v in fig.tick_marks("y") if v in (0, 0.5, 1.0, 1.5)]
    marks = []
    for pos, v in labels:
        y = min(ticks, key=lambda t: abs(t - pos))
        assert abs(y - pos) < 2.0, (pos, v, y)
        marks.append((y, v))
    cal = calibrate(marks)
    unc = VECTOR_UNCERTAINTY_PT + abs(cal.residual / cal.slope)

    bars = sorted([d for d in draws if d.get("fill") is not None and "s" not in (d.get("type") or "")
                   and d["rect"].height > 15 and 10 < d["rect"].width < 20], key=lambda d: d["rect"].x0)
    assert len(bars) == 4, len(bars)
    errs = [d for d in draws if d.get("type") == "s" and len(d["items"]) == 4 and d["rect"].width < 5]
    dots = [d for d in draws if d.get("type") == "fs" and d["rect"].width < 3 and d["rect"].height < 3]

    out = {}
    for label, b in zip(LABELS, bars):
        r = b["rect"]
        mine = [d["rect"] for d in dots if r.x0 - 1 <= (d["rect"].x0 + d["rect"].x1) / 2 <= r.x1 + 1]
        pts = [point(cal, (q.y0 + q.y1) / 2, unc, ((q.x0 + q.x1) / 2, (q.y0 + q.y1) / 2))
               for q in sorted(mine, key=lambda q: (q.y0, q.x0))]
        eb = [d["rect"] for d in errs if r.x0 <= (d["rect"].x0 + d["rect"].x1) / 2 <= r.x1]
        assert len(eb) == 1, (label, len(eb))
        mean = point(cal, r.y0, unc, (r.x0, r.y0))
        top = point(cal, eb[0].y0, unc, (eb[0].x0, eb[0].y0))
        out[label] = {"points": pts, "countable": True,
                      "bar": {"mean": [mean["value"], mean["lo"], mean["hi"]],
                              "error": [top["value"], top["lo"], top["hi"]]}}
    return {"groups": out}
