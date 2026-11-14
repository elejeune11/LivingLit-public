"""Fig. 4a-f (author manuscript, p. 23): heart failure modelling in color-coded EHM. The figure is one raster image
(1032 x 1440 px over 248 x 346 pt, ~300 dpi), rendered at 300 dpi. Panels read here:

  a  FOC/CSA (mN/mm², y) against calcium (mM, x): one marker per group mean at each calcium, error bars (SEM) and a
     fitted curve per series. Control circles, NE 0.001 squares, NE 0.01 up-triangles, NE 0.1 down-triangles, NE 1
     diamonds, ET-1 0.01 grey stars.
  b  inotropic response to isoprenaline, FOC (% change): open bars with an upward error bar.
  d  cardiomyocyte size (fold), y axis from 0.8: red bars with an upward error bar.
  e  cell number (x10^5): stacked bars, RFP+ CM (red, bottom) and GFP+ Fib (green, on top), each with an upward
     error bar ending in a cap.
  f  NT-proBNP (ng/ml/CM): open bars with an upward error bar (no ET-1 bar).

Bars (b, d, e, f) are found from their black outlines. Every bar is outlined, so its top is the centre of the
outline run; an error bar is a 2 px stem from the top of a bar to a cap ~22 px wide. Two probe columns 7 px left and
right of the bar centre cross both the outline and the cap (they miss the stem and the asterisks); two probe
columns 5 px inside the bar's edges cross only the outline. A run seen by both kinds of probe is an outline; a run
seen only by the inner probes is a cap, and it belongs to the outline below it. Positions are darkness-weighted
row centres (weight 128 - max(R, G, B), so red and green fills weigh nothing). Bars carry no single EHM, so every
group is bar only (mean and upper error end).

In e the green segment is the GFP+ fibroblast number, drawn on top of the CM bar: its value is the height of the
green segment (top of the stack minus top of the red bar), and its error end is that value plus the stack's error
bar (cap minus stack top). The upper end of the CM error bar is its cap.

Panel a: no single EHM is drawn and the markers' error bars interleave, so only marker centres (bar means, with
the calcium as x) are read. Markers are the components of the dark mask left after a morphological opening with a
disc of radius OPEN_R (curves, stems and single caps are thinner and vanish). A marker's calcium is its calibrated x
rounded to 0.2 mM. NE 1 diamonds lie under the grey ET-1 stars at every calcium (grey is not dark), so neither gives
a reading. The other four series never cross (Control highest, then NE 0.001, NE 0.01, NE 0.1), so a column with
exactly four components is assigned top to bottom in that order, and kept only if the shapes agree: the square
(second) has the largest area and both triangles (third, fourth) are smaller than the circle. Columns with any other
count (merged markers, stacked caps kept by the opening) give no reading. The mean is the centre of the opened
component's box; the opening cuts a triangle's apex, so triangles carry TRI_PX more uncertainty.
"""
import cv2
import numpy as np

from livinglit.figures.source import calibrate, point

DPI = 300
UNC_PX = 0.6                         # 0.6 px at 300 dpi
T = 128                              # a pixel is dark where max(R, G, B) < T
W_MIN = 20                           # a run counts if its darkest pixel is below T - W_MIN (thin caps reach ~75)

# Per panel: the search box in render px (left, top, right, bottom) holding both axes, the printed y tick labels
# bottom to top, and the groups left to right; bars are probed from bars_top (default: the box top) down.
PANELS = {
    "b": {"box": (630, 80, 1000, 310), "yticks": [0, 20, 40, 60, 80, 100],
          "groups": ["ctr", "ne0001", "ne001", "ne01", "ne1", "et1"]},
    "d": {"box": (100, 770, 460, 1020), "yticks": [0.8, 1.0, 1.2, 1.4],
          "groups": ["ctr", "ne0001", "ne001", "ne01", "ne1", "et1"]},
    "e": {"box": (630, 775, 1000, 1022), "yticks": [0, 1, 2, 3], "bars_top": 822,   # below the legend boxes
          "groups": ["ctr", "ne0001", "ne001", "ne01", "ne1", "et1"]},
    "f": {"box": (100, 1140, 470, 1385), "yticks": [0, 0.01, 0.02, 0.03, 0.04],
          "groups": ["ctr", "ne0001", "ne001", "ne01", "ne1"]},
}
A_BOX = (100, 70, 450, 312)
A_YTICKS = [0.0, 0.5, 1.0]
A_XTICKS = [0, 1, 2, 3, 4, 5]
A_SERIES = ["ctr", "ne0001", "ne001", "ne01"]   # top to bottom wherever they are separate
A_STEP, A_TOL = 0.2, 0.06
TRI_PX = 2.0                         # extra uncertainty (px) of an opened triangle's box centre
OPEN_R = 3
# the same bar under a further label, so that a group compared in two or three items feeds each
ALSO = {"d_ctr": ["d_ctr for F4d_ne1", "d_ctr for F4d_et1"], "e_cm_ctr": ["e_cm_ctr for F4e_cm_et1"]}
AXIS_MIN = 150                       # an axis is a dark line at least this long (px)
INNER, EDGE = 7, 5                   # probe offsets (px): from the bar centre; inside the bar edges
BAR_MIN_W = 30


