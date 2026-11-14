"""Fig. 3B: actin angle histograms (normalized occurrence vs degrees), one representative tissue per loading condition.

Raster image. Four framed panels share one layout; y labels (0 to 0.03 by 0.005) are printed on the first panel only,
and every panel carries the same six tick marks, so each panel is calibrated on its own tick marks. x tick marks run
every 20 degrees across the frame (labels 20, 60, 100, 140 printed at the 2nd, 4th, 6th and 8th marks, so the frame
spans 0 to 180). The curve is the top of the filled histogram, sampled every 10 degrees from 10 to 170.
"""
import numpy as np

from livinglit.figures.source import calibrate, point

DPI = 300
PANELS = ["c1", "d1", "c8", "d8"]          # left to right: 1x Constrained, 1x Dynamic, 8x Constrained, 8x Dynamic
Y_VALUES = [0.03, 0.025, 0.02, 0.015, 0.01, 0.005]   # tick labels, top to bottom (first panel)
X_LABELLED = {1: 20, 3: 60, 5: 100, 7: 140}          # tick index (from the left frame line) -> printed label
SAMPLE_DEG = list(range(10, 171, 10))
PX_UNC = 0.6


def _runs(mask):
    idx = np.flatnonzero(mask)
    out = []
    for i in idx:
        if out and i == out[-1][1] + 1:
            out[-1][1] = i
        else:
            out.append([i, i])
    return [((a + b) / 2, b - a + 1) for a, b in out]


def read(fig):
    img, scale = fig.render(DPI)
    h, w, _ = img.shape
    grey = (img.max(2) < 200) & (np.abs(img[:, :, 2].astype(int) - img[:, :, 0].astype(int)) < 30)
    blue = (img[:, :, 2].astype(int) - img[:, :, 0].astype(int) > 40) & (img[:, :, 0] < 200)
    # frame lines: thin grey vertical lines crossing the plot area well above the fill
    band = slice(int(h * 0.15), int(h * 0.45))
    cols = grey[band].sum(0) > (band.stop - band.start) * 0.9
    frames = [c for c, width in _runs(cols) if width <= 4]
    assert len(frames) == 8, frames
    out = {}
    for k, gid in enumerate(PANELS):
        left, right = frames[2 * k], frames[2 * k + 1]
        L, R = int(round(left)), int(round(right))
        # y tick marks: short grey runs just inside the left frame
        ystrip = grey[:, L + 3:L + 10].any(1)
        yt = [c for c, width in _runs(ystrip) if width <= 4]
        top = yt[0]
        yt = yt[1:1 + len(Y_VALUES) - 1]
        ymarks = [(top, Y_VALUES[0])] + list(zip(yt, Y_VALUES[1:]))
        assert len(ymarks) == len(Y_VALUES), ymarks
        ycal = calibrate(ymarks)
        # x tick marks: short grey runs hanging from the top frame line
        t = int(round(top))
        xstrip = grey[t + 3:t + 12, L:R + 2].any(0)
        xt = [c + L for c, width in _runs(xstrip) if width <= 4]
        assert len(xt) == 10, xt
        xcal = calibrate([(xt[i], v) for i, v in X_LABELLED.items()])
        # degrees -> column
        inv = lambda deg: (deg - xcal.intercept) / xcal.slope
        ymis = ycal.residual / abs(ycal.slope)
        pts = []
        for deg in SAMPLE_DEG:
            cx = int(round(inv(deg)))
            tops = []
            for c in range(cx - 1, cx + 2):
                ys = np.flatnonzero(blue[:, c])
                if len(ys):
                    tops.append(ys.min())
            ytop = float(np.median(tops))
            unc = PX_UNC + ymis + (max(tops) - min(tops)) / 2
            pts.append(point(ycal, ytop, unc, fig.to_page(cx, ytop, scale), x=float(deg)))
        out[gid] = {"points": pts, "countable": True}
    return {"groups": out}
