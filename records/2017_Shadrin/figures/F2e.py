"""Fig. 2e: average conduction velocity at 1, 2 and 3 weeks (vector bar chart, mean + upper SEM bar, no
individual points).

The y axis is a black drawing of short tick rectangles left of the axis line; each tick is matched to the
nearest numeric label just left of it. Bars are one-rectangle drawings with a coloured fill; the week of a bar
is the legend square of the same fill (small coloured squares followed by the 1wk/2wk/3wk words). An error bar
is a black drawing of exactly a thin stem (width < 1 pt) and a short cap (height < 1 pt, width < 6 pt) centred on
the stem; the cap's centre is the upper end. The x axis' two end ticks are also a two-rectangle drawing, and
the significance brackets are single rectangles, so the stem/cap shape test keeps them out.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate

WEEK = {"1wk": "w1", "2wk": "w2", "3wk": "w3"}
# one label per (comparison item, group) the figure feeds
LABELS = {
    "cv_w2_vs_w1.w2": "w2", "cv_w2_vs_w1.w1": "w1",
    "cv_w3_vs_w1.w3": "w3", "cv_w3_vs_w1.w1": "w1",
}


def _black(d):
    return d.get("fill") is not None and max(d["fill"]) < 0.05


def _coloured(d):
    f = d.get("fill")
    return f is not None and len(d["items"]) == 1 and d["items"][0][0] == "re" and 0.05 < max(f) and min(f) < 0.95


def _cap(d):
    """The cap rectangle of a stem + cap error bar drawing, or None."""
    if not (_black(d) and len(d["items"]) == 2 and all(i[0] == "re" for i in d["items"])):
        return None
    a, b = (i[1] for i in d["items"])
    stem, cap = (a, b) if a.width < b.width else (b, a)
    if stem.width < 1 and stem.height > cap.height and cap.height < 1 and cap.width < 6 \
            and abs((stem.x0 + stem.x1) / 2 - (cap.x0 + cap.x1) / 2) < 0.2:
        return cap
    return None


def read(fig):
    draws = fig.drawings()
    words = fig.words()
    unc = VECTOR_UNCERTAINTY_PT
    cal = None
    for d in draws:
        if not _black(d):
            continue
        ticks = [i[1] for i in d["items"] if i[0] == "re" and 2.5 < i[1].width < 4 and i[1].height < 1]
        if len(ticks) >= 3:
            x0 = min(r.x0 for r in ticks)
            nums = fig.tick_marks("y", near=x0 - 7, tol=5)
            marks = []
            for r in ticks:
                y = (r.y0 + r.y1) / 2
                pos, v = min(nums, key=lambda m: abs(m[0] - y))
                if abs(pos - y) < 2:
                    marks.append((y, v))
            cal = calibrate(marks)
    legend = {}
    for d in draws:
        r = d["rect"]
        if _coloured(d) and r.width < 7 and r.height < 7:
            yc = (r.y0 + r.y1) / 2
            for x0, y0, x1, y1, t in words:
                if t in WEEK and 0 < x0 - r.x1 < 8 and abs((y0 + y1) / 2 - yc) < 2:
                    legend[tuple(round(c, 3) for c in d["fill"])] = WEEK[t]
    caps = [c for c in (_cap(d) for d in draws) if c is not None]
    bars = {}
    for d in draws:
        r = d["rect"]
        if not (_coloured(d) and r.height > 7):
            continue
        week = legend[tuple(round(c, 3) for c in d["fill"])]
        xc = (r.x0 + r.x1) / 2
        cap = min(caps, key=lambda c: abs((c.x0 + c.x1) / 2 - xc))
        assert abs((cap.x0 + cap.x1) / 2 - xc) < 1, "error bar not centred on its bar"
        top, ce = r.y0, (cap.y0 + cap.y1) / 2
        mlo, mhi = cal.interval(top, unc)
        elo, ehi = cal.interval(ce, unc)
        bars[week] = {"points": [], "countable": False,
                      "bar": {"mean": [cal.value(top), mlo - cal.residual, mhi + cal.residual],
                              "error": [cal.value(ce), elo - cal.residual, ehi + cal.residual]}}
    return {"groups": {label: bars[w] for label, w in LABELS.items()}}
