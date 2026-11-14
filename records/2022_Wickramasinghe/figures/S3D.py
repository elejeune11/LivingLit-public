"""Fig. S3D (supplement p. 7): PCA of ATAC-seq, control (grey circles) and GW0742 (pink triangles), n = 3 each. The
page is one image (about 340 dpi). Each marker's PC1 coordinate (horizontal axis) is the reading; PC2 is not stored
(a reading has one value, and an `x` would mark it as a point on a curve).

The plot frame is found from its long dark lines. The x axis has no tick mark that stands clear of its labels (the
labels are printed over the axis line), so it is calibrated on the centres of its four labels -1000, 0, 1000, 2000 (minus sign included); the misfit of that fit is added to every interval.
Markers are the connected fills of the two marker colours inside the frame; a triangle's data position is the
centroid of its fill (R draws pch 24 about its centroid), a circle's the centre of its fill.
"""
import numpy as np

from livinglit.figures.source import calibrate, point, colour_mask, blobs, RASTER_UNCERTAINTY_PX_300DPI

DPI = 300
X_LABELS = [-1000, 0, 1000, 2000]           # printed, left to right
GROUPS = {"S3D_pca/control": (196, 190, 188), "S3D_pca/gw": (204, 132, 132)}   # marker fill colours
FILL_TOL = 18
FILL_AREA = (100, 400)                       # px at 300 dpi; a marker fill is about 150-180 px


def _runs(idx, gap=1):
    """Groups of consecutive indices (allowing gaps up to `gap`)."""
    out = []
    for i in idx:
        if out and i - out[-1][-1] <= gap:
            out[-1].append(i)
        else:
            out.append([i])
    return out


def _frame(lum):
    dark = lum < 128
    cols = [c for c in range(dark.shape[1]) if dark[:, c].sum() > 0.8 * dark.shape[0]]
    rows = [r for r in range(dark.shape[0]) if dark[r, :].sum() > 0.8 * dark.shape[1]]
    left, right = _runs(cols)[0], _runs(cols)[-1]
    top, bottom = _runs(rows)[0], _runs(rows)[-1]
    return np.mean(left), max(left), min(right), np.mean(right), np.mean(top), max(top), min(bottom), np.mean(bottom)


def read(fig):
    img, scale = fig.render(DPI)
    lum = img.astype(float).mean(axis=2)
    lx, lx_in, rx_in, rx, ty, ty_in, by_in, by = _frame(lum)

    # x labels: ink in the rows just above and below the axis line (the line's own 3 rows left out), clustered into
    # labels by gaps wider than 8 px
    r = int(round(by))
    ink = np.vstack([lum[r - 4:r - 1, :], lum[r + 2:r + 7, :]]) < 200
    near = ink.any(axis=0)
    labels = _runs([c for c in range(int(lx_in) + 1, int(rx_in)) if near[c]], gap=8)
    if len(labels) != len(X_LABELS):
        raise ValueError(f"expected {len(X_LABELS)} x labels, found {len(labels)}")
    xcal = calibrate([((run[0] + run[-1]) / 2, v) for run, v in zip(labels, X_LABELS)])

    unc = RASTER_UNCERTAINTY_PX_300DPI * DPI / 300
    misfit_px = xcal.residual / abs(xcal.slope)
    out = {}
    for label, rgb in GROUPS.items():
        pts = []
        found = [b for b in blobs(colour_mask(img, rgb, FILL_TOL), min_area=FILL_AREA[0], max_area=FILL_AREA[1])
                 if lx_in < b["x"] < rx_in and ty_in < b["y"] < by_in]
        for b in sorted(found, key=lambda b: b["x"]):
            pts.append(point(xcal, b["x"], unc + misfit_px, fig.to_page(b["x"], b["y"], scale)))
        out[label] = {"points": pts, "countable": True}
    return {"groups": out}
