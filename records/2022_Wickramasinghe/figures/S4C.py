"""Fig. S4C (NIHMS1982259-supplement-Supplement_text.pdf p. 9): % SIRPA+CD36+ cells in hPSC-CMs from two lines, five bars
(Control, LCFA, GW0742, LCFA + GW0742, GSK0660; mean + SD with upper and lower caps) with black markers, one per
biological replicate: circle = H9 (hESC), square = WTC11 (hiPSC), drawn open, filled or crossed (an open circle with an
X). Every bar shows one marker of each of the five kinds (open, filled and crossed circle; open and filled square), so
five markers per bar; the legend prints no n. Raster (the page is one 300 dpi image).

The y axis column and its tick marks are found in the image (tick values are the printed labels 80, 60, ..., 0); bars
are the five non-white spans just above the baseline, in legend order, checked by their fill colour. Markers are black, so
they are found on each pixel's brightest channel (in which the red, pink and blue fills are light): peaks of the
normalised correlation (image upsampled 4x) with five templates (outline width 1.4 px, outer size 16 px), each kept
only when a shape test (_kind: sides, arcs, corners, core and X darker than the samples beside them) names its kind
within 1.5 px of the peak; the marker is centred on the offsets that pass. A bar's markers are countable when
exactly one marker of each kind is found, no two markers' footprints share a pixel, and no dark outline pixels are left
in the marker band once the found markers, whisker, caps and bar outline are taken out. Otherwise the bar gives the bar
only.
"""
import numpy as np
import cv2
from scipy.ndimage import map_coordinates

from livinglit.figures.source import calibrate, point, RASTER_UNCERTAINTY_PX_300DPI

DPI = 300
TICK_VALUES = [80, 60, 40, 20, 0]  # printed tick labels, top to bottom
BARS = ["control", "lcfa", "gw", "lcfa_gw", "gsk"]   # legend order, left to right
FILL = ["grey", "grey", "red", "red", "blue"]       # checked against each bar's fill
LABELS = {
    "S4C_cd36/control": "control", "S4C_cd36/lcfa": "lcfa", "S4C_cd36/gw": "gw",
    "S4C_cd36/lcfa_gw": "lcfa_gw", "S4C_cd36/gsk": "gsk",
    "S4C_cd36_gw/gw": "gw", "S4C_cd36_gw/control": "control",
    "S4C_cd36_lcfa_gw/lcfa_gw": "lcfa_gw", "S4C_cd36_lcfa_gw/control": "control",
}
KINDS = ["open_circle", "filled_circle", "crossed_circle", "open_square", "filled_square"]
R, LW, UP = 7.3, 1.4, 4            # half outer size minus half line width (px at 300 dpi), line width, upsampling
HALF = R + LW / 2                  # half the outer size (8 px)
MATCH_MIN = 0.35
SEARCH = np.arange(-1.5, 1.51, 0.5)  # offsets (px) from a template peak tried by the shape test
DARK_MIN = 50                     # grey levels below the local background for a dark part
RESIDUAL_MAX = 20                  # outline pixels allowed outside found markers
CAP_MIN_COLS = 6


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
    """Axis column (longest dark column in the left quarter) and tick-mark rows (darkness centroids)."""
    w = g.shape[1] // 4
    col = int((g[:, :w] < 200).sum(0).argmax())
    span = g[:, col - 6:col - 1]
    ticks = []
    for a, b in _runs((span < 200).sum(1) >= 4):
        idx = np.arange(a - 1, b + 2)
        d = 255 - span[idx].mean(1)
        ticks.append(float((idx * d).sum() / d.sum()))
    return col, ticks


def _template(kind):
    """Dark (0) shape on light (1), in upsampled pixels, with the shape's centre at the template centre."""
    h = int(np.ceil((HALF + 2) * UP))
    yy, xx = np.mgrid[-h:h + 1, -h:h + 1] / UP
    if kind.endswith("circle"):
        d = np.hypot(xx, yy)
        ring = np.abs(d - R) < LW / 2
        disc = d < HALF
    else:
        d = np.maximum(np.abs(xx), np.abs(yy))
        ring = np.abs(d - R) < LW / 2
        disc = d < HALF
    dark = disc if kind.startswith("filled") else ring
    if kind == "crossed_circle":
        dark = dark | ((np.minimum(np.abs(xx - yy), np.abs(xx + yy)) / np.sqrt(2) < LW / 2) & (np.hypot(xx, yy) < R))
    return np.where(dark, 0.0, 1.0).astype(np.float32), h


