"""Fig. 3F (nuclei per cardiomyocyte, %: mono-, bi-, trinucleated; DMSO 30d, SP 30d, untreated 60d), main.pdf page 6.

Vector panel. Each point is a translucent grey disc stored as flattened pieces (grey where it stands alone,
mixed with the bar colour or black where it overlaps a bar or a stroke), so no piece is a whole disc. Centres
come from the arcs of the disc boundary (_util.arc_centres / discs). Columns come from the error bars: each
error bar is one black filled outline about 4.7 pt wide; its centre x is the column. Categories come from the
x-axis ticks (Mono, Bi, Tri); within a category the columns are, left to right, DMSO, SP, 60d.

The y axis has three segments (75-100, 10-25, 0-3), each calibrated alone. Tick labels are outlined glyphs (no
text), so tick values are stated from the printed labels and matched in order from the top to the major ticks
and, where a label sits at a break, to the break stroke (the wider stroke across the axis).

The mean is the midpoint of the error-bar outline (SEM bars are symmetric); it is checked against the top of
the bar outline. The upper error-bar end is the top edge of the outline plus half the stroke width (0.56 pt).
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

from _util import arc_centres, discs

STROKE = 0.56
DISC_RADIUS = 1.125
# segment -> tick values from the top, and whether its break strokes carry labels
SEGMENTS = [([100, 90, 80], False), ([25, 20, 15, 10], True), ([3, 2, 1, 0], True)]
CATEGORIES = ["Mono", "Bi", "Tri"]
COLUMNS = ["DMSO", "SP", "60d"]
LABELS = {  # label -> (category, column); a column serves each pairwise item it is in
    "Mono SP vs DMSO: SP": ("Mono", "SP"), "Mono SP vs DMSO: DMSO": ("Mono", "DMSO"),
    "Mono 60d vs DMSO: 60d": ("Mono", "60d"), "Mono 60d vs DMSO: DMSO": ("Mono", "DMSO"),
    "Mono SP vs 60d: SP": ("Mono", "SP"), "Mono SP vs 60d: 60d": ("Mono", "60d"),
    "Bi SP vs DMSO: SP": ("Bi", "SP"), "Bi SP vs DMSO: DMSO": ("Bi", "DMSO"),
    "Bi 60d vs DMSO: 60d": ("Bi", "60d"), "Bi 60d vs DMSO: DMSO": ("Bi", "DMSO"),
    "Bi SP vs 60d: SP": ("Bi", "SP"), "Bi SP vs 60d: 60d": ("Bi", "60d"),
    "Tri SP vs DMSO: SP": ("Tri", "SP"), "Tri SP vs DMSO: DMSO": ("Tri", "DMSO"),
    "Tri SP vs 60d: SP": ("Tri", "SP"), "Tri SP vs 60d: 60d": ("Tri", "60d"),
}


def _strokes(fig):
    """Single-line unfilled strokes: (x0, y0, x1, y1)."""
    out = []
    for d in fig.drawings():
        if d.get("fill") is None and len(d["items"]) == 1 and d["items"][0][0] == "l":
            a, b = d["items"][0][1], d["items"][0][2]
            out.append((min(a.x, b.x), min(a.y, b.y), max(a.x, b.x), max(a.y, b.y)))
    return out


def _black(f):
    return f is not None and max(f) < 0.1


def _axis(st):
    """y-axis x, its segments [(top, bottom)], major tick ys, break-stroke ys, x-tick xs and x-axis y."""
    vert = [s for s in st if s[0] == s[2] and s[3] - s[1] > 15]
    ax = min(s[0] for s in vert)
    segs = sorted((s[1], s[3]) for s in vert if s[0] == ax)
    major = sorted(s[1] for s in st if s[1] == s[3] and abs(s[2] - ax) < 0.05 and 3.9 < s[2] - s[0] < 4.5)
    breaks = sorted(s[1] for s in st if s[1] == s[3] and s[0] < ax < s[2] and 5.3 < s[2] - s[0] < 6.0)
    xaxis = segs[-1][1]
    xticks = sorted(s[0] for s in st if s[0] == s[2] and 3.9 < s[3] - s[1] < 4.5 and abs(s[1] - xaxis) < 0.05)
    return ax, segs, major, breaks, xticks, xaxis


def _error_bars(fig, ax):
    """Error-bar outlines: black filled pieces about 4.7 pt wide and of 24 path items. Returns (cx, top, bottom)."""
    out = []
    for d in fig.drawings():
        r = d["rect"]
        if _black(d.get("fill")) and r.x0 > ax and 4.5 < r.width < 4.9 and len(d["items"]) == 24:
            out.append(((r.x0 + r.x1) / 2, r.y0, r.y1))
    return sorted(out)


def _bar_top(fig, cx):
    """Top of the black bar outline (about 8.35 pt wide) centred on cx."""
    tops = [d["rect"].y0 for d in fig.drawings()
            if _black(d.get("fill")) and 8.2 < d["rect"].width < 8.5 and abs((d["rect"].x0 + d["rect"].x1) / 2 - cx) < 0.3]
    if not tops:
        raise ValueError(f"no bar outline at {cx}")
    return min(tops)


def read(fig):
    st = _strokes(fig)
    ax, segs, major, breaks, xticks, xaxis = _axis(st)
    if len(segs) != len(SEGMENTS) or len(xticks) != len(CATEGORIES):
        raise ValueError(f"{len(segs)} axis segments, {len(xticks)} x ticks")
    cals = []
    for (top, bottom), (values, with_breaks) in zip(segs, SEGMENTS):
        ys = [y for y in major if top - 0.05 <= y <= bottom + 0.05]
        if with_breaks:
            ys += [y for y in breaks if abs(y - top) < 0.05 or abs(y - bottom) < 0.05]
        ys = sorted(set(round(y, 3) for y in ys))
        if len(ys) != len(values):
            raise ValueError(f"segment {top}-{bottom}: {len(ys)} ticks for {len(values)} labels")
        cal = calibrate(list(zip(ys, values)))
        cals.append((top, bottom, cal, VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)))
    if abs(cals[0][2].value(segs[0][1]) - 75) > 0.1:
        raise ValueError("upper segment does not end at 75")

    def seg_of(y):
        for top, bottom, cal, unc in cals:
            if top - DISC_RADIUS - 0.3 <= y <= bottom + DISC_RADIUS + 0.3:
                return cal, unc
        raise ValueError(f"y {y} lies in no axis segment")

    bars = _error_bars(fig, ax)
    if len(bars) != len(CATEGORIES) * len(COLUMNS):
        raise ValueError(f"{len(bars)} error bars")
    box = (ax, segs[0][0] - 10, xticks[-1] + 20, xaxis + 3)
    ds = discs(arc_centres(fig, box), DISC_RADIUS, rtol=0.1)
    per = {}
    used = 0
    for i, cat in enumerate(CATEGORIES):
        cols = sorted(b for b in bars if min(range(len(xticks)), key=lambda k: abs(xticks[k] - b[0])) == i)
        if len(cols) != len(COLUMNS):
            raise ValueError(f"{cat}: {len(cols)} columns")
        for col, (cx, etop, ebot) in zip(COLUMNS, cols):
            mean_y = (etop + ebot) / 2
            if abs(_bar_top(fig, cx) - mean_y) > 0.1:
                raise ValueError(f"{cat} {col}: error-bar midpoint is not at the bar top")
            err_y = etop + STROKE / 2
            cal, unc = seg_of(mean_y)
            m, e = point(cal, mean_y, unc, (cx, mean_y)), point(cal, err_y, unc, (cx, err_y))
            mine = sorted((d for d in ds if abs(d[0] - cx) < 4.2), key=lambda d: d[1])
            used += len(mine)
            pts = []
            for x, y, _ in mine:
                pc, pu = seg_of(y)
                pts.append(point(pc, y, pu, (x, y)))
            per[(cat, col)] = {"points": pts, "countable": True,
                               "bar": {"mean": [m["value"], m["lo"], m["hi"]], "error": [e["value"], e["lo"], e["hi"]]}}
    if used != len(ds):
        raise ValueError("a disc lies outside every column")
    return {"groups": {label: per[key] for label, key in LABELS.items()}}
