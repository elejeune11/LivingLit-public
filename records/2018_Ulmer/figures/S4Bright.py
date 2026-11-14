"""Fig. S4B (right): mtDNA content (Mt-DNA/g-actin) per line, ND1 and ND2 columns for 2D (blue) and 3D (red);
read here: control line 2, ND2, 2D (blue triangles) and 3D (red triangles) (raster image embedded at ~218 dpi,
rendered at 300 dpi). Printed y tick labels 4000 to 0 by 1000 are stated here. The eight x tick marks stand for
the columns line 1 2D ND1, ND2, 3D ND1, ND2, line 2 2D ND1, ND2, 3D ND1, ND2. A marker is a blob of saturated
colour within half a column spacing of its tick; its value is the centre of the blob's bounding box. Counts are
used only when every blob has one marker's size."""
import numpy as np

from _util import grey, ticks, cal_from_ticks, y_axis, find_baseline, unc_px, runs
from livinglit.figures.source import blobs

NATIVE_DPI = 218


def x_ticks(img, base, x0, x1, depth=(4, 10)):
    dark = 255.0 - grey(img)
    prof = dark[base + depth[0]:base + depth[1], x0:x1].mean(axis=0)
    on = prof > 0.35 * prof.max()
    out = []
    for a, b in runs(on):
        w = prof[a:b + 1]
        out.append(x0 + float((np.arange(a, b + 1) * w).sum() / w.sum()))
    return out


def read(fig):
    img, scale = fig.render(300)
    H, W = img.shape[:2]
    col, top, bottom = y_axis(img, (0, 0, W // 3, H))
    base = find_baseline(img, col, bottom)
    cal = cal_from_ticks(ticks(img, col, top, bottom), [4000, 3000, 2000, 1000, 0])
    xt = x_ticks(img, base, col + 6, W)
    if len(xt) != 8:
        raise ValueError(f"found {len(xt)} x ticks, expected 8")
    half = (xt[-1] - xt[0]) / 7 / 2
    r, g, b = (img[:, :, i].astype(int) for i in range(3))
    blue = (b - r > 35) & (r < 140) & (b > 100)
    red = (r - b > 90) & (r > 180) & (g < 150)
    out = {}
    for label, mk, tick in (("line 2 2D ND2", blue, xt[5]), ("line 2 3D ND2", red, xt[7])):
        m = mk.copy()
        m[:, :int(tick - half)] = False
        m[:, int(tick + half):] = False
        m[base - 1:, :] = False
        bl = blobs(m, min_area=20)
        areas = [x["area"] for x in bl]
        pts = []
        for x in sorted(bl, key=lambda q: q["y"]):
            bx, by, bw, bh = x["box"]
            cy = by + (bh - 1) / 2.0
            cx = bx + (bw - 1) / 2.0
            v = cal.value(cy)
            lo, hi = cal.interval(cy, unc_px(NATIVE_DPI))
            pts.append({"value": v, "lo": min(lo, v) - cal.residual, "hi": max(hi, v) + cal.residual,
                        "at": [fig.crop[0] + cx / scale, fig.crop[1] + cy / scale]})
        alone = bool(areas) and max(areas) <= 1.6 * min(areas)
        out[label] = {"points": pts if alone else [], "countable": alone}
    return {"groups": out}
