"""Fig. 1C (main.pdf p. 3): cellular circularity (AU) per culture condition, raster image embedded at ~300 dpi.

Each group plots its replicate points with a black mean line and an error bar (SEM per legend). GLUC markers are
black circles, GLPAT pink circles (pink error bar), MM red squares, MPAT blue triangles. Tick labels are part of the
image, so the y axis is calibrated from the raster tick marks, taken top to bottom as the printed 0.6, 0.4, 0.2.
Markers are separated from the 2–3 px mean lines and error bars by a morphological opening (5 × 5 ellipse).
The same group's points are returned once per circularity item (labels "<item suffix>/<group>"), because a figure
label links to one item.
"""
import cv2
import numpy as np

from livinglit.figures.source import (RASTER_UNCERTAINTY_PX_300DPI, blobs, calibrate, colour_mask, dark_mask,
                                      point)

TICK_VALUES = [0.6, 0.4, 0.2]  # printed y tick labels, top to bottom
GROUPS = ["GLUC", "GLPAT", "MM", "MPAT"]  # x-axis order
COLOURS = {"GLPAT": (230, 30, 120), "MM": (230, 0, 0), "MPAT": (20, 40, 200)}
ITEMS = {  # item suffix -> its two groups
    "MPAT_v_GLUC": ("MPAT", "GLUC"), "MM_v_GLUC": ("MM", "GLUC"), "MM_v_GLPAT": ("MM", "GLPAT"),
    "GLPAT_v_GLUC": ("GLPAT", "GLUC"), "MPAT_v_GLPAT": ("MPAT", "GLPAT"), "MPAT_v_MM": ("MPAT", "MM"),
}
HALF = 42  # px either side of a group's x tick


def _bands(rows):
    """Contiguous runs of row indices -> list of (start, end)."""
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
    h, w = dark.shape
    unc_px = RASTER_UNCERTAINTY_PX_300DPI

    # axes: y axis = column with the longest dark vertical run; x axis = row with the longest dark run below it
    ycol_counts = dark.sum(axis=0)
    yaxis = [c for c in range(w) if ycol_counts[c] >= 0.9 * ycol_counts.max()]
    ax0, ax1 = min(yaxis), max(yaxis)
    top, axis_end = max(_bands(list(np.where(dark[:, ax0])[0])), key=lambda b: b[1] - b[0])  # the axis line itself
    xrow_counts = dark[:, ax1 + 1:].sum(axis=1)
    xaxis = [r for r in range(top, axis_end + 3) if xrow_counts[r] >= 0.9 * xrow_counts[top:axis_end + 3].max()]
    bottom = min(xaxis)

    # y ticks: dark pixels just left of the axis
    tick_rows = [r for r in range(top, bottom) if dark[r, ax0 - 8:ax0].sum() >= 6]
    bands = _bands(tick_rows)
    if len(bands) != len(TICK_VALUES):
        raise ValueError(f"expected {len(TICK_VALUES)} y ticks, found {bands}")
    marks = []
    for (a, b), v in zip(bands, TICK_VALUES):
        g = (255 - img[a - 1:b + 2, ax0 - 8:ax0].mean(axis=(1, 2)))
        yc = float(np.sum(np.arange(a - 1, b + 2) * g) / g.sum())
        marks.append((fig.to_page(0, yc, scale)[1], v))
    cal = calibrate(marks)
    misfit_pt = cal.residual / abs(cal.slope)

    # x ticks below the x axis give the group centres
    below = dark[max(xaxis) + 1:max(xaxis) + 10, :]
    tick_cols = [c for c in range(ax1 + 1, w) if below[:, c].sum() >= 6]
    xb = _bands(tick_cols)
    if len(xb) != len(GROUPS):
        raise ValueError(f"expected {len(GROUPS)} x ticks, found {xb}")
    centres = {g: (a + b) / 2 for g, (a, b) in zip(GROUPS, xb)}

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    per_group = {}
    for g in GROUPS:
        c0, c1 = int(centres[g] - HALF), int(centres[g] + HALF)
        region = np.zeros_like(dark)
        region[top:bottom, c0:c1] = True
        raw = (dark if g == "GLUC" else colour_mask(img, COLOURS[g], 60)) & region
        opened = cv2.morphologyEx(raw.astype(np.uint8), cv2.MORPH_OPEN, kernel).astype(bool)
        found = blobs(opened, min_area=40, max_area=400)
        n_raw, lab, stats, _ = cv2.connectedComponentsWithStats(raw.astype(np.uint8), connectivity=8)
        areas = sorted(b["area"] for b in found)
        typical = areas[len(areas) // 2]
        pts = []
        for b in sorted(found, key=lambda b: b["y"]):
            raw_area = stats[lab[int(round(b["y"])), int(round(b["x"]))], cv2.CC_STAT_AREA]
            touches_line = raw_area > 1.5 * typical  # marker merged with a mean line or error bar before opening
            u = (unc_px + (1.0 if touches_line else 0.0)) / scale + misfit_pt
            bx, by, bw, bh = b["box"]  # plotted position = marker box centre (a triangle's centroid sits low)
            at = fig.to_page(bx + (bw - 1) / 2, by + (bh - 1) / 2, scale)
            pts.append(point(cal, at[1], u, at))

        # mean line (~58 px wide, black) and upper error-bar cap (~28 px wide, black or group colour)
        lines = dark | (colour_mask(img, COLOURS[g], 60) if g in COLOURS else dark)
        runs = {r: _centred_run(lines[r], centres[g]) for r in range(top, bottom)}
        mean_rows = [r for r, n in runs.items() if 50 <= n <= 62]
        mb = _bands(mean_rows)
        if len(mb) != 1:
            raise ValueError(f"{g}: expected one mean line, found {mb}")
        my = (mb[0][0] + mb[0][1]) / 2
        cap_rows = [r for r, n in runs.items() if 24 <= n <= 32 and r < mb[0][0]]
        cb = _bands(cap_rows)
        if not cb:
            raise ValueError(f"{g}: no upper error-bar cap")
        cy = (cb[-1][0] + cb[-1][1]) / 2  # the cap nearest above the mean
        lu = (unc_px + 1.0) / scale + misfit_pt  # line centre: 2–3 px thick
        my_pt, cy_pt = fig.to_page(0, my, scale)[1], fig.to_page(0, cy, scale)[1]
        mlo, mhi = cal.interval(my_pt, lu)
        elo, ehi = cal.interval(cy_pt, lu)
        per_group[g] = {"points": pts, "countable": True,
                        "bar": {"mean": [cal.value(my_pt), mlo, mhi], "error": [cal.value(cy_pt), elo, ehi]}}

    out = {}
    for suffix, pair in ITEMS.items():
        for g in pair:
            out[f"{suffix}/{g}"] = per_group[g]
    return {"groups": out}
