"""Fig. 1c (author manuscript, p. 18): actinin+ cells (%) before and after metabolic selection, n=8 pairs.

The panel is a raster image. Markers of a column overlap (before: two markers near 60 % lie almost on top of
each other; after: six of eight markers merge into one blob), so markers are not counted from blobs. Each pair
is joined by a straight line drawn centre to centre, and the eight lines stand apart between the columns.
Each line is found by a constrained Hough search: from each before-marker blob, every end height in the after
column is scored by the mean darkness along the segment (marker disks excluded); peaks above SCORE are lines.
A pair's before value is its line's start blob centre; its after value is the line's end. The isolated after
marker (lowest) checks that line ends land on marker centres.
"""
import cv2
import numpy as np

from livinglit.figures.source import blobs, calibrate, dark_mask, point

DPI = 600
UNC_PX = 0.6 * DPI / 300          # 0.6 px at 300 dpi, in px at DPI
SCORE = 0.85                      # mean darkness along a segment counted as a drawn line
TICKS = [50, 60, 70, 80, 90, 100]  # printed y tick labels, bottom to top


def _axis_and_ticks(m):
    col = m.sum(0)
    ax = int(np.argmax(col))                       # y axis: the longest dark column
    while ax > 0 and col[ax - 1] > 0.8 * col[ax]:  # its left edge
        ax -= 1
    stub = m[:, ax - 8:ax - 2].all(axis=1)         # tick stubs to the left of the axis
    rows = np.flatnonzero(stub)
    groups = np.split(rows, np.flatnonzero(np.diff(rows) > 1) + 1)
    return ax, [float(g.mean()) for g in groups if len(g)]


def _segment_score(dark, x0, y0, x1, y1, skip):
    n = int(abs(x1 - x0))
    t = np.linspace(0, 1, n)
    xs, ys = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
    keep = (xs > x0 + skip) & (xs < x1 - skip)
    xs, ys = xs[keep], ys[keep]
    v = cv2.remap(dark, xs.astype(np.float32)[None, :], ys.astype(np.float32)[None, :], cv2.INTER_LINEAR)
    return float(v.mean())


def read(fig):
    img, s = fig.render(DPI)
    m = dark_mask(img, 110)
    ax, ticks = _axis_and_ticks(m.astype(np.uint8))
    if len(ticks) != len(TICKS):
        raise ValueError(f"found {len(ticks)} y ticks, expected {len(TICKS)}")
    marks = list(zip(sorted(ticks, reverse=True), TICKS))  # lowest tick (largest row) is 50
    cal_px = calibrate(marks)

    # markers: opening with a disk wider than a line, narrower than a marker
    op = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17)))
    bl = [b for b in blobs(op, 100) if b["x"] > ax + 20]
    xs = sorted(b["x"] for b in bl)
    split = (xs[0] + xs[-1]) / 2
    before = sorted([b for b in bl if b["x"] < split], key=lambda b: b["y"])
    after = sorted([b for b in bl if b["x"] >= split], key=lambda b: b["y"])
    r = min(b["box"][2] for b in bl) / 2            # marker radius (px)
    xb = float(np.mean([b["x"] for b in before]))
    xa = float(np.mean([b["x"] for b in after]))
    ytop = min(b["box"][1] for b in after) + r
    ybot = max(b["box"][1] + b["box"][3] for b in after) - r
    dark = m.astype(np.float32)

    pairs = []
    for b in before:
        top, bot = b["box"][1] + r, b["box"][1] + b["box"][3] - r   # where this blob's marker centres can be
        yb = b["y"]
        cand = np.arange(ytop - 2, ybot + 2, 0.25)
        sc = np.array([_segment_score(dark, xb, yb, xa, ya, 1.6 * r) for ya in cand])
        on = sc >= SCORE
        runs = np.split(np.flatnonzero(on), np.flatnonzero(np.diff(np.flatnonzero(on)) > 1) + 1)
        for run in runs:
            if not len(run):
                continue
            ya = float(cand[run][np.argmax(sc[run])])
            half = (cand[run][-1] - cand[run][0]) / 2
            pairs.append({"yb": yb, "yb_lo": top, "yb_hi": bot, "ya": ya, "ya_half": half})

    pairs.sort(key=lambda p: (p["yb"], p["ya"]))
    misfit_px = cal_px.residual / abs(cal_px.slope)
    out_b, out_a = [], []
    for p in pairs:
        vb = cal_px.value(p["yb"])
        lo_b, hi_b = sorted([cal_px.value(p["yb_hi"] + UNC_PX + misfit_px), cal_px.value(p["yb_lo"] - UNC_PX - misfit_px)])
        out_b.append({"value": vb, "lo": min(lo_b, vb), "hi": max(hi_b, vb),
                      "at": list(fig.to_page(xb, p["yb"], s))})
        ua = p["ya_half"] + UNC_PX + misfit_px
        out_a.append(point(cal_px, p["ya"], ua, fig.to_page(xa, p["ya"], s)))
    return {"groups": {"before": {"points": out_b, "countable": True},
                       "after": {"points": out_a, "countable": True}}}