def _runs(idx):
    idx = np.asarray(idx)
    return [r for r in np.split(idx, np.flatnonzero(np.diff(idx) > 1) + 1) if len(r)]


def _centre(w):
    """Weighted centres of the runs of a darkness profile (each run widened by one sample each side)."""
    out = []
    for r in _runs(np.flatnonzero(w > 0)):
        i = np.arange(max(r[0] - 1, 0), min(r[-1] + 2, len(w)))
        if w[i].max() >= W_MIN:
            out.append(float((i * w[i]).sum() / w[i].sum()))
    return out


def _axes(v, box):
    """Left column of the y axis and top row of the x axis inside a search box."""
    x0, y0, x1, y1 = box
    d = v[y0:y1, x0:x1] < T
    cols = [c for c in range(d.shape[1]) if max((len(r) for r in _runs(np.flatnonzero(d[:, c]))), default=0) >= AXIS_MIN]
    rows = [r for r in range(d.shape[0]) if max((len(q) for q in _runs(np.flatnonzero(d[r]))), default=0) >= AXIS_MIN]
    if not cols or not rows:
        raise ValueError(f"axes not found in {box}")
    return x0 + cols[0], y0 + rows[0]


def _yticks(v, ax, y0, y1, values):
    w = np.clip(T - v[y0:y1, ax - 7:ax - 1], 0, None).sum(axis=1)
    pos = [y0 + c for c in _centre(np.where(w > 0.4 * w.max(), w, 0))]
    if len(pos) != len(values):
        raise ValueError(f"found {len(pos)} y ticks, expected {len(values)}")
    return calibrate(list(zip(sorted(pos, reverse=True), values)))


def _probe(v, col, top, bottom):
    """Weighted row centres of dark runs in a 3 px column band, rows top..bottom."""
    w = np.clip(T - v[top:bottom, col - 1:col + 2], 0, None).mean(axis=1)
    return [top + c for c in _centre(w)]


def _match(a, b, tol=1.5):
    """Positions found in both lists (mean of each pair)."""
    out = []
    for p in a:
        q = [x for x in b if abs(x - p) <= tol]
        if q:
            out.append((p + q[0]) / 2)
    return out


def _bars(v, ay, x0, x1, top):
    """(left, right) outline columns of the bars, read along a row just above the x axis."""
    cols = _runs(np.flatnonzero(v[ay - 6, x0:x1] < T))
    edges = [x0 + float(r.mean()) for r in cols]
    bars, i = [], 0
    while i + 1 < len(edges):
        if edges[i + 1] - edges[i] >= BAR_MIN_W:
            bars.append((edges[i], edges[i + 1]))
            i += 2
        else:
            i += 1
    return bars


def _bar_levels(v, l, r, top, ay):
    """Outline rows (bottom to top) and the cap above each, for one bar column."""
    c = (l + r) / 2
    inner = [_probe(v, int(round(c + s * INNER)), top, ay - 3) for s in (-1, 1)]
    edge = [_probe(v, int(round(e)), top, ay - 3) for e in (l + EDGE, r - EDGE)]
    runs_in = _match(*inner)
    outlines = sorted(_match(*edge), reverse=True)
    caps = sorted([p for p in runs_in if all(abs(p - o) > 1.5 for o in outlines)], reverse=True)
    levels = []
    for i, o in enumerate(outlines):
        nxt = outlines[i + 1] if i + 1 < len(outlines) else -np.inf
        cap = [p for p in caps if nxt < p < o]
        if len(cap) > 1:
            raise ValueError(f"bar at {c:.0f}: {len(cap)} caps above one outline")
        levels.append((o, cap[0] if cap else None))
    return levels


