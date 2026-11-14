"""Fig. 2F (journal_version.pdf p. 5): percentage of binucleated hPSC-CMs, nine bars (Control, LCFA, WY14643,
LCFA + WY14643, GW0742, LCFA + GW0742, Rosiglitazone, LCFA + Rosiglitazone, GSK0660, in legend order), mean ± SD
with open circle markers (dark outline, bar-coloured fill; one per biological replicate, n = 4). Raster (the page
figure is one 300 dpi JPEG image).

The y axis column and its tick marks are found in the image (tick values are the printed labels 25, 20, ..., 0).
Bars are the nine non-white spans just above the baseline. Markers are about 6 px rings that sit on whiskers and
caps and over the bar fill, so they are found by matching a ring template (radius 2.7 px, ring 1.4 px wide) on the
grey image upsampled 4x (normalised correlation); a marker's value is the template centre (0.25 px steps). True
rings score 0.55-0.84, other shapes in the plot area at most 0.47; peaks are kept above 0.5. A bar's markers are
countable when there are four and every pair of centres lies at least one ring diameter plus 1 px apart (there is
background between them). Bar mean is read as in figures/F1H.py; the upper cap is found on the cap columns
free of markers (see read()).
"""
import numpy as np
import cv2

from livinglit.figures.source import calibrate, point, RASTER_UNCERTAINTY_PX_300DPI

DPI = 300
TICK_VALUES = [25, 20, 15, 10, 5, 0]    # printed tick labels, top to bottom
BARS = ["control", "lcfa", "wy", "lcfa_wy", "gw", "lcfa_gw", "rosi", "lcfa_rosi", "gsk"]
# label returned -> bar read
LABELS = {f"F2F_binuc/{b}": b for b in BARS}
LABELS.update({"F2F_binuc_lcfa_gw/lcfa_gw": "lcfa_gw", "F2F_binuc_lcfa_gw/control": "control"})
N_MARKERS = 4                      # n = 4 per the legend
RING_R, RING_W, UP = 2.7, 1.4, 4   # ring radius and width (px at 300 dpi), upsampling
MATCH_MIN = 0.5
CAP_MIN_COLS = 6                   # cap columns free of markers needed to call a row a cap (caps ~21 px wide)


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
    out = []
    while True:
        y, x = np.unravel_index(m.argmax(), m.shape)
        if m[y, x] < MATCH_MIN:
            break
        # upsampled pixel u covers native pixel-index coordinate (u + 0.5) / UP - 0.5
        cx, cy = (x + h + 0.5) / UP - 0.5, (y + h + 0.5) / UP - 0.5
        if cx > x_min and cy < y_max:
            out.append((cx, cy, float(m[y, x])))
        m[max(0, y - 4 * UP):y + 4 * UP, max(0, x - 4 * UP):x + 4 * UP] = -1
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

    # bars: non-white spans a few rows above the baseline, right of the axis
    row = g[base - 4, col + 3:]
    spans = [(a + col + 3, b + col + 3) for a, b in _runs(row < 235) if b - a >= 30]
    if len(spans) != len(BARS):
        raise ValueError(f"{len(spans)} bars found, {len(BARS)} expected")

    rings = _rings(g, col + 3, base - 2)
    marker_mask = np.zeros(g.shape, bool)
    rr = int(np.ceil(RING_R + 2))
    for cx, cy, _ in rings:
        marker_mask[int(cy) - rr:int(cy) + rr + 2, int(cx) - rr:int(cx) + rr + 2] = True
    # tight mask for the cap test: a disc just past a ring's outer edge (a cap may pass through a ring's top)
    yy, xx = np.mgrid[:g.shape[0], :g.shape[1]]
    ring_disc = np.zeros(g.shape, bool)
    for cx, cy, _ in rings:
        ring_disc |= np.hypot(xx - cx, yy - cy) <= RING_R + 1.3
    dk = (g < 200) & (sat < 60)

    res = {}
    for grp, (x0, x1) in zip(BARS, spans):
        xc = (x0 + x1) / 2
        # bar top: per marker-free interior column away from the whisker, the top of the non-white run rising
        # from the baseline; the outline by darkness against white above and the fill below
        cols = [x for x in range(x0 + 3, x1 - 2) if abs(x - xc) > 3 and not marker_mask[:, x].any()]
        tops = []
        for x in cols:
            y = base - 2
            while y > 0 and g[y - 1, x] < 235:
                y -= 1
            tops.append(y)
        top = int(np.median(tops))
        fill = float(np.median(g[top + 5:top + 10, cols]))
        idx = np.arange(top - 2, top + 5)
        prof = g[idx][:, cols].mean(1)
        k = int(prof.argmin())
        ref = np.where(np.arange(len(idx)) < k, 255.0, fill)
        ref[k] = (255.0 + fill) / 2
        wgt = np.clip(ref - prof, 0, None)
        wgt[np.abs(np.arange(len(idx)) - k) > 1] = 0
        bar_row = float((idx * wgt).sum() / wgt.sum())
        bar = {"mean": [cal.value(bar_row), *cal.interval(bar_row, unc)]}

        # upper cap: the first row above the bar top that is dark across the cap columns (4.5-9.5 px either side
        # of the whisker; caps reach about 10.5) not covered by a marker. A marker can sit centred on the cap,
        # and a side-by-side pair of markers covers every cap column, so it cannot pass for a cap. The cap rows
        # are weighted by their median darkness over those columns.
        capcols = [x for x in range(int(xc) - 10, int(xc) + 11) if 4.5 <= abs(x - xc) <= 9.5]

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

        mine = sorted([r for r in rings if x0 - 4 <= r[0] <= x1 + 4], key=lambda r: r[1])
        apart = all(np.hypot(a[0] - b[0], a[1] - b[1]) >= 2 * RING_R + RING_W + 1
                    for i, a in enumerate(mine) for b in mine[i + 1:])
        pts = [point(cal, cy, unc, fig.to_page(cx + 0.5, cy + 0.5, scale)) for cx, cy, _ in mine]
        countable = len(pts) == N_MARKERS and apart
        res[grp] = {"points": pts if countable else [], "countable": countable, "bar": bar}
    return {"groups": {label: res[grp] for label, grp in LABELS.items()}}
