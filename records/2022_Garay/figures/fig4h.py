"""Fig. 4H (MKI67 log2 counts per million; DMSO 30d, SP 30d, untreated 90d), main.pdf page 7.

Vector panel. Each point is a coloured disc (radius about 1.82 pt) stored as one closed path of Bezier arcs;
the centre comes from the arcs (_util.arc_centres / discs). Columns come from the x-axis ticks; left to right
DMSO, SP, 90d. Mean and SEM are unfilled strokes centred on the column: the mean is the long horizontal stroke
(about 12.2 pt), the SEM ends are the short caps (about 6.1 pt); the upper cap is the upper error-bar end.

Tick labels are outlined glyphs (no text), so tick values are stated from the printed labels (8 to 4 from the
top) and matched in order to the major ticks (about 4.6 pt long) on the y axis.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

from _util import arc_centres, discs

DISC_RADIUS = 1.82
TICKS = [8, 7, 6, 5, 4]
COLUMNS = ["DMSO", "SP", "90d"]
LABELS = {  # label -> column; DMSO serves both pairwise items
    "SP vs DMSO: SP": "SP", "SP vs DMSO: DMSO": "DMSO",
    "90d vs DMSO: 90d": "90d", "90d vs DMSO: DMSO": "DMSO",
}


def _strokes(fig):
    """Single-line unfilled strokes: (x0, y0, x1, y1)."""
    out = []
    for d in fig.drawings():
        if d.get("fill") is None and len(d["items"]) == 1 and d["items"][0][0] == "l":
            a, b = d["items"][0][1], d["items"][0][2]
            out.append((min(a.x, b.x), min(a.y, b.y), max(a.x, b.x), max(a.y, b.y)))
    return out


def read(fig):
    st = _strokes(fig)
    vert = [s for s in st if s[0] == s[2] and s[3] - s[1] > 50]
    if len(vert) != 1:
        raise ValueError(f"{len(vert)} y-axis candidates")
    ax, xaxis = vert[0][0], vert[0][3]
    major = sorted(s[1] for s in st if s[1] == s[3] and abs(s[2] - ax) < 0.05 and 4.3 < s[2] - s[0] < 4.9)
    if len(major) != len(TICKS):
        raise ValueError(f"{len(major)} major ticks for {len(TICKS)} labels")
    cal = calibrate(list(zip(major, TICKS)))
    unc = VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)
    xticks = sorted(s[0] for s in st if s[0] == s[2] and abs(s[1] - xaxis) < 0.05 and 4.3 < s[3] - s[1] < 4.9)
    if len(xticks) != len(COLUMNS):
        raise ValueError(f"{len(xticks)} x ticks")
    box = (ax, major[0] - 10, xticks[-1] + 10, xaxis)
    ds = discs(arc_centres(fig, box, keep=lambda f: min(f) > 0.4), DISC_RADIUS, rtol=0.05)
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
        mine = sorted((d for d in ds if abs(d[0] - cx) < 6.5), key=lambda d: d[1])
        used += len(mine)
        per[col] = {"points": [point(cal, y, unc, (x, y)) for x, y, _ in mine], "countable": True,
                    "bar": {"mean": [m["value"], m["lo"], m["hi"]], "error": [e["value"], e["lo"], e["hi"]]}}
    if used != len(ds):
        raise ValueError("a disc lies outside every column")
    return {"groups": {label: per[col] for label, col in LABELS.items()}}
