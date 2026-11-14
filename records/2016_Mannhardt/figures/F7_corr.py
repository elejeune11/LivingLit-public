"""Fig. 7: THV for T2 prolongation (y, nM) against the 10-20% APD90 increase (x, nM), log-log scatter
of ten labelled compounds (raster, 300 dpi).

Both axes are calibrated on their decade tick marks (10^0 ... 10^6 as printed). The y decade ticks
are longer than the minor ticks (only they reach 9-12 px left of the axis line at 300 dpi); the x
decade ticks are the evenly spaced marks below the axis. Markers are the filled discs left after an opening that removes lines and letters; each
stands alone, so each is a point. A marker is named by the compound label printed next to it:
ANCHORS give each label's approximate place in decades (used only to tell markers apart, never
as a value). x is the APD90 value read from the x axis (nM)."""
import numpy as np

from _util import UNC_PX, axes, blobs, calibrate, dark, gray, opened, reading, runs, x_axis_bottom, x_axis_ticks

DECADES = [6, 5, 4, 3, 2, 1, 0]  # printed y labels top to bottom: 10^6 ... 10^0
ANCHORS = {  # label: (log10 x, log10 y), approximate
    "procai": (5.0, 5.5), "beprid": (4.0, 5.0), "mexile": (4.0, 4.5), "ajmali": (3.5, 4.0),
    "flecai": (4.0, 3.0), "diphen": (3.35, 3.0), "sertin": (1.1, 2.5), "quinid": (2.5, 2.0),
    "ibutil": (1.0, 1.0), "cisapr": (1.0, 0.5),
}


def read(fig):
    img, scale = fig.render(300)
    img = img.astype(int)
    ax = axes(img)[0]
    g = gray(img)
    # y decade ticks: the only marks reaching 9-12 px left of the axis line
    c0, c1 = ax[0] - 12, ax[0] - 9
    ink = (g[:, c0:c1] < 128).all(axis=1)
    yt = []
    for a, b in runs(ink):
        if 2 <= b - a + 1 <= 9:
            w = (255 - g[a - 1:b + 2, c0:c1]).sum(axis=1).astype(float)
            rows = np.arange(a - 1, b + 2)
            yt.append(float((rows * w).sum() / w.sum()))
    if len(yt) != len(DECADES):
        raise ValueError(f"{len(yt)} y decade ticks: {yt}")
    caly = calibrate([(p, 10.0 ** d) for p, d in zip(yt, DECADES)], log=True)
    bottom, line = x_axis_bottom(img, ax, img.shape[1])
    xt = [p for p, n in x_axis_ticks(img, bottom, ax[0] - 2, img.shape[1])]
    if len(xt) != 7:
        raise ValueError(f"{len(xt)} x decade ticks: {xt}")
    calx = calibrate([(p, 10.0 ** d) for p, d in zip(xt, range(7))], log=True)
    m = opened(dark(img, 110), 9)
    discs = [b for b in blobs(m) if 250 <= b["area"] <= 450 and b["x"] > ax[1] + 5 and b["y"] < bottom - 3]
    if len(discs) != len(ANCHORS):
        raise ValueError(f"{len(discs)} markers for {len(ANCHORS)} labels")
    groups, used = {}, set()
    for lab, (lx, ly) in ANCHORS.items():
        d2 = [((np.log10(calx.value(b["x"])) - lx) ** 2 + (np.log10(caly.value(b["y"])) - ly) ** 2, i)
              for i, b in enumerate(discs)]
        dist, i = min(d2)
        if i in used or dist > 0.25:
            raise ValueError(f"no unique marker near the label {lab}")
        used.add(i)
        b = discs[i]
        p = reading(caly, b["y"], UNC_PX, fig, scale, (b["x"], b["y"]), x=float(f"{calx.value(b['x']):.4g}"))
        groups[lab] = {"points": [p], "countable": True}
    return {"groups": groups}
