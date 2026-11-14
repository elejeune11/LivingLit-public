"""Suppl. Fig. 6 (supplement p. 49): two columns (HES2 left, hiPS-G1 right; the column headings) of three panels:
(a) output CM number (x10^5) and (b) CSA (mm²) as bars at Week 2/4/6 (HES2) or Week 2/4/8 (hiPS-G1), each with an
upper error bar; (c) FOC (mN, y) against calcium (mM, x), one series per week, each plot marker a group mean with a
symmetric vertical error bar and a fitted curve through each series. No single EHM is drawn, so every bar and every
curve marker is returned as a bar (mean and upper error end), with no points and no n.

The page is vector. Each panel has one y axis path (axis line plus tick stubs), calibrated from the stubs matched in
order to the printed numbers left of it; the panel is named by the y axis title word (CM, CSA, FOC) and its column by
the heading above it. Bars (a, b) are white-filled rectangles; the mean is the rectangle's top edge, and the error end
is the top of the T-shaped error path (stem plus cap) centred on the bar and standing on its top. The week of a bar
is the 'Week N' label below its centre.

In (c) the x axis path is calibrated likewise from the stubs below it and the numbers under them; x is the calibrated
marker centre rounded to 0.1 mM (the concentrations are not printed; every marker must lie within X_TOL of a step).
Markers are filled circles, squares and triangles of one size; the legend (marker left of each 'Week N' word, on its
line) gives each shape its week. The mean is the marker's bounding-box centre. Each error bar is drawn as two vertical
halves that meet at the marker centre; the upper half's top is 'error', and the halves are checked to be symmetric. A
marker with no halves meeting at its centre (bar hidden inside the marker) gives no error end.
"""
from livinglit.figures.source import calibrate, point

UNC_PT = 0.5
COLUMNS = {"HES2": "hes2", "hiPS-G1": "g1"}                    # column headings
PANELS = {"CM": "a", "CSA": "b", "FOC": "c"}                   # first word of each y axis title
Y_TICKS = {"a": [0, 1, 2, 3, 4, 5], "b": [0, 0.5, 1.0, 1.5], "c": [0, 1, 2, 3, 4]}
X_TICKS = [0, 1, 2, 3, 4]                                      # panel c, Calcium (mM)
WEEKS = {"hes2": [2, 4, 6], "g1": [2, 4, 8]}
ITEMS = {
    "a": {"hes2": ["S6a_hes2"], "g1": ["S6a_g1"]},
    "b": {"hes2": ["S6b_hes2_w4_hes2_w2", "S6b_hes2_w6_hes2_w4", "S6b_hes2_w6_hes2_w2"],
          "g1": ["S6b_g1_w4_g1_w2", "S6b_g1_w8_g1_w2"]},
    "c": {"hes2": ["S6c_hes2"], "g1": ["S6c_g1"]},
}
ITEM_GROUPS = {                                                # groups of each item, as the record lists them
    "S6a_hes2": ["hes2_w2", "hes2_w4", "hes2_w6"], "S6a_g1": ["g1_w2", "g1_w4", "g1_w8"],
    "S6b_hes2_w4_hes2_w2": ["hes2_w4", "hes2_w2"], "S6b_hes2_w6_hes2_w4": ["hes2_w6", "hes2_w4"],
    "S6b_hes2_w6_hes2_w2": ["hes2_w6", "hes2_w2"], "S6b_g1_w4_g1_w2": ["g1_w4", "g1_w2"],
    "S6b_g1_w8_g1_w2": ["g1_w8", "g1_w2"],
    "S6c_hes2": ["hes2_w2", "hes2_w4", "hes2_w6"], "S6c_g1": ["g1_w2", "g1_w4", "g1_w8"],
}
SHAPES = {"cccc": "circle", "re": "square", "llll": "square", "lll": "triangle"}
X_STEP, X_TOL = 0.1, 0.03
SAME = 0.1                                   # pt: centres and line ends that coincide
SYM = 0.1                                    # pt: upper and lower bar halves agree within this
TOUCH = 1.0                                  # pt: an error path stands on its bar top, centred on it, within this


def _kind(d):
    return "".join(i[0] for i in d["items"])


