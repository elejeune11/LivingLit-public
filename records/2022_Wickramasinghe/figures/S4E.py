"""Fig. S4E (NIHMS1982259-supplement-Supplement_text.pdf p. 9): PMP70 mean intensity fold (flow cytometry) in hPSC-CMs,
five bars (Control, LCFA, GW0742, LCFA + GW0742, GSK0660; mean with an SD whisker and caps) with one circle marker per
replicate: a black outline filled with the bar's colour. Raster (the page is one image, about 300 dpi). Fig. S4D is
images only.

The y axis column and its tick marks are found in the image (tick values are the printed labels 1.4, 1.3, ..., 0.8);
bars are the five non-white spans just above the baseline, in legend order, checked by their fill colour. Markers are
peaks of the normalised correlation (image upsampled 4x) with a ring template, each kept only when a shape test passes:
the ring is darker than the samples 2 px outside it on at least 6 of 8 arcs placed off the axes (a whisker, bar top or
neighbour may darken two) and darker than the marker's centre (sampled off the axes, where a whisker may cross it).
The upper cap is the highest thin grey line on white above the bar top joined to it by the whisker. A bar's markers
are countable when no two markers' footprints share a pixel and no dark outline pixels are left in the marker band once
the found markers, whisker, caps and bar outline are taken out. Otherwise the bar gives the bar only.
"""
import numpy as np
import cv2
from scipy.ndimage import map_coordinates

from livinglit.figures.source import calibrate, point, RASTER_UNCERTAINTY_PX_300DPI

DPI = 300
TICK_VALUES = [1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8]  # printed tick labels, top to bottom
BARS = ["control", "lcfa", "gw", "lcfa_gw", "gsk"]   # legend order, left to right
FILL = ["light grey", "dark grey", "red", "red", "blue"]
LABELS = {
    "S4E_pmp70/control": "control", "S4E_pmp70/lcfa": "lcfa", "S4E_pmp70/gw": "gw",
    "S4E_pmp70/lcfa_gw": "lcfa_gw", "S4E_pmp70/gsk": "gsk",
    "S4E_pmp70_gw/gw": "gw", "S4E_pmp70_gw/control": "control",
    "S4E_pmp70_lcfa_gw/lcfa_gw": "lcfa_gw", "S4E_pmp70_lcfa_gw/control": "control",
}
R, LW, UP = 3.5, 1.5, 4        # ring radius at the outline's centre, line width (px at 300 dpi), upsampling
HALF = R + LW / 2              # half the outer size
MATCH_MIN = 0.4
DARK_MIN = 50                  # grey levels below the samples beside it for a dark part
CENTRE_MIN = 30                # grey levels the ring lies below the marker's centre
ARCS_MIN = 6                   # of 8 arcs dark against outside (a whisker, bar edge or neighbour may darken two)
RESIDUAL_MAX = 6               # outline pixels allowed outside found markers
CAP_MIN_COLS = 8
CAP_HALF = 20                  # caps reach about 20 px either side of the whisker


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
    col = int((g[:, :w] < 150).sum(0).argmax())
    span = g[:, max(0, col - 6):col - 1]
    ticks = []
    for a, b in _runs((span < 150).sum(1) >= 3):
        idx = np.arange(a - 1, b + 2)
        d = 255 - span[idx].mean(1)
        ticks.append(float((idx * d).sum() / d.sum()))
    return col, ticks


def _template():
    """Dark (0) ring on light (1), in upsampled pixels, centred."""
    h = int(np.ceil((HALF + 2) * UP))
    yy, xx = np.mgrid[-h:h + 1, -h:h + 1] / UP
    ring = np.abs(np.hypot(xx, yy) - R) < LW / 2
    return np.where(ring, 0.0, 1.0).astype(np.float32), h


def _sample(g, cx, cy, pts):
    pts = np.asarray(pts, float)
    return map_coordinates(g, [cy + pts[:, 1], cx + pts[:, 0]], order=1, mode="nearest")


