"""Fig. 2d: PCA scores of each sample on PC3 (x) and PC4 (y), one marker per sample.

Raster panel (embedded image, ~300 dpi). Legend (printed beside Fig. 2c): green = organoid (open control, filled
infarct), blue = human LV (open non-failing, filled ICM), purple = mouse LV (open sham, filled MI).
Each marker gives two readings, label <group>_pc3 and <group>_pc4; index i is the same marker in both
(markers ordered top to bottom, then left to right).

Only the blue markers each stand alone (8 filled + 8 open, all separate). The green and purple markers
merge into clusters, so those groups return no points (countable: false).
"""
import numpy as np
from scipy import ndimage as nd

from livinglit.figures.source import RASTER_UNCERTAINTY_PX_300DPI, calibrate, dark_mask, point

DPI = 300
GROUPS = ["ctrl", "inf", "m_sham", "m_mi", "h_nf", "h_icm"]


def _tick_centres(profile, rows):
    """Darkness-weighted centre of each run of tick rows."""
    out = []
    for r in rows:
        w = profile[r - 2:r + 3]
        out.append(float(np.sum(np.arange(r - 2, r + 3) * w) / np.sum(w)))
    return out


def _labels(fig, axis, near, tol):
    """Numeric tick labels; this panel prints negatives with an en dash, which tick_marks() does not read."""
    out = []
    for x0, y0, x1, y1, t in fig.words():
        try:
            v = float(t.replace("–", "-").replace("−", "-"))
        except ValueError:
            continue
        pos, other = ((y0 + y1) / 2, (x0 + x1) / 2) if axis == "y" else ((x0 + x1) / 2, (y0 + y1) / 2)
        if abs(other - near) <= tol:
            out.append((pos, v))
    return out


def _axis(fig, img, scale, axis):
    dk = dark_mask(img, 120)
    grey = 255 - img.astype(float).mean(axis=2)
    if axis == "y":
        # vertical axis line: the leftmost long dark column; tick marks run left of it
        x_ax = int(np.argmax(dk.sum(0) > 0.8 * img.shape[0]))
        band = slice(x_ax - 9, x_ax)
        hits = [i for i in range(img.shape[0]) if dk[i, band].sum() >= 6]
        prof = grey[:, band].sum(1)
        near, tol = fig.crop[0] + (x_ax - 15) / scale, 15
    else:
        y_ax = int(np.max(np.nonzero(dk.sum(1) > 0.8 * img.shape[1])[0]))
        band = slice(y_ax + 1, y_ax + 12)
        hits = [j for j in range(img.shape[1]) if dk[band, j].sum() >= 6]
        prof = grey[band, :].sum(0)
        near, tol = fig.crop[1] + (y_ax + 28) / scale, 3
    runs = [h for k, h in enumerate(hits) if k == 0 or h - hits[k - 1] > 1]
    ticks = _tick_centres(prof, runs)
    marks = []
    for pos, v in _labels(fig, axis, near, tol):
        px = (pos - (fig.crop[1] if axis == "y" else fig.crop[0])) * scale
        t = min(ticks, key=lambda q: abs(q - px))
        assert abs(t - px) < 3, (axis, v, px, t)
        marks.append((t, v))
    assert len(marks) == 4, (axis, marks)
    return calibrate(marks)


def read(fig):
    img, scale = fig.render(DPI)
    caly, calx = _axis(fig, img, scale, "y"), _axis(fig, img, scale, "x")
    uy = RASTER_UNCERTAINTY_PX_300DPI + abs(caly.residual / caly.slope)
    ux = RASTER_UNCERTAINTY_PX_300DPI + abs(calx.residual / calx.slope)

    I = img.astype(int)
    r, g, b = I[..., 0], I[..., 1], I[..., 2]
    blue = (b - np.maximum(r, g) > 50) & (np.abs(r - g) < 40)  # purple has r far above g
    lab, n = nd.label(nd.binary_fill_holes(blue))
    markers = {"h_icm": [], "h_nf": []}
    for i in range(1, n + 1):
        reg = lab == i
        area = int(reg.sum())
        if area < 50:
            continue
        ys, xs = np.nonzero(reg)
        # one marker is ~16 x 16 px (area ~195); anything larger would be touching markers
        assert area < 260 and np.ptp(xs) < 18 and np.ptp(ys) < 18, ("blue markers touch", area)
        solid = float(blue[reg].mean())
        markers["h_icm" if solid > 0.9 else "h_nf"].append((float(xs.mean()), float(ys.mean())))

    out = {}
    for grp in GROUPS:
        if grp not in markers:
            out[f"{grp}_pc3"] = {"points": [], "countable": False}
            out[f"{grp}_pc4"] = {"points": [], "countable": False}
            continue
        ms = sorted(markers[grp], key=lambda m: (round(m[1]), m[0]))
        p3, p4 = [], []
        for px, py in ms:
            at = fig.to_page(px, py, scale)
            p3.append(point(calx, px, ux, at))
            p4.append(point(caly, py, uy, at))
        out[f"{grp}_pc3"] = {"points": p3, "countable": True}
        out[f"{grp}_pc4"] = {"points": p4, "countable": True}
    return {"groups": out}
