"""Fig. 5e, f: conduction velocity and APD80 of 3-week ctrl, Mega and Giga cardiopatches (two vector bar charts,
mean + upper SEM bar, no individual points).

Each panel's y axis is a black drawing of short tick rectangles left of the axis line; each tick is matched to
the nearest numeric label just left of it. The panel is named by its rotated y-axis title (CV / APD80) left of
the ticks. Only the Ctrl bar is read (the item groups no text gives): it is the one-rectangle solid fill above
the rotated word "Ctrl"; Mega and Giga are hatched outlines whose means are printed in the Results. The bar's
fill top is the centre of its outline stroke and the bottom of its error bar's stem. An error bar is a black
drawing of exactly a thin stem (width < 1 pt) and a short cap (height < 1 pt, width < 6 pt) centred on the stem;
the cap's centre is the upper end.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate

TITLES = {"CV": "cv", "APD80": "apd"}
LABELS = {"cv.ctrl": ("cv", "Ctrl"), "apd.ctrl": ("apd", "Ctrl")}


def _black(d):
    return d.get("fill") is not None and max(d["fill"]) < 0.05


def _solid(d):
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
    axes = []  # (x of tick column, panel, calibration)
    for d in draws:
        if not _black(d):
            continue
        ticks = [i[1] for i in d["items"] if i[0] == "re" and 2.5 < i[1].width < 4 and i[1].height < 1]
        if len(ticks) < 3:
            continue
        x0 = min(r.x0 for r in ticks)
        nums = fig.tick_marks("y", near=x0 - 7, tol=6)
        marks = []
        for r in ticks:
            y = (r.y0 + r.y1) / 2
            pos, v = min(nums, key=lambda m: abs(m[0] - y))
            if abs(pos - y) < 2:
                marks.append((y, v))
        assert len(marks) == len(ticks), "a tick without its label"
        titles = [TITLES[t] for wx0, wy0, wx1, wy1, t in words if t in TITLES and 0 < x0 - wx1 < 30]
        assert len(titles) == 1, "panel title not found"
        axes.append((x0, titles[0], calibrate(marks)))
    assert sorted(a[1] for a in axes) == ["apd", "cv"]
    caps = [c for c in (_cap(d) for d in draws) if c is not None]
    bars = {}
    for d in draws:
        r = d["rect"]
        if not (_solid(d) and r.height > 7):
            continue
        xc = (r.x0 + r.x1) / 2
        names = [t for wx0, wy0, wx1, wy1, t in words if wx0 < xc < wx1 and 0 < wy0 - r.y1 < 10]
        assert len(names) == 1, "bar without its category word"
        x0, panel, cal = max((a for a in axes if a[0] < r.x0), key=lambda a: a[0])
        cap = min(caps, key=lambda c: abs((c.x0 + c.x1) / 2 - xc))
        assert abs((cap.x0 + cap.x1) / 2 - xc) < 1, "error bar not centred on its bar"
        top, ce = r.y0, (cap.y0 + cap.y1) / 2
        mlo, mhi = cal.interval(top, unc)
        elo, ehi = cal.interval(ce, unc)
        bars[(panel, names[0])] = {"points": [], "countable": False,
                                   "bar": {"mean": [cal.value(top), mlo - cal.residual, mhi + cal.residual],
                                           "error": [cal.value(ce), elo - cal.residual, ehi + cal.residual]}}
    return {"groups": {label: bars[key] for label, key in LABELS.items()}}
