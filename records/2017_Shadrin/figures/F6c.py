"""Fig. 6c: blood vessel density (BVD, A.U.) of cardiopatches and blanks at d7 and d14 post implantation
(vector line plot, one mean marker ± SEM per series and day, no individual points).

The y axis is a black drawing of short tick rectangles left of the axis line; each tick is matched to the nearest
numeric label just left of it. Series are told apart by marker shape: a square (one 're' item) and a diamond (a
filled path whose first vertex is the top centre of its box). Each shape is named by the legend word just right
of its legend copy (the copy above the axis top). A plotted marker's day is the nearest x-axis word (d7 / d14)
below the axis; its mean is the marker box centre. An error bar is a black drawing of a thin stem (width < 1 pt)
and two short caps (height < 1 pt) centred on it; it belongs to the marker at its x whose centre is nearest the
bar's midpoint, and its upper end is the centre of the upper cap.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate

SERIES = {"Cardiopatch": "patch", "Blank": "blank"}
LABELS = {
    "time.patch_d14": ("patch", "d14"),
    "time.blank_d14": ("blank", "d14"),
    "time.patch_d7": ("patch", "d7"),
    "time.blank_d7": ("blank", "d7"),
    "interaction.patch_d7": ("patch", "d7"),
    "interaction.patch_d14": ("patch", "d14"),
    "interaction.blank_d7": ("blank", "d7"),
    "interaction.blank_d14": ("blank", "d14"),
    "d14_vs_d7.patch_d14": ("patch", "d14"),
    "d14_vs_d7.patch_d7": ("patch", "d7"),
    "patch_vs_blank.patch_d14": ("patch", "d14"),
    "patch_vs_blank.blank_d14": ("blank", "d14"),
}


def _black(d):
    return d.get("fill") is not None and max(d["fill"]) < 0.05


def _shape(d):
    """'square' or 'diamond' for a filled marker body without stroke, else None."""
    r = d["rect"]
    if d.get("fill") is None or d.get("color") is not None or _black(d):
        return None
    if not (3 < r.width < 4.5 and 3 < r.height < 4.5):
        return None
    items = d["items"]
    if len(items) == 1 and items[0][0] == "re":
        return "square"
    if items[0][0] == "l":
        p = items[0][1]
        if abs(p.x - (r.x0 + r.x1) / 2) < 0.1 and abs(p.y - r.y0) < 0.1:
            return "diamond"
    return None


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
        cal, top, bottom = calibrate(marks), min(r.y0 for r in ticks), max(r.y1 for r in ticks)
    assert cal is not None, "y axis not found"

    shapes = [(s, d["rect"]) for s, d in ((_shape(d), d) for d in draws) if s]
    names, plotted = {}, []
    for s, r in shapes:
        yc = (r.y0 + r.y1) / 2
        if r.y1 < top:  # legend copy
            right = [(wx0, t) for wx0, wy0, wx1, wy1, t in words if t in SERIES and wy0 < yc < wy1 and wx0 > r.x1]
            assert len(right) == 1, "legend marker without its word"
            assert s not in names, "two legend entries with one shape"
            names[s] = SERIES[right[0][1]]
        else:
            plotted.append((s, r))
    assert sorted(names.values()) == ["blank", "patch"]

    days = [((wx0 + wx1) / 2, t) for wx0, wy0, wx1, wy1, t in words if t in ("d7", "d14") and wy0 > bottom]
    bars = [b for b in (_errbar(d) for d in draws) if b is not None]
    out = {}
    for s, r in plotted:
        xc, yc = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
        day = min(days, key=lambda w: abs(w[0] - xc))[1]
        key = (names[s], day)
        assert key not in out, "two markers for one series and day"
        out[key] = (xc, yc)
    assert len(out) == 4, "expected 4 plotted markers"

    groups = {}
    for key, (xc, yc) in out.items():
        same_x = [k for k, (x, _) in out.items() if abs(x - xc) < 1]
        mine = []
        for bx, up, lo in bars:
            if abs(bx - xc) > 1:
                continue
            mid = (up + lo) / 2
            if min(same_x, key=lambda k: abs(out[k][1] - mid)) == key:
                mine.append(up)
        assert len(mine) == 1, "marker without exactly one error bar"
        mlo, mhi = cal.interval(yc, unc)
        elo, ehi = cal.interval(mine[0], unc)
        groups[key] = {"points": [], "countable": False,
                       "bar": {"mean": [cal.value(yc), mlo - cal.residual, mhi + cal.residual],
                               "error": [cal.value(mine[0]), elo - cal.residual, ehi + cal.residual]}}
    return {"groups": {label: groups[key] for label, key in LABELS.items()}}
