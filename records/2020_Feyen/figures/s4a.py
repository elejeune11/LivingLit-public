"""Fig. S4A (mmc1.pdf p. 8): IK1 density at -140 mV and cell capacitance, RPMI/B27 vs MM.

Raster image. Both panels are dot plots whose markers overlap each other and the mean
and error-bar lines, so they are not countable: only each group's mean line and the
upper end of its error bar are read. Mean lines are ~70 px and caps ~35 px wide at
300 dpi, centred on the group; RPMI/B27 markers are grey, so a dark threshold keeps
only black (lines and MM markers). Axes are calibrated from the detected y tick marks,
labelled with the printed tick values.
"""
import numpy as np

from livinglit.figures.source import calibrate, dark_mask, point

DPI = 300
UNC_PX = 0.6
PLOT_ROWS = (90, 450)  # the plot area, below the group labels above the IK1 panel
INNER_ROWS = (100, 438)  # inside the plot area, clear of the x axis lines (rows 96-97 and 443)
# panel: (y-axis column px, printed tick values top to bottom, {label: (x window px)})
PANELS = {
    "ik1": (150, [0, -5, -10, -15, -20], {"ik1_rpmi": (160, 262), "ik1_mm": (272, 372)}),
    "cap": (512, [100, 75, 50, 25, 0], {"cap_rpmi": (522, 624), "cap_mm": (634, 736)}),
}


def _runs(flags):
    """Groups of consecutive indices where flags is true, as (start, end)."""
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


def _run_at(row, c):
    """Length, start and end of the dark run through column c."""
    if not row[c]:
        return 0, c, c
    a, b = c, c
    while a > 0 and row[a - 1]:
        a -= 1
    while b < len(row) - 1 and row[b + 1]:
        b += 1
    return b - a + 1, a, b


def _ticks(dm, axis_col):
    """Rows of the tick marks left of the y axis (>= 6 of the 14 px left of it dark)."""
    flags = [PLOT_ROWS[0] <= r <= PLOT_ROWS[1] and dm[r, axis_col - 14:axis_col].sum() >= 6
             for r in range(dm.shape[0])]
    return [(a + b) / 2 for a, b in _runs(flags)]


def _bar(dm, x0, x1):
    """Mean line (dark run >= 60 px inside the window) and its two caps (30-38 px runs centred on it)."""
    H = dm.shape[0]
    mean_rows, centre = [], None
    for r in range(INNER_ROWS[0], INNER_ROWS[1] + 1):
        row = dm[r, x0:x1]
        for a, b in _runs(list(row)):
            if b - a + 1 >= 60:
                mean_rows.append(r)
                centre = x0 + (a + b) / 2
    groups = _runs([r in mean_rows for r in range(H)])
    if len(groups) != 1:
        raise ValueError(f"expected one mean line in columns {x0}-{x1}, found {len(groups)}")
    m0, m1 = groups[0]
    c = int(round(centre))

    def cap(rows):
        found = []
        for r in rows:
            n, a, b = _run_at(dm[r], c)
            if 30 <= n <= 38 and abs((a + b) / 2 - centre) <= 2:
                found.append(r)
            elif found:
                break
        if not found:
            raise ValueError(f"no cap found from the mean line at column {c}")
        return sum(found) / len(found)

    upper = cap(range(m0 - 2, 0, -1))
    lower = cap(range(m1 + 2, H))
    return (m0 + m1) / 2, upper, lower, centre


def read(fig):
    img, scale = fig.render(DPI)
    dm = dark_mask(img, 110)
    out = {}
    for axis_col, values, groups in PANELS.values():
        rows = _ticks(dm, axis_col)
        if len(rows) != len(values):
            raise ValueError(f"expected {len(values)} y ticks at column {axis_col}, found {rows}")
        cal = calibrate(list(zip(rows, values)))
        res = cal.residual
        for label, (x0, x1) in groups.items():
            m, up, _lo, cx = _bar(dm, x0, x1)
            pm = point(cal, m, UNC_PX, fig.to_page(cx, m, scale))
            pu = point(cal, up, UNC_PX, fig.to_page(cx, up, scale))
            out[label] = {
                "points": [],
                "countable": False,
                "bar": {"mean": [pm["value"], pm["lo"] - res, pm["hi"] + res],
                        "error": [pu["value"], pu["lo"] - res, pu["hi"] + res]},
            }
    return {"groups": out}
