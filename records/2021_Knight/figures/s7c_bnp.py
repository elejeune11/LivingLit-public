"""Fig. S7C (mmc1.pdf p. 15): BNP+ cells (%) in CUSO-2 hiPSC-CMs, GLUC and MPAT with DFO - and +; the figure is one
raster image embedded at ~590 dpi, read at 600 dpi.

Each group plots its replicate points with a black mean line (~107 px wide, ~8 px thick at 600 dpi) and an SEM
error bar in the group's colour (GLUC black, MPAT blue). GLUC and MPAT DFO - markers are circles (~19 px across),
MPAT DFO + markers are squares (~17 px across).
Tick labels are part of the image, so the y axis is calibrated from the five raster tick marks left of the axis,
taken top to bottom as the printed 40, 30, 20, 10, 0 (0 sits on the x axis). Group centres are the three raster
tick marks below the x axis, in x order GLUC, MPAT DFO -, MPAT DFO +.
Significance lines (~250 px wide, ~4 px thick) and their stars lie above the points; each group's search starts
below the lowest significance line over its centre. Markers touch error-bar caps of their own colour (the MPAT DFO +
square at ~24 sits on the upper cap), so a marker centre is a peak of the distance transform of the group's colour
mask (bars, caps and lines are 4-8 px thick and peak at <= 4.5). A peak lower than the typical marker radius gets
the shortfall added to its interval, and every point gets 1 px for the peak's pixel grid.
The same group's points are returned once per item (labels "<item suffix>/<group>"), because a figure label links to
one item.
"""
import cv2
import numpy as np
from scipy.ndimage import label, maximum_filter

from livinglit.figures.source import RASTER_UNCERTAINTY_PX_300DPI, calibrate, colour_mask, point

DPI = 600
TICK_VALUES = [40, 30, 20, 10, 0]  # printed y tick labels, top to bottom
GROUPS = ["GLUC", "MPAT_VEH", "MPAT_DFO"]  # x order
COLOURS = {"GLUC": (0, 0, 0), "MPAT": (0, 0, 255)}
EXPECTED = {"GLUC": 5, "MPAT_VEH": 5, "MPAT_DFO": 5}  # markers visible per group
ITEMS = {  # item suffix -> its two groups
    "MPAT_VEH_v_GLUC": ("MPAT_VEH", "GLUC"), "MPAT_DFO_v_MPAT_VEH": ("MPAT_DFO", "MPAT_VEH"),
}
HALF = 75  # px either side of a group's centre (groups are ~165 px apart)
MEAN_HALF = 45  # a mean-line row is black over centre +- 45 px ...
MEAN_OUT = 62  # ... and not at centre +- 62 px (significance lines run on past a mean line)
SIG_MIN = 150  # px: a black row run at least this long above the x axis is a significance line
CAP_HALF = 20  # a cap row is filled over centre +- 20 px (caps are ~53 px wide)
LINE_MAX = 10  # px: a mean line or cap band is at most this thick
PEAK_MIN = 6.5  # px: distance-transform peak of a marker (radius ~8-9); lines and bars peak at <= 4.5


def _bands(rows):
    """Contiguous runs of indices -> list of (start, end)."""
    out = []
    for r in rows:
        if out and r == out[-1][1] + 1:
            out[-1][1] = r
        else:
            out.append([r, r])
    return [tuple(b) for b in out]


def _mask(img, g):
    return colour_mask(img, COLOURS[g.split("_")[0]], 110)


