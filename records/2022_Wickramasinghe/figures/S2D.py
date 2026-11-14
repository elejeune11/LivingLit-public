"""Fig. S2D (supplement p. 6): EdU+ cells (%) in cTnT+ hPSC-CMs, ten bars (mean + SD, n = 4) with one marker per
replicate. Only the first bar (Control) and the last (iPSC Control) are read: the unit's items need no other bar. The
page is one image (about 312 dpi). The y axis is broken: a lower segment with ticks 0, 2, 4 and an upper segment with
ticks 80, 100; each segment is calibrated on its own ticks, and a row is read on the segment whose axis line holds it.

Markers are ellipses about 11 px wide and 8.5 px tall at 300 dpi: rings (dark outline, bar-coloured fill) on white and
on the light-grey Control bar, rings darker than the near-black fill inside the iPSC bar, and outlined discs filled with
the bar's dark colour above the iPSC bar (their top on the upper cap). Candidates are peaks of the normalised correlation
(image upsampled 4x) with a ring or a filled-ellipse template; a candidate is kept when its outline is darker than
2 px outside it on at least 6 of 8 arcs and it is either a ring (outline darker than its centre) or a filled disc
(centre dark against outside). Markers are countable when no two footprints overlap and no outline pixels are left in
the bar's columns once the markers, whisker, caps and bar outline are taken out.
"""
import numpy as np
import cv2
from scipy.ndimage import map_coordinates

from livinglit.figures.source import calibrate, point, RASTER_UNCERTAINTY_PX_300DPI

DPI = 300
UPPER_TICKS = [100, 80]          # printed tick labels on the upper axis segment, top to bottom
LOWER_TICKS = [4, 2, 0]          # and on the lower one
LABELS = {"S2D_ipsc/control": 0, "S2D_ipsc/ipsc": -1}   # bar index, left to right (legend order)
N_BARS = 10
A, B, LW, UP = 5.0, 4.0, 1.5, 4  # ellipse semi-axes at the outline's centre (x, y), line width (px), upsampling
MATCH_MIN = 0.35
ARCS_MIN = 6
RATIO = 0.8                      # outline below 0.8 x the grey level outside (or inside, for a ring)
RESIDUAL_MAX = 6
MARGIN = 10                      # columns beside a bar in which its markers may lie


def _runs(mask):
    out, st = [], None
    for i, b in enumerate(list(mask) + [False]):
        if b and st is None:
            st = i
        if not b and st is not None:
            out.append((st, i - 1))
            st = None
    return out


def _axis(g):
    """Axis column (longest dark column in the left quarter), its dark runs (the segments of the broken axis), and tick
    rows: darkness centroids of rows dark on at least 6 of the 8 columns left of the axis (the break marks are
    shorter)."""
    w = g.shape[1] // 4
    col = int((g[:, :w] < 150).sum(0).argmax())
    segs = [(a, b) for a, b in _runs(g[:, col] < 150) if b - a > 20]
    span = g[:, col - 8:col]
    ticks = []
    for a, b in _runs((span < 150).sum(1) >= 6):
        idx = np.arange(a - 1, b + 2)
        d = 255 - span[idx].mean(1)
        ticks.append(float((idx * d).sum() / d.sum()))
    return col, segs, ticks


def _template(filled):
    hx, hy = int(np.ceil((A + LW / 2 + 1) * UP)), int(np.ceil((B + LW / 2 + 1) * UP))
    yy, xx = np.mgrid[-hy:hy + 1, -hx:hx + 1] / UP
    r = np.hypot(xx / A, yy / B)
    m = r <= 1 + LW / 2 / B if filled else np.abs(r - 1) * B < LW / 2
    return np.where(m, 0.0, 1.0).astype(np.float32), hx, hy


def _sample(g, pts):
    pts = np.asarray(pts, float)
    return map_coordinates(g, [pts[:, 1], pts[:, 0]], order=1, mode="nearest")


