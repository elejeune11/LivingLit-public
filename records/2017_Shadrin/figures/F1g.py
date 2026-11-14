"""Fig. 1g: % Ki67+ CMs at 1, 2 and 3 weeks (vector bar chart, mean + upper SEM bar, no individual points).

Bars are single filled rectangles (non-black fill); each error bar is a black two-rectangle shape (stem + cap)
centred on its bar. The y axis is calibrated from the left tick marks (short horizontal rectangles left of the
axis line) matched to the nearest numeric tick label. The x tick labels (1wk/2wk/3wk) name the bars.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate

WEEK = {"1wk": "w1", "2wk": "w2", "3wk": "w3"}
# one label per (comparison item, group) the figure feeds
LABELS = {"w2_vs_w1.w2": "w2", "w2_vs_w1.w1": "w1", "w3_vs_w2.w3": "w3", "w3_vs_w2.w2": "w2",
          "w3_vs_w1.w3": "w3", "w3_vs_w1.w1": "w1"}


def _black(d):
    return d.get("fill") is not None and max(d["fill"]) < 0.05


def read(fig):
    words = fig.words()
    draws = fig.drawings()
    # y-axis ticks: short black rectangles (width ~3 pt, height < 1 pt) left of the axis line
    ticks = []
    for d in draws:
        if not _black(d):
            continue
        for it in d["items"]:
            if it[0] == "re":
                r = it[1]
                if 2.5 < r.width < 4 and r.height < 1:
                    ticks.append(((r.y0 + r.y1) / 2, r.x1))
    nums = fig.tick_marks("y")
    marks = []
    for y, _ in ticks:
        pos, v = min(nums, key=lambda m: abs(m[0] - y))
        if abs(pos - y) < 2:
            marks.append((y, v))
    cal = calibrate(marks)
    unc = VECTOR_UNCERTAINTY_PT
    # bars: one-rectangle drawings with a coloured (non-black, non-white) fill
    bars = [d["rect"] for d in draws if d.get("fill") is not None and len(d["items"]) == 1 and d["items"][0][0] == "re"
            and 0.05 < min(d["fill"]) and min(d["fill"]) < 0.95 and d["rect"].height > 5]
    # error bars: black shapes of two rectangles (stem, cap) above a bar
    caps = []
    for d in draws:
        if _black(d) and len(d["items"]) == 2 and all(i[0] == "re" for i in d["items"]):
            cap = min((i[1] for i in d["items"]), key=lambda r: r.y0)
            caps.append(cap)
    weeks = {}
    for x0, y0, x1, y1, t in words:
        if t in WEEK:
            xc = (x0 + x1) / 2
            bar = min(bars, key=lambda r: abs((r.x0 + r.x1) / 2 - xc))
            cap = min(caps, key=lambda r: abs((r.x0 + r.x1) / 2 - xc))
            top = bar.y0
            ce = (cap.y0 + cap.y1) / 2
            m = cal.value(top)
            e = cal.value(ce)
            mlo, mhi = cal.interval(top, unc)
            elo, ehi = cal.interval(ce, unc)
            weeks[WEEK[t]] = {"points": [], "countable": False,
                              "bar": {"mean": [m, mlo - cal.residual, mhi + cal.residual],
                                      "error": [e, elo - cal.residual, ehi + cal.residual]}}
    return {"groups": {label: weeks[w] for label, w in LABELS.items()}}
