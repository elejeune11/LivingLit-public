"""Fig. 4B: FOC/CSA (mN/mm²) of ECM-EHTs at L0 and Lmax (raster, greyscale JPEG).

The y axis is calibrated from its six tick marks (0.0 to 0.5 in steps of 0.1, as printed).
Each group has a mean line and SEM caps (horizontal lines centred on the group's x tick).
Several markers in both groups touch or sit under the mean line and the SEM caps, so the
markers do not each stand alone: the groups return the mean and the upper SEM end only.
"""
import numpy as np

from livinglit.figures.source import calibrate, dark_mask, RASTER_UNCERTAINTY_PX_300DPI

DPI = 300
TICK_VALUES = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]  # printed tick labels, bottom to top
GROUPS = ["L0", "Lmax"]  # x tick labels, left to right


def _runs(idx):
    """Consecutive index runs as (start, end)."""
    out = []
    for i in idx:
        if out and i == out[-1][1] + 1:
            out[-1][1] = i
        else:
            out.append([i, i])
    return [tuple(r) for r in out]


def read(fig):
    img, scale = fig.render(DPI)
    m = dark_mask(img, 128)
    h, w = m.shape

    # axes: the y axis is the longest dark column, the x axis the longest dark row
    yaxis = int(np.argmax(m.sum(0)))
    xaxis_rows = _runs(np.where(m.sum(1) > 0.6 * w)[0])
    xaxis = xaxis_rows[-1]

    # y ticks: short dark runs just left of the y axis
    band = m[:, yaxis - 8:yaxis - 1].sum(1)
    ticks = [(a + b) / 2 for a, b in _runs(np.where(band >= 4)[0])]
    if len(ticks) != len(TICK_VALUES):
        raise ValueError(f"expected {len(TICK_VALUES)} y ticks, found {len(ticks)}")
    cal = calibrate(list(zip(sorted(ticks, reverse=True), TICK_VALUES)))

    # x ticks: short dark runs just below the x axis
    below = m[xaxis[1] + 2:xaxis[1] + 9, yaxis + 3:].sum(0)
    xt = [yaxis + 3 + (a + b) / 2 for a, b in _runs(np.where(below >= 4)[0])]
    if len(xt) != len(GROUPS):
        raise ValueError(f"expected {len(GROUPS)} x ticks, found {len(xt)}")

    unc = RASTER_UNCERTAINTY_PX_300DPI  # rendered at 300 dpi, so positions are in 300-dpi pixels

    def val(row):
        v = cal.value(row)
        lo, hi = cal.interval(row, unc)
        return [v, lo - cal.residual, hi + cal.residual]

    groups = {}
    for label, cx in zip(GROUPS, xt):
        x0, x1 = int(cx) - 70, int(cx) + 70
        # horizontal lines in the group's column: rows whose longest dark run is at least 40 px wide
        rows = []
        for y in range(0, xaxis[0] - 2):
            r = _runs(np.where(m[y, max(x0, yaxis + 3):min(x1, w)])[0])
            if r and max(b - a + 1 for a, b in r) >= 40:
                rows.append(y)
        lines = []
        for a, b in _runs(rows):
            width = max(max(bb - aa + 1 for aa, bb in _runs(np.where(m[y, max(x0, yaxis + 3):min(x1, w)])[0]))
                        for y in range(a, b + 1))
            lines.append(((a + b) / 2, width))
        # the bracket above the plot (top rows) is not a group line: keep lines below the top tick
        lines = [l for l in lines if l[0] > min(ticks) + 2]
        if len(lines) != 3:
            raise ValueError(f"{label}: expected mean line and two SEM caps, found {len(lines)}")
        mean = max(lines, key=lambda l: l[1])[0]
        caps = sorted(l[0] for l in lines if l[0] != mean)
        groups[label] = {"points": [], "countable": False,
                         "bar": {"mean": val(mean), "error": val(caps[0])}}
    return {"groups": groups}