def _centre(r):
    return (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2


def _segs(d):
    return [(i[1].x, i[1].y, i[-1].x, i[-1].y) for i in d["items"] if i[0] == "l"]


def _axes(draws, vertical):
    """Axis paths (one line plus perpendicular stubs, nothing else): [(line position, sorted stub positions)]."""
    out = []
    for d in draws:
        segs, r = _segs(d), d["rect"]
        if len(segs) != len(d["items"]) or len(segs) < 4:
            continue
        if vertical and r.height > 100 and r.width < 6:
            stubs = sorted(s[1] for s in segs if abs(s[1] - s[3]) < 0.01)
            out.append((r.x1, stubs))
        elif not vertical and r.width > 150 and r.height < 6:
            stubs = sorted(s[0] for s in segs if abs(s[0] - s[2]) < 0.01)
            out.append((r.y0, stubs))
    return out


def _num(t):
    try:
        return float(t)
    except ValueError:
        return None


def _triple(cal, pos, unc):
    p = point(cal, pos, unc, (0, 0))
    return [p["value"], p["lo"], p["hi"]]


def _panel(words, heads, ax_x, stubs):
    """(panel letter, column) of a y axis: the title word left of it, the heading over its column."""
    top, bottom = min(stubs), max(stubs)
    title = [w for w in words if w[4] in PANELS and ax_x - 40 < w[2] < ax_x - 10 and top <= (w[1] + w[3]) / 2 <= bottom]
    if len(title) != 1:
        raise ValueError(f"y axis at x {ax_x:.1f}: title words {title}")
    col = min(heads, key=lambda h: abs((h[0] + h[2]) / 2 - (ax_x + 110)))
    return PANELS[title[0][4]], COLUMNS[col[4]]


def _ycal(words, ax_x, stubs, ticks):
    labs = sorted(((w[1] + w[3]) / 2, _num(w[4])) for w in words if _num(w[4]) is not None
                  and ax_x - 20 < w[2] < ax_x and min(stubs) - 4 < (w[1] + w[3]) / 2 < max(stubs) + 4)
    vals = [v for _, v in labs][::-1]
    if vals != ticks or len(stubs) != len(ticks):
        raise ValueError(f"y axis at x {ax_x:.1f}: labels {vals}, {len(stubs)} stubs")
    for (ly, _), s in zip(labs, stubs):
        if abs(ly - s) > 2:
            raise ValueError(f"y label at {ly:.1f} does not sit on stub {s:.1f}")
    return calibrate(list(zip(sorted(stubs, reverse=True), ticks)))


def _bars(draws, words, ax_x, base, top, col, cal):
    """{week: bar} for the white bars right of a y axis between its top stub and its base."""
    unc = UNC_PT + cal.residual / abs(cal.slope)
    rects = [d["rect"] for d in draws if d.get("fill") == (1.0, 1.0, 1.0) and _kind(d) in ("re", "llll")
             and ax_x < d["rect"].x0 < ax_x + 230 and abs(d["rect"].y1 - base) < TOUCH and d["rect"].y0 > top - 2]
    errs = [d["rect"] for d in draws if _kind(d) == "lll" and d.get("fill") is None
            and ax_x < d["rect"].x0 < ax_x + 230 and top - 2 < d["rect"].y0 < base]
    out = {}
    for r in rects:
        cx = (r.x0 + r.x1) / 2
        lab = [w for w in words if w[4] == "Week" and 0 < w[1] - base < 25 and abs((w[0] + w[2]) / 2 + 4 - cx) < 15]
        num = [w for w in words if lab and w[0] > lab[0][2] and abs(w[1] - lab[0][1]) < 1 and w[0] - lab[0][2] < 6]
        if len(lab) != 1 or len(num) != 1:
            raise ValueError(f"bar at x {cx:.1f}: label {lab} {num}")
        week = int(num[0][4])
        e = [x for x in errs if abs((x.x0 + x.x1) / 2 - cx) < TOUCH and abs(x.y1 - r.y0) < TOUCH]
        if len(e) != 1:
            raise ValueError(f"{col} week {week}: {len(e)} error paths on the bar")
        if week in out:
            raise ValueError(f"two {col} bars at week {week}")
        out[week] = {"mean": _triple(cal, r.y0, unc), "error": _triple(cal, e[0].y0, unc)}
    if sorted(out) != WEEKS[col]:
        raise ValueError(f"{col} bars at weeks {sorted(out)}")
    return out


def _curves(draws, words, ax_x, ystubs, col, caly, xaxes):
    """{week: {calcium: bar}} for the curve markers of one panel c."""
    unc = UNC_PT + caly.residual / abs(caly.slope)
    left, right, top, bottom = ax_x, ax_x + 240, min(ystubs) - 10, max(ystubs) + 10
    xa = [a for a in xaxes if abs(a[1][0] - ax_x) < 15 and a[0] > max(ystubs) - 5]
    if len(xa) != 1:
        raise ValueError(f"panel c {col}: {len(xa)} x axes")
    xy, xstubs = xa[0]
    xlab = sorted(((w[0] + w[2]) / 2, _num(w[4])) for w in words if _num(w[4]) is not None and 0 < w[1] - xy < 15
                  and left - 10 < w[0] < right)
    if [v for _, v in xlab] != X_TICKS or len(xstubs) != len(X_TICKS):
        raise ValueError(f"panel c {col}: x labels {xlab}, stubs {xstubs}")
    for (lx, _), s in zip(xlab, xstubs):
        if abs(lx - s) > 2:
            raise ValueError(f"x label at {lx:.1f} does not sit on stub {s:.1f}")
    calx = calibrate(list(zip(xstubs, X_TICKS)))

    marks = []                                    # (shape, cx, cy) of filled markers
    for d in draws:
        r = d["rect"]
        if d.get("fill") is None or not (2 < r.width < 4 and 2 < r.height < 4) or _kind(d) not in SHAPES:
            continue
        cx, cy = _centre(r)
        if left < cx < right and top < cy < bottom:
            marks.append((SHAPES[_kind(d)], cx, cy, r))
    weeks = [w for w in words if w[4] == "Week" and left < w[0] < right and top < w[1] < bottom]
    legend, plot = {}, []
    for m in marks:
        on = [w for w in weeks if abs((w[1] + w[3]) / 2 - m[2]) < 3 and 0 < w[0] - m[1] < 30]
        if not on:
            plot.append(m)
            continue
        num = [w for w in words if w[0] > on[0][2] and abs(w[1] - on[0][1]) < 1 and w[0] - on[0][2] < 6]
        if len(on) != 1 or len(num) != 1 or m[0] in legend:
            raise ValueError(f"panel c {col}: legend marker {m[0]} at {m[1]:.1f}, {m[2]:.1f}")
        legend[m[0]] = int(num[0][4])
    if sorted(legend.values()) != WEEKS[col]:
        raise ValueError(f"panel c {col}: legend weeks {legend}")

    halves = [_segs(d)[0] for d in draws if _kind(d) == "l" and d.get("fill") is None
              and abs(d["rect"].width) < 0.01 and d["rect"].height > 0.01]
    series = {w: {} for w in legend.values()}
    for shape, cx, cy, r in plot:
        week = legend[shape]
        ca = round(calx.value(cx) / X_STEP) * X_STEP
        if abs(calx.value(cx) - ca) > X_TOL:
            raise ValueError(f"{col} week {week} marker at {calx.value(cx):.3f} mM is not on a {X_STEP} step")
        ca = round(ca, 6)
        if ca in series[week]:
            raise ValueError(f"two {col} week {week} markers at {ca} mM")
        at = [h for h in halves if abs(h[0] - cx) < SAME]
        up = [min(h[1], h[3]) for h in at if abs(max(h[1], h[3]) - cy) < SAME]
        down = [max(h[1], h[3]) for h in at if abs(min(h[1], h[3]) - cy) < SAME]
        if len(up) > 1 or len(down) > 1 or len(up) != len(down):
            raise ValueError(f"{col} week {week} at {ca}: {len(up)} upper and {len(down)} lower bar halves")
        bar = {"mean": _triple(caly, cy, unc), "x": ca}
        if up:
            if abs((cy - up[0]) - (down[0] - cy)) > SYM:
                raise ValueError(f"{col} week {week} at {ca}: bar not symmetric ({cy - up[0]:.2f} vs {down[0] - cy:.2f})")
            bar["error"] = _triple(caly, up[0], unc)
        series[week][ca] = bar
    steps = {w: tuple(sorted(s)) for w, s in series.items()}
    if len(set(steps.values())) != 1 or not all(steps.values()):
        raise ValueError(f"panel c {col}: series not read at the same calcium concentrations: {steps}")
    return series


def read(fig):
    draws, words = fig.drawings(), fig.words()
    heads = [w for w in words if w[4] in COLUMNS]
    if sorted(h[4] for h in heads) != sorted(COLUMNS):
        raise ValueError(f"column headings {heads}")
    xaxes = _axes(draws, False)
    groups, seen = {}, set()
    for ax_x, stubs in _axes(draws, True):
        panel, col = _panel(words, heads, ax_x, stubs)
        if (panel, col) in seen:
            raise ValueError(f"two y axes for panel {panel} {col}")
        seen.add((panel, col))
        cal = _ycal(words, ax_x, stubs, Y_TICKS[panel])
        if panel in "ab":
            bars = _bars(draws, words, ax_x, max(stubs), min(stubs), col, cal)
            for item in ITEMS[panel][col]:
                for g in ITEM_GROUPS[item]:
                    groups[f"{item}/{g}"] = {"points": [], "countable": False, "bar": bars[int(g.split("_w")[1])]}
        else:
            series = _curves(draws, words, ax_x, stubs, col, cal, xaxes)
            for item in ITEMS[panel][col]:
                for g in ITEM_GROUPS[item]:
                    for ca, bar in sorted(series[int(g.split("_w")[1])].items()):
                        groups[f"{item}/{g}_{ca:g}"] = {"points": [], "countable": False, "bar": bar}
    if len(seen) != 6:
        raise ValueError(f"panels found: {sorted(seen)}")
    return {"groups": groups}
