"""Fig. 6A (journal version, p. 8): nine raster bar-and-scatter panels of RT-qPCR fold change, groups UL, K1–K4.

Panels, row by row: MYH6, MYH7, MYL2 / ACTC1, TNNI3, ITGB1BP2 / CASQ2, CACNA1C, SCN5A. Each y axis
is "ΔΔCt Fold Change: GENE / HPRT normalized to EHTs at Day 1" (unitless). The whole of Fig. 6 is
one embedded image (~300 dpi); the crop holds panel A only.

Each group is a light grey bar (mean), coloured markers (one per EHT, legend) and two black
horizontal caps joined by a short vertical line (legend: "error bars represent S.E.M.").
Markers touch or sit under the caps in most groups, so no group is countable: only the caps
are read. The mean is the midpoint of the two caps; "error" is the upper cap. Where the two
caps merge into one thick band (small error), their separation is the band's ink thickness
minus one cap's thickness (median of the separate caps), +0.5 px. The significance bars above
the data are thin lines and are dropped by their thickness.

Each panel is boxed. Its y axis is calibrated from the dark marks on the band just inside the
left axis line (frame top and bottom lines and the tick marks between), matched top-down to
the printed tick labels (the TNNI3 frame top is unlabelled and not used). Group centres are the centres of the light grey bars just above the
bottom axis line, in the printed order UL, K1, K2, K3, K4. UL is drawn but no F6A item involves
it, so it is not read.
"""
import numpy as np

from livinglit.figures.source import calibrate, point

DPI = 300
PX_UNC = 0.6
GROUPS = ["UL", "K1", "K2", "K3", "K4"]
READ = ["K1", "K2", "K3", "K4"]
MIN_CAP_INK = 3.0  # summed ink across a band's rows: caps ~4–6, significance lines ~1.5–2
CAP_IN, CAP_OUT = 13, 18  # columns from the group centre used to see the caps beside the markers

# panel: (approximate frame in px of the 300 dpi crop render: x0, x1, y0, y1;
#         labels of the marks on the left axis, top-down, None for an unlabelled mark)
_C = [(92, 385), (505, 797), (925, 1219)]
_R = [(58, 321), (431, 692), (794, 1055)]
PANELS = {
    "MYH6": (_C[0] + _R[0], [0.8, 0.6, 0.4, 0.2, 0]),
    "MYH7": (_C[1] + _R[0], [8, 6, 4, 2, 0]),
    "MYL2": (_C[2] + _R[0], [20, 15, 10, 5, 0]),
    "ACTC1": (_C[0] + _R[1], [2.5, 2, 1.5, 1, 0.5, 0]),
    "TNNI3": (_C[1] + _R[1], [None, 3, 2, 1, 0]),
    "ITGB1BP2": (_C[2] + _R[1], [1, 0.5, 0]),
    "CASQ2": (_C[0] + _R[2], [20, 15, 10, 5, 0]),
    "CACNA1C": (_C[1] + _R[2], [3, 2, 1, 0]),
    "SCN5A": (_C[2] + _R[2], [3, 2, 1, 0]),
}

ALL = ["K1", "K2", "K3", "K4"]
ITEMS = {
    "MYH6": [("F6A_MYH6_K4vK1", ["K4", "K1"]), ("F6A_MYH6_K4vK2", ["K4", "K2"]),
             ("F6A_MYH6_K4vK3", ["K4", "K3"])],
    "MYH7": [("F6A_MYH7_K4vK1", ["K4", "K1"]), ("F6A_MYH7_K3vK1", ["K3", "K1"]),
             ("F6A_MYH7_K2vK1", ["K2", "K1"])],
    "MYL2": [("F6A_MYL2_K4vK1", ["K4", "K1"]), ("F6A_MYL2_K4vK2", ["K4", "K2"]),
             ("F6A_MYL2_K4vK3", ["K4", "K3"]), ("F6A_MYL2_K3vK1", ["K3", "K1"])],
    "ACTC1": [("F6A_ACTC1_K4vK1", ["K4", "K1"]), ("F6A_ACTC1_K4vK2", ["K4", "K2"]),
              ("F6A_ACTC1_K4vK3", ["K4", "K3"])],
    "TNNI3": [("F6A_TNNI3_K4vK1", ["K4", "K1"]), ("F6A_TNNI3_K4vK2", ["K4", "K2"])],
    "ITGB1BP2": [("F6A_ITGB1BP2_K4vK1", ["K4", "K1"]), ("F6A_ITGB1BP2_K4vK2", ["K4", "K2"])],
    "CASQ2": [("F6A_CASQ2", ALL)],
    "CACNA1C": [("F6A_CACNA1C", ALL)],
    "SCN5A": [("F6A_SCN5A", ALL)],
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
    """Ink-weighted horizontal bands at the outer ends of a group's caps: (centroid row, thickness).

    Caps reach ±19.5 px from the group centre; markers (drawn over the caps) reach about ±12 px.
    Each side's profile is the median over its outer columns; a cap is seen if either side is clear.
    """
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
    panels = {}
    for name, ((x0, x1, y0, y1), labels) in PANELS.items():
        x0 = _refine(ink, x0, (y0 + 10, y1 - 10))
        x1 = _refine(ink, x1, (y0 + 10, y1 - 10))
        y0 = _refine(ink.T, y0, (x0 + 10, x1 - 10))
        y1 = _refine(ink.T, y1, (x0 + 10, x1 - 10))
        cal = calibrate(_ticks(ink, x0, y0, y1, labels))
        caps = {}
        for g, cx in zip(GROUPS, _group_centres(img, x0, x1, y1)):
            if g in READ:
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
