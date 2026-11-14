"""Suppl. Fig. 3c (supplement p. 44): normalized FOC (fold) at 2 mmol/L calcium of EHM made with bovine collagen only,
plus fibronectin or plus laminin (n=4/group). One open bar per group (a group mean) with one upward error bar; no
single EHM is drawn, so every group is bar only (countable false).

The panel is vector. The y axis is a long vertical line with separate tick stubs, calibrated from the stubs matched in
order to the printed labels left of it (0, 0.5, 1.0, 1.5). Under the x axis 'Bovine collagen' heads a horizontal rule
spanning all three bars; below the rule '+ Fibronectin' and '+ Laminin' name the bar that contains the centre of their
second word. The one bar left without a sub-label (the leftmost) is bovine collagen only. Each bar is one white-filled,
stroked path; its top is the mean. Each error bar is a horizontal cap and a separate vertical line from the cap down to
the bar top; 'error' is the cap. The line's base is checked to lie within 0.5 pt of its bar's top.

Both items share the collagen bar, so labels are <item>/<group> and the collagen bar is repeated.
"""
from livinglit.figures.source import calibrate

UNC_PT = 0.5                                              # vector position uncertainty (pt)
TICKS = [0.0, 0.5, 1.0, 1.5]
SUBLABELS = {"Fibronectin": "fn", "Laminin": "lam"}       # word under the rule -> group
UNLABELLED = "coll"                                       # the bar with no sub-label
ITEMS = {"S3c_fn": ["fn", "coll"], "S3c_lam": ["lam", "coll"]}
BASE_TOL = 0.5                                            # pt: error line base to bar top


def _lines(fig):
    out = []
    for d in fig.drawings():
        it = d["items"]
        if d.get("fill") is None and all(i[0] == "l" for i in it):
            out.append((d, it))
    return out


def read(fig):
    lines = _lines(fig)
    verts = [(it[0][1].x, min(it[0][1].y, it[0][2].y), max(it[0][1].y, it[0][2].y)) for d, it in lines
             if len(it) == 1 and abs(it[0][1].x - it[0][2].x) < 0.01]
    axis = [v for v in verts if v[2] - v[1] > 100]
    if len(axis) != 1:
        raise ValueError(f"y axes {axis}")
    ax_x, ax_top, ax_bot = axis[0]
    stubs = sorted({round(it[0][1].y, 3) for d, it in lines if len(it) == 1 and abs(it[0][1].y - it[0][2].y) < 0.01
                    and 0 < abs(it[0][1].x - it[0][2].x) < 4 and min(it[0][1].x, it[0][2].x) < ax_x}, reverse=True)
    words = fig.words()
    printed = sorted(float(w[4]) for w in words if ax_x - 25 < w[2] < ax_x and w[4].replace(".", "").isdigit())
    if printed != TICKS or len(stubs) != len(TICKS):
        raise ValueError(f"tick labels {printed}, stubs {stubs}")
    cal = calibrate(list(zip(stubs, TICKS)))
    k = abs(cal.slope)
    mis = cal.residual / k                    # calibration misfit in pt
    bars = sorted((d["rect"] for d in fig.drawings() if d.get("fill") == (1.0, 1.0, 1.0) and d["rect"].width > 15
                   and abs(d["rect"].y1 - ax_bot) < 0.05), key=lambda r: r.x0)
    if len(bars) != 3:
        raise ValueError(f"{len(bars)} bars")
    named = {}
    for w in words:
        if w[4] in SUBLABELS and w[1] > ax_bot:
            xc = (w[0] + w[2]) / 2
            rs = [i for i, r in enumerate(bars) if r.x0 < xc < r.x1]
            if len(rs) != 1:
                raise ValueError(f"{w[4]}: bars {rs}")
            named[rs[0]] = SUBLABELS[w[4]]
    rest = [i for i in range(len(bars)) if i not in named]
    if len(named) != 2 or rest != [0]:
        raise ValueError(f"sub-labels {named}")
    named[0] = UNLABELLED
    caps = [(d["rect"], d["rect"].y0) for d, it in lines if len(it) == 2 and abs(it[0][1].y - it[0][2].y) < 0.01]
    read_bars = {}
    for i, g in named.items():
        r = bars[i]
        top = r.y0
        v = [v for v in verts if r.x0 < v[0] < r.x1 and v[2] - v[1] < 100]
        c = [c for c in caps if c[0].x0 < (r.x0 + r.x1) / 2 < c[0].x1]
        if len(v) != 1 or len(c) != 1 or abs(v[0][2] - top) > BASE_TOL or abs(v[0][1] - c[0][1]) > 0.01:
            raise ValueError(f"{g}: error lines {v}, caps {c}, bar top {top}")
        mean = cal.value(top)
        unc = (UNC_PT + mis) * k
        err = cal.value(c[0][1])
        read_bars[g] = {"mean": [mean, mean - unc, mean + unc], "error": [err, err - unc, err + unc]}
    groups = {}
    for item, gs in ITEMS.items():
        for g in gs:
            groups[f"{item}/{g}"] = {"points": [], "countable": False, "bar": read_bars[g]}
    return {"groups": groups}
