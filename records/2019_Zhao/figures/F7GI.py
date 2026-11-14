"""Fig. 7G-7I (journal_version.pdf p. 11): AP amplitude, APD30 and APD30/90 by tissue region, raster scatter with mean ± SEM.

The whole page is one JPEG (about 300 dpi), so the panels are read from a 300 dpi render. Markers (about 1 pt) touch
each other and the mean and SEM lines in every column (atrial APD30 is one merged blob), so no marker count or point
value is taken: each group returns its bar only, with countable false.

Axes: each panel's y spine is the longest dark vertical run; its tick marks are the dark rows just left of the spine,
taken bottom to top as the printed labels (tick labels are part of the image). The three x ticks are the dark columns
just below the x axis. In each group's column (x tick ± 45 px; dark grey atrial, dark red mid, blue ventricular), the
mean is the band of rows whose longest coloured run is at least 55 px (the mean line, about 71 px), and the SEM caps
are the bands of rows whose run is 25-54 px (about 35 px); the error end is the cap band above the mean.

The atrial group is compared with both mid and ventricular in separate items, so its bar is returned under two labels.
"""
from itertools import combinations

import numpy as np

from livinglit.figures.source import RASTER_UNCERTAINTY_PX_300DPI, calibrate

DPI = 300
PANELS = {  # panel -> (tick values bottom to top, measure label in figures.yaml)
    "G": [0, 20, 40, 60, 80, 100],
    "H": [0, 20, 40, 60],
    "I": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
}
COLUMNS = ["Atrial End", "Mid Region", "Ventricular End"]
COLOUR = {"Atrial End": "dark", "Mid Region": "red", "Ventricular End": "blue"}


def _masks(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return {"dark": (a.mean(2) < 120) & (np.ptp(a, 2) < 40),
            "red": (r > 90) & (r - g > 35) & (r - b > 35),
            "blue": (b > 90) & (b - r > 35) & (b - g > 30)}


def _bands(rows):
    """Consecutive row indices grouped into bands."""
    out = []
    for y in rows:
        if out and y == out[-1][-1] + 1:
            out[-1].append(y)
        else:
            out.append([y])
    return out


def _longest_run(row):
    best = cur = 0
    for v in row:
        cur = cur + 1 if v else 0
        best = max(best, cur)
    return best


def read(fig):
    img, scale = fig.render(DPI)
    a = img.astype(int)
    m = _masks(a)
    dark = m["dark"]
    h, w = dark.shape
    unc_px = RASTER_UNCERTAINTY_PX_300DPI * scale / (300 / 72.0)

    spines = [x for x in range(w) if dark[:, x].sum() > 150]
    spines = [b[len(b) // 2] for b in _bands(spines)]
    xaxis = max(range(h), key=lambda y: dark[y].sum())  # the x-axis row
    assert len(spines) == 3, spines

    groups = {}
    for (panel, ticks), sp in zip(PANELS.items(), spines):
        # y ticks: dark rows in the 4 px just left of the spine, down to the x axis
        win = a[:, sp - 6:sp - 2].mean(2).min(1)
        trows = [b for b in _bands([y for y in range(h) if win[y] < 130 and y <= xaxis + 2])]
        tpos = [float(np.mean(b)) for b in trows][-len(ticks):]
        assert len(tpos) == len(ticks), (panel, trows)
        cal = calibrate([(fig.crop[1] + y / scale, v) for y, v in zip(sorted(tpos, reverse=True), ticks)])
        unc = unc_px / scale + cal.residual / abs(cal.slope)
        top = min(tpos) + 3

        # x ticks: dark columns just below the x axis, right of this spine
        right = sp
        while right + 1 < w and dark[xaxis - 1:xaxis + 2, right + 1].any():  # end of this panel's x axis
            right += 1
        below = a[xaxis + 2:xaxis + 5, :].mean(2).max(0)  # dark in every row under the axis: a tick, not label text
        xt = [float(np.mean(b)) for b in _bands([x for x in range(sp + 10, right) if below[x] < 140])]
        if len(xt) > 3:  # 7I has a stray short tick at 1400 px beside the ventricular one: keep the evenly spaced three
            xt = list(min(combinations(xt, 3), key=lambda t: abs((t[1] - t[0]) - (t[2] - t[1]))))
        assert len(xt) == 3, (panel, xt)

        for col, cx in zip(COLUMNS, xt):
            cx = int(round(cx))
            mk = m[COLOUR[col]][:, cx - 45:cx + 45]
            runs = {y: _longest_run(mk[y]) for y in range(int(top), xaxis - 2)}
            mean_rows = [y for y, v in runs.items() if v >= 55]
            mean_bands = _bands(mean_rows)
            assert len(mean_bands) == 1, (panel, col, mean_bands)
            ym = float(np.mean(mean_bands[0]))
            caps = _bands([y for y, v in runs.items() if 25 <= v < 55])
            upper = [b for b in caps if np.mean(b) < ym]
            assert upper, (panel, col, caps)
            yu = float(np.mean(max(upper, key=lambda b: np.mean(b))))  # the cap band nearest above the mean
            pm, pu = fig.crop[1] + ym / scale, fig.crop[1] + yu / scale
            bar = {"mean": [cal.value(pm), *cal.interval(pm, unc)],
                   "error": [cal.value(pu), *cal.interval(pu, unc)]}
            labels = [f"{panel} {col}"]
            if col == "Atrial End":
                labels = [f"{panel} Atrial End vs Mid", f"{panel} Atrial End vs Ventricular"]
            for lab in labels:
                groups[lab] = {"points": [], "countable": False, "bar": bar}
    return {"groups": groups}
