"""Fig. 7A (journal version, p. 9): five raster bar-and-scatter plots, "ΔΔCt Fold Change: GENE / HPRT normalized to
EHTs at Day 1", for NPPA, NPPB, ACTA1, ADRA1B and ATP2A2 left to right; groups UL, K1–K4 left to right. Day 1 is the
reference of the normalisation and is not drawn.

The figure is one embedded image at 300 dpi, rendered at that resolution. Each plot is boxed (2 px frame); y-axis tick
marks are short dark marks just inside the left frame line. Each group is a light grey bar (mean), coloured markers
(one per EHT, all in one column) and a black S.E.M. error bar: two caps ~36 px wide and 3–4 px thick joined by a
vertical stem. Unlike Fig. S7, the error bar is drawn over the markers, so the stem cuts markers in two and a cap can
hide part of a marker.

Bars: cap rows are rows holding a black run 28–44 px long centred within 8 px of the group's grey bar (significance
lines above the data are longer, or centred between groups). Mean = midpoint of the two cap centroids (it coincides
with the top of the grey bar); error = upper cap.

Points: markers are saturated pixels within ±20 px of the stem; stem pixels flanked by marker pixels on both sides of
the same row are given back to the marker before blobs are found. A group is countable only if every marker stands
alone: every blob has the area of one marker (0.8–1.25 of the median blob area of the figure), no blob touches a cap
(a cap may hide part of it), and there are at least 4 blobs (the smallest printed n; fewer means markers are stacked).
Otherwise only its bar is returned. A marker's position is the centre of its blob's bounding box; for triangles the
data point may sit at the centroid instead, so the interval adds the distance between the two to the pixel
uncertainty (0.6 px) and the calibration misfit.

Axes: calibrated from the tick marks inside the left frame line, matched top-down to the printed labels, plus the
frame bottom (0) and the frame top where it carries a label. UL is drawn but no item involves it, so it is not
returned.
"""
import numpy as np

from livinglit.figures.source import blobs, calibrate, point

DPI = 300
PX_UNC = 0.6
# gene, approximate frame in px of the crop render (x0, x1, y0, y1), printed labels top-down (None: frame top unlabelled)
PANELS = [
    ("NPPA", (134, 436, 50, 347), [None, 2, 1.5, 1, 0.5, 0]),
    ("NPPB", (554, 856, 50, 347), [0.8, 0.6, 0.4, 0.2, 0]),
    ("ACTA1", (968, 1275, 50, 347), [3, 2, 1, 0]),
    ("ADRA1B", (1403, 1705, 50, 347), [None, 1.5, 1, 0.5, 0]),
    ("ATP2A2", (1830, 2132, 50, 347), [1.2, 0.9, 0.6, 0.3, 0]),
]
BARS = ["UL", "K1", "K2", "K3", "K4"]
# gene -> (item, groups) that rest on it
ITEMS = {
    "NPPA": [("F7A_NPPA_K4vK1", ["K4", "K1"]), ("F7A_NPPA_K4vDay1", ["K4"])],
    "NPPB": [("F7A_NPPB_K4vK1", ["K4", "K1"]), ("F7A_NPPB_K4vK2", ["K4", "K2"]),
             ("F7A_NPPB_K3vK1", ["K3", "K1"]), ("F7A_NPPB_K3vK2", ["K3", "K2"])],
    "ACTA1": [("F7A_ACTA1_K4vK1", ["K4", "K1"]), ("F7A_ACTA1_K4vK2", ["K4", "K2"]),
              ("F7A_ACTA1_K4vK3", ["K4", "K3"]), ("F7A_ACTA1_K4vDay1", ["K4"])],
    "ADRA1B": [("F7A_ADRA1B_K4vK1", ["K4", "K1"])],
    "ATP2A2": [("F7A_ATP2A2", ["K1", "K2", "K3", "K4"])],
}
GROUPS = ["K1", "K2", "K3", "K4"]
CAP_LEN = (28, 44)
CAP_OFF = 8
WINDOW = 20
SAT = 80
AREA_TOL = (0.8, 1.25)
MIN_N = 4


def _runs(mask):
    idx = np.flatnonzero(mask)
    if not len(idx):
        return []
    return [(int(r[0]), int(r[-1])) for r in np.split(idx, np.flatnonzero(np.diff(idx) > 1) + 1)]


def _refine(ink, approx, span):
    """The darkest column within ±4 px of an approximate frame edge."""
    lo, hi = span
    return max(range(approx - 4, approx + 5), key=lambda p: ink[lo:hi, p].mean())


def _centroid(profile, lo, hi):
    rows = np.arange(lo, hi + 1)
    w = profile[lo:hi + 1]
    return float((rows * w).sum() / w.sum())


def _calibration(ink, x0, y0, y1, labels):
    """Tick marks in the 2 columns just right of the left frame line, plus frame bottom and (if labelled) top."""
    inner = ink[y0 + 10:y1 - 10]
    c = x0
    while np.median(inner[:, c + 1]) > 0.3:
        c += 1
    band = ink[:, c + 1:c + 3].max(axis=1)
    lo = y0 + 4
    ticks = [_centroid(band, lo + a - 1, lo + b + 1) for a, b in _runs(band[lo:y1 - 3] > 0.3)]
    frame = ink[:, c + 5:c + 15].mean(axis=1)
    top = _centroid(frame, y0 - 2, y0 + 2)
    bottom = _centroid(frame, y1 - 2, y1 + 2)
    marks = ([top] if labels[0] is not None else []) + ticks + [bottom]
    values = [v for v in labels if v is not None]
    if len(marks) != len(values):
        raise ValueError(f"found {len(marks)} axis marks for {len(values)} labels")
    return calibrate(list(zip(marks, values)))


