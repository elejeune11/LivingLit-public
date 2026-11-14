"""Suppl. Fig. 1e (supplement p. 40): fraction of CM (%) that are MLC2A single positive (green), MLC2A/V double positive
(grey) and MLC2V single positive (magenta), in input cells, undefined EHM and defined EHM. One stacked bar per group
(magenta at the base, grey above it, green on top, summing to 100%); each segment is a group mean with one upward error
bar. No single cell pool is drawn, so every group is bar only (countable false).

The panel is vector. The y axis is one path (a long vertical line plus tick stubs), calibrated from its stubs matched in
order to the printed labels 0, 50, 100. Series colours come from the legend: each legend word (MLC2A, MLC2A+V, MLC2V)
is matched to the filled swatch on its line. Bars are the filled shapes of a series colour below the legend's left edge;
columns are named from the words under the x axis (Input, Undef., Def.).

Segments are drawn as overlapping shapes (e.g. Input: grey ends at 615.02, magenta starts at 614.17), so each boundary
between two segments is the midpoint of the upper segment's bottom and the lower segment's top, with half their gap
added to its uncertainty; the bar base is the 0 tick and the bar top is the top of the green segment. A segment's mean
is the height between its two boundaries in axis units.

Each error bar is a T: a horizontal cap and a vertical line from the cap down to the segment's top. 'error' is the
segment's mean plus the T's length (cap to base), i.e. the bar's upper end in units of the segment's own fraction. The
T's base is checked to lie within 1.5 pt of the segment top it belongs to.

One bar is used by several record items (e.g. Undef. by S1e_dp_undef_input and S1e_dp_def_undef), and a figures.yaml
label links to one item, so each reading is returned once per item that uses it: label "<item>/<group>".
"""
from livinglit.figures.source import calibrate

UNC_PT = 0.5                                  # vector position uncertainty (pt)
TICKS = [0, 50, 100]                          # printed y tick labels, bottom to top: Fraction of CM (%)
SERIES = {"MLC2A": "a", "MLC2A+V": "dp", "MLC2V": "v"}           # legend word -> series
COLUMNS = {"Input": "input", "Undef.": "undef", "Def.": "def"}  # word under the x axis -> group
ITEMS = {"S1e_dp_undef_input": ("dp", ["undef", "input"]), "S1e_dp_def_input": ("dp", ["def", "input"]),
         "S1e_dp_def_undef": ("dp", ["def", "undef"]),
         "S1e_mlc2a": ("a", ["input", "undef", "def"]), "S1e_mlc2v": ("v", ["input", "undef", "def"])}
STACK = ["v", "dp", "a"]                      # bottom to top
COL_TOL = 0.02                                # fill colour match
BASE_TOL = 1.5                                # pt: T base to segment top


def _same(c1, c2):
    return c1 is not None and c2 is not None and max(abs(a - b) for a, b in zip(c1, c2)) <= COL_TOL


def _axis(fig):
    for d in fig.drawings():
        items = d["items"]
        if len(items) < 3 or any(it[0] != "l" for it in items):
            continue
        long = [it for it in items if abs(it[1].x - it[2].x) < 0.01 and abs(it[1].y - it[2].y) > 100]
        if len(long) == 1:
            stubs = [it[1].y for it in items if abs(it[1].y - it[2].y) < 0.01 and 0 < abs(it[1].x - it[2].x) < 6]
            return long[0][1].x, sorted(stubs, reverse=True)
    raise ValueError("no y axis path")


def _legend(fig):
    """Series -> (fill colour, legend left edge)."""
    out, swatches = {}, [d for d in fig.drawings() if d.get("fill") is not None and d["rect"].width > 5
                         and d["rect"].height > 5 and d["rect"].height < 10]
    for w in fig.words():
        if w[4] not in SERIES:
            continue
        cy = (w[1] + w[3]) / 2
        near = [d for d in swatches if d["rect"].x1 <= w[0] and d["rect"].y0 <= cy <= d["rect"].y1
                and d["fill"] not in ((1.0, 1.0, 1.0), (0.0, 0.0, 0.0))]
        fills = {tuple(round(c, 3) for c in d["fill"]) for d in near}
        if len(fills) != 1:
            raise ValueError(f"legend {w[4]}: swatch fills {fills}")
        out[SERIES[w[4]]] = (near[0]["fill"], min(d["rect"].x0 for d in near))
    if len(out) != 3:
        raise ValueError(f"legend series {sorted(out)}")
    return out


