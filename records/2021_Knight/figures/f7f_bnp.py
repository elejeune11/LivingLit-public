"""Fig. 7F (main.pdf p. 11): BNP+ cells (%) in CUSO-1 hiPSC-CMs, GLUC, MM and MPAT with DFO - and +; the page is one
raster image embedded at ~300 dpi.

Each group plots its replicate points (one per induction) with a black mean line (~42 px wide) and an SEM error bar
in the group's colour (GLUC black, MM red, MPAT blue); all markers are circles (~12 px across).
Tick labels are part of the image, so the y axis is calibrated from the five raster tick marks left of the axis,
taken top to bottom as the printed 40, 30, 20, 10, 0 (0 sits on the x axis). Group centres are the five raster tick
marks below the x axis, in x order GLUC, MM -, MM +, MPAT -, MPAT +.
Markers touch error-bar caps of their own colour, and three GLUC markers overlap one another, so markers are not
taken as connected blobs: a marker centre is a peak of the distance transform of the group's colour mask (bars, caps
and lines are 3-5 px thick and peak lower). A peak lower than the typical marker radius (a marker partly covered by
the black mean line or a neighbour) gets the shortfall added to its interval, and every point gets 1 px for the
peak's pixel grid.
The same group's points are returned once per item (labels "<item suffix>/<group>"), because a figure label links to
one item.
"""
import cv2
import numpy as np
from scipy.ndimage import label, maximum_filter

from livinglit.figures.source import RASTER_UNCERTAINTY_PX_300DPI, calibrate, colour_mask, dark_mask, point

TICK_VALUES = [40, 30, 20, 10, 0]  # printed y tick labels, top to bottom
GROUPS = ["GLUC", "MM_VEH", "MM_DFO", "MPAT_VEH", "MPAT_DFO"]  # x order
COLOURS = {"GLUC": (0, 0, 0), "MM": (255, 0, 0), "MPAT": (0, 55, 255)}
EXPECTED = {"GLUC": 4, "MM_VEH": 4, "MM_DFO": 4, "MPAT_VEH": 3, "MPAT_DFO": 3}  # markers visible per group
ITEMS = {  # item suffix -> its two groups
    "MM_VEH_v_GLUC": ("MM_VEH", "GLUC"), "MM_DFO_v_MM_VEH": ("MM_DFO", "MM_VEH"),
    "MPAT_DFO_v_MPAT_VEH": ("MPAT_DFO", "MPAT_VEH"), "MPAT_DFO_v_GLUC": ("MPAT_DFO", "GLUC"),
}
HALF = 28  # px either side of a group's centre (groups are ~63 px apart)
MEAN_HALF = 18  # a mean-line row is black over centre +- 18 px
CAP_HALF = 8  # a cap row is filled over centre +- 8 px
LINE_MAX = 6  # px: a mean line or cap band is at most this thick
PEAK_MIN = 4.0  # px: distance-transform peak of a marker (radius ~6); lines and bars peak at <= 3


def _bands(rows):
    """Contiguous runs of row indices -> list of (start, end)."""
    out = []
    for r in rows:
        if out and r == out[-1][1] + 1:
            out[-1][1] = r
        else:
            out.append([r, r])
    return [tuple(b) for b in out]


def _mask(img, g):
    return colour_mask(img, COLOURS[g.split("_")[0]], 110 if g == "GLUC" else 90)


