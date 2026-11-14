"""Fig. S8 (supplement 2, p. 5): nine raster bar-and-scatter plots of fold change in gene expression (relative to HPRT,
normalized by EHT Day 1). Row A (Metabolism): GLUT4, CPT1B, TFAM, CKMT2. Row B (Fibrosis Markers): TGFB2, CTGF,
COL5A2, FN1, POSTN. Groups UL, K1–K4 left to right in every plot.

The figure is one embedded image of 400 dpi, rendered at that resolution. Each group is a light grey bar (mean),
coloured markers (one per EHT; K1 blue down-triangles, K2 green circles, K3 red squares, K4 yellow up-triangles) and an
error bar (mean ± S.E.M.) of two black caps joined by a black vertical line. The error bar is drawn over the markers,
with a thin light outline, so it can hide parts of markers.

Bars: the caps reach about ±25 px from the group centre, beyond the markers and the grey bar (both about ±15 px).
A cap is a band of black at both ±18–22 px that is not black at ±29–32 px; this rejects the significance lines of the
CTGF plot, which run on past at least one side of a group. Mean = midpoint of the two caps; error = upper cap. Where
the two caps touch (one band taller than any single cap) the mean is the band's midpoint and the upper cap's centre is
half a cap height (median of the separate caps in the figure) below the band's top, its interval widened by half the
spread of those cap heights.
Group centres are the centres of the grey bars on a row just above the bottom axis line.

Points: a group's markers are the saturated pixels within ±26 px of its centre (the black lines and grey bars are
unsaturated). Where the error bar crosses a marker it splits it, so gaps of up to 12 px that lie wholly on the error bar
(black pixels and their 2 px outline) are bridged between saturated pixels, along rows and along columns. The group is
countable only if every blob has the area of one marker (0.8–1.25 of a reference area: the median of the blobs of the
same colour across the figure that are no larger than 1.5 times that colour's lower-quartile blob area, since most
blobs here are several touching markers and would bias a plain median); a blob of touching markers, or a marker cut short by a cap, makes the group not countable and only its bar
is returned. A marker's position is the centre of its blob's bounding box; for triangles the data point may sit at the
shape's centroid instead, so the interval adds the distance between the two to the pixel uncertainty (0.6 px at
300 dpi = 0.8 px here) and the calibration misfit.

Axes: each plot is boxed; its y axis is calibrated from the dark marks on the band just inside the left axis line
(frame top, inward tick marks, frame bottom), matched top-down to the printed labels. UL is drawn but no S8 item
involves it, so it is not returned.
"""
import numpy as np

from livinglit.figures.source import blobs, calibrate, point

DPI = 400
PX_UNC = 0.6 * DPI / 300
# gene, approximate frame in px of the crop render (x0, x1, y0, y1), left-axis marks top-down
PANELS = [
    ("GLUT4", (128, 538, 77, 450), [3, 2, 1, 0]),
    ("CPT1B", (681, 1107, 77, 450), [0.8, 0.6, 0.4, 0.2, 0]),
    ("TFAM", (1287, 1742, 77, 450), [0.8, 0.6, 0.4, 0.2, 0]),
    ("CKMT2", (1909, 2323, 77, 450), [6, 4, 2, 0]),
    ("TGFB2", (128, 534, 647, 1021), [0.6, 0.4, 0.2, 0]),
    ("CTGF", (688, 1117, 647, 1021), [1.5, 1, 0.5, 0]),
    ("COL5A2", (1287, 1750, 647, 1021), [1.5, 1, 0.5, 0]),
    ("FN1", (1918, 2330, 647, 1021), [2, 1.5, 1, 0.5, 0]),
    ("POSTN", (2503, 2912, 647, 1021), [6, 4, 2, 0]),
]
BARS = ["UL", "K1", "K2", "K3", "K4"]
# returned label -> (gene, group); CTGF items are pairwise contrasts, the others involve K1–K4
LABELS = {f"S8_{g}/{k}": (g, k) for g in ["GLUT4", "CPT1B", "TFAM", "CKMT2", "TGFB2", "COL5A2", "FN1", "POSTN"]
          for k in ["K1", "K2", "K3", "K4"]}
