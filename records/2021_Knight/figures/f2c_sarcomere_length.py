"""Fig. 2C (main.pdf p. 4): sarcomere length (µm) per culture condition, raster image embedded at ~300 dpi.

Each group plots hundreds of individual SL measurements (GLUC black circles, MM red squares, MPAT blue squares) that
overlap heavily, so no marker count or point value is readable: every group returns its bar only, countable false.
The mean is a black line ~63 px wide; the SEM error bar has caps ~31 px wide, black for MM and MPAT (merged with the
mean line into one block) and light grey for GLUC (drawn over the black points). Tick labels are part of the image,
so the y axis is calibrated from the raster tick marks, top to bottom the printed 2.5, 2.0, 1.5, 1.0, 0.5.
The same group's bar is returned once per sarcomere-length item (labels "<item suffix>/<group>").
"""
import numpy as np

from livinglit.figures.source import RASTER_UNCERTAINTY_PX_300DPI, calibrate

TICK_VALUES = [2.5, 2.0, 1.5, 1.0, 0.5]  # printed y tick labels, top to bottom (0.5 sits on the x axis)
GROUPS = ["GLUC", "MM", "MPAT"]  # x-axis order
ITEMS = {"sl_MM_v_GLUC": ("MM", "GLUC"), "sl_MPAT_v_MM": ("MPAT", "MM")}
MEAN_WIDTH = (55, 70)  # px, mean line
CAP_WIDTH = (26, 36)  # px, error-bar cap


def _bands(rows):
    out = []
    for r in rows:
        if out and r == out[-1][1] + 1:
            out[-1][1] = r
        else:
            out.append([r, r])
    return [tuple(b) for b in out]


def _centred_run(row, centre, tol=4):
    """Length of the run through the centre column, or 0 if it is not centred there within tol px."""
    c = int(round(centre))
    if not row[c]:
        return 0
    a = c
    while a > 0 and row[a - 1]:
        a -= 1
    b = c
    while b < len(row) - 1 and row[b + 1]:
        b += 1
    return b - a + 1 if abs((a + b) / 2 - centre) <= tol else 0


def read(fig):
    img, scale = fig.render(300)
    rgb = img[:, :, :3].astype(int)
    black = rgb.max(axis=2) < 100  # excludes the red and blue markers
    spread = rgb.max(axis=2) - rgb.min(axis=2)
    grey = (spread < 25) & (rgb.mean(axis=2) > 100) & (rgb.mean(axis=2) < 215)
    h, w = black.shape
    unc_px = RASTER_UNCERTAINTY_PX_300DPI

    # axes: y axis = columns with the most black; x axis = rows with the longest black extent right of it
    cc = black.sum(axis=0)
    yaxis = [c for c in range(w) if cc[c] >= 0.9 * cc.max()]
    ax0, ax1 = min(yaxis), max(yaxis)
    rc = black[:, ax1 + 1:].sum(axis=1)
    xaxis = [r for r in range(h) if rc[r] >= 0.8 * rc.max()]
    bottom, xr = min(xaxis), max(xaxis)

    # y ticks: black pixels just left of the axis
    bands = _bands([r for r in range(h) if black[r, ax0 - 8:ax0].sum() >= 6])
    if len(bands) != len(TICK_VALUES):
        raise ValueError(f"expected {len(TICK_VALUES)} y ticks, found {bands}")
    marks = []
    for (a, b), v in zip(bands, TICK_VALUES):
        g = 255 - img[a - 1:b + 2, ax0 - 8:ax0, :3].mean(axis=(1, 2))
        yc = float(np.sum(np.arange(a - 1, b + 2) * g) / g.sum())
        marks.append((fig.to_page(0, yc, scale)[1], v))
    cal = calibrate(marks)
    misfit_pt = cal.residual / abs(cal.slope)
    top = bands[0][0]

    # x ticks: columns black all the way down a short stub below the x axis
    stub = black[xr + 1:xr + 7, ax1 + 1:].all(axis=0)
    xb = _bands([c + ax1 + 1 for c in np.where(stub)[0]])
    if len(xb) != len(GROUPS):
        raise ValueError(f"expected {len(GROUPS)} x ticks, found {xb}")
    centres = {g: (a + b) / 2 for g, (a, b) in zip(GROUPS, xb)}

    lu = (unc_px + 1.0) / scale + misfit_pt  # line centre or edge: lines are 1–4 px thick
    per_group = {}
    for g in GROUPS:
        runs = {r: _centred_run(black[r], centres[g]) for r in range(top, bottom)}
        mb = _bands([r for r, n in runs.items() if MEAN_WIDTH[0] <= n <= MEAN_WIDTH[1]])
        if len(mb) != 1:
            raise ValueError(f"{g}: expected one mean line, found {mb}")
        my = (mb[0][0] + mb[0][1]) / 2
        # upper cap: black cap-width rows joined to the mean line (MM, MPAT), else the grey cap above it (GLUC)
        start = mb[0][0] - 1
        while CAP_WIDTH[1] < runs[start] < MEAN_WIDTH[0]:  # anti-aliased edge of the mean line
            start -= 1
        r = start
        while CAP_WIDTH[0] <= runs[r] <= CAP_WIDTH[1]:
            r -= 1
        if r < start:
            cy = r + 1  # top edge of the merged cap/bar block
        else:
            g_runs = {q: _centred_run(grey[q], centres[g]) for q in range(mb[0][0] - 20, mb[0][0])}
            cb = _bands([q for q, n in g_runs.items() if CAP_WIDTH[0] <= n <= CAP_WIDTH[1]])
            if not cb:
                raise ValueError(f"{g}: no upper error-bar cap")
            cy = (cb[-1][0] + cb[-1][1]) / 2
        my_pt, cy_pt = fig.to_page(0, my, scale)[1], fig.to_page(0, cy, scale)[1]
        mlo, mhi = cal.interval(my_pt, lu)
        elo, ehi = cal.interval(cy_pt, lu)
        per_group[g] = {"points": [], "countable": False,
                        "bar": {"mean": [cal.value(my_pt), mlo, mhi], "error": [cal.value(cy_pt), elo, ehi]}}

    out = {}
    for suffix, pair in ITEMS.items():
        for g in pair:
            out[f"{suffix}/{g}"] = per_group[g]
    return {"groups": out}
