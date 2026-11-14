"""Fig. 2g–j: maximum active force (g), specific force (h), CV (i) and APD80 (j) of cardiopatches in 3D RB+ medium
or switched to 5% FBS medium at d14, d7 or d0 (four vector bar charts, mean + upper SEM bar, no individual points).

The four panels share one crop; each has its own y axis (a black drawing of short tick rectangles left of the axis
line). Tick rectangles are matched to the nearest numeric label just left of them. Bars are one-rectangle drawings
with a coloured fill and a bar belongs to the nearest axis to its left. The group of a bar is read from its rotated
x-axis label: the "(dN–21)" word whose right end lines up with the bar's right end names the switch day, and the
word printed before it ("RB+" or "FBS") separates 3D RB+ (d0–21) from 5% FBS (d0–21). Each error bar is a black
stem + cap shape centred on its bar; the cap's centre is the upper end.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate

PANELS = ["force", "specific", "cv", "apd"]  # g, h, i, j from left to right
# one label per (comparison item, group) the figure feeds
LABELS = {
    "force_omnibus.rb": ("force", "rb"), "force_omnibus.fbs14": ("force", "fbs14"),
    "force_omnibus.fbs7": ("force", "fbs7"), "force_omnibus.fbs0": ("force", "fbs0"),
    "cv_omnibus.rb": ("cv", "rb"), "cv_omnibus.fbs14": ("cv", "fbs14"),
    "cv_omnibus.fbs7": ("cv", "fbs7"), "cv_omnibus.fbs0": ("cv", "fbs0"),
    "specific_rb_vs_fbs14.rb": ("specific", "rb"), "specific_rb_vs_fbs14.fbs14": ("specific", "fbs14"),
    "specific_rb_vs_fbs7.rb": ("specific", "rb"), "specific_rb_vs_fbs7.fbs7": ("specific", "fbs7"),
    "specific_rb_vs_fbs0.rb": ("specific", "rb"), "specific_rb_vs_fbs0.fbs0": ("specific", "fbs0"),
    "apd_rb_vs_fbs14.rb": ("apd", "rb"), "apd_rb_vs_fbs14.fbs14": ("apd", "fbs14"),
    "apd_rb_vs_fbs7.rb": ("apd", "rb"), "apd_rb_vs_fbs7.fbs7": ("apd", "fbs7"),
    "apd_rb_vs_fbs0.rb": ("apd", "rb"), "apd_rb_vs_fbs0.fbs0": ("apd", "fbs0"),
}
DAY = {"(d14–21)": "fbs14", "(d7–21)": "fbs7"}


def _black(d):
    return d.get("fill") is not None and max(d["fill"]) < 0.05


def _coloured(d):
    f = d.get("fill")
    return f is not None and len(d["items"]) == 1 and d["items"][0][0] == "re" and 0.05 < max(f) and min(f) < 0.95


def _group(bar, words):
    """The group named by the x-axis label under a bar."""
    day = min((w for w in words if w[4].startswith("(d") and w[4].endswith("–21)")), key=lambda w: abs(w[2] - bar.x1))
    if abs(day[2] - bar.x1) > 3:
        raise ValueError(f"no x-axis label under the bar at x={bar.x1:.1f}")
    if day[4] in DAY:
        return DAY[day[4]]
    before = [w for w in words if day[0] < w[2] < day[0] + 6 and abs((w[1] + w[3]) / 2 - (day[1] + day[3]) / 2) < 20]
    names = {w[4] for w in before if w[4] in ("RB+", "FBS")}  # a y tick label may sit nearby
    if names == {"RB+"}:
        return "rb"
    if names == {"FBS"}:
        return "fbs0"
    raise ValueError(f"x-axis label at x={day[0]:.1f} is not read: {names}")


def read(fig):
    draws = fig.drawings()
    words = fig.words()
    unc = VECTOR_UNCERTAINTY_PT
    # axes: black drawings made of ≥3 short tick rectangles (width ~3 pt, height < 1 pt)
    axes = []
    for d in draws:
        if not _black(d):
            continue
        ticks = [i[1] for i in d["items"] if i[0] == "re" and 2.5 < i[1].width < 4 and i[1].height < 1]
        if len(ticks) >= 3:
            x0 = min(r.x0 for r in ticks)
            nums = fig.tick_marks("y", near=x0 - 7, tol=5)
            marks = []
            for r in ticks:
                y = (r.y0 + r.y1) / 2
                pos, v = min(nums, key=lambda m: abs(m[0] - y))
                if abs(pos - y) < 2:
                    marks.append((y, v))
            axes.append((d["rect"].x1, calibrate(marks)))
    axes.sort(key=lambda a: a[0])
    if len(axes) != len(PANELS):
        raise ValueError(f"expected {len(PANELS)} axes, found {len(axes)}")
    caps = []
    for d in draws:
        if _black(d) and len(d["items"]) == 2 and all(i[0] == "re" for i in d["items"]):
            caps.append(min((i[1] for i in d["items"]), key=lambda r: r.y0))
    panels = {p: {} for p in PANELS}
    for d in draws:
        r = d["rect"]
        if not (_coloured(d) and r.height > 7):
            continue
        k = max(i for i, (ax, _) in enumerate(axes) if ax < r.x0)
        cal = axes[k][1]
        g = _group(r, words)
        xc = (r.x0 + r.x1) / 2
        cap = min(caps, key=lambda c: abs((c.x0 + c.x1) / 2 - xc))
        top, ce = r.y0, (cap.y0 + cap.y1) / 2
        mlo, mhi = cal.interval(top, unc)
        elo, ehi = cal.interval(ce, unc)
        panels[PANELS[k]][g] = {"points": [], "countable": False,
                                "bar": {"mean": [cal.value(top), mlo - cal.residual, mhi + cal.residual],
                                        "error": [cal.value(ce), elo - cal.residual, ehi + cal.residual]}}
    return {"groups": {label: panels[p][g] for label, (p, g) in LABELS.items()}}
