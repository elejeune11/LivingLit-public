"""Fig. S4A (NIHMS1982259-supplement-Supplement_text.pdf p. 9): % SIRPA+CD90-CD36+ cells at nine LCFA concentrations
(0, 5, 12.5, 25, 50, 75, 100, 125, 250 μM), a grey bar (Control at 0 μM, LCFA otherwise) and a red bar (GW0742 at
0 μM, LCFA + GW0742 otherwise) per concentration; mean with an upper error bar and elliptical markers (dark outline,
bar-coloured fill; one per biological replicate, n = 4). Raster (the page is one 300 dpi image).

Read as figures/F4B.py: the y axis column and its tick marks are found in the image (tick values are the printed
labels 100, 80, ..., 0); bars are the 18 non-white spans just above the baseline; markers are ellipse outlines found
by normalised correlation with an ellipse-ring template on the grey image upsampled 4x (markers are about 19 x 10 px
outer, so the outline ellipse has semi-axes 8.7 x 4.0 px). A bar's markers are countable when exactly the printed
n = 4 are found, no two outlines touch (identical axis-aligned ellipses with outer semi-axes A, B leave a gap of at
least 1 px when (dx/2A')^2 + (dy/2B')^2 >= 1 with A' = A + 0.5, B' = B + 0.5), and no outline pixels are left in
the marker band once the found ellipses, whisker, caps and bar outline are taken out. Otherwise the bar gives the bar
only.
"""
import numpy as np
import cv2

from livinglit.figures.source import calibrate, point, RASTER_UNCERTAINTY_PX_300DPI

DPI = 300
TICK_VALUES = [100, 80, 60, 40, 20, 0]    # printed tick labels, top to bottom
DOSES = ["0", "5", "12p5", "25", "50", "75", "100", "125", "250"]
BARS = [g for d in DOSES for g in ((f"ctrl_{d}", f"gw_{d}") if d == "0" else (f"lcfa_{d}", f"lcfa_gw_{d}"))]
LABELS = {}                        # label returned -> bar read
for d in DOSES:
    for b in BARS:
        if b.endswith(f"_{d}"):
            LABELS[f"S4A_{d}/{b}"] = b
for d in DOSES[1:]:
    LABELS[f"S4A_dose/lcfa_gw_{d}"] = f"lcfa_gw_{d}"
N = 4                              # n = 4 biological replicates per the legend
EA, EB, EW, UP = 8.7, 4.0, 1.6, 4  # outline ellipse semi-axes and line width (px at 300 dpi), upsampling
EA_ALL = (7.2, 8.0, 8.7)           # horizontal semi-axes tried (the narrowest markers are 16 px across)
OA, OB = EA + EW / 2 + 0.5, EB + EW / 2 + 0.5   # outer semi-axes plus half the 1 px gap
RESIDUAL_MAX = 20                  # outline pixels allowed outside found ellipses
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


def _ellipses(g, x_min, y_max):
    """Centres (x, y, score) of ellipse outlines: peaks of the normalised correlation with an ellipse-ring template."""
    gu = cv2.resize(g, None, fx=UP, fy=UP, interpolation=cv2.INTER_CUBIC)
    hx, hy = int(np.ceil((EA + 2) * UP)), int(np.ceil((EB + 2) * UP))
    yy, xx = np.mgrid[-hy:hy + 1, -hx:hx + 1] / UP
    m = None
    for ea in EA_ALL:   # marker widths differ (outer 16-19 px): best match over the template widths
        # distance to the ellipse approximated by the normalised radius times the local semi-axis
        r = np.hypot(xx / ea, yy / EB)
        loc = np.hypot(xx, yy) / np.maximum(r, 1e-6)
        t = np.where(np.abs(r - 1) * loc < EW / 2, 0.0, 1.0).astype(np.float32)
        mi = cv2.matchTemplate(gu, t, cv2.TM_CCOEFF_NORMED)
        m = mi if m is None else np.maximum(m, mi)
    sx, sy = int(round(1.6 * EA * UP)), int(round(1.6 * EB * UP))
    out = []
    while True:
        y, x = np.unravel_index(m.argmax(), m.shape)
        if m[y, x] < MATCH_MIN:
            break
        cx, cy = (x + hx + 0.5) / UP - 0.5, (y + hy + 0.5) / UP - 0.5
        if cx > x_min and cy < y_max:
            out.append((cx, cy, float(m[y, x])))
        m[max(0, y - sy):y + sy, max(0, x - sx):x + sx] = -1
    return out


