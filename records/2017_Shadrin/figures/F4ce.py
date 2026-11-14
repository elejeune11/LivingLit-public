"""Fig. 4c and 4e: protein/DNA ratio (c) and βMHC, SAA, Cx43 and GAPDH protein relative to LamB1 (e) in 1MM and
0.5MM cardiopatches (vector bar charts, linear axes, mean + upper error bar, no individual points).

The crop spans panels c, d and e. Each panel has its own y axis: a black drawing of short tick rectangles left of
the axis line, each tick matched to the nearest numeric label just left of it. Each panel has a black drawing of
short vertical category ticks below its x axis; panel c has one category (protein/DNA), panel e four, named by the
rotated gene labels in x order. The panel of a bar is the panel whose category ticks span it. Bars are
one-rectangle drawings with a fill; the group of a bar is the legend square of the same fill (panel e's legend,
small squares followed by d0/1MM/0.5MM; panel c has no legend of its own and uses the same fills). The d0 (white)
bars of panel e enter no item and are not returned. An error bar is a black drawing of exactly a thin stem
(width < 1 pt) and a short cap (height < 1 pt, width < 6 pt) centred on the stem; the cap's centre is the upper end.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate

GENES = {"βMHC": "bMHC", "SAA": "SAA", "Cx43": "Cx43", "GAPDH": "gapdh"}
GROUP = {"d0": "d0", "1MM": "mm1", "0.5MM": "mm05"}


def _black(d):
    return d.get("fill") is not None and max(d["fill"]) < 0.05


def _filled(d):
    return d.get("fill") is not None and len(d["items"]) == 1 and d["items"][0][0] == "re" and not _black(d)


def _key(d):
    return tuple(round(c, 3) for c in d["fill"])


def _cap(d):
    """The cap rectangle of a stem + cap error bar drawing, or None."""
    if not (_black(d) and len(d["items"]) == 2 and all(i[0] == "re" for i in d["items"])):
        return None
    a, b = (i[1] for i in d["items"])
    stem, cap = (a, b) if a.width < b.width else (b, a)
    if stem.width < 1 and stem.height > cap.height and cap.height < 1 and cap.width < 6 \
            and abs((stem.x0 + stem.x1) / 2 - (cap.x0 + cap.x1) / 2) < 0.2:
        return cap
    return None


def read(fig):
    draws = fig.drawings()
    words = fig.words()
    unc = VECTOR_UNCERTAINTY_PT
    axes, cats = [], []
    for d in draws:
        if not _black(d):
            continue
        rects = [i[1] for i in d["items"] if i[0] == "re"]
        ticks = [r for r in rects if 2.5 < r.width < 4 and r.height < 1]
        if len(ticks) >= 3 and len(ticks) == len(d["items"]):
            x0 = min(r.x0 for r in ticks)
            nums = fig.tick_marks("y", near=x0 - 7, tol=5)
            marks = []
            for r in ticks:
                y = (r.y0 + r.y1) / 2
                pos, v = min(nums, key=lambda m: abs(m[0] - y))
                if abs(pos - y) < 2:
                    marks.append((y, v))
            assert len(marks) == len(ticks), "a y tick without a label"
            axes.append((x0, calibrate(marks)))
        vt = [r for r in rects if r.width < 1 and 2.5 < r.height < 4]
        if len(vt) >= 2 and len(vt) == len(d["items"]):
            cats.append(sorted((r.x0 + r.x1) / 2 for r in vt))
    axes.sort()
    # a panel's first category tick sits on its y-axis line, just right of the y ticks
    cats = sorted(c for c in cats if any(0 < c[0] - x0 < 4 for x0, _ in axes))
    assert len(axes) == 2 and len(cats) == 2, f"expected two panels, found {len(axes)} y axes, {len(cats)} x axes"
    (_, cal_c), (_, cal_e) = axes
    cats_c, cats_e = cats
    assert len(cats_c) == 2 and len(cats_e) == len(GENES) + 1, "category ticks differ from one + four genes"
    # panel d's blot labels carry the same gene names, left of panel e's categories
    labels = sorted((w for w in words if w[4] in GENES and cats_e[0] < (w[0] + w[2]) / 2 < cats_e[-1]),
                    key=lambda w: w[0])
    assert [w[4] for w in labels] == list(GENES), f"gene labels {[w[4] for w in labels]}"
    legend = {}
    for d in draws:
        r = d["rect"]
        if _filled(d) and r.width < 7 and r.height < 7:
            yc = (r.y0 + r.y1) / 2
            for x0, y0, x1, y1, t in words:
                if t in GROUP and 0 < x0 - r.x1 < 8 and abs((y0 + y1) / 2 - yc) < 2:
                    legend[_key(d)] = GROUP[t]
    assert sorted(legend.values()) == ["d0", "mm05", "mm1"], f"legend not found: {legend}"
    caps = [c for c in (_cap(d) for d in draws) if c is not None]
    bars = [d for d in draws if _filled(d) and d["rect"].height > 7 and _key(d) in legend]
    panels = [("proteindna", cal_c, cats_c[0], cats_c[1], ["mm05", "mm1"])]
    panels += [(GENES[g], cal_e, lo, hi, ["d0", "mm05", "mm1"]) for g, lo, hi in zip(GENES, cats_e, cats_e[1:])]
    out = {}
    for name, cal, lo_x, hi_x, expect in panels:
        mine = [d for d in bars if lo_x < (d["rect"].x0 + d["rect"].x1) / 2 < hi_x]
        groups = sorted(legend[_key(d)] for d in mine)
        assert groups == expect, f"{name}: bars {groups}"
        for d in mine:
            group = legend[_key(d)]
            if group == "d0":
                continue
            r = d["rect"]
            xc = (r.x0 + r.x1) / 2
            cap = min(caps, key=lambda c: abs((c.x0 + c.x1) / 2 - xc))
            assert abs((cap.x0 + cap.x1) / 2 - xc) < 1, "error bar not centred on its bar"
            top, ce = r.y0, (cap.y0 + cap.y1) / 2
            mlo, mhi = cal.interval(top, unc)
            elo, ehi = cal.interval(ce, unc)
            out[f"{name}.{group}"] = {"points": [], "countable": False,
                                      "bar": {"mean": [cal.value(top), mlo - cal.residual, mhi + cal.residual],
                                              "error": [cal.value(ce), elo - cal.residual, ehi + cal.residual]}}
    return {"groups": out}
