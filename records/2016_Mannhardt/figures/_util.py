"""Helpers for reading 2016_Mannhardt's raster panels (this paper's alone).

Every figure in this paper is one embedded image per page (main article at 300 dpi,
supplement at 220 dpi). A script crops one panel (or one row of panels), these
helpers find the axis line and its tick marks in the render, calibrate against the
tick values printed on the labels (passed in by the script), and locate red mean
lines, bar tops, error-bar caps and black markers. Intervals: 0.6 px at the
image's own resolution plus the calibration misfit.
"""
from __future__ import annotations

import numpy as np

from livinglit.figures.source import blobs, calibrate

UNC_PX = 0.6


def render(fig, dpi):
    img, scale = fig.render(dpi)
    return img.astype(int), scale


def gray(img):
    return img.mean(axis=2)


def dark(img, thr=110):
    """Dark, unsaturated pixels (black ink)."""
    g = gray(img)
    sat = img.max(axis=2) - img.min(axis=2)
    return (g < thr) & (sat < 60)


def red(img):
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    return (r > 150) & (r - g > 45) & (r - b > 45)


def runs(v):
    """Runs of True in a 1-D boolean array: list of (start, end_inclusive)."""
    out, s = [], None
    for i, x in enumerate(v):
        if x and s is None:
            s = i
        elif not x and s is not None:
            out.append((s, i - 1))
            s = None
    if s is not None:
        out.append((s, len(v) - 1))
    return out


def y_ticks(img, ax, min_len=2, thr=110, side="left", min_ink=0.35):
    """Tick marks sticking out of the y-axis line, top to bottom: (row centre px, length px).
    Antialiased ticks spread over 2-3 rows, so the centre is the ink-weighted mean row of the
    min_len columns next to the axis; a tick needs ink in each of them."""
    g = gray(img)
    x0, x1, top, bot = ax
    cols = list(range(x0 - min_len, x0)) if side == "left" else list(range(x1 + 1, x1 + 1 + min_len))
    ink = np.clip(255 - g[:, cols], 0, 255) / 255.0  # rows x cols
    y_a, y_b = max(top - 3, 0), min(bot + 4, g.shape[0])
    axis_ink = float(np.clip(255 - g[top:bot + 1, x0:x1 + 1], 0, 255).max(axis=1).mean() / 255.0)
    k = min(1.0, axis_ink / 0.7)  # light-grey axes have light ticks
    on = (ink.min(axis=1) >= min_ink * 0.5 * k) & (ink.mean(axis=1) >= min_ink * 0.6 * k)
    out = []
    for a, b in runs(on[y_a:y_b]):
        a += y_a
        b += y_a
        if b - a > 5:  # not a tick: a label or a bar touching the axis
            continue
        lo, hi = max(a - 1, 0), min(b + 1, g.shape[0] - 1)
        w = ink[lo:hi + 1].mean(axis=1)
        rows = np.arange(lo, hi + 1)
        # length: dark run outward from the axis on the darkest row
        yr = int(rows[np.argmax(w)])
        n = 0
        x = x0 - 1 if side == "left" else x1 + 1
        while 0 <= x < g.shape[1] and g[yr, x] < 200:
            n += 1
            x += -1 if side == "left" else 1
        out.append((float((rows * w).sum() / w.sum()), n))
    return out


def cal_from(ticks_px, values, log=False):
    """Calibration from tick rows (top to bottom) and the printed values (top to bottom)."""
    if len(ticks_px) != len(values):
        raise ValueError(f"{len(ticks_px)} ticks found for {len(values)} printed values: {ticks_px}")
    return calibrate(list(zip(ticks_px, values)), log=log)


