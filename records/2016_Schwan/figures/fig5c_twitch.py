"""Fig. 5c: peak stress, time-to-peak (TTP) and RT50 per EHT, longitudinal vs transverse, with mean and SEM (vector).

Three stacked subpanels, each with its own y axis. Tick labels are outlined glyphs (no text layer), so each axis's three
tick lines are matched in order to the printed labels (Peak Stress 0, 1, 2; TTP 0.09, 0.12, 0.15; RT50 0.07, 0.09, 0.11).
Markers: Long. black filled circles, Trans. green filled squares (some drawn as a fill plus a separate stroke path; the
fill is used, centres deduplicated). Groups split by x at the gap between the two columns. Each group's mean is a
horizontal line about 37 pt long; its SEM is a path of two caps about 16-19 pt long, the higher cap the upper end.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

SPLIT_X = 500.5                 # between the Long. and Trans. columns
PLOT_X = (460.0, 546.0)         # inside the axes
PANELS = [("stress", [2.0, 1.0, 0.0]), ("ttp", [0.15, 0.12, 0.09]), ("rt50", [0.11, 0.09, 0.07])]  # top to bottom
FILLS = {"long": (0.0, 0.0, 0.0), "trans": (0.0, 0.753, 0.0)}


def _close(a, b, tol=0.02):
    return a is not None and all(abs(x - y) <= tol for x, y in zip(a, b))


def _hlines(d):
    return [(it[1].x, it[2].x, it[1].y) for it in d["items"] if it[0] == "l" and abs(it[1].y - it[2].y) < 0.01]


def read(fig):
    draws = fig.drawings()
    # y axes: stroked paths holding one long vertical spine and three short tick lines
    axes = []
    for d in draws:
        if d["type"] != "s":
            continue
        its = [it for it in d["items"] if it[0] == "l"]
        ticks = [it[1].y for it in its if abs(it[1].y - it[2].y) < 0.01 and abs(it[1].x - it[2].x) < 6]
        spine = [it for it in its if abs(it[1].x - it[2].x) < 0.01 and abs(it[1].y - it[2].y) > 60]
        if len(ticks) == 3 and len(spine) == 1:
            axes.append((min(ticks), max(ticks), sorted(ticks)))
    axes.sort()
    assert len(axes) == 3, axes

    groups = {}
    for (name, values), (top, bottom, ticks) in zip(PANELS, axes):
        cal = calibrate(list(zip(ticks, values)))
        unc = VECTOR_UNCERTAINTY_PT + abs(cal.residual / cal.slope) if cal.slope else VECTOR_UNCERTAINTY_PT

        def inside(cx, cy):
            return PLOT_X[0] <= cx < PLOT_X[1] and top - 2 <= cy <= bottom - 1

        means, caps = {}, {}
        for d in draws:
            if d["type"] != "s":
                continue
            for x0, x1, y in _hlines(d):
                cx, length = (x0 + x1) / 2, abs(x1 - x0)
                if not inside(cx, y):
                    continue
                side = "long" if cx < SPLIT_X else "trans"
                if 30 < length < 45:
                    means.setdefault(side, []).append((cx, y))
                elif 12 < length < 22:
                    caps.setdefault(side, []).append((cx, y))

        for side, rgb in FILLS.items():
            pts = set()
            for d in draws:
                r = d["rect"]
                cx, cy = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
                if not inside(cx, cy) or (cx < SPLIT_X) != (side == "long"):
                    continue
                if 2.5 < r.width < 4 and 2.5 < r.height < 4 and d.get("fill") is not None and _close(d["fill"], rgb):
                    pts.add((round(cy, 3), round(cx, 3)))
            assert len(means.get(side, [])) == 1 and len(caps.get(side, [])) == 2, (name, side, means, caps)
            mx, my = means[side][0]
            cx, up_y = min(caps[side], key=lambda c: c[1])
            m = point(cal, my, unc, (mx, my))
            e = point(cal, up_y, unc, (cx, up_y))
            groups[f"{name}_{side}"] = {
                "points": [point(cal, y, unc, (x, y)) for y, x in sorted(pts)],
                "countable": True,
                "bar": {"mean": [m["value"], m["lo"], m["hi"]], "error": [e["value"], e["lo"], e["hi"]]},
            }
    return {"groups": groups}
