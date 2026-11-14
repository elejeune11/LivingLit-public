"""Suppl. Fig. 10b (supplement p. 57): change after 7 days of 1 umol/L NE compared to untreated controls, as bars for
FOC, ISO and CM size. Y axis '% change compared to untreated' (ticks -80 ... 20). Black bars: Starting Protocol (n=8);
grey bars: Serum-free Protocol (n=11) (legend, right of the bars, outside the crop). Each bar is a group mean with a
one-sided error bar drawn away from zero (the legend does not say SD or SEM); no single EHM is drawn.

The panel is vector. The y axis is the drawing with a long vertical line; its short horizontal stubs are matched to
the nearest printed tick label. A bar is a filled rectangle of the group's colour with one edge on the zero line
(the horizontal axis line); its other edge is the mean. The bar's category is the label (FOC, ISO, CM) below the
zero line whose centre lies between the centres of the bar and its partner of the other colour. Each error bar is one stroked path: a short cap and a
stem from the cap centre to the bar's far edge; the cap is 'error' (below the mean for negative bars, so 'error' is
the far end of the bar, not always the upper end).
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate

ITEMS = {"FOC": "S10b_foc", "ISO": "S10b_iso", "CM": "S10b_cmsize"}   # category label under the bars -> item
GROUPS = {"sp": (0.0, 0.0, 0.0), "sf": (0.628, 0.628, 0.643)}        # fill RGB of each group's bars
COL_TOL = 0.05        # colour match (RGB 0-1)
STUB_MAX = 6.0        # tick stubs are shorter than this (pt)
CAP_MAX = 15.0        # error caps are shorter than this (pt)
AXIS_MIN = 100.0      # the axis lines are longer than this (pt)
LABEL_TOL = 1.5       # a tick stub lies within this of its label's centre (pt)
EDGE_TOL = 0.05       # a bar edge lies on the zero line, and a stem meets the bar edge, within this (pt)
CENTRE_TOL = 0.2      # stem and cap are centred on the bar within this (pt)


def _same(c, rgb):
    return c is not None and max(abs(a - b) for a, b in zip(c, rgb)) <= COL_TOL


def _segs(d):
    return [(it[1], it[2]) for it in d["items"] if it[0] == "l"]


def _axes(fig):
    ystubs, zero = [], None
    for d in fig.drawings():
        segs = _segs(d)
        if any(abs(a.x - b.x) < 0.01 and abs(a.y - b.y) > AXIS_MIN for a, b in segs):
            ystubs += [a.y for a, b in segs if abs(a.y - b.y) < 0.01 and abs(a.x - b.x) < STUB_MAX]
        if d.get("fill") is None and len(segs) == 1:
            a, b = segs[0]
            if abs(a.y - b.y) < 0.01 and abs(a.x - b.x) > AXIS_MIN:
                zero = a.y
    labels = fig.tick_marks("y")
    marks = []
    for y in ystubs:
        near = [v for p, v in labels if abs(p - y) <= LABEL_TOL]
        if len(near) != 1:
            raise ValueError(f"y stub at {y:.1f}: {len(near)} labels within {LABEL_TOL} pt")
        marks.append((y, near[0]))
    if len(marks) < 3:
        raise ValueError(f"found {len(marks)} labelled y ticks")
    cal = calibrate(marks)
    if zero is None or abs(cal.value(zero)) > cal.residual + 1e-6 + abs(cal.slope) * EDGE_TOL:
        raise ValueError(f"zero line at {zero} does not read 0")
    return cal, zero


def _bars(fig, zero):
    """{group: [(x_centre, mean_y)]} for filled rectangles with one edge on the zero line."""
    out = {g: [] for g in GROUPS}
    for d in fig.drawings():
        r = d["rect"]
        if d.get("fill") is None or len(_segs(d)) != 4 or r.width < STUB_MAX:
            continue
        g = [k for k, rgb in GROUPS.items() if _same(d["fill"], rgb)]
        if len(g) != 1:
            continue
        if abs(r.y0 - zero) <= EDGE_TOL:
            far = r.y1
        elif abs(r.y1 - zero) <= EDGE_TOL:
            far = r.y0
        else:
            continue          # legend swatches
        out[g[0]].append(((r.x0 + r.x1) / 2, far))
    return out


def _cap(fig, x, far):
    """The cap y of the error path whose stem runs from (x, far)."""
    found = []
    for d in fig.drawings():
        if d.get("fill") is not None:
            continue
        segs = _segs(d)
        stems = [(a, b) for a, b in segs if abs(a.x - b.x) < 0.01 and abs(a.x - x) <= CENTRE_TOL
                 and min(abs(a.y - far), abs(b.y - far)) <= EDGE_TOL]
        caps = [(a, b) for a, b in segs if abs(a.y - b.y) < 0.01 and 0 < abs(a.x - b.x) < CAP_MAX
                and abs((min(a.x, b.x) + max(a.x, b.x)) / 2 - x) <= CENTRE_TOL]
        if len(stems) == 1 and caps:
            a, b = stems[0]
            end = a.y if abs(b.y - far) <= EDGE_TOL else b.y
            cy = {round(c[0].y, 4) for c in caps}
            if cy != {round(end, 4)}:
                raise ValueError(f"error path at x={x:.1f}: cap {cy} does not meet stem end {end}")
            found.append(end)
    if len(found) != 1:
        raise ValueError(f"expected one error bar at x={x:.1f}, found {found}")
    return found[0]


def _category(fig, x0, x1, zero):
    names = [w[4] for w in fig.words() if w[4] in ITEMS and w[1] > zero and x0 < (w[0] + w[2]) / 2 < x1]
    if len(names) != 1:
        raise ValueError(f"bars at {x0:.1f}-{x1:.1f}: category labels {names}")
    return names[0]


def _triple(cal, pos, unc):
    v = cal.value(pos)
    a, b = cal.interval(pos, unc)
    return [v, min(a, v), max(b, v)]


def read(fig):
    cal, zero = _axes(fig)
    unc = VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)
    bars = _bars(fig, zero)
    sp, sf = sorted(bars["sp"]), sorted(bars["sf"])
    if len(sp) != len(ITEMS) or len(sf) != len(ITEMS):
        raise ValueError(f"bars found: sp {len(sp)}, sf {len(sf)}")
    groups = {}
    for (xa, ya), (xb, yb) in zip(sp, sf):
        if not xa < xb:
            raise ValueError(f"pair order at {xa:.1f}, {xb:.1f}")
        item = ITEMS[_category(fig, xa, xb, zero)]
        for g, x, y in (("sp", xa, ya), ("sf", xb, yb)):
            cap = _cap(fig, x, y)
            if (cap - y) * (y - zero) < 0:
                raise ValueError(f"{item}/{g}: error bar points toward zero")
            groups[f"{item}/{g}"] = {"points": [], "countable": False,
                                     "bar": {"mean": _triple(cal, y, unc), "error": _triple(cal, cap, unc)}}
    if len(groups) != 2 * len(ITEMS):
        raise ValueError(f"groups read: {sorted(groups)}")
    return {"groups": groups}