def _is_marker(g, cx, cy):
    """A ring at (cx, cy): dark on at least 7 of 8 arcs off the axes against 2 px outside it, and the ring as a whole
    darker (by CENTRE_MIN) than its centre, which holds the bar's colour (as dark as 120 grey levels)."""
    # the centre off the axes, where a whisker or cap may run through the marker
    centre = float(np.median(_sample(g, cx, cy, [[1.1, 1.1], [1.1, -1.1], [-1.1, 1.1], [-1.1, -1.1]])))
    ok, ons = 0, []
    for c in np.pi / 8 * np.array([1, 3, 5, 7, 9, 11, 13, 15]):
        u = c + np.linspace(-0.2, 0.2, 3)
        n = np.c_[np.cos(u), np.sin(u)]
        on = min(float(np.median(_sample(g, cx, cy, r * n))) for r in (R - 0.5, R, R + 0.5))
        out = float(np.median(_sample(g, cx, cy, (R + 2.0) * n)))
        ok += on < out - DARK_MIN
        ons.append(on)
    return ok >= ARCS_MIN and float(np.median(ons)) < centre - CENTRE_MIN


def _markers(g, x_min, y_min, y_max):
    """Markers (x, y): template peaks, highest first, kept when the shape test passes at an offset up to 1 px."""
    gu = cv2.resize(g, None, fx=UP, fy=UP, interpolation=cv2.INTER_CUBIC)
    t, h = _template()
    best = cv2.matchTemplate(gu, t, cv2.TM_CCOEFF_NORMED)
    s, s0 = int(round(1.5 * HALF * UP)), UP
    out = []
    offs = np.arange(-1.0, 1.01, 0.5)
    while True:
        y, x = np.unravel_index(best.argmax(), best.shape)
        if best[y, x] < MATCH_MIN:
            break
        cx, cy = (x + h + 0.5) / UP - 0.5, (y + h + 0.5) / UP - 0.5
        hits = []
        if x_min < cx and y_min < cy < y_max:
            hits = [(cx + dx, cy + dy) for dx in offs for dy in offs if _is_marker(g, cx + dx, cy + dy)]
        if hits:
            out.append((float(np.mean([p for p, _ in hits])), float(np.mean([q for _, q in hits]))))
            best[max(0, y - s):y + s, max(0, x - s):x + s] = -1
        else:
            best[max(0, y - s0):y + s0, max(0, x - s0):x + s0] = -1
    return out


def _foot(xx, yy, cx, cy, grow=0.0):
    return np.hypot(xx - cx, yy - cy) <= HALF + grow


