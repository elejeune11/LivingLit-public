"""Fig. 7G (conduction velocity, cm/s) and Fig. 7I (field potential duration, FPD, ms); DMSO 30d (D), SP 30d (SP)
and untreated 60d in PLZ/MYL2 on microelectrode arrays, main.pdf page 12.

Both panels are vector GraphPad dot plots. Mean and SEM are unfilled strokes centred on each column: the mean is
the long horizontal stroke (about 9.3 pt), the SEM ends are the short caps (about 4.5 pt); the upper cap is the
upper error-bar end. Columns, left to right D, SP, 60d, are the centres of the mean strokes. Significance brackets
are three-segment paths and are ignored. Tick labels are outlined glyphs (no text), so tick values are stated from
the printed labels and matched in order to the major ticks (about 4.6 pt long).

7G: one y axis, 0 to 20 by 4. Its translucent discs (hundreds per column) are flattened into about 110 000 pieces
whose boundary arcs do not keep the disc radius (fitted radii spread from 1 to 3 pt); clustering their centres gives
anything from about 70 to 4 500 discs as the tolerance changes, so no point is read: the groups carry mean and SEM
only (countable false).

7I: broken y axis. The lower segment (0 to the break cap labelled 100) and the upper segment (break cap labelled
250, major ticks 300 to 600 by 50) are two vertical strokes at the same x; each is calibrated alone and a point is
read on the segment it lies on. Each point is a translucent disc (radius about 1.85 pt) stored as flattened pieces;
the centre comes from the arcs of the disc boundary (_util.arc_centres / discs). Discs drawn on top of each other
at the same place cannot be told apart; the mean and SEM of the discs read agree with the drawn bars, so the
columns are taken as countable.
"""
from livinglit.figures.source import VECTOR_UNCERTAINTY_PT, calibrate, point

from _util import arc_centres, discs

SPLIT = (300.0, 458.0)  # 7G lies left of the first x, 7I right of the second; 7H lies between
G_TICKS = [20, 16, 12, 8, 4, 0]  # 7G major ticks from the top
I_UPPER_TICKS = [600, 550, 500, 450, 400, 350, 300]  # 7I upper segment major ticks from the top
I_UPPER_CAP, I_LOWER_CAP, I_LOWER_TICKS = 250, 100, [0]  # 7I break caps and the lower segment's major tick
DISC_RADIUS = 1.85
COLUMNS = ["D", "SP", "60d"]
PAIRS = {  # label suffix -> column; a column serves every pairwise item it is in
    "SP vs DMSO: SP": "SP", "SP vs DMSO: DMSO": "D",
    "60d vs DMSO: 60d": "60d", "60d vs DMSO: DMSO": "D",
    "SP vs 60d: SP": "SP", "SP vs 60d: 60d": "60d",
}


def _strokes(fig, x0, x1):
    """Single-line unfilled strokes within x0..x1: (x0, y0, x1, y1)."""
    out = []
    for d in fig.drawings():
        if d.get("fill") is None and len(d["items"]) == 1 and d["items"][0][0] == "l":
            a, b = d["items"][0][1], d["items"][0][2]
            s = (min(a.x, b.x), min(a.y, b.y), max(a.x, b.x), max(a.y, b.y))
            if x0 <= s[0] and s[2] <= x1:
                out.append(s)
    return out


def _bars(horiz, ax, pt):
    """Mean and upper SEM end of each column, left to right."""
    means = sorted((s for s in horiz if 9.0 < s[2] - s[0] < 9.6 and s[0] > ax), key=lambda s: s[0])
    if len(means) != len(COLUMNS):
        raise ValueError(f"{len(means)} mean strokes")
    out = []
    for col, ms in zip(COLUMNS, means):
        cx = (ms[0] + ms[2]) / 2
        ends = sorted(s[1] for s in horiz if 4.3 < s[2] - s[0] < 4.7 and abs((s[0] + s[2]) / 2 - cx) < 0.15)
        if len(ends) != 2:
            raise ValueError(f"{col}: {len(ends)} caps")
        m, e = pt(cx, ms[1]), pt(cx, ends[0])
        out.append((col, cx, {"mean": [m["value"], m["lo"], m["hi"]], "error": [e["value"], e["lo"], e["hi"]]}))
    return out


