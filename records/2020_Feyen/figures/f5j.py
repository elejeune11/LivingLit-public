"""Fig. 5J (journal_version.pdf p. 8): maximum APD75 shortening by mexiletine, change from untreated wells (ms).

Raster image (embedded at ~300 dpi). Five bars (mean +/- SEM) from the zero line: HD1, HD2, HD3 (MM),
F1473C RPMI/B27, F1473C MM, one marker per well (circles and triangles = 2 batches). Only F1473C MM is
read: its markers stand alone (3 black triangles on the dark grey bar fill, 6 black circles below the
bar, apart from each other and from every line). The HD and RPMI/B27 markers sit on the dotted zero
line, the mean lines and the caps and touch each other, so they are not read (see figures.yaml).

Markers are connected components of pixels darker than BLACK (well below the bar fill, ~100-127).
Triangles are searched inside the bar between the zero line and the upper SEM cap, circles below the
lower cap. Each blob must be one marker (box at most 8 x 8 px). A circle's position is its
darkness-weighted centroid. For a triangle it is the middle of its box; the triangle's own centroid
lies about a sixth of its height lower, so the interval covers both, plus 0.6 px.

The bar is drawn from 0 down to the mean: the mean is the bar's bottom edge, where the column
darkness falls to half the fill's, averaged over columns clear of the error line; its interval adds
1 px for the bar's 1 px border. The upper SEM end (the higher value, inside the bar) is the
darkness-weighted centre, above the fill, of the cap rows at columns clear of the vertical line.

The y axis is calibrated from its six tick marks (200 to -800), left of the axis line.
"""
import numpy as np

from livinglit.figures.source import blobs, calibrate, point

DPI = 300
UNC_PX = 0.6
BORDER_PX = 1.0
BLACK = 60
TICK_COLS = (76, 81)
TICK_VALUES = [200, 0, -200, -400, -600, -800]  # top to bottom
BAR_COLS = (334, 368)  # inside the F1473C MM bar outline
ERR_COLS = (346, 352)  # vertical error line and its surroundings
CAP_COLS = (341, 345)  # upper cap, left of the vertical line
ZERO_CLEAR = 50  # first row below the dotted zero line
CIRCLE_ROWS = (117, 130)
CIRCLE_COLS = (330, 375)
MAX_BOX = 8
N_TRIANGLES, N_CIRCLES = 3, 6


def _runs(flags):
    out, start = [], None
    for i, f in enumerate(flags):
        if f and start is None:
            start = i
        if not f and start is not None:
            out.append((start, i - 1))
            start = None
    if start is not None:
        out.append((start, len(flags) - 1))
    return out


def _ticks(g):
    dark = 255 - g[:, TICK_COLS[0]:TICK_COLS[1] + 1].mean(axis=1)
    rows = []
    for a, b in _runs(list(dark > 128)):
        r = np.arange(a - 1, b + 2)
        rows.append(float((r * dark[r]).sum() / dark[r].sum()))
    return rows


def _bar_bottom(g):
    cols = [c for c in range(BAR_COLS[0] + 2, BAR_COLS[1] - 1) if not ERR_COLS[0] <= c <= ERR_COLS[1]]
    edges = []
    for c in cols:
        col = 255 - g[:, c]
        fill = float(np.median(col[ZERO_CLEAR + 5:ZERO_CLEAR + 20]))
        r = ZERO_CLEAR + 20
        while col[r + 1] > fill / 2:
            r += 1
        # sub-pixel: the half-fill crossing between row r and r + 1
        edges.append(r + (col[r] - fill / 2) / (col[r] - col[r + 1]))
    if max(edges) - min(edges) > 1.5:
        raise ValueError(f"bar bottom uneven: {edges}")
    return float(np.mean(edges))


def _cap(g, bottom):
    dark = 255 - g[:, CAP_COLS[0]:CAP_COLS[1] + 1].mean(axis=1)
    fill = float(np.median(dark[ZERO_CLEAR + 5:ZERO_CLEAR + 20]))
    runs = [(a, b) for a, b in _runs(list(dark > fill + 15)) if ZERO_CLEAR < a and b < bottom - 1]
    if len(runs) != 1:
        raise ValueError(f"expected one upper cap inside the bar, found {runs}")
    a, b = runs[0]
    r = np.arange(a - 1, b + 2)
    w = np.clip(dark[r] - fill, 0, None)
    return float((r * w).sum() / w.sum())


def _markers(g, r0, r1, c0, c1):
    sub = g[r0:r1 + 1, c0:c1 + 1]
    out = []
    for b in blobs(sub < BLACK, min_area=4):
        x, y, w, h = b["box"]
        if w > MAX_BOX or h > MAX_BOX:
            raise ValueError(f"blob {b} is larger than one marker: markers touch")
        win = sub[max(0, y - 1):y + h + 1, max(0, x - 1):x + w + 1]
        wt = np.clip(255 - win, 0, None)
        rr = np.arange(max(0, y - 1), max(0, y - 1) + win.shape[0])
        cc = np.arange(max(0, x - 1), max(0, x - 1) + win.shape[1])
        cy = float((wt.sum(axis=1) * rr).sum() / wt.sum())
        cx = float((wt.sum(axis=0) * cc).sum() / wt.sum())
        out.append({"cx": c0 + cx, "cy": r0 + cy, "mid": r0 + y + (h - 1) / 2})
    return sorted(out, key=lambda m: (m["cx"], m["cy"]))


def read(fig):
    img, scale = fig.render(DPI)
    g = img.astype(float).mean(axis=2)
    rows = _ticks(g)
    if len(rows) != len(TICK_VALUES):
        raise ValueError(f"expected {len(TICK_VALUES)} y ticks, found {rows}")
    cal = calibrate(list(zip(rows, TICK_VALUES)))
    res = cal.residual

    bottom = _bar_bottom(g)
    cap = _cap(g, bottom)
    cx = (BAR_COLS[0] + BAR_COLS[1]) / 2
    pm = point(cal, bottom, UNC_PX + BORDER_PX, fig.to_page(cx, bottom, scale))
    pu = point(cal, cap, UNC_PX, fig.to_page(cx, cap, scale))
    bar = {"mean": [pm["value"], pm["lo"] - res, pm["hi"] + res],
           "error": [pu["value"], pu["lo"] - res, pu["hi"] + res]}

    tris = _markers(g, ZERO_CLEAR, int(cap) - 3, BAR_COLS[0], BAR_COLS[1])
    circles = _markers(g, *CIRCLE_ROWS, *CIRCLE_COLS)
    if len(tris) != N_TRIANGLES or len(circles) != N_CIRCLES:
        raise ValueError(f"expected {N_TRIANGLES} triangles and {N_CIRCLES} circles, found {tris} and {circles}")
    pts = []
    for m in tris:
        p = point(cal, m["mid"], UNC_PX, fig.to_page(m["cx"], m["mid"], scale))
        a, b = cal.value(m["cy"] + UNC_PX), cal.value(m["cy"] - UNC_PX)
        p["lo"], p["hi"] = min(p["lo"], a, b) - res, max(p["hi"], a, b) + res
        pts.append(p)
    for m in circles:
        p = point(cal, m["cy"], UNC_PX, fig.to_page(m["cx"], m["cy"], scale))
        p["lo"], p["hi"] = p["lo"] - res, p["hi"] + res
        pts.append(p)
    grp = {"points": pts, "countable": True, "bar": bar}
    return {"groups": {"lqt_mm": grp, "lqt_mm_media": dict(grp)}}
