"""Fig. S7 (supplement 2, p. 5): two raster bar-and-scatter plots, "Normalized Protein Relative to EHTs at Day 1":
left αMHC / LAMIN A/C (0–1.5), right βMHC / LAMIN A/C (0–15); groups UL, K1–K4 left to right.

The figure is one embedded image (~240 dpi), rendered at that resolution. Each group is a light grey bar (mean),
coloured markers (one per EHT) and two black horizontal caps joined by a short vertical line (mean ± S.E.M., as in
main Fig. 6C). Markers are drawn over the caps, so no marker is hidden by a cap.

Bars: the caps are seen 13–16 px either side of the group centre, beyond the markers (markers reach ±11 px). Mean =
midpoint of the two caps; error = upper cap. Group centres are the centres of the grey bars on a row just above the
bottom axis line (UL, K1, K2, K3, K4 in printed order).

Points: a group's markers are the saturated pixels within ±18 px of its centre (markers are blue, green, red and
yellow; the black caps and grey bars are unsaturated). The group is countable only if every blob has the area of one
marker (within 0.8–1.25 of the median blob area of the whole figure); a blob of two or three touching markers makes
the group not countable, and only its bar is returned. A marker's position is the centre of its blob's bounding box;
for triangles the data point may sit at the shape's centroid instead, so the interval adds the distance between the
two to the pixel uncertainty (0.6 px at 300 dpi = 0.48 px here) and the calibration misfit.

Axes: each plot is boxed; its y axis is calibrated from the dark marks on the band just inside the left axis line
(frame top, two tick marks, frame bottom), matched top-down to the printed labels. UL is drawn but no S7 item
involves it, so it is not returned.
"""
import numpy as np

from livinglit.figures.source import blobs, calibrate, point

DPI = 240
PX_UNC = 0.6 * DPI / 300
# item, approximate frame in px of the crop render (x0, x1, y0, y1), left-axis marks top-down
PANELS = [
    ("S7_aMHC", (121, 446, 80, 320), [1.5, 1, 0.5, 0]),
    ("S7_bMHC", (546, 869, 82, 319), [15, 10, 5, 0]),
]
BARS = ["UL", "K1", "K2", "K3", "K4"]
GROUPS = ["K1", "K2", "K3", "K4"]
CAP_IN, CAP_OUT = 13, 16
WINDOW = 18
SAT = 80
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


def _caps(ink, c, y0, y1):
    """Centroid rows of the horizontal bands at the outer ends of a group's caps."""
    left = np.median(ink[:, c - CAP_OUT:c - CAP_IN + 1], axis=1)
    right = np.median(ink[:, c + CAP_IN:c + CAP_OUT + 1], axis=1)
    prof = np.maximum(left, right)
    return sorted(_centroids(prof, _clusters(prof, range(y0 + 3, y1 - 2), 0.5)))


def _markers(sat, c, y0, y1):
    """Blobs of saturated pixels in a group's window: (bounding-box centre row, centroid row, area), in crop px."""
    xa = c - WINDOW
    sub = sat[y0 + 2:y1 - 1, xa:c + WINDOW + 1] > SAT
    out = []
    for b in blobs(sub, min_area=10):
        bx, by, w, h = b["box"]
        out.append({"x": xa + bx + (w - 1) / 2, "y": y0 + 2 + by + (h - 1) / 2,
                    "cy": y0 + 2 + b["y"], "area": b["area"]})
    return out


def read(fig):
    img, scale = fig.render(DPI)
    img = img.astype(int)
    ink = np.clip(1 - img.max(axis=2) / 235.0, 0, 1)
    sat = img.max(axis=2) - img.min(axis=2)
    panels = []
    for item, (x0, x1, y0, y1), labels in PANELS:
        x0 = _refine(ink, x0, (y0 + 10, y1 - 10))
        x1 = _refine(ink, x1, (y0 + 10, y1 - 10))
        y0 = _refine(ink.T, y0, (x0 + 10, x1 - 10))
        y1 = _refine(ink.T, y1, (x0 + 10, x1 - 10))
        cal = _calibration(ink, x0, y0, y1, labels)
        centres = dict(zip(BARS, _group_centres(img, x0, x1, y1)))
        panels.append((item, cal, centres, y0, y1))
    all_blobs = [m for _, _, centres, y0, y1 in panels for g in GROUPS
                 for m in _markers(sat, round(centres[g]), y0, y1)]
    ref = float(np.median([m["area"] for m in all_blobs]))

    out = {}
    for item, cal, centres, y0, y1 in panels:
        res = cal.residual
        for g in GROUPS:
            cx = centres[g]
            caps = _caps(ink, round(cx), y0, y1)
            if len(caps) != 2:
                raise ValueError(f"{item}/{g}: {len(caps)} cap bands")
            up, low = caps
            mid = (up + low) / 2
            mean = point(cal, mid, PX_UNC, fig.to_page(cx, mid, scale))
            err = point(cal, up, PX_UNC, fig.to_page(cx, up, scale))
            bar = {"mean": [mean["value"], mean["lo"] - res, mean["hi"] + res],
                   "error": [err["value"], err["lo"] - res, err["hi"] + res]}
            marks = _markers(sat, round(cx), y0, y1)
            countable = bool(marks) and all(AREA_TOL[0] * ref <= m["area"] <= AREA_TOL[1] * ref for m in marks)
            points = []
            if countable:
                for m in sorted(marks, key=lambda m: m["y"]):
                    p = point(cal, m["y"], PX_UNC + abs(m["cy"] - m["y"]), fig.to_page(m["x"], m["y"], scale))
                    p["lo"] -= res
                    p["hi"] += res
                    points.append(p)
            out[f"{item}/{g}"] = {"points": points, "countable": countable, "bar": bar}
    return {"groups": out}
