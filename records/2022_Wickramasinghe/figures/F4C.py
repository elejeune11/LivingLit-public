"""Fig. 4C (journal_version.pdf p. 10): % SIRPA+CD90-CD36+ cells in ventricular and atrial hPSC-CMs, ten bars in five
pairs (Control, LCFA, GW0742, LCFA + GW0742, GSK0660; ventricular light grey, atrial dark grey), mean ± SD with circle
markers (one per biological replicate, n = 2-4). Raster (the page figure is one 300 dpi JPEG image).

The y axis column and its tick marks are found in the image (tick values are the printed labels 100, 80, ..., 0);
bars are the ten non-white spans just above the baseline. Markers are about 9 px across with a dark outline:
ventricular markers have a light fill, atrial markers a dark grey fill (the bar colour). They are found by normalised
correlation (grey image upsampled 4x) with two templates: a ring (open markers, and atrial markers inside the dark
bars, where only the outline differs from the fill) and a filled disc (atrial markers on white). A bar's markers are
countable when their number lies within the printed n = 2-4 and every pair of centres lies at least 11 px apart
(outer diameter about 10 px, plus 1 px of background), no dark pixels are left in the marker band once the found
markers, whisker, caps and bar outline are taken out (touching markers the templates miss leave 20 or more), and the
found points' mean lies within 0.5 of the bar top (a marker hidden exactly under another changes the mean); otherwise
the bar gives the bar only.
The bar top is the outline row found as in figures/F4B.py; the upper cap is the first row above the bar top dark
across the cap columns not covered by a marker.
"""
import numpy as np
import cv2

from livinglit.figures.source import calibrate, point, RASTER_UNCERTAINTY_PX_300DPI

DPI = 300
TICK_VALUES = [100, 80, 60, 40, 20, 0]    # printed tick labels, top to bottom
BARS = ["v_control", "a_control", "v_lcfa", "a_lcfa", "v_gw", "a_gw", "v_lcfa_gw", "a_lcfa_gw", "v_gsk", "a_gsk"]
LABELS = {f"F4C_cd36/{b}": b for b in BARS}
for _b in ["v_gw", "v_lcfa_gw", "a_gw", "a_lcfa_gw"]:
    LABELS[f"F4C_{_b}/{_b}"] = _b
    LABELS[f"F4C_{_b}/{_b[0]}_control"] = f"{_b[0]}_control"
N_RANGE = (2, 4)                   # n = 2-4 per the legend
RING_R, RING_W, DISC_R, UP = 4.0, 1.8, 4.3, 4
APART = 11.0
RING_MIN, DISC_MIN = 0.6, 0.8
MEAN_TOL = 0.5                     # axis units (about 1.7 px): found points' mean against the bar top
RESIDUAL_MAX = 10                  # dark pixels allowed outside found markers, whisker, caps and outlines
CAP_MIN_COLS = 5
DEBUG = False


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


def _peaks(m, h, minimum, keep):
    sup = int(round(2 * RING_R * UP * 0.8))
    m = m.copy()
    out = []
    while True:
        y, x = np.unravel_index(m.argmax(), m.shape)
        if m[y, x] < minimum:
            break
        cx, cy = (x + h + 0.5) / UP - 0.5, (y + h + 0.5) / UP - 0.5
        if keep(cx, cy):
            out.append((cx, cy, float(m[y, x])))
        m[max(0, y - sup):y + sup, max(0, x - sup):x + sup] = -1
    return out


def _markers(g, keep):
    """Centres (x, y, score, kind) of ring-shaped and filled-disc marks: correlation peaks, merged."""
    gu = cv2.resize(g, None, fx=UP, fy=UP, interpolation=cv2.INTER_CUBIC)
    h = int(np.ceil((DISC_R + 1.5) * UP))
    yy, xx = np.mgrid[-h:h + 1, -h:h + 1] / UP
    rr = np.hypot(yy, xx)
    ring = np.where(np.abs(rr - RING_R) < RING_W / 2, 0.0, 1.0).astype(np.float32)
    disc = np.where(rr <= DISC_R, 0.0, 1.0).astype(np.float32)
    found = [(*p, "ring") for p in _peaks(cv2.matchTemplate(gu, ring, cv2.TM_CCOEFF_NORMED), h, RING_MIN, keep)]
    for p in _peaks(cv2.matchTemplate(gu, disc, cv2.TM_CCOEFF_NORMED), h, DISC_MIN, keep):
        if all(np.hypot(p[0] - q[0], p[1] - q[1]) > 4 for q in found):
            found.append((*p, "disc"))
    return found


