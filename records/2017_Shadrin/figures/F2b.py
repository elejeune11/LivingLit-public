"""Fig. 2b: maximum active force (left) and specific force (right) at 1, 2 and 3 weeks (vector bar charts,
mean + upper SEM bar, no individual points).

Two sub-panels share one crop; each has its own y axis (a black drawing of short tick rectangles left of the
axis line). Tick rectangles are matched to the nearest numeric label just left of them. Bars are one-rectangle
drawings with a coloured fill; the week of a bar is the legend square of the same fill (legend squares are the
small coloured rectangles next to the 1wk/2wk/3wk words). Each error bar is a black stem + cap shape centred on
its bar; the cap's centre is the upper end. A bar belongs to the nearest axis to its left.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate

WEEK = {"1wk": "w1", "2wk": "w2", "3wk": "w3"}
# one label per (comparison item, group) the figure feeds; the left axis is force, the right specific force
LABELS = {
    "force_w2_vs_w1.w2": (0, "w2"), "force_w2_vs_w1.w1": (0, "w1"),
    "force_w3_vs_w1.w3": (0, "w3"), "force_w3_vs_w1.w1": (0, "w1"),
    "specific_w2_vs_w1.w2": (1, "w2"), "specific_w2_vs_w1.w1": (1, "w1"),
    "specific_w3_vs_w1.w3": (1, "w3"), "specific_w3_vs_w1.w1": (1, "w1"),
}


def _black(d):
    return d.get("fill") is not None and max(d["fill"]) < 0.05


def _coloured(d):
    f = d.get("fill")
    return f is not None and len(d["items"]) == 1 and d["items"][0][0] == "re" and 0.05 < max(f) and min(f) < 0.95


def read(fig):
    draws = fig.drawings()
    words = fig.words()
    unc = VECTOR_UNCERTAINTY_PT
    # axes: black drawings made of ≥3 short tick rectangles (width ~3 pt, height < 1 pt)
    axes = []
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
            axes.append((d["rect"].x1, calibrate(marks)))
    axes.sort(key=lambda a: a[0])
    # legend: small coloured squares, each followed on the same line by a week word
    legend = {}
    for d in draws:
        r = d["rect"]
        if _coloured(d) and r.width < 7 and r.height < 7:
            yc = (r.y0 + r.y1) / 2
            for x0, y0, x1, y1, t in words:
                if t in WEEK and 0 < x0 - r.x1 < 8 and abs((y0 + y1) / 2 - yc) < 2:
                    legend[tuple(round(c, 3) for c in d["fill"])] = WEEK[t]
    caps = []
    for d in draws:
        if _black(d) and len(d["items"]) == 2 and all(i[0] == "re" for i in d["items"]):
            caps.append(min((i[1] for i in d["items"]), key=lambda r: r.y0))
    panels = [{} for _ in axes]
    for d in draws:
        r = d["rect"]
        if not (_coloured(d) and r.height > 7):
            continue
        week = legend[tuple(round(c, 3) for c in d["fill"])]
        k = max(i for i, (ax, _) in enumerate(axes) if ax < r.x0)
        cal = axes[k][1]
        xc = (r.x0 + r.x1) / 2
        cap = min(caps, key=lambda c: abs((c.x0 + c.x1) / 2 - xc))
        top, ce = r.y0, (cap.y0 + cap.y1) / 2
        mlo, mhi = cal.interval(top, unc)
        elo, ehi = cal.interval(ce, unc)
        panels[k][week] = {"points": [], "countable": False,
                           "bar": {"mean": [cal.value(top), mlo - cal.residual, mhi + cal.residual],
                                   "error": [cal.value(ce), elo - cal.residual, ehi + cal.residual]}}
    return {"groups": {label: panels[k][w] for label, (k, w) in LABELS.items()}}
