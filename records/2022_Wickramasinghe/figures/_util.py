"""Helpers for this paper's Seahorse bar panels (Fig. 5H, Fig. S5D): five bars (Control, LCFA, GW0742,
LCFA + GW0742, GSK0660; mean with an SD whisker and caps) with one ring marker per biological replicate (dark outline,
bar-coloured fill), raster at about 300 dpi. The method is that of figures/F5C.py (same marker style), with the tick
labels and the returned labels passed in: the y axis column and its tick marks are found in the image; bars are the
five non-white spans just above the baseline, checked by fill colour; markers are peaks of the normalised correlation
(image upsampled 4x) with a ring template, kept only when a shape test passes (ring darker than 2 px outside it on at
least 6 of 8 arcs, and darker than its centre). The upper cap is the highest thin grey line on white above the bar top
joined to it by the whisker. A bar's markers are countable when no two markers' footprints share a pixel and no dark
outline pixels are left in the marker band once the found markers, whisker, caps and bar outline are taken out.
Otherwise the bar gives the bar only.
"""
import numpy as np
import cv2
from scipy.ndimage import map_coordinates

from livinglit.figures.source import calibrate, point, RASTER_UNCERTAINTY_PX_300DPI

DPI = 300
BARS = ["control", "lcfa", "gw", "lcfa_gw", "gsk"]   # legend order, left to right
FILL = ["light grey", "dark grey", "red", "red", "blue"]
R, LW, UP = 3.5, 1.5, 4        # ring radius at the outline's centre, line width (px at 300 dpi), upsampling
HALF = R + LW / 2              # half the outer size
MATCH_MIN = 0.4
DARK_MIN = 50                  # grey levels below the samples beside it for a dark part
CENTRE_MIN = 30                # grey levels the ring lies below the marker's centre
ARCS_MIN = 6                   # of 8 arcs dark against outside (a whisker, bar edge or neighbour may darken two)
RESIDUAL_MAX = 6               # outline pixels allowed outside found markers
CAP_MIN_COLS = 8
CAP_FILL_MIN = 40              # grey levels a cap row inside the bar lies below the fill (brightest channel)
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


def _axis(g, tick_min=3):
    """Axis column (longest dark column in the left quarter) and tick-mark rows (darkness centroids): rows dark on at
    least tick_min of the 5 columns left of the axis."""
    w = g.shape[1] // 4
    col = int((g[:, :w] < 150).sum(0).argmax())
    span = g[:, max(0, col - 6):col - 1]
    ticks = []
    for a, b in _runs((span < 150).sum(1) >= tick_min):
        idx = np.arange(a - 1, b + 2)
        d = 255 - span[idx].mean(1)
        ticks.append(float((idx * d).sum() / d.sum()))
    return col, ticks


def _template(rad=R, lw=LW):
    """Dark (0) ring on light (1), in upsampled pixels, centred."""
    h = int(np.ceil((rad + lw / 2 + 2) * UP))
    yy, xx = np.mgrid[-h:h + 1, -h:h + 1] / UP
    ring = np.abs(np.hypot(xx, yy) - rad) < lw / 2
    return np.where(ring, 0.0, 1.0).astype(np.float32), h


def _sample(g, cx, cy, pts):
    pts = np.asarray(pts, float)
    return map_coordinates(g, [cy + pts[:, 1], cx + pts[:, 0]], order=1, mode="nearest")


def _is_marker(g, cx, cy, rad=R):
    """A ring at (cx, cy): dark on at least ARCS_MIN of 8 arcs against 2 px outside it, and the ring as a whole
    darker (by CENTRE_MIN) than its centre, which holds the bar's colour."""
    centre = float(np.median(_sample(g, cx, cy, [[1.1, 1.1], [1.1, -1.1], [-1.1, 1.1], [-1.1, -1.1]])))
    ok, ons = 0, []
    for c in np.pi / 8 * np.array([1, 3, 5, 7, 9, 11, 13, 15]):
        u = c + np.linspace(-0.2, 0.2, 3)
        n = np.c_[np.cos(u), np.sin(u)]
        on = min(float(np.median(_sample(g, cx, cy, r * n))) for r in (rad - 0.5, rad, rad + 0.5))
        out = float(np.median(_sample(g, cx, cy, (rad + 2.0) * n)))
        ok += on < out - DARK_MIN
        ons.append(on)
    return ok >= ARCS_MIN and float(np.median(ons)) < centre - CENTRE_MIN


