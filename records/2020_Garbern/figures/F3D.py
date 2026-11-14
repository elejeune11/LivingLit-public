"""Fig. 3D (nihms-1549573.pdf p. 22): mtDNA:nuclear DNA ratio (ND1:B2M, normalized to control), Control / Torin1
(200 nM), n=3 each.

Read from the author manuscript copy (300 dpi image; the journal page p. 8 holds the same figure at ~200 dpi),
rendered at 600 dpi. Axis 0.0-1.5 from the four y tick marks (labels as printed).
Markers touch the error-bar stems and caps, so thin lines are removed by a morphological opening with a disc
wider than a line and narrower than a marker; what remains is one blob per marker. A marker left larger than the
median blob by a line remnant gets half the excess added to its uncertainty.
Bar mean = centre of the bar-top line beside the markers; error = centre of the upper cap, read clear of markers.
"""
import cv2
import numpy as np

from livinglit.figures.source import blobs, calibrate, dark_mask, point

DPI = 600
TICKS = [1.5, 1.0, 0.5, 0.0]  # y tick labels, top to bottom, as printed
GROUPS = ["Control", "Torin1 (200 nM)"]  # x tick labels, left to right
DISC = 15  # px at 600 dpi: lines are ~8 px thick, markers ~18 px
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
    ax = int(np.argmax(m.sum(0)))  # y axis line (longest vertical)
    ax_l = ax
    while m[:, ax_l - 1].sum() > 0.5 * m[:, ax].sum():
        ax_l -= 1
    base = _runs(np.where(m[:, ax + 20:].mean(1) > 0.8)[0])[-1]  # x axis line rows
    ticks = _runs(np.where(m[:, ax_l - 10:ax_l - 3].all(1))[0])
    assert len(ticks) == len(TICKS), ticks
    cal = calibrate([((a + b) / 2, v) for (a, b), v in zip(ticks, TICKS)])
    line = base[1] - base[0] + 1
    below = m[base[1] + 3:base[1] + 12, ax + 20:].all(0)  # x tick marks below the x axis
    xt = [(a + b) / 2 + ax + 20 for a, b in _runs(np.where(below)[0])]
    assert len(xt) == len(GROUPS), xt
    half = (xt[1] - xt[0]) / 2

    ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (DISC, DISC))
    opened = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, ker)
    found = [b for b in blobs(opened, 100) if b["x"] > ax + 20 and b["y"] < base[0]]
    size = float(np.median([min(b["box"][2:]) for b in found]))
    res_px = cal.residual / abs(cal.slope)

    out = {}
    for g, x0 in zip(GROUPS, xt):
        tops = []
        for c in [int(x0 + s * d) for s in (-1, 1) for d in (0.45 * half, 0.50 * half, 0.55 * half)]:
            r = _runs(np.where(m[:base[0] - 2, c])[0])[-1]
            tops.append((r[0] + r[1]) / 2)
        top = float(np.median(tops))
        spread = (max(tops) - min(tops)) / 2
        mean = point(cal, top, BASE_UNC_PX + spread + res_px, (x0, top))
        bar = {"mean": [mean["value"], mean["lo"], mean["hi"]]}
        stem = m[:int(top - line), int(round(x0)) - 1:int(round(x0)) + 2].any(1)
        run = _runs(np.where(stem)[0])
        if run and run[-1][1] >= int(top - line) - 1:
            cap_top = run[-1][0]
            cap = np.where(m[cap_top:cap_top + 2 * line, int(x0 + 30):int(x0 + 50)].all(1))[0]
            if len(cap):
                cy = cap_top + (cap[0] + cap[-1]) / 2
                e = point(cal, cy, BASE_UNC_PX + line / 2 + res_px, (x0, cy))
                bar["error"] = [e["value"], e["lo"], e["hi"]]
        mine = sorted((b for b in found if abs(b["x"] - x0) < half), key=lambda b: b["x"])
        alone = len(mine) == 3 and all(max(b["box"][2:]) < 1.5 * size for b in mine)
        pts = []
        if alone:
            for b in mine:
                bias = max(0.0, max(b["box"][2:]) - size) / 2  # line remnant left on a marker by the opening
                pts.append(point(cal, b["y"], BASE_UNC_PX + bias + res_px, fig.to_page(b["x"], b["y"], scale)))
        out[g] = {"points": pts, "countable": alone,
                  "bar": {k: [float(x) for x in v] for k, v in bar.items()}}
    return {"groups": out}
