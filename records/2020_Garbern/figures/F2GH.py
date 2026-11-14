"""Fig. 2H (journal_version.pdf p. 6): sarcomere length (µm), Control (DMSO) n=13 cells / Torin1 (200 nM) n=17 cells.

Raster panel (~200 dpi image), rendered at 600 dpi. Axis 0.0-2.5 from the six y tick marks (labels as printed).
The markers do not stand alone: the Torin1 squares merge with each other and with the bar-top line into one strip,
and the control circles near the mean touch the error bar, its cap and the bar top. Both groups therefore give the
bar only (countable: false, no points).
Bar mean = centre of the bar-top line (rows dark across the whole bar interior). Error = centre of the upper cap,
found as the stem rising from the bar-top line at the bar centre; the Torin1 error bar does not rise above the
bar-top line, so that group has no error reading.
"""
import numpy as np

from livinglit.figures.source import calibrate, dark_mask, point

DPI = 600
TICKS = [2.5, 2.0, 1.5, 1.0, 0.5, 0.0]  # y tick labels, top to bottom, as printed
GROUPS = ["Control (DMSO)", "Torin1 (200 nM)"]  # x tick labels, left to right
CAP_HALF = 12  # px at 600 dpi: the cap is wider than the stem (~6 px) on both sides of the bar centre
BASE_UNC_PX = 0.6 * DPI / 300  # 0.6 px at 300 dpi


def _runs(idx):
    """Consecutive runs of integer indices -> list of (start, end)."""
    out = []
    for i in idx:
        if out and i == out[-1][1] + 1:
            out[-1][1] = i
        else:
            out.append([i, i])
    return [tuple(r) for r in out]


def read(fig):
    img, scale = fig.render(DPI)
    m = dark_mask(img, 110)
    ax = int(np.argmax(m.sum(0)))  # y axis line
    ax_l = ax
    while m[:, ax_l - 1].sum() > 0.5 * m[:, ax].sum():
        ax_l -= 1
    ax_r = ax
    while m[:, ax_r + 1].sum() > 0.5 * m[:, ax].sum():
        ax_r += 1
    base = _runs(np.where(m[:, ax_r + 1:].mean(1) > 0.6)[0])[-1]  # x axis line rows
    ticks = _runs(np.where(m[:base[1] + 1, ax_l - 10:ax_l - 3].all(1))[0])
    assert len(ticks) == len(TICKS), ticks
    cal = calibrate([((a + b) / 2, v) for (a, b), v in zip(ticks, TICKS)])
    res_px = cal.residual / abs(cal.slope)
    # bar edges: long vertical lines right of the axis, standing on the x axis
    tall = m[:base[0], ax_r + 1:].sum(0) > 0.5 * (base[0] - ticks[0][0])
    edges = [(a + ax_r + 1, b + ax_r + 1) for a, b in _runs(np.where(tall)[0])]
    assert len(edges) == 2 * len(GROUPS), edges

    out = {}
    for i, g in enumerate(GROUPS):
        left, right = edges[2 * i][1] + 1, edges[2 * i + 1][0]
        c = int(round((left + right) / 2))
        full = _runs(np.where(m[:base[0], left:right].mean(1) > 0.97)[0])
        top_run = full[0]  # bar-top line
        top = (top_run[0] + top_run[1]) / 2
        line = top_run[1] - top_run[0] + 1
        mean = point(cal, top, BASE_UNC_PX + res_px, fig.to_page(c, top, scale))
        bar = {"mean": [float(mean["value"]), float(mean["lo"]), float(mean["hi"])]}
        stem = _runs(np.where(m[:top_run[0], c - 1:c + 2].all(1))[0])
        if stem and stem[-1][1] == top_run[0] - 1:
            rows = [r for r in range(stem[-1][0], stem[-1][1] + 1)
                    if m[r, c - CAP_HALF:c + CAP_HALF + 1].all()]
            cap = _runs(rows)
            if cap:
                cy = (cap[0][0] + cap[0][1]) / 2
                e = point(cal, cy, BASE_UNC_PX + line / 2 + res_px, fig.to_page(c, cy, scale))
                bar["error"] = [float(e["value"]), float(e["lo"]), float(e["hi"])]
        out[g] = {"points": [], "countable": False, "bar": bar}
    return {"groups": out}
