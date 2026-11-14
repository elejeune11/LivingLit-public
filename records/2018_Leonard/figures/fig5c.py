"""Fig. 5C (journal version, p. 8): three raster bar-and-scatter panels, groups UL, K1–K4.

Left: time to peak (s); middle: time to 50% decay (s); right: decay constant τ (s). The whole
of Fig. 5 is one embedded image (~300 dpi); the crop holds panel C only (the left panel's axis
title is cut off; it is not read).

Each group is a light grey bar (mean), coloured markers (one per EHT, legend) and two black
horizontal caps joined by a short vertical line (legend: "error bars represent S.E.M.").
Markers touch or sit under the caps in most groups, so no group is countable: only the caps
are read. The mean is the midpoint of the two caps; "error" is the upper cap. Where the two
caps merge into one thick band (small error), their separation is the band's ink thickness
minus one cap's thickness (median of the separate caps), +0.5 px. The significance bars above
the data are thin lines (about 2 px of ink against about 4.6 px for a cap) and are dropped by
their thickness.

The y axis of each panel is calibrated from the dark marks on the band just inside the left
axis line (frame top and bottom lines and the tick marks between), matched top-down to the
printed tick labels; unlabelled marks are not used. Group centres are the centres of the light
grey bars just above the bottom axis line, in the printed order UL, K1, K2, K3, K4.
"""
import numpy as np

from livinglit.figures.source import calibrate, point

DPI = 300
PX_UNC = 0.6
GROUPS = ["UL", "K1", "K2", "K3", "K4"]
MIN_CAP_INK = 3.0  # summed ink across a band's rows: caps ~4.2–5.6, significance lines ~1.5–2.0

# panel: (approximate frame in px of the 300 dpi crop render: x0, x1, y0, y1;
#         labels of the marks on the left axis, top-down, None for an unlabelled mark)
PANELS = {
    "ttp": ((59, 351, 33, 334), [0.3, None, 0.2, None, 0.1, None, 0]),
    "t50": ((493, 784, 33, 328), [0.3, None, 0.2, None, 0.1, None, 0]),
    "tau": ((909, 1192, 34, 328), [None, 0.4, None, 0.2, None, 0]),
}

ITEMS = {
    "ttp": [("F5_ttp_K4vK1", ["K4", "K1"]), ("F5_ttp_K3vK1", ["K3", "K1"]),
            ("F5_ttp_K2vK1", ["K2", "K1"]), ("F5_ttp_K4vK2", ["K4", "K2"])],
    "t50": [("F5_t50_K4vK1", ["K4", "K1"]), ("F5_t50_K3vK1", ["K3", "K1"])],
    "tau": [("F5_tau_K3vK1", ["K3", "K1"])],
}


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


def _ticks(ink, x0, y0, y1, labels):
    """(row, value) for the marks on the band just inside the left axis line, matched top-down to labels."""
    band = ink[:, x0 + 2:x0 + 4].mean(axis=1)
    cents = sorted(_centroids(band, _clusters(band, range(y0 - 5, y1 + 6), 0.3)))
    if len(cents) != len(labels):
        raise ValueError(f"found {len(cents)} axis marks for {len(labels)} labels")
    return [(c, v) for c, v in zip(cents, labels) if v is not None]


def _group_centres(img, x0, x1, y1):
    """Centres of the light grey bars on a row just above the bottom axis line, left to right."""
    row = img[y1 - 8, x0 + 3:x1 - 2].astype(int)
    hi, lo = row.max(axis=1), row.min(axis=1)
    grey = ((hi > 180) & (hi < 245) & (hi - lo < 15)).astype(float)
    runs = [c for c in _clusters(grey, range(len(grey)), 0.5) if len(c) >= 10]
    if len(runs) != len(GROUPS):
        raise ValueError(f"found {len(runs)} grey bars for {len(GROUPS)} groups")
    return [x0 + 3 + (c[0] + c[-1]) / 2 for c in runs]


def _caps(ink, c, y0, y1):
    """Ink-weighted horizontal bands in a group's column, away from the whisker: (centroid row, thickness)."""
    cols = list(range(c - 14, c - 4)) + list(range(c + 5, c + 15))
    prof = np.median(ink[:, cols], axis=1)
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
    panels = {}
    for name, ((x0, x1, y0, y1), labels) in PANELS.items():
        x0 = _refine(ink, x0, (y0 + 10, y1 - 10))
        x1 = _refine(ink, x1, (y0 + 10, y1 - 10))
        y0 = _refine(ink.T, y0, (x0 + 10, x1 - 10))
        y1 = _refine(ink.T, y1, (x0 + 10, x1 - 10))
        cal = calibrate(_ticks(ink, x0, y0, y1, labels))
        caps = {}
        for g, cx in zip(GROUPS, _group_centres(img, x0, x1, y1)):
            caps[g] = (cx, _caps(ink, round(cx), y0, y1))
        panels[name] = (cal, caps)

    singles = [w for cal, caps in panels.values() for _, b in caps.values() if len(b) == 2 for _, w in b]
    t0 = float(np.median(singles))

    out = {}
    for name, (cal, caps) in panels.items():
        res = cal.residual
        bars = {}
        for g, (cx, bands) in caps.items():
            if len(bands) == 2:
                (up, _), (low, _) = sorted(bands)
                extra = 0.0
            elif len(bands) == 1:
                (cen, w), = bands
                sep = max(w - t0, 0.0)
                up, low = cen - sep / 2, cen + sep / 2
                extra = 0.5  # merged caps: separation from ink thickness
            else:
                raise ValueError(f"{name} {g}: {len(bands)} cap bands")
            unc = PX_UNC + extra
            mid = (up + low) / 2
            mean = point(cal, mid, unc, fig.to_page(cx, mid, scale))
            err = point(cal, up, unc, fig.to_page(cx, up, scale))
            bars[g] = {"mean": [mean["value"], mean["lo"] - res, mean["hi"] + res],
                       "error": [err["value"], err["lo"] - res, err["hi"] + res]}
        for item, gs in ITEMS[name]:
            for g in gs:
                out[f"{item}/{g}"] = {"points": [], "countable": False, "bar": bars[g]}
    return {"groups": out}
