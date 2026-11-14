"""Suppl. Fig. 4 (supplement p. 46): (a) a table of the EHM built per cell line (rows HES2, H7, hiPS-G1, iCell) and
protocol (columns Starting, Matrix, Serum-free), each cell showing that combination's plot marker and its n (or
'n.d.'); (b) force of contraction (FOC, mN, y) against calcium (mmol/L, x) at W4, one series per combination. Each plot
marker is a group mean at one calcium concentration with a symmetric vertical error bar, and a fitted curve runs
through each series. No single EHM is drawn, so every marker is returned as a bar (mean and upper error end) under
the label <item>/<group>_<calcium>, with the calcium concentration as the bar's x.

The panel is vector. A marker is a stroked outline (square 're', triangle 'lll', circle 'cccc', hexagon 'llllll') or,
in the table, a filled shape with no outline; it is filled when a filled path of its own size shares its centre, half
filled when a filled path of half its width starts at its centre (the right half), open otherwise. The table gives
each marker class its cell line and protocol: the row word left of it and the column header between the same table
rules; a cell with the word 'n.d.' is a class that must not be read. Plot markers are mapped to groups through that
table (the mapping is not typed in), and each read group must have one marker at each of the same calcium steps.

The y axis is one path (axis line plus tick stubs) calibrated from the stubs matched in order to the printed labels
left of it; the x axis likewise from the stubs below it. x is the calibrated marker centre rounded to 0.1 mmol/L (the
concentrations are not printed; every marker must lie within X_TOL of a step). The mean is the marker's bounding-box
centre. Each error bar is drawn as a vertical line from the marker (its centre for filled markers, its edge for open
and half filled ones) out to the bar end, above and below; the upper end is 'error'. Both halves are checked to be symmetric about the centre.
A marker whose bar is hidden inside it has no vertical line and gives no error end; a marker with only the lower half
drawn has it mirrored. Caps are not used (some are missing from the drawing).
"""
from livinglit.figures.source import calibrate, point

UNC_PT = 0.5
Y_TICKS = [0, 0.5, 1, 1.5, 2]                # printed y tick labels, bottom to top (FOC (mN))
X_TICKS = [0, 1, 2, 3, 4]                    # printed x tick labels, left to right (Calcium (mmol/L))
SHAPES = {"re": "square", "lll": "triangle", "cccc": "circle", "llllll": "hexagon"}
HALVES = {"square": "llll", "triangle": "lll", "circle": "lccl", "hexagon": "lllll"}
FULLS = {"square": "llll", "triangle": "lll", "circle": "cccc", "hexagon": "llllll"}
LINES = {"HES2": "hes2", "H7": "h7", "hiPS-G1": "g1", "iCell": "icell"}            # table row words
PROTOCOLS = {"Starting,": "start", "Matrix,": "matrix", "Serum-free,": "sf"}       # table column header words
ITEMS = {
    "S4_hes2_sf_hes2_start": ["hes2_sf", "hes2_start"],
    "S4_h7_sf_h7_matrix": ["h7_sf", "h7_matrix"],
    "S4_g1_sf_g1_start": ["g1_sf", "g1_start"],
    "S4_g1_sf_g1_matrix": ["g1_sf", "g1_matrix"],
    "S4_icell_sf_icell_matrix": ["icell_sf", "icell_matrix"],
}
X_STEP, X_TOL = 0.1, 0.03
SAME = 0.1                                   # pt: centres and line ends that coincide
SYM = 0.1                                    # pt: upper and lower bar halves agree within this


def _kind(d):
    return "".join(i[0] for i in d["items"])


