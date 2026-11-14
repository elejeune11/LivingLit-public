"""Supplementary Fig. 14B: JPH2 and Cav3 protein relative to GAPDH in input cells (d0) and 3wk-old cardiopatches
(vector grouped bar chart, mean + upper SEM bar, no individual points).

The y axis is a grey drawing of short horizontal tick lines (about 3.2 pt long), each matched to the numeric label
just left of it (labels end in "!" in this PDF's text layer, so they are parsed here). Category slots are the short
vertical grey ticks under the x-axis line, named by the category words (JPH2, Cav3) centred in each slot. The d0 bars
and the d0 legend square are drawn as unfilled black outlines, the patch bars and square as blue fills, so a bar's
group is the legend square with the same fill (or likewise unfilled) followed by its d0/Patch word. Bars are
the rectangles standing on the x-axis line; legend squares are not. An error bar is a filled drawing of a vertical
stem rising from the bar top and a horizontal cap at the upper end.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate

GROUP = {"d0": "d0", "Patch": "patch"}
CATEGORIES = ("JPH2", "Cav3")
LABELS = {f"{c}.{g}": (c, g) for c in CATEGORIES for g in ("patch", "d0")}


def _lines(d):
    its = d["items"]
    return list(its) if its and all(i[0] == "l" for i in its) else []


def _rects(draws):
    """Every rectangle drawn, merged by position: (rect, style), where style is its fill colour, or "outline" when
    the rectangle is only stroked (filled rectangles are drawn twice, fill then outline)."""
    seen = {}
    for d in draws:
        if not (d["items"] and all(i[0] == "re" for i in d["items"])):
            continue
        if d.get("fill") == (1.0, 1.0, 1.0):  # page background
            continue
        for i in d["items"]:
            r = i[1]
            k = tuple(round(v, 1) for v in (r.x0, r.y0, r.x1, r.y1))
            r0, fill = seen.get(k, (r, None))
            if d.get("fill") is not None:
                assert fill is None or fill == d["fill"], "rectangle filled twice in different colours"
                fill = d["fill"]
            seen[k] = (r0, fill)
    return [(r, "outline" if f is None else tuple(round(c, 3) for c in f)) for r, f in seen.values()]


def _word(t):
    return t.rstrip("!")


def _num(t):
    return float(_word(t).replace("−", "-"))


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

    # category slots: short vertical ticks hanging below the x-axis line, named by the word centred in each
    slots = [d for d in draws if len(_lines(d)) >= 2
             and all(abs(a.x - b.x) < 0.01 and 2 < abs(b.y - a.y) < 6 and min(a.y, b.y) >= base_y - 0.1
                     for _, a, b in _lines(d))]
    assert len(slots) == 1, "category ticks not found"
    edges = sorted(a.x for _, a, _b in _lines(slots[0]))
    assert len(edges) == len(CATEGORIES) + 1, "category count differs from the printed labels"
    names = []
    for k in range(len(edges) - 1):
        ws = [_word(w[4]) for w in words if w[1] > base_y and edges[k] < (w[0] + w[2]) / 2 < edges[k + 1]
              and _word(w[4]) in CATEGORIES]
        assert len(ws) == 1, "category slot without a single name"
        names.append(ws[0])

    # legend: small squares (filled or outline-only) each followed by a group word on its right
    rects = _rects(draws)
    legend = {}
    for r, style in rects:
        if not (r.width < 9 and r.height < 9 and abs(r.y1 - base_y) > 0.2):
            continue
        yc = (r.y0 + r.y1) / 2
        for wx0, wy0, wx1, wy1, t in words:
            if _word(t) in GROUP and 0 < wx0 - r.x1 < 8 and abs((wy0 + wy1) / 2 - yc) < 3:
                legend.setdefault(style, set()).add(GROUP[_word(t)])
    assert sorted(g for s in legend.values() for g in s) == ["d0", "patch"], "legend not found"
    assert all(len(s) == 1 for s in legend.values()), "legend style shared by two groups"
    legend = {k: next(iter(s)) for k, s in legend.items()}

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
    for r, style in rects:
        if abs(r.y1 - base_y) > 0.2 or r.x0 < xaxis:  # legend square, not a bar standing on the axis
            continue
        assert style in legend, "bar style not in the legend"
        xc = (r.x0 + r.x1) / 2
        slot = [k for k in range(len(names)) if edges[k] < xc < edges[k + 1]]
        assert len(slot) == 1, "bar outside the category slots"
        sx, sbottom, cap = min(stems, key=lambda s: abs(s[0] - xc))
        assert abs(sx - xc) < 1 and abs(sbottom - r.y0) < 0.2, "error bar not on its bar"
        key = (names[slot[0]], legend[style])
        assert key not in out, "two bars of one group in one slot"
        out[key] = (r.y0, cap)

    groups = {}
    for label, key in LABELS.items():
        top, cap = out[key]
        mlo, mhi = cal.interval(top, unc)
        elo, ehi = cal.interval(cap, unc)
        groups[label] = {"points": [], "countable": False,
                         "bar": {"mean": [cal.value(top), mlo - cal.residual, mhi + cal.residual],
                                 "error": [cal.value(cap), elo - cal.residual, ehi + cal.residual]}}
    return {"groups": groups}
