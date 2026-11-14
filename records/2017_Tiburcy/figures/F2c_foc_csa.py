"""Fig. 2c (author manuscript, p. 20): FOC per cross sectional area (FOC/CSA, mN/mm², y) against calcium (mM, x) for
serum-free EHM from HES2 (left plot: Week 2 circles, Week 4 squares, Week 6 triangles) and hiPS-G1 (right plot: Week 2
circles, Week 4 squares, Week 8 triangles). Each marker is a group mean at one calcium concentration with a vertical
error bar (SEM, Methods), and a fitted curve runs through each series.

The panel is a raster image (300 dpi, rendered at 600 dpi). No single EHM is drawn, so every marker is returned as a
bar (mean and upper error end) under its own label <group>_<calcium>, with the calcium concentration as the bar's x.
Markers are the components left after a morphological opening with a disc (the curves, error bars and caps are
thinner than the disc and vanish; markers whose caps touch them keep the caps). A marker's calcium is its calibrated
x rounded to 0.2 mM (the concentrations are not printed; every marker lies within X_TOL of a step). Components off
the steps (legend symbols, asterisks) are ignored. Within one plot and one calcium the three series never cross
(Week 2 lowest, the latest week highest), so the components of a column are assigned bottom to top. A column of
fewer than three components holds merged markers; it is resolved only where the lone single marker is the bottom
circle or the top triangle, and merged components give no reading.

The mean is the midpoint of the two error-bar caps when both are clean (the bars are symmetric, mean +/- SEM): a cap
is a run of 2..CAP_RUN_MAX rows of near-constant width CAP_MIN..CAP_MAX px at the end of the bar (outside the marker,
or touching it). Otherwise it is the marker centre: the box centre of a circle or square (checked against the cap
midpoint wherever both exist), and for a triangle the box centre plus the offset measured on the triangles with both
caps (median; the spread is added to the interval), since the opening cuts the apex. A component of a full column
that is one marker with both caps fused to it (no bar leaves it, both end rows cap-wide) gives the midpoint of its
ends as the mean and no error end (the fused caps' thickness is not seen). The upper error end is the top
cap, or the bottom cap mirrored about the mean; a bar whose caps are both hidden or merged gives no error end.
"""
import cv2
import numpy as np

from livinglit.figures.source import calibrate, point

DPI = 600
UNC_PX = 0.6 * DPI / 300             # 0.6 px at 300 dpi, in px at DPI
Y_TICKS = [0, 2, 4, 6, 8]            # printed y tick labels, bottom to top (FOC/CSA (mN/mm²)), both plots
X_TICKS = [0, 1, 2, 3, 4]            # printed x tick labels, left to right (Calcium (mM)), both plots
SERIES = [("hes2_w2", "hes2_w4", "hes2_w6"),   # left plot, bottom to top at every calcium
          ("g1_w2", "g1_w4", "g1_w8")]         # right plot
AXIS_RUN_MIN = 600                   # a y axis is a vertical line at least this long (px)
XAXIS_RUN_MIN = 600                  # an x axis is a horizontal line at least this long (px)
OPEN_R = 5                           # opening disc radius (px); bars are ~6 px wide, caps ~5 px thick
X_STEP, X_TOL = 0.2, 0.03            # calcium (mM) step and tolerance
SINGLE_H, SINGLE_W = 28, 27          # a component no larger than this is one marker
TRI_AREA_MAX = 340                   # opened triangles 240-330 px², circles 340-430, squares >= 440
CIRCLE_H_MAX = 23
BAR_HALF = 1                         # half width of the bar probe (px)
WIN = 15                             # widths are measured within x +/- WIN
CAP_MIN, CAP_MAX = 12, 18            # cap width (px); markers are wider, bars narrower
CAP_FLAT = 3                         # a cap's width varies by at most this (a circle's or triangle's top grows)
CAP_RUN_MAX = 7
CENTRE_TOL = 2.0                     # cap midpoint and circle/square box centre agree within this (px)


def _runs(idx):
    idx = np.asarray(idx)
    return [r for r in np.split(idx, np.flatnonzero(np.diff(idx) > 1) + 1) if len(r)]


def _centres(profile, frac=0.5):
    return [float((r * profile[r]).sum() / profile[r].sum()) for r in _runs(np.flatnonzero(profile > frac * profile.max()))]


