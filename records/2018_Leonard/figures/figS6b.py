"""Fig. S6B (supplement 2, p. 4): four raster histograms of individual cell areas, K1–K4, left to right.

Each panel is a MATLAB grouped bar chart: x = cell area (μm²), 0–250; y = count, 0–15+. Every area bin
holds one bar per EHT (legend: EHT 1–5 for K1 and K4, EHT 1–6 for K2 and K3), side by side in legend
order and coloured as in the legend. The image is embedded at ~444 dpi and rendered at that resolution.

Counts: bar heights sit on whole counts (1 count ≈ 28 px); a bar's count is its height rounded, and a
height more than 0.25 count from a whole number stops the reading. Bars are side by side, never on top
of one another, and adjacent bars in a bin are different EHTs (different legend hues), so each bar is
read on its own and the groups are countable. Each cell is returned as one point whose value is its bin
centre and whose interval is the bin (centre ± half the bin spacing) plus the x calibration misfit: a
histogram gives each area only to within its bin. Cells of all EHTs of a group are pooled into that
group (the record's n counts tissues, 5–6 per group).

Columns: each column's coloured fill is followed up from the bottom frame line; its top (one px of
outline above) gives the height, its hue just under the top the legend EHT of nearest hue (legend hues
are taken from the panel's own legend swatches; bars are darker than the swatches, so only hue is
compared). Grey edge shading, outlines and edge columns mixing two fills (low saturation, or a hue
outside the legend hue's tolerance) are skipped.

Bins and bars: bar groups lie on a regular lattice (spacing P, centre c0); P and c0 are fitted per panel
so that each fill column falls in the slot of its EHT (equal slots across a group width g·P, g fitted
too), and a column belongs to the nearest bin centre. Within a bin, the fill columns of one EHT form one
bar, whose height is its tallest column (edge columns show a lower fill top); EHTs out of legend order
within a bin stop the reading. Axes: x from the frame's left (0) and right (250) lines and the four tick
marks inside the top frame line (50–200); y from the bottom frame line (0) and the three tick marks
inside the left frame line (5, 10, 15). Ticks are matched to the printed labels by order.
"""
import colorsys

import numpy as np

from livinglit.figures.source import calibrate

DPI = 444
# left to right: group, EHTs in the legend, approximate frame in px of the crop render (x0, x1, y0, y1)
PANELS = [
    ("K1", 5, (229, 817, 38, 539)),
    ("K2", 6, (976, 1569, 32, 529)),
    ("K3", 6, (1743, 2333, 27, 533)),
    ("K4", 5, (2497, 3088, 30, 536)),
]
X_TICKS = [50, 100, 150, 200]
X_FRAME = (0, 250)
Y_TICKS = [15, 10, 5]
ITEM = "S6_area"
SAT = 35        # a fill column's colour spread (max - min channel); outlines and grey edges are below
MIN_S = 0.45    # HSV saturation of a fill column near its top; edge columns mixed with outline are below
HUE_TOL = (3.0, 20.0)  # bounds of the hue tolerance in degrees (K1/K4 olive and yellow are 5 apart)


def ycal_row(cal, value):
    """Pixel row of an axis value (inverse of a linear calibration)."""
    return (value - cal.intercept) / cal.slope


def _clusters(profile, idx, thr):
    out = []
    for i in idx:
        if profile[i] > thr:
            if out and i - out[-1][-1] <= 1:
                out[-1].append(i)
            else:
                out.append([i])
    return out


def _centroids(profile, clusters):
    return [sum(i * profile[i] for i in c) / sum(profile[i] for i in c) for c in clusters]


def _line(profile, approx):
    """Centroid of the dark line within ±5 px of an approximate frame position."""
    cl = [c for c in _clusters(profile, range(approx - 5, approx + 6), 0.6)]
    if len(cl) != 1:
        raise ValueError(f"frame line near {approx}: {len(cl)} candidates")
    lo, hi = cl[0][0] - 1, cl[0][-1] + 1
    return _centroids(profile, [list(range(lo, hi + 1))])[0]


def _legend(img, x0, x1, m):
    """Mean colour of the m legend swatches (the most saturated column in the panel's right part)."""
    sat = img.max(axis=2) - img.min(axis=2)
    cols = range(x0 + int(0.55 * (x1 - x0)), x1 - 20)
    cc = max(cols, key=lambda c: int((sat[45:330, c] > 60).sum()))
    runs = _clusters(sat[:, cc].astype(float), range(40, 340), 60)
    if len(runs) != m:
        raise ValueError(f"legend: {len(runs)} swatches for {m} EHTs")
    return np.array([np.median(img[r[2]:r[-2], cc - 5:cc + 5].reshape(-1, 3), axis=0) for r in runs], float)


def _hue(rgb):
    """Hue in degrees (the bars are darker than their legend swatches, so only hue is compared)."""
    return colorsys.rgb_to_hsv(*(np.asarray(rgb, float) / 255.0))[0] * 360.0


def _hdist(a, b):
    return min(abs(a - b), 360 - abs(a - b))


def _nearest(hue, swatch_hues):
    """Index of the nearest legend hue if within its tolerance (half the gap to the next legend hue,
    3–20 degrees), else None: an edge column mixing two fills or a fill and an outline."""
    d = [_hdist(hue, h) for h in swatch_hues]
    k = int(np.argmin(d))
    gap = min(_hdist(swatch_hues[k], h) for i, h in enumerate(swatch_hues) if i != k)
    return k if d[k] <= min(max(gap / 2, HUE_TOL[0]), HUE_TOL[1]) else None


