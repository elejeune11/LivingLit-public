"""Supplementary Fig. 5B: average force-frequency relationship, force normalised to 1 Hz (vector line plot of
means at 1, 1.5 and 2 Hz, with mean ± SEM error bars at 1.5 and 2 Hz; no individual points).

The y axis is grey: a drawing of short horizontal tick lines (about 3 pt) on the axis line, each matched to the
numeric label just left of it. The x axis has a grey drawing of short vertical category ticks at the slot edges;
each frequency label (1Hz, 1.5hz, 2Hz) sits under the middle of its slot. The means are the vertices of a single
black polyline (one vertex per slot). An error bar is a black drawing of a vertical stem (two segments meeting at
the mean) and two horizontal caps; the cap with the smaller page y is the upper end. The 1 Hz point is the
normalisation reference and has no error bar.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate

FREQ = {"1Hz!": "f1", "1.5hz!": "f15", "2Hz!": "f2"}
# one label per (item, group) the figure feeds
LABELS = {"f15.f15": "f15", "f15.f1": "f1", "f2.f2": "f2", "f2.f1": "f1"}


def _lines(d):
    return [(a, b) for i in d["items"] for a, b in [i[1:3]]] if all(i[0] == "l" for i in d["items"]) else []


def _black(c):
    return c is not None and max(c) < 0.05


def read(fig):
    draws = fig.drawings()
    words = fig.words()
    unc = VECTOR_UNCERTAINTY_PT

    # y axis: the drawing of >= 3 short horizontal tick lines sharing one x span
    ticks = [d for d in draws if len(_lines(d)) >= 3
             and all(abs(a.y - b.y) < 0.01 and 2 < abs(b.x - a.x) < 4 for a, b in _lines(d))]
    assert len(ticks) == 1, "y-axis ticks not found"
    ls = _lines(ticks[0])
    x0 = min(min(a.x, b.x) for a, b in ls)
    nums = [((w[1] + w[3]) / 2, _num(w[4])) for w in words if _isnum(w[4]) and 0 < x0 - w[2] < 6]
    marks = []
    for a, _b in ls:
        cands = [v for pos, v in nums if abs(pos - a.y) < 2]
        assert len(cands) == 1, "tick without a single label"
        marks.append((a.y, cands[0]))
    cal = calibrate(marks)

    # frequency of each slot from the label under it
    slots = {FREQ[w[4]]: (w[0] + w[2]) / 2 for w in words if w[4] in FREQ}
    assert len(slots) == 3, "frequency labels not found"

    # means: vertices of the one black stroked polyline
    poly = [d for d in draws if d.get("fill") is None and _black(d.get("color")) and len(_lines(d)) == 2
            and all(abs(a.y - b.y) > 0.5 for a, b in _lines(d))]
    assert len(poly) == 1, "mean polyline not found"
    (p0, p1), (_q, p2) = _lines(poly[0])
    vertices = [p0, p1, p2]

    # error bars: filled black drawings of vertical segments and two horizontal caps
    bars = []
    for d in draws:
        if not _black(d.get("fill")):
            continue
        segs = _lines(d)
        v = [(a, b) for a, b in segs if abs(a.x - b.x) < 0.05]
        h = [(a, b) for a, b in segs if abs(a.y - b.y) < 0.05]
        if v and len(h) == 2 and len(v) + len(h) == len(segs):
            bars.append((v[0][0].x, min(a.y for a, _ in h)))

    out = {}
    for f, sx in slots.items():
        vx = min(vertices, key=lambda p: abs(p.x - sx))
        assert abs(vx.x - sx) < 3, "no mean vertex under the slot label"
        lo, hi = cal.interval(vx.y, unc)
        g = {"points": [], "countable": False,
             "bar": {"mean": [cal.value(vx.y), lo - cal.residual, hi + cal.residual]}}
        near = [b for b in bars if abs(b[0] - vx.x) < 0.2]
        assert len(near) <= 1, "several error bars at one mean"
        if near:
            elo, ehi = cal.interval(near[0][1], unc)
            g["bar"]["error"] = [cal.value(near[0][1]), elo - cal.residual, ehi + cal.residual]
        out[f] = g
    assert "error" in out["f15"]["bar"] and "error" in out["f2"]["bar"] and "error" not in out["f1"]["bar"]
    return {"groups": {label: out[f] for label, f in LABELS.items()}}


def _isnum(t):
    try:
        _num(t)
        return True
    except ValueError:
        return False


def _num(t):
    return float(t.rstrip("!").replace("−", "-"))
