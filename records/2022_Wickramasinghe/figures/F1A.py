"""Fig. 1A (journal_version.pdf p. 4): RT-qPCR of PPARA, PPARD, PPARG; 26 bars per gene (days 0-42 of
differentiation, then LV, RV, Apex, LA, RA, AVJ, HH), mean ± SD with open-circle points. Raster (300 dpi).

Three stacked panels, each with its own y axis. Per panel: axis column and ticks found in the image (tick values
are the printed labels), bars on a regular grid fitted to the clean bar outlines at the baseline, bar mean at the
top outline, error at the cap, points by matching one marker ring cut from the figure itself (the LV bar of PPARA)
and refined to the ring's darkness centroid. A group's points are returned only when every marker stands alone
(well matched, coloured like a marker, no other marker or doubtful match within one marker width); otherwise the
bar only, countable false.
"""
import numpy as np
import cv2

from livinglit.figures.source import calibrate, point, RASTER_UNCERTAINTY_PX_300DPI

DPI = 300
DAYS = ["d0", "d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8", "d9", "d10", "d14", "d18", "d22", "d26", "d30",
        "d34", "d38", "d42"]
TISSUE = ["LV", "RV", "Apex", "LA", "RA", "AVJ", "HH"]
GROUPS = DAYS + TISSUE
# gene: (band top and bottom in page pt, printed tick labels top to bottom, tissue groups compared with day 0)
PANELS = {
    "PPARA": ((101.0, 169.0), [6, 4, 2, 0], ["LV", "RV", "Apex", "LA", "RA", "AVJ"]),
    "PPARD": ((169.0, 232.0), [8, 6, 4, 2, 0], ["LV", "LA", "AVJ"]),
    "PPARG": ((232.0, 293.0), [2.0, 1.5, 1.0, 0.5, 0], ["LV", "RV", "HH"]),
}
# the marker template: PPARA LV bar, two clean rings inside the bar (page pt of the 8x7 px patches' top-left)
TEMPLATE_AT = [(59 + 658 / 4.1667, 101 + 179 / 4.1667), (59 + 658 / 4.1667, 101 + 203 / 4.1667)]
GOOD, WEAK = 0.75, 0.6     # template scores: a lone marker, a possible (touching or hidden) marker
ALONE_PX = 6.0             # one marker width: closer centres overlap


def _runs(mask):
    out, st = [], None
    for i, b in enumerate(list(mask) + [False]):
        if b and st is None:
            st = i
        if not b and st is not None:
            out.append((st, i - 1))
            st = None
    return out


def _sat(px):
    return px.max(-1).astype(int) - px.min(-1).astype(int)


def _axis(g, y0, y1):
    """Axis column (longest dark column left of the bars) and tick centres (px rows)."""
    d = g[y0:y1, :140] < 160
    col = int(d.sum(0).argmax())
    ticks = []  # tick marks are thin and may be anti-aliased over two rows: a lighter threshold
    for a, b in _runs((g[y0:y1, col - 6:col - 1] < 200).sum(1) >= 3):
        w = 255 - g[y0 + a:y0 + b + 1, col - 6:col - 1].mean(1)
        ticks.append(y0 + a + float((np.arange(a, b + 1) * w).sum() / w.sum()) - a)
    return col, ticks


def _bars(g, base, col, n):
    """Bar centres and half width from clean bar spans at the baseline, fitted to a regular grid."""
    row = g[base - 3, col + 3:]
    spans = [(a + col + 3, b + col + 3) for a, b in _runs(row < 235) if 17 <= b - a + 1 <= 23]
    cs = np.array([(a + b) / 2 for a, b in spans])
    pitch = float(np.median(np.diff(cs)[np.diff(cs) < 30]))
    k = np.round((cs - cs[0]) / pitch)
    (p, c0), *_ = np.linalg.lstsq(np.vstack([k, np.ones_like(k)]).T, cs, rcond=None)
    # the first clean span may not be the first bar: the first bar starts just right of the axis
    first = int(np.floor((c0 - (col + 3)) / p))
    centres = [c0 + p * (i - first) for i in range(n)]
    hw = float(np.median([b - a for a, b in spans])) / 2
    return centres, hw


