"""Fig. 5C (main.pdf p. 11): MDS plot of day-5 progenitors, raster image at its native 300 dpi.

Each point is one sample: value = leading logFC dim 2 (y axis), x = leading logFC dim 1 (x axis).
Axes are calibrated from the tick marks found in the image (labels as printed: y 1, 0, -1, -2 top to
bottom; x -2 .. 2 left to right). Markers are found by colour; the legend box's markers are excluded.
The two gut markers overlap into one blob (not standing alone), so gut gives only the blob's centre,
which for two equal circles is the mean of the two samples (countable: false).
"""
import numpy as np

from livinglit.figures.source import RASTER_UNCERTAINTY_PX_300DPI, blobs, calibrate, colour_mask, point

DPI = 300
Y_TICKS = [1, 0, -1, -2]          # as printed, top to bottom
X_TICKS = [-2, -1, 0, 1, 2]       # as printed, left to right
COLOURS = {"Multilineage": (37, 146, 199), "Cardiac": (186, 31, 0), "Gut": (12, 21, 82)}
STANDALONE = {"Multilineage": True, "Cardiac": True, "Gut": False}


def _runs(idx):
    """Centres of runs of consecutive indices."""
    out, start = [], None
    for i, v in enumerate(idx):
        if start is None:
            start = v
        if i == len(idx) - 1 or idx[i + 1] != v + 1:
            out.append((start + v) / 2)
            start = None
    return out


def read(fig):
    img, s = fig.render(DPI)
    dark = img.astype(int).mean(axis=2) < 110
    h, w = dark.shape
    rows = np.where(dark.sum(1) > 0.6 * w)[0]
    cols = np.where(dark.sum(0) > 0.6 * h)[0]
    top, bottom, left, right = rows.min(), rows.max(), cols.min(), cols.max()

    # tick marks: short dark segments just outside the left and bottom frame lines
    ys = _runs([i for i in np.where(dark[:, left - 5:left - 1].sum(1) >= 2)[0] if i <= bottom])
    xs = _runs(list(np.where(dark[bottom + 1:bottom + 5, :].sum(0) >= 2)[0]))
    if len(ys) != len(Y_TICKS) or len(xs) != len(X_TICKS):
        raise ValueError(f"tick marks found: y {ys}, x {xs}")
    ycal = calibrate(list(zip(ys, Y_TICKS)))
    xcal = calibrate(list(zip(xs, X_TICKS)))
    yunc = RASTER_UNCERTAINTY_PX_300DPI + ycal.residual / abs(ycal.slope)
    xunc = RASTER_UNCERTAINTY_PX_300DPI + xcal.residual / abs(xcal.slope)

    # legend box: the long dark lines inside the frame
    inner = dark[top + 5:bottom - 5, left + 5:right - 5]
    leg_top = top + 5 + np.where(inner.sum(1) > 0.3 * (right - left))[0].min()
    leg_left = left + 5 + np.where(inner.sum(0) > 0.3 * (bottom - top))[0].min()

    groups = {}
    for label, rgb in COLOURS.items():
        found = [b for b in blobs(colour_mask(img, rgb, 50), min_area=50)
                 if left + 3 < b["x"] < right - 3 and top + 3 < b["y"] < bottom - 3
                 and not (b["x"] > leg_left and b["y"] > leg_top)]
        found.sort(key=lambda b: (b["x"], b["y"]))
        if STANDALONE[label]:
            pts = [point(ycal, b["y"], yunc, fig.to_page(b["x"], b["y"], s), x=round(xcal.value(b["x"]), 3))
                   for b in found]
            groups[label] = {"points": pts, "countable": True}
        else:
            if len(found) != 1:
                raise ValueError(f"{label}: expected one merged blob, found {len(found)}")
            b = found[0]
            v = ycal.value(b["y"])
            lo, hi = ycal.interval(b["y"], yunc)
            groups[label] = {"points": [], "countable": False,
                             "bar": {"mean": [v, min(lo, v), max(hi, v)], "x": round(xcal.value(b["x"]), 3)}}
    return {"groups": groups}
