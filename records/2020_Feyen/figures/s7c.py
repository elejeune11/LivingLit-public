"""Fig. S7C left panel (mmc1.pdf p. 14): mt-DNA ND1/g-actin (qPCR), ctr vs MM.

Raster image (the whole supplementary page is one picture). Bar chart, mean +/- SEM (legend: "Data was
presented as mean ±SEM"), one marker per EHT; the marker shape (circle, square, triangle, diamond) marks the
batch. ctr: grey markers and error bar (~160) on a light grey bar (~207); MM: black markers and error bar
(~5) on a dark grey bar (~130). No marker touches another, but some sit on error-bar lines: in ctr one
diamond on the right end of the upper cap and one on the left end of the lower cap; in MM one diamond on
the vertical line and one circle on the lower cap. A marker that stands alone in the colour mask is read
from its own pixels; a component holding lines is opened with a 9 px disc at 600 dpi (lines ~4 px,
markers 15-19 px), which removes the lines and keeps the marker cores. Each marker's position is the
middle of its vertical extent; for triangles this differs from the area centroid by a sixth of the
height, and the interval covers both (and the opened blob's extent where opened). The mean is the bar top
(fill edge in columns with white above it); the error end is the upper cap. The y axis is calibrated from
its five tick marks (800-0). The right panel (ND2/g-actin) is not read: the record has one item for both
measures, and its points would be pooled with these.
"""
import numpy as np

from livinglit.figures.source import calibrate, point

DPI = 600
UNC_PX = 1.2  # 0.6 px at 300 dpi
TICK_COLS = (46, 62)  # tick marks left of the axis line (axis at 67-72)
TICK_VALUES = [800, 600, 400, 200, 0]  # top to bottom
ROWS = (180, 664)  # below the significance bracket, above the bar's bottom edge
MARKER_MAX = 24  # px, a single marker's box side
# label: (column window px, line/marker colour threshold, bar fill grey, a row inside the bar below every marker)
GROUPS = {
    "ctr": ((125, 250), 183, 207, 640),
    "mm": ((272, 400), 68, 130, 640),
}


def _runs(flags):
    out, start = [], None
    for i, f in enumerate(flags):
        if f and start is None:
            start = i
        if not f and start is not None:
            out.append((start, i - 1))
            start = None
    if start is not None:
        out.append((start, len(flags) - 1))
    return out


def _ticks(g):
    """Darkness-weighted row centres of the y tick marks, top first."""
    band = 255 - g[:, TICK_COLS[0]:TICK_COLS[1]].mean(axis=1)
    out = []
    for a, b in _runs(list(band > 60)):
        rows = np.arange(a - 1, b + 2)
        w = band[a - 1:b + 2]
        out.append(float((rows * w).sum() / w.sum()))
    return out


def _extent(m):
    """(middle of the vertical extent, centroid row, centroid col) of a single-marker mask."""
    rows = np.nonzero(m.any(axis=1))[0]
    ys, xs = np.nonzero(m)
    return (rows[0] + rows[-1]) / 2, float(ys.mean()), float(xs.mean())


def _markers(m):
    """Marker centres (col, row, half-interval px)."""
    import cv2
    out = []
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), connectivity=8)
    for i in range(1, n):
        w, h, a = stats[i, 2], stats[i, 3], stats[i, 4]
        if a < 30:
            continue
        comp = lab == i
        if w <= MARKER_MAX and h <= MARKER_MAX:
            parts = [comp]
        else:  # markers joined to error-bar lines
            disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
            opened = cv2.morphologyEx(comp.astype(np.uint8), cv2.MORPH_OPEN, disc)
            k, lab2, st2, _ = cv2.connectedComponentsWithStats(opened, connectivity=8)
            parts = []
            for j in range(1, k):
                if st2[j, 4] < 30:
                    continue
                if st2[j, 2] > MARKER_MAX or st2[j, 3] > MARKER_MAX:
                    raise ValueError(f"opened blob too large for one marker: {st2[j].tolist()}")
                parts.append(lab2 == j)
        for p in parts:
            mid, cy, cx = _extent(p)
            est = [mid, cy]
            out.append((cx, float(np.mean([min(est), max(est)])), UNC_PX + (max(est) - min(est)) / 2))
    return out


def _caps(m, x0):
    """Row centres of the error-bar caps (rows whose longest line-colour run is 28-70 px), top first; centre column."""
    rows, centres = [], {}
    for r in range(m.shape[0]):
        best = max(((b - a + 1, (a + b) / 2) for a, b in _runs(list(m[r]))), default=(0, 0))
        if 28 <= best[0] <= 70:
            rows.append(r)
            centres[r] = x0 + best[1]
    groups = _runs([r in rows for r in range(m.shape[0])])
    return [((a + b) / 2, float(np.mean([centres[r] for r in range(a, b + 1)])), (b - a) / 2) for a, b in groups]


def _bar_top(g, x0, x1, fill, r0, r1):
    """Fill edge (row, half-crossing between white and fill) in bar columns with white just above it."""
    tops = []
    for c in range(x0, x1):
        col = g[:, c]
        for r in range(r0 + 3, r1):
            if abs(col[r] - fill) <= 6 and abs(col[r + 1] - fill) <= 6 and abs(col[r + 2] - fill) <= 6:
                if (col[r - 4:r - 2] > 240).all():  # the edge spans up to two anti-aliased rows
                    half = (255 + fill) / 2
                    k = next(k for k in range(r - 3, r + 1) if col[k] <= half)
                    v0, v1 = col[k - 1], col[k]
                    frac = 0.0 if v0 == v1 else (v0 - half) / (v0 - v1)
                    tops.append(k - 1 + min(max(frac, 0.0), 1.0))
                break
    if len(tops) < 10:
        raise ValueError(f"bar top found in only {len(tops)} columns of {x0}-{x1}")
    return float(np.median(tops)), (max(tops) - min(tops)) / 2


def read(fig):
    img, scale = fig.render(DPI)
    g = img.astype(float).mean(axis=2)
    ticks = _ticks(g)
    if len(ticks) != len(TICK_VALUES):
        raise ValueError(f"expected {len(TICK_VALUES)} y tick marks, found {ticks}")
    cal = calibrate(list(zip(ticks, TICK_VALUES)))
    res = cal.residual
    r0, r1 = ROWS
    out = {}
    for label, ((x0, x1), thr, fill, inside) in GROUPS.items():
        win = np.zeros_like(g, dtype=bool)
        win[r0:r1, x0:x1] = True
        m = (g < thr) & win
        pts = []
        for cx, cy, u in sorted(_markers(m), key=lambda t: t[1]):
            p = point(cal, cy, u, fig.to_page(cx, cy, scale))
            p["lo"] -= res
            p["hi"] += res
            pts.append(p)
        caps = _caps(m[:, x0:x1], x0)
        if len(caps) != 2:
            raise ValueError(f"expected 2 caps in {label}, found {caps}")
        (up, ucx, uh), _lower = caps
        bar_cols = [c for c in range(x0, x1) if abs(g[inside, c] - fill) <= 6]
        top, th = _bar_top(g, bar_cols[0] + 2, bar_cols[-1] - 1, fill, r0, r1)
        pm = point(cal, top, UNC_PX + th, fig.to_page(ucx, top, scale))
        pu = point(cal, up, UNC_PX + uh, fig.to_page(ucx, up, scale))
        out[label] = {
            "points": pts,
            "countable": True,
            "bar": {"mean": [pm["value"], pm["lo"] - res, pm["hi"] + res],
                    "error": [pu["value"], pu["lo"] - res, pu["hi"] + res]},
        }
    return {"groups": out}
