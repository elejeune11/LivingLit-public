"""Fig. 3h: lactate-related gene expression as ratios of transcripts per million (RNA-seq, D10), two stacked bar
panels with individual samples as filled circles.

Vector panel. Top panel LDHA/LDHB (y ticks 0, 0.5, 1.0, 1.5), bottom panel SLC16A1/SLC16A3 (y ticks 0 to 2.5 in
steps of 0.5). In each, left bar Control (blue fill, dark blue dots), right bar Infarct (light orange fill, orange
dots); "Control" and "Infarct" are printed under the bars. Each bar's error bar is one stroked path of four lines
(two vertical halves and two caps); the upper cap is the error reading. The two panels are told apart by their own
axis paths (a vertical axis line with short tick lines on its left).
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

DOT = {"control": (0.0, 0.0, 0.75), "infarct": (1.0, 0.38, 0.0)}
PANELS = ("ldh", "slc16")  # top to bottom


def _near(c, rgb, tol=0.03):
    return c is not None and len(c) == 3 and max(abs(a - b) for a, b in zip(c, rgb)) <= tol


def _hline(it):
    return it[0] == "l" and abs(it[1].y - it[2].y) < 0.05


def _vline(it):
    return it[0] == "l" and abs(it[1].x - it[2].x) < 0.05


def read(fig):
    draws = fig.drawings()

    # axis paths: a long vertical line plus short tick lines on its left
    axes = []
    for d in draws:
        if d.get("type") != "s" or len(d["items"]) < 5:
            continue
        vert = [it for it in d["items"] if _vline(it) and abs(it[1].y - it[2].y) > 40]
        ticks = [it for it in d["items"] if _hline(it) and abs(it[1].x - it[2].x) < 4
                 and max(it[1].x, it[2].x) <= vert[0][1].x + 0.2] if vert else []
        if vert and len(ticks) >= 4:
            axes.append((d, vert[0][1].x, sorted(it[1].y for it in ticks)))
    axes.sort(key=lambda a: a[0]["rect"].y0)
    assert len(axes) == 2, len(axes)

    out = {}
    for name, (ax, axis_x, ticks) in zip(PANELS, axes):
        top, bottom = ax["rect"].y0, ax["rect"].y1
        labels = [(pos, v) for pos, v in fig.tick_marks("y", near=axis_x - 8, tol=6)
                  if top - 3 <= pos <= bottom + 3]
        assert len(labels) == len(ticks), (name, labels, ticks)
        marks = []
        for pos, v in labels:
            y = min(ticks, key=lambda t: abs(t - pos))
            assert abs(y - pos) < 2.0, (name, pos, v, y)
            marks.append((y, v))
        cal = calibrate(marks)
        unc = VECTOR_UNCERTAINTY_PT + abs(cal.residual / cal.slope)

        inside = [d for d in draws if d["rect"].y0 >= top - 4 and d["rect"].y1 <= bottom + 0.5
                  and d["rect"].x0 > axis_x]
        bars = sorted([d for d in inside if d.get("type") == "f" and d["rect"].height > 10
                       and 15 < d["rect"].width < 30], key=lambda d: d["rect"].x0)
        assert len(bars) == 2, (name, len(bars))
        errs = [d for d in inside if d.get("type") == "s" and len(d["items"]) == 4
                and all(it[0] == "l" for it in d["items"])
                and sum(_hline(it) and abs(it[1].x - it[2].x) > 4 for it in d["items"]) == 2]

        for group, b in zip(("control", "infarct"), bars):
            r = b["rect"]
            dots = [d["rect"] for d in inside if d.get("type") == "fs" and d["rect"].width < 3.5
                    and d["rect"].height < 3.5 and _near(d.get("fill"), DOT[group])]
            assert dots and all(r.x0 - 3 <= (q.x0 + q.x1) / 2 <= r.x1 + 3 for q in dots), (name, group)
            pts = [point(cal, (q.y0 + q.y1) / 2, unc, ((q.x0 + q.x1) / 2, (q.y0 + q.y1) / 2))
                   for q in sorted(dots, key=lambda q: (q.y0, q.x0))]
            eb = [d for d in errs if any(_vline(it) and r.x0 < it[1].x < r.x1 for it in d["items"])]
            assert len(eb) == 1, (name, group, len(eb))
            top_y = min(it[1].y for it in eb[0]["items"] if _hline(it) and abs(it[1].x - it[2].x) > 4)
            mean = point(cal, r.y0, unc, (r.x0, r.y0))
            upper = point(cal, top_y, unc, ((r.x0 + r.x1) / 2, top_y))
            out[f"{name}_{group}"] = {"points": pts, "countable": True,
                                      "bar": {"mean": [mean["value"], mean["lo"], mean["hi"]],
                                              "error": [upper["value"], upper["lo"], upper["hi"]]}}
    return {"groups": out}
