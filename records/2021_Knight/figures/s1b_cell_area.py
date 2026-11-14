"""Fig. S1B (mmc1.pdf p. 3): CUSO-2 cell area (µm2) per culture condition and AMVCMs, raster image embedded at ~300 dpi.

Each group plots hundreds of individual cell areas (legend: 275 or more cells per group; GLUC black, MM red, MPAT blue
circles, AMVCM orange triangles) that overlap heavily, so no marker count or point value is readable: every group returns
its bar only, countable false. The legend says "Black bars indicate means"; there are no error bars, so only the mean is
read. The mean is a black line ~61 px wide and ~3 px thick, drawn over the coloured markers. Tick labels are part of the
image, so the y axis is calibrated from the raster tick marks, top to bottom the printed 30000, 20000, 10000, 0.
Only MM, MPAT and AMVCM are read (the groups figures-needed lists); the same group's bar is returned once per item
(labels "<item suffix>/<group>").
"""
import numpy as np

from livinglit.figures.source import RASTER_UNCERTAINTY_PX_300DPI, calibrate

TICK_VALUES = [30000, 20000, 10000, 0]  # printed y tick labels, top to bottom (0 sits on the x axis)
GROUPS = ["GLUC", "MM", "MPAT", "AMVCM"]  # x-axis order
ITEMS = {"area_MM_v_AMVCM": ("MM", "AMVCM"), "area_MPAT_v_AMVCM": ("MPAT", "AMVCM")}
READ = ["MM", "MPAT", "AMVCM"]
MEAN_WIDTH = (57, 66)  # px, mean line
STEP = 5  # px: the mean line's run is at least this much wider than the rows just above and below it


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
    black = rgb.max(axis=2) < 100  # excludes the red, blue and orange markers
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
    bands = _bands([r for r in range(xr + 1) if black[r, ax0 - 6:ax0].sum() >= 5])  # below: x labels
    if len(bands) != len(TICK_VALUES):
        raise ValueError(f"expected {len(TICK_VALUES)} y ticks, found {bands}")
    marks = []
    for (a, b), v in zip(bands, TICK_VALUES):
        g = 255 - img[a - 1:b + 2, ax0 - 6:ax0, :3].mean(axis=(1, 2))
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

    lu = (unc_px + 1.0) / scale + misfit_pt  # line centre: the line is ~3 px thick
    per_group = {}
    for g in READ:
        runs = {r: _centred_run(black[r], centres[g]) for r in range(top - 1, bottom + 1)}
        cand = _bands([r for r in range(top, bottom) if MEAN_WIDTH[0] <= runs[r] <= MEAN_WIDTH[1]])
        mb = [(a, b) for a, b in cand
              if min(runs[r] for r in range(a, b + 1)) - max(runs[a - 1], runs[b + 1]) >= STEP and b - a <= 4]
        if len(mb) != 1:
            raise ValueError(f"{g}: expected one mean line, found {mb} among {cand}")
        my_pt = fig.to_page(0, (mb[0][0] + mb[0][1]) / 2, scale)[1]
        mlo, mhi = cal.interval(my_pt, lu)
        per_group[g] = {"points": [], "countable": False, "bar": {"mean": [cal.value(my_pt), mlo, mhi]}}

    out = {}
    for suffix, pair in ITEMS.items():
        for g in pair:
            out[f"{suffix}/{g}"] = per_group[g]
    return {"groups": out}