def _sample(g, cx, cy, pts):
    """Grey values at (dx, dy) offsets from (cx, cy), bilinear."""
    pts = np.asarray(pts, float)
    return map_coordinates(g, [cy + pts[:, 1], cx + pts[:, 0]], order=1, mode="nearest")


def _kind(g, cx, cy):
    """The marker kind drawn at (cx, cy), or None. Each part of a shape must be darker (by DARK_MIN, as medians, so a
    whisker or cap crossing a few samples does not decide it) than the samples 2.5 px outside it, and an outline also
    than the samples 2.5 px inside it; so a bar's fill or corner, lighter than black, is never a marker."""
    def med(pts):
        return float(np.median(_sample(g, cx, cy, pts)))

    def line(path, normal, filled):
        if filled:   # a solid shape's edge: its rim 1.5 px inside the outline's centre against 2.5 px outside
            return med(path - 1.5 * normal) < med(path + 2.5 * normal) - DARK_MIN
        v = med(path)
        return v < med(path + 2.5 * normal) - DARK_MIN and v < med(path - 2.5 * normal) - DARK_MIN

    t = np.linspace(-R + 1.5, R - 1.5, 9)
    sides = []
    for s in (-1, 1):
        sides.append((np.c_[np.full_like(t, s * R), t], np.array([s, 0.0])))
        sides.append((np.c_[t, np.full_like(t, s * R)], np.array([0.0, s])))
    arcs = []   # eight arcs between the axes (whisker, caps) and the diagonals (a crossed circle's X)
    for c in np.pi / 8 * np.array([1, 3, 5, 7, 9, 11, 13, 15]):
        u = c + np.linspace(-0.25, 0.25, 5)
        n = np.c_[np.cos(u), np.sin(u)]
        arcs.append((R * n, n))
    a = np.linspace(0, 2 * np.pi, 32, endpoint=False)
    around = med(np.c_[(HALF + 2.5) * np.cos(a), (HALF + 2.5) * np.sin(a)])
    # core off the diagonals and axes (whisker, caps): dark for filled shapes
    off = np.array([[4.5 * np.cos(c), 4.5 * np.sin(c)] for c in np.pi / 8 * np.array([1, 3, 5, 7, 9, 11, 13, 15])])
    filled = med(off) < around - DARK_MIN
    if filled:   # a solid disc has no gaps (an asterisk has): its ring at 0.7 R dark all round
        ring = _sample(g, cx, cy, np.c_[0.7 * R * np.cos(a), 0.7 * R * np.sin(a)])
        if (ring >= around - DARK_MIN).sum() > 1:
            return None
    # corners: dark for a square (inside a solid one, on an outline's corner), outside a circle
    c = 6.0 if filled else R
    corners = [med(np.array([[s * c, u * c], [s * c, u * (c - 1)], [s * (c - 1), u * c]])) < around - DARK_MIN
               for s in (-1, 1) for u in (-1, 1)]
    square = sum(corners) >= 3
    if sum(corners) == 2:
        return None
    if square and not all(line(p, n, filled) for p, n in sides):
        return None
    if not square and sum(line(p, n, filled) for p, n in arcs) < len(arcs) - 1:   # one arc may lie on a bar edge
        return None
    if filled:
        return "filled_square" if square else "filled_circle"
    if square:
        return "open_square"
    xs = np.array([[s * d, u * d] for d in (2.0, 3.5) for s in (-1, 1) for u in (-1, 1)])   # on the X
    return "crossed_circle" if med(xs) < med(off) - DARK_MIN else "open_circle"


