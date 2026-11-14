"""Supplementary Fig. 7a: FITC-dextran (3 kDa) concentration at 5 min, 1, 24, 48 and 72 hr (raster).

Bars are mean ± s.d. with n=3 markers per time point (circles, squares at 1 hr, triangles at 24 hr).
The figure is one embedded image (~121 dpi). At 300 dpi, dots are found by a disc opening of the
dark mask (as in _util). A marker stands alone when its connected component of the unopened dark
mask holds no other marker and is not the axes-and-bars component (the largest one). At this
resolution the markers sit on the bar tops and touch each other: in every time point at least one
marker is joined to the bar outline or to another marker, so no time point is countable and none
returns points. The bar tops (means) and caps are covered by the same markers, so no bar is returned.
The test is rerun at every audit; a time point whose markers all stood alone would return points.
y axis 0-12 µM, ticks every 2.
"""
import cv2
import numpy as np

from _util import DPI, NATIVE_PX, _runs
from livinglit.figures.source import blobs, calibrate, dark_mask

CATEGORIES = ["m5", "h1", "h24", "h48", "h72"]
TICK_VALUES = [0, 2, 4, 6, 8, 10, 12]
KERNEL = 13


def read(fig):
    img, scale = fig.render(DPI)
    m = dark_mask(img, 128)
    h, w = m.shape
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    axes = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))

    col = m.sum(0)
    x_axis0, x_axis1 = max(_runs([i for i in range(w) if col[i] > 0.6 * h]), key=lambda r: col[r[0]])
    row = m[:, x_axis1 + 1:].sum(1)
    y_axis0, y_axis1 = _runs([i for i in range(h) if row[i] > 0.6 * row.max()])[-1]

    left = m[:, x_axis0 - 14:x_axis0 - 2].sum(1)
    ticks = [(a + b) / 2 for a, b in _runs([i for i in range(h) if left[i] >= 8])]
    if len(ticks) != len(TICK_VALUES):
        raise ValueError(f"found {len(ticks)} y ticks, expected {len(TICK_VALUES)}")
    cal = calibrate([(fig.to_page(0, t, scale)[1], v) for t, v in zip(sorted(ticks, reverse=True), TICK_VALUES)])
    cal_px = cal.residual / abs(cal.slope) * scale

    below = m[y_axis1 + 3:y_axis1 + 14, :].sum(0)
    cats = [(a + b) / 2 for a, b in _runs([i for i in range(x_axis1 + 6, w) if below[i] >= 5])]
    if len(cats) != len(CATEGORIES):
        raise ValueError(f"found {len(cats)} x ticks, expected {len(CATEGORIES)}")
    half = min(np.diff(cats)) / 2

    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (KERNEL, KERNEL))
    op = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, k).astype(bool)
    dots = [b for b in blobs(op, min_area=KERNEL * KERNEL // 2)
            if b["x"] > x_axis1 + 6 and min(ticks) - 30 < b["y"] < y_axis0]
    diam = float(np.median([min(b["box"][2], b["box"][3]) for b in dots]))
    h_min = min(b["box"][3] for b in dots)
    comp_of = [int(lab[int(round(b["y"])), int(round(b["x"]))]) for b in dots]

    def alone(i):
        c, b = comp_of[i], dots[i]
        return (c not in (0, axes) and comp_of.count(c) == 1
                and b["box"][2] <= 1.3 * diam and b["box"][3] <= 1.3 * diam)

    out = {}
    for cx, label in zip(cats, CATEGORIES):
        mine = [i for i, b in enumerate(dots) if abs(b["x"] - cx) < half]
        g = {"points": [], "countable": bool(mine) and all(alone(i) for i in mine)}
        if g["countable"]:
            for i in sorted(mine, key=lambda i: dots[i]["y"]):
                b = dots[i]
                unc = NATIVE_PX + (b["box"][3] - h_min) / 2 + cal_px
                v = cal.value(fig.to_page(0, b["y"], scale)[1])
                a, c = (cal.value(fig.to_page(0, b["y"] + s * unc, scale)[1]) for s in (1, -1))
                g["points"].append({"value": v, "lo": min(a, c, v), "hi": max(a, c, v),
                                    "at": list(fig.to_page(b["x"], b["y"], scale))})
        out[label] = g
    return {"groups": out}
