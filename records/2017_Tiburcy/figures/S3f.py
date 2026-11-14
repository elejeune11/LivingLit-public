"""Suppl. Fig. 3f (supplement p. 44): normalized FOC (fold) of EHM cultured with 2% or 4% full B27, 4% B27 without
antioxidants (-AO) or 4% B27 without insulin. One open bar per group (a group mean) with one upward error bar; no single
EHM is drawn, so every group is bar only (countable false). The Matrix Protocol EHM reference is a dark dashed line
with a grey dashed line above and below it (its mean and error band).

The panel is vector. The y axis is one path (the axis line plus three tick stubs), calibrated from the stubs matched
in order to the printed labels left of it (0, 0.5, 1.0). Each bar is one white-filled, stroked path; its top is the
mean. Each error bar is one path: a horizontal cap and a vertical line from the cap down to the bar top; 'error' is
the cap. The line's base is checked to lie within 0.5 pt of its bar's top. Bars are named from the words under the x
axis whose centre lies within the bar: the percentage ('2%', '4%') and, for two of the 4% bars, '-AO' or '-insulin'.

The reference: the dashed line is the mean; the grey dashed lines are rows of small grey filled rectangles, read at
their centre; 'error' is the upper grey line, and the lower one is checked to mirror it within the reading
uncertainty.

-AO is drawn but no item uses it. Labels are <item>/<group>; shared groups are repeated.
"""
from livinglit.figures.source import calibrate

UNC_PT = 0.5                                              # vector position uncertainty (pt)
TICKS = [0.0, 0.5, 1.0]
ITEMS = {"S3f_b27_2_matrix": ["b27_2", "matrix_ref"], "S3f_b27_4_matrix": ["b27_4", "matrix_ref"],
         "S3f_ins_b27_2": ["b27_ins", "b27_2"], "S3f_ins_b27_4": ["b27_ins", "b27_4"]}
NAMES = {("2%", None): "b27_2", ("4%", None): "b27_4", ("4%", "-AO"): "b27_ao", ("4%", "-insulin"): "b27_ins"}
BASE_TOL = 0.5                                            # pt: error line base to bar top
WHITE, BLACK = (1.0, 1.0, 1.0), (0.0, 0.0, 0.0)


def _segs(d):
    return [(i[1].x, i[1].y, i[2].x, i[2].y) for i in d["items"] if i[0] == "l"]


def read(fig):
    draws = fig.drawings()
    words = fig.words()
    # y axis: the stroked path holding one long vertical line and short horizontal stubs left of it
    axes = []
    for d in draws:
        s = _segs(d)
        if d.get("fill") is None and s and len(s) == len(d["items"]):
            long_v = [g for g in s if abs(g[0] - g[2]) < 0.01 and abs(g[1] - g[3]) > 100]
            if len(long_v) == 1:
                axes.append((long_v[0], [g for g in s if abs(g[1] - g[3]) < 0.01 and 0 < abs(g[0] - g[2]) < 6]))
    if len(axes) != 1:
        raise ValueError(f"y axes {axes}")
    (ax_x, _, _, _), stubs = axes[0]
    stub_y = sorted((g[1] for g in stubs if max(g[0], g[2]) <= ax_x + 0.01), reverse=True)
    ax_bot = stub_y[0]
    printed = sorted(float(w[4]) for w in words if ax_x - 25 < w[2] < ax_x and w[4].replace(".", "").isdigit())
    if printed != TICKS or len(stub_y) != len(TICKS):
        raise ValueError(f"tick labels {printed}, stubs {stub_y}")
    cal = calibrate(list(zip(stub_y, TICKS)))
    k = abs(cal.slope)
    unc = (UNC_PT + cal.residual / k) * k

    bars = sorted((d["rect"] for d in draws if d.get("fill") == WHITE and d.get("color") == BLACK
                   and d["rect"].width > 15 and abs(d["rect"].y1 - ax_bot) < 0.5), key=lambda r: r.x0)
    if len(bars) != 4:
        raise ValueError(f"{len(bars)} bars")
    under = [w for w in words if w[1] > ax_bot]
    named = {}
    for i, r in enumerate(bars):
        inside = [w[4] for w in under if r.x0 < (w[0] + w[2]) / 2 < r.x1]
        pct = [t for t in inside if t in ("2%", "4%")]
        mod = [t for t in inside if t.startswith("-")]
        if len(pct) != 1 or len(mod) > 1 or "B27" not in inside:
            raise ValueError(f"bar {i}: words {inside}")
        key = (pct[0], mod[0] if mod else None)
        if key not in NAMES:
            raise ValueError(f"bar {i}: label {key}")
        named[i] = NAMES[key]
    if sorted(named.values()) != sorted(NAMES.values()):
        raise ValueError(f"bar labels {named}")

    errs = [d for d in draws if d.get("fill") is None and d.get("color") == BLACK and len(_segs(d)) == 3
            and len(d["items"]) == 3 and d["rect"].y1 < ax_bot]
    read_bars = {}
    for i, g in named.items():
        r = bars[i]
        e = [d for d in errs if r.x0 < (d["rect"].x0 + d["rect"].x1) / 2 < r.x1]
        if len(e) != 1:
            raise ValueError(f"{g}: error paths {e}")
        segs = _segs(e[0])
        # the cap may be drawn as two collinear horizontal segments (across, then back to the centre)
        horiz = [s for s in segs if abs(s[1] - s[3]) < 0.01]
        cap = [s for s in horiz if abs(s[0] - s[2]) > 5]
        vert = [s for s in segs if abs(s[0] - s[2]) < 0.01 and abs(s[1] - s[3]) > 0.01]
        if len(cap) < 1 or len(vert) != 1 or len(horiz) + len(vert) != len(segs) \
                or max(h[1] for h in horiz) - min(h[1] for h in horiz) > 0.01 or abs(max(vert[0][1], vert[0][3]) - r.y0) > BASE_TOL \
                or abs(min(vert[0][1], vert[0][3]) - cap[0][1]) > 0.01:
            raise ValueError(f"{g}: cap {cap}, line {vert}, bar top {r.y0}")
        mean, err = cal.value(r.y0), cal.value(cap[0][1])
        read_bars[g] = {"mean": [mean, mean - unc, mean + unc], "error": [err, err - unc, err + unc]}

    # Matrix Protocol reference: dashed line (mean) between two grey dashed lines (error band)
    dashed = [d for d in draws if d.get("fill") is None and d.get("dashes") not in (None, "", "[] 0")
              and d["rect"].height < 0.01 and d["rect"].width > 100]
    greys = sorted((d["rect"] for d in draws if d.get("color") is None and d.get("fill") not in (None, WHITE, BLACK)
                    and d["rect"].width > 100 and d["rect"].height < 1 and len(d["items"]) > 20), key=lambda r: r.y0)
    if len(dashed) != 1 or len(greys) != 2:
        raise ValueError(f"reference: dashed {dashed}, grey {greys}")
    ref = cal.value(dashed[0]["rect"].y0)
    hi, lo = (cal.value((r.y0 + r.y1) / 2) for r in greys)
    if abs((hi - ref) - (ref - lo)) > 2 * unc:
        raise ValueError(f"reference band not symmetric: {lo}, {ref}, {hi}")
    read_bars["matrix_ref"] = {"mean": [ref, ref - unc, ref + unc], "error": [hi, hi - unc, hi + unc]}

    groups = {}
    for item, gs in ITEMS.items():
        for g in gs:
            groups[f"{item}/{g}"] = {"points": [], "countable": False, "bar": read_bars[g]}
    return {"groups": groups}
