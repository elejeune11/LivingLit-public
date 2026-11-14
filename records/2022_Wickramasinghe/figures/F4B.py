"""Fig. 4B (journal_version.pdf p. 10): % SIRPA+CD90-CD36+ cells, six bars (Control, LCFA, GW0742, LCFA + GW0742,
GSK0660, LCFA + GSK0660, in legend order), mean ± SD with circle markers (dark outline, bar-coloured fill; one per
biological replicate, n = 7-19). Raster (the page figure is one 300 dpi JPEG image).

Read as figures/F2F.py: the y axis column and its tick marks are found in the image (tick values are the printed
labels 100, 80, ..., 0); bars are the six non-white spans just above the baseline; markers are rings found by
normalised correlation with a ring template on the grey image upsampled 4x (markers here are about 9 px across, so
the ring radius is 3.6 px). A bar's markers are countable when their number lies within the printed n = 7-19, every
pair of centres lies at least 11 px apart (outer diameter about 10 px, plus 1 px of background between them), and
no outline pixels are left in the marker band once the found rings, whisker, caps and bar outline are taken out
(overlapping markers the template misses leave 45 or more). The low bars' markers are packed into touching or
overlapping rows, so those bars give the bar only. The bar top is the highest row from which the bar is solid down
to the baseline, since markers sit on it.
"""
import numpy as np
import cv2

from livinglit.figures.source import calibrate, point, RASTER_UNCERTAINTY_PX_300DPI

DPI = 300
TICK_VALUES = [100, 80, 60, 40, 20, 0]    # printed tick labels, top to bottom
BARS = ["control", "lcfa", "gw", "lcfa_gw", "gsk", "lcfa_gsk"]
# label returned -> bar read
LABELS = {f"F4B_cd36/{b}": b for b in BARS}
LABELS.update({
    "F4B_cd36_lcfa/lcfa": "lcfa", "F4B_cd36_lcfa/control": "control",
    "F4B_cd36_lcfa_gw/lcfa_gw": "lcfa_gw", "F4B_cd36_lcfa_gw/control": "control",
    "F4B_cd36_gw/gw": "gw", "F4B_cd36_gw/control": "control",
})
N_RANGE = (7, 19)                  # n = 7-19 per the legend
RING_R, RING_W, UP = 3.6, 1.4, 4   # ring radius and width (px at 300 dpi), upsampling
APART = 11.0                       # markers are about 10 px across (outer edge); centres this far apart leave a gap
RESIDUAL_MAX = 20                  # outline pixels allowed outside found rings (bars with hidden markers leave 45+)
MATCH_MIN = 0.5
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
    """Axis column (longest dark column in the left third) and tick-mark rows (darkness centroids)."""
    w = g.shape[1] // 3
    col = int((g[:, :w] < 200).sum(0).argmax())
    span = g[:, col - 6:col - 1]
    ticks = []
    for a, b in _runs((span < 200).sum(1) >= 4):
        idx = np.arange(a - 1, b + 2)
        d = 255 - span[idx].mean(1)
        ticks.append(float((idx * d).sum() / d.sum()))
    return col, ticks


