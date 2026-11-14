"""Supplementary Fig. 11A, B: expression of ten maturation genes in 3-week cardiopatches relative to d0 hiPSC-CMs (A)
and to age-matched 2D monolayers (B) (vector grouped bar charts, mean + upper SEM bar, no individual points).

Each row (A, B) has three y axes. An axis is a grey drawing of short horizontal tick lines (about 3 pt) on the axis
line, each matched to the numeric label just left of it (labels end in "!" in this PDF's text layer). Its row is the
row whose rotated y-axis title ("Expression rel. to d0" / "... to monolayer") overlaps it vertically. The x axis is a
grey baseline from the axis with a drawing of short vertical ticks at the category boundaries; a bar's category is
the slot between two such ticks. Bars are 're' items of filled drawings whose bottom sits on the baseline; the group
of a bar is the legend square of the same fill in that row (small square followed by the Patch/d0/Monolayer word).
An error bar is a filled drawing of two lines, a vertical stem rising from the bar top and a horizontal cap; the
cap's height is the upper end (zero-length stems are drawn for bars with a tiny SEM).

The gene names under the bars are drawn as glyph outlines, not text, so they cannot be read by code; the order
below is the printed left-to-right order (the same in A and B, and the order of Supplementary Tables 3-4). The
script asserts that each axis has exactly that many categories, each holding one bar per group.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate

GREY = 0.596
ROWS = {"Expression,rel.,to,d0,": "patch_vs_d0", "Expression,rel.,to,monolayer,": "patch_vs_mono"}
WORD_GROUP = {"Patch": "patch", "d0": "d0", "Monolayer": "mono"}
GENES = [["TNNI3", "MYL2", "MYOM2", "MYOM3"], ["CASQ2", "S100A1", "PLN"], ["COX6A2", "CKMT2", "CKM"]]
ROW_GROUPS = {"patch_vs_d0": ("patch", "d0"), "patch_vs_mono": ("patch", "mono")}


def _grey(d):
    c = d.get("color")
    return d.get("fill") is None and c is not None and all(abs(v - GREY) < 0.01 for v in c)


def _lines(d):
    return [i for i in d["items"] if i[0] == "l"] if d["items"] and all(i[0] == "l" for i in d["items"]) else []


def _key(fill):
    return tuple(round(c, 3) for c in fill)


def read(fig):
    draws = fig.drawings()
    words = fig.words()
    unc = VECTOR_UNCERTAINTY_PT

    titles = [(ROWS[w[4]], w[1], w[3]) for w in words if w[4] in ROWS]
    assert len(titles) == 2, "row titles not found"

    # y axes: grey drawings of >= 3 short horizontal tick lines
    axes = []
    for d in draws:
        ls = _lines(d)
        if _grey(d) and len(ls) >= 3 and all(abs(a.y - b.y) < 0.01 and 2 < abs(b.x - a.x) < 4 for _, a, b in ls):
            x0 = min(min(a.x, b.x) for _, a, b in ls)
            x1 = max(max(a.x, b.x) for _, a, b in ls)
            nums = [((w[1] + w[3]) / 2, _num(w[4])) for w in words if _isnum(w[4]) and 0 < x0 - w[2] < 6]
            marks = []
            for _, a, _b in ls:
                cands = [v for pos, v in nums if abs(pos - a.y) < 2]
                assert len(cands) == 1, "tick without a single label"
                marks.append((a.y, cands[0]))
            top, bottom = min(m[0] for m in marks), max(m[0] for m in marks)
            over = [(min(bottom, t1) - max(top, t0), row) for row, t0, t1 in titles]
            ov, row = max(over)
            assert ov > 0, "axis outside both rows"
            axes.append({"row": row, "x": x1, "bottom": bottom, "cal": calibrate(marks)})
    assert len(axes) == 6, f"expected 6 y axes, found {len(axes)}"

    for ax in axes:
        base = [(a, b) for d in draws if _grey(d) and len(_lines(d)) == 1
                for _, a, b in _lines(d) if abs(a.y - b.y) < 0.01 and abs(a.x - ax["x"]) < 0.5 and b.x - a.x > 20]
        assert len(base) == 1, "x-axis baseline not found"
        ax["y0"], ax["x1"] = base[0][0].y, base[0][1].x
        ticks = [d for d in draws if _grey(d) and len(_lines(d)) >= 3
                 and all(abs(a.x - b.x) < 0.01 and abs(min(a.y, b.y) - ax["y0"]) < 0.3 for _, a, b in _lines(d))
                 and abs(min(a.x for _, a, _b in _lines(d)) - ax["x"]) < 0.5]
        assert len(ticks) == 1, "category ticks not found"
        ax["slots"] = sorted(a.x for _, a, _b in _lines(ticks[0]))
    axes.sort(key=lambda a: (a["row"], a["x"]))

    # legend: small filled squares with a group word just right of them, per row
    legend = {}
    squares = []
    for d in draws:
        if d.get("fill") is None or len(d["items"]) != 1 or d["items"][0][0] != "re":
            continue
        r = d["rect"]
        if 4 < r.width < 7 and 4 < r.height < 7:
            yc = (r.y0 + r.y1) / 2
            for x0, y0, x1, y1, t in words:
                if t.rstrip("!") in WORD_GROUP and 0 < x0 - r.x1 < 8 and abs((y0 + y1) / 2 - yc) < 3:
                    row = [row for row, t0, t1 in titles if t0 - 15 < yc < t1][0]
                    legend[(row, _key(d["fill"]))] = WORD_GROUP[t.rstrip("!")]
                    squares.append(tuple(r))

    stems = []  # (x, bottom, cap y) of filled stem + cap drawings
    for d in draws:
        ls = _lines(d)
        if d.get("fill") is None or len(ls) != 2:
            continue
        v = [(a, b) for _, a, b in ls if abs(a.x - b.x) < 0.05]
        h = [(a, b) for _, a, b in ls if abs(a.y - b.y) < 0.05 and abs(a.x - b.x) > 1]
        if len(v) == 1 and len(h) == 1:
            (a, b), (c, e) = v[0], h[0]
            assert abs((c.x + e.x) / 2 - a.x) < 0.4 and abs(c.y - min(a.y, b.y)) < 0.05
            stems.append((a.x, max(a.y, b.y), c.y))

    out = {}
    for ax_i, ax in enumerate(axes):
        genes = GENES[ax_i % 3]
        assert len(ax["slots"]) == len(genes) + 1, "category count differs from the gene list"
        cal = ax["cal"]
        seen = set()
        for d in draws:
            f = d.get("fill")
            if f is None or (ax["row"], _key(f)) not in legend:
                continue
            for it in d["items"]:
                if it[0] != "re":
                    continue
                r = it[1]
                if tuple(r) in squares or not (ax["x"] < r.x0 and r.x1 < ax["x1"] and abs(r.y1 - ax["y0"]) < 0.3):
                    continue
                group = legend[(ax["row"], _key(f))]
                xc = (r.x0 + r.x1) / 2
                k = [i for i in range(len(genes)) if ax["slots"][i] < xc < ax["slots"][i + 1]]
                assert len(k) == 1, "bar outside a category slot"
                gene = genes[k[0]]
                assert (gene, group) not in seen, "two bars of one group in a category"
                seen.add((gene, group))
                sx, sbottom, ce = min(stems, key=lambda s: abs(s[0] - xc) + abs(s[1] - r.y0))
                assert abs(sx - xc) < 1 and abs(sbottom - r.y0) < 0.2, "error bar not on its bar"
                top = r.y0
                mlo, mhi = cal.interval(top, unc)
                elo, ehi = cal.interval(ce, unc)
                out[f"{gene}.{ax['row']}.{group}"] = {
                    "points": [], "countable": False,
                    "bar": {"mean": [cal.value(top), mlo - cal.residual, mhi + cal.residual],
                            "error": [cal.value(ce), elo - cal.residual, ehi + cal.residual]}}
        assert len(seen) == 2 * len(genes) and {g for _, g in seen} == set(ROW_GROUPS[ax["row"]]), \
            "each category needs one bar per group"
    return {"groups": out}


def _isnum(t):
    try:
        _num(t)
        return True
    except ValueError:
        return False


def _num(t):
    return float(t.rstrip("!").replace("−", "-"))
