"""Suppl. Fig. 10a, left plot (supplement p. 57): force-frequency response of serum-free EHM (Serum-free Protocol,
n=4) after 7 days of 1 umol/L NE. Y axis '% of FOC at 1 Hz' (ticks 50, 100, 150), x axis 'Stimulation frequency (Hz)'
(1, 2, 3). Black filled circles: Untreated; red filled squares: 1 umol/L NE (legend, right of the Starting protocol
plot, outside the crop). Each marker is a group mean with a vertical error bar (the legend does not say SD or SEM);
no single EHM is drawn. The asterisk bracket joins the two curves at 3 Hz.

The panel is vector. Only the 3 Hz means the record's item compares are read (sf_unt_3, sf_ne_3), as bars (mean and
upper error end, x = 3 Hz), no points. The y axis is the drawing with a long vertical line; its short horizontal stubs
are matched to the nearest printed tick label. The x axis stubs are matched to the printed 1, 2, 3. A marker is a
small filled shape of the group's colour at the 3 Hz stub; its centre is checked against the vertex of the group's
connecting polyline (segments longer than a stub, shorter than the axis). The upper error end is the short horizontal cap of the same colour nearest above the marker;
the lower cap is checked to mirror it.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate

ITEM = "S10a_sf3"
GROUPS = {"sf_unt_3": (0.0, 0.0, 0.0), "sf_ne_3": (0.628, 0.0, 0.0)}   # fill/stroke RGB of each group's marks
HZ = 3
X_TICKS = [1, 2, 3]
COL_TOL = 0.05        # colour match (RGB 0-1)
STUB_MAX = 6.0        # tick stubs and error caps are shorter than this (pt)
AXIS_MIN = 100.0      # the axis lines are longer than this (pt)
X_TOL = 1.0           # marker, cap and vertex share the stub's x within this (pt)
LABEL_TOL = 1.5       # a tick stub lies within this of its label's centre (pt)
VERTEX_TOL = 0.2      # marker centre and polyline vertex agree within this (pt)
SYM_TOL = 0.2         # upper and lower caps are equidistant from the mean within this (pt)


def _same(c, rgb):
    return c is not None and max(abs(a - b) for a, b in zip(c, rgb)) <= COL_TOL


def _lines(fig):
    """(drawing, p1, p2) for every straight segment in the crop."""
    for d in fig.drawings():
        for it in d["items"]:
            if it[0] == "l":
                yield d, it[1], it[2]


def _axes(fig):
    ystubs, xstubs, axis_y = [], [], None
    for d in fig.drawings():
        segs = [it for it in d["items"] if it[0] == "l"]
        vert = [s for s in segs if abs(s[1].x - s[2].x) < 0.01 and abs(s[1].y - s[2].y) > AXIS_MIN]
        horiz = [s for s in segs if abs(s[1].y - s[2].y) < 0.01 and abs(s[1].x - s[2].x) > AXIS_MIN]
        if vert:
            ystubs += [s[1].y for s in segs if abs(s[1].y - s[2].y) < 0.01 and abs(s[1].x - s[2].x) < STUB_MAX]
        if horiz:
            axis_y = horiz[0][1].y
            xstubs += [s[1].x for s in segs if abs(s[1].x - s[2].x) < 0.01 and abs(s[1].y - s[2].y) < STUB_MAX]
    labels = fig.tick_marks("y")
    marks = []
    for y in ystubs:
        near = [(abs(p - y), v) for p, v in labels if abs(p - y) <= LABEL_TOL]
        if len(near) != 1:
            raise ValueError(f"y stub at {y:.1f}: {len(near)} labels within {LABEL_TOL} pt")
        marks.append((y, near[0][1]))
    if len(marks) < 3:
        raise ValueError(f"found {len(marks)} labelled y ticks")
    xstubs = sorted(xstubs)
    if len(xstubs) != len(X_TICKS):
        raise ValueError(f"found {len(xstubs)} x stubs")
    xlab = sorted(float(w[4]) for w in fig.words() if w[1] > axis_y and w[4] in {str(t) for t in X_TICKS})
    if xlab != X_TICKS:
        raise ValueError(f"x labels {xlab}")
    return calibrate(marks), dict(zip(X_TICKS, xstubs))


def _marker(fig, rgb, x):
    found = [((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2) for d in fig.drawings()
             for r in [d["rect"]] if _same(d.get("fill"), rgb) and 0.3 < r.width <= STUB_MAX
             and 0.3 < r.height <= STUB_MAX and abs((r.x0 + r.x1) / 2 - x) <= X_TOL]
    found = sorted(set((round(a, 4), round(b, 4)) for a, b in found))
    if len(found) != 1:
        raise ValueError(f"expected one marker at x={x:.1f}, found {found}")
    return found[0]


def _vertex(fig, rgb, x):
    v = {round(p.y, 4) for d, a, b in _lines(fig) if _same(d.get("color"), rgb)
         for p in (a, b) if abs(p.x - x) <= X_TOL and STUB_MAX < abs(a.x - b.x) < AXIS_MIN}
    if len(v) != 1:
        raise ValueError(f"expected one polyline vertex at x={x:.1f}, found {v}")
    return v.pop()


def _caps(fig, rgb, x, y):
    caps = sorted({round(a.y, 4) for d, a, b in _lines(fig) if _same(d.get("color"), rgb) and abs(a.y - b.y) < 0.01
                   and 0 < abs(a.x - b.x) < STUB_MAX and abs((a.x + b.x) / 2 - x) <= X_TOL})
    up = [c for c in caps if c < y]
    lo = [c for c in caps if c > y]
    if not up or not lo:
        raise ValueError(f"caps at x={x:.1f}: {caps}")
    up, lo = max(up), min(lo)
    if abs((y - up) - (lo - y)) > SYM_TOL:
        raise ValueError(f"caps {up}, {lo} not symmetric about {y}")
    return up


def _triple(cal, pos, unc):
    v = cal.value(pos)
    a, b = cal.interval(pos, unc)
    return [v, min(a, v), max(b, v)]


def read(fig):
    cal, xs = _axes(fig)
    unc = VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)
    x = xs[HZ]
    groups = {}
    for g, rgb in GROUPS.items():
        mx, my = _marker(fig, rgb, x)
        vy = _vertex(fig, rgb, x)
        if abs(vy - my) > VERTEX_TOL:
            raise ValueError(f"{g}: marker centre {my} and polyline vertex {vy} disagree")
        up = _caps(fig, rgb, x, my)
        groups[f"{ITEM}/{g}"] = {"points": [], "countable": False,
                                 "bar": {"mean": _triple(cal, my, unc), "error": _triple(cal, up, unc), "x": HZ}}
    return {"groups": groups}