def _centroid(vals, idx):
    w = np.clip(vals, 0, None)
    return float((idx * w).sum() / w.sum()) if w.sum() > 0 else float(idx.mean())


def _fill(img, base, col):
    """The panel's bar fill: the median coloured pixel just above the baseline."""
    row = img[base - 3, col + 3:]
    return np.median(row[_sat(row) > 40], axis=0)


def _mean_and_error(img, g, xc, hw, base, top_px, fill):
    """Rows (px) of the bar's top outline (None when no fill shows: the outline is under markers) and of its
    error-bar cap (None when no cap shows)."""
    xl, xr = int(round(xc - hw)), int(round(xc + hw))
    cols = [x for x in range(xl + 2, xr - 1) if abs(x - xc) > 2.5]
    isfill = (np.abs(img.astype(int) - fill.astype(int)).max(-1) < 30)
    y = base - 1
    top_fill = None
    while y > top_px:
        if isfill[y, cols].mean() >= 0.3:
            top_fill = y
        elif top_fill is not None and y < top_fill - 6:
            break
        y -= 1
    if top_fill is None:  # a bar of one or two pixels whose top is covered by its markers
        return None, None
    # the top outline is anti-aliased into the fill (dark brown, not black): darker than the fill, and its
    # centre is the darkness centroid below the fill's grey (white above and fill below weigh nothing)
    fg = float(fill.mean())
    rows = [r for r in range(top_fill - 4, top_fill) if (g[r, cols] < fg - 25).mean() >= 0.5]
    if not rows:
        return None, None
    idx = np.arange(min(rows) - 1, max(rows) + 2)
    bar_row = _centroid(fg - g[idx][:, cols].mean(1), idx)
    # error bar: the dark line on the bar's centre going up from the top outline, ending at a cap
    cx = int(round(xc))
    y = int(np.floor(bar_row)) - 2
    line_top = None
    while y > top_px and g[y, cx - 1:cx + 2].min() < 170:
        line_top = y
        y -= 1
    cap = None
    if line_top is not None and bar_row - line_top >= 3:
        capcols = list(range(cx - 4, cx + 5))
        black = (g[:, capcols] < 170) & (_sat(img[:, capcols]) < 35)
        cand = [r for r in range(line_top, line_top + 4) if black[r].mean() >= 0.6]
        if cand:
            idx = np.arange(min(cand) - 1, max(cand) + 2)
            cap = _centroid(255 - g[idx][:, capcols].mean(1) - 80, idx)
    return bar_row, cap


def _unexplained_ink(ink, xc, hw, top_px, base, bar_row, good):
    """Marker ink in the bar's column that no lone matched ring accounts for: a touching or hidden marker.
    The bar's edges, its top outline and the baseline are masked, and so is everything within a marker radius
    of a matched ring."""
    xl, xr = int(round(xc - hw)), int(round(xc + hw))
    a, b = xl - 3, xr + 4
    yy, xx = np.mgrid[top_px:base - 1, a:b]
    m = ink[top_px:base - 1, a:b] & ~((np.abs(xx - xl) <= 2) | (np.abs(xx - xr) <= 2))
    if bar_row is not None:
        m &= ~(np.abs(yy - bar_row) <= 1.5)
    for f in good:
        m &= ~(np.hypot(yy - f["y"], xx - f["x"]) <= 4.0)
    n, _, stats, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), connectivity=8)
    return any(stats[i, cv2.CC_STAT_AREA] >= 3 for i in range(1, n))


