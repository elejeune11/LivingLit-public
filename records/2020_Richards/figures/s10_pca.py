"""Supplementary Fig. 10b: PCA scores of each sample on PC3 (x) and PC4 (y), Donor B organoids with mouse and human LV.

The panel is a raster TIFF (word/media/image10.tif, 150 dpi) embedded in the supplement .docx;
crop is panel b's box in that image's pixels. Legend: dark green = Donor B organoid (open control,
filled infarct, n = 3 each), blue = human LV (open non-failing, filled ICM, n = 8 each), purple =
mouse LV (open sham, filled MI, n = 4 each).
Each marker gives two readings, label <group>_pc3 and <group>_pc4; index i is the same marker in
both (markers ordered top to bottom).

Only the blue markers each stand alone (8 filled + 8 open, each one blob of one marker's area).
The green control rings and infarct dots each merge into one blob of three; the purple sham rings
merge into one blob; the purple MI dots show as one double blob and one single dot (n = 4). Those
groups return no points (countable: false). Panel a (PC1/PC2 strip plot) is not read: every group
there is a merged cluster.
"""
import numpy as np
from scipy import ndimage as nd

from _util import dark, docx_image, row_centre
from livinglit.figures.source import RASTER_UNCERTAINTY_PX_300DPI, calibrate, point

MEMBER = "word/media/image10.tif"
DPI = 150
# printed labels; rows/columns are search hints. The -20 tick on y carries no printed label and is not used.
Y_TICKS = {20.0: 92.5, 10.0: 144.0, 0.0: 195.5, -10.0: 247.0, -30.0: 350.0}
X_TICKS = {-40.0: 721.0, -20.0: 810.0, 0.0: 897.5, 20.0: 986.5}
GROUPS = ["ctrl", "inf", "m_sham", "m_mi", "h_nf", "h_icm"]


def _col_centre(img, rows, cols):
    win = img[rows.start:rows.stop, cols.start:cols.stop].astype(float).mean(axis=2)
    w = (255.0 - win).sum(axis=0)
    return float((np.arange(cols.start, cols.stop) * w).sum() / w.sum())


def read(fig):
    img = docx_image(fig.pdf, MEMBER)
    x0, y0, x1, y1 = (int(v) for v in fig.crop)
    d = dark(img)
    px = RASTER_UNCERTAINTY_PX_300DPI * DPI / 300

    # plot frame of panel b: the long dark columns and rows inside the crop
    cols = x0 + np.nonzero(d[y0:y1, x0:x1].sum(axis=0) > 0.6 * (y1 - y0))[0]
    rows = y0 + np.nonzero(d[y0:y1, x0:x1].sum(axis=1) > 0.5 * (x1 - x0))[0]
    left, right, top, bottom = int(cols.min()), int(cols.max()), int(rows.min()), int(rows.max())

    ymarks = [(row_centre(img, range(int(h) - 3, int(h) + 4), range(left - 12, left - 1)), v) for v, h in Y_TICKS.items()]
    xmarks = [(_col_centre(img, range(bottom + 2, bottom + 14), range(int(h) - 3, int(h) + 4)), v) for v, h in X_TICKS.items()]
    for (pos, _), hint in zip(ymarks + xmarks, list(Y_TICKS.values()) + list(X_TICKS.values())):
        if abs(pos - hint) > 1.5:
            raise ValueError(f"tick mark not found near {hint}")
    caly, calx = calibrate(ymarks), calibrate(xmarks)
    my, mx = abs(caly.residual / caly.slope), abs(calx.residual / calx.slope)

    I = img.astype(int)
    r, g, b = I[..., 0], I[..., 1], I[..., 2]
    blue = (b - np.maximum(r, g) > 50) & (np.abs(r - g) < 40)  # purple has r far above g
    inner = np.zeros_like(blue)
    inner[top + 3:bottom - 2, left + 3:right - 2] = True
    lab, n = nd.label(blue & inner, structure=np.ones((3, 3)))

    found = {"h_icm": [], "h_nf": []}
    areas = []
    for i in range(1, n + 1):
        reg = lab == i
        if reg.sum() < 20:
            continue  # anti-aliasing specks
        filled = nd.binary_fill_holes(reg)
        solid = reg.sum() / filled.sum() > 0.9  # an open ring encloses white pixels; a filled dot does not
        ys, xs = np.nonzero(reg)
        found["h_icm" if solid else "h_nf"].append((reg, xs, ys))
        areas.append(int(filled.sum()))

    single_area = float(np.median(areas))
    out = {}
    for grp in GROUPS:
        ms = found.get(grp)
        if not ms or any(not 0.75 * single_area <= nd.binary_fill_holes(m[0]).sum() <= 1.35 * single_area for m in ms):
            out[f"{grp}_pc3"] = {"points": [], "countable": False}
            out[f"{grp}_pc4"] = {"points": [], "countable": False}
            continue
        p3, p4 = [], []
        for reg, xs, ys in sorted(ms, key=lambda m: m[2].mean()):
            w = (255.0 - r[reg]).astype(float)  # ink weight: red channel is 0 on the blue ink
            cx, cy = float((xs * w).sum() / w.sum()), float((ys * w).sum() / w.sum())
            bx, by = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
            at = (cx, cy)
            p3.append(point(calx, cx, px + abs(cx - bx) + mx, at))
            p4.append(point(caly, cy, px + abs(cy - by) + my, at))
        out[f"{grp}_pc3"] = {"points": p3, "countable": True}
        out[f"{grp}_pc4"] = {"points": p4, "countable": True}
    return {"groups": out}