for a, b in [("K4", "K1"), ("K4", "K2"), ("K3", "K1"), ("K3", "K2")]:
    for k in (a, b):
        LABELS[f"S8_CTGF_{a}v{b}/{k}"] = ("CTGF", k)
CAP_IN, CAP_OUT = 18, 22
CAP_END = (29, 32)
WINDOW = 26
SAT = 80
BLACK = 90
GAP = 12
AREA_TOL = (0.8, 1.25)


def _refine(ink, approx, span):
    """The darkest column within ±4 px of an approximate frame edge."""
    lo, hi = span
    return max(range(approx - 4, approx + 5), key=lambda p: ink[lo:hi, p].mean())


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
    out = []
    for c in clusters:
        rows = range(c[0] - 1, c[-1] + 2)
        out.append(sum(i * profile[i] for i in rows) / sum(profile[i] for i in rows))
    return out


def _calibration(ink, x0, y0, y1, labels):
    band = ink[:, x0 + 2:x0 + 5].mean(axis=1)
    cents = sorted(_centroids(band, _clusters(band, range(y0 - 3, y1 + 4), 0.4)))
    if len(cents) != len(labels):
        raise ValueError(f"found {len(cents)} axis marks for {len(labels)} labels")
    return calibrate(list(zip(cents, labels)))


def _group_centres(img, x0, x1, y1):
    row = img[y1 - 8, x0 + 3:x1 - 2]
    hi, lo = row.max(axis=1), row.min(axis=1)
    grey = ((hi > 180) & (hi < 245) & (hi - lo < 15)).astype(float)
    runs = [c for c in _clusters(grey, range(len(grey)), 0.5) if len(c) >= 10]
    if len(runs) != len(BARS):
        raise ValueError(f"found {len(runs)} grey bars for {len(BARS)} groups")
    return [x0 + 3 + (c[0] + c[-1]) / 2 for c in runs]


def _caps(black, c, y0, y1):
    """Row runs of the black bands at ±18–22 px of a group centre that end before ±29–32 px: (first, last, centroid)."""
    def left(a, b):
        return black[:, c - b:c - a + 1].mean(axis=1)

    def right(a, b):
        return black[:, c + a:c + b + 1].mean(axis=1)

    prof = (np.minimum(left(CAP_IN, CAP_OUT), right(CAP_IN, CAP_OUT))
            * (1 - np.maximum(left(*CAP_END), right(*CAP_END))))
    runs = _clusters(prof, range(y0 + 3, y1 - 2), 0.5)
    return [(r[0], r[-1], cy) for r, cy in zip(runs, _centroids(prof, runs))]


def _bridge(mask, occl):
    """Fill runs of up to GAP px lying wholly on the error bar between marked pixels, along each row of the array."""
    out = mask.copy()
    for r in range(mask.shape[0]):
        idx = np.flatnonzero(mask[r])
        for a, b in zip(idx[:-1], idx[1:]):
            if 1 < b - a <= GAP + 1 and occl[r, a + 1:b].all():
                out[r, a + 1:b] = True
    return out


def _dilate(mask, k):
    out = mask.copy()
    for dy in range(-k, k + 1):
        for dx in range(-k, k + 1):
            out |= np.roll(np.roll(mask, dy, axis=0), dx, axis=1)
    return out


