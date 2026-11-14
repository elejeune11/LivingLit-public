"""Fig. 1H (journal_version.pdf p. 4): SIRPA+CD90- hPSC-CMs at day 35, normalised to control (%), five bars (Control,
GW6471, GSK0660, GW9662, All Antag.), mean ± SD with black filled markers (circle, diamond, square, triangle and a
second circle: one marker per biological replicate). Raster (the page figure is one 300 dpi image). Read the same
way as Fig. 1G (figures/F1G.py), with this panel's ticks, labels and marker count.

The y axis column and its tick marks are found in the image (tick values are the printed labels 125, 100, ..., 0).
Bars are the five non-white spans just above the baseline. Markers: black pixels opened with a 3x3 square, which
removes the 1-2 px lines they sit on (the control bar's top outline, error-bar whiskers and caps) and keeps the
6-8 px markers; a marker's value is its box centre. The opening trims the 1-2 px apex of a triangle, so a
triangle's box centre may sit up to half a pixel low (within the interval). Bar mean: the darkness centroid of the
bar's top outline (against white above, the fill below) over columns free of markers. Error: the upper cap, the first row above the bar top that is dark
across the whisker's cap columns (markers masked out).
"""
import numpy as np
import cv2

from livinglit.figures.source import calibrate, point, RASTER_UNCERTAINTY_PX_300DPI

DPI = 300
TICK_VALUES = [125, 100, 75, 50, 25, 0]    # printed tick labels, top to bottom
BARS = ["control", "gw6471", "gsk", "gw9662", "all_antag"]
# label returned -> bar read
LABELS = {
    "F1H_gw6471/gw6471": "gw6471",
    "F1H_gw6471/control": "control",
}
N_MARKERS = 5                      # five markers on the control bar: biological replicates
CAP_MIN_PX = 15                    # caps are about 25 px wide at 300 dpi, markers at most 8


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
    span = g[:, col - 7:col - 2]
    ticks = []
    for a, b in _runs((span < 200).sum(1) >= 4):
        idx = np.arange(a - 1, b + 2)
        d = 255 - span[idx].mean(1)
        ticks.append(float((idx * d).sum() / d.sum()))
    return col, ticks


def _marker(black, upright, sx, sy):
    """A marker's box (x0, x1, y0, y1 in px) grown from a seed in the black mask. A row belongs to the marker when
    it holds at least two black pixels within the marker's width that are not part of a long upright line (a bar
    edge or a whisker); rows where black runs on past both sides (a cap or a bar outline crossing the marker) are
    bridged but never end it. Columns: the black run through the seed's row."""
    cx, cy = int(round(sx)), int(round(sy))
    win = (black & ~upright)[:, cx - 4:cx + 5]

    def crossing(y):
        return black[y, cx - 7] and black[y, cx + 7]

    def part(y):
        return win[y].sum() >= 2 and not crossing(y)

    if not part(cy) and not crossing(cy):
        return None
    ends = []
    for step in (-1, 1):
        y = cy
        while True:
            if part(y + step):
                y += step
            elif crossing(y + step) and part(y + 2 * step):
                y += 2 * step
            else:
                break
        ends.append(y)
    row = black[cy, cx - 6:cx + 7]
    xs = [cx - 6 + i for i, b in enumerate(row) if b]
    return (min(xs), max(xs), ends[0], ends[1]) if xs else None


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

    black = (g < 110) & (sat < 60)
    # marker seeds: what survives a 3x3 opening (lines of 1-2 px do not), marker-sized
    opened = cv2.morphologyEx(black.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, _, stats, cents = cv2.connectedComponentsWithStats(opened, connectivity=8)
    seeds = [(float(cents[i][0]), float(cents[i][1])) for i in range(1, n)
             if stats[i, cv2.CC_STAT_AREA] >= 9 and stats[i, cv2.CC_STAT_WIDTH] <= 11
             and stats[i, cv2.CC_STAT_HEIGHT] <= 11]
    upright = cv2.morphologyEx(black.astype(np.uint8), cv2.MORPH_OPEN, np.ones((12, 1), np.uint8)).astype(bool)
    markers = [m for m in (_marker(black, upright, sx, sy) for sx, sy in seeds) if m is not None]
    marker_mask = np.zeros_like(black)
    for x0, x1, y0, y1 in markers:
        marker_mask[y0 - 2:y1 + 3, x0 - 2:x1 + 3] = True

    res = {}
    for grp, (x0, x1) in zip(BARS, spans):
        if grp not in LABELS.values():
            continue
        xc = (x0 + x1) / 2
        # bar top: per marker-free interior column, the top of the non-white run rising from the baseline;
        # the outline by darkness
        cols = [x for x in range(x0 + 3, x1 - 2) if abs(x - xc) > 3 and not marker_mask[:, x].any()]
        tops = []
        for x in cols:
            y = base - 2
            while y > 0 and g[y - 1, x] < 235:
                y -= 1
            tops.append(y)
        top = int(np.median(tops))
        # the outline's darkness against its own background: white above its darkest row, the fill below
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
        # upper cap: the first row above the bar top whose dark run through the whisker is cap-wide (markers are
        # at most 8 px, so they cannot make one, even when they sit on the cap and cover most of it); its row
        # and the next are weighted by the median darkness over the cap columns (robust to marker pixels)
        capcols = [x for x in range(int(xc) - 11, int(xc) + 13) if abs(x - xc) >= 4.5]
        dk = (g < 200) & (sat < 60)

        def run_through(y):
            a = b = int(round(xc))
            if not dk[y, a]:
                return 0
            while dk[y, a - 1]:
                a -= 1
            while dk[y, b + 1]:
                b += 1
            return b - a + 1

        cap = None
        for y in range(top - 3, 0, -1):
            if run_through(y) >= CAP_MIN_PX:
                ii = np.array([r for r in range(y - 2, y + 3) if run_through(r) >= CAP_MIN_PX])
                ww = np.clip(200 - np.median(g[ii][:, capcols], 1), 0, None)
                cap = float((ii * ww).sum() / ww.sum())
                break
            if y < top - 12 and not (g[y, int(xc) - 1:int(xc) + 2] < 220).any():
                break  # no whisker: no error bar
        if cap is not None:
            bar["error"] = [cal.value(cap), *cal.interval(cap, unc)]
        bar = {k: [v[0], min(v[1], v[0]), max(v[2], v[0])] for k, v in bar.items()}
        # a replicate of n lies at most (n-1)/sqrt(n) SD from the mean: marks higher up are not markers;
        # one marker height of slack
        k_sd = (N_MARKERS - 1) / N_MARKERS ** 0.5
        highest = bar_row - k_sd * (bar_row - cap if cap is not None else 0) - 8
        mine = [m for m in markers if x0 - 4 <= (m[0] + m[1]) / 2 <= x1 + 4 and highest <= (m[2] + m[3]) / 2 < base]
        pts = [point(cal, (y0 + y1) / 2, unc, fig.to_page((mx0 + mx1 + 1) / 2, (y0 + y1 + 1) / 2, scale))
               for mx0, mx1, y0, y1 in sorted(mine, key=lambda m: m[2])]
        res[grp] = {"points": pts, "countable": len(pts) == N_MARKERS, "bar": bar}
    return {"groups": {label: res[grp] for label, grp in LABELS.items()}}
