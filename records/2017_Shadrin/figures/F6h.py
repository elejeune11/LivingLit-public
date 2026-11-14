"""Fig. 6h: Ca2+ transient amplitude (dF/F, norm.) of implanted cardiopatches at d7 and d14 (vector plot, one mean
marker ± SEM per day joined by a line, no individual points).

The y axis is a black drawing of short tick rectangles left of the axis line; each tick is matched to the nearest
numeric label just left of it. A mean marker is a filled, unstroked, non-black diamond (a path of 'l' items whose
first vertex is the top centre of its box); its slightly larger outline copy and the joining line start elsewhere and
are skipped. A marker's day is the nearest x-axis word (d7 / d14) below the axis; its mean is the box centre. An
error bar is a black drawing of a thin stem (width < 1 pt) and two short caps (height < 1 pt) centred on it, at the
marker's x; its upper end is the centre of the upper cap. Panel g (images and a time trace) has no group values.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate

LABELS = {"dff.d14": "d14", "dff.d7": "d7"}


def _black(d):
    return d.get("fill") is not None and max(d["fill"]) < 0.05


def _diamond(d):
    r = d["rect"]
    if d.get("fill") is None or d.get("color") is not None or _black(d):
        return False
    if not (3 < r.width < 6 and 3 < r.height < 6):
        return False
    items = d["items"]
    if not all(i[0] == "l" for i in items):
        return False
    p = items[0][1]
    return abs(p.x - (r.x0 + r.x1) / 2) < 0.1 and abs(p.y - r.y0) < 0.1


def _errbar(d):
    """(x, upper cap centre y, lower cap centre y) of a stem + two caps drawing, or None."""
    if not (_black(d) and len(d["items"]) == 3 and all(i[0] == "re" for i in d["items"])):
        return None
    rs = [i[1] for i in d["items"]]
    stems = [r for r in rs if r.width < 1 and r.height > 1]
    caps = sorted((r for r in rs if r.height < 1 and r.width > 2), key=lambda r: r.y0)
    if len(stems) != 1 or len(caps) != 2:
        return None
    xc = (stems[0].x0 + stems[0].x1) / 2
    assert all(abs((c.x0 + c.x1) / 2 - xc) < 0.2 for c in caps), "cap not centred on its stem"
    return xc, (caps[0].y0 + caps[0].y1) / 2, (caps[1].y0 + caps[1].y1) / 2


def read(fig):
    draws = fig.drawings()
    words = fig.words()
    unc = VECTOR_UNCERTAINTY_PT

    cal = None
    for d in draws:
        if not _black(d):
            continue
        ticks = [i[1] for i in d["items"] if i[0] == "re" and 2 < i[1].width < 4 and i[1].height < 1]
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
        assert cal is None, "two y axes"
        cal, bottom = calibrate(marks), max(r.y1 for r in ticks)
    assert cal is not None, "y axis not found"

    days = [((wx0 + wx1) / 2, t) for wx0, wy0, wx1, wy1, t in words if t in ("d7", "d14") and wy0 > bottom]
    assert sorted(t for _, t in days) == ["d14", "d7"], "day labels not found"
    bars = [b for b in (_errbar(d) for d in draws) if b is not None]
    means = {}
    for d in draws:
        if not _diamond(d):
            continue
        r = d["rect"]
        xc, yc = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
        day = min(days, key=lambda w: abs(w[0] - xc))[1]
        assert day not in means, "two markers for one day"
        means[day] = (xc, yc)
    assert len(means) == 2, "expected 2 mean markers"

    groups = {}
    for day, (xc, yc) in means.items():
        mine = [b for b in bars if abs(b[0] - xc) < 1]
        assert len(mine) == 1, "marker without exactly one error bar"
        _, up, lo = mine[0]
        assert up < yc < lo, "error bar does not straddle its mean"
        mlo, mhi = cal.interval(yc, unc)
        elo, ehi = cal.interval(up, unc)
        groups[day] = {"points": [], "countable": False,
                       "bar": {"mean": [cal.value(yc), mlo - cal.residual, mhi + cal.residual],
                               "error": [cal.value(up), elo - cal.residual, ehi + cal.residual]}}
    return {"groups": {label: groups[day] for label, day in LABELS.items()}}