def _markers(sat, occl, c, y0, y1):
    """Blobs of saturated pixels in a group's window, bridged across the error bar:
    (x, bounding-box centre row, centroid row, area), in crop px."""
    xa, ya = c - WINDOW, y0 + 2
    sub = sat[ya:y1 - 1, xa:c + WINDOW + 1] > SAT
    oc = occl[ya:y1 - 1, xa:c + WINDOW + 1]
    sub = _bridge(sub, oc)
    sub = _bridge(sub.T, oc.T).T
    out = []
    for b in blobs(sub, min_area=10):
        bx, by, w, h = b["box"]
        out.append({"x": xa + bx + (w - 1) / 2, "y": ya + by + (h - 1) / 2, "cy": ya + b["y"], "area": b["area"]})
    return out


def read(fig):
    img, scale = fig.render(DPI)
    img = img.astype(int)
    ink = np.clip(1 - img.max(axis=2) / 235.0, 0, 1)
    sat = img.max(axis=2) - img.min(axis=2)
    black = img.max(axis=2) < BLACK
    occl = _dilate(black, 2) & (sat <= SAT)
    panels = {}
    for gene, (x0, x1, y0, y1), labels in PANELS:
        x0 = _refine(ink, x0, (y0 + 10, y1 - 10))
        x1 = _refine(ink, x1, (y0 + 10, y1 - 10))
        y0 = _refine(ink.T, y0, (x0 + 10, x1 - 10))
        y1 = _refine(ink.T, y1, (x0 + 10, x1 - 10))
        cal = _calibration(ink, x0, y0, y1, labels)
        centres = dict(zip(BARS, _group_centres(img, x0, x1, y1)))
        panels[gene] = (cal, centres, y0, y1)
    marks = {(gene, k): _markers(sat, occl, round(centres[k]), y0, y1)
             for gene, (cal, centres, y0, y1) in panels.items() for k in BARS[1:]}
    ref = {}
    for k in BARS[1:]:
        areas = np.array([m["area"] for (_, g), ms in marks.items() if g == k for m in ms])
        ref[k] = float(np.median(areas[areas <= 1.5 * np.percentile(areas, 25)]))
    caps = {(gene, k): _caps(black.astype(float), round(centres[k]), y0, y1)
            for gene, (cal, centres, y0, y1) in panels.items() for k in BARS[1:]}
    heights = [b - a + 1 for cs in caps.values() if len(cs) == 2 for a, b, _ in cs]
    cap_h, cap_spread = float(np.median(heights)), (max(heights) - min(heights)) / 2

    out = {}
    for label, (gene, k) in LABELS.items():
        cal, centres, y0, y1 = panels[gene]
        res = cal.residual
        cx = centres[k]
        cs = caps[(gene, k)]
        if len(cs) == 2:
            (_, _, up), (_, _, low) = cs
            mid, up_unc = (up + low) / 2, PX_UNC
        elif len(cs) == 1 and cs[0][1] - cs[0][0] + 1 > max(heights):
            # the two caps touch: the band's midpoint is the mean; the upper cap is a cap height below its top
            a, b, _ = cs[0]
            mid, up, up_unc = (a + b) / 2, a + (cap_h - 1) / 2, PX_UNC + cap_spread
        else:
            raise ValueError(f"{gene}/{k}: {len(cs)} cap bands")
        mean = point(cal, mid, PX_UNC, fig.to_page(cx, mid, scale))
        err = point(cal, up, up_unc, fig.to_page(cx, up, scale))
        bar = {"mean": [mean["value"], mean["lo"] - res, mean["hi"] + res],
               "error": [err["value"], err["lo"] - res, err["hi"] + res]}
        ms = marks[(gene, k)]
        countable = bool(ms) and all(AREA_TOL[0] * ref[k] <= m["area"] <= AREA_TOL[1] * ref[k] for m in ms)
        points = []
        if countable:
            for m in sorted(ms, key=lambda m: m["y"]):
                p = point(cal, m["y"], PX_UNC + abs(m["cy"] - m["y"]), fig.to_page(m["x"], m["y"], scale))
                p["lo"] -= res
                p["hi"] += res
                points.append(p)
        out[label] = {"points": points, "countable": countable, "bar": bar}
    return {"groups": out}