def _fill_kind(rgb):
    r, g_, b = (float(v) for v in rgb)
    if max(r, g_, b) - min(r, g_, b) < 20:
        return "light grey" if r > 160 else "dark grey"
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

    # markers are black outlines: found on the darkest channel, in which the outline stays darkest
    found = _markers(g, col + 3, ticks[0] - 2, base - 2)
    yy, xx = np.mgrid[:g.shape[0], :g.shape[1]]
    disc = np.zeros(g.shape, bool)
    for cx, cy in found:
        disc |= _foot(xx, yy, cx, cy, 1.0)
    outline = (g < 90) & (sat < 60)
    dk = (g < 200) & (sat < 60)

    res = {}
    for grp, kind, (x0, x1) in zip(BARS, FILL, spans):
        mid = (x0 + x1) // 2
        # whisker: the column near the span centre with the most dark neutral pixels above the baseline, off markers
        ol = outline[:base - 3, mid - 6:mid + 7] & ~disc[:base - 3, mid - 6:mid + 7]
        xc = float(mid - 6 + int(ol.sum(0).argmax()))
        # bar top: the highest row from which every row down to the baseline is non-white across 90% of the interior
        # away from the whisker; the outline row is the darkest row there on the interior columns with no marker
        inner = [x for x in range(x0 + 3, x1 - 2) if abs(x - xc) > 2]
        solid = (g[:, inner] < 235).mean(1) >= 0.9
        top = base - 2
        while top > 0 and solid[top - 1]:
            top -= 1
        cols = [x for x in inner if not disc[max(0, top - 2):top + 4, x].any()]
        fills = img[top + 3:base - 3][:, cols or inner].reshape(-1, 3)
        if _fill_kind(np.median(fills, 0)) != kind:
            raise ValueError(f"bar {grp}: fill is not {kind}")
        bar = {}
        if len(cols) >= 3:
            idx = np.arange(top - 1, top + 4)
            prof = g[idx][:, cols].mean(1)
            k = int(prof.argmin())
            fill = float(np.median(g[top + 4:top + 7, cols]))
            wgt = np.clip(np.minimum(255.0, fill) - prof, 0, None)
            wgt[np.abs(np.arange(len(idx)) - k) > 1] = 0
            bar_row = float((idx * wgt).sum() / wgt.sum()) if wgt.sum() > 0 else float(idx[k])
            bar["mean"] = [cal.value(bar_row), *cal.interval(bar_row, unc)]

        mine = sorted([e for e in found if x0 - 8 <= e[0] <= x1 + 8], key=lambda e: e[1])
        apart = all(np.hypot(a[0] - b[0], a[1] - b[1]) > 2 * HALF for i, a in enumerate(mine) for b in mine[i + 1:])

        capcols = [x for x in range(int(xc) - 14, int(xc) + 15) if abs(x - xc) >= 2.5]

        def free(y):
            return [x for x in capcols if not disc[y, x]]

        def lines(mask, y0, y1):
            """Runs of rows in [y0, y1) dark across 80% of the free cap columns: horizontal cap lines."""
            rows = [len(free(y)) >= CAP_MIN_COLS and mask[y, free(y)].mean() >= 0.8 for y in range(y0, y1)]
            return [(a + y0, b + y0) for a, b in _runs(rows)]

        # caps inside the bar are black on the fill (for the residual test); the upper cap is a thin line, drawn
        # grey by anti-aliasing, on white above the bar top
        caps = lines(outline, 0, base - 3) + lines(dk, 0, top - 2)
        cap = None
        for a, b in sorted(lines(dk, 0, top - 2)):
            # joined to the bar top by the whisker (dark or under a marker on 80% of the rows between)
            seg = range(b + 1, top - 1)
            joined = [(g[y, int(xc) - 1:int(xc) + 2] < 200).any() or disc[y, int(xc)] for y in seg]
            if not joined or np.mean(joined) >= 0.8:
                ii = np.arange(a - 1, b + 2)
                cs = free(a)
                ww = np.clip(250 - np.median(g[ii][:, cs], 1), 0, None)
                cap = float((ii * ww).sum() / ww.sum())
                break
        if cap is not None:
            bar["error"] = [cal.value(cap), *cal.interval(cap, unc)]
        bar = {k: [v[0], min(v[1], v[0]), max(v[2], v[0])] for k, v in bar.items()}

        # hidden markers: outline pixels left in the marker band once markers, whisker, caps, bar outline and
        # baseline are taken out
        left = 0
        if mine:
            r_ = outline.copy()
            r_[disc] = False
            r_[:, :x0 - 8] = False
            r_[:, x1 + 9:] = False
            r_[base - 3:] = False
            r_[:int(min(e[1] for e in mine)) - 8] = False
            r_[int(max(e[1] for e in mine)) + 8:] = False
            r_[:, int(xc) - 1:int(xc) + 2] = False
            r_[:, x0 - 1:x0 + 2] = False
            r_[:, x1 - 1:x1 + 2] = False
            r_[top - 1:top + 3] = False
            for a, b in caps:
                r_[a - 1:b + 2, int(xc) - CAP_HALF - 2:int(xc) + CAP_HALF + 3] = False   # the cap's full width
            left = int(r_.sum())
        countable = bool(mine) and apart and left <= RESIDUAL_MAX
        pts = [point(cal, cy, unc, fig.to_page(cx + 0.5, cy + 0.5, scale)) for cx, cy in mine]
        res[grp] = {"points": pts if countable else [], "countable": countable, "bar": bar}
    return {"groups": {label: res[grp] for label, grp in LABELS.items()}}
