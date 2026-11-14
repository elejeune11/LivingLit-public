"""Fig. 4C, isometric twitch amplitude (mN/mm2) against strain (%), NS / SS / SE: raster Excel chart.

Grey gridlines at 0.1-0.4 and the x axis (0) calibrate y; x tick marks at 105-130 % calibrate
strain (the 100 % tick is hidden by a marker). Each marker is a group mean with a black SEM bar:
one label per marker, '<group> #<i>' from left to right (105 % onwards), with the mean (marker centre), the
upper bar end, and its strain as x (read, rounded to 0.1 %). Diamonds = SE, squares = SS,
triangles = NS (legend). NS triangles lie on the x axis; their bars are not readable. At
100 % strain the three groups' markers overlap at the origin in one blob: not readable.
"""
import numpy as np
import cv2
import _util as U
from livinglit.figures.source import blobs

ITEM = "F4C_curve"
LEGEND_BOTTOM = 50  # legend markers sit above this row (px)


def classify(b):
    """Squares fill their box; a triangle's centroid sits below its box centre; diamonds are symmetric."""
    x, y, w, h = b["box"]
    if b["area"] / float(w * h) > 0.85:
        return "SS"
    return "NS" if (b["y"] - (y + (h - 1) / 2)) / h > 0.04 else "SE"


def upper_cap(black, cx, top):
    """Topmost row of the black bar rising from a marker's top edge, and the cap's centre row."""
    col = black[:top + 4, int(cx) - 2:int(cx) + 3].any(1)
    starts = [r for r in range(top - 2, top + 4) if col[r]]
    if not starts:
        return None
    y = starts[-1]
    while y > 0 and col[y - 1]:
        y -= 1
    if top - y < 4:
        return None
    rows = [r for r in range(y, y + 12) if black[r, int(cx) - 12:int(cx) + 13].sum() >= 10]
    if not rows:
        return None
    rows = U.runs(rows)[0]
    return (rows[0] + rows[1]) / 2


def read(fig):
    img, scale = fig.render(U.DPI)
    g = img.astype(int).mean(2)
    grey = (g >= 90) & (g < 200)
    black = g < 70
    # y: gridlines (rows with long grey runs) and the x axis
    lines = [y for y in range(grey.shape[0]) if grey[y, 140:].sum() > 700]
    centres = [(s + e) / 2 for s, e in U.runs(lines)]
    cal = U.fit(centres, [0.4, 0.3, 0.2, 0.1, 0.0])
    axis_bottom = int(U.runs(lines)[-1][1])
    xt = U.x_ticks(grey, axis_bottom, reach=(2, 6), x_lo=200)
    calx = U.fit(xt, [105, 110, 115, 120, 125, 130])
    k = 11
    opened = cv2.morphologyEx(grey.astype(np.uint8), cv2.MORPH_OPEN,
                              cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))).astype(bool)
    origin = xt[0] - (xt[1] - xt[0])  # px of the 100 % tick (hidden under markers)
    marks = [b for b in blobs(opened, min_area=200) if b["y"] > LEGEND_BOTTOM]
    # the three groups' markers overlap at the origin (100 %, 0) in one blob: not readable
    marks = [b for b in marks if abs(b["x"] - origin) > 0.5 * (xt[1] - xt[0])]
    found = {"NS": [], "SS": [], "SE": []}
    for b in marks:
        found[classify(b)].append(b)
    out = {}
    for grp, bs in found.items():
        for i, b in enumerate(sorted(bs, key=lambda q: q["x"])):
            x, y, w, h = b["box"]
            if grp == "NS":  # triangle: centroid and box centre differ; the interval covers both
                cy, extra = (b["y"] + y + (h - 1) / 2) / 2, abs(b["y"] - (y + (h - 1) / 2)) / 2
            else:
                cy, extra = b["y"], 0.0
            strain = round(calx.value(b["x"]), 1)
            bar = {"mean": U.bar(cal, cy, extra), "x": strain}
            if grp != "NS":
                cap = upper_cap(black, b["x"], y)
                if cap is not None:
                    bar["error"] = U.bar(cal, cap)
            out[f"{grp} #{i + 1}"] = {"points": [], "countable": False, "bar": bar}
    return {"groups": out}
