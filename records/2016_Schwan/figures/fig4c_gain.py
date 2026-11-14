"""Fig. 4c: length-tension (length-stress) gain per EHT at Day9, Day16 and Day23, with mean and SEM bars (vector).

Tick labels are outlined glyphs (no text layer), so the three y tick lines of the axis path are matched in order to
the printed labels 0, 3.25 and 6.5. Markers: Day9 blue filled circles, Day16 red filled squares, Day23 black filled
triangles (each drawn as a fill and a stroke path; the fill is used). Groups split by x between the category columns;
the legend (x > 510) is excluded. Each column's mean/SEM path is three horizontal lines: the longest is the mean,
the higher short cap is the upper end of the error bar.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

PLOT_X = (422.0, 510.0)          # inside the axes, left of the legend
COLUMNS = {"Day9": (422.0, 452.0), "Day16": (452.0, 484.0), "Day23": (484.0, 510.0)}
TICK_VALUES = [6.5, 3.25, 0.0]   # printed labels, top to bottom
FILLS = {"Day9": (0.0, 0.0, 1.0), "Day16": (1.0, 0.0, 0.0), "Day23": (0.0, 0.0, 0.0)}


def _close(a, b, tol=0.02):
    return a is not None and all(abs(x - y) <= tol for x, y in zip(a, b))


def read(fig):
    draws = fig.drawings()
    # axis: the stroked path holding the y-axis spine and its short tick lines
    axis = max((d for d in draws if d["type"] == "s"), key=lambda d: d["rect"].width * d["rect"].height)
    ticks = sorted(it[1].y for it in axis["items"]
                   if it[0] == "l" and abs(it[1].y - it[2].y) < 0.01 and abs(it[1].x - it[2].x) < 4)
    cal = calibrate(list(zip(ticks, TICK_VALUES)))
    unc = VECTOR_UNCERTAINTY_PT + abs(cal.residual / cal.slope) if cal.slope else VECTOR_UNCERTAINTY_PT

    groups = {}
    for label, (x0, x1) in COLUMNS.items():
        pts = []
        for d in draws:
            r = d["rect"]
            cx, cy = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
            if not (x0 <= cx < x1 and PLOT_X[0] <= cx < PLOT_X[1]):
                continue
            if 2.5 < r.width < 4 and 2.5 < r.height < 4 and d.get("fill") is not None and _close(d["fill"], FILLS[label]):
                pts.append((cy, cx))
        pts = sorted(set((round(y, 3), round(x, 3)) for y, x in pts))
        # mean/SEM path of this column
        bars = [d for d in draws if d["type"] == "s" and d is not axis and x0 <= (d["rect"].x0 + d["rect"].x1) / 2 < x1
                and d["rect"].width > 15 and d["rect"].height < 15]
        hl = [(abs(it[2].x - it[1].x), it[1].y) for it in bars[0]["items"] if it[0] == "l" and abs(it[1].y - it[2].y) < 0.01]
        mean_y = max(hl)[1]
        caps = [y for w, y in hl if y != mean_y]
        up_y = min(caps)
        m = point(cal, mean_y, unc, ((x0 + x1) / 2, mean_y))
        e = point(cal, up_y, unc, ((x0 + x1) / 2, up_y))
        groups[label] = {
            "points": [point(cal, y, unc, (x, y)) for y, x in pts],
            "countable": True,
            "bar": {"mean": [m["value"], m["lo"], m["hi"]], "error": [e["value"], e["lo"], e["hi"]]},
        }
    return {"groups": groups}