def _markers(g, x_min, y_min, y_max, rad=R, lw=LW):
    """Markers (x, y): template peaks, highest first, kept when the shape test passes at an offset up to 1 px."""
    gu = cv2.resize(g, None, fx=UP, fy=UP, interpolation=cv2.INTER_CUBIC)
    t, h = _template(rad, lw)
    best = cv2.matchTemplate(gu, t, cv2.TM_CCOEFF_NORMED)
    s, s0 = int(round(1.5 * (rad + lw / 2) * UP)), UP
    out = []
    offs = np.arange(-1.0, 1.01, 0.5)
    while True:
        y, x = np.unravel_index(best.argmax(), best.shape)
        if best[y, x] < MATCH_MIN:
            break
        cx, cy = (x + h + 0.5) / UP - 0.5, (y + h + 0.5) / UP - 0.5
        hits = []
        if x_min < cx and y_min < cy < y_max:
            hits = [(cx + dx, cy + dy) for dx in offs for dy in offs if _is_marker(g, cx + dx, cy + dy, rad)]
        if hits:
            out.append((float(np.mean([p for p, _ in hits])), float(np.mean([q for _, q in hits]))))
            best[max(0, y - s):y + s, max(0, x - s):x + s] = -1
        else:
            best[max(0, y - s0):y + s0, max(0, x - s0):x + s0] = -1
    return out


def _foot(xx, yy, cx, cy, grow=0.0, half=HALF):
    return np.hypot(xx - cx, yy - cy) <= half + grow


def _fill_kind(rgb):
    r, g_, b = (float(v) for v in rgb)
    if max(r, g_, b) - min(r, g_, b) < 20:
        return "light grey" if r > 160 else "dark grey"
    return "red" if r > b else "blue"