def _longest_run(v):
    best, cur = 0, 0
    for b in v:
        cur = cur + 1 if b else 0
        best = max(best, cur)
    return best


def _axes(m):
    """Per plot (left to right): x-axis column range, calx, caly."""
    cols = [c for c in range(m.shape[1]) if m[:, c].sum() >= AXIS_RUN_MIN and _longest_run(m[:, c]) >= AXIS_RUN_MIN]
    yaxes = [(r[0], r[-1]) for r in _runs(cols)]
    rows = [r for r in range(m.shape[0]) if _longest_run(m[r]) >= XAXIS_RUN_MIN]
    if len(yaxes) != 2 or not rows:
        raise ValueError(f"found {len(yaxes)} y axes and {len(rows)} x-axis rows")
    xr0, xr1 = rows[0], rows[-1]
    segs = _runs(np.flatnonzero(m[(xr0 + xr1) // 2]))
    segs = [(s[0], s[-1]) for s in segs if len(s) >= XAXIS_RUN_MIN]
    if len(segs) != 2:
        raise ValueError(f"found {len(segs)} x-axis segments")
    out = []
    for (a0, a1), (s0, s1) in zip(yaxes, segs):
        yt = _centres(m[:xr0, a0 - 7:a0 - 1].sum(1).astype(float))          # y tick stubs left of the axis
        xt = [t + s0 - 3 for t in _centres(m[xr1 + 3:xr1 + 12, s0 - 3:s1 + 4].sum(0).astype(float))]
        if len(yt) != len(Y_TICKS) or len(xt) != len(X_TICKS):
            raise ValueError(f"found {len(yt)} y and {len(xt)} x ticks")
        out.append(((s0, s1), calibrate(list(zip(sorted(xt), X_TICKS))),
                    calibrate(list(zip(sorted(yt, reverse=True), Y_TICKS)))))
    return out, xr0


def _width(m, y, x):
    """Length of the dark run through column x in row y, within x +/- WIN."""
    row = m[y, x - WIN:x + WIN + 1]
    if not row[WIN - BAR_HALF:WIN + BAR_HALF + 1].any():
        return 0
    c = WIN - BAR_HALF + int(np.flatnonzero(row[WIN - BAR_HALF:WIN + BAR_HALF + 1])[0])
    lo = hi = c
    while lo > 0 and row[lo - 1]:
        lo -= 1
    while hi < len(row) - 1 and row[hi + 1]:
        hi += 1
    return hi - lo + 1


def _cap(m, b, others, sgn):
    """Row of the cap ending the bar above (sgn=-1) or below (sgn=+1) the component, or None."""
    x = int(round(b["cx"]))
    y = b["top"] if sgn < 0 else b["bot"]
    while m[y + sgn, x - BAR_HALF:x + BAR_HALF + 1].any():
        y += sgn
        if any(o["top"] - 2 <= y <= o["bot"] + 2 for o in others):
            return None                              # the bar runs into the next marker: its end is not clean
    rows = list(range(y, y - sgn * (CAP_RUN_MAX + 3), -sgn))
    ws = [_width(m, r, x) for r in rows]
    if ws[0] < CAP_MIN:                              # one anti-aliased end row
        rows, ws = rows[1:], ws[1:]
    run = []
    for r, w in zip(rows, ws):
        if CAP_MIN <= w <= CAP_MAX:
            run.append((r, w))
        else:
            break
    if not 2 <= len(run) <= CAP_RUN_MAX or len(run) == len(rows):
        return None
    if max(w for _, w in run) - min(w for _, w in run) > CAP_FLAT:
        return None
    return (run[0][0] + run[-1][0]) / 2


def _fused_ends(m, b):
    """Midpoint of a component that is one marker with both caps fused to it: no bar leaves either end and both end
    rows are cap-wide (flat), so the ends are the outer edges of two equal caps. None otherwise."""
    x = int(round(b["cx"]))
    ends = []
    for y, sgn in ((b["top"], -1), (b["bot"], 1)):
        if m[y + sgn, x - BAR_HALF:x + BAR_HALF + 1].any():
            return None
        ws = [_width(m, y - sgn * i, x) for i in range(3)]
        if ws[0] < CAP_MIN:                          # one anti-aliased end row
            y, ws = y - sgn, ws[1:]
        if not all(CAP_MIN <= w <= CAP_MAX for w in ws[:2]):
            return None
        ends.append(y)
    return (ends[0] + ends[1]) / 2


def _triple(cal, pos, unc):
    p = point(cal, pos, unc, (0, 0))
    return [p["value"], p["lo"], p["hi"]]


def _components(m, ay):
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * OPEN_R + 1, 2 * OPEN_R + 1))
    op = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, k)
    op[ay - 2:] = 0
    n, lab, st, _ = cv2.connectedComponentsWithStats(op)
    return [{"cx": x + (w - 1) / 2, "cy": y + (h - 1) / 2, "top": int(y), "bot": int(y + h - 1), "w": int(w),
             "h": int(h), "area": int(a), "single": h <= SINGLE_H and w <= SINGLE_W}
            for x, y, w, h, a in st[1:]]


