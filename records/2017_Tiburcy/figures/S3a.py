"""Suppl. Fig. 3a (supplement p. 44): normalized FOC (fold) at 2 mmol/L calcium of EHM made with rat collagen plus
Matrigel (n=12) or bovine collagen plus Matrigel (n=14). One open bar per group (a group mean) with one upward error
bar; no single EHM is drawn, so both groups are bar only (countable false).

The panel is vector. The y axis is a long vertical line with separate tick stubs, calibrated from the stubs matched in
order to the printed labels left of it (0, 0.5, 1.0, 1.5). Columns are named from the words under the x axis
('Rat', 'Bovine'). Each bar is one white-filled, stroked path; its top is the mean. Each error bar is a horizontal cap
and a separate vertical line from the cap down to the bar top; 'error' is the cap. The line's base is checked to lie
within 0.5 pt of its bar's top.
"""
from livinglit.figures.source import calibrate

UNC_PT = 0.5                                  # vector position uncertainty (pt)
TICKS = [0.0, 0.5, 1.0, 1.5]
COLUMNS = {"Rat": "rat", "Bovine": "bovine"}  # word under the x axis -> group
BASE_TOL = 0.5                                # pt: error line base to bar top


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
    cols = {COLUMNS[w[4]]: w for w in words if w[4] in COLUMNS and w[1] > ax_bot}
    if len(cols) != 2:
        raise ValueError(f"columns {cols}")
    bars = [d["rect"] for d in fig.drawings() if d.get("fill") == (1.0, 1.0, 1.0) and d["rect"].width > 15
            and abs(d["rect"].y1 - ax_bot) < 0.05]
    caps = [(d["rect"], d["rect"].y0) for d, it in lines if len(it) == 2 and abs(it[0][1].y - it[0][2].y) < 0.01]
    groups = {}
    for g, w in cols.items():
        rs = [r for r in bars if r.x0 < w[0] < r.x1 or r.x0 < w[2] < r.x1]
        if len(rs) != 1:
            raise ValueError(f"{g}: {len(rs)} bars")
        r = rs[0]
        top = r.y0
        v = [v for v in verts if r.x0 < v[0] < r.x1 and v[2] - v[1] < 100]
        c = [c for c in caps if c[0].x0 < (r.x0 + r.x1) / 2 < c[0].x1]
        if len(v) != 1 or len(c) != 1 or abs(v[0][2] - top) > BASE_TOL or abs(v[0][1] - c[0][1]) > 0.01:
            raise ValueError(f"{g}: error lines {v}, caps {c}, bar top {top}")
        mean = cal.value(top)
        unc = (UNC_PT + mis) * k
        err = cal.value(c[0][1])
        groups[g] = {"points": [], "countable": False,
                     "bar": {"mean": [mean, mean - unc, mean + unc], "error": [err, err - unc, err + unc]}}
    return {"groups": groups}