def read_bars(fig, tick_values, labels, tick_min=3, bars=BARS, fills=FILL, find_spans=None, margin=8, cap_reach=14,
              cap_min_cols=CAP_MIN_COLS, cap_half=CAP_HALF, ring=(R, LW), cap_join_rows=0):
    """Read the five bars; tick_values are the printed tick labels top to bottom, labels maps returned label -> bar;
    tick_min is passed to _axis (shorter tick marks need 2). Panels with other bars (Fig. 7D: 14 narrow bars) pass
    bars and fills, find_spans(g, col, ticks, base, sat) -> [(x0, x1)], the columns beside a bar in which its markers may
    lie (margin), and the cap's reach either side of the whisker (cap_reach for finding it, cap_half for taking it out
    of the hidden-marker test) with the free columns a cap row needs (cap_min_cols), the markers' ring radius and
    line width (ring), and the rows just below an upper cap that must all be whisker or marker (cap_join_rows: a row
    of significance asterisks, a few px above the top marker, otherwise passes for a cap on narrow bars)."""
    rad, lw = ring
    half = rad + lw / 2
    img, scale = fig.render(DPI)
    g = img.astype(np.float32).mean(2)
    sat = img.max(2).astype(int) - img.min(2).astype(int)
    col, ticks = _axis(g, tick_min)
    if len(ticks) != len(tick_values):
        raise ValueError(f"{len(ticks)} ticks found, {len(tick_values)} labels")
    cal = calibrate(list(zip(ticks, tick_values)))
    unc = RASTER_UNCERTAINTY_PX_300DPI + cal.residual / abs(cal.slope)
    base = int(round(ticks[-1]))

    if find_spans is None:
        row = g[base - 2, col + 3:]
        spans = [(a + col + 3, b + col + 3) for a, b in _runs(row < 235) if b - a >= 25]
    else:
        spans = find_spans(g, col, ticks, base, sat)
    if len(spans) != len(bars):
        raise ValueError(f"{len(spans)} bars found, {len(bars)} expected")

    # markers are dark outlines on the bar's colour: found on the brightest channel, in which the red and blue fills
    # stay light and the outline stays dark
    gm = img.max(2).astype(np.float32)
    found = _markers(gm, col + 3, ticks[0] - 2, base - 2, rad, lw)
    yy, xx = np.mgrid[:g.shape[0], :g.shape[1]]
    disc = np.zeros(g.shape, bool)
    for cx, cy in found:
        disc |= _foot(xx, yy, cx, cy, 1.0, half)
    outline = (g < 90) & (sat < 60)
    marks = gm < 90                # dark outline pixels whatever the fill, for the hidden-marker test
    dk = (g < 200) & (sat < 60)

    res = {}
    for grp, kind, (x0, x1) in zip(bars, fills, spans):
        mid = (x0 + x1) // 2
        # whisker: the column near the span centre that is darkest on average from the top tick to the baseline, off
        # markers (in Fig. 5H the whisker above the bar is a mid grey, lighter than the outline threshold F5C used)
        win = np.where(disc[int(ticks[0]):base - 3, mid - 6:mid + 7], np.nan, g[int(ticks[0]):base - 3, mid - 6:mid + 7])
        xc = float(mid - 6 + int(np.nanargmin(np.nanmean(win, 0))))
        # bar top: the highest row from which every row down to the baseline is non-white across 90% of the interior
        # away from the whisker; the outline row is the darkest row there on the interior columns with no marker
        inner = [x for x in range(x0 + 3, x1 - 2) if abs(x - xc) > 2]
        solid = (g[:, inner] < 235).mean(1) >= 0.9
        top = base - 2
        while top > 0 and solid[top - 1]:
            top -= 1
        cols = [x for x in inner if not disc[max(0, top - 2):top + 4, x].any()]
        # the fill is sampled off the marker footprints, on the brighter half of those pixels (in a low bar the
        # outlines of markers not found can be half of them); a bar too low to hold fill rows between its outline and
        # the baseline is not checked
        fsel = ~disc[top + 3:base - 3][:, cols or inner]
        if fsel.sum() >= 10:
            bar_fill = img[top + 3:base - 3][:, cols or inner][fsel]
            bright = bar_fill.max(1)
            bar_fill = bar_fill[bright >= np.median(bright)]
            if _fill_kind(np.median(bar_fill, 0)) != kind:
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

        mine = sorted([e for e in found if x0 - margin <= e[0] <= x1 + margin], key=lambda e: e[1])
        apart = all(np.hypot(a[0] - b[0], a[1] - b[1]) > 2 * half for i, a in enumerate(mine) for b in mine[i + 1:])

        capcols = [x for x in range(int(xc) - cap_reach, int(xc) + cap_reach + 1) if abs(x - xc) >= 2.5]

        def free(y):
            return [x for x in capcols if not disc[y, x]]

        def lines(mask, y0, y1):
            """Runs of rows in [y0, y1) dark across 80% of the free cap columns: horizontal cap lines."""
            rows = [len(free(y)) >= cap_min_cols and mask[y, free(y)].mean() >= 0.8 for y in range(y0, y1)]
            return [(a + y0, b + y0) for a, b in _runs(rows)]

        # caps inside the bar are dark on the fill (brightest channel); the upper cap is a thin grey line on white
        # above the bar top
        fill_m = float(np.median(gm[top + 3:base - 3][:, cols or inner]))
        caps = lines(marks, 0, base - 3) + lines(gm < fill_m - CAP_FILL_MIN, top + 2, base - 3) + lines(dk, 0, top - 2)
        cap = None
        for a, b in sorted(lines(dk, 0, top - 2)):
            # joined to the bar top by the whisker (dark or under a marker on 80% of the rows between)
            seg = range(b + 1, top - 1)
            joined = [(g[y, int(xc) - 1:int(xc) + 2] < 200).any() or disc[y, int(xc)] for y in seg]
            if (not joined or np.mean(joined) >= 0.8) and all(joined[:cap_join_rows]):
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
            r_ = marks.copy()
            r_[disc] = False
            r_[:, :x0 - margin] = False
            r_[:, x1 + margin + 1:] = False
            r_[base - 3:] = False
            r_[:int(min(e[1] for e in mine)) - 8] = False
            r_[int(max(e[1] for e in mine)) + 8:] = False
            r_[:, int(xc) - 1:int(xc) + 2] = False
            r_[:, x0 - 1:x0 + 2] = False
            r_[:, x1 - 1:x1 + 2] = False
            r_[top - 1:top + 3] = False
            for a, b in caps:
                r_[a - 1:b + 2, int(xc) - cap_half - 2:int(xc) + cap_half + 3] = False   # the cap's full width
            left = int(r_.sum())
        countable = bool(mine) and apart and left <= RESIDUAL_MAX
        pts = [point(cal, cy, unc, fig.to_page(cx + 0.5, cy + 0.5, scale)) for cx, cy in mine]
        res[grp] = {"points": pts if countable else [], "countable": countable, "bar": bar}
    return {"groups": {label: res[grp] for label, grp in labels.items()}}