def _is_marker(g, cx, cy):
    centre = float(np.median(_sample(g, [[cx + dx, cy + dy] for dx in (-1.1, 1.1) for dy in (-1.1, 1.1)])))
    ok, ons, outs = 0, [], []
    for c in np.pi / 8 * np.array([1, 3, 5, 7, 9, 11, 13, 15]):
        u = c + np.linspace(-0.2, 0.2, 3)
        e = np.c_[A * np.cos(u), B * np.sin(u)]
        on = min(float(np.median(_sample(g, np.c_[cx, cy] + f * e))) for f in (0.9, 1.0, 1.1))
        out = float(np.median(_sample(g, np.c_[cx, cy] + (1 + 2.0 / B) * e)))
        ok += on < RATIO * out
        ons.append(on)
        outs.append(out)
    ring = float(np.median(ons)) < RATIO * centre
    disc = centre < 0.5 * float(np.median(outs))
    return ok >= ARCS_MIN and (ring or disc)


def _markers(g, x0, x1, y0, y1):
    """Markers (x, y) whose centres lie in columns x0..x1 and rows y0..y1: peaks of either template, best first."""
    gu = cv2.resize(g, None, fx=UP, fy=UP, interpolation=cv2.INTER_CUBIC)
    lo_x, lo_y = max(0, int(x0 - 10)), max(0, int(y0 - 10))
    sub = gu[lo_y * UP:int(y1 + 10) * UP, lo_x * UP:int(x1 + 10) * UP]
    cands = []
    for filled in (False, True):
        t, hx, hy = _template(filled)
        best = cv2.matchTemplate(sub, t, cv2.TM_CCOEFF_NORMED)
        ys, xs = np.where(best >= MATCH_MIN)
        for y, x in zip(ys, xs):
            cands.append((float(best[y, x]), (x + hx + 0.5) / UP - 0.5 + lo_x, (y + hy + 0.5) / UP - 0.5 + lo_y))
    cands.sort(reverse=True)
    out = []
    for s, cx, cy in cands:
        if not (x0 <= cx <= x1 and y0 <= cy <= y1):
            continue
        if any(abs(cx - px) < A and abs(cy - py) < B for px, py in out):
            continue
        if _is_marker(g, cx, cy):
            out.append((cx, cy))
    return out


def _foot(xx, yy, cx, cy, grow=0.0):
    return np.hypot((xx - cx) / (A + LW / 2 + grow), (yy - cy) / (B + LW / 2 + grow)) <= 1


