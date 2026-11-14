"""Fig. S6B (mmc1.pdf p. 12): adult/fetal SCN5a expression ratio (qPCR), RPMI/B27 vs MM.

Raster image (the whole supplementary page is one picture). Bar chart, mean +/- error bar,
one filled circle per batch (n = 4). RPMI/B27: grey circles and error bar (~129) on a light
grey bar (~192); MM: black circles and error bar (~6) on a dark grey bar (~130). In each group
the circles are apart from each other, but some sit on error-bar lines: RPMI/B27 has one circle
on the vertical line and one on the lower cap; MM has one circle touching the upper cap, one on
the vertical line and one at each end of the lower cap. The lines are ~3 px thick at 300 dpi
and the circles ~11 px across, so a morphological opening with a 9 px disc removes the lines
and keeps the circles; each circle's centre is the mean of its blob centroid and the midpoints
of its chords in the columns 4 px either side of the centroid, skipping a chord that runs into a
line (longer than a circle), and the interval covers all estimates. The mean is the bar top
(fill edge, in columns with white above it); the error end is the upper cap (rows with a run of
24-50 px of line colour). The y axis is calibrated from its five tick marks (20-0).
"""
import numpy as np

from livinglit.figures.source import blobs, calibrate, point

DPI = 300
UNC_PX = 0.6
TICK_COLS = (86, 92)  # tick marks left of the axis line
TICK_VALUES = [20, 15, 10, 5, 0]  # top to bottom
MAX_CHORD = 14
# label: (column window px, rows (below the significance bracket, above the x axis),
#         line/marker colour threshold, bar fill grey, a row inside the bar below every marker)
GROUPS = {
    "rpmi": ((120, 215), (75, 321), 160, 192, 310),
    "mm": ((215, 312), (75, 321), 70, 130, 200),
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
    """Darkness-weighted row centres of the y tick marks, top first, with half-widths."""
    band = 255 - g[:, TICK_COLS[0]:TICK_COLS[1]].mean(axis=1)
    out = []
    for a, b in _runs(list(band > 60)):
        rows = np.arange(a - 1, b + 2)
        w = band[a - 1:b + 2]
        out.append((float((rows * w).sum() / w.sum()), (b - a + 1) / 2))
    return out


def _chord_mid(m, r, c):
    if not m[r, c]:
        return None
    a, z = r, r
    while m[a - 1, c]:
        a -= 1
    while m[z + 1, c]:
        z += 1
    if z - a + 1 > MAX_CHORD:
        return None  # runs into an error-bar line
    return (a + z) / 2


def _markers(m):
    """Marker centres (col, row, half-interval px) in a window mask with the lines opened away."""
    import cv2
    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    opened = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, disc)
    out = []
    for b in blobs(opened, min_area=30, max_area=250):
        cx, cy = b["x"], b["y"]
        r = int(round(cy))
        mids = [v for v in (_chord_mid(m, r, int(round(cx)) + d) for d in (-4, 4)) if v is not None]
        if not mids:
            raise ValueError(f"no clean chord for the marker at ({cx:.1f}, {cy:.1f})")
        est = [cy] + mids
        out.append((cx, float(np.mean(est)), UNC_PX + (max(est) - min(est)) / 2))
    return out


def _caps(m, x0):
    """Row centres of the error-bar caps (rows whose longest line-colour run is 24-50 px), top first; centre column."""
    rows, centres = [], {}
    for r in range(m.shape[0]):
        best = max(((b - a + 1, (a + b) / 2) for a, b in _runs(list(m[r]))), default=(0, 0))
        if 24 <= best[0] <= 50:
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
    cal = calibrate([(row, v) for (row, _h), v in zip(ticks, TICK_VALUES)])
    res = cal.residual
    out = {}
    for label, ((x0, x1), (r0, r1), thr, fill, inside) in GROUPS.items():
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