# Fig. 6H (EHT force bars): the same five bars, with one marker per EHT in four shapes (circle, square, triangle,
# diamond: one per biological replicate), dark outline and bar-coloured fill, about 9 px across at 300 dpi.
SHAPE_DARK = 0.2        # a pixel is outline when its brightest channel is below its background (fill or white) by
SHAPE_DARK_MIN = 10     # 0.2 x the background, and at least by 10 grey levels. The dark grey fill renders at 106 and
                        # its marker outlines at about 92-98, so markers inside the LCFA bar are mostly missed; the
                        # count test below then makes that bar not countable.
SHAPE_TEXT_MAX = 80     # a blob whose median brightest channel is below this is solid black: an asterisk, not a marker
SHAPE_HOLE_MAX = 60     # enclosed light regions up to this area (px) are marker interiors
SHAPE_OPEN = 5          # opening with a 5 px disc takes out whisker, caps and bar edges (2-3 px) and keeps markers
SHAPE_AREA = (25, 95)   # one opened marker (about 8-10 px across); larger blobs are markers that touch or overlap
SHAPE_SPAN_MAX = 11     # nor may one marker's opened blob be wider or taller than this (px)


def shape_markers(img, x0, x1, top, base, y_min, fill_m):
    """Markers of one bar in its column (x0 - 12 .. x1 + 12, rows y_min .. base - 3): pixels darker than their
    background (the bar fill inside the bar, white elsewhere; above the bar a marker's bar-coloured fill is itself
    darker than white, inside it only the outline is), plus small enclosed light regions (marker interiors), opened
    with a 5 px disc so that lines go and marker bodies stay. Each blob is one marker, centred on the middle of its
    extent. Returns [(x, y, w, h, area)] in image px."""
    gm = img.max(2).astype(np.float32)
    xa, xb, ya, yb = max(0, x0 - 12), x1 + 13, int(y_min), base - 3
    sub = gm[ya:yb, xa:xb]
    bg = np.full(sub.shape, 255.0, np.float32)
    bg[max(0, top - ya):, x0 - xa:x1 + 1 - xa] = fill_m
    dark = sub < bg - np.maximum(SHAPE_DARK_MIN, SHAPE_DARK * bg)
    n, lab, st, _ = cv2.connectedComponentsWithStats((~dark).astype(np.uint8), connectivity=4)
    u = dark.copy()
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if a <= SHAPE_HOLE_MAX and x > 0 and y > 0 and x + w < sub.shape[1] and y + h < sub.shape[0]:
            u |= lab == i
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (SHAPE_OPEN, SHAPE_OPEN))
    op = cv2.morphologyEx(u.astype(np.uint8), cv2.MORPH_OPEN, k)
    n, lab, st, _ = cv2.connectedComponentsWithStats(op, connectivity=8)
    out = []
    for i in range(1, n):
        x, y, w, h, a = (int(v) for v in st[i])
        if float(np.median(sub[lab == i])) < SHAPE_TEXT_MAX:
            continue
        out.append((xa + x + (w - 1) / 2, ya + y + (h - 1) / 2, w, h, a))
    return out, (xa, ya, dark, u, op)


