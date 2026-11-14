"""Fig. S7I: % SMA positive cells in CTRL-CFs and ACM-CFs (mmc1.pdf p. 10), one embedded image (~300 dpi).

Tick labels are part of the image, so tick marks are found in the raster (left of the y axis) and given
their printed values 15, 10, 5, 0 top to bottom. Dots are small black discs (~25 px); the horizontal line
beside each group is read as the mean (the legend does not say mean or median).

Both groups: two dots stand clear of the group line (legend N=2), read as points; the line is read as well.
"""
import numpy as np

from livinglit.figures.source import RASTER_UNCERTAINTY_PX_300DPI, blobs, calibrate, dark_mask

TICK_X = (90, 95)            # px columns of the tick marks, left of the y axis (axis at cols 96-97)
TICKS = [15, 10, 5, 0]       # printed tick labels, top to bottom
PLOT_X = (99, 300)           # px columns right of the y axis
PLOT_Y = (60, 307)           # px rows below the panel title and above the x axis (x axis at rows 309-311)
DOT_AREA = (15, 45)          # px area of one standalone dot


def _runs(flags):
    out, start = [], None
    for i, f in enumerate(list(flags) + [False]):
        if f and start is None:
            start = i
        elif not f and start is not None:
            out.append((start, i - 1))
            start = None
    return out


def _ticks(gray):
    dark = 255.0 - gray[:, TICK_X[0]:TICK_X[1] + 1]
    rows = dark.mean(axis=1)
    ys = []
    for a, b in _runs(rows > 100):
        if not PLOT_Y[0] <= a <= PLOT_Y[1] + 6:
            continue
        w = rows[a - 1:b + 2]
        ys.append(float(np.sum(np.arange(a - 1, b + 2) * w) / np.sum(w)))
    return ys


def _line_y(gray, box):
    x0, y0, w, h = box
    sub = 255.0 - gray[y0 - 1:y0 + h + 1, x0:x0 + w]
    wt = np.where(sub > 30, sub, 0).sum(axis=1)
    return float(np.sum(np.arange(y0 - 1, y0 + h + 1) * wt) / np.sum(wt))


def _interval(cal, pos, unc):
    v = cal.value(pos)
    lo, hi = cal.interval(pos, unc)
    return [v, min(lo, v) - cal.residual, max(hi, v) + cal.residual]


def read(fig):
    img, scale = fig.render(300)
    gray = img.astype(float).mean(axis=2)
    unc = RASTER_UNCERTAINTY_PX_300DPI

    ticks = _ticks(gray)
    if len(ticks) != len(TICKS):
        raise ValueError(f"tick marks found: {ticks}")
    cal = calibrate(list(zip(ticks, TICKS)))

    mask = dark_mask(img, 100)
    inside = [b for b in blobs(mask, 4) if PLOT_X[0] <= b["box"][0] and b["box"][0] + b["box"][2] - 1 <= PLOT_X[1]
              and PLOT_Y[0] <= b["box"][1] and b["box"][1] + b["box"][3] - 1 <= PLOT_Y[1]]
    lines = sorted([b for b in inside if b["box"][2] > 20 and b["box"][3] <= 4], key=lambda b: b["x"])
    dots = [b for b in inside if DOT_AREA[0] <= b["area"] <= DOT_AREA[1] and b["box"][2] <= 7 and b["box"][3] <= 9]
    if len(lines) != 2:
        raise ValueError(f"expected two group lines, found {lines}")

    groups = {}
    for label, ln in zip(("CTRL", "ACM"), lines):
        x0, _, w, _ = ln["box"]
        own = sorted([d for d in dots if x0 <= d["x"] <= x0 + w - 1], key=lambda d: d["y"])
        pts = []
        for d in own:
            v, lo, hi = _interval(cal, d["y"], unc)
            pts.append({"value": v, "lo": lo, "hi": hi, "at": list(fig.to_page(d["x"], d["y"], scale))})
        groups[label] = {"points": pts, "countable": True, "bar": {"mean": _interval(cal, _line_y(gray, ln["box"]), unc)}}
    return {"groups": groups}
