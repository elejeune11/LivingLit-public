"""Fig. 7f: host epicardial CV and APD80 in control hearts, under and away from the implanted cardiopatch (vector bar
chart of mean ± SEM on one shared y axis printed "CV (cm/s) or APD80 (ms)", no individual points).

The y axis is a black drawing of short tick rectangles left of the axis line; each tick is matched to the nearest
numeric label just left of it. Each bar is a black outline drawn as a filled ring (outer and inner edge); its top edge
is two horizontal segments of bar width, and the bar's value is the midline between them. One bar (Under patch, APD)
has its outline baked into an embedded hatch image; its top is taken where its vector error stem ends, which on the
five vector bars lies within 0.1 pt of the outline midline, and a dark outline row on the render is required there
(a check only). Ctrl bars also carry a red
're' fill; the hatched bars' fill is not a vector object. A bar's measure is the nearest x-axis word (CV / APD) below
the axis. Within a measure the bars are named from the legend: the bar with a red 're' fill is Ctrl, and each hatched
bar is matched to the legend swatch (Under patch / Away from patch) whose hatch runs the same diagonal way, judged on a
render by how well the red/white mask matches itself shifted along each diagonal. An error bar is a black drawing of a
thin stem (width < 1 pt) and one cap (height < 1 pt) above the bar, at the bar's x; its upper end is the cap centre.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate

LABELS = {"cv.control": ("CV", "control"), "cv.under": ("CV", "under"), "cv.away": ("CV", "away"),
          "apd.control": ("APD", "control"), "apd.under": ("APD", "under"), "apd.away": ("APD", "away")}
LEGEND = {"Ctrl": "control", "Under": "under", "Away": "away"}


def _black(d):
    return d.get("fill") is not None and max(d["fill"]) < 0.05


def _red(d):
    f = d.get("fill")
    return f is not None and f[0] > 0.9 and f[1] < 0.1 and f[2] < 0.1


def _errbar(d):
    """(x, cap centre y, stem bottom y) of a stem + one cap drawing, or None."""
    if not (_black(d) and len(d["items"]) == 2 and all(i[0] == "re" for i in d["items"])):
        return None
    rs = [i[1] for i in d["items"]]
    stems = [r for r in rs if r.width < 1 and r.height > 1]
    caps = [r for r in rs if r.height < 1 and 2 < r.width < 6]
    if len(stems) != 1 or len(caps) != 1:
        return None
    xc = (stems[0].x0 + stems[0].x1) / 2
    assert abs((caps[0].x0 + caps[0].x1) / 2 - xc) < 0.2, "cap not centred on its stem"
    return xc, (caps[0].y0 + caps[0].y1) / 2, stems[0].y1


def _diagonal(img, scale, crop, box):
    """+1 if the red/white hatch in box (page pt) runs '/', -1 if '\\'."""
    x0, y0, x1, y1 = box
    a = img[int((y0 - crop[1]) * scale):int((y1 - crop[1]) * scale),
            int((x0 - crop[0]) * scale):int((x1 - crop[0]) * scale)]
    m = a[:, :, 1] < 128
    score = 0.0
    for k in (2, 3, 4):
        back = (m[:-k, :-k] == m[k:, k:]).mean()
        fwd = (m[:-k, k:] == m[k:, :-k]).mean()
        score += fwd - back
    assert abs(score) > 0.5, "hatch direction unclear"
    return 1 if score > 0 else -1


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
        cal, bottom, axis_x = calibrate(marks), max(r.y1 for r in ticks), max(r.x1 for r in ticks)
    assert cal is not None, "y axis not found"

    # bar tops: horizontal segments of bar width in black outline drawings right of the axis, above the baseline
    tops = {}
    for d in draws:
        if not _black(d):
            continue
        for it in d["items"]:
            if it[0] != "l":
                continue
            p, q = it[1], it[2]
            if abs(p.y - q.y) < 0.01 and 7 < abs(p.x - q.x) < 8 and min(p.x, q.x) > axis_x and p.y < bottom - 2:
                xc = round((p.x + q.x) / 2)
                tops.setdefault(xc, []).append(p.y)
    errs = [b for b in (_errbar(d) for d in draws) if b is not None]
    assert len(errs) == 6, "expected 6 error bars, one per bar"
    img, scale = fig.render(300)
    crop = fig.crop
    bars = []
    for xc, up, stem_bottom in errs:
        ys = next((v for k, v in tops.items() if abs(k - xc) < 1), None)
        if ys is not None:
            assert len(ys) == 2, "bar top is not one outer and one inner edge"
            top = sum(ys) / 2
            assert abs(stem_bottom - top) < 0.1, "error stem does not end at its bar's outline"
        else:
            # outline baked into an embedded image: the stem ends on the bar top (as it does, within 0.1 pt, on
            # every bar whose outline is vector); check a dark outline row on the render beside the stem
            top = stem_bottom
            col = img[:, int((xc + 2 - crop[0]) * scale) - 1:int((xc + 2 - crop[0]) * scale) + 2].astype(int)
            dark = [crop[1] + (y + 0.5) / scale for y in range(col.shape[0]) if col[y].mean() < 60]
            assert any(abs(y - top) < 0.6 for y in dark), "no outline on the render where the stem ends"
        bars.append((xc, top, up))
    assert sum(1 for k in tops if any(abs(k - e[0]) < 1 for e in errs)) >= 5, "too few vector bar outlines"
    reds = [d["rect"] for d in draws if _red(d) and d["rect"].x0 > axis_x and d["rect"].height > 5]

    measures = [((wx0 + wx1) / 2, t) for wx0, wy0, wx1, wy1, t in words if t in ("CV", "APD") and wy0 > bottom]
    assert sorted(t for _, t in measures) == ["APD", "CV"], "measure labels not found"

    legend = {}
    for wx0, wy0, wx1, wy1, t in words:
        if t not in LEGEND:
            continue
        swatch = [d["rect"] for d in draws if _black(d) and 5 < d["rect"].width < 7 and 5 < d["rect"].height < 7
                  and d["rect"].x1 < wx0 and wx0 - d["rect"].x1 < 4 and abs((d["rect"].y0 + d["rect"].y1) / 2
                                                                            - (wy0 + wy1) / 2) < 2]
        assert len(swatch) == 1, "legend entry without one swatch"
        s = swatch[0]
        if LEGEND[t] != "control":
            legend[_diagonal(img, scale, crop, (s.x0 + 1, s.y0 + 1, s.x1 - 1, s.y1 - 1))] = LEGEND[t]
    assert len(legend) == 2, "the two hatched legend swatches do not run opposite ways"

    found = {}
    for xc, top, up in bars:
        measure = min(measures, key=lambda w: abs(w[0] - xc))[1]
        if any(abs((r.x0 + r.x1) / 2 - xc) < 1 for r in reds):
            group = "control"
        else:
            group = legend[_diagonal(img, scale, crop, (xc - 2.5, top + 4, xc + 2.5, bottom - 4))]
        assert (measure, group) not in found, "two bars for one group"
        assert up < top, "error bar does not rise above its bar"
        mlo, mhi = cal.interval(top, unc)
        elo, ehi = cal.interval(up, unc)
        found[(measure, group)] = {"points": [], "countable": False,
                                   "bar": {"mean": [cal.value(top), mlo - cal.residual, mhi + cal.residual],
                                           "error": [cal.value(up), elo - cal.residual, ehi + cal.residual]}}
    return {"groups": {label: found[key] for label, key in LABELS.items()}}
