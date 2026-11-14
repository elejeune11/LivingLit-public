"""Fig. 4A (journal_version.pdf p. 7): western blot quantification of SR proteins, RPMI/B27 vs MM.

Raster image (embedded at ~300 dpi). Bars (mean +/- SEM) with one dot per batch (n = 3).
The dots are not countable: in SERCA2a and PLN RPMI/B27 they overlap each other, and in
most MM groups a dot sits on the bar top or on the error-bar cap. So only each bar's mean
(its top edge) and the upper end of its error bar (the cap) are read.

Bars are found as runs of fill colour on one row near the x axis: RPMI/B27 light grey
(~180), MM dark grey (~104), in plotted order SERCA2a, PLN, CASQ2 (printed "CASLQ"), JPH2.
A bar's top is read on its four leftmost inner columns, which no dot reaches, as the row
of the first fully filled pixel minus the fraction of fill colour in the rows above it.
The cap is the run of rows above the bar, joined to the bar top by the error line (so not a
significance line), where both cap ends (4.5-5.5 px either side of
the bar centre) are dark; dots are at most 9 px wide, so only the 12-13 px cap darkens both ends.
Its position is the darkness-weighted centre of those rows. The y axis is calibrated
from its four tick marks (0, 1, 2, 3), the bottom one at the x axis line.
"""
import numpy as np

from livinglit.figures.source import calibrate, point

DPI = 300
UNC_PX = 0.6
AXIS_COL = 39
TICK_COLS = (32, 37)  # tick marks left of the y axis
TICK_VALUES = [3, 2, 1, 0]  # top to bottom
FILL_ROW = 200  # a row inside every bar, above the x axis
ORDER = [("serca_rpmi", "rpmi"), ("serca_mm", "mm"), ("pln_rpmi", "rpmi"), ("pln_mm", "mm"),
         ("casq_rpmi", "rpmi"), ("casq_mm", "mm"), ("jph2_rpmi", "rpmi"), ("jph2_mm", "mm")]
FILL = {"rpmi": (165, 195), "mm": (75, 130)}  # grey level of each condition's bar fill


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


def _ticks(g):
    dark = 255 - g[:, TICK_COLS[0]:TICK_COLS[1] + 1].mean(axis=1)
    rows = []
    for a, b in _runs(list(dark > 128)):
        r = np.arange(a - 1, b + 2)
        rows.append(float((r * dark[r]).sum() / dark[r].sum()))
    return rows


def _bars(g):
    row = g[FILL_ROW]
    bars = []
    for cond in ("rpmi", "mm"):
        lo, hi = FILL[cond]
        for a, b in _runs(list((row >= lo) & (row <= hi))):
            if b - a >= 18:
                bars.append((a, b, cond))
    bars.sort()
    if [c for _, _, c in bars] != [c for _, c in ORDER]:
        raise ValueError(f"expected 8 bars alternating RPMI/B27, MM; found {bars}")
    return bars


def _top(g, x0, x1):
    fill = float(np.median(g[FILL_ROW, x0 + 2:x1 - 1]))
    tops = []
    for c in range(x0 + 1, x0 + 5):
        col = g[:, c]
        r = FILL_ROW
        while r > 0 and col[r - 1] < fill + 12:
            r -= 1
        cover = sum(min(1.0, max(0.0, (255 - col[k]) / (255 - fill))) for k in range(r - 3, r))
        tops.append(r - cover)
    if max(tops) - min(tops) > 1.0:
        raise ValueError(f"bar top uneven on its left columns {x0}-{x0 + 4}: {tops}")
    return float(np.mean(tops))


def _cap(g, centre, top):
    c = int(round(centre))
    ends = [int(round(centre + d)) for d in (-5.5, -4.5, 4.5, 5.5)]
    dark = 255 - g[:, ends]
    flags = [r < top - 2 and (dark[r] > 25).all() for r in range(g.shape[0])]
    line = (255 - g[:, [int(np.floor(centre)), int(np.ceil(centre))]]).max(axis=1) > 25
    runs = [(a, b) for a, b in _runs(flags) if line[b:int(top)].all()]  # joined to the bar by the error line
    if not runs:
        raise ValueError(f"no error-bar cap above the bar at column {c}")
    a, b = runs[-1]
    r = np.arange(a - 1, b + 2)
    w = dark[r].mean(axis=1)
    return float((r * w).sum() / w.sum())


def read(fig):
    img, scale = fig.render(DPI)
    g = img.astype(float).mean(axis=2)
    rows = _ticks(g)
    if len(rows) != len(TICK_VALUES):
        raise ValueError(f"expected {len(TICK_VALUES)} y ticks, found {rows}")
    cal = calibrate(list(zip(rows, TICK_VALUES)))
    res = cal.residual
    out = {}
    for (x0, x1, _), (label, _) in zip(_bars(g), ORDER):
        cx = (x0 + x1) / 2
        top = _top(g, x0, x1)
        cap = _cap(g, cx, top)
        pm = point(cal, top, UNC_PX, fig.to_page(cx, top, scale))
        pu = point(cal, cap, UNC_PX, fig.to_page(cx, cap, scale))
        out[label] = {"points": [], "countable": False,
                      "bar": {"mean": [pm["value"], pm["lo"] - res, pm["hi"] + res],
                              "error": [pu["value"], pu["lo"] - res, pu["hi"] + res]}}
    return {"groups": out}