def _inside(xx, yy, cx, cy, grow=0.0):
    return ((xx - cx) / (EA + EW / 2 + 1.0 + grow)) ** 2 + ((yy - cy) / (EB + EW / 2 + 1.0 + grow)) ** 2 <= 1


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

    found = _ellipses(g, col + 3, base - 1)
    yy, xx = np.mgrid[:g.shape[0], :g.shape[1]]
    disc = np.zeros(g.shape, bool)
    for cx, cy, _ in found:
        disc |= _inside(xx, yy, cx, cy)
    dk = (g < 200) & (sat < 60)
    outline = (g < 100) & (sat < 60)

    res = {}
    for grp, (x0, x1) in zip(BARS, spans):
        xc = (x0 + x1) / 2
        # bar top: the highest row from which every row down to the baseline is non-white across 95% of the
        # interior away from the whisker; the outline row weighted on the interior columns with no marker there
        inner = [x for x in range(x0 + 3, x1 - 2) if abs(x - xc) > 3]
        solid = (g[:, inner] < 235).mean(1) >= 0.95
        top = base - 2
        while top > 0 and solid[top - 1]:
            top -= 1
        cols = [x for x in inner if not disc[max(0, top - 2):top + 3, x].any()]
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

        mine = sorted([e for e in found if x0 - 8 <= e[0] <= x1 + 8], key=lambda e: e[1])
        apart = all(((a[0] - b[0]) / (2 * OA)) ** 2 + ((a[1] - b[1]) / (2 * OB)) ** 2 >= 1
                    for i, a in enumerate(mine) for b in mine[i + 1:])
        # hidden markers: dark neutral (outline) pixels left in the marker band once found ellipses, the whisker,
        # caps, the bar top and sides and the baseline are taken out
        left = 0
        if mine:
            r_ = outline.copy()
            r_[disc] = False
            r_[:, :x0 - 10] = False
            r_[:, x1 + 11:] = False
            r_[base - 3:] = False
            r_[:int(mine[0][1]) - 7] = False
            r_[int(mine[-1][1]) + 8:] = False
            r_[:, int(xc) - 2:int(xc) + 3] = False
            r_[:, x0 - 2:x0 + 3] = False
            r_[:, x1 - 2:x1 + 3] = False
            for y in range(r_.shape[0]):
                if outline[y, int(xc) - 8:int(xc) + 9].mean() > 0.7 or outline[y, x0 + 2:x1 - 1].mean() > 0.5:
                    r_[y] = False
            left = int(r_.sum())
        # upper cap: the first row above the bar top dark across the cap columns not covered by a marker
        hidden = left > RESIDUAL_MAX
        capcols = [x for x in range(int(xc) - 14, int(xc) + 15) if 2.5 <= abs(x - xc) <= 7.5]

        def free(y):
            return [x for x in capcols if not disc[y, x]]

        def is_cap(y):
            # a thin dark line (at most 3 rows) with white rows just above and below it, where no found marker
            # covers those rows (an unfound marker's outline has fill on one side)
            cs = free(y)
            if len(cs) < CAP_MIN_COLS or dk[y, cs].mean() < 0.8:
                return False
            a = y
            while a > y - 3 and dk[a - 1, cs].mean() >= 0.5:
                a -= 1
            b = y
            while b < y + 3 and dk[b + 1, cs].mean() >= 0.5:
                b += 1
            sides = [([x for x in cs if not disc[r, x]], r) for r in (a - 2, b + 2)]   # past the antialiased edge
            # next to hidden markers both sides must be seen white (a covered side may hide a marker's fill)
            if max(len(s) for s, _ in sides) < 3 or (hidden and min(len(s) for s, _ in sides) < 3):
                return False
            return all(len(s) < 3 or (g[r, s] > 220).mean() >= 0.8 for s, r in sides)

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
            if y < top - 12 and not (g[y, int(xc) - 1:int(xc) + 2] < 220).any():
                break  # no whisker: no error bar
        if cap is not None:
            bar["error"] = [cal.value(cap), *cal.interval(cap, unc)]
        bar = {k: [v[0], min(v[1], v[0]), max(v[2], v[0])] for k, v in bar.items()}

        pts = [point(cal, cy, unc, fig.to_page(cx + 0.5, cy + 0.5, scale)) for cx, cy, _ in mine]
        countable = len(pts) == N and apart and left <= RESIDUAL_MAX
        res[grp] = {"points": pts if countable else [], "countable": countable, "bar": bar}
    return {"groups": {label: res[grp] for label, grp in LABELS.items()}}
