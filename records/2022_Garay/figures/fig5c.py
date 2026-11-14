"""Fig. 5C (normalized contraction force, uN/um2 x 10^-5; DMSO 30d, SP 30d, untreated 60d in the PLZ and MYL2
lines), main.pdf page 9.

Vector panel with a broken y axis: the lower segment (0 to 20) and the upper segment (45 to 100) are two vertical
strokes at the same x, each ending in a wide break cap (about 6.2 pt). Major ticks (about 4.6 pt long) carry the
labels; the lower break cap carries the label 20. Each segment is calibrated alone and a point is read on the
segment it lies on.

Each point is a translucent disc (radius about 1.85 pt) stored as flattened pieces; the centre comes from the arcs
of the disc boundary (_util.arc_centres / discs). Mean and SEM are unfilled strokes centred on each column: the mean
is the long horizontal stroke (about 11.7 pt), the SEM ends are the short caps (about 5.75 pt); the upper cap is the
upper error-bar end. Columns, left to right PLZ DMSO, SP, 60d, MYL2 DMSO, SP, 60d, are the centres of the mean
strokes. Significance brackets are multi-segment paths and are ignored.

Tick labels are outlined glyphs (no text), so tick values are stated from the printed labels and matched in order
to the major ticks of each segment.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

from _util import arc_centres, discs

DISC_RADIUS = 1.85
LOWER_TICKS = [15, 10, 5, 0]  # major ticks from the top; the break cap above them is 20
LOWER_CAP = 20
UPPER_TICKS = [100, 80, 60]  # major ticks from the top; the break cap below them carries no label
COLUMNS = ["PLZ DMSO", "PLZ SP", "PLZ 60d", "MYL2 DMSO", "MYL2 SP", "MYL2 60d"]
LABELS = {  # label -> column; a column serves every pairwise item it is in
    "PLZ SP vs DMSO: SP": "PLZ SP", "PLZ SP vs DMSO: DMSO": "PLZ DMSO",
    "PLZ 60d vs DMSO: 60d": "PLZ 60d", "PLZ 60d vs DMSO: DMSO": "PLZ DMSO",
    "PLZ SP vs 60d: SP": "PLZ SP", "PLZ SP vs 60d: 60d": "PLZ 60d",
    "MYL2 SP vs DMSO: SP": "MYL2 SP", "MYL2 SP vs DMSO: DMSO": "MYL2 DMSO",
    "MYL2 60d vs DMSO: 60d": "MYL2 60d", "MYL2 60d vs DMSO: DMSO": "MYL2 DMSO",
    "MYL2 SP vs 60d: SP": "MYL2 SP", "MYL2 SP vs 60d: 60d": "MYL2 60d",
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
    axes = sorted((s for s in st if s[0] == s[2] and s[3] - s[1] > 30), key=lambda s: s[1])
    if len(axes) != 2 or axes[0][0] != axes[1][0]:
        raise ValueError(f"{len(axes)} y-axis segments")
    ax = axes[0][0]
    upper, lower = axes
    horiz = [s for s in st if s[1] == s[3]]
    major = [s[1] for s in horiz if abs(s[2] - ax) < 0.05 and 4.3 < s[2] - s[0] < 4.9]
    caps = [s[1] for s in horiz if s[0] < ax < s[2] and 5.9 < s[2] - s[0] < 6.4]
    lo_major = sorted(y for y in major if lower[1] - 0.05 <= y <= lower[3] + 0.05)
    up_major = sorted(y for y in major if upper[1] - 0.05 <= y <= upper[3] + 0.05)
    lo_cap = [y for y in caps if abs(y - lower[1]) < 0.05]
    if len(lo_major) != len(LOWER_TICKS) or len(up_major) != len(UPPER_TICKS) or len(lo_cap) != 1:
        raise ValueError(f"ticks: lower {len(lo_major)}+{len(lo_cap)} cap, upper {len(up_major)}")
    cals = []
    for (top, bottom), marks in (((lower[1], lower[3]), list(zip(lo_major, LOWER_TICKS)) + [(lo_cap[0], LOWER_CAP)]),
                                 ((upper[1], upper[3]), list(zip(up_major, UPPER_TICKS)))):
        cal = calibrate(marks)
        cals.append((top, bottom, cal, VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)))

    def at(y):
        for top, bottom, cal, unc in cals:
            if top - DISC_RADIUS <= y <= bottom + DISC_RADIUS:
                return cal, unc
        raise ValueError(f"y = {y:.2f} lies in the axis break")

    def pt(x, y):
        cal, unc = at(y)
        return point(cal, y, unc, (x, y))

    means = sorted((s for s in horiz if 11.2 < s[2] - s[0] < 12.2 and s[0] > ax), key=lambda s: s[0])
    if len(means) != len(COLUMNS):
        raise ValueError(f"{len(means)} mean strokes")
    centres = [(s[0] + s[2]) / 2 for s in means]
    ds = discs(arc_centres(fig, (ax, upper[1] - 10, centres[-1] + 12, lower[3] + 5), keep=lambda f: min(f) > 0.05),
               DISC_RADIUS)
    per, used = {}, 0
    for col, cx, ms in zip(COLUMNS, centres, means):
        ends = sorted(s[1] for s in horiz if 5.5 < s[2] - s[0] < 6.0 and abs((s[0] + s[2]) / 2 - cx) < 0.05)
        if len(ends) != 2:
            raise ValueError(f"{col}: {len(ends)} caps")
        m, e = pt(cx, ms[1]), pt(cx, ends[0])
        mine = sorted((d for d in ds if abs(d[0] - cx) < 8.8), key=lambda d: d[1])
        used += len(mine)
        per[col] = {"points": [pt(x, y) for x, y, _ in mine], "countable": True,
                    "bar": {"mean": [m["value"], m["lo"], m["hi"]], "error": [e["value"], e["lo"], e["hi"]]}}
    if used != len(ds):
        raise ValueError("a disc lies outside every column")
    return {"groups": {label: per[c] for label, c in LABELS.items()}}