def read(fig):
    ax_x, stubs = _axis(fig)
    printed = sorted(float(w[4]) for w in fig.words() if w[2] < ax_x and w[4].isdigit())
    if printed != TICKS or len(stubs) != len(TICKS):
        raise ValueError(f"tick labels {printed}, {len(stubs)} stubs")
    cal = calibrate(list(zip(stubs, TICKS)))
    k = abs(cal.slope)
    mis = cal.residual / k                    # calibration misfit in pt
    zero = stubs[0]
    legend = _legend(fig)
    left_of_legend = min(x for _, x in legend.values())
    cols = {COLUMNS[w[4]]: (w[0] + w[2]) / 2 for w in fig.words() if w[4] in COLUMNS and w[1] > zero}
    if len(cols) != 3:
        raise ValueError(f"columns {cols}")
    draws = [d for d in fig.drawings() if ax_x < d["rect"].x0 and d["rect"].x1 < left_of_legend]
    ts = []                                   # error bar Ts: (x, cap y, base y)
    for d in draws:
        it = d["items"]
        if d.get("fill") is None and len(it) == 3 and all(i[0] == "l" for i in it):
            vert = [i for i in it if abs(i[1].x - i[2].x) < 0.01 and abs(i[1].y - i[2].y) > 0.01]
            horiz = [i for i in it if abs(i[1].y - i[2].y) < 0.01]
            if len(vert) == 1 and len(horiz) == 2:
                cap = horiz[0][1].y
                ys = (vert[0][1].y, vert[0][2].y)
                if abs(min(ys) - cap) > 0.01:
                    raise ValueError(f"T at {d['rect']}: cap not at the top")
                ts.append((vert[0][1].x, cap, max(ys)))
    bars = {}
    for g, cx in cols.items():
        seg = {}
        for s, (fill, _) in legend.items():
            rs = [d["rect"] for d in draws if _same(d.get("fill"), fill) and d["rect"].x0 < cx < d["rect"].x1]
            if len(rs) != 1:
                raise ValueError(f"{g} {s}: {len(rs)} segments")
            seg[s] = rs[0]
        # boundaries bottom to top: (position, half gap)
        bounds = [(zero, abs(seg["v"].y1 - zero) / 2)]
        for lo_s, up_s in zip(STACK, STACK[1:]):
            a, b = seg[lo_s].y0, seg[up_s].y1
            bounds.append(((a + b) / 2, abs(a - b) / 2))
        bounds.append((seg["a"].y0, 0.0))
        mine = [t for t in ts if all(r.x0 < t[0] < r.x1 for r in seg.values())]
        if len(mine) != 3:
            raise ValueError(f"{g}: {len(mine)} error bars")
        for i, s in enumerate(STACK):
            (yb, gb), (yt, gt) = bounds[i], bounds[i + 1]
            mean = (yb - yt) * k
            unc = (2 * (UNC_PT + mis) + gb + gt) * k
            t = [t for t in mine if abs(t[2] - yt) <= BASE_TOL]
            if len(t) != 1:
                raise ValueError(f"{g} {s}: error bars at segment top {t}")
            length = (t[0][2] - t[0][1]) * k
            lunc = 2 * (UNC_PT + mis) * k
            bars[(s, g)] = {"points": [], "countable": False,
                            "bar": {"mean": [mean, mean - unc, mean + unc],
                                    "error": [mean + length, mean + length - unc - lunc, mean + length + unc + lunc]}}
    groups = {}
    for item, (s, gs) in ITEMS.items():
        for g in gs:
            groups[f"{item}/{g}"] = bars[(s, g)]
    return {"groups": groups}
