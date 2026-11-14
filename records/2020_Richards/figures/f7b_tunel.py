"""Fig. 7b: normalized TUNEL index, bars with error bars and individual organoids as filled dots.

Vector panel. Four DOX doses (0, 0.1, 1.0, 10.0 µM) on the x axis, each with a Control bar (light blue
fill, dark blue dots) left of the dose tick and an Infarct bar (light orange fill, orange dots) right of it.
Only the 1.0 µM pair is read: it is the only pair an evidence item compares (F7b_tunel, i1 vs c1).
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

DOSE = 1.0
BAR_FILL = {"control": (0.553, 0.553, 1.0), "infarct": (1.0, 0.753, 0.502)}
DOT_FILL = {"control": (0.0, 0.0, 0.75), "infarct": (1.0, 0.38, 0.0)}


def _same(a, b, tol=0.02):
    return a is not None and all(abs(p - q) <= tol for p, q in zip(a, b))


def _axis_ticks(draws, vertical):
    """Tick positions on an axis path: short lines perpendicular to the axis line."""
    out = []
    for d in draws:
        if d.get("type") != "s":
            continue
        for it in d["items"]:
            if it[0] != "l":
                continue
            p, q = it[1], it[2]
            if vertical and abs(p.y - q.y) < 0.05 and 1.5 < abs(p.x - q.x) < 4:
                out.append(p.y)
            if not vertical and abs(p.x - q.x) < 0.05 and 1.5 < abs(p.y - q.y) < 4:
                out.append(p.x)
    return out


def read(fig):
    draws = fig.drawings()

    # y axis: tick lines on the left axis path, matched to the numeric labels left of it
    yticks = _axis_ticks(draws, vertical=True)
    axis_x = min(d["rect"].x1 for d in draws if d.get("type") == "s" and d["rect"].height > 60)
    marks = []
    for pos, v in fig.tick_marks("y"):
        words = [w for w in fig.words() if abs((w[1] + w[3]) / 2 - pos) < 0.01 and w[2] < axis_x]
        if not words:
            continue
        y = min(yticks, key=lambda t: abs(t - pos))
        assert abs(y - pos) < 2.0, (pos, v, y)
        marks.append((y, v))
    assert sorted(v for _, v in marks) == [0.0, 0.5, 1.0], marks
    cal = calibrate(marks)
    unc = VECTOR_UNCERTAINTY_PT + abs(cal.residual / cal.slope)

    # x axis: the dose tick labelled 1.0 (labels sit below the axis, rotated)
    xticks = _axis_ticks(draws, vertical=False)
    base = max(yticks)
    dose_words = [w for w in fig.words() if w[1] > base and w[4] in ("0", "0.1", "1.0", "10.0")]
    assert len(dose_words) == 4, dose_words
    label = [w for w in dose_words if float(w[4]) == DOSE][0]
    xt = min(xticks, key=lambda t: abs(t - (label[0] + label[2]) / 2))
    assert abs(xt - (label[0] + label[2]) / 2) < 6, (xt, label)

    errs = [d["rect"] for d in draws if d.get("type") == "s" and len(d["items"]) == 4 and d["rect"].width < 2]
    out = {}
    for grp, side in (("control", -1), ("infarct", 1)):
        bars = [d["rect"] for d in draws if d.get("type") == "f" and _same(d.get("fill"), BAR_FILL[grp])
                and d["rect"].height > 5 and 0 < side * ((d["rect"].x0 + d["rect"].x1) / 2 - xt) < 8]
        assert len(bars) == 1, (grp, bars)
        r = bars[0]
        dots = [d["rect"] for d in draws if d.get("type") == "fs" and _same(d.get("fill"), DOT_FILL[grp])
                and d["rect"].width < 2 and r.x0 - 2 <= (d["rect"].x0 + d["rect"].x1) / 2 <= r.x1 + 2]
        pts = [point(cal, (q.y0 + q.y1) / 2, unc, ((q.x0 + q.x1) / 2, (q.y0 + q.y1) / 2))
               for q in sorted(dots, key=lambda q: (q.y0, q.x0))]
        eb = [e for e in errs if r.x0 <= (e.x0 + e.x1) / 2 <= r.x1]
        assert len(eb) == 1, (grp, eb)
        mean = point(cal, r.y0, unc, (r.x0, r.y0))
        top = point(cal, eb[0].y0, unc, (eb[0].x0, eb[0].y0))
        out[grp] = {"points": pts, "countable": True,
                    "bar": {"mean": [mean["value"], mean["lo"], mean["hi"]],
                            "error": [top["value"], top["lo"], top["hi"]]}}
    return {"groups": out}
