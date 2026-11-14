"""Fig. 4D (journal_version.pdf p. 8): normalized PRP per tissue, vector scatter with mean ± SD lines.

Tick labels are outlined glyphs (no text layer), so the y axis is calibrated from the six tick rects of the
axis drawing, ordered bottom to top as the printed labels 0, 1, 2, 3, 4, 5. Each marker is drawn twice (fill
and an outline path of ~3.15 pt); the outline paths are taken, and their bounding-box centres are the points.
Markers are assigned to the nearest x-axis tick (category). The mean is the widest short horizontal rect over
a category; the error ends are the two caps (narrower rects) above and below it.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

LABELS = ["Atrial UnST", "Atrial ST", "Ventricular UnST", "Ventricular ST"]
READ = {"Ventricular UnST", "Ventricular ST"}  # the groups an item of the record rests on
TICK_VALUES = [0, 1, 2, 3, 4, 5]


def _axes(fig):
    y_axis = x_axis = None
    for d in fig.drawings():
        if not d["items"] or any(it[0] != "re" for it in d["items"]):
            continue
        rects = [it[1] for it in d["items"]]
        if len(rects) == 7 and d["rect"].height > 50:
            y_axis = rects
        if len(rects) == 5 and d["rect"].width > 50:
            x_axis = rects
    spine = max(y_axis, key=lambda r: r.height)
    yticks = sorted(((r.y0 + r.y1) / 2 for r in y_axis if r is not spine), reverse=True)
    xspine = max(x_axis, key=lambda r: r.width)
    xticks = sorted((r.x0 + r.x1) / 2 for r in x_axis if r is not xspine)
    return yticks, xticks


def read(fig):
    yticks, xticks = _axes(fig)
    assert len(yticks) == len(TICK_VALUES) and len(xticks) == len(LABELS)
    cal = calibrate(list(zip(yticks, TICK_VALUES)))
    unc = VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)
    near = lambda x: min(range(len(xticks)), key=lambda i: abs(xticks[i] - x))

    pts = {lab: [] for lab in LABELS}
    means, caps = {lab: [] for lab in LABELS}, {lab: [] for lab in LABELS}
    for d in fig.drawings():
        r = d["rect"]
        if 2.8 < r.width < 3.6 and 2.8 < r.height < 3.6 and len(d["items"]) > 4:  # marker outline paths
            pts[LABELS[near((r.x0 + r.x1) / 2)]].append(((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2))
        elif len(d["items"]) == 1 and d["items"][0][0] == "re" and r.height < 1.2 and 6 < r.width < 16:
            lab = LABELS[near((r.x0 + r.x1) / 2)]
            (means if r.width > 10 else caps)[lab].append((r.y0 + r.y1) / 2)

    groups = {}
    for lab in LABELS:
        if lab not in READ:
            continue
        assert len(means[lab]) == 1 and len(caps[lab]) == 2, lab
        m = means[lab][0]
        upper = min(caps[lab])  # page y grows downward: the upper end has the smaller y
        groups[lab] = {
            "points": [point(cal, y, unc, (x, y)) for x, y in sorted(pts[lab], key=lambda p: p[1])],
            "countable": True,
            "bar": {"mean": [cal.value(m), *cal.interval(m, unc)],
                    "error": [cal.value(upper), *cal.interval(upper, unc)]},
        }
    return {"groups": groups}