def read(fig):
    img, scale = fig.render(DPI)
    g = img.astype(np.float32).mean(2)
    T = sum(g[int(round((ty - fig.crop[1]) * scale)):int(round((ty - fig.crop[1]) * scale)) + 8,
              int(round((tx - fig.crop[0]) * scale)):int(round((tx - fig.crop[0]) * scale)) + 7]
            for tx, ty in TEMPLATE_AT) / len(TEMPLATE_AT)
    R = cv2.matchTemplate(g, T, cv2.TM_CCOEFF_NORMED)
    peaks = (R == cv2.dilate(R, np.ones((4, 4), np.uint8))) & (R > WEAK)
    found = []
    for py, px in zip(*np.where(peaks)):
        cy, cx = py + T.shape[0] / 2, px + T.shape[1] / 2
        y0, x0 = int(cy) - 4, int(cx) - 4
        win = g[y0:y0 + 9, x0:x0 + 9]
        yy, xx = np.mgrid[y0:y0 + 9, x0:x0 + 9]
        # the ring's darkness centroid within one marker radius of the match (pixel index coordinates)
        w = np.clip(np.median(win) - win, 0, None) * (np.hypot(yy + 0.5 - cy, xx + 0.5 - cx) <= 3.5)
        ring = w > 20
        sat = float(_sat(img[y0:y0 + 9, x0:x0 + 9])[ring].mean()) if ring.any() else 0.0
        found.append({"x": float((xx * w).sum() / w.sum()), "y": float((yy * w).sum() / w.sum()),
                      "score": float(R[py, px]), "marker_colour": sat > 25})
    # marker ink: coloured pixels darker than the fill (rings; also bar edges and outlines, masked per bar)
    ink = (_sat(img) > 35) & (g < 150)
    out = {}
    for gene, ((t_pt, b_pt), tick_vals, compared) in PANELS.items():
        y0, y1 = int((t_pt - fig.crop[1]) * scale), int((b_pt - fig.crop[1]) * scale)
        col, ticks = _axis(g, y0, y1)
        if len(ticks) != len(tick_vals):
            raise ValueError(f"{gene}: {len(ticks)} ticks found, {len(tick_vals)} labels")
        cal = calibrate(list(zip(ticks, tick_vals)))
        unc = RASTER_UNCERTAINTY_PX_300DPI + cal.residual / abs(cal.slope)
        base = int(round(ticks[-1]))
        centres, hw = _bars(g, base, col, len(GROUPS))
        fill = _fill(img, base, col)
        res = {}
        for grp, xc in zip(GROUPS, centres):
            bar_row, cap = _mean_and_error(img, g, xc, hw, base, y0, fill)
            bar = {}
            for kind, row in (("mean", bar_row), ("error", cap)):
                if row is not None:
                    v = cal.value(row)
                    lo, hi = cal.interval(row, unc)
                    bar[kind] = [v, min(lo, v), max(hi, v)]
            mine = [f for f in found if abs(f["x"] - xc) <= hw + 3 and y0 < f["y"] < base + 2 and f["marker_colour"]]
            good = [f for f in mine if f["score"] >= GOOD]
            alone = len(good) == len(mine) and all(
                np.hypot(a["x"] - b["x"], a["y"] - b["y"]) >= ALONE_PX
                for i, a in enumerate(mine) for b in mine[i + 1:])
            alone = alone and not _unexplained_ink(ink, xc, hw, y0, base, bar_row, good)
            pts = [point(cal, f["y"], unc, fig.to_page(f["x"] + 0.5, f["y"] + 0.5, scale))
                   for f in sorted(good, key=lambda f: f["y"])] if alone and good else []
            res[grp] = {"points": pts, "countable": bool(alone and good), "bar": bar}
        for grp in GROUPS:
            out[f"F1A_{gene}/{grp}"] = res[grp]
        for t in compared:
            out[f"F1A_{gene}_{t}/{t}"] = res[t]
            out[f"F1A_{gene}_{t}/d0"] = res["d0"]
    return {"groups": out}