def _fit_lattice(cols, cls, m):
    """(P, c0, g) maximising columns whose predicted slot is the EHT of their colour; gap columns count against."""
    best = None
    cols = np.asarray(cols, float)[None, :]
    for P, g in ((P, g) for P in np.arange(12.0, 40.0, 0.02) for g in np.arange(0.70, 0.96, 0.01)):
        s = g * P / m
        c0 = np.arange(0.0, P, 0.1)[:, None]
        u = (cols - c0) / P
        off = (u - np.round(u)) * P + g * P / 2  # px from the group's left edge
        k = np.clip(np.floor(off / s), 0, m - 1)
        inside = (off >= -1) & (off <= g * P + 1)
        score = ((k == cls[None, :]) & inside).sum(axis=1) - 3 * (~inside).sum(axis=1)
        i = int(np.argmax(score))
        if best is None or score[i] > best[0]:
            best = (int(score[i]), float(P), float(c0[i, 0]), float(g))
    return best[1], best[2], best[3]


def read(fig):
    img, scale = fig.render(DPI)
    img = img.astype(int)
    dark = 1 - img.max(axis=2) / 255.0  # black frame ~0.85
    out = {}
    for group, m, (ax0, ax1, ay0, ay1) in PANELS:
        mid_rows = slice(ay0 + 60, ay1 - 60)
        x0 = _line(dark[mid_rows, :].mean(axis=0), ax0)
        x1 = _line(dark[mid_rows, :].mean(axis=0), ax1)
        xin = slice(int(x0) + 8, int(x1) - 8)
        y0 = _line(dark[:, xin].mean(axis=1), ay0)
        y1 = _line(dark[:, xin].mean(axis=1), ay1)

        yt = _centroids(*(lambda p: (p, _clusters(p, range(int(y0) + 5, int(y1) - 4), 0.3)))(
            dark[:, int(x0) + 3:int(x0) + 7].mean(axis=1)))
        if len(yt) != len(Y_TICKS):
            raise ValueError(f"{group}: {len(yt)} y tick marks")
        ycal = calibrate(list(zip(yt, Y_TICKS)) + [(y1, 0)])
        xt = _centroids(*(lambda p: (p, _clusters(p, range(int(x0) + 5, int(x1) - 4), 0.3)))(
            dark[int(y0) + 3:int(y0) + 8, :].mean(axis=0)))
        if len(xt) != len(X_TICKS):
            raise ValueError(f"{group}: {len(xt)} x tick marks")
        xcal = calibrate(list(zip(xt, X_TICKS)) + [(x0, X_FRAME[0]), (x1, X_FRAME[1])])

        # each column's coloured fill, from the bottom frame line up: its top gives the height (one px of
        # outline above it), its hue near the top the legend EHT of nearest hue; columns without fill
        # (outlines, grey edges, background) are skipped
        swatch = [_hue(rgb) for rgb in _legend(img, int(x0), int(x1), m)]
        sat = img.max(axis=2) - img.min(axis=2)
        base = int(round(y1)) - 3
        heights, cls = {}, {}
        for c in range(int(x0) + 4, int(x1) - 3):
            if sat[base, c] <= SAT:
                continue
            r = base
            while r > y0 + 3 and sat[r, c] > SAT:
                r -= 1
            top = r + 1
            rgb = np.median(img[top:min(top + 10, base), c], axis=0)
            if colorsys.rgb_to_hsv(*(rgb / 255.0))[1] < MIN_S:
                continue  # an edge column, fill mixed with outline: its hue is not reliable
            k = _nearest(_hue(rgb), swatch)
            if k is None:
                continue
            heights[c] = (ycal.value(top - 1.0), top)
            cls[c] = k
        cols = sorted(heights)

        # bins: a regular lattice fitted to the fill columns; a column belongs to the nearest bin centre
        P, c0, _ = _fit_lattice(cols, np.array([cls[c] for c in cols]), m)

        # bars: within a bin, the fill columns of one EHT, which must form one block (only edge columns
        # between) and come in legend order; a bar's height is its tallest fill column (edge columns
        # mixed with a neighbour's outline show a lower fill top)
        bars = []
        for c in cols:
            j, k = int(round((c - c0) / P)), cls[c]
            if bars and bars[-1]["j"] == j and bars[-1]["k"] == k and c - bars[-1]["cols"][-1] <= 2:
                bars[-1]["cols"].append(c)
                bars[-1]["h"].append(heights[c][0])
            else:
                bars.append({"j": j, "k": k, "cols": [c], "h": [heights[c][0]]})
        points, last = [], {}
        for b in bars:
            xc = float(np.mean(b["cols"]))
            h = float(max(b["h"]))
            n = int(round(h))
            if abs(h - n) > 0.25 or n == 0:
                raise ValueError(f"{group}: bar at column {xc:.0f} has height {h:.2f}, not a whole count")
            j = b["j"]
            if j in last and b["k"] <= last[j]:
                raise ValueError(f"{group}: bin {j} has EHT {b['k'] + 1} after EHT {last[j] + 1} (column {xc:.0f})")
            last[j] = b["k"]
            centre = c0 + j * P
            v = xcal.value(centre)
            lo = xcal.value(centre - P / 2) - xcal.residual
            hi = xcal.value(centre + P / 2) + xcal.residual
            for i in range(n):
                yrow = ycal_row(ycal, i + 0.5)
                points.append({"value": v, "lo": lo, "hi": hi, "at": list(fig.to_page(xc, yrow, scale))})
        out[f"{ITEM}/{group}"] = {"points": points, "countable": True}
    return {"groups": out}