def read(fig):
    img, scale = fig.render(300)
    dark = dark_mask(img, 110)
    h, w = dark.shape
    unc_px = RASTER_UNCERTAINTY_PX_300DPI

    # y axis = the columns with the longest dark vertical runs
    counts = dark.sum(axis=0)
    yaxis = [c for c in range(w) if counts[c] >= 0.9 * counts.max()]
    ax0, ax1 = min(yaxis), max(yaxis)
    axc = int(np.argmax(counts))  # the axis's edge column has JPEG gaps
    top, bottom = max(_bands(list(np.where(dark[:, axc])[0])), key=lambda b: b[1] - b[0])

    # y ticks: dark pixels just left of the axis
    tick_rows = [r for r in range(max(top - 3, 1), min(bottom + 4, h - 1)) if dark[r, ax0 - 10:ax0 - 1].sum() >= 8]
    bands = _bands(tick_rows)
    if len(bands) != len(TICK_VALUES):
        raise ValueError(f"expected {len(TICK_VALUES)} y ticks, found {bands}")
    marks = []
    for (a, b), v in zip(bands, TICK_VALUES):
        g = 255 - img[a - 1:b + 2, ax0 - 10:ax0 - 1].mean(axis=(1, 2))
        yc = float(np.sum(np.arange(a - 1, b + 2) * g) / g.sum())
        marks.append((fig.to_page(0, yc, scale)[1], v))
    cal = calibrate(marks)
    misfit_pt = cal.residual / abs(cal.slope)
    xaxis = bands[-1]

    # group centres: tick marks below the x axis (dark over 6 rows just below it), right of the y axis
    below = dark[xaxis[1] + 2:xaxis[1] + 8]
    cols = [c for c in range(ax1 + 3, w) if below[:, c].all()]
    xt = []
    for c in cols:
        if xt and c == xt[-1][-1] + 1:
            xt[-1].append(c)
        else:
            xt.append([c])
    if len(xt) != len(GROUPS):
        raise ValueError(f"expected {len(GROUPS)} x ticks, found {[(t[0], t[-1]) for t in xt]}")
    centre_by = {g: float(np.mean(t)) for g, t in zip(GROUPS, xt)}

    black = _mask(img, "GLUC")
    plot_rows = slice(top + 5, xaxis[0] - 2)
    found_by, mean_by, mask_by = {}, {}, {}
    for g in GROUPS:
        cx = centre_by[g]
        m0, m1 = int(round(cx - MEAN_HALF)), int(round(cx + MEAN_HALF)) + 1
        # significance lines (~111 px) run on past both ends of a mean line (~42 px)
        mrows = [r for r in range(plot_rows.start, plot_rows.stop) if black[r, m0:m1].all()
                 and not (black[r, m0 - 8] and black[r, m1 + 7])]
        # one row filled across overlapping GLUC markers is not a line (a mean line is 3-4 px thick)
        mb = [b for b in _bands(mrows) if 2 <= b[1] - b[0] + 1 <= LINE_MAX]
        if len(mb) != 1:
            raise ValueError(f"{g}: expected one mean line, found {_bands(mrows)}")
        mean_by[g] = mb[0]

        mask = np.zeros_like(dark)
        x0, x1 = int(cx - HALF), int(cx + HALF) + 1
        mask[plot_rows, x0:x1] = _mask(img, g)[plot_rows, x0:x1]
        mask_by[g] = mask
        dt = cv2.distanceTransform(mask.astype(np.uint8), cv2.DIST_L2, 5)
        peaks = (dt == maximum_filter(dt, size=7)) & (dt >= PEAK_MIN)
        lab, n = label(peaks)
        found = []
        for i in range(1, n + 1):
            ys, xs = np.where(lab == i)
            found.append((float(xs.mean()), float(ys.mean()), float(dt[ys, xs].max())))
        if len(found) != EXPECTED[g]:
            raise ValueError(f"{g}: expected {EXPECTED[g]} markers, found {[(round(x), round(y)) for x, y, _ in found]}")
        found_by[g] = found

    radius = float(np.median([d for g in GROUPS for _, _, d in found_by[g]]))
    per_group = {}
    for g in GROUPS:
        pts = []
        for x, y, d in sorted(found_by[g], key=lambda t: t[1]):
            u = (unc_px + 1.0 + max(radius - d, 0.0)) / scale + misfit_pt
            at = fig.to_page(x, y, scale)
            pts.append(point(cal, at[1], u, at))

        # upper cap: nearest band above the mean line filled over centre +- CAP_HALF in the group's colour;
        # a band thicker than a cap has markers on it, and its whole thickness goes into the interval
        cx = centre_by[g]
        c0, c1 = int(round(cx - CAP_HALF)), int(round(cx + CAP_HALF)) + 1
        mt, mbot = mean_by[g]
        cap_rows = [r for r in range(plot_rows.start, mt - 1) if mask_by[g][r, c0:c1].all()]
        cb = _bands(cap_rows)
        if not cb:
            raise ValueError(f"{g}: no upper error-bar cap")
        a, b = cb[-1]
        cy = (a + b) / 2
        cu = (unc_px + 1.0 + max((b - a + 1) - LINE_MAX, 0) / 2) / scale + misfit_pt
        my = (mt + mbot) / 2
        lu = (unc_px + 1.0) / scale + misfit_pt
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
