"""Fig. 3I (cardiomyocyte volume, x 10^3 um3; DMSO 30d and SP 30d, MYL2 line), main.pdf page 6.

Vector panel. Each point is a translucent disc (radius about 1.69 pt) stored as flattened pieces, so no piece is
a whole disc. Centres come from the arcs of the disc boundary (_util.arc_centres / discs). Columns come from the
x-axis ticks (DMSO, SP from left to right); a disc belongs to the nearer tick.

The mean is the wide horizontal stroke (about 12 pt) on the column; the SEM bar is the vertical stroke with two
caps (about 6 pt). The upper error-bar end is the centre line of the upper cap (the stroke's own y). Tick labels are
outlined glyphs (no text), so tick values are stated from the printed labels (0 to 50 by 10) and matched from the
bottom to the major ticks (4.23 pt long); minor ticks (2.1 pt) are not used.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

from _util import arc_centres, discs

DISC_RADIUS = 1.69
TICKS = [0, 10, 20, 30, 40, 50]
COLUMNS = ["DMSO", "SP"]
LABELS = {"SP vs DMSO: SP": "SP", "SP vs DMSO: DMSO": "DMSO"}


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
    ax = min(s[0] for s in st if s[0] == s[2] and s[3] - s[1] > 50)
    xaxis = max(s[1] for s in st if s[1] == s[3] and s[2] - s[0] > 30)
    major = sorted((s[1] for s in st if s[1] == s[3] and abs(s[2] - ax) < 0.05 and 3.9 < s[2] - s[0] < 4.5),
                   reverse=True)
    if len(major) != len(TICKS):
        raise ValueError(f"{len(major)} major ticks for {len(TICKS)} labels")
    cal = calibrate(list(zip(major, TICKS)))
    unc = VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)
    xticks = sorted(s[0] for s in st if s[0] == s[2] and abs(s[1] - xaxis) < 0.05 and 3.9 < s[3] - s[1] < 4.5)
    if len(xticks) != len(COLUMNS):
        raise ValueError(f"{len(xticks)} x ticks")
    means = [s for s in st if s[1] == s[3] and 11.5 < s[2] - s[0] < 12.5]
    caps = [s for s in st if s[1] == s[3] and 5.5 < s[2] - s[0] < 6.5]
    ds = discs(arc_centres(fig, (ax + 0.1, fig.crop[1], fig.crop[2], xaxis + DISC_RADIUS + 1),
                           keep=lambda f: max(f) > 0.1), DISC_RADIUS, rtol=0.08)
    per, used = {}, 0
    for col, tx in zip(COLUMNS, xticks):
        mean = [s for s in means if abs((s[0] + s[2]) / 2 - tx) < 0.3]
        cap = sorted(s[1] for s in caps if abs((s[0] + s[2]) / 2 - tx) < 0.3)
        if len(mean) != 1 or len(cap) != 2:
            raise ValueError(f"{col}: {len(mean)} mean strokes, {len(cap)} caps")
        mean_y, err_y = mean[0][1], cap[0]
        if abs((cap[0] + cap[1]) / 2 - mean_y) > 0.1:
            raise ValueError(f"{col}: mean stroke is not midway between the caps")
        m, e = point(cal, mean_y, unc, (tx, mean_y)), point(cal, err_y, unc, (tx, err_y))
        mine = sorted((d for d in ds if min(xticks, key=lambda t: abs(t - d[0])) == tx), key=lambda d: d[1])
        used += len(mine)
        per[col] = {"points": [point(cal, y, unc, (x, y)) for x, y, _ in mine], "countable": True,
                    "bar": {"mean": [m["value"], m["lo"], m["hi"]], "error": [e["value"], e["lo"], e["hi"]]}}
    if used != len(ds):
        raise ValueError("a disc lies outside every column")
    return {"groups": {label: per[col] for label, col in LABELS.items()}}