def _assign(col, names):
    """{series: component} for one column (components sorted bottom to top)."""
    if len(col) == len(names):
        return dict(zip(names, col))
    if len(col) == 2:
        bot, top = col
        if bot["single"] and bot["area"] >= TRI_AREA_MAX and bot["h"] <= CIRCLE_H_MAX and not top["single"]:
            return {names[0]: bot}
        if top["single"] and top["area"] < TRI_AREA_MAX and not bot["single"]:
            return {names[-1]: top}
    return {}


def read(fig):
    img, s = fig.render(DPI)
    grey = img.astype(float).mean(axis=2)
    m = grey < 128
    plots, ay = _axes(m)
    comps = _components(m, ay)
    found = []                                       # (series, calcium, component, plot index)
    for pi, ((s0, s1), calx, caly) in enumerate(plots):
        cols = {}
        for b in comps:
            if not s0 - 10 <= b["cx"] <= s1 + 10:
                continue
            v = calx.value(b["cx"])
            ca = round(round(v / X_STEP) * X_STEP, 6)
            if abs(v - ca) > X_TOL or not 0 < ca <= X_TICKS[-1]:
                continue                             # legend symbol, asterisk
            cols.setdefault(ca, []).append(b)
        for ca, col in sorted(cols.items()):
            col.sort(key=lambda b: -b["cy"])
            for name, b in _assign(col, SERIES[pi]).items():
                if b["single"] and (b["area"] < TRI_AREA_MAX) != (name == SERIES[pi][-1]):
                    raise ValueError(f"{name} at {ca} mM: marker shape does not match its series")
                others = [o for o in col if o is not b]
                found.append((name, ca, b, pi, _cap(m, b, others, -1), _cap(m, b, others, 1)))
    tri = [(u + lo) / 2 - b["cy"] for name, _, b, pi, u, lo in found
           if name == SERIES[pi][-1] and b["single"] and u is not None and lo is not None]
    if len(tri) < 3:
        raise ValueError("too few triangles with both caps to place the triangle centre")
    tri_off = float(np.median(tri))
    tri_unc = float(max(abs(t - tri_off) for t in tri))
    groups = {}
    for name, ca, b, pi, u, lo in found:
        caly = plots[pi][2]
        mis_y = caly.residual / abs(caly.slope)
        unc = UNC_PX + mis_y
        if u is not None and lo is not None:
            mean = (u + lo) / 2
            if b["single"] and name != SERIES[pi][-1] and abs(mean - b["cy"]) > CENTRE_TOL:
                raise ValueError(f"{name} at {ca} mM: cap midpoint {mean} and marker centre {b['cy']} disagree")
        elif b["single"]:
            mean = b["cy"]
            if name == SERIES[pi][-1]:
                mean += tri_off
                unc += tri_unc
        elif _fused_ends(m, b) is not None:          # one marker (full column) with both caps fused: mean only
            mean, u, lo = _fused_ends(m, b), None, None
        else:
            continue                                 # merged component without both caps: no reading
        key = f"{name}_{ca:g}"
        if key in groups:
            raise ValueError(f"two {name} markers at {ca} mM")
        bar = {"mean": _triple(caly, mean, unc), "x": ca}
        up = u if u is not None else (2 * mean - lo if lo is not None else None)
        if up is not None:
            bar["error"] = _triple(caly, up, unc)
        groups[key] = {"points": [], "countable": False, "bar": bar}
    return {"groups": groups}
