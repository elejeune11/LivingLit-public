"""Supplementary Fig. 9: PCA scores of each organoid sample on PC1 (x) and PC2 (y), two iPSC donors.

The panel is a raster TIFF (word/media/image9.tif, 150 dpi) embedded in the supplement .docx;
crop is the whole image in its own pixels. Legend: bright green = Donor A, dark green = Donor B;
open circle = control organoid, filled circle = infarct organoid (n = 3 each).
Each marker gives two readings, label <group>_pc1 and <group>_pc2; index i is the same marker in
both (markers ordered top to bottom).

Only Donor B's markers each stand alone (3 open + 3 filled, each one blob of one marker's area).
Donor A's control rings: one alone, two touching; Donor A's infarct dots merge into one blob of
three. Those groups return no points (countable: false).
"""
import numpy as np
from scipy import ndimage as nd

from _util import dark, docx_image, row_centre
from livinglit.figures.source import RASTER_UNCERTAINTY_PX_300DPI, calibrate, point

MEMBER = "word/media/image9.tif"
DPI = 150
Y_TICKS = {40.0: 55.5, 20.0: 129.5, 0.0: 204.5, -20.0: 277.5, -40.0: 351.5}  # printed labels; rows are search hints
X_TICKS = {-50.0: 192.5, 0.0: 301.5, 50.0: 412.5}  # printed labels; columns are search hints
BRIGHT = 180  # Donor A green (0, 255, 0) vs Donor B green (0, 100, 0): median green channel of the marker's ink
GROUPS = ["a_ctrl", "a_inf", "b_ctrl", "b_inf"]


def _col_centre(img, rows, cols):
    win = img[rows.start:rows.stop, cols.start:cols.stop].astype(float).mean(axis=2)
    w = (255.0 - win).sum(axis=0)
    return float((np.arange(cols.start, cols.stop) * w).sum() / w.sum())


def read(fig):
    img = docx_image(fig.pdf, MEMBER)
    d = dark(img)
    px = RASTER_UNCERTAINTY_PX_300DPI * DPI / 300

    # plot frame: the long dark columns and rows
    cols = np.nonzero(d.sum(axis=0) > 0.6 * img.shape[0])[0]
    rows = np.nonzero(d.sum(axis=1) > 0.4 * img.shape[1])[0]
    left, right, top, bottom = int(cols.min()), int(cols.max()), int(rows.min()), int(rows.max())

    ymarks = [(row_centre(img, range(int(h) - 3, int(h) + 4), range(left - 10, left - 1)), v) for v, h in Y_TICKS.items()]
    xmarks = [(_col_centre(img, range(bottom + 2, bottom + 11), range(int(h) - 3, int(h) + 4)), v) for v, h in X_TICKS.items()]
    for (pos, _), hint in zip(ymarks + xmarks, list(Y_TICKS.values()) + list(X_TICKS.values())):
        if abs(pos - hint) > 1.5:
            raise ValueError(f"tick mark not found near {hint}")
    caly, calx = calibrate(ymarks), calibrate(xmarks)
    my, mx = abs(caly.residual / caly.slope), abs(calx.residual / calx.slope)

    I = img.astype(int)
    r, g, b = I[..., 0], I[..., 1], I[..., 2]
    green = g - np.maximum(r, b) > 10
    inner = np.zeros_like(green)
    inner[top + 2:bottom - 1, left + 2:right - 1] = True
    lab, n = nd.label(green & inner, structure=np.ones((3, 3)))

    found = {grp: [] for grp in GROUPS}
    areas = []
    for i in range(1, n + 1):
        reg = lab == i
        if reg.sum() < 20:
            continue  # anti-aliasing specks
        ink = reg & (r < 60)  # pure ink pixels, not blended with the white ground
        donor = "a" if np.median(g[ink]) > BRIGHT else "b"
        filled = nd.binary_fill_holes(reg)
        solid = reg.sum() / filled.sum() > 0.9  # an open ring encloses white pixels; a filled dot does not
        ys, xs = np.nonzero(reg)
        found[f"{donor}_{'inf' if solid else 'ctrl'}"].append((reg, xs, ys))
        areas.append(int(filled.sum()))

    single_area = float(np.median(areas))
    out = {}
    for grp in GROUPS:
        ms = found[grp]
        if not ms:
            raise ValueError(f"no markers found for {grp}")
        if any(not 0.75 * single_area <= nd.binary_fill_holes(m[0]).sum() <= 1.35 * single_area for m in ms):
            out[f"{grp}_pc1"] = {"points": [], "countable": False}
            out[f"{grp}_pc2"] = {"points": [], "countable": False}
            continue
        p1, p2 = [], []
        for reg, xs, ys in sorted(ms, key=lambda m: m[2].mean()):
            w = (255.0 - r[reg]).astype(float)  # ink weight: red channel is 0 on both greens
            cx, cy = float((xs * w).sum() / w.sum()), float((ys * w).sum() / w.sum())
            bx, by = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
            at = (cx, cy)
            p1.append(point(calx, cx, px + abs(cx - bx) + mx, at))
            p2.append(point(caly, cy, px + abs(cy - by) + my, at))
        out[f"{grp}_pc1"] = {"points": p1, "countable": True}
        out[f"{grp}_pc2"] = {"points": p2, "countable": True}
    return {"groups": out}