def _triple(cal, pos, unc):
    p = point(cal, pos, unc, (0, 0))
    return [p["value"], p["lo"], p["hi"]]


def _panel_bars(v, key, spec):
    x0, y0, x1, y1 = spec["box"]
    ax, ay = _axes(v, spec["box"])
    cal = _yticks(v, ax, y0, ay + 6, spec["yticks"])
    unc = UNC_PX + cal.residual / abs(cal.slope)
    bars = _bars(v, ay, ax + 3, x1, y0)
    if len(bars) != len(spec["groups"]):
        raise ValueError(f"panel {key}: found {len(bars)} bars, expected {len(spec['groups'])}")
    out = {}
    for name, (l, r) in zip(spec["groups"], bars):
        levels = _bar_levels(v, l, r, spec.get("bars_top", y0), ay)
        want = 2 if key == "e" else 1
        if len(levels) != want:
            raise ValueError(f"panel {key} {name}: {len(levels)} outline levels, expected {want}")
        if key != "e":
            o, cap = levels[0]
            bar = {"mean": _triple(cal, o, unc)}
            if cap is not None:
                bar["error"] = _triple(cal, cap, unc)
            out[f"{key}_{name}"] = {"points": [], "countable": False, "bar": bar}
            continue
        (cm, cm_cap), (tot, tot_cap) = levels
        bar = {"mean": _triple(cal, cm, unc)}
        if cm_cap is not None:
            bar["error"] = _triple(cal, cm_cap, unc)
        out[f"e_cm_{name}"] = {"points": [], "countable": False, "bar": bar}
        # green segment: height = stack top - CM top; both ends carry the interval
        s = cal.slope
        fib = s * (tot - cm)
        d = abs(s) * 2 * unc
        bar = {"mean": [fib, fib - d, fib + d]}
        if tot_cap is not None:
            e = fib + s * (tot_cap - tot)
            bar["error"] = [e, e - d, e + d]
        out[f"e_fib_{name}"] = {"points": [], "countable": False, "bar": bar}
    return out


def _panel_a(v):
    x0, y0, x1, y1 = A_BOX
    ax, ay = _axes(v, A_BOX)
    caly = _yticks(v, ax, y0, ay, A_YTICKS)
    w = np.clip(T - v[ay + 2:ay + 8, x0:x1], 0, None).sum(axis=0)
    xs = [x0 + c for c in _centre(np.where(w > 0.4 * w.max(), w, 0))]
    if len(xs) != len(A_XTICKS):
        raise ValueError(f"panel a: found {len(xs)} x ticks")
    calx = calibrate(list(zip(xs, A_XTICKS)))
    unc = UNC_PX + caly.residual / abs(caly.slope)
    m = (v[y0:ay - 2, ax + 3:x1] < T).astype(np.uint8)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * OPEN_R + 1, 2 * OPEN_R + 1))
    op = cv2.morphologyEx(m, cv2.MORPH_OPEN, k)
    n, _, st, cen = cv2.connectedComponentsWithStats(op, connectivity=8)
    cols = {}
    for i in range(1, n):
        cx, cy = cen[i][0] + ax + 3, cen[i][1] + y0
        ca = calx.value(cx)
        step = round(round(ca / A_STEP) * A_STEP, 6)
        if abs(ca - step) > A_TOL or not 0 < step <= A_XTICKS[-2]:
            continue
        cols.setdefault(step, []).append((cy, st[i]))
    out = {}
    for ca, comps in sorted(cols.items()):
        if len(comps) != len(A_SERIES):
            continue
        comps.sort(key=lambda c: c[0])
        areas = [int(c[1][4]) for c in comps]
        if areas[1] != max(areas) or max(areas[2:]) >= areas[0]:
            continue
        for i, (name, (_, st)) in enumerate(zip(A_SERIES, comps)):
            cy = y0 + st[1] + (st[3] - 1) / 2
            u = unc + (TRI_PX if i >= 2 else 0)
            out[f"a_{name}_{ca:g}"] = {"points": [], "countable": False,
                                       "bar": {"mean": _triple(caly, cy, u), "x": ca}}
    return out


def read(fig):
    img, _ = fig.render(DPI)
    v = img.astype(int).max(axis=2)
    groups = {}
    groups.update(_panel_a(v))
    for key, spec in PANELS.items():
        groups.update(_panel_bars(v, key, spec))
    for label, more in ALSO.items():
        for m in more:
            groups[m] = groups[label]
    return {"groups": groups}