def read(fig):
    img, scale = fig.render(DPI)
    g = img.astype(np.float32).mean(2)
    col, ticks = _axis(g)
    if len(ticks) != len(TICK_VALUES):
        raise ValueError(f"{len(ticks)} ticks found, {len(TICK_VALUES)} labels")
    cal = calibrate(list(zip(ticks, TICK_VALUES)))
    unc = RASTER_UNCERTAINTY_PX_300DPI + cal.residual / abs(cal.slope)
    base = int(round(ticks[-1]))

    row = g[base - 2, col + 3:]
    spans = [(a + col + 3, b + col + 3) for a, b in _runs(row < 235) if b - a >= 20]
    if len(spans) != len(BARS):
        raise ValueError(f"{len(spans)} bars found, {len(BARS)} expected")

    def keep(cx, cy):
        return cy < base + 1 and any(x0 - 5 <= cx <= x1 + 5 for x0, x1 in spans)

    marks = _markers(g, keep)
    if DEBUG:
        for m in sorted(marks):
            print("mark", [round(v, 2) if isinstance(v, float) else v for v in m], round(cal.value(m[1]), 2))
    yy, xx = np.mgrid[:g.shape[0], :g.shape[1]]
    disc_px = np.zeros(g.shape, bool)
    for cx, cy, _, _ in marks:
        disc_px |= np.hypot(xx - cx, yy - cy) <= RING_R + 1.8

    res = {}
    for grp, (x0, x1) in zip(BARS, spans):
        xc = (x0 + x1) / 2
        inner = [x for x in range(x0 + 3, x1 - 2) if abs(x - xc) > 3]
        solid = (g[:, inner] < 235).mean(1) >= 0.95
        top = base - 2
        while top > 0 and solid[top - 1]:
            top -= 1
        cols = [x for x in inner if not disc_px[max(0, top - 2):top + 5, x].any()]
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

        capcols = [x for x in range(int(xc) - 14, int(xc) + 15) if 3.5 <= abs(x - xc) <= 7.5]

        def free(y):
            return [x for x in capcols if not disc_px[y, x]]

        def is_cap(y):
            cs = free(y)
            return len(cs) >= CAP_MIN_COLS and (g[y, cs] < 200).mean() >= 0.8

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

        mine = sorted([m for m in marks if x0 - 5 <= m[0] <= x1 + 5], key=lambda m: m[1])
        apart = all(np.hypot(a[0] - b[0], a[1] - b[1]) >= APART
                    for i, a in enumerate(mine) for b in mine[i + 1:])
        # hidden markers: pixels much darker than their background (white above the bar top, the fill below) left
        # in the marker band once found markers, the whisker, caps, the bar top and sides and the baseline are out
        left = 0
        if mine:
            bg = np.where(yy < top - 1, 255.0, fill)
            res_ = (bg - g) > (60 if fill > 150 else 30)
            res_[disc_px] = False
            res_[:, :x0 - 5] = False
            res_[:, x1 + 6:] = False
            res_[base - 3:] = False
            res_[:int(mine[0][1]) - 6] = False
            res_[:, int(xc) - 2:int(xc) + 3] = False
            res_[:, x0 - 2:x0 + 3] = False
            res_[:, x1 - 2:x1 + 3] = False
            res_[top - 2:top + 3] = False
            for y in range(res_.shape[0]):
                if (bg[y, capcols] - g[y, capcols] > 30).mean() >= 0.7:
                    res_[y - 1:y + 2] = False
            left = int(res_.sum())
        pts = [point(cal, cy, unc, fig.to_page(cx + 0.5, cy + 0.5, scale)) for cx, cy, _, _ in mine]
        # a marker hidden exactly under another leaves no trace in the image, but the found points then miss the
        # drawn mean
        agree = bool(pts) and abs(np.mean([p["value"] for p in pts]) - bar["mean"][0]) <= MEAN_TOL
        countable = N_RANGE[0] <= len(pts) <= N_RANGE[1] and apart and left <= RESIDUAL_MAX and agree
        if DEBUG:
            print(grp, len(pts), apart, left, [round(p["value"], 2) for p in pts], bar)
        res[grp] = {"points": pts if countable else [], "countable": countable, "bar": bar}
    return {"groups": {label: res[grp] for label, grp in LABELS.items()}}