def reading(cal, pos_px, unc_px, fig, scale, at_px, x=None):
    """A point (value, interval, page position) from a row in px; widened by the calibration misfit."""
    v = cal.value(pos_px)
    a, b = cal.value(pos_px - unc_px), cal.value(pos_px + unc_px)
    lo, hi = min(a, b, v), max(a, b, v)
    if cal.residual:
        if cal.log:
            lo, hi = lo / 10 ** cal.residual, hi * 10 ** cal.residual
        else:
            lo, hi = lo - cal.residual, hi + cal.residual
    px, py = fig.to_page(at_px[0], at_px[1], scale)
    d = {"value": float(v), "lo": float(lo), "hi": float(hi), "at": [float(px), float(py)]}
    if x is not None:
        d["x"] = x
    return d


def triple(p):
    return [p["value"], p["lo"], p["hi"]]


def markers(img, x_from, x_to, y_from, y_to, thr=110, min_area=2):
    """Black marker blobs inside a plot box (px)."""
    d = dark(img, thr)
    sub = np.zeros_like(d)
    sub[y_from:y_to, x_from:x_to] = d[y_from:y_to, x_from:x_to]
    return blobs(sub, min_area=min_area)


def axes(img, min_frac=0.45, thr=150):
    """All y-axis lines in a render, left to right: (left col, right col, top row, bottom row).
    A y-axis is a column run whose longest dark vertical run is at least min_frac of the height
    and which has tick marks on its left."""
    d = dark(img, thr)
    H = d.shape[0]
    best = np.array([max((b - a + 1 for a, b in runs(d[:, x])), default=0) for x in range(d.shape[1])])
    out = []
    g = gray(img)
    for a, b in runs(best >= min_frac * H):
        # drop faint antialiased edge columns of the axis line
        means = [float(np.sort(g[:, x])[: int(min_frac * H)].mean()) for x in range(a, b + 1)]
        keep = [x for x, m in zip(range(a, b + 1), means) if m <= min(means) + 60]
        a, b = keep[0], keep[-1]
        col = d[:, a:b + 1].any(axis=1)
        rr = max(runs(col), key=lambda r: r[1] - r[0])
        ax = (a, b, rr[0], rr[1])
        if len(y_ticks(img, ax, min_len=2, thr=thr)) >= 3:
            out.append(ax)
    if out:  # bar edges are shorter than the axis lines
        m = max(o[3] - o[2] for o in out)
        out = [o for o in out if o[3] - o[2] >= 0.9 * m]
    return out


def scatter_row(fig, dpi, specs, min_frac=0.45, thr=150):
    """A row of scatter-with-mean panels. specs: one per y-axis, left to right:
    (prefix, printed tick values top to bottom, group labels left to right, exact n or None[, options])."""
    img, scale = render(fig, dpi)
    found = axes(img, min_frac, thr)
    if len(found) != len(specs):
        raise ValueError(f"{len(found)} y-axes found for {len(specs)} panels: {found}")
    groups = {}
    for i, (ax, spec) in enumerate(zip(found, specs)):
        prefix, values, labels, n = spec[:4]
        opt = spec[4] if len(spec) > 4 else {}
        right = found[i + 1][0] - opt.get("right_margin", 28) if i + 1 < len(found) else img.shape[1]
        ticks = [t for t, ln in y_ticks(img, ax, min_len=opt.get("tick_len", 2), thr=thr)]
        if "tick_select" in opt:
            ticks = [ticks[j] for j in opt["tick_select"]]
        try:
            g = scatter_panel2(fig, img, scale, ax, right, ticks, values, labels, log=opt.get("log", False),
                               n_exact=n, thr=thr)
        except ValueError as e:
            raise ValueError(f"panel {prefix}: {e}") from None
        for k, v in g.items():
            groups[f"{prefix}|{k}"] = v
    return {"groups": groups}


def x_axis_row(img, ax, x_to, thr=150):
    """The x-axis row near the bottom of a y-axis: the row with the longest dark extent to the right of it."""
    d = dark(img, thr)
    best, row = -1, ax[3]
    for y in range(max(ax[3] - 3, 0), min(ax[3] + 3, d.shape[0])):
        n = int(d[y, ax[1] + 1:x_to].sum())
        if n > best:
            best, row = n, y
    return row


