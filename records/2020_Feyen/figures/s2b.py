"""Fig. S2B right chart (mmc1.pdf p. 4): cTnT mean fluorescent intensity, RPMI/B27 vs MM.

Raster image (the whole supplementary page is one picture). Bar chart, mean +/- error bar,
one filled circle per batch (n = 4). RPMI/B27: grey circles and grey error bar (~130) on
a light grey bar (~192); MM: black circles and black error bar (~7) on a dark grey bar
(~131). In each group the circles are apart from each other, but two of them sit on
error-bar lines (one on the upper cap; one on the vertical line or the lower cap). The
lines are 2-5 px thick at 300 dpi and the circles ~12 px across, so a morphological
opening with a 9 px disc removes the lines and keeps the circles; each circle's centre is
then the midpoint of its chords in the columns 4 px either side of its centroid (clear of
the vertical error line), and the interval covers both estimates. The mean is the bar top
(fill edge, in columns with white above it); the error end is the upper cap (rows with a
run >= 24 px of line colour). The y axis is calibrated from its four tick marks.
"""
import numpy as np

from livinglit.figures.source import blobs, calibrate, point

DPI = 300
UNC_PX = 0.6
AXIS_COL = 108
TICK_VALUES = [150000, 100000, 50000, 0]  # top to bottom
ROWS = (90, 356)  # below the significance bracket (row ~72), above the x axis (row ~360)
# label: (column window px, line/marker colour threshold, bar fill grey)
GROUPS = {
    "rpmi": ((140, 236), 160, 192),
    "mm": ((242, 334), 70, 131),
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
    flags = [g[r, AXIS_COL - 14:AXIS_COL - 1].__lt__(110).sum() >= 6 for r in range(g.shape[0])]
    return [(a + b) / 2 for a, b in _runs(flags)]


def _markers(m):
    """Circle centres (col, row, half-interval px) in a window mask with the lines opened away."""
    import cv2
    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    opened = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, disc)
    out = []
    for b in blobs(opened, min_area=30, max_area=250):
        cx, cy = b["x"], b["y"]
        mids = []
        for c in (int(round(cx)) - 4, int(round(cx)) + 4):
            r = int(round(cy))
            if not m[r, c]:
                raise ValueError(f"circle chord missing at column {c}, row {r}")
            a, z = r, r
            while m[a - 1, c]:
                a -= 1
            while m[z + 1, c]:
                z += 1
            if z - a + 1 > 14:
                raise ValueError(f"chord at column {c} longer than a circle ({z - a + 1} px)")
            mids.append((a + z) / 2)
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


def _bar_top(g, x0, x1, fill):
    """Fill edge (row, half-crossing between white and fill) in bar columns with white just above it."""
    tops = []
    for c in range(x0, x1):
        col = g[:, c]
        for r in range(ROWS[0] + 3, ROWS[1]):
            if abs(col[r] - fill) <= 6 and abs(col[r + 1] - fill) <= 6 and abs(col[r + 2] - fill) <= 6:
                if (col[r - 3:r - 1] > 240).all():
                    half = (255 + fill) / 2
                    # interpolate the crossing between row r-1 and r
                    v0, v1 = col[r - 1], col[r]
                    frac = 0.0 if v0 == v1 else (v0 - half) / (v0 - v1)
                    tops.append(r - 1 + min(max(frac, 0.0), 1.0))
                break
    if len(tops) < 10:
        raise ValueError(f"bar top found in only {len(tops)} columns of {x0}-{x1}")
    return float(np.median(tops)), (max(tops) - min(tops)) / 2


def read(fig):
    img, scale = fig.render(DPI)
    g = img.astype(float).mean(axis=2)
    ticks = _ticks(g)
    if len(ticks) != len(TICK_VALUES):
        raise ValueError(f"expected {len(TICK_VALUES)} y ticks, found {ticks}")
    cal = calibrate(list(zip(ticks, TICK_VALUES)))
    res = cal.residual
    out = {}
    for label, ((x0, x1), thr, fill) in GROUPS.items():
        win = np.zeros_like(g, dtype=bool)
        win[ROWS[0]:ROWS[1], x0:x1] = True
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
        # bar columns: fill-coloured columns on a row inside the bar below every marker
        bar_cols = [c for c in range(x0, x1) if abs(g[350, c] - fill) <= 6]
        top, th = _bar_top(g, bar_cols[0] + 2, bar_cols[-1] - 1, fill)
        pm = point(cal, top, UNC_PX + th, fig.to_page(ucx, top, scale))
        pu = point(cal, up, UNC_PX + uh, fig.to_page(ucx, up, scale))
        out[label] = {
            "points": pts,
            "countable": True,
            "bar": {"mean": [pm["value"], pm["lo"] - res, pm["hi"] + res],
                    "error": [pu["value"], pu["lo"] - res, pu["hi"] + res]},
        }
    return {"groups": out}