def read(fig):
    img, scale = fig.render(DPI)
    black = _mask(img, "GLUC")
    h, w = black.shape
    unc0 = RASTER_UNCERTAINTY_PX_300DPI / (300 / 72)  # pt

    # y axis = the columns with the longest black vertical runs
    counts = black.sum(axis=0)
    axc = int(np.argmax(counts))
    yaxis = [c for c in range(w) if counts[c] >= 0.9 * counts.max()]
    ax0, ax1 = min(yaxis), max(yaxis)
    top, bottom = max(_bands(list(np.where(black[:, axc])[0])), key=lambda b: b[1] - b[0])

    # y ticks: black pixels just left of the axis
    tick_rows = [r for r in range(max(top - 3, 1), min(bottom + 4, h - 1)) if black[r, ax0 - 15:ax0 - 1].all()]
    bands = _bands(tick_rows)
    if len(bands) != len(TICK_VALUES):
        raise ValueError(f"expected {len(TICK_VALUES)} y ticks, found {bands}")
    marks = []
    for (a, b), v in zip(bands, TICK_VALUES):
        g = 255 - img[a - 1:b + 2, ax0 - 15:ax0 - 1].mean(axis=(1, 2))
        yc = float(np.sum(np.arange(a - 1, b + 2) * g) / g.sum())
        marks.append((fig.to_page(0, yc, scale)[1], v))
    cal = calibrate(marks)
    misfit_pt = cal.residual / abs(cal.slope)
    xaxis = bands[-1]

    # group centres: tick marks below the x axis (black over 10 rows just below it), right of the y axis
    below = black[xaxis[1] + 3:xaxis[1] + 13]
    xt = _bands([c for c in range(ax1 + 5, w) if below[:, c].all()])
    if len(xt) != len(GROUPS):
        raise ValueError(f"expected {len(GROUPS)} x ticks, found {xt}")
    centre_by = {g: (a + b) / 2 for g, (a, b) in zip(GROUPS, xt)}

    # significance lines: long thin black runs above the x axis
    sig = []
    for r in range(top, xaxis[0] - 2):
        for a, b in _bands(list(np.where(black[r, ax1 + 5:])[0] + ax1 + 5)):
            if b - a + 1 >= SIG_MIN:
                sig.append((r, a, b))

    found_by, mean_by, mask_by, start_by = {}, {}, {}, {}
    for g in GROUPS:
        cx = centre_by[g]
        over = [r for r, a, b in sig if a <= cx <= b]
        start = (max(over) + 3) if over else top + 5
        start_by[g] = start
        rows = range(start, xaxis[0] - 2)
        m0, m1 = int(round(cx - MEAN_HALF)), int(round(cx + MEAN_HALF)) + 1
        o0, o1 = int(round(cx - MEAN_OUT)), int(round(cx + MEAN_OUT))
        mrows = [r for r in rows if black[r, m0:m1].all() and not (black[r, o0] or black[r, o1])]
        mb = [b for b in _bands(mrows) if 3 <= b[1] - b[0] + 1 <= LINE_MAX]
        if len(mb) != 1:
            raise ValueError(f"{g}: expected one mean line, found {_bands(mrows)}")
        mean_by[g] = mb[0]

        mask = np.zeros_like(black)
        x0, x1 = int(cx - HALF), int(cx + HALF) + 1
        mask[start:xaxis[0] - 2, x0:x1] = _mask(img, g)[start:xaxis[0] - 2, x0:x1]
        mask_by[g] = mask
        dt = cv2.distanceTransform(mask.astype(np.uint8), cv2.DIST_L2, 5)
        peaks = (dt == maximum_filter(dt, size=9)) & (dt >= PEAK_MIN)
        lab, n = label(peaks)
        found = []
        for i in range(1, n + 1):
            ys, xs = np.where(lab == i)
            found.append((float(xs.mean()), float(ys.mean()), float(dt[ys, xs].max())))
        if len(found) != EXPECTED[g]:
            raise ValueError(f"{g}: expected {EXPECTED[g]} markers, found {[(round(x), round(y), round(d, 1)) for x, y, d in found]}")
        found_by[g] = found

    radius_by = {s: float(np.median([d for g in GROUPS if (g == "MPAT_DFO") == (s == "square") for _, _, d in found_by[g]]))
                 for s in ("circle", "square")}
    per_group = {}
    for g in GROUPS:
        radius = radius_by["square" if g == "MPAT_DFO" else "circle"]
        pts = []
        for x, y, d in sorted(found_by[g], key=lambda t: t[1]):
            u = unc0 + (1.0 + max(radius - d, 0.0)) / scale + misfit_pt
            at = fig.to_page(x, y, scale)
            pts.append(point(cal, at[1], u, at))

        # upper cap: nearest band above the mean line filled over centre +- CAP_HALF in the group's colour;
        # a band thicker than a cap has a marker on it, and its excess thickness goes into the interval
        cx = centre_by[g]
        c0, c1 = int(round(cx - CAP_HALF)), int(round(cx + CAP_HALF)) + 1
        mt, mbot = mean_by[g]
        cap_rows = [r for r in range(start_by[g], mt - 1) if mask_by[g][r, c0:c1].all()]
        cb = _bands(cap_rows)
        if not cb:
            raise ValueError(f"{g}: no upper error-bar cap")
        a, b = cb[-1]
        cy = (a + b) / 2
        cu = unc0 + (1.0 + max((b - a + 1) - LINE_MAX, 0) / 2) / scale + misfit_pt
        my = (mt + mbot) / 2
        lu = unc0 + 1.0 / scale + misfit_pt
        my_pt, cy_pt = fig.to_page(0, my, scale)[1], fig.to_page(0, cy, scale)[1]
        mlo, mhi = cal.interval(my_pt, lu)
        elo, ehi = cal.interval(cy_pt, cu)
        per_group[g] = {"points": pts, "countable": True,
                        "bar": {"mean": [cal.value(my_pt), mlo, mhi], "error": [cal.value(cy_pt), elo, ehi]}}

    out = {}
    for suffix, pair in ITEMS.items():
        for g in pair:
            out[f"{suffix}/{g}"] = per_group[g]
    return {"groups": out}
