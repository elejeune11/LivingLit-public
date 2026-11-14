"""Fig. 7D lower panel: PKP2 protein expression (norm. GAPDH), western blot densitometry.

The whole of Fig. 7 is one embedded image (~300 dpi), so tick labels are not text: tick marks are
found in the raster and given their printed values in order. The y axis is broken: an upper segment
1-5 (EPI groups) and a lower segment 0.00-0.15 (CF groups), each calibrated on its own ticks.

CF squares (black CTRL-CFs, red ACM-CFs) each stand alone (one 13x13 px blob apiece) and are read as
points; the horizontal line is read as the mean. The EPI circles touch each other and the mean line
is drawn across them, so those groups give the line only (countable: false, no points).
"""
import numpy as np

from livinglit.figures.source import RASTER_UNCERTAINTY_PX_300DPI, blobs, calibrate, colour_mask, dark_mask

AXIS_X = (172, 177)      # px columns of the y axis line
TICK_X = (163, 171)      # px columns of the tick marks, left of the axis
UPPER = [5, 4, 3, 2, 1]  # printed tick labels, top to bottom, upper segment
LOWER = [0.15, 0.10, 0.05, 0.00]
PLOT_X = (185, 520)      # px columns of the plotting area (legend lies to the right)
PLOT_Y = (0, 345)        # px rows above the x axis
MARKER_AREA = (150, 200)  # px area of one whole 13x13 square marker


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
        w = rows[a - 1:b + 2]
        ys.append(float(np.sum(np.arange(a - 1, b + 2) * w) / np.sum(w)))
    return ys


def _segments(gray):
    axis = (gray[:, AXIS_X[0]:AXIS_X[1] + 1] < 100).any(axis=1)
    return [r for r in _runs(axis) if r[1] - r[0] > 50]


def _line_y(gray, cols, rows):
    """Darkness-weighted row of a horizontal line seen in the given columns (markers excluded)."""
    sub = 255.0 - gray[rows[0]:rows[1] + 1][:, cols]
    w = np.where(sub > 30, sub, 0).sum(axis=1)
    return float(np.sum(np.arange(rows[0], rows[1] + 1) * w) / np.sum(w))


def _interval(cal, pos, unc):
    v = cal.value(pos)
    lo, hi = cal.interval(pos, unc)
    return [v, min(lo, v) - cal.residual, max(hi, v) + cal.residual]


def read(fig):
    img, scale = fig.render(300)
    gray = img.astype(float).mean(axis=2)
    unc = RASTER_UNCERTAINTY_PX_300DPI

    segs = _segments(gray)
    if len(segs) < 2:
        raise ValueError(f"expected a broken y axis with two segments, found {segs}")
    up_seg, lo_seg = segs[0], segs[1]
    ticks = _ticks(gray)
    up_t = [y for y in ticks if up_seg[0] - 3 <= y <= up_seg[1] + 3]
    lo_t = [y for y in ticks if lo_seg[0] - 3 <= y <= lo_seg[1] + 3]
    if len(up_t) != len(UPPER) or len(lo_t) != len(LOWER):
        raise ValueError(f"tick marks found: upper {up_t}, lower {lo_t}")
    cal_up = calibrate(list(zip(up_t, UPPER)))
    cal_lo = calibrate(list(zip(lo_t, LOWER)))

    def in_plot(b):
        return PLOT_X[0] <= b["x"] <= PLOT_X[1] and PLOT_Y[0] <= b["y"] <= PLOT_Y[1]

    red = colour_mask(img, (255, 0, 0), 90)
    black = dark_mask(img, 80)
    red_b = [b for b in blobs(red, 10) if in_plot(b)]
    black_b = [b for b in blobs(black, 10) if in_plot(b)]

    def squares(bs):
        return [b for b in bs if MARKER_AREA[0] <= b["area"] <= MARKER_AREA[1]
                and 12 <= b["box"][2] <= 14 and 12 <= b["box"][3] <= 14 and b["y"] > lo_seg[0]]

    groups = {}
    for label, bs in (("CTRL-CFs", black_b), ("ACM-CFs", red_b)):
        sq = sorted(squares(bs), key=lambda b: (b["x"], b["y"]))
        pts = []
        for b in sq:
            v, lo, hi = _interval(cal_lo, b["y"], unc)
            pts.append({"value": v, "lo": lo, "hi": hi,
                        "at": list(fig.to_page(b["x"], b["y"], scale))})
        xs = [b["x"] for b in sq]
        x0, x1 = int(min(xs)) - 6, int(max(xs)) + 6
        cols = [c for c in range(x0 - 20, x1 + 21) if all(abs(c - b["x"]) > 8 for b in sq)]
        ys = [b["y"] for b in sq]
        line = _line_y(gray, cols, (int(min(ys)) - 2, int(max(ys)) + 2))
        groups[label] = {"points": pts, "countable": True,
                         "bar": {"mean": _interval(cal_lo, line, unc)}}

    # EPI groups: the mean line across each pair of circles, read in columns clear of the circles
    lines = sorted([b for b in black_b if b["y"] < up_seg[1] and b["box"][2] > 30], key=lambda b: b["x"])
    if len(lines) != 2:
        raise ValueError(f"expected two EPI mean lines, found {lines}")
    for label, b in zip(("CTRL-EPI", "ACM-EPI"), lines):
        x0, w = b["box"][0], b["box"][2]
        xc = x0 + w / 2.0
        cols = [c for c in range(x0, x0 + w) if abs(c - xc) > 9]  # clear of the circles (13 px wide)
        line = _line_y(gray, cols, (b["box"][1], b["box"][1] + b["box"][3] - 1))
        groups[label] = {"points": [], "countable": False, "bar": {"mean": _interval(cal_up, line, unc)}}
    return {"groups": groups}
