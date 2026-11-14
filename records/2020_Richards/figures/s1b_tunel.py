"""Supplementary Fig. 1b: TUNEL index, exterior vs interior, 10% oxygen and 1 µM norepinephrine organoids.

The panel is a raster TIFF (word/media/image1.tiff, 220 dpi) embedded in the supplement .docx;
crop is the panel's box in that image's pixels. Four bars (mean ± s.d.) in figure order:
10% O2 exterior, 10% O2 interior, NE exterior, NE interior, each with one dot per organoid.
Dots stand alone only for NE interior; the other groups' dots touch or merge into clumps, so
those give the bar only (countable: false). The upper cap of the 10% O2 exterior error bar is
hidden under its dots and is not read.
"""
import numpy as np

from _util import dark, docx_image, row_centre
from livinglit.figures.source import RASTER_UNCERTAINTY_PX_300DPI, blobs, calibrate, colour_mask, point

MEMBER = "word/media/image1.tiff"
DPI = 220
TICKS = {1.5: 63, 1.0: 191.5, 0.5: 319.5, 0.0: 447.5}  # printed tick labels; rows are search hints only
LABELS = ["hyp_exterior", "hyp_interior", "ne_exterior", "ne_interior"]
NE_DOT = (255, 160, 64)
TOP_LIMIT = 175  # rows above hold the significance lines and their labels


def read(fig):
    img = docx_image(fig.pdf, MEMBER)
    x0, y0, x1, y1 = (int(v) for v in fig.crop)
    d = dark(img)
    px = RASTER_UNCERTAINTY_PX_300DPI * DPI / 300

    # y axis: the longest dark column on the left; tick marks just left of it
    colsum = d[y0:y1, x0:x1].sum(axis=0)
    axis_x = x0 + int(np.argmax(colsum[: (x1 - x0) // 2]))
    marks = []
    for v, hint in TICKS.items():
        h = int(hint)
        marks.append((row_centre(img, range(h - 3, h + 4), range(axis_x - 8, axis_x - 1)), v))
    cal = calibrate(marks)
    misfit = cal.residual / abs(cal.slope)
    base = max(m[0] for m in marks)

    # bar outlines: columns dark over most of the lower plot area, between the axis and the frame
    lower = d[int(base) - 150:int(base) - 5, :]
    full = [x for x in range(axis_x + 4, x1 - 6) if lower[:, x].mean() > 0.9]
    groups, run = [], [full[0]]
    for x in full[1:]:
        if x - run[-1] <= 1:
            run.append(x)
        else:
            groups.append(run)
            run = [x]
    groups.append(run)
    top_tick = min(m[0] for m in marks)
    frame = d[int(top_tick) + 20:TOP_LIMIT, :]  # the plot frame's right edge runs the full height; bar sides do not
    sides = [(g[0], g[-1]) for g in groups if frame[:, g[0]].mean() < 0.5]
    if len(sides) != 8:
        raise ValueError(f"expected 8 bar sides, found {len(sides)}")
    bars = [(sides[2 * i][0], sides[2 * i + 1][-1]) for i in range(4)]

    out = {}
    for label, (bl, br) in zip(LABELS, bars):
        c = (bl + br) // 2
        top = next(r for r in range(TOP_LIMIT, int(base))
                   if d[r:r + 9, bl:bl + 2].any(axis=1).all() and d[r:r + 9, br - 1:br + 1].any(axis=1).all())
        mean_pos = top + 0.5
        bar = {"mean": _iv(cal, mean_pos, 1.0 + misfit)}
        caps = [r for r in range(TOP_LIMIT, top) if d[r, c - 9:c + 10].sum() >= 8]
        if caps:
            first = [caps[0]]
            for r in caps[1:]:
                if r - first[-1] == 1:
                    first.append(r)
            bar["error"] = _iv(cal, float(np.mean(first)), 1.0 + misfit)
        g = {"points": [], "countable": False, "bar": bar}
        if label == "ne_interior":
            m = colour_mask(img, NE_DOT, tol=40)
            m[:TOP_LIMIT, :] = False
            m[int(base):, :] = False
            m[:, :bl - 15] = False
            m[:, br + 15:] = False
            dots = blobs(m, min_area=10)
            med = float(np.median([b["area"] for b in dots]))
            if any(not 0.6 * med <= b["area"] <= 1.4 * med for b in dots):
                raise ValueError("a dot blob is not one marker; points do not stand alone")
            pts = []
            for b in sorted(dots, key=lambda b: (b["y"], b["x"])):
                bx, by, bw, bh = b["box"]
                box_y = by + (bh - 1) / 2  # extent centre: robust to a line crossing the dot's interior
                y = (b["y"] + box_y) / 2
                unc = px + abs(b["y"] - box_y) / 2 + misfit
                pts.append(point(cal, y, unc, (b["x"], y)))
            g["points"], g["countable"] = pts, True
        out[label] = g
    return {"groups": out}


def _iv(cal, pos, unc):
    lo, hi = cal.interval(pos, unc)
    v = cal.value(pos)
    return [v, min(lo, v), max(hi, v)]
