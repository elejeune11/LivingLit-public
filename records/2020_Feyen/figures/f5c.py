"""Fig. 5C (journal_version.pdf p. 8): fetal TTN by qRT-PCR, maturation media (MM) RBM20-WT vs RBM20-R634Q.

Raster image (embedded at ~300 dpi). Bars (mean +/- SEM) on a dark grey fill (~101) with one
black dot per batch (n = 3). Only the two MM bars are read (the groups the record asks for).

The dots stand apart from each other but touch lines: in MM WT all three sit on the black band
that the mean and both SEM caps make together; in MM R634Q the middle dot sits on the vertical
error line. A dot is therefore found from its column chords, not from a connected blob: in every
column of the group's window, each run of black pixels (< 50, below the bar fill) 4-10 px long is a
dot chord. The mean/cap band (3 px) and the caps are shorter and the vertical error line (> 30 px)
is longer, so neither counts; a dot's columns on both sides of a vertical line are kept, so its
centre is not pulled. Each chord's centre is the midpoint of its sub-pixel top and bottom edges
(coverage of the edge pixel against the background just outside: white or bar fill). Chords
within 4 columns and 4 rows of each other form one dot; its centre is the mean of its chords.

MM R634Q: the bar top (no outline) is read on four inner columns at its left edge, which no dot,
cap or line reaches, as the sub-pixel edge between white and fill; the upper SEM cap is the
darkness-weighted centre of its rows at columns clear of the vertical line. MM WT: the bar top
and both caps are hidden in one black band, so its mean is given as the band's centre with the
band's top and bottom edges as its interval, and no error end is read.

The y axis is calibrated from its four tick marks (15, 10, 5, 0), the bottom one at the x axis.
"""
import numpy as np

from livinglit.figures.source import calibrate, point

DPI = 300
UNC_PX = 0.6
BLACK = 50
TICK_COLS = (88, 92)  # tick marks left of the y axis line
TICK_VALUES = [15, 10, 5, 0]  # top to bottom
PLOT_ROWS = (58, 206)  # below the significance lines, above the x axis line
CHORD = (4, 10)
# label: (column window of the group's bar and dots)
GROUPS = {"mm_wt": (228, 282), "mm_mut": (290, 342)}
MUT_TOP_COLS = (297, 301)  # inner left columns of the MM R634Q bar
MUT_CAP_COLS = (306, 311)  # upper cap, left of the vertical error line
WT_BAND_COLS = (244, 249)  # mean/cap band between the left and middle dots of MM WT


def _runs(flags):
    out, start = [], None
    for i, f in enumerate(flags):
        if f and start is None:
            start = i
        if not f and start is not None:
            out.append((start, i - 1))
            start = None
    if start is not None:
        out.append((start, len(flags) - 1))
    return out


def _cover(v, bg):
    return float(min(1.0, max(0.0, (bg - v) / bg)))


def _edges(col, a, b):
    """Sub-pixel top and bottom edges (pixel-centre rows) of the black run a..b in one column."""
    top = a - 0.5 - _cover(col[a - 1], col[a - 3])
    bot = b + 0.5 + _cover(col[b + 1], col[b + 3])
    return top, bot


def _ticks(g):
    dark = 255 - g[:, TICK_COLS[0]:TICK_COLS[1] + 1].mean(axis=1)
    rows = []
    for a, b in _runs(list(dark > 128)):
        r = np.arange(a - 1, b + 2)
        rows.append(float((r * dark[r]).sum() / dark[r].sum()))
    return rows


def _dots(g, c0, c1):
    chords = []
    for c in range(c0, c1 + 1):
        col = g[:, c]
        flags = [PLOT_ROWS[0] <= r <= PLOT_ROWS[1] and col[r] < BLACK for r in range(len(col))]
        for a, b in _runs(flags):
            if CHORD[0] <= b - a + 1 <= CHORD[1]:
                top, bot = _edges(col, a, b)
                chords.append((c, (top + bot) / 2))
    dots = []
    for c, y in chords:
        for d in dots:
            if abs(c - d[-1][0]) <= 4 and abs(y - d[-1][1]) <= 4:
                d.append((c, y))
                break
        else:
            dots.append([(c, y)])
    return [(float(np.mean([c for c, _ in d])), float(np.mean([y for _, y in d])), len(d)) for d in dots]


