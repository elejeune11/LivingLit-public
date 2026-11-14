"""Fig. 4K (% cTnT+ pHH3+ nuclei; DMSO 30d, SP 30d, untreated 60d; PLZ line), main.pdf page 7.

Vector panel. Each point is a translucent disc (radius about 1.82 pt) stored as flattened pieces; the centre
comes from the arcs of the disc boundary (_util.arc_centres / discs). The y axis is the long vertical stroke;
its major ticks (about 4.54 pt long) carry the labels. Mean and SEM are unfilled strokes centred on each column:
the mean is the long horizontal stroke (about 18.2 pt), the SEM ends are the short caps (about 9.1 pt); the
upper cap is the upper error-bar end. Columns, left to right DMSO, SP, 60d, are the centres of the mean strokes
(two of the three x ticks are filled rectangles, one a stroke). Significance brackets are multi-segment paths
and are ignored.

Tick labels are outlined glyphs (no text), so tick values are stated from the printed labels (1.5 to 0.0,
from the top) and matched in order to the major ticks on the y axis.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

from _util import arc_centres, discs

DISC_RADIUS = 1.82
TICKS = [1.5, 1.2, 0.9, 0.6, 0.3, 0.0]  # from the top
COLUMNS = ["DMSO", "SP", "60d"]
LABELS = {  # label -> column; a column serves every pairwise item it is in
    "SP vs DMSO: SP": "SP", "SP vs DMSO: DMSO": "DMSO",
    "60d vs DMSO: 60d": "60d", "60d vs DMSO: DMSO": "DMSO",
    "SP vs 60d: SP": "SP", "SP vs 60d: 60d": "60d",
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
    axes = [s for s in st if s[0] == s[2] and s[3] - s[1] > 100]
    if len(axes) != 1:
        raise ValueError(f"{len(axes)} y-axis candidates")
    ax, top, bottom = axes[0][0], axes[0][1], axes[0][3]
    major = sorted(s[1] for s in st if s[1] == s[3] and abs(s[2] - ax) < 0.05 and 4.3 < s[2] - s[0] < 4.8)
    if len(major) != len(TICKS):
        raise ValueError(f"{len(major)} major ticks for {len(TICKS)} labels")
    cal = calibrate(list(zip(major, TICKS)))
    unc = VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)

    means = sorted((s for s in st if s[1] == s[3] and 17.5 < s[2] - s[0] < 19.0 and s[0] > ax), key=lambda s: s[0])
    if len(means) != len(COLUMNS):
        raise ValueError(f"{len(means)} mean strokes")
    centres = [(s[0] + s[2]) / 2 for s in means]
    ds = discs(arc_centres(fig, (ax, top - 10, centres[-1] + 20, bottom + 5), keep=lambda f: min(f) > 0.05),
               DISC_RADIUS, rtol=0.05)
    per, used = {}, 0
    for col, cx, ms in zip(COLUMNS, centres, means):
        caps = sorted(s[1] for s in st if s[1] == s[3] and 8.5 < s[2] - s[0] < 9.7
                      and abs((s[0] + s[2]) / 2 - cx) < 0.05)
        if len(caps) != 2:
            raise ValueError(f"{col}: {len(caps)} caps")
        m = point(cal, ms[1], unc, (cx, ms[1]))
        e = point(cal, caps[0], unc, (cx, caps[0]))
        mine = sorted((d for d in ds if abs(d[0] - cx) < 12.0), key=lambda d: d[1])
        used += len(mine)
        per[col] = {"points": [point(cal, y, unc, (x, y)) for x, y, _ in mine], "countable": True,
                    "bar": {"mean": [m["value"], m["lo"], m["hi"]], "error": [e["value"], e["lo"], e["hi"]]}}
    if used != len(ds):
        raise ValueError("a disc lies outside every column")
    return {"groups": {label: per[c] for label, c in LABELS.items()}}
