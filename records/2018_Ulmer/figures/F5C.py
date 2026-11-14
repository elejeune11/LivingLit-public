"""Fig. 5C: normalized force (%) of 3D CMs over 100 min hypoxia and reoxygenation, mean curves with error bars
for glucose (blue), fatty acid (orange) and lactate (green) (raster, 300 dpi). Printed y tick labels 150 to 0 by 50
are stated here; the x tick marks below the axis stand for 0 to 180 min by 10 (the Baseline point left of 0 is not
read). At each time the curve's value is the mean of the line's centre a few pixels left and right of the error bar
(the error bar hides the line at the time itself); a time where a colour's line is hidden on either side by another
curve is not read. Intervals add half the line's thickness to the raster uncertainty. Error bars are not read."""
import numpy as np

from _util import grey, ticks, cal_from_ticks, y_axis, find_baseline, unc_px, runs

TIMES = list(range(0, 190, 10))


def masks(img):
    r, g, b = (img[:, :, i].astype(int) for i in range(3))
    return {
        "glc": (b - r > 50) & (r < 130) & (g < 130),
        "fa": (r - b > 100) & (r > 180) & (g > 60) & (g < 180),
        "lac": (g - r > 60) & (g - b > 50),
    }


def x_ticks(img, base, x0, x1, depth=(4, 10)):
    """Tick marks below the x axis: columns dark in the rows just under the axis stroke."""
    dark = 255.0 - grey(img)
    prof = dark[base + depth[0]:base + depth[1], x0:x1].mean(axis=0)
    on = prof > 0.35 * prof.max()
    out = []
    for a, b in runs(on):
        w = prof[a:b + 1]
        out.append(x0 + float((np.arange(a, b + 1) * w).sum() / w.sum()))
    return out


def centre(col_mask):
    rr = runs(col_mask)
    if len(rr) != 1:
        return None, None
    a, b = rr[0]
    return (a + b) / 2.0, b - a + 1


def read(fig):
    img, scale = fig.render(300)
    H, W = img.shape[:2]
    col, top, bottom = y_axis(img, (0, 0, W // 3, H))
    base = find_baseline(img, col, bottom)
    cal = cal_from_ticks(ticks(img, col, top, bottom), [150, 100, 50, 0])
    xt = x_ticks(img, base, col + 3, W)
    if len(xt) != len(TIMES) + 1:
        raise ValueError(f"found {len(xt)} x ticks, expected {len(TIMES) + 1} (Baseline + 0..180)")
    xt = xt[1:]  # drop the Baseline tick
    m = masks(img)
    d = 8
    out = {}
    for name, mk in m.items():
        pts = []
        for t, X in zip(TIMES, xt):
            X = int(round(X))
            yl, wl = centre(mk[:base - 2, X - d])
            yr, wr = centre(mk[:base - 2, X + d])
            if yl is None or yr is None:
                continue
            y = (yl + yr) / 2.0
            u = unc_px() + max(wl, wr) / 2.0
            v = cal.value(y)
            lo, hi = cal.interval(y, u)
            pts.append({"value": v, "lo": min(lo, v) - cal.residual, "hi": max(hi, v) + cal.residual,
                        "at": [fig.crop[0] + X / scale, fig.crop[1] + y / scale], "x": float(t)})
        out[name] = {"points": pts}
    return {"groups": out}
