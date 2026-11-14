"""Suppl. Fig. 1c (supplement p. 40): FOC (mN, left) and time to 50% relaxation (T2-50, ms, right) in undefined vs.
defined EHM at 0.8 mmol/l Ca2+, then Iso 1 µmol/l, then Iso 1 + Carb 10 µmol/l. Each marker is a group mean with a
vertical error bar; no single EHM is drawn, so every group is bar only (countable false).

Both panels are vector and share one crop; each panel spans from its y axis to the next panel's. A mean marker is a
small filled path drawn inside the axis range (legend markers sit above it): four curve segments (circle) for Undef.
EHM, four lines (square) for Def. EHM, as the legend draws them. Its error bar is two vertical single-line paths at the
marker's x that meet at one point: that joint is the mean (the connecting lines' vertices fall on it too; the marker's
box centre is checked against it within 0.1 pt), and the top end of the upper path is 'error' (a cap must be drawn
there). Columns are named from the rows printed under the x axis: the column with neither an Iso nor a Carb value is
baseline ("base"), Iso only is "iso", Iso and Carb is "carb". Each y axis is calibrated from its axis path's tick stubs,
matched in order to the printed tick labels (the right axis has a break below 60; its stubs start at 60).

One curve point is shared by several record items (e.g. Def. Iso by S1c_foc_def_iso and S1c_foc_def_carb), and a
figures.yaml label links to one item, so each reading is returned once per item that uses it: label "<item>/<group>".
"""
from livinglit.figures.source import calibrate, point

UNC_PT = 0.5                                  # vector position uncertainty (pt)
PANELS = [                                    # left to right: panel, printed y tick labels bottom to top
    ("foc", [0, 0.2, 0.4, 0.6, 0.8, 1.0]),    # FOC (mN)
    ("t50", [60, 80, 100, 120]),              # Time to 50% relaxation (T2-50, ms)
]
ITEMS = {                                     # record items per panel, and the groups each one involves
    "foc": {"S1c_foc_def_iso": ["def_iso", "def_base"], "S1c_foc_def_carb": ["def_carb", "def_iso"],
            "S1c_foc_undef_iso": ["undef_iso", "undef_base"], "S1c_foc_undef_carb": ["undef_carb", "undef_iso"]},
    "t50": {"S1c_t50_def_iso": ["def_iso", "def_base"], "S1c_t50_def_carb": ["def_carb", "def_iso"],
            "S1c_t50_undef_iso": ["undef_iso", "undef_base"], "S1c_t50_undef_carb": ["undef_carb", "undef_iso"],
            "S1c_t50_protocol": ["def_base", "def_iso", "def_carb", "undef_base", "undef_iso", "undef_carb"]},
}
MARKER_MAX = 7.0                              # markers are ~5.2 pt across
TOL = 0.15                                    # pt: segment ends meeting, x alignment


def _axes(fig):
    """Each y axis path (a long vertical line plus short tick stubs to its left): (x, stub y positions), left to right."""
    out = []
    for d in fig.drawings():
        items = d["items"]
        if len(items) < 3 or any(it[0] != "l" for it in items):
            continue
        long = [it for it in items if abs(it[1].x - it[2].x) < 0.01 and abs(it[1].y - it[2].y) > 100]
        if len(long) == 1:
            stubs = [it[1].y for it in items if abs(it[1].y - it[2].y) < 0.01 and 0 < abs(it[1].x - it[2].x) < 6]
            out.append((long[0][1].x, stubs))
    return sorted(out)


def _columns(fig, ax_x, x_end):
    """Column x centres from the Ca2+ row ('0.8' under each column), named by the Iso and Carb rows beneath it."""
    words = [w for w in fig.words() if ax_x < (w[0] + w[2]) / 2 < x_end]
    ca = sorted((w[0] + w[2]) / 2 for w in words if w[4] == "0.8")
    if len(ca) != 3:
        raise ValueError(f"{len(ca)} Ca2+ columns")
    row_y = {name: max((w for w in fig.words() if w[4] == name and w[2] < ax_x), key=lambda w: w[0])[1]
             for name in ("Iso", "Carb")}                       # this panel's row label: the nearest left of its axis
    has = {c: set() for c in ca}
    for w in words:
        for name, y in row_y.items():
            if abs(w[1] - y) < 3 and w[4].isdigit():
                has[min(ca, key=lambda c: abs(c - (w[0] + w[2]) / 2))].add(name)
    names = {frozenset(): "base", frozenset({"Iso"}): "iso", frozenset({"Iso", "Carb"}): "carb"}
    cols = {names[frozenset(has[c])]: c for c in ca}
    if len(cols) != 3:
        raise ValueError(f"columns {has}")
    return cols


