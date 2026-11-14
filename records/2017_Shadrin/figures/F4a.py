"""Fig. 4a: expression of 10 maturation genes relative to adult left ventricle at d0, 1, 2 and 3 weeks (vector bar
chart on a log axis, mean + upper error bar, no individual points).

The chart is drawn as three sections (structural, E-C coupling, metabolic), each with its own x-axis line and
category ticks; only the left section has y ticks (0.0001-1.0000, one per decade). The y axis is calibrated on a
log scale from those tick rectangles, each matched to the nearest numeric label left of it. The middle and right
x-axis lines (where the bars start, at 0.0001) sit 0.40 pt below and 0.29 pt above the left one, so their bars'
intervals are widened by that offset in pt.

A gene's bars are the one-rectangle coloured drawings between the two category ticks around its italic label,
taken in x order as d0, 1wk, 2wk, 3wk (the legend's order). The script checks the fills against the legend: d0,
1wk and 3wk bars carry the legend fills; the 2wk bars of MYL2 and MYOM2 are a different blue from the legend's
2wk square, so the 2wk fill is only checked to be none of the other three. An error bar is a black drawing of a
thin stem (width < 1 pt) and a short cap (height < 1 pt, width 2-6 pt) centred on the stem; the cap's centre is the
upper end. Two error bars (MYOM2 d0, CASQ2 3wk) have stems shorter than the cap is thick, so stem height is not tested.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate

GENES = ["TNNI3", "MYL2", "MYOM2", "MYOM3", "CASQ2", "S100A1", "PLN", "COX6A2", "CKMT2", "CKM"]
LEGEND = {"d0": "d0", "1wk": "w1", "2wk": "w2", "3wk": "w3"}
ORDER = ["d0", "w1", "w2", "w3"]


def _black(d):
    return d.get("fill") is not None and max(d["fill"]) < 0.05


def _rect_fill(d):
    f = d.get("fill")
    return f is not None and len(d["items"]) == 1 and d["items"][0][0] == "re" and max(f) >= 0.05


def _same(a, b):
    return max(abs(x - y) for x, y in zip(a, b)) < 0.01


def _cap(d):
    """The cap rectangle of a stem + cap error bar drawing, or None."""
    if not (_black(d) and len(d["items"]) == 2 and all(i[0] == "re" for i in d["items"])):
        return None
    a, b = (i[1] for i in d["items"])
    stem, cap = (a, b) if a.width < b.width else (b, a)
    if stem.width < 1 and 2 < cap.width < 6 and cap.height < 1 \
            and abs((stem.x0 + stem.x1) / 2 - (cap.x0 + cap.x1) / 2) < 0.2:
        return cap
    return None


def read(fig):
    draws = fig.drawings()
    words = fig.words()
    # y axis: the black drawing of >= 3 short horizontal tick rectangles in one column (the LV line's dashes are not)
    cal = None
    for d in draws:
        if not _black(d):
            continue
        ticks = [i[1] for i in d["items"] if i[0] == "re" and 2.5 < i[1].width < 4 and i[1].height < 1]
        if len(ticks) >= 3 and len(ticks) == len(d["items"]) and max(r.x0 for r in ticks) - min(r.x0 for r in ticks) < 0.1:
            x0 = min(r.x0 for r in ticks)
            nums = [m for m in fig.tick_marks("y", near=x0 - 18, tol=14) if m[1] > 0]
            marks = []
            for r in ticks:
                y = (r.y0 + r.y1) / 2
                pos, v = min(nums, key=lambda m: abs(m[0] - y))
                if abs(pos - y) < 2:
                    marks.append((y, v))
            assert len(marks) == len(ticks), "a y tick without a label"
            cal = calibrate(marks, log=True)
            y_left = max(r.y0 + r.y1 for r in ticks) / 2  # lowest tick (0.0001), where the left section's bars start
    # sections: each x-axis line (a long thin black rectangle) and its category ticks (short vertical rectangles)
    sections = []
    for d in draws:
        if not _black(d):
            continue
        cats = [i[1] for i in d["items"] if i[0] == "re" and i[1].width < 1 and 2.5 < i[1].height < 4]
        if len(cats) >= 2 and len(cats) == len(d["items"]):
            top = min(r.y0 for r in cats)
            line = [e for e in draws if _black(e) and len(e["items"]) == 1 and e["rect"].width > 50
                    and e["rect"].height < 1 and abs((e["rect"].y0 + e["rect"].y1) / 2 - top) < 0.1]
            assert len(line) == 1, "x-axis line not found"
            sections.append((sorted((r.x0 + r.x1) / 2 for r in cats), top))
    legend = {}
    for d in draws:
        r = d["rect"]
        if _rect_fill(d) and r.width < 6 and r.height < 6:
            yc = (r.y0 + r.y1) / 2
            for x0, y0, x1, y1, t in words:
                if t in LEGEND and 0 < x0 - r.x1 < 5 and abs((y0 + y1) / 2 - yc) < 2:
                    legend[LEGEND[t]] = d["fill"]
    assert set(legend) == set(ORDER), "legend not found"
    bars = [d for d in draws if _rect_fill(d) and d["rect"].height > 7]
    caps = [c for c in (_cap(d) for d in draws) if c is not None]
    out = {}
    for gene in GENES:
        (wx0, _, wx1, _, _), = [w for w in words if w[4] == gene]
        wc = (wx0 + wx1) / 2
        (edges, base), = [(s, b) for s, b in sections if s[0] < wc < s[-1]]
        lo_x = max(e for e in edges if e < wc)
        hi_x = min(e for e in edges if e > wc)
        mine = sorted((d for d in bars if lo_x < (d["rect"].x0 + d["rect"].x1) / 2 < hi_x),
                      key=lambda d: d["rect"].x0)
        assert len(mine) == 4, f"{gene}: {len(mine)} bars"
        unc = VECTOR_UNCERTAINTY_PT + abs(base - y_left)
        for g, d in zip(ORDER, mine):
            f = d["fill"]
            if g == "w2":
                assert not any(_same(f, legend[o]) for o in ("d0", "w1", "w3")), f"{gene} 2wk fill"
            else:
                assert _same(f, legend[g]), f"{gene} {g} fill differs from legend"
            r = d["rect"]
            assert abs(r.y1 - base) < 0.1, f"{gene} {g}: bar does not start on its axis line"
            xc = (r.x0 + r.x1) / 2
            cap = min(caps, key=lambda c: abs((c.x0 + c.x1) / 2 - xc))
            assert abs((cap.x0 + cap.x1) / 2 - xc) < 1, "error bar not centred on its bar"
            top, ce = r.y0, (cap.y0 + cap.y1) / 2
            k = 10 ** cal.residual  # calibration misfit, in decades on this log axis
            mlo, mhi = cal.interval(top, unc)
            elo, ehi = cal.interval(ce, unc)
            out[f"{gene}.{g}"] = {"points": [], "countable": False,
                                  "bar": {"mean": [cal.value(top), mlo / k, mhi * k],
                                          "error": [cal.value(ce), elo / k, ehi * k]}}
    return {"groups": out}
