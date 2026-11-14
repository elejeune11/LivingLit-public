"""Fig. 2B (journal version, p. 5): eight raster bar-and-scatter panels, groups K1–K4.

Each group is drawn as a light grey bar (mean), coloured markers (one per EHT) and two black
horizontal caps joined by a short vertical line (mean ± S.E.M., legend). Markers overlap one
another and the caps in every group, so no group is countable: only the caps are read.
The mean is the midpoint of the two caps; "error" is the upper cap. Where the two caps
merge into one thick band (small S.E.M.), their separation is the band's ink thickness
minus one cap's thickness.

The y axis of each panel is calibrated from its tick marks (short dark marks just inside the
left axis line), matched bottom-up to the tick labels printed on that panel. Groups sit at
x = 1..4 on an axis from 0 to 5 (bottom tick marks confirm this), so group k's centre is
x0 + k (x1 - x0) / 5 of the panel frame.
"""
import numpy as np

from livinglit.figures.source import calibrate, point

DPI = 300
PX_UNC = 0.6

# panel: (approximate frame in px of the 300 dpi crop render: x0, x1, y0, y1; tick labels bottom-up)
PANELS = {
    "rl": ((160, 535, 26, 334), [5, 6, 7, 8, 9]),
    "force": ((692, 1072, 25, 335), [0, 200, 400, 600]),
    "vel": ((1233, 1604, 21, 333), [0, 2, 4, 6]),
    "power": ((1756, 2140, 23, 330), [0, 200, 400, 600, 800]),
    "fs": ((160, 537, 436, 744), [0, 5, 10, 15]),
    "stress": ((692, 1072, 436, 744), [0, 0.2, 0.4, 0.6, 0.8]),
    "t50": ((1233, 1604, 430, 743), [100, 120, 140, 160]),
    "work": ((1758, 2140, 434, 743), [0, 10, 20, 30, 40, 50]),
}

# record items each panel's groups serve (comparisons tested in the record)
ITEMS = {
    "rl": ["K4vK1", "K3vK1", "K2vK1", "K4vK2"],
    "force": ["K4vK1", "K3vK1", "K2vK1", "K4vK2", "K3vK2"],
    "vel": ["K4vK1", "K3vK1", "K2vK1", "K4vK2", "K3vK2", "K4vK3"],
    "power": ["K4vK1", "K3vK1", "K4vK2", "K4vK3"],
    "fs": ["K4vK1", "K3vK1", "K2vK1", "K4vK2", "K3vK2", "K4vK3"],
    "stress": ["K4vK1", "K3vK1", "K2vK1", "K4vK2", "K3vK2"],
    "t50": ["K4vK1", "K3vK1", "K4vK2", "K3vK2"],
    "work": ["K4vK1", "K4vK2", "K4vK3"],
}


def _refine(dark, approx, axis, span):
    """The darkest line (column or row) within ±4 px of an approximate frame edge."""
    lo, hi = span
    best = None
    for p in range(max(approx - 4, 0), min(approx + 5, dark.shape[1])):
        v = dark[lo:hi, p].mean() if axis == "col" else dark[p, lo:hi].mean()
        if best is None or v > best[0]:
            best = (v, p)
    return best[1]


def _clusters(profile, rows, thr):
    out = []
    for y in rows:
        if profile[y] > thr:
            if out and y - out[-1][-1] <= 1:
                out[-1].append(y)
            else:
                out.append([y])
    return out


def _ticks(ink, ax, y0, y1, labels):
    """(row, value) for tick marks just inside the left axis line, matched bottom-up to labels."""
    band = ink[:, ax + 3:ax + 5].mean(axis=1)
    cl = _clusters(band, range(y0 - 5, y1 + 6), 0.4)
    cents = [sum(y * band[y] for y in c) / sum(band[y] for y in c) for c in cl]
    cents.sort(reverse=True)  # bottom first
    if len(cents) < len(labels):
        raise ValueError(f"found {len(cents)} tick marks for {len(labels)} labels")
    extra = cents[len(labels):]
    if any(abs(e - y0) > 3 for e in extra):
        raise ValueError(f"unlabelled tick marks away from the frame top: {extra}")
    return list(zip(cents[:len(labels)], labels))


def _caps(ink, c, y0, y1):
    """Ink-weighted cap bands in a group's column: list of (centroid row, ink thickness)."""
    cols = list(range(c - 32, c - 4)) + list(range(c + 5, c + 33))
    prof = np.median(ink[:, cols], axis=1)
    bands = []
    for cl in _clusters(prof, range(y0 + 4, y1 - 3), 0.5):
        rows = range(cl[0] - 1, cl[-1] + 2)
        w = sum(prof[y] for y in rows)
        bands.append((sum(y * prof[y] for y in rows) / w, w))
    return bands


def read(fig):
    img, scale = fig.render(DPI)
    im = img.astype(int)
    ink = np.clip(1 - im.max(axis=2) / 235.0, 0, 1)  # black lines ~1; grey bar, background and coloured markers low
    panels = {}
    for name, ((x0, x1, y0, y1), labels) in PANELS.items():
        x0 = _refine(ink, x0, "col", (y0 + 10, y1 - 10))
        x1 = _refine(ink, x1, "col", (y0 + 10, y1 - 10))
        y0 = _refine(ink.T, y0, "col", (x0 + 10, x1 - 10))
        y1 = _refine(ink.T, y1, "col", (x0 + 10, x1 - 10))
        marks = _ticks(ink, x0, y0, y1, labels)
        cal = calibrate(marks)
        caps = {}
        for k in range(1, 5):
            c = round(x0 + k * (x1 - x0) / 5)
            bands = [b for b in _caps(ink, c, y0, y1) if b[1] >= 3.0]  # significance bars are ~2 px, caps ~4 px
            caps[k] = (c, bands)
        panels[name] = (cal, caps)

    singles = [w for _, (_, caps) in panels.items() for _, (_, b) in caps.items() if len(b) == 2 for _, w in b]
    t0 = float(np.median(singles))

    out = {}
    for name, (cal, caps) in panels.items():
        for k, (c, bands) in caps.items():
            if len(bands) == 2:
                (up, _), (low, _) = sorted(bands)
                extra = 0.0
            elif len(bands) == 1:
                (cen, w), = bands
                sep = max(w - t0, 0.0)
                up, low = cen - sep / 2, cen + sep / 2
                extra = 0.5  # merged caps: separation from ink thickness
            else:
                raise ValueError(f"{name} K{k}: {len(bands)} cap bands")
            unc = PX_UNC + extra
            mid = (up + low) / 2
            mean = point(cal, mid, unc, fig.to_page(c, mid, scale))
            err = point(cal, up, unc, fig.to_page(c, up, scale))
            res = cal.residual
            bar = {"mean": [mean["value"], mean["lo"] - res, mean["hi"] + res],
                   "error": [err["value"], err["lo"] - res, err["hi"] + res]}
            g = f"K{k}"
            for cmp in ITEMS[name]:
                if g in cmp.split("v"):
                    out[f"F2_{name}_{cmp}/{g}"] = {"points": [], "countable": False, "bar": bar}
    return {"groups": out}
