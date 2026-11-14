"""Fig. 4I (% MHC+ cells, left; % Ki-67+ cells, right; DMSO 30d, SP 30d, untreated 60d), main.pdf page 7.

Vector panels. Each point is a translucent disc (radius about 1.82 pt) stored as flattened pieces; the centre
comes from the arcs of the disc boundary (_util.arc_centres / discs). Each panel has its own y axis (a long
vertical stroke); columns come from its x-axis ticks, left to right DMSO, SP, 60d. Mean and SEM are unfilled
strokes centred on the column: the mean is the long horizontal stroke (about 12.1 pt), the SEM ends are the
short caps (about 6.1 pt); the upper cap is the upper error-bar end.

Tick labels are outlined glyphs (no text), so tick values are stated from the printed labels (MHC 100 to 0,
Ki-67 30 to 0, from the top) and matched in order to the major ticks (about 4.55 pt long) on each y axis.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

from _util import arc_centres, discs

DISC_RADIUS = 1.82
PANELS = {  # left to right
    "MHC": [100, 80, 60, 40, 20, 0],
    "Ki-67": [30, 25, 20, 15, 10, 5, 0],
}
COLUMNS = ["DMSO", "SP", "60d"]
LABELS = {  # label -> (panel, column); a column serves every pairwise item it is in
    "MHC: DMSO": ("MHC", "DMSO"), "MHC: SP": ("MHC", "SP"), "MHC: 60d": ("MHC", "60d"),
    "Ki-67 SP vs DMSO: SP": ("Ki-67", "SP"), "Ki-67 SP vs DMSO: DMSO": ("Ki-67", "DMSO"),
    "Ki-67 60d vs DMSO: 60d": ("Ki-67", "60d"), "Ki-67 60d vs DMSO: DMSO": ("Ki-67", "DMSO"),
    "Ki-67 SP vs 60d: SP": ("Ki-67", "SP"), "Ki-67 SP vs 60d: 60d": ("Ki-67", "60d"),
}


def _strokes(fig):
    """Single-line unfilled strokes: (x0, y0, x1, y1)."""
    out = []
    for d in fig.drawings():
        if d.get("fill") is None and len(d["items"]) == 1 and d["items"][0][0] == "l":
            a, b = d["items"][0][1], d["items"][0][2]
            out.append((min(a.x, b.x), min(a.y, b.y), max(a.x, b.x), max(a.y, b.y)))
    return out


def _panel(fig, st, axis, ticks):
    ax, xaxis = axis[0], axis[3]
    major = sorted(s[1] for s in st if s[1] == s[3] and abs(s[2] - ax) < 0.05 and 4.3 < s[2] - s[0] < 4.9)
    if len(major) != len(ticks):
        raise ValueError(f"{len(major)} major ticks for {len(ticks)} labels")
    cal = calibrate(list(zip(major, ticks)))
    unc = VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)
    xticks = sorted(s[0] for s in st if s[0] == s[2] and abs(s[1] - xaxis) < 0.05 and 4.3 < s[3] - s[1] < 4.9
                    and ax < s[0] < ax + 70)
    if len(xticks) != len(COLUMNS):
        raise ValueError(f"{len(xticks)} x ticks")
    box = (ax, major[0] - 10, xticks[-1] + 10, xaxis)
    ds = discs(arc_centres(fig, box, keep=lambda f: min(f) > 0.2), DISC_RADIUS, rtol=0.05)
    per, used = {}, 0
    for col, cx in zip(COLUMNS, xticks):
        def centred(lo, hi):
            return sorted(s[1] for s in st if s[1] == s[3] and lo < s[2] - s[0] < hi
                          and abs((s[0] + s[2]) / 2 - cx) < 0.05)
        means, caps = centred(11.5, 13.0), centred(5.6, 6.6)
        if len(means) != 1 or len(caps) != 2:
            raise ValueError(f"{col}: {len(means)} mean strokes, {len(caps)} caps")
        m = point(cal, means[0], unc, (cx, means[0]))
        e = point(cal, caps[0], unc, (cx, caps[0]))
        mine = sorted((d for d in ds if abs(d[0] - cx) < 7.0), key=lambda d: d[1])
        used += len(mine)
        per[col] = {"points": [point(cal, y, unc, (x, y)) for x, y, _ in mine], "countable": True,
                    "bar": {"mean": [m["value"], m["lo"], m["hi"]], "error": [e["value"], e["lo"], e["hi"]]}}
    if used != len(ds):
        raise ValueError("a disc lies outside every column")
    return per


def read(fig):
    st = _strokes(fig)
    axes = sorted((s for s in st if s[0] == s[2] and s[3] - s[1] > 50), key=lambda s: s[0])
    if len(axes) != len(PANELS):
        raise ValueError(f"{len(axes)} y-axis candidates")
    per = {name: _panel(fig, st, axis, ticks) for (name, ticks), axis in zip(PANELS.items(), axes)}
    return {"groups": {label: per[p][c] for label, (p, c) in LABELS.items()}}
