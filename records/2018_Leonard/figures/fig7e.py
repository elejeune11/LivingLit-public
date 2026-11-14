"""Fig. 7E (journal version, p. 9): raster bar-and-scatter plot, "Tissue Stiffness (kPa)", groups UL, K1–K4 left to
right. Panel 7D (representative passive force–strain curves) carries no evidence item and is not read.

The figure is one embedded image at 300 dpi, rendered at that resolution. The plot is boxed (2 px frame); y-axis tick
marks are short dark marks just inside the left frame line, labelled 0, 0.5, 1, 1.5 bottom-up; the frame top is
unlabelled. Each group is a light grey bar (mean), markers (one per EHT, one column; UL grey, K1–K4 coloured) and a
black S.E.M. error bar: two caps ~43 px wide and 3–4 px thick joined by a vertical stem, drawn over the markers.

Bars: cap rows are rows holding a black run 36–50 px long centred within 8 px of the group's grey bar (the "n.s."
label is short text). Mean = midpoint of the two cap centroids (it coincides with the top of the grey bar); error =
upper cap.

Points: marker pixels within ±22 px of the stem (saturated pixels; for UL, mid-grey pixels darker than the bar and
lighter than the black error bar); stem pixels flanked by marker pixels on both sides of a row are given back to the
marker. A group is countable only if every marker stands alone: every blob has the area of one marker of its group
(0.8–1.25 of the median blob area of the group), no blob touches a cap (a cap may hide part of it), and there are at
least 3 blobs (the smallest printed n). Otherwise only its bar is returned. A marker's position is the centre of its
blob's bounding box; the interval adds the distance to the blob centroid (triangles) to the pixel uncertainty (0.6 px)
and the calibration misfit.
"""
import numpy as np

from livinglit.figures.source import blobs, calibrate, point

DPI = 300
PX_UNC = 0.6
# approximate frame in px of the crop render (x0, x1, y0, y1); printed labels top-down (None: frame top unlabelled)
FRAME = (103, 442, 19, 302)
LABELS = [None, 1.5, 1, 0.5, 0]
BARS = ["UL", "K1", "K2", "K3", "K4"]
ITEMS = [("F7E_stiff_ULvK1", ["UL", "K1"]), ("F7E_stiff_ULvK2", ["UL", "K2"]),
         ("F7E_stiff_ULvK3", ["UL", "K3"]), ("F7E_stiff_ULvK4", ["UL", "K4"])]
CAP_LEN = (36, 50)
CAP_OFF = 8
WINDOW = 22
SAT = 80
GREY = (90, 200)  # max channel of a UL marker pixel: darker than the bar (~233), lighter than black (<60)
AREA_TOL = (0.8, 1.25)
MIN_N = 3


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


def _calibration(ink, x0, y0, y1):
    """Tick marks in the 2 columns just right of the left frame line, plus the frame bottom (0)."""
    inner = ink[y0 + 10:y1 - 10]
    c = x0
    while np.median(inner[:, c + 1]) > 0.3:
        c += 1
    band = ink[:, c + 1:c + 3].max(axis=1)
    lo = y0 + 4
    ticks = [_centroid(band, lo + a - 1, lo + b + 1) for a, b in _runs(band[lo:y1 - 3] > 0.3)]
    frame = ink[:, c + 5:c + 15].mean(axis=1)
    bottom = _centroid(frame, y1 - 2, y1 + 2)
    marks = ticks + [bottom]
    values = [v for v in LABELS if v is not None]
    if len(marks) != len(values):
        raise ValueError(f"found {len(marks)} axis marks for {len(values)} labels")
    return calibrate(list(zip(marks, values)))


def _group_centres(img, x0, x1, y1):
    row = img[y1 - 12, x0 + 3:x1 - 2]
    hi, lo = row.max(axis=1), row.min(axis=1)
    grey = (hi > 180) & (hi < 245) & (hi - lo < 15)
    runs = [r for r in _runs(grey) if r[1] - r[0] >= 9]
    if len(runs) != len(BARS):
        raise ValueError(f"found {len(runs)} grey bars for {len(BARS)} groups")
    return [x0 + 3 + (a + b) / 2 for a, b in runs]


def _error_bar(black, c, y0, y1):
    """Cap centroid rows (upper, lower), stem column and cap row bands of the error bar near column c."""
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


def _markers(mark, black, stem, bands, y0, y1):
    """Blobs of marker pixels in the window around the stem: bounding-box centre, centroid row, area, touches-cap."""
    xa = round(stem) - WINDOW
    xb = round(stem) + WINDOW + 1
    ya, yb = y0 + 4, y1 - 4  # clear of the frame's anti-aliased edge, which the UL grey mask would pick up
    m = mark[ya:yb, xa:xb].copy()
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
    grey_mark = (img.max(axis=2) >= GREY[0]) & (img.max(axis=2) <= GREY[1]) & (sat < 20)
    x0, x1, y0, y1 = FRAME
    x0 = _refine(ink, x0, (y0 + 10, y1 - 10))
    x1 = _refine(ink, x1, (y0 + 10, y1 - 10))
    y0 = _refine(ink.T, y0, (x0 + 10, x1 - 10))
    y1 = _refine(ink.T, y1, (x0 + 10, x1 - 10))
    cal = _calibration(ink, x0, y0, y1)
    res = cal.residual

    read_g = {}
    for g, cx in zip(BARS, _group_centres(img, x0, x1, y1)):
        (up, low), stem, bands = _error_bar(black, round(cx), y0, y1)
        marks = _markers(grey_mark if g == "UL" else sat > SAT, black, stem, bands, y0, y1)
        mid = (up + low) / 2
        mean = point(cal, mid, PX_UNC, fig.to_page(stem, mid, scale))
        err = point(cal, up, PX_UNC, fig.to_page(stem, up, scale))
        bar = {"mean": [mean["value"], mean["lo"] - res, mean["hi"] + res],
               "error": [err["value"], err["lo"] - res, err["hi"] + res]}
        ref = float(np.median([m["area"] for m in marks])) if marks else 0.0
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

    out = {}
    for item, gs in ITEMS:
        for g in gs:
            out[f"{item}/{g}"] = read_g[g]
    return {"groups": out}