def read_shape_bars(fig, tick_values, labels, n_markers, tick_min=2, debug=False):
    """Bars (mean, upper SD cap) as read_bars reads them; points are shape_markers. A bar's markers are countable
    when every blob is one marker (area within SHAPE_AREA, span at most SHAPE_SPAN_MAX: markers that touch each other
    or overlap make one larger blob) and there are n_markers of them (the legend's n x EHTs per replicate), so that
    no marker is hidden or missed. Otherwise the bar gives the bar only. Fig. 6H's tick marks are 3-4 px long and the
    rendered axis is two columns wide, so tick_min is 2."""
    bars = read_bars(fig, tick_values, {b: b for b in BARS}, tick_min)["groups"]
    img, scale = fig.render(DPI)
    g = img.astype(np.float32).mean(2)
    col, ticks = _axis(g, tick_min)
    cal = calibrate(list(zip(ticks, tick_values)))
    unc = RASTER_UNCERTAINTY_PX_300DPI + cal.residual / abs(cal.slope)
    base = int(round(ticks[-1]))
    row = g[base - 2, col + 3:]
    spans = [(a + col + 3, b + col + 3) for a, b in _runs(row < 235) if b - a >= 25]
    res, dbg = {}, {}
    for grp, (x0, x1) in zip(BARS, spans):
        inner = list(range(x0 + 3, x1 - 2))
        solid = (g[:, inner] < 235).mean(1) >= 0.6
        top = base - 2
        while top > 0 and solid[top - 1]:
            top -= 1
        fill_m = float(np.median(img.max(2)[base - 30:base - 5, x0 + 5:x1 - 4]))
        found, masks = shape_markers(img, x0, x1, top, base, ticks[0] - 2, fill_m)
        found = sorted(found, key=lambda e: e[1])
        single = all(SHAPE_AREA[0] <= a <= SHAPE_AREA[1] and max(w, h) <= SHAPE_SPAN_MAX for _, _, w, h, a in found)
        countable = single and len(found) == n_markers
        pts = [point(cal, cy, unc, fig.to_page(cx + 0.5, cy + 0.5, scale)) for cx, cy, _, _, _ in found]
        res[grp] = {"points": pts if countable else [], "countable": countable, "bar": bars[grp]["bar"]}
        dbg[grp] = (found, masks, top, single)
    out = {"groups": {label: res[grp] for label, grp in labels.items()}}
    return (out, dbg, img) if debug else out


# Fig. 7D (RNA-seq reads of eight FAO genes): 14 narrow bars (about 21 px at 300 dpi, 6 px apart) in four sets split
# by grey dashed lines: 2D (Control, LCFA, GW0742, LCFA + GW0742, GSK0660), EHT and Lact (Control, LCFA, GW0742,
# LCFA + GW0742) and EB, with the ring markers of figures/F5C.py. Caps reach about 6 px either side of the whisker.
F7D_BARS = ["c2d_control", "c2d_lcfa", "c2d_gw", "c2d_lcfa_gw", "c2d_gsk",
            "eht_control", "eht_lcfa", "eht_gw", "eht_lcfa_gw",
            "lact_control", "lact_lcfa", "lact_gw", "lact_lcfa_gw", "eb"]
F7D_FILL = FILL + FILL[:4] + FILL[:4] + ["light grey"]
DASH_LEN = (8, 14)       # dashes are about 11 px long on a 17 px period (300 dpi)
DASH_RUNS_MIN = 8        # a separator column holds at least this many dash-long runs of non-white above the baseline
BAR_WIDTH_MIN = 12
F7D_RING = (2.9, 1.3)    # these rings are about 7 px across at 300 dpi


def dashed_spans(g, col, ticks, base, sat):
    """Bar spans on the row 2 px above the baseline, once the dashed separator columns (many dash-long runs of
    non-white from the top tick down) are taken out: a bar beside a separator otherwise joins it into one span."""
    band = (g < 235)[int(ticks[0]):base - 3]
    nruns = np.array([sum(DASH_LEN[0] <= b - a + 1 <= DASH_LEN[1] for a, b in _runs(band[:, x]))
                      for x in range(g.shape[1])])
    row = g[base - 2] < 235
    row[:col + 3] = False
    sep = nruns >= DASH_RUNS_MIN
    row[np.convolve(sep, np.ones(3), "same") > 0] = False
    return [(a, b) for a, b in _runs(row) if b - a >= BAR_WIDTH_MIN]


def read_f7d(fig, tick_values, item, n_min=3):
    """One Fig. 7D gene panel; labels are '<item>/<group>' for the 14 bars. The hidden-marker test of read_bars only
    looks between the highest and lowest marker found, so a bar whose other markers sit on the baseline or in the bar
    outline could pass with one; a bar is countable only if it also shows at least the legend's n = 3 markers (some
    2D bars show four, which are kept and logged)."""
    out = read_bars(fig, tick_values, {f"{item}/{b}": b for b in F7D_BARS}, bars=F7D_BARS, fills=F7D_FILL,
                    find_spans=dashed_spans, margin=3, cap_reach=5, cap_min_cols=4, cap_half=6, ring=F7D_RING,
                    cap_join_rows=6)
    for r in out["groups"].values():
        if len(r["points"]) < n_min:
            r["points"], r["countable"] = [], False
    return out
