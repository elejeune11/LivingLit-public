"""Fig. S1E (mmc1.pdf p. 3, upper right panel): circularity of MD-186C hiPSC-CMs, GLUC vs MPAT, raster image embedded
at ~410 dpi and rendered at 300 dpi.

Each group plots its replicate points over a black mean line and an error bar (mean ± SEM per legend). GLUC markers
are black circles, MPAT blue triangles drawn on top of the lines. Tick labels are part of the image, so the y axis is
calibrated from the four raster tick marks, taken top to bottom as the printed 0.8, 0.6, 0.4, 0.2 (the 0.2 tick sits
on the x axis). The crop starts below the significance line.
MPAT markers are the connected components of their colour; GLUC's black circles are separated from the 3 px mean
line, caps and bar by a morphological opening (5 × 5 ellipse). Positions are marker box centres. Markers that touch a
line carry 1 px of extra interval.
"""
import cv2
import numpy as np

from livinglit.figures.source import (RASTER_UNCERTAINTY_PX_300DPI, blobs, calibrate, colour_mask, dark_mask,
                                      point)

TICK_VALUES = [0.8, 0.6, 0.4, 0.2]  # printed y tick labels, top to bottom
GROUPS = ["GLUC", "MPAT"]  # x-axis order
COLOURS = {"MPAT": (3, 3, 193)}
HALF = 40  # px either side of a group's x tick
MEAN_RUN = (64, 80)  # px, mean line width (~72 px)
CAP_RUN = (28, 44)  # px, error-bar cap width (~35 px)


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
    h, w = dark.shape
    unc_px = RASTER_UNCERTAINTY_PX_300DPI

    # axes: y axis = columns with the most dark; x axis = rows with the most dark right of it
    cc = dark.sum(axis=0)
    yaxis = [c for c in range(w) if cc[c] >= 0.9 * cc.max()]
    ax0, ax1 = min(yaxis), max(yaxis)
    rc = dark[:, ax1 + 1:].sum(axis=1)
    xaxis = [r for r in range(h) if rc[r] >= 0.9 * rc.max()]
    bottom, xr = min(xaxis), max(xaxis)

    # y ticks: dark pixels just left of the axis (the lowest one is level with the x axis)
    bands = _bands([r for r in range(xr + 1) if dark[r, ax0 - 6:ax0].sum() >= 5])
    if len(bands) != len(TICK_VALUES):
        raise ValueError(f"expected {len(TICK_VALUES)} y ticks, found {bands}")
    marks = []
    for (a, b), v in zip(bands, TICK_VALUES):
        g = 255 - img[a - 1:b + 2, ax0 - 6:ax0, :3].mean(axis=(1, 2))
        yc = float(np.sum(np.arange(a - 1, b + 2) * g) / g.sum())
        marks.append((fig.to_page(0, yc, scale)[1], v))
    cal = calibrate(marks)
    misfit_pt = cal.residual / abs(cal.slope)

    # x ticks: columns dark all the way down a short stub below the x axis
    stub = dark[xr + 1:xr + 7, ax1 + 1:].all(axis=0)
    xb = _bands([c + ax1 + 1 for c in np.where(stub)[0]])
    if len(xb) != len(GROUPS):
        raise ValueError(f"expected {len(GROUPS)} x ticks, found {xb}")
    centres = {g: (a + b) / 2 for g, (a, b) in zip(GROUPS, xb)}

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    ring = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    lu = (unc_px + 1.0) / scale + misfit_pt  # line centre: 2–3 px thick
    out = {}
    for g in GROUPS:
        c0, c1 = int(centres[g] - HALF), int(centres[g] + HALF)
        region = np.zeros_like(dark)
        region[:bottom, c0:c1] = True
        if g == "GLUC":
            raw = dark & region
            found = blobs(cv2.morphologyEx(raw.astype(np.uint8), cv2.MORPH_OPEN, kernel).astype(bool),
                          min_area=60, max_area=400)
            n_raw, lab, stats, _ = cv2.connectedComponentsWithStats(raw.astype(np.uint8), connectivity=8)
        else:
            raw = colour_mask(img, COLOURS[g], 60) & region
            found = blobs(raw, min_area=60, max_area=400)
        areas = sorted(b["area"] for b in found)
        typical = areas[len(areas) // 2]
        if any(not 0.6 * typical <= a <= 1.4 * typical for a in areas):
            raise ValueError(f"{g}: marker areas {areas} are not one marker each")
        pts = []
        for b in sorted(found, key=lambda b: b["y"]):
            bx, by, bw, bh = b["box"]
            if g == "GLUC":  # merged with a mean line, cap or bar before the opening
                touches = stats[lab[int(round(b["y"])), int(round(b["x"]))], cv2.CC_STAT_AREA] > 1.5 * b["area"]
            else:  # dark pixels next to the marker
                m = np.zeros_like(dark)
                m[by:by + bh, bx:bx + bw] = raw[by:by + bh, bx:bx + bw]
                near = cv2.dilate(m.astype(np.uint8), ring).astype(bool) & ~m
                touches = int(dark[near].sum()) >= 3
            u = (unc_px + (1.0 if touches else 0.0)) / scale + misfit_pt
            at = fig.to_page(bx + (bw - 1) / 2, by + (bh - 1) / 2, scale)  # box centre (a triangle's centroid sits low)
            pts.append(point(cal, at[1], u, at))

        # mean line (~72 px wide, black) and upper error-bar cap (~35 px wide, black)
        lines = dark | (colour_mask(img, COLOURS[g], 60) if g in COLOURS else dark)
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
    return {"groups": out}