def _bar_top(g, c0, c1):
    tops = []
    for c in range(c0, c1 + 1):
        col = g[:, c]
        fill = float(col[PLOT_ROWS[1] - 20])
        r = PLOT_ROWS[1] - 20
        while col[r - 1] < fill + 12:
            r -= 1
        tops.append(r - 0.5 - sum(min(1.0, max(0.0, (255 - col[k]) / (255 - fill))) for k in range(r - 3, r)))
    if max(tops) - min(tops) > 1.0:
        raise ValueError(f"bar top uneven on columns {c0}-{c1}: {tops}")
    return float(np.mean(tops))


def _cap(g, c0, c1, below):
    """Darkness-weighted centre of the lowest black run above row `below` in columns c0..c1."""
    dark = 255 - g[:, c0:c1 + 1].mean(axis=1)
    runs = [(a, b) for a, b in _runs(list(dark > 128)) if b < below and a >= PLOT_ROWS[0]]
    if not runs:
        raise ValueError("no error-bar cap found")
    a, b = runs[-1]
    r = np.arange(a - 1, b + 2)
    return float((r * dark[r]).sum() / dark[r].sum())


def _band(g, c0, c1):
    """Top and bottom edges of the black mean/cap band (mean over columns)."""
    tops, bots = [], []
    for c in range(c0, c1 + 1):
        col = g[:, c]
        runs = [(a, b) for a, b in _runs(list(col < BLACK)) if PLOT_ROWS[0] <= a <= PLOT_ROWS[1]]
        if len(runs) != 1 or runs[0][1] - runs[0][0] > 5:
            raise ValueError(f"expected one mean/cap band in column {c}, found {runs}")
        t, b = _edges(col, *runs[0])
        tops.append(t)
        bots.append(b)
    return float(np.mean(tops)), float(np.mean(bots))


def read(fig):
    img, scale = fig.render(DPI)
    g = img.astype(float).mean(axis=2)
    rows = _ticks(g)
    if len(rows) != len(TICK_VALUES):
        raise ValueError(f"expected {len(TICK_VALUES)} y ticks, found {rows}")
    cal = calibrate(list(zip(rows, TICK_VALUES)))
    res = cal.residual
    out = {}
    for label, (c0, c1) in GROUPS.items():
        dots = _dots(g, c0, c1)
        if len(dots) != 3:
            raise ValueError(f"{label}: expected 3 dots (n = 3 batches), found {dots}")
        pts = []
        for cx, cy, _ in sorted(dots, key=lambda d: d[0]):
            p = point(cal, cy, UNC_PX, fig.to_page(cx, cy, scale))
            p["lo"], p["hi"] = p["lo"] - res, p["hi"] + res
            pts.append(p)
        out[label] = {"points": pts, "countable": True}
    cx = (MUT_TOP_COLS[0] + MUT_TOP_COLS[1]) / 2
    top = _bar_top(g, *MUT_TOP_COLS)
    cap = _cap(g, *MUT_CAP_COLS, below=top)
    pm = point(cal, top, UNC_PX, fig.to_page(cx, top, scale))
    pu = point(cal, cap, UNC_PX, fig.to_page(cx, cap, scale))
    out["mm_mut"]["bar"] = {"mean": [pm["value"], pm["lo"] - res, pm["hi"] + res],
                            "error": [pu["value"], pu["lo"] - res, pu["hi"] + res]}
    t, b = _band(g, *WT_BAND_COLS)
    hi, lo = cal.value(t - UNC_PX), cal.value(b + UNC_PX)
    out["mm_wt"]["bar"] = {"mean": [cal.value((t + b) / 2), lo - res, hi + res]}
    return {"groups": out}