def _panel_g(fig):
    st = _strokes(fig, fig.crop[0], SPLIT[0])
    axes = [s for s in st if s[0] == s[2] and s[3] - s[1] > 100]
    if len(axes) != 1:
        raise ValueError(f"7G: {len(axes)} y axes")
    ax = axes[0][0]
    horiz = [s for s in st if s[1] == s[3]]
    major = sorted(s[1] for s in horiz if abs(s[2] - ax) < 0.05 and 4.3 < s[2] - s[0] < 4.9)
    if len(major) != len(G_TICKS):
        raise ValueError(f"7G: {len(major)} major ticks")
    cal = calibrate(list(zip(major, G_TICKS)))
    unc = VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)
    return {col: {"points": [], "countable": False, "bar": bar}
            for col, _, bar in _bars(horiz, ax, lambda x, y: point(cal, y, unc, (x, y)))}


def _panel_i(fig):
    st = _strokes(fig, SPLIT[1], fig.crop[2])
    axes = sorted((s for s in st if s[0] == s[2] and s[3] - s[1] > 9), key=lambda s: s[1])
    if len(axes) != 2 or axes[0][0] != axes[1][0]:
        raise ValueError(f"7I: {len(axes)} y-axis segments")
    ax = axes[0][0]
    upper, lower = axes
    horiz = [s for s in st if s[1] == s[3]]
    major = [s[1] for s in horiz if abs(s[2] - ax) < 0.05 and 4.3 < s[2] - s[0] < 4.9]
    caps = [s[1] for s in horiz if s[0] < ax < s[2] and 5.9 < s[2] - s[0] < 6.4]
    up_major = sorted(y for y in major if upper[1] - 0.05 <= y <= upper[3] + 0.05)
    lo_major = sorted(y for y in major if lower[1] - 0.05 <= y <= lower[3] + 0.05)
    up_cap = [y for y in caps if abs(y - upper[3]) < 0.05]
    lo_cap = [y for y in caps if abs(y - lower[1]) < 0.05]
    if len(up_major) != len(I_UPPER_TICKS) or len(lo_major) != len(I_LOWER_TICKS) or len(up_cap) != 1 \
            or len(lo_cap) != 1:
        raise ValueError(f"7I ticks: upper {len(up_major)}+{len(up_cap)} cap, lower {len(lo_major)}+{len(lo_cap)} cap")
    cals = []
    for (top, bottom), marks in (((upper[1], upper[3]), list(zip(up_major, I_UPPER_TICKS)) + [(up_cap[0], I_UPPER_CAP)]),
                                 ((lower[1], lower[3]), list(zip(lo_major, I_LOWER_TICKS)) + [(lo_cap[0], I_LOWER_CAP)])):
        cal = calibrate(marks)
        cals.append((top, bottom, cal, VECTOR_UNCERTAINTY_PT + cal.residual / abs(cal.slope)))

    def pt(x, y):
        for top, bottom, cal, unc in cals:
            if top - DISC_RADIUS <= y <= bottom + DISC_RADIUS:
                return point(cal, y, unc, (x, y))
        raise ValueError(f"7I: y = {y:.2f} lies in the axis break")

    bars = _bars(horiz, ax, pt)
    ds = discs(arc_centres(fig, (ax, fig.crop[1], fig.crop[2], lower[3] + 5), keep=lambda f: min(f) > 0.05),
               DISC_RADIUS)
    out, used = {}, 0
    for col, cx, bar in bars:
        mine = sorted((d for d in ds if abs(d[0] - cx) < 6.5), key=lambda d: d[1])
        used += len(mine)
        out[col] = {"points": [pt(x, y) for x, y, _ in mine], "countable": True, "bar": bar}
    if used != len(ds):
        raise ValueError("7I: a disc lies outside every column")
    return out


def read(fig):
    g, i = _panel_g(fig), _panel_i(fig)
    groups = {}
    for panel, per in (("G", g), ("I", i)):
        for suffix, col in PAIRS.items():
            groups[f"{panel} {suffix}"] = per[col]
    return {"groups": groups}
