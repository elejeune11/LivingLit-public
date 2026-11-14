"""Supplementary Fig. 12B: relative phosphorylation of Akt, mTOR and AMPK in 0.5MM vs 1MM cardiopatches, normalised
to 1MM (vector grouped bar chart, mean + upper SEM bar, no individual points).

The y axis is a grey drawing of short horizontal tick lines (about 3.9 pt long), each matched to the numeric label
just left of it (labels end in "!" in this PDF's text layer, so they are parsed here). Category slots are the short
vertical grey ticks under the x-axis line. Bars are filled rectangles, one drawing per legend colour holding one
rectangle per category; the group of a bar is the legend square of the same fill followed by the 1MM/0.5MM word.
An error bar is a filled drawing of a vertical stem rising from the bar top and a horizontal cap at the upper end.
The category names under the axis are glyph outlines, not text, so their printed left-to-right order is fixed here
and the slot count is asserted.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate

GROUP = {"1MM": "mm1", "0.5MM": "mm05"}
CATEGORIES = ["Akt", "mTOR", "AMPK"]  # printed order under the x axis (glyph outlines)
LABELS = {f"{c}.{g}": (c, g) for c in CATEGORIES for g in ("mm05", "mm1")}


def _lines(d):
    its = d["items"]
    return [i for i in its] if its and all(i[0] == "l" for i in its) else []


def _key(fill):
    return tuple(round(c, 3) for c in fill)


def _coloured(fill):
    return fill is not None and max(fill) > 0.05 and min(fill) < 0.95


def _num(t):
    return float(t.rstrip("!").replace("−", "-"))


def _isnum(t):
    try:
        _num(t)
        return True
    except ValueError:
        return False


def read(fig):
    draws = fig.drawings()
    words = fig.words()
    unc = VECTOR_UNCERTAINTY_PT

    # y axis: the drawing of >= 3 short horizontal tick lines
    ticks = [d for d in draws if len(_lines(d)) >= 3
             and all(abs(a.y - b.y) < 0.01 and 2 < abs(b.x - a.x) < 5 for _, a, b in _lines(d))]
    assert len(ticks) == 1, "y-axis ticks not found"
    ls = _lines(ticks[0])
    x0 = min(min(a.x, b.x) for _, a, b in ls)
    xaxis = max(max(a.x, b.x) for _, a, b in ls)
    nums = [((w[1] + w[3]) / 2, _num(w[4])) for w in words if _isnum(w[4]) and 0 < x0 - w[2] < 6]
    marks = []
    for _, a, _b in ls:
        cands = [v for pos, v in nums if abs(pos - a.y) < 2]
        assert len(cands) == 1, "tick without a single label"
        marks.append((a.y, cands[0]))
    cal = calibrate(marks)
    base_y = max(a.y for _, a, _b in ls)

    # category slots: short vertical ticks hanging below the x-axis line
    slots = [d for d in draws if len(_lines(d)) >= 2
             and all(abs(a.x - b.x) < 0.01 and 2 < abs(b.y - a.y) < 6 and min(a.y, b.y) >= base_y - 0.1
                     for _, a, b in _lines(d))]
    assert len(slots) == 1, "category ticks not found"
    edges = sorted(a.x for _, a, _b in _lines(slots[0]))
    assert len(edges) == len(CATEGORIES) + 1, "category count differs from the printed labels"

    legend = {}
    for d in draws:
        r, f = d["rect"], d.get("fill")
        if _coloured(f) and len(d["items"]) == 1 and d["items"][0][0] == "re" and r.width < 9 and r.height < 9:
            yc = (r.y0 + r.y1) / 2
            for wx0, wy0, wx1, wy1, t in words:
                if t.rstrip("!") in GROUP and 0 < wx0 - r.x1 < 8 and abs((wy0 + wy1) / 2 - yc) < 3:
                    legend[_key(f)] = GROUP[t.rstrip("!")]
    assert sorted(legend.values()) == ["mm05", "mm1"], "legend not found"

    stems = []  # (x, bottom, cap y) of filled stem + cap drawings
    for d in draws:
        ls2 = _lines(d)
        if d.get("fill") is None or len(ls2) != 2:
            continue
        v = [(a, b) for _, a, b in ls2 if abs(a.x - b.x) < 0.05]
        h = [(a, b) for _, a, b in ls2 if abs(a.y - b.y) < 0.05]
        if len(v) == 1 and len(h) == 1:
            (a, b), (c, e) = v[0], h[0]
            if abs(c.y - min(a.y, b.y)) < 0.05 and min(c.x, e.x) <= a.x <= max(c.x, e.x):
                stems.append((a.x, max(a.y, b.y), c.y))

    out = {}
    for d in draws:
        f = d.get("fill")
        if not (_coloured(f) and _key(f) in legend and all(i[0] == "re" for i in d["items"])):
            continue
        group = legend[_key(f)]
        for i in d["items"]:
            r = i[1]
            if r.height < 9 or r.x0 < xaxis:  # legend square
                continue
            xc = (r.x0 + r.x1) / 2
            slot = [k for k in range(len(CATEGORIES)) if edges[k] < xc < edges[k + 1]]
            assert len(slot) == 1, "bar outside the category slots"
            assert abs(r.y1 - base_y) < 0.1, "bar not on the baseline"
            sx, sbottom, cap = min(stems, key=lambda s: abs(s[0] - xc))
            assert abs(sx - xc) < 1 and abs(sbottom - r.y0) < 0.2, "error bar not on its bar"
            key = (CATEGORIES[slot[0]], group)
            assert key not in out, "two bars of one group in one slot"
            mlo, mhi = cal.interval(r.y0, unc)
            elo, ehi = cal.interval(cap, unc)
            out[key] = {"points": [], "countable": False,
                        "bar": {"mean": [cal.value(r.y0), mlo - cal.residual, mhi + cal.residual],
                                "error": [cal.value(cap), elo - cal.residual, ehi + cal.residual]}}
    return {"groups": {label: out[key] for label, key in LABELS.items()}}
