"""Fig. 6A, twitch force amplitude normalised to 2 Hz, NS / SS / SE at 2, 2.5 and 3 Hz: raster Excel chart.

The y axis has two labelled ticks (1 and 0.5); they calibrate y (no misfit can be measured).
Series are told apart by grey level (legend): NS dark diamonds, SS mid-grey triangles, SE light
squares. Each marker is a group mean with a black SEM bar: mean at the marker centre (box centre
for triangles, the interval covering the centroid), upper end at the cap centre. At 2 Hz the three
markers overlap at 1 (the normalising value) and only the SE square, drawn on top, is read. At
2.5 Hz the SS triangle is partly hidden under the SE square, with its upper bar: not read.
The bar of the SE square at 2 Hz and the NS diamond at 3 Hz cross the marker; the black bar
pixels inside a marker are bridged before markers are found.
"""
import numpy as np
import cv2
import _util as U
from livinglit.figures.source import blobs

ITEMS = {"F6A_curve": ["NS_25", "NS_3", "SS_3", "SE_2", "SE_25", "SE_3"],
         "F6A_NS": ["NS_3"], "F6A_SS": ["SS_3"], "F6A_SE": ["SE_3", "SE_2"]}
GREY = {"NS": (80, 106), "SS": (112, 142), "SE": (158, 190)}  # mean grey level of each series (legend)
LEGEND_BOTTOM = 120
X_TICKS_HZ = {2: "2", 2.5: "25", 3: "3"}


def upper_cap(black, cx, top_limit):
    """Centre row of the cap at the top of the black bar through column cx (searching above top_limit)."""
    col = black[:top_limit, int(cx) - 1:int(cx) + 2].any(1)
    rows = np.nonzero(col)[0]
    if len(rows) == 0:
        return None
    run = U.runs(list(rows))[-1]  # the bar segment that reaches down towards the marker
    if top_limit - 1 - run[1] > 6:
        return None
    y = run[0]
    cap = [r for r in range(y, y + 8) if black[r, int(cx) - 10:int(cx) + 11].sum() >= 10]
    if not cap:
        return None
    c = U.runs(cap)[0]
    return (c[0] + c[1]) / 2


def read(fig):
    img, scale = fig.render(U.DPI)
    g = img.astype(int).mean(2)
    axis = U.y_axis(g < 200, 100, 160)
    cal = U.fit(U.y_ticks(g < 200, axis[0], reach=(3, 9), y_lo=LEGEND_BOTTOM), [1, 0.5])
    black = g < 50
    # x: the marker columns at 2, 2.5 and 3 Hz are the x tick marks below the axis
    xaxis = [y for y in range(g.shape[0]) if (g[y, axis[1]:] < 200).sum() > 700]
    xt = U.x_ticks(g < 200, max(xaxis), reach=(2, 7), x_lo=axis[1] + 5)
    # the two ticks sit between the three categories (Excel): centres lie half a spacing either side
    sp = xt[1] - xt[0]
    centres = [xt[0] - sp / 2, xt[0] + sp / 2, xt[1] + sp / 2]
    out = {}
    for grp, (lo, hi) in GREY.items():
        m = ((g >= lo) & (g < hi)).astype(np.uint8)
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((1, 7), np.uint8))  # bridge a bar crossing a marker
        k = 11 if grp == "SS" else 15  # a triangle's inscribed circle is small; series lines are ~9 px
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
        for b in blobs(m.astype(bool), min_area=150):
            if b["y"] < LEGEND_BOTTOM:
                continue
            k = int(np.argmin([abs(b["x"] - c) for c in centres]))
            if abs(b["x"] - centres[k]) > 15:
                continue
            hz = [2, 2.5, 3][k]
            x, y, w, h = b["box"]
            if grp == "SS":
                cy, extra = (b["y"] + y + (h - 1) / 2) / 2, abs(b["y"] - (y + (h - 1) / 2)) / 2
            else:
                cy, extra = b["y"], 0.0
            label = f"{grp}_{X_TICKS_HZ[hz]}"
            if (hz == 2 and grp != "SE") or (hz == 2.5 and grp == "SS"):
                continue  # hidden under the SE square
            bar = {"mean": U.bar(cal, cy, extra)}
            cap = upper_cap(black, b["x"], y + 2)
            if cap is not None:
                bar["error"] = U.bar(cal, cap)
            out[label] = {"points": [], "countable": False, "bar": bar}
    return U.per_item(out, ITEMS)
