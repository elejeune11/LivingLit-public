"""Suppl. Fig. 1a,b (supplement p. 40): (a) force per cardiomyocyte (nN) and (b) actinin MFI in undefined vs. defined
EHM; one marker per EHM, with a horizontal mean line and an error bar (whisker caps) per group.

Both panels are vector and share one crop; each panel spans from its y axis to the next panel's. Each EHM is a small
filled path (squares; panel b's defined group is triangles), drawn once filled and once stroked; the filled copy is
taken. A marker belongs to the group whose x-axis label ("Undef." / "Def.") is nearest in x. A marker's position is
its bounding-box centre, triangles included (TRIANGLE_AT: the vertex centroid would sit 0.87 pt lower and puts the
mean of panel b's defined points 0.67 MFI below the drawn mean line; the box centre matches it). Each y axis is
calibrated from its axis path's tick stubs, matched in order to the printed tick labels. In each group column the
longest horizontal line is the mean and the two shorter caps are the error-bar ends; the upper one (smaller page y)
is 'error'.
"""
from livinglit.figures.source import calibrate, point

UNC_PT = 0.5                          # vector position uncertainty (pt)
PANELS = [                            # left to right: panel, printed y tick labels bottom to top
    ("a", [0, 5, 10, 15]),            # Force per CM (nN)
    ("b", [0, 20, 40, 60, 80, 100]),  # Actinin MFI
]
GROUP_WORDS = {"Undef.": "undef", "Def.": "def"}
MARKER_MAX = 7.0                      # markers are ~5.2 pt across
MEAN_MIN = 55.0                       # mean lines are ~64 pt long; caps ~32 pt
CAP_MIN = 20.0
TRIANGLE_AT = "bbox"                  # "centroid" or "bbox"


def _axes(fig):
    """Each y axis path (a long vertical line plus short tick stubs to its left): (x, stub y positions), left to right."""
    out = []
    for d in fig.drawings():
        items = d["items"]
        if len(items) < 3 or any(it[0] != "l" for it in items):
            continue
        a, b = items[0][1], items[0][2]
        if abs(a.x - b.x) < 0.01 and abs(a.y - b.y) > 100:
            stubs = [it[1].y for it in items[1:] if abs(it[1].y - it[2].y) < 0.01 and abs(it[1].x - it[2].x) < 6]
            out.append((a.x, stubs))
    return sorted(out)


def _centre(d):
    r = d["rect"]
    if len(d["items"]) == 3 and TRIANGLE_AT == "centroid":
        v = [it[1] for it in d["items"]]
        return sum(p.x for p in v) / 3, sum(p.y for p in v) / 3
    return (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2


def _panel(fig, name, ticks, ax_x, stubs, x_end, labels_from):
    words = [w for w in fig.words() if labels_from <= w[0] < x_end]
    printed = sorted(float(w[4]) for w in words if w[2] < ax_x and w[4].isdigit())
    if printed != sorted(float(t) for t in ticks) or len(stubs) != len(ticks):
        raise ValueError(f"{name}: tick labels {printed}, {len(stubs)} stubs")
    cal = calibrate(list(zip(sorted(stubs, reverse=True), ticks)))
    unc = UNC_PT + abs(cal.residual / cal.slope)
    cols = {GROUP_WORDS[w[4]]: (w[0] + w[2]) / 2 for w in words if w[4] in GROUP_WORDS and w[0] > ax_x}

    def group_of(x):
        return min(cols, key=lambda g: abs(cols[g] - x))

    pts = {g: [] for g in cols}
    lines = {g: [] for g in cols}
    for d in fig.drawings():
        r = d["rect"]
        if not (ax_x < r.x0 < x_end):
            continue
        if d.get("fill") is not None and 0.3 < r.width <= MARKER_MAX and 0.3 < r.height <= MARKER_MAX:
            x, y = _centre(d)
            pts[group_of(x)].append((x, y))
        elif d.get("fill") is None and len(d["items"]) == 1 and d["items"][0][0] == "l" and r.height < 0.01 \
                and CAP_MIN <= r.width < 150:
            lines[group_of((r.x0 + r.x1) / 2)].append((r.width, r.y0))
    out = {}
    for g in cols:
        mean = [y for w, y in lines[g] if w >= MEAN_MIN]
        caps = [y for w, y in lines[g] if w < MEAN_MIN]
        if len(mean) != 1 or len(caps) != 2:
            raise ValueError(f"{name}_{g}: {len(mean)} mean lines, {len(caps)} caps")
        m, top = mean[0], min(caps)
        out[f"{name}_{g}"] = {
            "points": [point(cal, y, unc, (x, y)) for x, y in sorted(pts[g], key=lambda p: (p[1], p[0]))],
            "countable": True,
            "bar": {"mean": [cal.value(m), *cal.interval(m, unc)],
                    "error": [cal.value(top), *cal.interval(top, unc)]},
        }
    return out


def read(fig):
    axes = _axes(fig)
    if len(axes) != len(PANELS):
        raise ValueError(f"found {len(axes)} y axes")
    groups = {}
    for i, ((name, ticks), (ax_x, stubs)) in enumerate(zip(PANELS, axes)):
        x_end = axes[i + 1][0] - 40 if i + 1 < len(axes) else fig.crop[2]
        labels_from = axes[i - 1][0] if i else fig.crop[0]
        labels_from = max(labels_from, ax_x - 40)
        groups.update(_panel(fig, name, ticks, ax_x, stubs, x_end, labels_from))
    return {"groups": groups}