def _markers(g, x_min, y_min, y_max):
    """Markers (x, y, kind, score): peaks of the best normalised correlation over the five templates, highest first,
    kept when the shape test names a kind (the test's kind is kept)."""
    gu = cv2.resize(g, None, fx=UP, fy=UP, interpolation=cv2.INTER_CUBIC)
    maps = []
    for kind in KINDS:
        t, h = _template(kind)
        maps.append(cv2.matchTemplate(gu, t, cv2.TM_CCOEFF_NORMED))
    best = np.stack(maps).max(0)
    s, s0 = int(round(1.6 * HALF * UP)), 2 * UP
    out = []
    while True:
        y, x = np.unravel_index(best.argmax(), best.shape)
        if best[y, x] < MATCH_MIN:
            break
        cx, cy = (x + h + 0.5) / UP - 0.5, (y + h + 0.5) / UP - 0.5
        kind = None
        if x_min < cx and y_min < cy < y_max:
            # the shape test over offsets up to 1.5 px from the peak; the marker is the most frequent kind, centred
            # on the offsets that pass as it
            hits = [(k, cx + dx, cy + dy) for dx in SEARCH for dy in SEARCH if (k := _kind(g, cx + dx, cy + dy))]
            if hits:
                kinds = [k for k, _, _ in hits]
                kind = max(set(kinds), key=kinds.count)
                cx = float(np.mean([p for k, p, _ in hits if k == kind]))
                cy = float(np.mean([q for k, _, q in hits if k == kind]))
        if kind:
            out.append((cx, cy, kind, float(best[y, x])))
            best[max(0, y - s):y + s, max(0, x - s):x + s] = -1
        else:
            best[max(0, y - s0):y + s0, max(0, x - s0):x + s0] = -1
    return out


def _foot(xx, yy, cx, cy, grow=0.0):
    return (np.abs(xx - cx) <= HALF + grow) & (np.abs(yy - cy) <= HALF + grow)


def _fill_kind(rgb):
    r, g_, b = (float(v) for v in rgb)
    if max(r, g_, b) - min(r, g_, b) < 20:
        return "grey"
    return "red" if r > b else "blue"


