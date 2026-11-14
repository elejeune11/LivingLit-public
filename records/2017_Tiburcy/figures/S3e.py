"""Suppl. Fig. 3e (supplement p. 44): normalized FOC (fold) of EHM cultured without growth factor (No GF), with IGF,
FGF, VEGF, TGFβ1 or all of them on d0-10, or with TGFβ1 on d0-3. One open bar per group (a group mean) with one upward
error bar; no single EHM is drawn, so every group is bar only (countable false). The Matrix Protocol EHM reference is
a black dashed line with a grey dashed line above and below it (its mean and error band).

The panel is vector. The y axis is one path (the axis line plus three tick stubs), calibrated from the stubs matched
in order to the printed labels left of it (0, 0.5, 1.0). Each bar is one white-filled, stroked path; its top is the
mean. Each error bar is one path: a horizontal cap and a vertical line from the cap down to the bar top; 'error' is
the cap. The line's base is checked to lie within 0.5 pt of its bar's top. Bars are named by the word under the x
axis whose centre lies within the bar; the two 'TGFβ1' bars (the β is not in the text layer) are told apart by the
'd0-10' rule (a horizontal line under IGF to ALL) and the 'd0-3' word under the bar right of the axis break.

The reference: the black dashed line is the mean; the grey dashed lines are rows of small grey filled rectangles,
read at their centre; 'error' is the upper grey line, and the lower one is checked to mirror it within the reading
uncertainty.

FGF is drawn but no item uses it. Labels are <item>/<group>; shared groups are repeated.
"""
from livinglit.figures.source import calibrate

UNC_PT = 0.5                                              # vector position uncertainty (pt)
TICKS = [0.0, 0.5, 1.0]
WORDS = {"No": "nogf", "IGF": "igf", "FGF": "fgf", "VEGF": "vegf", "ALL": "all"}
ITEMS = {"S3e_nogf_matrix": ["nogf", "matrix_ref"], "S3e_igf_matrix": ["igf", "matrix_ref"],
         "S3e_vegf_matrix": ["vegf", "matrix_ref"], "S3e_tgfb1_matrix": ["tgfb1", "matrix_ref"],
         "S3e_tgfb1_d03_matrix": ["tgfb1_d03", "matrix_ref"], "S3e_all_nogf": ["all", "nogf"]}
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
    if len(bars) != 7:
        raise ValueError(f"{len(bars)} bars")
    under = [w for w in words if w[1] > ax_bot]
    rule = [d["rect"] for d in draws if d.get("fill") is None and d["rect"].y0 > ax_bot + 5 and d["rect"].width > 100
            and d["rect"].height < 1]
    d03 = [w for w in under if w[4] == "d0-3"]
    if len(rule) != 1 or len(d03) != 1:
        raise ValueError(f"rule {rule}, d0-3 {d03}")
    named = {}
    for w in under:
        g = WORDS.get(w[4]) or ("tgfb1?" if w[4].startswith("TGF") else None)
        if g is None:
            continue
        xc = (w[0] + w[2]) / 2
        rs = [i for i, r in enumerate(bars) if r.x0 < xc < r.x1]
        if len(rs) != 1 or rs[0] in named:
            raise ValueError(f"{w[4]}: bars {rs}")
        r = bars[rs[0]]
        bc = (r.x0 + r.x1) / 2
        if g == "tgfb1?":
            in_rule = rule[0].x0 < bc < rule[0].x1
            in_d03 = d03[0][0] < bc < d03[0][2]
            if in_rule == in_d03:
                raise ValueError(f"TGF bar at {bc}: rule {in_rule}, d0-3 {in_d03}")
            g = "tgfb1" if in_rule else "tgfb1_d03"
        named[rs[0]] = g
    if sorted(named.values()) != sorted(list(WORDS.values()) + ["tgfb1", "tgfb1_d03"]):
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
        cap = [s for s in segs if abs(s[1] - s[3]) < 0.01 and abs(s[0] - s[2]) > 5]
        vert = [s for s in segs if abs(s[0] - s[2]) < 0.01 and abs(s[1] - s[3]) > 0.01]
        if len(cap) != 1 or len(vert) != 1 or abs(max(vert[0][1], vert[0][3]) - r.y0) > BASE_TOL \
                or abs(min(vert[0][1], vert[0][3]) - cap[0][1]) > 0.01:
            raise ValueError(f"{g}: cap {cap}, line {vert}, bar top {r.y0}")
        mean, err = cal.value(r.y0), cal.value(cap[0][1])
        read_bars[g] = {"mean": [mean, mean - unc, mean + unc], "error": [err, err - unc, err + unc]}

    # Matrix Protocol reference: black dashed line (mean) between two grey dashed lines (error band)
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
