"""Fig. 1i: % MLC2v and % MLC2a+2v hiPSC-CMs at 1, 2 and 3 weeks (vector grouped bar chart, mean + upper SEM bar,
no individual points).

Each week has two adjacent bars, one per series; a bar is a one-rectangle fill whose bottom sits on the x axis
line, and its colour names the series through the legend (a small square of the same fill left of the series
word). Each error bar is a black two-rectangle shape (stem + cap) centred on its bar; its value is the cap centre.
The y axis is calibrated from the left tick marks (short horizontal rectangles left of the axis line) matched to
the nearest tick label as printed ("0%", "33%", "67%", "100%"); the rounded 33/67 labels enter the calibration
misfit. The x tick labels (1wk/2wk/3wk) name the weeks.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate

WEEK = {"1wk": "w1", "2wk": "w2", "3wk": "w3"}
SERIES = {"MLC2v": "mlc2v", "MLC2a+2v": "mlc2a2v"}
# one label per (comparison item, group) the figure feeds
LABELS = {f"{s}_{a}_vs_w1.{g}": (s, g) for s in ("mlc2v", "mlc2a2v") for a in ("w2", "w3") for g in (a, "w1")}


def _black(d):
    return d.get("fill") is not None and max(d["fill"]) < 0.05


def _rects(d):
    return [it[1] for it in d["items"] if it[0] == "re"]


def _same(f, g, tol=0.05):
    return max(abs(a - b) for a, b in zip(f, g)) < tol


def read(fig):
    words = fig.words()
    draws = fig.drawings()
    # y-axis ticks: short black rectangles (width ~3 pt, height < 1 pt) left of the axis line
    ticks = [((r.y0 + r.y1) / 2, r.x1) for d in draws if _black(d) for r in _rects(d)
             if 2.5 < r.width < 4 and r.height < 1]
    labels = []
    for x0, y0, x1, y1, t in words:
        if t.endswith("%"):
            try:
                labels.append(((y0 + y1) / 2, float(t[:-1])))
            except ValueError:
                pass
    marks = []
    for y, _ in ticks:
        pos, v = min(labels, key=lambda m: abs(m[0] - y))
        if abs(pos - y) < 2:
            marks.append((y, v))
    cal = calibrate(marks)
    unc = VECTOR_UNCERTAINTY_PT
    # x axis: the long thin black rectangle; its centre line is the bar base
    axis = max((r for d in draws if _black(d) for r in _rects(d) if r.height < 1), key=lambda r: r.width)
    base = (axis.y0 + axis.y1) / 2
    fills = [d for d in draws if d.get("fill") is not None and not _black(d) and len(d["items"]) == 1
             and d["items"][0][0] == "re"]
    bars = [d for d in fills if abs(d["rect"].y1 - base) < 0.5]
    # legend: a filled square left of each series word
    colour = {}
    for x0, y0, x1, y1, t in words:
        if t in SERIES:
            sq = min((d for d in fills if d not in bars),
                     key=lambda d: abs((d["rect"].y0 + d["rect"].y1) / 2 - (y0 + y1) / 2) + abs(d["rect"].x1 - x0))
            colour[SERIES[t]] = sq["fill"]
    # error bars: black shapes of two rectangles (stem, cap) above a bar
    caps = [min(_rects(d), key=lambda r: r.y0) for d in draws
            if _black(d) and len(d["items"]) == 2 and all(i[0] == "re" for i in d["items"])]
    out = {}
    for x0, y0, x1, y1, t in words:
        if t not in WEEK:
            continue
        xc = (x0 + x1) / 2
        for s, f in colour.items():
            bar = min((d["rect"] for d in bars if _same(d["fill"], f)), key=lambda r: abs((r.x0 + r.x1) / 2 - xc))
            bx = (bar.x0 + bar.x1) / 2
            cap = min(caps, key=lambda r: abs((r.x0 + r.x1) / 2 - bx))
            top, ce = bar.y0, (cap.y0 + cap.y1) / 2
            mlo, mhi = cal.interval(top, unc)
            elo, ehi = cal.interval(ce, unc)
            out[(s, WEEK[t])] = {"points": [], "countable": False,
                                 "bar": {"mean": [cal.value(top), mlo - cal.residual, mhi + cal.residual],
                                         "error": [cal.value(ce), elo - cal.residual, ehi + cal.residual]}}
    return {"groups": {label: out[key] for label, key in LABELS.items()}}
