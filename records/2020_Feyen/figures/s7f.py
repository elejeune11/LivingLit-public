"""Fig. S7F (mmc1.pdf p. 14): beat rate (BPM, last day of culture) per batch, ctr vs MM.

Raster image (the whole supplementary page is one picture, ~406 dpi native). Six bars, ctr and MM for
batch1-3, mean +/- SEM (S7 legend: "Data was presented as mean ±SEM"), one marker per EHT (legend
n=3-8 EHTs); the marker shape (circle, square, triangle) marks the batch. ctr: grey markers and error
bar (~125) on a light grey bar (~192); MM: black markers and error bar (~5) on a dark grey bar (~130).
No marker touches another marker, but some sit on error-bar lines of their own colour (ctr b1: a circle
on the upper cap; ctr b2: a square on the vertical line; ctr b3: a triangle on the lower cap; MM b2: a
square on the vertical line; MM b3: two triangles at both ends of the caps). A marker that stands
alone in the colour mask is read from its own pixels; a component wider than one marker is opened
with a 7 px disc at 600 dpi (lines ~2-3 px, markers 16-19 px), which removes the lines and keeps the
marker cores. Each marker's position is the middle of its vertical extent; for triangles this differs
from the area centroid by a sixth of the height, and the interval covers both; for opened markers it
also covers up to half the disc radius lost at either end (apices) or gained from a line.
The mean is the bar top (fill edge in columns with white above it); the error end is the upper cap,
found in the lines left after removing the opened markers (not readable where markers cover it).
The y axis is calibrated from its six tick marks (100-0). Points are returned per batch bar; each
label maps to the item's ctr or mm group.
"""
import numpy as np

from livinglit.figures.source import calibrate, point

DPI = 600
UNC_PX = 1.2  # 0.6 px at 300 dpi
TICK_COLS = (110, 128)  # tick marks left of the axis line (axis at 129-134)
TICK_VALUES = [100, 80, 60, 40, 20, 0]  # top to bottom
ROW_END = 520  # above the x axis line (524-529)
MARKER_MAX = 22  # px, a single marker's box side
DISC = 7
CAP_HALF = 26  # px either side of the bar centre searched for a cap (caps ~43 px wide)
# label: (column window px, first row (below brackets and legend), marker colour threshold, bar fill grey)
GROUPS = {
    "ctr_b1": ((165, 275), 120, 158, 192),
    "mm_b1": ((295, 405), 120, 68, 130),
    "ctr_b2": ((425, 535), 115, 158, 192),
    "mm_b2": ((555, 665), 120, 68, 130),
    "ctr_b3": ((685, 795), 251, 158, 192),
    "mm_b3": ((815, 976), 300, 68, 130),
}
INSIDE_ROW = 515  # a row inside every bar below every marker


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
    """Marker centres (col, row, half-interval px) and the line pixels left once markers are removed."""
    import cv2
    out = []
    lines = np.zeros_like(m, dtype=bool)
    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (DISC, DISC))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), connectivity=8)
    for i in range(1, n):
        w, h, a = stats[i, 2], stats[i, 3], stats[i, 4]
        if a < 30:
            continue
        comp = lab == i
        extra = 0.0
        if w <= MARKER_MAX and h <= MARKER_MAX:
            parts = [comp]
        else:  # markers joined to error-bar lines, or the error bar alone
            opened = cv2.morphologyEx(comp.astype(np.uint8), cv2.MORPH_OPEN, disc)
            k, lab2, st2, _ = cv2.connectedComponentsWithStats(opened, connectivity=8)
            parts = []
            for j in range(1, k):
                if st2[j, 4] < 60:
                    continue
                if st2[j, 2] > MARKER_MAX or st2[j, 3] > MARKER_MAX:
                    raise ValueError(f"opened blob too large for one marker: {st2[j].tolist()}")
                parts.append(lab2 == j)
            grown = cv2.dilate(opened, np.ones((5, 5), np.uint8)) > 0
            lines |= comp & ~grown
            extra = DISC / 4  # half the disc radius
        for p in parts:
            mid, cy, cx = _extent(p)
            est = [mid, cy]
            out.append((cx, float(np.mean([min(est), max(est)])), UNC_PX + extra + (max(est) - min(est)) / 2))
    return out, lines


def _upper_cap(lines, centre):
    """Row centre (half-extent) and centre column of the topmost cap row cluster, or None.

    A cap row has line pixels spanning 18-50 px within CAP_HALF of the bar centre (a marker on the cap
    splits it into pieces, so the span is taken from the first to the last line pixel, not one run)."""
    c0 = int(round(centre)) - CAP_HALF
    rows, centres = [], {}
    for r in range(lines.shape[0]):
        xs = np.nonzero(lines[r, c0:c0 + 2 * CAP_HALF + 1])[0]
        if len(xs) >= 12 and 18 <= xs[-1] - xs[0] + 1 <= 50:
            rows.append(r)
            centres[r] = c0 + (xs[0] + xs[-1]) / 2
    groups = _runs([r in rows for r in range(lines.shape[0])])
    if not groups:
        return None
    a, b = groups[0]
    return (a + b) / 2, float(np.mean([centres[r] for r in range(a, b + 1)])), (b - a) / 2


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
    out = {}
    for label, ((x0, x1), r0, thr, fill) in GROUPS.items():
        win = np.zeros_like(g, dtype=bool)
        win[r0:ROW_END, x0:x1] = True
        m = (g < thr) & win
        markers, lines = _markers(m)
        pts = []
        for cx, cy, u in sorted(markers, key=lambda t: t[1]):
            p = point(cal, cy, u, fig.to_page(cx, cy, scale))
            p["lo"] -= res
            p["hi"] += res
            pts.append(p)
        bar_cols = [c for c in range(x0, x1) if abs(g[INSIDE_ROW, c] - fill) <= 6]
        top, th = _bar_top(g, bar_cols[0] + 2, bar_cols[-1] - 1, fill, r0, ROW_END)
        centre = (bar_cols[0] + bar_cols[-1]) / 2
        pm = point(cal, top, UNC_PX + th, fig.to_page(centre, top, scale))
        bar = {"mean": [pm["value"], pm["lo"] - res, pm["hi"] + res]}
        cap = _upper_cap(lines, centre)
        if cap is not None and cap[0] < top:
            up, ucx, uh = cap
            pu = point(cal, up, UNC_PX + uh, fig.to_page(ucx, up, scale))
            bar["error"] = [pu["value"], pu["lo"] - res, pu["hi"] + res]
        out[label] = {"points": pts, "countable": True, "bar": bar}
    return {"groups": out}