def _panel(fig, ticks, ax_x, stubs, x_end, labels_from):
    printed = sorted(float(w[4]) for w in fig.words()
                     if labels_from <= w[0] and w[2] < ax_x and w[4].replace(".", "", 1).isdigit())
    if printed != sorted(float(t) for t in ticks) or len(stubs) != len(ticks):
        raise ValueError(f"tick labels {printed}, {len(stubs)} stubs")
    cal = calibrate(list(zip(sorted(stubs, reverse=True), ticks)))
    unc = UNC_PT + abs(cal.residual / cal.slope)
    top, bottom = min(stubs), max(stubs)
    cols = _columns(fig, ax_x, x_end)
    draws = [d for d in fig.drawings() if ax_x < d["rect"].x0 < x_end]
    segs = [(d["items"][0][1], d["items"][0][2]) for d in draws if len(d["items"]) == 1 and d["items"][0][0] == "l"]
    vert = [(a.x, min(a.y, b.y), max(a.y, b.y)) for a, b in segs if abs(a.x - b.x) < 0.01 and abs(a.y - b.y) > 0.01]
    caps = [((a.x + b.x) / 2, a.y) for a, b in segs if abs(a.y - b.y) < 0.01 and 3 < abs(a.x - b.x) < MARKER_MAX]
    out = {}
    for d in draws:
        r = d["rect"]
        if d.get("fill") is None or not (0.3 < r.width <= MARKER_MAX and 0.3 < r.height <= MARKER_MAX) \
                or not top - 10 < r.y0 < bottom:
            continue
        ops = {it[0] for it in d["items"]}
        shape = "undef" if ops == {"c"} and len(d["items"]) == 4 else "def" if ops == {"l"} and len(d["items"]) == 4 \
            else None
        if shape is None:
            raise ValueError(f"marker of unknown shape at {r}")
        mx, my = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
        col = min(cols, key=lambda c: abs(cols[c] - mx))
        group = f"{shape}_{col}"
        mine = [v for v in vert if abs(v[0] - mx) < TOL and (abs(v[1] - my) < 1 or abs(v[2] - my) < 1)]
        upper = [v for v in mine if abs(v[2] - my) < 1]
        lower = [v for v in mine if abs(v[1] - my) < 1]
        if len(upper) != 1 or len(lower) != 1 or abs(upper[0][2] - lower[0][1]) > TOL:
            raise ValueError(f"{group}: error bar segments {mine}")
        mean, err = upper[0][2], upper[0][1]
        if abs(mean - my) > 0.1:
            raise ValueError(f"{group}: marker centre {my:.2f} off the bar joint {mean:.2f}")
        if not any(abs(cx - mx) < TOL and abs(cy - err) <= UNC_PT for cx, cy in caps):  # t50 def_carb: cap 0.29 pt off
            raise ValueError(f"{group}: no cap at the upper end")
        if group in out:
            raise ValueError(f"{group}: two markers")
        out[group] = {"points": [], "countable": False,
                      "bar": {"mean": [cal.value(mean), *cal.interval(mean, unc)],
                              "error": [cal.value(err), *cal.interval(err, unc)]}}
    if len(out) != 6:
        raise ValueError(f"found groups {sorted(out)}")
    return out


def read(fig):
    axes = _axes(fig)
    if len(axes) != len(PANELS):
        raise ValueError(f"found {len(axes)} y axes")
    groups = {}
    for i, ((name, ticks), (ax_x, stubs)) in enumerate(zip(PANELS, axes)):
        x_end = axes[i + 1][0] - 60 if i + 1 < len(axes) else fig.crop[2]
        labels_from = max(axes[i - 1][0] if i else fig.crop[0], ax_x - 40)
        bars = _panel(fig, ticks, ax_x, stubs, x_end, labels_from)
        for item, gs in ITEMS[name].items():
            for g in gs:
                groups[f"{item}/{g}"] = bars[g]
    return {"groups": groups}