def group_ticks(img, ax, x_to, min_len=2, thr=150, min_ink=0.3):
    """Columns (px) of the tick marks hanging below the x-axis line: one per plotted group."""
    g = gray(img)
    row = x_axis_row(img, ax, x_to, thr)
    # the axis line may be 2-3 px thick (antialiased): start below its last inked row
    r0 = row + 1
    while r0 < g.shape[0] and (255 - g[r0, ax[1] + 3:x_to]).mean() / 255 > 0.25:
        r0 += 1
    rows = list(range(r0, min(r0 + min_len, g.shape[0])))
    if len(rows) < min_len:
        raise ValueError("crop too short for the x-axis tick marks")
    ink = np.clip(255 - g[rows, :], 0, 255) / 255.0
    axis_ink = float(np.clip(255 - g[ax[2]:ax[3] + 1, ax[0]:ax[1] + 1], 0, 255).max(axis=1).mean() / 255.0)
    on = ink.min(axis=0) >= min_ink * min(1.0, axis_ink / 0.7)
    out = []
    for a, b in runs(on):
        if a <= ax[1] + 1 or b >= min(x_to, g.shape[1]) - 2:
            continue
        if b - a > 4:
            continue
        lo, hi = max(a - 1, 0), min(b + 1, g.shape[1] - 1)
        w = ink[:, lo:hi + 1].mean(axis=0)
        cols = np.arange(lo, hi + 1)
        out.append(float((cols * w).sum() / w.sum()))
    return out, row


def red_mean_at(img, cx, half, y_from, y_to):
    """The red mean line of one group: red pieces within cx ± half, clustered by row; the cluster with the
    widest total extent; its row is the r-g weighted mean row. Returns (x_centre, row, width) or None."""
    m = red(img)
    x0, x1 = int(round(cx - half)), int(round(cx + half)) + 1
    sub = np.zeros_like(m)
    sub[y_from:y_to, x0:x1] = m[y_from:y_to, x0:x1]
    comps = [c for c in blobs(sub, min_area=1) if c["box"][3] <= 6]
    if not comps:
        return None
    comps.sort(key=lambda c: c["y"])
    clusters = []
    for c in comps:
        if clusters and abs(c["y"] - clusters[-1][-1]["y"]) <= 2:
            clusters[-1].append(c)
        else:
            clusters.append([c])
    best = max(clusters, key=lambda cl: sum(c["box"][2] for c in cl))
    xa = min(c["box"][0] for c in best)
    xb = max(c["box"][0] + c["box"][2] - 1 for c in best)
    width = xb - xa + 1 if sum(c["area"] for c in best) >= 3 else 0  # extent: markers drawn over a line split it
    ya = max(min(c["box"][1] for c in best) - 1, 0)
    yb = min(max(c["box"][1] + c["box"][3] - 1 for c in best) + 1, m.shape[0] - 1)
    rg = np.clip(img[ya:yb + 1, xa:xb + 1, 0] - img[ya:yb + 1, xa:xb + 1, 1], 0, 255)
    rg = np.where(m[ya:yb + 1, xa:xb + 1] | (rg > 20), rg, 0)
    w = rg.sum(axis=1).astype(float)
    rows = np.arange(ya, yb + 1)
    return ((xa + xb) / 2.0, float((rows * w).sum() / w.sum()), width)


