"""Fig. 4b: expression of MYOM3, CASQ2, S100A1 and COX6A2 in 0.5MM cardiopatches relative to 1MM (vector bar
chart, linear axis 0-2, mean + upper error bar, no individual points).

The y axis is a black drawing of short tick rectangles left of the axis line; each tick is matched to the
nearest numeric label just left of it. The x axis has category ticks (a black drawing of short vertical
rectangles) that bound one gene each; the genes are the rotated labels below the axis, taken in x order and
paired with the category intervals in x order. Bars are one-rectangle drawings with a coloured fill; the group of a
bar is the legend square of the same fill (small coloured squares followed by the 1MM/0.5MM words). An error bar is
a black drawing of exactly a thin stem (width < 1 pt) and a short cap (height < 1 pt, width < 6 pt) centred on the
stem; the cap's centre is the upper end. The 1MM bars (the reference, near 1) also carry error bars.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate

GENES = ["MYOM3", "CASQ2", "S100A1", "COX6A2"]
GROUP = {"1MM": "mm1", "0.5MM": "mm05"}


def _black(d):
    return d.get("fill") is not None and max(d["fill"]) < 0.05


def _coloured(d):
    f = d.get("fill")
    return f is not None and len(d["items"]) == 1 and d["items"][0][0] == "re" and 0.05 < max(f) and min(f) < 0.95


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
    cal = None
    cats = None
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
            cal = calibrate(marks)
        vt = [r for r in rects if r.width < 1 and 2.5 < r.height < 4]
        if len(vt) >= 3 and len(vt) == len(d["items"]):
            assert cats is None, "two sets of category ticks"
            cats = sorted((r.x0 + r.x1) / 2 for r in vt)
    assert cal is not None and cats is not None, "axes not found"
    labels = sorted((w for w in words if w[4] in GENES), key=lambda w: w[0])
    assert [w[4] for w in labels] == GENES and len(cats) == len(GENES) + 1, "gene labels and categories differ"
    legend = {}
    for d in draws:
        r = d["rect"]
        if _coloured(d) and r.width < 7 and r.height < 7:
            yc = (r.y0 + r.y1) / 2
            for x0, y0, x1, y1, t in words:
                if t in GROUP and 0 < x0 - r.x1 < 8 and abs((y0 + y1) / 2 - yc) < 2:
                    legend[tuple(round(c, 3) for c in d["fill"])] = GROUP[t]
    assert sorted(legend.values()) == ["mm05", "mm1"], "legend not found"
    caps = [c for c in (_cap(d) for d in draws) if c is not None]
    bars = [d for d in draws if _coloured(d) and d["rect"].height > 7]
    out = {}
    for gene, lo_x, hi_x in zip(GENES, cats, cats[1:]):
        mine = [d for d in bars if lo_x < (d["rect"].x0 + d["rect"].x1) / 2 < hi_x]
        groups = sorted(legend[tuple(round(c, 3) for c in d["fill"])] for d in mine)
        assert groups == ["mm05", "mm1"], f"{gene}: bars {groups}"
        for d in mine:
            r = d["rect"]
            group = legend[tuple(round(c, 3) for c in d["fill"])]
            xc = (r.x0 + r.x1) / 2
            cap = min(caps, key=lambda c: abs((c.x0 + c.x1) / 2 - xc))
            assert abs((cap.x0 + cap.x1) / 2 - xc) < 1, "error bar not centred on its bar"
            top, ce = r.y0, (cap.y0 + cap.y1) / 2
            mlo, mhi = cal.interval(top, unc)
            elo, ehi = cal.interval(ce, unc)
            out[f"{gene}.{group}"] = {"points": [], "countable": False,
                                      "bar": {"mean": [cal.value(top), mlo - cal.residual, mhi + cal.residual],
                                              "error": [cal.value(ce), elo - cal.residual, ehi + cal.residual]}}
    return {"groups": out}
