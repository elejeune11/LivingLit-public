"""Supplementary Fig. 7b: FITC-dextran (3 kDa) at the top and bottom of the transwell, 5 min to 72 hr (raster).

Bars are mean ± s.d. (black: top, grey: bottom) with n=3 hollow markers per time point (open circles
on the black bars, open squares on the grey bars). The figure is one embedded image (~121 dpi).
At 300 dpi a marker is found by its white interior: an enclosed light component of the dark mask,
right of the y axis and above the x axis, no larger than a marker (the grey bar fills are light
too but far larger). Where markers overlap, one marker's outline splits another's interior into
pieces; each piece is kept, and the pieces then share an outline component.
A marker stands alone when the dark component of its outline (the dark pixels within RING px of
its interior) holds no other marker's interior and is not the axes-and-bars component (the
largest one). Markers sit on the bar tops and on each other, so a time point returns points only
if every one of its markers stands alone; otherwise it is not countable and returns nothing. The
bar tops (means) and caps are covered by the same markers, so no bar is returned.
The test is rerun at every audit.
y axis 0-20 µM, ticks every 5.
"""
import cv2
import numpy as np

from _util import DPI, NATIVE_PX, _runs
from livinglit.figures.source import calibrate, dark_mask

CATEGORIES = ["top_m5", "top_h1", "top_h24", "top_h48", "top_h72",
              "bottom_m5", "bottom_h1", "bottom_h24", "bottom_h48", "bottom_h72"]
TICK_VALUES = [0, 5, 10, 15, 20]
MAX_HOLE = 400  # px at 300 dpi; a marker interior is ~13-15 px across
RING = 4


def read(fig):
    img, scale = fig.render(DPI)
    m = dark_mask(img, 128)
    h, w = m.shape

    col = m.sum(0)
    x_axis0, x_axis1 = _runs([i for i in range(w) if col[i] > 0.8 * h])[0]  # leftmost full-height line
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

    n_d, dark_lab, dark_st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    axes = 1 + int(np.argmax(dark_st[1:, cv2.CC_STAT_AREA]))
    n_l, light_lab, light_st, light_c = cv2.connectedComponentsWithStats((~m).astype(np.uint8), 4)
    holes = []
    for i in range(1, n_l):
        x, y, bw, bh, a = light_st[i]
        cx, cy = light_c[i]
        if (a >= 4 and a <= MAX_HOLE and x > 0 and y > 0 and x + bw < w and y + bh < h
                and cx > x_axis1 + 6 and cy < y_axis0):
            ring = cv2.dilate((light_lab == i).astype(np.uint8), np.ones((2 * RING + 1,) * 2, np.uint8)).astype(bool)
            outline = set(np.unique(dark_lab[ring & m]).tolist()) - {0}
            holes.append({"x": float(cx), "y": float(cy), "box": (x, y, bw, bh), "outline": outline})

    def alone(i):
        o = holes[i]["outline"]
        return (bool(o) and axes not in o
                and not any(o & holes[j]["outline"] for j in range(len(holes)) if j != i))

    out = {}
    for cx, label in zip(cats, CATEGORIES):
        mine = [i for i, b in enumerate(holes) if abs(b["x"] - cx) < half]
        g = {"points": [], "countable": bool(mine) and all(alone(i) for i in mine)}
        if g["countable"]:
            for i in sorted(mine, key=lambda i: holes[i]["y"]):
                b = holes[i]
                unc = NATIVE_PX + cal_px
                v = cal.value(fig.to_page(0, b["y"], scale)[1])
                a, c = (cal.value(fig.to_page(0, b["y"] + s * unc, scale)[1]) for s in (1, -1))
                g["points"].append({"value": v, "lo": min(a, c, v), "hi": max(a, c, v),
                                    "at": list(fig.to_page(b["x"], b["y"], scale))})
        out[label] = g
    return {"groups": out}