def _rings(g, x_min, y_max):
    """Centres (x, y, score) of ring-shaped marks: peaks of the normalised correlation with a ring template."""
    gu = cv2.resize(g, None, fx=UP, fy=UP, interpolation=cv2.INTER_CUBIC)
    h = int(np.ceil((RING_R + 1.5) * UP))
    yy, xx = np.mgrid[-h:h + 1, -h:h + 1] / UP
    t = np.where(np.abs(np.hypot(yy, xx) - RING_R) < RING_W / 2, 0.0, 1.0).astype(np.float32)
    m = cv2.matchTemplate(gu, t, cv2.TM_CCOEFF_NORMED)
    sup = int(round(2 * RING_R * UP * 0.8))
    out = []
    while True:
        y, x = np.unravel_index(m.argmax(), m.shape)
        if m[y, x] < MATCH_MIN:
            break
        cx, cy = (x + h + 0.5) / UP - 0.5, (y + h + 0.5) / UP - 0.5
        if cx > x_min and cy < y_max:
            out.append((cx, cy, float(m[y, x])))
        m[max(0, y - sup):y + sup, max(0, x - sup):x + sup] = -1
    return out


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
    spans = [(a + col + 3, b + col + 3) for a, b in _runs(row < 235) if b - a >= 30]
    if len(spans) != len(BARS):
        raise ValueError(f"{len(spans)} bars found, {len(BARS)} expected")

    rings = _rings(g, col + 3, base - 1)
    yy, xx = np.mgrid[:g.shape[0], :g.shape[1]]
    ring_disc = np.zeros(g.shape, bool)
    for cx, cy, _ in rings:
        ring_disc |= np.hypot(xx - cx, yy - cy) <= RING_R + 1.8
    dk = (g < 200) & (sat < 60)
    outline = (g < 100) & (sat < 60)

    res = {}
    for grp, (x0, x1) in zip(BARS, spans):
        xc = (x0 + x1) / 2
        # bar top: per marker-free interior column away from the whisker, the top of the non-white run rising
        # from the baseline; the outline row by darkness against white above and the fill below
        # (markers cover every column of the low bars and touch their tops, so the top is the highest row from
        # which every row down to the baseline is non-white across 95% of the interior; the outline is then
        # weighted on the interior columns with no marker at that row)
        inner = [x for x in range(x0 + 3, x1 - 2) if abs(x - xc) > 3]
        solid = (g[:, inner] < 235).mean(1) >= 0.95
        top = base - 2
        while top > 0 and solid[top - 1]:
            top -= 1
        cols = [x for x in inner if not ring_disc[max(0, top - 2):top + 5, x].any()]
        if len(cols) < 3:
            raise ValueError(f"{grp}: {len(cols)} marker-free columns at the bar top")
        fill = float(np.median(g[top + 3:top + 6, cols]))
        idx = np.arange(top - 2, top + 5)
        prof = g[idx][:, cols].mean(1)
        k = int(prof.argmin())
        ref = np.where(np.arange(len(idx)) < k, 255.0, fill)
        ref[k] = (255.0 + fill) / 2
        wgt = np.clip(ref - prof, 0, None)
        wgt[np.abs(np.arange(len(idx)) - k) > 1] = 0
        bar_row = float((idx * wgt).sum() / wgt.sum()) if wgt.sum() > 0 else float(idx[k])
        bar = {"mean": [cal.value(bar_row), *cal.interval(bar_row, unc)]}

        # upper cap: the first row above the bar top dark across the cap columns not covered by a marker
        capcols = [x for x in range(int(xc) - 14, int(xc) + 15) if 4.5 <= abs(x - xc) <= 12.5]

        def free(y):
            return [x for x in capcols if not ring_disc[y, x]]

        def is_cap(y):
            cs = free(y)
            return len(cs) >= CAP_MIN_COLS and dk[y, cs].mean() >= 0.8

        cap = None
        for y in range(top - 3, 0, -1):
            if is_cap(y):
                ii = [r for r in range(y - 2, y + 3) if is_cap(r)]
                ww = np.array([max(200 - float(np.median(g[r, free(r)])), 0) for r in ii])
                cap = float((np.array(ii) * ww).sum() / ww.sum())
                break
            if y < top - 12 and not (g[y, int(xc) - 1:int(xc) + 2] < 220).any():
                break  # no whisker: no error bar
        if cap is not None:
            bar["error"] = [cal.value(cap), *cal.interval(cap, unc)]
        bar = {k: [v[0], min(v[1], v[0]), max(v[2], v[0])] for k, v in bar.items()}

        mine = sorted([r for r in rings if x0 - 5 <= r[0] <= x1 + 5], key=lambda r: r[1])
        apart = all(np.hypot(a[0] - b[0], a[1] - b[1]) >= APART
                    for i, a in enumerate(mine) for b in mine[i + 1:])
        # hidden markers: dark neutral (outline) pixels left in the marker band once found rings, the whisker,
        # caps, the bar top and sides and the baseline are taken out
        left = 0
        if mine:
            res_ = outline.copy()
            res_[ring_disc] = False
            res_[:, :x0 - 5] = False
            res_[:, x1 + 6:] = False
            res_[base - 3:] = False
            res_[:int(mine[0][1]) - 6] = False
            res_[:, int(xc) - 2:int(xc) + 3] = False
            res_[:, x0 - 2:x0 + 3] = False
            res_[:, x1 - 2:x1 + 3] = False
            for y in range(res_.shape[0]):
                if outline[y, int(xc) - 8:int(xc) + 9].mean() > 0.7 or outline[y, x0 + 2:x1 - 1].mean() > 0.5:
                    res_[y] = False
            left = int(res_.sum())
        pts = [point(cal, cy, unc, fig.to_page(cx + 0.5, cy + 0.5, scale)) for cx, cy, _ in mine]
        countable = N_RANGE[0] <= len(pts) <= N_RANGE[1] and apart and left <= RESIDUAL_MAX
        res[grp] = {"points": pts if countable else [], "countable": countable, "bar": bar}
    return {"groups": {label: res[grp] for label, grp in LABELS.items()}}