def _group_centres(img, x0, x1, y1):
    row = img[y1 - 15, x0 + 3:x1 - 2]
    hi, lo = row.max(axis=1), row.min(axis=1)
    grey = (hi > 180) & (hi < 245) & (hi - lo < 15)
    runs = [r for r in _runs(grey) if r[1] - r[0] >= 9]
    if len(runs) != len(BARS):
        raise ValueError(f"found {len(runs)} grey bars for {len(BARS)} groups")
    return [x0 + 3 + (a + b) / 2 for a, b in runs]


def _error_bar(black, c, y0, y1):
    """Cap centroid rows (upper, lower) and stem column of the error bar near column c."""
    xa = c - 60
    rows, spans = [], []
    for y in range(y0 + 3, y1 - 2):
        for a, b in _runs(black[y, xa:c + 61]):
            n = b - a + 1
            if CAP_LEN[0] <= n <= CAP_LEN[1] and abs(xa + (a + b) / 2 - c) <= CAP_OFF:
                rows.append(y)
                spans.append((xa + a, xa + b))
                break
    bands = _runs(np.isin(np.arange(y1 + 1), rows))
    if len(bands) != 2:
        raise ValueError(f"{len(bands)} cap bands near column {c}")
    caps = []
    for a, b in bands:
        w = black[a - 1:b + 2, c - 25:c + 26].sum(axis=1).astype(float)
        caps.append(float((np.arange(a - 1, b + 2) * w).sum() / w.sum()))
    stem = float(np.mean([(a + b) / 2 for a, b in spans]))
    return caps, stem, bands


def _markers(sat, black, stem, bands, y0, y1):
    """Blobs of marker pixels in the window around the stem: bounding-box centre, centroid row, area, touches-cap."""
    xa = round(stem) - WINDOW
    xb = round(stem) + WINDOW + 1
    ya, yb = y0 + 2, y1 - 1
    m = sat[ya:yb, xa:xb] > SAT
    blk = black[ya:yb, xa:xb]
    for r in range(m.shape[0]):
        for a, b in _runs(blk[r] & ~m[r]):
            if a > 0 and b < m.shape[1] - 1 and m[r, max(0, a - 2):a].any() and m[r, b + 1:b + 3].any() \
                    and b - a <= 4:
                m[r, a:b + 1] = True
    cap_rows = set()
    for a, b in bands:
        cap_rows |= set(range(a - 1, b + 2))
    out = []
    for bl in blobs(m, min_area=10):
        bx, by, w, h = bl["box"]
        top, bot = ya + by, ya + by + h - 1
        out.append({"x": xa + bx + (w - 1) / 2, "y": ya + by + (h - 1) / 2, "cy": ya + bl["y"], "area": bl["area"],
                    "at_cap": any(top - 1 <= r <= bot + 1 for r in cap_rows)})
    return out


def read(fig):
    img, scale = fig.render(DPI)
    img = img.astype(int)
    ink = np.clip(1 - img.max(axis=2) / 235.0, 0, 1)
    sat = img.max(axis=2) - img.min(axis=2)
    black = (ink > 0.5) & (sat < 60)
    panels = []
    for gene, (x0, x1, y0, y1), labels in PANELS:
        x0 = _refine(ink, x0, (y0 + 10, y1 - 10))
        x1 = _refine(ink, x1, (y0 + 10, y1 - 10))
        y0 = _refine(ink.T, y0, (x0 + 10, x1 - 10))
        y1 = _refine(ink.T, y1, (x0 + 10, x1 - 10))
        cal = _calibration(ink, x0, y0, y1, labels)
        groups = {}
        for g, cx in zip(BARS, _group_centres(img, x0, x1, y1)):
            if g in GROUPS:
                caps, stem, bands = _error_bar(black, round(cx), y0, y1)
                groups[g] = (caps, stem, _markers(sat, black, stem, bands, y0, y1))
        panels.append((gene, cal, groups))
    ref = float(np.median([m["area"] for _, _, gs in panels for _, _, ms in gs.values() for m in ms]))

    out = {}
    for gene, cal, groups in panels:
        res = cal.residual
        read_g = {}
        for g, ((up, low), stem, marks) in groups.items():
            mid = (up + low) / 2
            mean = point(cal, mid, PX_UNC, fig.to_page(stem, mid, scale))
            err = point(cal, up, PX_UNC, fig.to_page(stem, up, scale))
            bar = {"mean": [mean["value"], mean["lo"] - res, mean["hi"] + res],
                   "error": [err["value"], err["lo"] - res, err["hi"] + res]}
            countable = len(marks) >= MIN_N and all(
                AREA_TOL[0] * ref <= m["area"] <= AREA_TOL[1] * ref and not m["at_cap"] for m in marks)
            points = []
            if countable:
                for m in sorted(marks, key=lambda m: m["y"]):
                    p = point(cal, m["y"], PX_UNC + abs(m["cy"] - m["y"]), fig.to_page(m["x"], m["y"], scale))
                    p["lo"] -= res
                    p["hi"] += res
                    points.append(p)
            read_g[g] = {"points": points, "countable": countable, "bar": bar}
        for item, gs in ITEMS[gene]:
            for g in gs:
                out[f"{item}/{g}"] = read_g[g]
    return {"groups": out}
