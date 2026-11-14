"""Fig. 4C (journal_version.pdf p. 7): CTD75-25 normalized after siSERCA2a (left) or siPLN (right).

Raster image (embedded at ~300 dpi). Two bar charts (mean +/- SEM), each with four bars in plotted
order RPMI siCtr, MM siCtr, RPMI siRNA, MM siRNA, and one marker per well (circles, squares and
triangles for the three batches; legend n = 3 batches, n = 3 wells each). The markers are not
countable: in every group read here at least one marker touches the bar top, the mean line or an
error-bar cap (in MM bars black markers on black lines), so only each bar's mean (its top edge) and
the upper end of its error bar (the cap) are read.

Bars are found as runs of fill colour on one row near the x axis: RPMI light grey (~180), MM dark
grey (~102). A bar's top is read per column (away from the error bar) by walking up from that row
while the pixel stays within the fill colour; a column counts only if the rows just above where the
walk stops are background (a marker on or inside the bar stops it with marker colour above). The
top is the mean over those columns, each refined by the fraction of fill colour in the rows above. The cap is the run of rows above the top, joined to it by the error line, where
both cap ends (6-8 px either side of the bar centre) are dark; its position is the centre of those
rows weighted by the lightest of the end columns, so a marker covering one end does not pull it.
Each y axis is calibrated from its four labelled tick marks above the x axis.
"""
import numpy as np

from livinglit.figures.source import calibrate, point

DPI = 300
UNC_PX = 0.6
FILL_ROW = 220  # a row inside every bar, below every marker, above the x axis (row ~227)
FILL = {"rpmi": (165, 195), "mm": (85, 120)}  # grey level of each condition's bar fill
BACKGROUND = 235  # lighter than this is background
MARKER_BELOW = {"rpmi": 160, "mm": 60}  # darker than this near a bar top is a marker (fill and outline are lighter)
PANELS = [  # (tick columns, tick values top to bottom, column range of the panel's bars)
    ((40, 47), [1.6, 1.4, 1.2, 1.0], (48, 330)),
    ((360, 367), [1.4, 1.2, 1.0, 0.8], (368, 700)),
]
BAR_CONDS = ["rpmi", "mm", "rpmi", "mm"]  # per panel: siCtr RPMI, siCtr MM, siRNA RPMI, siRNA MM
# label -> (panel, bar index in the panel); MM + siSERCA2a serves two items
LABELS = {
    "serca_mm_sictr": (0, 1),
    "serca_mm_siserca": (0, 3),
    "rpmi_vs_mm_siserca": (0, 3),
    "rpmi_vs_rpmi_siserca": (0, 2),
    "pln_mm_sictr": (1, 1),
    "pln_mm_sipln": (1, 3),
}


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


def _ticks(g, cols):
    dark = 255 - g[:FILL_ROW, cols[0]:cols[1] + 1].mean(axis=1)
    rows = []
    for a, b in _runs(list(dark > 60)):
        r = np.arange(max(a - 1, 0), b + 2)
        rows.append(float((r * dark[r]).sum() / dark[r].sum()))
    return rows


def _bars(g, span):
    row = g[FILL_ROW]
    bars = []
    for cond, (lo, hi) in FILL.items():
        for a, b in _runs(list((row >= lo) & (row <= hi))):
            if b - a >= 30 and span[0] <= a and b <= span[1]:
                bars.append((a, b, cond))
    bars.sort()
    if [c for _, _, c in bars] != BAR_CONDS:
        raise ValueError(f"expected 4 bars RPMI, MM, RPMI, MM in columns {span}; found {bars}")
    return bars


def _top(g, x0, x1, cond):
    fill = float(np.median(g[FILL_ROW, x0 + 3:x1 - 2]))
    cx = (x0 + x1) / 2
    tops = []
    for c in range(x0 + 3, x1 - 2):
        if abs(c - cx) <= 3:  # the error line
            continue
        col = g[:, c]
        r = FILL_ROW
        while r > 0 and col[r - 1] <= BACKGROUND:
            r -= 1
        # a marker on the bar top (rows above r are background; the lower cap lies >= 5 rows below)
        if (g[r:r + 4, c - 1:c + 2] < MARKER_BELOW[cond]).any():
            continue
        cover = min(1.0, max(0.0, (255 - col[r - 1]) / (255 - fill)))
        tops.append(r - cover)
    tops = np.array(tops)
    if len(tops) < 3 or tops.max() - tops.min() > 1.0:
        raise ValueError(f"bar top at columns {x0}-{x1} not found on enough clean columns: {sorted(tops)}")
    return float(tops.mean())


def _cap(g, centre, top):
    ends = [int(round(centre + d)) for d in (-8, -6, 6, 8)]
    dark = 255 - g[:, ends]
    flags = [r < top - 2 and (dark[r] > 25).all() for r in range(g.shape[0])]
    line = (255 - g[:, [int(np.floor(centre)) - 1, int(np.floor(centre)), int(np.ceil(centre)),
                        int(np.ceil(centre)) + 1]]).max(axis=1) > 25
    runs = [(a, b) for a, b in _runs(flags) if line[b:int(top)].all()]  # joined to the bar by the error line
    if not runs:
        raise ValueError(f"no error-bar cap above the bar at column {centre}")
    a, b = runs[-1]
    r = np.arange(a - 1, b + 2)
    w = dark[r].min(axis=1)
    return float((r * w).sum() / w.sum())


def read(fig):
    img, scale = fig.render(DPI)
    g = img.astype(float).mean(axis=2)
    bars = {}
    for p, (tcols, tvals, span) in enumerate(PANELS):
        rows = _ticks(g, tcols)
        if len(rows) != len(tvals):
            raise ValueError(f"panel {p}: expected {len(tvals)} y ticks above the x axis, found {rows}")
        cal = calibrate(list(zip(rows, tvals)))
        res = cal.residual
        for i, (x0, x1, _) in enumerate(_bars(g, span)):
            if (p, i) not in LABELS.values():  # RPMI + siCtr is in no item
                continue
            cx = (x0 + x1) / 2
            top = _top(g, x0, x1, BAR_CONDS[i])
            cap = _cap(g, cx, top)
            pm = point(cal, top, UNC_PX, fig.to_page(cx, top, scale))
            pu = point(cal, cap, UNC_PX, fig.to_page(cx, cap, scale))
            bars[(p, i)] = {"points": [], "countable": False,
                            "bar": {"mean": [pm["value"], pm["lo"] - res, pm["hi"] + res],
                                    "error": [pu["value"], pu["lo"] - res, pu["hi"] + res]}}
    return {"groups": {label: bars[key] for label, key in LABELS.items()}}