def _centre(r):
    return (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2


def _markers(draws):
    """(shape, fill, cx, cy, rect) for every marker: stroked outlines, and filled shapes with no outline."""
    small = [d for d in draws if 4 < d["rect"].width < 8 and 4 < d["rect"].height < 8]
    outlines = [d for d in small if d.get("fill") is None and _kind(d) in SHAPES]
    fills = [d for d in draws if d.get("fill") is not None and d["rect"].height > 4 and d["rect"].width < 8]
    out = []
    for d in outlines:
        shape, r = SHAPES[_kind(d)], d["rect"]
        cx, cy = _centre(r)
        full = [f for f in fills if _kind(f) == FULLS[shape] and abs(f["rect"].width - r.width) < 0.2
                and max(abs(a - b) for a, b in zip(_centre(f["rect"]), (cx, cy))) < SAME]
        half = [f for f in fills if _kind(f) == HALVES[shape] and abs(f["rect"].width - r.width / 2) < 0.2
                and abs(f["rect"].x0 - cx) < SAME and abs(_centre(f["rect"])[1] - cy) < SAME]
        if full and half:
            raise ValueError(f"marker at {cx:.2f}, {cy:.2f} is both filled and half filled")
        out.append((shape, "filled" if full else "half" if half else "open", cx, cy, r))
    for f in fills:                              # filled shapes drawn without an outline (the table)
        k, r = _kind(f), f["rect"]
        shape = {"lll": "triangle", "llllll": "hexagon", "cccc": "circle"}.get(k)
        if shape is None or r.width < 4:
            continue
        cx, cy = _centre(r)
        if not any(m[0] == shape and abs(m[2] - cx) < SAME and abs(m[3] - cy) < SAME for m in out):
            out.append((shape, "filled", cx, cy, r))
    return out


def _axis(draws, vertical):
    """The axis path: one long line with its tick stubs; returns the stub positions (y for the y axis, x for x)."""
    for d in draws:
        segs = [(i[1].x, i[1].y, i[-1].x, i[-1].y) for i in d["items"] if i[0] == "l"]
        if len(segs) != len(d["items"]) or len(segs) != 6:
            continue
        r = d["rect"]
        if vertical and r.height > 200 and r.width < 10:
            return sorted(s[1] for s in segs if abs(s[1] - s[3]) < 0.01)
        if not vertical and r.width > 300 and r.height < 10:
            return sorted(s[0] for s in segs if abs(s[0] - s[2]) < 0.01)
    raise ValueError("axis path not found")


def _legend(draws, words, marks, plot_top):
    """{(shape, fill): group or None (n.d.)} from the table: row word, column header between the table rules."""
    rules = sorted(_centre(d["rect"])[0] for d in draws if _kind(d) == "l" and d["rect"].height > 100
                   and d["rect"].width < 1 and d["rect"].y1 < plot_top)
    rows = [w for w in words if w[4] in LINES]
    heads = [w for w in words if w[4] in PROTOCOLS]
    table = {}
    for shape, fill, cx, cy, _ in marks:
        if cy > plot_top:
            continue
        row = [w for w in rows if w[1] < cy < w[3]]
        left = max(x for x in rules if x < cx)
        right = min(x for x in rules + [1e9] if x > cx)
        head = [w for w in heads if left < (w[0] + w[2]) / 2 < right]
        cell = [w[4] for w in words if left < w[0] < right and abs((w[1] + w[3]) / 2 - cy) < 4]
        if len(row) != 1 or len(head) != 1:
            raise ValueError(f"table marker at {cx:.1f}, {cy:.1f}: row {row}, header {head}")
        group = f"{LINES[row[0][4]]}_{PROTOCOLS[head[0][4]]}"
        if (shape, fill) in table:
            raise ValueError(f"two table cells use {shape} {fill}")
        table[(shape, fill)] = None if "n.d." in cell else group
    return table


def _bar_ends(draws, cx, cy, r, fill):
    """Far ends of the vertical bar halves above and below a marker, or None for a half not drawn. The halves start
    at the centre of a filled marker and at the edge of an open or half filled one, half the marker's width from
    its centre (the hexagon outline is flatter than that, and its bar starts above and below its outline)."""
    top, bottom = (cy, cy) if fill == "filled" else (cy - r.width / 2, cy + r.width / 2)
    lines = [d["rect"] for d in draws if _kind(d) == "l" and d.get("fill") is None and d["rect"].width < 0.01
             and abs(d["rect"].x0 - cx) < SAME]
    up = [v for v in lines if abs(v.y1 - top) < SAME and v.y0 < v.y1 - 0.01]
    down = [v for v in lines if abs(v.y0 - bottom) < SAME and v.y1 > v.y0 + 0.01]
    if len(up) > 1 or len(down) > 1:             # another series' line meets this marker: keep the symmetric pair
        pairs = [(u, d) for u in up for d in down if abs((top - u.y0) - (d.y1 - bottom)) < SYM]
        if len(pairs) != 1:
            raise ValueError(f"marker at {cx:.2f}, {cy:.2f}: {len(up)} upper and {len(down)} lower bar lines")
        up, down = [pairs[0][0]], [pairs[0][1]]
    return (up[0].y0 if up else None), (down[0].y1 if down else None)


def _triple(cal, pos, unc):
    p = point(cal, pos, unc, (0, 0))
    return [p["value"], p["lo"], p["hi"]]


def read(fig):
    draws, words = fig.drawings(), fig.words()
    ystubs, xstubs = _axis(draws, True), _axis(draws, False)
    plot_top = min(ystubs) - 2
    ylab = sorted(float(w[4]) for w in words if w[2] < min(xstubs) - 20 and w[1] > plot_top - 10
                  and w[4].replace(".", "").isdigit())
    xlab = sorted(float(w[4]) for w in words if w[1] > max(ystubs) + 20 and w[4].isdigit())
    if ylab != Y_TICKS or len(ystubs) != len(Y_TICKS) or xlab != X_TICKS or len(xstubs) != len(X_TICKS):
        raise ValueError(f"ticks: y {ylab} {ystubs}, x {xlab} {xstubs}")
    caly = calibrate(list(zip(sorted(ystubs, reverse=True), Y_TICKS)))
    calx = calibrate(list(zip(xstubs, X_TICKS)))
    unc = UNC_PT + caly.residual / abs(caly.slope)

    marks = _markers(draws)
    table = _legend(draws, words, marks, plot_top)
    if sorted(g for g in table.values() if g) != sorted({g for gs in ITEMS.values() for g in gs}):
        raise ValueError(f"table groups {table}")

    series, skipped = {}, []
    for shape, fill, cx, cy, r in marks:
        if cy < plot_top:
            continue
        if (shape, fill) not in table:
            raise ValueError(f"plot marker {shape} {fill} at {cx:.1f}, {cy:.1f} is not in the table")
        g = table[(shape, fill)]
        ca = round(calx.value(cx) / X_STEP) * X_STEP
        if abs(calx.value(cx) - ca) > X_TOL:
            raise ValueError(f"{shape} {fill} marker at {calx.value(cx):.3f} mmol/L is not on a {X_STEP} step")
        ca = round(ca, 6)
        if g is None:                            # a class the table marks n.d.: drawn but not read
            skipped.append((shape, fill, ca))
            continue
        if ca in series.setdefault(g, {}):
            raise ValueError(f"two {g} markers at {ca} mmol/L")
        up, down = _bar_ends(draws, cx, cy, r, fill)
        if up is not None and down is not None and abs((cy - up) - (down - cy)) > SYM:
            raise ValueError(f"{g} at {ca}: error bar not symmetric ({cy - up:.2f} vs {down - cy:.2f} pt)")
        bar = {"mean": _triple(caly, cy, unc), "x": ca}
        end = up if up is not None else (2 * cy - down if down is not None else None)
        if end is not None:
            bar["error"] = _triple(caly, end, unc)
        series[g][ca] = bar
    steps = {g: sorted(s) for g, s in series.items()}
    if len({tuple(s) for s in steps.values()}) != 1:
        raise ValueError(f"series are not read at the same calcium concentrations: {steps}")

    groups = {}
    for item, gs in ITEMS.items():
        for g in gs:
            for ca, bar in series[g].items():
                groups[f"{item}/{g}_{ca:g}"] = {"points": [], "countable": False, "bar": bar}
    return {"groups": groups}