def read(fig):
    img, scale = fig.render(DPI)
    g = img.astype(np.float32).mean(2)
    col, segs, ticks = _axis(g)
    if len(segs) != 2:
        raise ValueError(f"{len(segs)} axis segments found, 2 expected")
    cals = []
    for (a, b), vals in zip(segs, [UPPER_TICKS, LOWER_TICKS]):
        mine = [t for t in ticks if a - 1 <= t <= b + 1]
        if len(mine) != len(vals):
            raise ValueError(f"segment {a}-{b}: {len(mine)} ticks found, {len(vals)} labels")
        cal = calibrate(list(zip(mine, vals)))
        cals.append((a, b, cal, RASTER_UNCERTAINTY_PX_300DPI + cal.residual / abs(cal.slope)))

    def on_axis(row):
        for a, b, cal, unc in cals:
            if a - 1 <= row <= b + 1:
                return cal, unc
        raise ValueError(f"row {row:.1f} lies in the axis break")

    base = segs[1][1]
    spans = [(a + col + 3, b + col + 3) for a, b in _runs(g[base - 2, col + 3:] < 235) if b - a >= 20]
    if len(spans) != N_BARS:
        raise ValueError(f"{len(spans)} bars found, {N_BARS} expected")

    yy, xx = np.mgrid[:g.shape[0], :g.shape[1]]
    res = {}
    for label, i in LABELS.items():
        x0, x1 = spans[i]
        mid = (x0 + x1) // 2
        inner = list(range(x0 + 3, x1 - 2))
        fill = float(np.median(g[base - 12:base - 4, inner]))
        if (i == 0) != (fill > 160):
            raise ValueError(f"bar {label}: fill {fill:.0f} is not {'light' if i == 0 else 'dark'} grey")
        found = _markers(g, x0 - MARGIN, x1 + MARGIN, segs[0][0] - 2, base - 3)
        disc = np.zeros(g.shape, bool)
        for cx, cy in found:
            disc |= _foot(xx, yy, cx, cy, 1.0)

        # bar top: the highest row from which every row down to the baseline is non-white across 90% of the interior
        # away from the whisker; the outline row is the darkness centroid of the darkest row there, off the markers
        solid = (g[:, [x for x in inner if abs(x - mid) > 3]] < 235).mean(1) >= 0.9
        top = base - 2
        while top > 0 and solid[top - 1]:
            top -= 1
        cols = [x for x in inner if abs(x - mid) > 3 and not disc[top - 2:top + 4, x].any()]
        idx = np.arange(top - 1, top + 4)
        prof = g[idx][:, cols].mean(1)
        k = int(prof.argmin())
        wgt = np.clip(fill - prof, 0, None)
        wgt[np.abs(np.arange(len(idx)) - k) > 1] = 0
        bar_row = float((idx * wgt).sum() / wgt.sum())
        cal, unc = on_axis(bar_row)
        bar = {"mean": [cal.value(bar_row), *cal.interval(bar_row, unc)]}

        # whisker: the darkest column near the bar centre between the bar top and the upper axis end, off markers;
        # upper cap: the highest row of the run of dark whisker rows rising from the bar top, as a darkness centroid
        win = np.where(disc[segs[0][0]:top - 2, mid - 6:mid + 7], np.nan, g[segs[0][0]:top - 2, mid - 6:mid + 7])
        xc = mid - 6 + int(np.nanargmin(np.nanmean(win, 0)))
        r = top - 2
        while r > segs[0][0] and g[r - 1, xc] < 200:
            r -= 1
        cap_idx = np.arange(r - 1, r + 2)
        # (the cap reaches about 18 px either side of the whisker; the columns used are those off the markers' own
        # footprints, which on the iPSC bar leave only its two ends)
        own = np.zeros(g.shape, bool)
        for cx, cy in found:
            own |= _foot(xx, yy, cx, cy)
        cap_cols = [x for x in range(xc - 18, xc + 19) if abs(x - xc) > 1 and not own[r - 1:r + 2, x].any()]
        d = np.clip(255 - g[cap_idx][:, cap_cols].mean(1), 0, None)
        cap_row = float((cap_idx * d).sum() / d.sum())
        cal_c, unc_c = on_axis(cap_row)
        bar["error"] = [cal_c.value(cap_row), *cal_c.interval(cap_row, unc_c)]

        # countable: footprints apart, and no outline pixels left in the bar's columns (dark on white, or darker than
        # the fill inside the bar) once markers, whisker, horizontal lines (caps, bar top, baseline) and the bar's
        # side edges are taken out
        apart = all(np.hypot((p[0] - q[0]) / (2 * A + LW), (p[1] - q[1]) / (2 * B + LW)) > 1
                    for j, p in enumerate(found) for q in found[j + 1:])
        ys = slice(segs[0][0], base - 3)
        xs = slice(x0 - MARGIN, x1 + MARGIN + 1)
        sub = g[ys, xs]
        inside = (xx[ys, xs] >= x0) & (xx[ys, xs] <= x1) & (yy[ys, xs] >= top)
        mark = np.where(inside, sub < fill - 15, sub < 120)
        mark &= ~disc[ys, xs]
        mark &= np.abs(xx[ys, xs] - xc - 0.5) > 2
        mark &= (np.abs(xx[ys, xs] - x0) > 2) & (np.abs(xx[ys, xs] - x1) > 2)
        mark &= ~((np.abs(yy[ys, xs] - cap_row) <= 1.5) & (np.abs(xx[ys, xs] - xc) <= 20))   # the upper cap
        rows_line = (mark.sum(1) >= 15)
        mark[rows_line | np.r_[rows_line[1:], False] | np.r_[False, rows_line[:-1]]] = False
        countable = apart and int(mark.sum()) <= RESIDUAL_MAX

        pts = []
        if countable:
            for cx, cy in sorted(found, key=lambda e: e[1]):
                c, u = on_axis(cy)
                pts.append(point(c, cy, u, fig.to_page(cx, cy, scale)))
        res[label] = {"points": pts, "countable": countable, "bar": bar}
    return {"groups": res}
