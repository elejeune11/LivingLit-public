"""Fig. 3D–F (journal version, p. 6): three raster bar-and-scatter panels, groups UL, K1–K4.

D: slope of the Frank-Starling curve (μN / strain); E: maximum isometric twitch force (μN);
F: maximum contraction velocity at Lmax (mN / sec). The crop also holds the right part of
panel C, which is not read.

Each group is a light grey bar (mean), coloured markers (one per EHT) and two black horizontal
caps joined by a short vertical line (mean ± S.E.M., legend). Markers touch or sit under the
caps in most groups, so no group is countable: only the caps are read. The mean is the midpoint
of the two caps; "error" is the upper cap. Significance bars (~2 px) are told from caps (~4 px)
by ink thickness.

The y axis of each panel is calibrated from its tick marks (short dark marks just inside the
left axis line), matched bottom-up to the tick labels printed on that panel; an unlabelled
tick at the frame top (F: 7) is dropped. Group centres are the five tick marks just above the
bottom axis line, in the printed order UL, K1, K2, K3, K4.
"""
import numpy as np

from livinglit.figures.source import calibrate, point

DPI = 300
PX_UNC = 0.6
GROUPS = ["UL", "K1", "K2", "K3", "K4"]

# panel: (approximate frame in px of the 300 dpi crop render: x0, x1, y0, y1; tick labels bottom-up)
PANELS = {
    "fsslope": ((721, 1120, 55, 410), [0, 500, 1000, 1500]),
    "maxforce": ((86, 497, 535, 893), [0, 200, 400, 600, 800, 1000]),
    "vel": ((721, 1120, 534, 897), [0, 2, 4, 6]),
}

# record labels each panel's groups serve: (item, groups)
ITEMS = {
    "fsslope": [("F3_fsslope", ["K1", "K2", "K3", "K4"]),
                ("F3_fs_response", ["UL", "K1", "K2", "K3", "K4"])],
    "maxforce": [("F3_maxforce_text", ["K2", "K3"]),
                 ("F3_maxforce_K4vK1", ["K4", "K1"]),
                 ("F3_maxforce_K1vUL", ["K1", "UL"]),
                 ("F3_maxforce_K2vUL", ["K2", "UL"]),
                 ("F3_maxforce_K3vUL", ["K3", "UL"]),
                 ("F3_maxforce_K4vUL", ["K4", "UL"])],
    "vel": [("F3_vel_K2vK1", ["K2", "K1"])],
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
    """(row, value) for tick marks just inside the left axis line, matched bottom-up to labels."""
    band = ink[:, x0 + 3:x0 + 5].mean(axis=1)
    cents = sorted(_centroids(band, _clusters(band, range(y0 - 5, y1 + 6), 0.4)), reverse=True)
    if len(cents) < len(labels):
        raise ValueError(f"found {len(cents)} tick marks for {len(labels)} labels")
    extra = cents[len(labels):]
    if any(abs(e - y0) > 3 for e in extra):
        raise ValueError(f"unlabelled tick marks away from the frame top: {extra}")
    return list(zip(cents[:len(labels)], labels))


def _group_centres(ink, x0, x1, y1):
    """Columns of the tick marks just above the bottom axis line, left to right."""
    band = ink[y1 - 6:y1 - 3, :].mean(axis=0)
    cents = _centroids(band, _clusters(band, range(x0 + 5, x1 - 4), 0.4))
    if len(cents) != len(GROUPS):
        raise ValueError(f"found {len(cents)} group tick marks for {len(GROUPS)} groups")
    return cents


def _caps(ink, c, y0, y1):
    """Ink-weighted horizontal bands in a group's column, away from the whisker: (centroid row, thickness)."""
    cols = list(range(c - 18, c - 4)) + list(range(c + 5, c + 19))
    prof = np.median(ink[:, cols], axis=1)
    bands = []
    for cl in _clusters(prof, range(y0 + 4, y1 - 3), 0.5):
        rows = range(cl[0] - 1, cl[-1] + 2)
        w = sum(prof[y] for y in rows)
        bands.append((sum(y * prof[y] for y in rows) / w, w))
    return bands


def read(fig):
    img, scale = fig.render(DPI)
    ink = np.clip(1 - img.astype(int).max(axis=2) / 235.0, 0, 1)  # black ~1; grey bars, background, markers low
    out = {}
    for name, ((x0, x1, y0, y1), labels) in PANELS.items():
        x0 = _refine(ink, x0, (y0 + 10, y1 - 10))
        x1 = _refine(ink, x1, (y0 + 10, y1 - 10))
        y0 = _refine(ink.T, y0, (x0 + 10, x1 - 10))
        y1 = _refine(ink.T, y1, (x0 + 10, x1 - 10))
        cal = calibrate(_ticks(ink, x0, y0, y1, labels))
        res = cal.residual
        bars = {}
        for g, cx in zip(GROUPS, _group_centres(ink, x0, x1, y1)):
            c = round(cx)
            bands = [b for b in _caps(ink, c, y0, y1) if b[1] >= 3.0]  # significance bars are ~2 px, caps ~4 px
            if len(bands) != 2:
                raise ValueError(f"{name} {g}: {len(bands)} cap bands")
            (up, _), (low, _) = sorted(bands)
            mid = (up + low) / 2
            mean = point(cal, mid, PX_UNC, fig.to_page(cx, mid, scale))
            err = point(cal, up, PX_UNC, fig.to_page(cx, up, scale))
            bars[g] = {"mean": [mean["value"], mean["lo"] - res, mean["hi"] + res],
                       "error": [err["value"], err["lo"] - res, err["hi"] + res]}
        for item, gs in ITEMS[name]:
            for g in gs:
                out[f"{item}/{g}"] = {"points": [], "countable": False, "bar": bars[g]}
    return {"groups": out}
