"""Fig. 3d: peak OCR after FCCP (percentage of non-mitochondrial respiration), bars with error bars and
individual organoids as filled circles.

Vector panel. Left bar Control (blue fill, dark blue dots), right bar Infarct (light orange fill, orange dots);
"Control" and "Infarct" are printed under the bars. Each bar's error bar is one stroked path with caps at both
ends; the upper cap is the error reading.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

DOT = {"control": (0.0, 0.0, 0.75), "infarct": (1.0, 0.38, 0.0)}


def _near(c, rgb, tol=0.03):
    return c is not None and len(c) == 3 and max(abs(a - b) for a, b in zip(c, rgb)) <= tol


def read(fig):
    draws = fig.drawings()

    # y tick lines: short horizontal segments left of the y axis
    ticks = []
    for d in draws:
        if d.get("fill") is None and len(d["items"]) >= 5:
            for it in d["items"]:
                if it[0] == "l":
                    p, q = it[1], it[2]
                    if abs(p.y - q.y) < 0.05 and abs(p.x - q.x) < 4:
                        ticks.append(p.y)
    labels = fig.tick_marks("y")
    labels = [(pos, v) for pos, v in labels if v in (0, 100, 200, 300, 400, 500)]
    assert len(labels) == 6, labels
    marks = []
    for pos, v in labels:
        y = min(ticks, key=lambda t: abs(t - pos))
        assert abs(y - pos) < 2.0, (pos, v, y)
        marks.append((y, v))
    cal = calibrate(marks)
    unc = VECTOR_UNCERTAINTY_PT + abs(cal.residual / cal.slope)

    bars = sorted([d for d in draws if d.get("type") == "f" and d["rect"].height > 10
                   and 15 < d["rect"].width < 30], key=lambda d: d["rect"].x0)
    assert len(bars) == 2, len(bars)
    errs = [d for d in draws if d.get("type") == "s" and len(d["items"]) == 8 and d["rect"].width < 30]

    out = {}
    for label, b in zip(("control", "infarct"), bars):
        r = b["rect"]
        dots = [d["rect"] for d in draws if d.get("type") == "fs" and d["rect"].width < 3
                and d["rect"].height < 3 and _near(d.get("fill"), DOT[label])]
        assert all(r.x0 - 3 <= (q.x0 + q.x1) / 2 <= r.x1 + 3 for q in dots), label
        pts = [point(cal, (q.y0 + q.y1) / 2, unc, ((q.x0 + q.x1) / 2, (q.y0 + q.y1) / 2))
               for q in sorted(dots, key=lambda q: (q.y0, q.x0))]
        eb = [d for d in errs if r.x0 - 0.1 <= d["rect"].x0 and d["rect"].x1 <= r.x1 + 0.1]
        assert len(eb) == 1, (label, len(eb))
        caps = [it[1].y for it in eb[0]["items"] if it[0] == "l" and abs(it[1].y - it[2].y) < 0.05
                and abs(it[1].x - it[2].x) > 4]
        top_y = min(caps)
        mean = point(cal, r.y0, unc, (r.x0, r.y0))
        top = point(cal, top_y, unc, ((r.x0 + r.x1) / 2, top_y))
        out[label] = {"points": pts, "countable": True,
                      "bar": {"mean": [mean["value"], mean["lo"], mean["hi"]],
                              "error": [top["value"], top["lo"], top["hi"]]}}
    return {"groups": out}
