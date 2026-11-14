"""Fig. S1G (mmc1.pdf p. 3, lower right panel): MLC-2V+ cells (%) of CUSO-2 hiPSC-CMs per culture condition,
raster image embedded at ~410 dpi and rendered at 300 dpi.

Each group plots its replicate points over a black mean line (~58 px wide) and an error bar (mean ± SEM per legend)
with caps ~27 px wide in the group's colour: GLUC black circles, MM red squares, MPAT blue triangles. Tick labels are
part of the image, so the y axis is calibrated from the five raster tick marks, taken top to bottom as the printed
100, 90, 80, 70, 60 (the 60 tick sits on the x axis). The crop starts below the 'N.S' line and right of the tick
labels. A group's ink is its colour mask (black: dark and neither red nor blue); markers are separated from the 1–3 px
lines of the same colour by a morphological opening (4 × 4 ellipse; 5 × 5 erases the ~30 px triangles), and positions are the opened blob's box centres.
Markers whose raw component is larger than the opened blob (drawn over the bar), or with black pixels next to them,
carry 2 px of extra interval (the opening trims a marker where the 2 px bar runs through it).
The same group's readings are returned once per item that figures-needed lists (labels "<item suffix>/<group>").
"""
import cv2
import numpy as np

from livinglit.figures.source import (RASTER_UNCERTAINTY_PX_300DPI, blobs, calibrate, colour_mask, dark_mask,
                                      point)

TICK_VALUES = [100, 90, 80, 70, 60]  # printed y tick labels, top to bottom
GROUPS = ["GLUC", "MM", "MPAT"]  # x-axis order
COLOURS = {"MM": (254, 0, 0), "MPAT": (0, 0, 255)}
COLOUR_TOL = 110  # antialiased line pixels reach (240, 96, 96)
ITEMS = {"mlc2v_omnibus": ("GLUC", "MM", "MPAT")}
HALF = 45  # px either side of a group's x tick
MEAN_RUN = (45, 70)  # px, mean line width (~58 px)
CAP_RUN = (18, 35)  # px, error-bar cap width (~27 px)
MIN_AREA = 8  # px, opened markers; what survives of a line crossing is smaller


def _bands(rows):
    """Contiguous runs of indices -> list of (start, end)."""
    out = []
    for r in rows:
        if out and r == out[-1][1] + 1:
            out[-1][1] = r
        else:
            out.append([r, r])
    return [tuple(b) for b in out]


