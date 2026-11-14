"""Supplementary Fig. 9B, C: relaxation time and twitch duration of 1MM and 0.5MM cardiopatches (vector bar
charts, mean + upper SEM bar, no individual points).

Only panels B and C are read: panel A's rise times are printed in the Results (98.0 ± 2.2 vs. 107.6 ± 2.4 ms).

Each panel has a grey y axis: a drawing of short horizontal tick lines (length about 3 pt) on the axis line, each
matched to the numeric label just left of it. The panel is named by its rotated y-axis title (the word left of
the tick labels). The panel's x extent is its x-axis baseline, a single horizontal grey line starting at the
axis. Bars are one-rectangle drawings with a coloured fill; the group of a bar is the legend square of the same
fill (small squares followed by the 1MM/0.5MM words). An error bar is a filled drawing of two lines, a vertical
stem rising from the bar top and a horizontal cap; the cap's height is the upper end.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate

GROUP = {"1MM": "mm1", "0.5MM": "mm05"}
PANEL = {"Relaxa4on,4me,(ms),": "relaxation", "Twitch,dura4on,(ms),": "duration"}
# one label per (item, group) the figure feeds
LABELS = {"relaxation.mm05": ("relaxation", "mm05"), "relaxation.mm1": ("relaxation", "mm1"),
          "duration.mm05": ("duration", "mm05"), "duration.mm1": ("duration", "mm1")}


def _lines(d):
    return [i for i in d["items"] if i[0] == "l"] if all(i[0] == "l" for i in d["items"]) else []


def _coloured(d):
    f = d.get("fill")
    return f is not None and len(d["items"]) == 1 and d["items"][0][0] == "re" and 0.05 < max(f) and min(f) < 0.95


def _key(fill):
    return tuple(round(c, 3) for c in fill)


def read(fig):
    draws = fig.drawings()
    words = fig.words()
    unc = VECTOR_UNCERTAINTY_PT

    # axes: tick drawings (>= 3 short horizontal lines sharing their x span)
    axes = []
    for d in draws:
        ls = _lines(d)
        if len(ls) >= 3 and all(abs(a.y - b.y) < 0.01 and 2 < abs(b.x - a.x) < 4 for _, a, b in ls):
            x0 = min(min(a.x, b.x) for _, a, b in ls)
            x1 = max(max(a.x, b.x) for _, a, b in ls)
            # tick labels end in "!" in this PDF's text layer, so they are parsed here rather than by tick_marks
            nums = [((w[1] + w[3]) / 2, _num(w[4])) for w in words if _isnum(w[4]) and 0 < x0 - w[2] < 6]
            marks = []
            for _, a, _b in ls:
                cands = [v for pos, v in nums if abs(pos - a.y) < 2]
                assert len(cands) == 1, "tick without a single label"
                marks.append((a.y, cands[0]))
            title = [w for w in words if w[4].endswith("(ms),") and 0 < x0 - w[2] < 30]
            assert len(title) == 1, "panel title not found"
            if title[0][4] not in PANEL:  # panel A (rise time), printed in the text
                continue
            axes.append({"panel": PANEL[title[0][4]], "x": x1, "cal": calibrate(marks)})
    for ax in axes:  # x extent from the baseline drawn from the axis
        base = [b for d in draws for _, a, b in _lines(d)
                if len(_lines(d)) == 1 and abs(a.y - b.y) < 0.01 and abs(a.x - ax["x"]) < 0.5 and b.x - a.x > 20]
        assert len(base) == 1, "x-axis baseline not found"
        ax["x1"] = base[0].x

    legend = {}
    for d in draws:
        r = d["rect"]
        if _coloured(d) and r.width < 7 and r.height < 7:
            yc = (r.y0 + r.y1) / 2
            for x0, y0, x1, y1, t in words:
                if t.rstrip("!") in GROUP and 0 < x0 - r.x1 < 8 and abs((y0 + y1) / 2 - yc) < 3:
                    legend[_key(d["fill"])] = GROUP[t.rstrip("!")]

    stems = []  # (x, bottom, cap y) of filled stem + cap drawings
    for d in draws:
        ls = _lines(d)
        if d.get("fill") is None or len(ls) != 2:
            continue
        v = [(a, b) for _, a, b in ls if abs(a.x - b.x) < 0.05]
        h = [(a, b) for _, a, b in ls if abs(a.y - b.y) < 0.05]
        if len(v) == 1 and len(h) == 1:
            (a, b), (c, e) = v[0], h[0]
            assert abs((c.x + e.x) / 2 - a.x) < 0.2 and abs(c.y - min(a.y, b.y)) < 0.05
            stems.append((a.x, max(a.y, b.y), c.y))

    bars = {}
    for ax in axes:
        cal = ax["cal"]
        for d in draws:
            r = d["rect"]
            if not (_coloured(d) and r.height > 7 and ax["x"] < r.x0 and r.x1 < ax["x1"]):
                continue
            group = legend[_key(d["fill"])]
            xc = (r.x0 + r.x1) / 2
            sx, sbottom, ce = min(stems, key=lambda s: abs(s[0] - xc))
            assert abs(sx - xc) < 1 and abs(sbottom - r.y0) < 0.2, "error bar not on its bar"
            top = r.y0
            mlo, mhi = cal.interval(top, unc)
            elo, ehi = cal.interval(ce, unc)
            bars[(ax["panel"], group)] = {
                "points": [], "countable": False,
                "bar": {"mean": [cal.value(top), mlo - cal.residual, mhi + cal.residual],
                        "error": [cal.value(ce), elo - cal.residual, ehi + cal.residual]}}
    return {"groups": {label: bars[key] for label, key in LABELS.items()}}


def _isnum(t):
    try:
        _num(t)
        return True
    except ValueError:
        return False


def _num(t):
    return float(t.rstrip("!").replace("−", "-"))
