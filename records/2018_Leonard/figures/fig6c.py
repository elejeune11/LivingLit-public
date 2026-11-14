"""Fig. 6C (journal version, p. 8), lower panel: raster bar-and-scatter plot of the western-blot ratio βMHC / αMHC
("Protein Ratio Relative to EHTs at Day 1"), groups Day1, UL, K1–K4.

The whole of Fig. 6 is one embedded image (~300 dpi); the crop holds the ratio plot only (not the blots).
Each group is a light grey bar (mean), coloured markers (one per EHT, legend) and two black horizontal
caps joined by a short vertical line (legend: "error bars represent S.E.M."). The K1 markers are stacked
on each other and over the caps, and K4 markers touch the upper cap, so no group is countable: only the
caps are read. The mean is the midpoint of the two caps; "error" is the upper cap. Coloured markers carry
almost no ink on the black-ink scale (their brightest channel is high), so the caps stand out. The
significance line above K1–K4 is a thin line and is dropped by its summed ink.

The plot is boxed. Its y axis is calibrated from the dark marks on the band just inside the left axis
line (frame top and bottom lines and the tick marks between), matched top-down to the printed tick
labels (the frame top is unlabelled and not used). Group centres are the centres of the light grey bars
on a row just above the bottom axis line; the Day1 bar (≈1) is too short to reach that row, so the bars
found there are UL, K1, K2, K3, K4 in printed order. Only K1 and K4 are read (the record's F6C item).
"""
import numpy as np

from livinglit.figures.source import calibrate, point

DPI = 300
PX_UNC = 0.6
FRAME = (60, 493, 14, 288)  # approximate frame in px of the 300 dpi crop render: x0, x1, y0, y1
LABELS = [None, 50, 40, 30, 20, 10, 0]  # marks on the left axis, top-down; None = unlabelled frame top
BARS = ["UL", "K1", "K2", "K3", "K4"]  # grey bars found just above the bottom axis line (Day1 is too short)
ITEMS = [("F6C_ratio_K4vK1", ["K4", "K1"])]
MIN_CAP_INK = 3.0  # summed ink across a band's rows: caps ~3–4, significance line ~1.8
CAP_IN, CAP_OUT = 13, 18  # columns from the group centre used to see the caps beside the markers (caps reach ±17)


def _refine(dark, approx, span):
    """The darkest column within ±4 px of an approximate frame edge."""
    lo, hi = span
    best = None
    for p in range(max(approx - 4, 0), min(approx + 5, dark.shape[1])):
        v = dark[lo:hi, p].mean()
        if best is None or v > best[0]:
            best = (v, p)
    return best[1]


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


def _ticks(ink, x0, y0, y1):
    """(row, value) for the marks on the band just inside the left axis line, matched top-down to LABELS."""
    band = ink[:, x0 + 2:x0 + 4].mean(axis=1)
    cents = sorted(_centroids(band, _clusters(band, range(y0 - 5, y1 + 6), 0.3)))
    if len(cents) != len(LABELS):
        raise ValueError(f"found {len(cents)} axis marks for {len(LABELS)} labels")
    return [(c, v) for c, v in zip(cents, LABELS) if v is not None]


def _group_centres(img, x0, x1, y1):
    """Centres of the light grey bars on a row just above the bottom axis line, left to right."""
    row = img[y1 - 8, x0 + 3:x1 - 2].astype(int)
    hi, lo = row.max(axis=1), row.min(axis=1)
    grey = ((hi > 180) & (hi < 245) & (hi - lo < 15)).astype(float)
    runs = [c for c in _clusters(grey, range(len(grey)), 0.5) if len(c) >= 10]
    if len(runs) != len(BARS):
        raise ValueError(f"found {len(runs)} grey bars for {len(BARS)} groups")
    return [x0 + 3 + (c[0] + c[-1]) / 2 for c in runs]


def _caps(ink, c, y0, y1):
    """Ink-weighted horizontal bands at the outer ends of a group's caps: (centroid row, summed ink)."""
    left = np.median(ink[:, c - CAP_OUT:c - CAP_IN + 1], axis=1)
    right = np.median(ink[:, c + CAP_IN:c + CAP_OUT + 1], axis=1)
    prof = np.maximum(left, right)
    bands = []
    for cl in _clusters(prof, range(y0 + 4, y1 - 3), 0.5):
        rows = range(cl[0] - 1, cl[-1] + 2)
        w = sum(prof[y] for y in rows)
        if w >= MIN_CAP_INK:
            bands.append((sum(y * prof[y] for y in rows) / w, w))
    return bands


def read(fig):
    img, scale = fig.render(DPI)
    ink = np.clip(1 - img.astype(int).max(axis=2) / 235.0, 0, 1)  # black ~1; grey bars, background, markers low
    x0, x1, y0, y1 = FRAME
    x0 = _refine(ink, x0, (y0 + 10, y1 - 10))
    x1 = _refine(ink, x1, (y0 + 10, y1 - 10))
    y0 = _refine(ink.T, y0, (x0 + 10, x1 - 10))
    y1 = _refine(ink.T, y1, (x0 + 10, x1 - 10))
    cal = calibrate(_ticks(ink, x0, y0, y1))
    res = cal.residual
    bars = {}
    needed = {g for _, gs in ITEMS for g in gs}
    for g, cx in zip(BARS, _group_centres(img, x0, x1, y1)):
        if g not in needed:
            continue
        bands = _caps(ink, round(cx), y0, y1)
        if len(bands) != 2:
            raise ValueError(f"{g}: {len(bands)} cap bands")
        (up, _), (low, _) = sorted(bands)
        mid = (up + low) / 2
        mean = point(cal, mid, PX_UNC, fig.to_page(cx, mid, scale))
        err = point(cal, up, PX_UNC, fig.to_page(cx, up, scale))
        bars[g] = {"mean": [mean["value"], mean["lo"] - res, mean["hi"] + res],
                   "error": [err["value"], err["lo"] - res, err["hi"] + res]}
    out = {}
    for item, gs in ITEMS:
        for g in gs:
            out[f"{item}/{g}"] = {"points": [], "countable": False, "bar": bars[g]}
    return {"groups": out}