def _centred_run(row, centre, tol=6):
    """Length of the run through the centre column, or 0 if the run is not centred there within tol px."""
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
    dark = dark_mask(img, 110)
    colour = {g: colour_mask(img, rgb, COLOUR_TOL) for g, rgb in COLOURS.items()}
    ink = {"GLUC": dark & ~colour["MM"] & ~colour["MPAT"], **colour}
    h, w = dark.shape
    unc_px = RASTER_UNCERTAINTY_PX_300DPI

    # axes: y axis = columns with the most black; x axis = rows with the most black right of it
    black = ink["GLUC"]
    cc = black.sum(axis=0)
    yaxis = [c for c in range(w) if cc[c] >= 0.9 * cc.max()]
    ax0, ax1 = min(yaxis), max(yaxis)
    rc = black[:, ax1 + 1:].sum(axis=1)
    xaxis = [r for r in range(h) if rc[r] >= 0.9 * rc.max()]
    bottom, xr = min(xaxis), max(xaxis)

    # y ticks: black pixels just left of the axis (the lowest one is level with the x axis)
    bands = _bands([r for r in range(xr + 1) if black[r, ax0 - 6:ax0].sum() >= 5])
    if len(bands) != len(TICK_VALUES):
        raise ValueError(f"expected {len(TICK_VALUES)} y ticks, found {bands}")
    marks = []
    for (a, b), v in zip(bands, TICK_VALUES):
        g = 255 - img[max(a - 1, 0):b + 2, ax0 - 6:ax0, :3].mean(axis=(1, 2))
        yc = float(np.sum(np.arange(max(a - 1, 0), b + 2) * g) / g.sum())
        marks.append((fig.to_page(0, yc, scale)[1], v))
    cal = calibrate(marks)
    misfit_pt = cal.residual / abs(cal.slope)

    # x ticks: columns black all the way down a short stub below the x axis
    stub = black[xr + 1:xr + 5, ax1 + 1:].all(axis=0)
    xb = _bands([c + ax1 + 1 for c in np.where(stub)[0]])
    if len(xb) != len(GROUPS):
        raise ValueError(f"expected {len(GROUPS)} x ticks, found {xb}")
    centres = {g: (a + b) / 2 for g, (a, b) in zip(GROUPS, xb)}

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
    lu = (unc_px + 1.0) / scale + misfit_pt  # line centre: 1–3 px thick
    out = {}
    for g in GROUPS:
        c0, c1 = int(centres[g] - HALF), int(centres[g] + HALF)
        raw = np.zeros_like(dark)
        raw[0:bottom, c0:c1] = ink[g][0:bottom, c0:c1]
        found = blobs(cv2.morphologyEx(raw.astype(np.uint8), cv2.MORPH_OPEN, kernel).astype(bool),
                      min_area=MIN_AREA, max_area=400)
        areas = sorted(b["area"] for b in found)
        typical = areas[len(areas) // 2]
        if any(not 0.5 * typical <= a <= 1.5 * typical for a in areas):
            raise ValueError(f"{g}: marker areas {areas} are not one marker each")
        _, lab, stats, _ = cv2.connectedComponentsWithStats(raw.astype(np.uint8), connectivity=8)
        pts = []
        for b in sorted(found, key=lambda b: b["y"]):
            bx, by, bw, bh = b["box"]
            touches = stats[lab[int(round(b["y"])), int(round(b["x"]))], cv2.CC_STAT_AREA] > 1.5 * b["area"]
            if g != "GLUC":  # black mean line next to a coloured marker
                near = np.zeros_like(dark)
                near[max(by - 2, 0):by + bh + 2, max(bx - 2, 0):bx + bw + 2] = True
                touches = touches or int((black & near).sum()) >= 3
            u = (unc_px + (2.0 if touches else 0.0)) / scale + misfit_pt
            at = fig.to_page(bx + (bw - 1) / 2, by + (bh - 1) / 2, scale)  # box centre (a triangle's centroid sits low)
            pts.append(point(cal, at[1], u, at))

        # black mean line (~58 px wide) and upper error-bar cap (~27 px wide, group colour); a marker drawn over a
        # line is counted as line so the run is not cut
        lines = np.zeros_like(dark)
        lines[0:bottom, c0:c1] = (ink[g] | black)[0:bottom, c0:c1]
        runs = {r: _centred_run(lines[r], centres[g]) for r in range(bottom)}
        mb = _bands([r for r, n in runs.items() if MEAN_RUN[0] <= n <= MEAN_RUN[1]])
        if len(mb) != 1:
            raise ValueError(f"{g}: expected one mean line, found {mb}")
        cb = _bands([r for r, n in runs.items() if CAP_RUN[0] <= n <= CAP_RUN[1] and r < mb[0][0]])
        if not cb:
            raise ValueError(f"{g}: no upper error-bar cap")
        my = (mb[0][0] + mb[0][1]) / 2
        cy = (cb[-1][0] + cb[-1][1]) / 2  # the cap nearest above the mean
        my_pt, cy_pt = fig.to_page(0, my, scale)[1], fig.to_page(0, cy, scale)[1]
        mlo, mhi = cal.interval(my_pt, lu)
        elo, ehi = cal.interval(cy_pt, lu)
        out[g] = {"points": pts, "countable": True,
                  "bar": {"mean": [cal.value(my_pt), mlo, mhi], "error": [cal.value(cy_pt), elo, ehi]}}
    return {"groups": {f"{item}/{g}": out[g] for item, groups in ITEMS.items() for g in groups}}
