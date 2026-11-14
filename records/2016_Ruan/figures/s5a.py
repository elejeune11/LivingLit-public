"""Supplement Fig. 5A, twitch amplitude (mN/mm2) against bath calcium (uM): raster Excel chart, one construct.

Tick marks calibrate both axes (y 0-0.1, x 0-3000 uM). Each black diamond is a mean with an
error bar (the legend names neither the spread nor the number of twitches): one label per
diamond, '#<i>' from low to high calcium, with the mean (diamond centre), the upper bar end
and the calcium as x (read, rounded to 10 uM). The two diamonds near 0 uM overlap in one blob
and are not read.
"""
import numpy as np
import cv2
import _util as U
from livinglit.figures.source import blobs

ITEM, GROUP = "S5A_calcium", "construct"


def upper_cap(black, cx, top):
    col = black[:top + 4, int(cx) - 2:int(cx) + 3].any(1)
    starts = [r for r in range(top - 3, top + 4) if col[r]]
    if not starts:
        return None
    y = starts[-1]
    while y > 0 and col[y - 1]:
        y -= 1
    if top - y < 4:
        return None
    cap = [r for r in range(y, y + 8) if black[r, int(cx) - 10:int(cx) + 11].sum() >= 10]
    if not cap:
        return None
    c = U.runs(cap)[0]
    return (c[0] + c[1]) / 2


def read(fig):
    img, scale = fig.render(U.DPI)
    g = img.astype(int).mean(2)
    axes = g < 215
    left, right = U.y_axis(axes, 150, 200)
    cal = U.fit(U.y_ticks(axes, left, reach=(3, 9), max_rows=5), [0.1, 0.08, 0.06, 0.04, 0.02, 0])
    xaxis = [y for y in range(g.shape[0]) if axes[y, right:].sum() > 700]
    bottom = max(xaxis)
    xt = U.x_ticks(axes, bottom, reach=(3, 12), x_lo=left - 2)
    calx = U.fit(xt, [0, 1000, 2000, 3000])
    black = g < 60
    opened = cv2.morphologyEx(black.astype(np.uint8), cv2.MORPH_OPEN,
                              cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))).astype(bool)
    bl = [b for b in blobs(opened, min_area=150) if b["y"] < bottom and b["x"] > right]
    single = float(np.median([b["area"] for b in bl]))
    bl = [b for b in bl if b["area"] <= 1.4 * single]  # overlapping diamonds near 0 uM are one blob
    out = {}
    for i, b in enumerate(sorted(bl, key=lambda q: q["x"])):
        bar = {"mean": U.bar(cal, b["y"]), "x": round(calx.value(b["x"]), -1)}
        cap = upper_cap(black, b["x"], b["box"][1])
        if cap is not None:
            bar["error"] = U.bar(cal, cap)
        out[f"#{i + 1}"] = {"points": [], "countable": False, "bar": bar}
    return {"groups": out}