def read(fig):
    img, scale = fig.render(DPI)
    g = img.astype(np.float32).mean(2)
    sat = img.max(2).astype(int) - img.min(2).astype(int)
    col, ticks = _axis(g)
    if len(ticks) != len(TICK_VALUES):
        raise ValueError(f"{len(ticks)} ticks found, {len(TICK_VALUES)} labels")
    cal = calibrate(list(zip(ticks, TICK_VALUES)))
    unc = RASTER_UNCERTAINTY_PX_300DPI + cal.residual / abs(cal.slope)
    base = int(round(ticks[-1]))

    row = g[base - 2, col + 3:]
    spans = [(a + col + 3, b + col + 3) for a, b in _runs(row < 235) if b - a >= 25]
    if len(spans) != len(BARS):
        raise ValueError(f"{len(spans)} bars found, {len(BARS)} expected")

    # markers centred inside the axis range at least half a marker below the top tick (the title reaches that row)
    # markers are black: found on the brightest channel, in which the coloured bar fills are light
    found = _markers(img.max(2).astype(np.float32), col + 3, ticks[0] + HALF + 2, base + 4)
    yy, xx = np.mgrid[:g.shape[0], :g.shape[1]]
    disc = np.zeros(g.shape, bool)
    for cx, cy, _, _ in found:
        disc |= _foot(xx, yy, cx, cy, 1.0)
    dk = (g < 200) & (sat < 60)
    outline = (g < 90) & (sat < 60)

    res = {}
    for grp, kind, (x0, x1) in zip(BARS, FILL, spans):
        # whisker: the column near the span centre with the most dark neutral pixels above the baseline
        mid = (x0 + x1) // 2
        xc = float(mid - 8 + int(outline[:base - 3, mid - 8:mid + 9].sum(0).argmax()))
        # bar top: the highest row from which every row down to the baseline is non-white across 90% of the
        # interior away from the whisker; the outline row weighted on the interior columns with no marker there
        inner = [x for x in range(x0 + 3, x1 - 2) if abs(x - xc) > 3]
        solid = (g[:, inner] < 235).mean(1) >= 0.9
        top = base - 2
        while top > 0 and solid[top - 1]:
            top -= 1
        cols = [x for x in inner if not disc[max(0, top - 2):top + 3, x].any()]
        fills = img[top + 3:base - 3][:, cols].reshape(-1, 3) if cols else img[top + 3:base - 3, x0 + 3:x1 - 2].reshape(-1, 3)
        if _fill_kind(np.median(fills, 0)) != kind:
            raise ValueError(f"bar {grp}: fill is not {kind}")
        bar = {}
        if len(cols) >= 3:   # otherwise markers cover the whole bar top: no mean
            fill = float(np.median(g[top + 3:top + 6, cols]))
            idx = np.arange(top - 2, top + 5)
            prof = g[idx][:, cols].mean(1)
            k = int(prof.argmin())
            ref = np.where(np.arange(len(idx)) < k, 255.0, fill)
            ref[k] = (255.0 + fill) / 2
            wgt = np.clip(ref - prof, 0, None)
            wgt[np.abs(np.arange(len(idx)) - k) > 1] = 0
            bar_row = float((idx * wgt).sum() / wgt.sum()) if wgt.sum() > 0 else float(idx[k])
            bar["mean"] = [cal.value(bar_row), *cal.interval(bar_row, unc)]

        mine = sorted([e for e in found if x0 - 10 <= e[0] <= x1 + 10], key=lambda e: e[1])
        kinds_ok = sorted(e[2] for e in mine) == sorted(KINDS)
        apart = all(not (_foot(xx, yy, a[0], a[1]) & _foot(xx, yy, b[0], b[1])).any()
                    for i, a in enumerate(mine) for b in mine[i + 1:])
        # hidden markers: dark neutral outline pixels left in the marker band once found markers, the whisker, caps,
        # the bar top and sides and the baseline are taken out
        left = 0
        if mine:
            r_ = outline.copy()
            r_[disc] = False
            r_[:, :x0 - 12] = False
            r_[:, x1 + 13:] = False
            r_[base - 3:] = False
            r_[:int(min(e[1] for e in mine)) - 10] = False
            r_[int(max(e[1] for e in mine)) + 10:] = False
            r_[:, int(xc) - 2:int(xc) + 3] = False
            r_[:, x0 - 2:x0 + 3] = False
            r_[:, x1 - 2:x1 + 3] = False
            for y in range(r_.shape[0]):
                if outline[y, int(xc) - 6:int(xc) + 7].mean() > 0.5 or dk[y, x0 + 2:x1 - 1].mean() > 0.5:
                    r_[y] = False
            left = int(r_.sum())
        hidden = left > RESIDUAL_MAX
        capcols = [x for x in range(int(xc) - 14, int(xc) + 15) if 2.5 <= abs(x - xc) <= 6.5]

        def free(y):
            return [x for x in capcols if not disc[y, x]]

        def is_cap(y):
            # a thin dark line (at most 3 rows) with white rows just above and below it where no found marker covers
            cs = free(y)
            if len(cs) < CAP_MIN_COLS or dk[y, cs].mean() < 0.8:
                return False
            a = y
            while a > y - 3 and dk[a - 1, cs].mean() >= 0.5:
                a -= 1
            b = y
            while b < y + 3 and dk[b + 1, cs].mean() >= 0.5:
                b += 1
            sides = [([x for x in cs if not disc[r, x]], r) for r in (a - 2, b + 2)]
            if max(len(s) for s, _ in sides) < 3 or (hidden and min(len(s) for s, _ in sides) < 3):
                return False
            return all(len(s) < 3 or (g[r, s] > 220).mean() >= 0.8 for s, r in sides)

        # upper cap: the first such line above the bar top, while the whisker continues
        cap = None
        for y in range(top - 3, 0, -1):
            if is_cap(y):
                ii = list(range(y - 2, y + 3))
                ww = np.array([max(235 - float(np.median(g[r, free(y)])), 0) for r in ii])
                ww[[not (dk[r, free(y)].mean() >= 0.5) for r in ii]] = 0
                for j in (1, 0):   # keep the dark run through y only
                    if ww[j + 1] == 0:
                        ww[j] = 0
                for j in (3, 4):
                    if ww[j - 1] == 0:
                        ww[j] = 0
                cap = float((np.array(ii) * ww).sum() / ww.sum())
                break
            if y < top - 12 and not (g[y, int(xc) - 1:int(xc) + 2] < 220).any() and not disc[y, int(xc)]:
                break  # no whisker: no error bar
        if cap is not None:
            bar["error"] = [cal.value(cap), *cal.interval(cap, unc)]
        bar = {k: [v[0], min(v[1], v[0]), max(v[2], v[0])] for k, v in bar.items()}

        pts = [point(cal, cy, unc, fig.to_page(cx + 0.5, cy + 0.5, scale)) for cx, cy, _, _ in mine]
        countable = kinds_ok and apart and not hidden
        res[grp] = {"points": pts if countable else [], "countable": countable, "bar": bar}
    return {"groups": {label: res[grp] for label, grp in LABELS.items()}}
