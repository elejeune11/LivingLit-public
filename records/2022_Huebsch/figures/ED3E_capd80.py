"""Extended Data Fig. 3e (journal_version.pdf p. 22): cAPD80 (msec) of SCVI273 MPS, MM vs SM.
Raster. Each group is an outlined bar (its top edge is the mean) with a mean + SD error bar. MM's red squares each
stand alone and are read as points; SM's blue circles touch in four clusters, so only SM's mean and SD are read.
Markers cover the middle of the bar tops and caps, so strokes are found from the ink left visible: the bar top is
the stroke whose ink (black or marker) spans the bar from side to side; the upper end of the SD bar is the topmost
stroke above it with ink on both sides of the centre line (significance brackets end at a centre line)."""
import numpy as np

import _util as u
from livinglit.figures.source import point

LABELS = [600, 400, 200, 0]  # y tick labels, top to bottom
SINGLE = {"red": (300, 345), "blue": (230, 270)}  # area (px at 300 dpi) of one square / one circle marker


def sides(img, near, row):
    """Outer columns of the bar box's two vertical sides, from a row low in the bar where no marker lies."""
    bk = u.black(img)[row]
    left = [c for c in range(near - 60, near) if bk[c]]
    right = [c for c in range(near + 1, near + 60) if bk[c]]
    return min(left), max(right)


def strokes(img, x0, x1, col, bottom, min_width=8):
    """Horizontal black strokes between the bar's sides (sides and centre line left out), top to bottom:
    (row, black width, ink spans the bar, ink on both sides of the centre line)."""
    bk = u.black(img)
    ink = bk | u.coloured(img, "red") | u.coloured(img, "blue")
    c = int(round(col))
    lo, hi = x0 + 8, x1 - 8  # inside the side lines (about 6 px wide)
    feats, cur = [], []
    for r in range(bottom):
        win = bk[r, lo:hi + 1].copy()
        win[c - 3 - lo:c + 4 - lo] = False
        w = int(win.sum())
        if w >= min_width:
            span = bool(ink[r, lo:hi + 1].all())
            both = bool(ink[r, c - 10:c - 4].any() and ink[r, c + 5:c + 11].any())
            cur.append((r, w, span, both))
        elif cur:
            feats.append(cur)
            cur = []
    if cur:
        feats.append(cur)
    return [(float(np.mean([f[0] for f in g])), max(f[1] for f in g), any(f[2] for f in g), any(f[3] for f in g))
            for g in feats]


def read_group(fig, img, scale, cal, unc, near, x_axis, colour):
    col = u.centre_column(img, near, bottom=x_axis - 5)
    x0, x1 = sides(img, near, x_axis - 30)
    fs = strokes(img, x0, x1, col, x_axis - 5)
    top = [f for f in fs if f[2]][0]
    cap = [f for f in fs if f[0] < top[0] and f[3] and not f[2]][0]
    m = point(cal, top[0], unc, fig.to_page(col, top[0], scale))
    e = point(cal, cap[0], unc, fig.to_page(col, cap[0], scale))
    g = {"points": [], "countable": False,
         "bar": {"mean": [m["value"], m["lo"], m["hi"]], "error": [e["value"], e["lo"], e["hi"]]}}
    bs, alone = u.markers(img, colour, x0, x1, SINGLE[colour])
    if alone:
        g["countable"] = True
        g["points"] = [point(cal, b["y"], unc, fig.to_page(b["x"], b["y"], scale)) for b in bs]
    return g


def read(fig):
    img, scale = fig.render(u.DPI)
    cal, unc, ax = u.axis(img, LABELS)
    x_axis = int(round(-cal.intercept / cal.slope))  # render row of the value 0 (the x axis line)
    return {"groups": {
        "MM": read_group(fig, img, scale, cal, unc, 228, x_axis, "red"),
        "SM": read_group(fig, img, scale, cal, unc, 344, x_axis, "blue"),
    }}
