"""Fig. 3g: normalized l-lactate level (absorbance index, a.u.) in the medium of D10 organoids, bars with
error bars and individual wells as filled circles.

Vector panel. Left bar Control (blue fill, dark blue dots), right bar Infarct (light orange fill, orange dots);
"Control" and "Infarct" are printed under the bars. Each bar's error bar is one stroked path of four lines (two
vertical halves and two caps); the upper cap is the error reading. The y axis has ticks at 0, 0.5, 1.0, 1.5 and
an unlabelled tick at the top of the frame, which is not used.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

DOT = {"control": (0.0, 0.0, 0.75), "infarct": (1.0, 0.38, 0.0)}


def _near(c, rgb, tol=0.03):
    return c is not None and len(c) == 3 and max(abs(a - b) for a, b in zip(c, rgb)) <= tol


def _hline(it):
    return it[0] == "l" and abs(it[1].y - it[2].y) < 0.05


def read(fig):
    draws = fig.drawings()

    # y tick lines: short horizontal segments left of the y axis, in the axis path
    ticks = []
    for d in draws:
        if d.get("fill") is None and len(d["items"]) >= 5:
            for it in d["items"]:
                if _hline(it) and abs(it[1].x - it[2].x) < 4:
                    ticks.append((it[1].y, max(it[1].x, it[2].x)))
    assert ticks, "no y ticks"
    axis_x = max(x for _, x in ticks)
    labels = [(pos, v) for pos, v in fig.tick_marks("y", near=axis_x - 8, tol=6) if v in (0, 0.5, 1.0, 1.5)]
    assert len(labels) == 4, labels
    marks = []
    for pos, v in labels:
        y = min((t for t, _ in ticks), key=lambda t: abs(t - pos))
        assert abs(y - pos) < 2.0, (pos, v, y)
        marks.append((y, v))
    cal = calibrate(marks)
    unc = VECTOR_UNCERTAINTY_PT + abs(cal.residual / cal.slope)

    bars = sorted([d for d in draws if d.get("type") == "f" and d["rect"].height > 10
                   and 15 < d["rect"].width < 30], key=lambda d: d["rect"].x0)
    assert len(bars) == 2, len(bars)
    errs = [d for d in draws if d.get("type") == "s" and len(d["items"]) == 4
            and all(it[0] == "l" for it in d["items"])
            and sum(_hline(it) and abs(it[1].x - it[2].x) > 4 for it in d["items"]) == 2]

    out = {}
    for label, b in zip(("control", "infarct"), bars):
        r = b["rect"]
        dots = [d["rect"] for d in draws if d.get("type") == "fs" and d["rect"].width < 3.5
                and d["rect"].height < 3.5 and _near(d.get("fill"), DOT[label])]
        assert all(r.x0 - 3 <= (q.x0 + q.x1) / 2 <= r.x1 + 3 for q in dots), label
        pts = [point(cal, (q.y0 + q.y1) / 2, unc, ((q.x0 + q.x1) / 2, (q.y0 + q.y1) / 2))
               for q in sorted(dots, key=lambda q: (q.y0, q.x0))]
        eb = [d for d in errs if any(it[0] == "l" and abs(it[1].x - it[2].x) < 0.05
                                     and r.x0 < it[1].x < r.x1 for it in d["items"])]
        assert len(eb) == 1, (label, len(eb))
        caps = [it[1].y for it in eb[0]["items"] if _hline(it) and abs(it[1].x - it[2].x) > 4]
        top_y = min(caps)
        mean = point(cal, r.y0, unc, (r.x0, r.y0))
        top = point(cal, top_y, unc, ((r.x0 + r.x1) / 2, top_y))
        out[label] = {"points": pts, "countable": True,
                      "bar": {"mean": [mean["value"], mean["lo"], mean["hi"]],
                              "error": [top["value"], top["lo"], top["hi"]]}}
    return {"groups": out}