def scatter_panel2(fig, img, scale, ax, x_to, ticks, values, labels, log=False, n_exact=None, unc=UNC_PX,
                   thr=150, min_line=0.35):
    """One scatter-with-mean panel, groups placed by the x-axis tick marks (left to right = labels).
    The mean is the group's red line. Points only when every marker of the group stands alone and their
    number equals the printed n (n_exact); otherwise the mean only, countable False."""
    cal = cal_from(ticks, values, log)
    gx, row = group_ticks(img, ax, x_to, thr=thr)
    if 1 < len(gx) < len(labels):
        gx = fill_grid(gx, len(labels))
    if len(gx) != len(labels):
        raise ValueError(f"{len(gx)} x tick marks for {len(labels)} groups: {[round(x) for x in gx]}")
    pitch = float(np.median(np.diff(gx))) if len(gx) > 1 else 20.0
    half = 0.45 * pitch
    bl = markers(img, ax[1] + 2, x_to, 0, row - 1)
    areas = sorted(b["area"] for b in bl)
    single = float(np.median(areas)) if areas else 0
    out = {}
    for lab, cx in zip(labels, gx):
        ln = red_mean_at(img, cx, half, 0, row + 2)
        if ln is None or ln[2] < min_line * pitch:
            raise ValueError(f"no red mean line for group {lab} at x={cx:.0f}")
        g = {"points": [], "countable": False,
             "bar": {"mean": triple(reading(cal, ln[1], unc, fig, scale, (ln[0], ln[1])))}}
        mine = [b for b in bl if abs(b["x"] - cx) < half]
        alone = all(b["area"] <= 1.6 * single and max(b["box"][2], b["box"][3]) <= 2.2 * min(b["box"][2], b["box"][3]) + 1
                    for b in mine)
        if n_exact is not None and alone and len(mine) == n_exact:
            g["points"] = [reading(cal, b["y"], unc, fig, scale, (b["x"], b["y"])) for b in mine]
            g["countable"] = True
        out[lab] = g
    return out


def fill_grid(xs, n, tol=2.0):
    """Tick marks are evenly spaced; when a marker drawn over the axis hides some, place the hidden ones on
    the grid of the found ones (used only to place group windows, never as a value). Returns xs unchanged
    if the found ticks do not sit on one grid of n positions."""
    xs = sorted(xs)
    d = np.diff(xs)
    pitch = float(min(d))
    if any(abs(x / pitch - round(x / pitch)) * pitch > tol for x in d):
        return xs
    k = [int(round((x - xs[0]) / pitch)) for x in xs]
    if k[-1] + 1 != n:
        return xs
    full = [xs[0] + j * pitch for j in range(n)]
    for j, x in zip(k, xs):
        full[j] = x
    return full


def first_run(col):
    rr = runs(col)
    return rr[0] if rr else None


def bar_row(fig, dpi, specs, min_frac=0.45, thr=150, ink_thr=110):
    """A row of bar charts (bars standing on the x-axis, black outlines, error bars above).
    specs: one per y-axis, left to right: (prefix, printed tick values top to bottom, bar labels left to
    right[, options]). Mean = centre of the bar's top outline; error = centre of the cap stroke."""
    img, scale = render(fig, dpi)
    found = axes(img, min_frac, thr)
    if len(found) != len(specs):
        raise ValueError(f"{len(found)} y-axes found for {len(specs)} panels: {found}")
    groups = {}
    for i, (ax, spec) in enumerate(zip(found, specs)):
        prefix, values, labels = spec[:3]
        opt = spec[3] if len(spec) > 3 else {}
        right = found[i + 1][0] - opt.get("right_margin", int(0.25 * dpi)) if i + 1 < len(found) else img.shape[1]
        ticks = [t for t, ln in y_ticks(img, ax)]
        try:
            cal = cal_from(ticks, opt.get("values", values), opt.get("log", False))
            res = bars_in(fig, img, scale, ax, right, cal, labels, ink_thr=ink_thr, opt=opt)
        except ValueError as e:
            raise ValueError(f"panel {prefix}: {e}") from None
        for k, v in res.items():
            groups[f"{prefix}|{k}"] = v
    return {"groups": groups}


