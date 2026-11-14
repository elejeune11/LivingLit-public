"""Supplementary Fig. 13b: XTT normalized absorbance of 2D hiPSC-CMs, control vs 1% O2 + 1 µM NE, at 0-10 µM DOX.

The panel is a raster TIFF (word/media/image13.tiff, 220 dpi) embedded in the supplement .docx; crop is
the panel's box in that image's pixels. Eight bars (mean ± s.d.) in figure order: control and
1% O2 + 1 µM NE at 0, 0.1, 1 and 10 µM DOX, each with one dot per well (blue = control, orange =
infarct), drawn over the bar and its error bar. Only the 1 and 10 µM bars are read. A group's dots
give points only when every dot blob is one marker; otherwise the group gives its bar only
(countable: false). The bar mean is the centre of the bar's top stroke, found from the top of its
side strokes and the stroke width; the error is the centre of the upper cap where dots leave
enough of it visible.
"""
import numpy as np

from _util import dark, docx_image, row_centre
from livinglit.figures.source import RASTER_UNCERTAINTY_PX_300DPI, blobs, calibrate, colour_mask, point

MEMBER = "word/media/image13.tiff"
DPI = 220
TICKS = {2.0: 93, 1.5: 163, 1.0: 233.5, 0.5: 304, 0.0: 374}  # printed tick labels; rows are search hints only
BARS = ["c0", "i0", "c01", "i01", "c1", "i1", "c10", "i10"]  # figure order, left to right
READ = {"c1": "control_1uM", "i1": "infarct_1uM", "c10": "control_10uM", "i10": "infarct_10uM"}
DOT = {"c": (0, 0, 255), "i": (255, 96, 0)}
CAP_HALF = 7  # half width of an error bar cap, px


def read(fig):
    img = docx_image(fig.pdf, MEMBER)
    x0, y0, x1, y1 = (int(v) for v in fig.crop)
    d = dark(img)
    px = RASTER_UNCERTAINTY_PX_300DPI * DPI / 300

    # y axis: the longest dark column in the left half; tick marks just left of it
    colsum = d[y0:y1, x0:x1].sum(axis=0)
    axis_x = x0 + int(np.argmax(colsum[: (x1 - x0) // 2]))
    marks = []
    for v, hint in TICKS.items():
        h = int(hint)
        marks.append((row_centre(img, range(h - 3, h + 4), range(axis_x - 7, axis_x - 1)), v))
    cal = calibrate(marks)
    misfit = cal.residual / abs(cal.slope)
    base = int(round(max(m[0] for m in marks)))  # the 0.0 line, drawn thick across the plot
    top_tick = min(m[0] for m in marks)

    # bar sides: dark runs on the row just above the 0.0 line, between the axis and the frame
    row = base - 3
    frame_x = x0 + (x1 - x0) // 2 + int(np.argmax(colsum[(x1 - x0) // 2:]))
    xs = [x for x in range(axis_x + 4, frame_x - 3) if d[row, x]]
    sides, run = [], [xs[0]]
    for x in xs[1:]:
        if x - run[-1] <= 1:
            run.append(x)
        else:
            sides.append(run)
            run = [x]
    sides.append(run)
    if len(sides) != 2 * len(BARS):
        raise ValueError(f"expected {2 * len(BARS)} bar sides, found {len(sides)}")
    bars = {b: (sides[2 * i], sides[2 * i + 1]) for i, b in enumerate(BARS)}

    # dots: saturated blue / orange blobs inside the plot
    dots = {}
    for k, rgb in DOT.items():
        m = colour_mask(img, rgb, tol=60)
        m[: int(top_tick) - 5, :] = False
        m[base + 8:, :] = False
        m[:, : axis_x + 3] = False
        m[:, frame_x - 2:] = False
        dots[k] = blobs(m, min_area=10)
    med = float(np.median([b["area"] for k in dots for b in dots[k]]))
    occluded = np.zeros(d.shape, bool)
    for rgb in DOT.values():
        occluded |= colour_mask(img, rgb, tol=150)

    out = {}
    for b, label in READ.items():
        left, right = bars[b]
        bl, br = left[0], right[-1]
        c = (bl + br) / 2
        # mean: top edge of the side strokes plus half the stroke width
        edges = []
        for x in left + right:
            r = base - 3
            while r > top_tick and d[r - 1, x]:
                r -= 1
            above = 1.0 - img[r - 1, x].astype(float).mean() / 255.0
            edges.append(r - above)
        width = (len(left) + len(right)) / 2
        mean_pos = float(np.median(edges)) - 0.5 + width / 2
        bar = {"mean": _iv(cal, mean_pos, 1.0 + misfit)}
        # error: first cap run above the bar top, along the whisker; cap pixels hidden under dots are skipped
        ci = int(round(c))
        cols = [x for x in range(ci - CAP_HALF, ci + CAP_HALF + 1) if abs(x - c) > 2.5]
        cap = []
        for r in range(int(mean_pos) - 4, int(top_tick), -1):
            if not (d[r, ci - 1:ci + 2] | occluded[r, ci - 1:ci + 2]).any():
                break  # the whisker ended without a visible cap
            seen = [x for x in cols if not occluded[r, x]]
            hit = len(seen) >= 4 and np.mean([d[r, x] for x in seen]) >= 0.8
            if hit:
                cap.append(r)
            elif cap:
                break
        if cap:
            bar["error"] = _iv(cal, float(np.mean(cap)), 1.0 + misfit)
        g = {"points": [], "countable": False, "bar": bar}
        own = [p for p in dots[b[0]] if bl - 12 <= p["x"] <= br + 12]
        if own and all(0.6 * med <= p["area"] <= 1.4 * med for p in own):
            pts = []
            for p in sorted(own, key=lambda p: (p["y"], p["x"])):
                _, by, _, bh = p["box"]
                box_y = by + (bh - 1) / 2
                y = (p["y"] + box_y) / 2
                unc = px + abs(p["y"] - box_y) / 2 + misfit
                pts.append(point(cal, y, unc, (p["x"], y)))
            g["points"], g["countable"] = pts, True
        out[label] = g
    return {"groups": out}


def _iv(cal, pos, unc):
    lo, hi = cal.interval(pos, unc)
    v = cal.value(pos)
    return [v, min(lo, v), max(hi, v)]
