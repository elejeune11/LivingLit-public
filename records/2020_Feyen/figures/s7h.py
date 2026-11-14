"""Fig. S7H right panel (mmc1.pdf p. 14): b-MHC/cTnT normalized to the mean of control EHTs per batch, ctr vs MM.

Raster image (the whole supplementary page is one picture, ~406 dpi native), rendered at 600 dpi. Two
bars, mean +/- SEM (S7 legend: "Data was presented as mean ±SEM"), one circle per EHT (5 ctr, 5 MM; the
western blot in S7G has 2+1+2 lanes per group over the three batches). ctr: grey markers and error bar
(~120) on a light grey bar (192); MM: black markers and error bar (~5) on a dark grey bar (131). No
marker touches another marker, but some sit on the error bar of their own colour (ctr: one on the upper
cap, one on the vertical line, one on the lower cap; MM: one on the upper cap, one on the vertical
line). Markers are circles ~24 px across, lines ~8-9 px thick. A component larger than one marker is
opened with a 15 px disc, which removes the lines and keeps whole circles. Each marker's position is
the middle of its vertical extent; where an opened blob is taller than the smallest stand-alone marker
(a line remnant), the interval covers every centre a marker of that height could have inside the blob.
The mean is the bar top (fill edge in columns with white above it); the error end is the upper cap,
found in the lines left after removing the opened markers. The y axis is calibrated from its five tick
marks (2.0-0.0).
"""
import numpy as np

from livinglit.figures.source import calibrate, point

DPI = 600
UNC_PX = 1.2  # 0.6 px at 300 dpi
TICK_COLS = (44, 60)  # tick marks left of the axis line (axis at 60-65)
TICK_VALUES = [2.0, 1.5, 1.0, 0.5, 0.0]  # top to bottom
ROW0 = 115  # below the significance bracket (rows 98-103) and asterisk
ROW_END = 710  # above the x axis line (715-720)
MARKER_MAX = 30  # px, a single marker's box side
DISC = 15
CAP_HALF = 40  # px either side of the bar centre searched for a cap (caps ~61 px wide)
# label: (column window px, marker colour threshold, bar fill grey)
GROUPS = {
    "ctr": ((90, 345), 158, 192),
    "mm": ((345, 560), 68, 131),
}
INSIDE_ROW = 700  # a row inside both bars below every marker


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


def _markers(m):
    """Marker blobs (top row, bottom row, centroid col, opened) and the line pixels left once markers are removed."""
    import cv2
    blobs = []
    lines = np.zeros_like(m, dtype=bool)
    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (DISC, DISC))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), connectivity=8)
    for i in range(1, n):
        w, h, a = stats[i, 2], stats[i, 3], stats[i, 4]
        if a < 30:
            continue
        comp = lab == i
        if w <= MARKER_MAX and h <= MARKER_MAX:
            parts, opened_flag = [comp], False
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
            grown = cv2.dilate(opened, np.ones((9, 9), np.uint8)) > 0
            lines |= comp & ~grown
            opened_flag = True
        for p in parts:
            rows = np.nonzero(p.any(axis=1))[0]
            xs = np.nonzero(p)[1]
            blobs.append((int(rows[0]), int(rows[-1]), float(xs.mean()), opened_flag))
    return blobs, lines


def _upper_cap(lines, centre):
    """Row centre (half-extent) and centre column of the topmost cap row cluster, or None.

    A cap row has line pixels spanning 45-75 px within CAP_HALF of the bar centre (a marker on the cap
    splits it into pieces, so the span is taken from the first to the last line pixel, not one run)."""
    c0 = int(round(centre)) - CAP_HALF
    rows, centres = [], {}
    for r in range(lines.shape[0]):
        xs = np.nonzero(lines[r, c0:c0 + 2 * CAP_HALF + 1])[0]
        if len(xs) >= 20 and 45 <= xs[-1] - xs[0] + 1 <= 75:
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
    for label, ((x0, x1), thr, fill) in GROUPS.items():
        win = np.zeros_like(g, dtype=bool)
        win[ROW0:ROW_END, x0:x1] = True
        m = (g < thr) & win
        blobs, lines = _markers(m)
        alone = [b - t + 1 for t, b, _, o in blobs if not o]
        if not alone:
            raise ValueError(f"{label}: no stand-alone marker to size the others")
        d_min = min(alone)
        pts = []
        for top, bottom, cx, opened in sorted(blobs, key=lambda t: t[0]):
            h = bottom - top + 1
            if h > d_min:  # centre lies between top + d/2 and bottom - d/2
                lo_c, hi_c = top + (d_min - 1) / 2, bottom - (d_min - 1) / 2
            else:
                lo_c = hi_c = (top + bottom) / 2
            cy = (lo_c + hi_c) / 2
            p = point(cal, cy, UNC_PX + (hi_c - lo_c) / 2, fig.to_page(cx, cy, scale))
            p["lo"] -= res
            p["hi"] += res
            pts.append(p)
        bar_cols = [c for c in range(x0, x1) if abs(g[INSIDE_ROW, c] - fill) <= 6]
        top, th = _bar_top(g, bar_cols[0] + 2, bar_cols[-1] - 1, fill, ROW0, ROW_END)
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