def bars_in(fig, img, scale, ax, right, cal, labels, ink_thr=110, opt=None):
    opt = opt or {}
    g = gray(img)
    d = dark(img, ink_thr)
    row = x_axis_row(img, ax, right)
    # axis stroke thickness: dark rows around the x-axis row on a column right of the y-axis
    xa = ax[1] + 3
    t_ax = max(1, len([y for y in range(row - 4, row + 5) if 0 <= y < g.shape[0] and g[y, xa] < 160]))
    # bars: columns with ink just above the axis (over several rows, so hatching counts)
    at = row
    line = np.where(g[row, ax[1] + 3:right] < 160)[0] + ax[1] + 3  # columns of the x-axis line
    while at - 1 > 0 and (g[at - 1, line] < 160).mean() > 0.9:
        at -= 1
    band = (g[at - opt.get("band", 12):at - 1, :] < 235).any(axis=0)
    band[: ax[1] + 3] = False
    band[right:] = False
    bars = [(a, b) for a, b in runs(band) if b - a + 1 >= opt.get("min_w", 8)]
    if len(bars) != len(labels):
        raise ValueError(f"{len(bars)} bars for {len(labels)} labels: {bars}")
    out = {}
    top_lim = opt.get("top", 0)
    for lab, (xl, xr) in zip(labels, bars):
        w = xr - xl + 1
        xe = int(round(xl + max(0.1 * w, t_ax + 2)))
        fr = first_run(d[top_lim:at - 1, xe])
        if fr is None:
            raise ValueError(f"no bar top for {lab}")
        a, b = fr[0] + top_lim, fr[1] + top_lim
        top = (a + b) / 2.0 if b - a + 1 <= 8 else a + (t_ax - 1) / 2.0
        res = {"points": [], "countable": False,
               "bar": {"mean": triple(reading(cal, top, UNC_PX, fig, scale, ((xl + xr) / 2, top)))}}
        xc = (xl + xr) / 2.0
        off = max(2, int(round(0.12 * w)))
        caps = []
        for x in (int(round(xc - off)), int(round(xc + off))):
            cr = first_run(d[top_lim:at - 1, x])
            if cr is not None and cr[0] + top_lim < a - 1 and cr[1] - cr[0] + 1 <= 8:
                caps.append((cr[0] + cr[1]) / 2.0 + top_lim)
        if len(caps) == 2 and abs(caps[0] - caps[1]) <= 1.5:
            cap = sum(caps) / 2
            res["bar"]["error"] = triple(reading(cal, cap, UNC_PX, fig, scale, (xc, cap)))
        out[lab] = res
    return out


def expand(res, links):
    """Relabel what a panel reads for each evidence item that rests on it: links maps the label in
    figures.yaml ('<item>|<group>') to the panel's own label ('<panel>|<group>')."""
    g = res["groups"]
    missing = sorted({b for b in links.values() if b not in g})
    if missing:
        raise ValueError(f"panel labels not read: {missing}")
    return {"groups": {new: g[base] for new, base in links.items()}}


def opened(mask, k):
    """Morphological opening with a k x k ellipse: removes lines and text strokes thinner than k px,
    keeps filled markers."""
    import cv2
    ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
    return cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_OPEN, ker).astype(bool)


def x_axis_ticks(img, row_bottom, x_from, x_to, max_len=30, min_ink=0.35):
    """Tick marks hanging below an x-axis line whose last row is row_bottom: (column centre, length)."""
    g = gray(img)
    out = []
    ink1 = np.clip(255 - g[row_bottom + 1, :], 0, 255) / 255.0
    for a, b in runs(ink1 >= min_ink):
        if a < x_from or b > x_to or b - a > 5:
            continue
        lo, hi = max(a - 1, 0), min(b + 1, g.shape[1] - 1)
        w = ink1[lo:hi + 1]
        cols = np.arange(lo, hi + 1)
        c = float((cols * w).sum() / w.sum())
        n = 0
        y = row_bottom + 1
        xi = int(round(c))
        while y < g.shape[0] and n < max_len and g[y, max(xi - 1, 0):xi + 2].min() < 200:
            n += 1
            y += 1
        out.append((c, n))
    return out


def x_axis_bottom(img, ax, x_to, thr=150):
    """Last dark row of the x-axis line."""
    g = gray(img)
    row = x_axis_row(img, ax, x_to, thr)
    line = np.where(g[row, ax[1] + 3:x_to] < 160)[0] + ax[1] + 3
    b = row
    while b + 1 < g.shape[0] and (g[b + 1, line] < 160).mean() > 0.9:
        b += 1
    return b, line


