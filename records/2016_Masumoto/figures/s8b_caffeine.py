"""Supplementary Fig. 8b (right): active force increase on 5 mM caffeine (%) by ECT type, a bar chart in a raster image.

The y axis is calibrated on its seven tick marks (printed labels bottom to top: 0, 10, ..., 60, unit "(%)"; the 0 tick
is the left end of the x axis line). Three bars, blue CM+EC, green CM+MC, red CM+EC+MC (left to right, as labelled
under the axis), each with an upward error bar (stem and cap, black). The bar's mean is its top edge: the row where the
bar's colour covers half its width, interpolated over the edge's antialiased rows (stem columns skipped). The error is
the cap's darkness-weighted centre. Intervals: raster uncertainty plus calibration misfit. Bars only: no points are
drawn, so nothing is countable. The left panel (a representative force trace) is not read.
"""
import numpy as np

from livinglit.figures.source import RASTER_UNCERTAINTY_PX_300DPI, calibrate

DPI = 300
TICK_VALUES = [0, 10, 20, 30, 40, 50, 60]  # bottom to top
BARS = ("ce", "cm", "cem")  # left to right


def _runs(idx):
    out, cur = [], []
    for i in idx:
        if cur and i != cur[-1] + 1:
            out.append(cur)
            cur = []
        cur.append(int(i))
    if cur:
        out.append(cur)
    return out


def _masks(img):
    a = img.astype(int)
    sat = a.max(2) - a.min(2)
    gray = (sat < 50) & (a.mean(2) < 140)
    colour = sat >= 60
    return gray, colour


def _centre(dark, rows, cols):
    """Darkness-weighted centre (px, pixel centres at r + 0.5) of a horizontal line over rows (one past each end)."""
    rr = np.arange(rows[0] - 1, rows[-1] + 2)
    w = dark[rr][:, cols].sum(1)
    return float((w * (rr + 0.5)).sum() / w.sum())


def _longest(v):
    return max(_runs(np.where(v)[0]), key=len, default=[])


def read(fig):
    img, scale = fig.render(DPI)
    gray, colour = _masks(img)
    dark = 255.0 - img.astype(float).mean(2)
    h, w = gray.shape

    # y axis: the leftmost long vertical dark run in the left third
    ax_cols = [(x, _longest(gray[:, x])) for x in range(w // 3)]
    ax_cols = [(x, r) for x, r in ax_cols if len(r) >= 0.5 * h]
    if not ax_cols:
        raise ValueError("no y axis found")
    ax_left = min(x for x, _ in ax_cols)
    ax_top = min(r[0] for _, r in ax_cols)
    ax_bottom = max(r[-1] for _, r in ax_cols)

    # ticks: short dark runs just left of the axis
    tick_cols = list(range(ax_left - 6, ax_left - 1))
    tick_rows = np.where(gray[ax_top - 3:ax_bottom + 3, tick_cols].all(1))[0] + ax_top - 3
    ticks = sorted((_centre(dark, r, tick_cols) for r in _runs(tick_rows) if 2 <= len(r) <= 10), reverse=True)
    if len(ticks) != len(TICK_VALUES):
        raise ValueError(f"found {len(ticks)} y ticks, expected {len(TICK_VALUES)}")
    ticks_pt = [fig.to_page(0, y, scale)[1] for y in ticks]
    cal = calibrate(list(zip(ticks_pt, TICK_VALUES)))
    zero_px = ticks[0]

    # bars: column runs right of the axis where the coloured mask fills the region just above the x axis
    probe = int(zero_px) - 10
    bar_cols = _runs([c for c in range(ax_left + 5, w) if colour[probe - 5:probe, c].all()])
    bar_cols = [c for c in bar_cols if len(c) >= 40]
    if len(bar_cols) != len(BARS):
        raise ValueError(f"found {len(bar_cols)} bars, expected {len(BARS)}")

    unc = RASTER_UNCERTAINTY_PX_300DPI / scale + cal.residual / abs(cal.slope)

    def value(y_px, x_px):
        ypt = fig.to_page(x_px, y_px, scale)[1]
        v = cal.value(ypt)
        lo, hi = cal.interval(ypt, unc)
        return [v, min(lo, v), max(hi, v)]

    groups = {}
    for label, cols in zip(BARS, bar_cols):
        cx = (cols[0] + cols[-1] + 1) / 2
        inner = list(cols[4:-4])
        frac = colour[:, inner].mean(1)
        body = _longest(frac >= 0.95)  # rows fully coloured, ending at the x axis
        if not body or body[-1] < probe - 5:
            raise ValueError(f"{label}: bar body not found")
        top = body[0]
        stem_cols = [c for c in inner if gray[top - 15:top - 3, c].all()]
        if not stem_cols:
            raise ValueError(f"{label}: no error stem above the bar")
        side = [c for c in inner if abs(c - (stem_cols[0] + stem_cols[-1]) / 2) > len(stem_cols) / 2 + 4]
        fs = colour[top - 6:top + 1, side].mean(1)  # partial coverage on the edge rows
        edge = top + 1 - fs.sum()  # px: rows fully coloured below, fractional ones above
        mean = value(edge, cx)

        # cap: the topmost dark horizontal run across the stem, wider than the stem
        stem_c = (stem_cols[0] + stem_cols[-1] + 1) / 2
        c0, c1 = int(stem_c) - 30, int(stem_c) + 30
        stem_top = _longest(gray[:top, int(stem_c)])[0]
        cap_rows = [r for r in range(stem_top - 2, stem_top + 15) if gray[r, c0:c1].sum() >= 2 * len(stem_cols) + 10]
        caps = _runs(cap_rows)
        if not caps:
            raise ValueError(f"{label}: no error cap")
        cap = caps[0]
        cap_cols = [c for c in range(c0, c1) if gray[cap[0]:cap[-1] + 1, c].any() and c not in stem_cols]
        err = value(_centre(dark, cap, cap_cols), stem_c)
        if not err[0] > mean[0]:
            raise ValueError(f"{label}: cap not above the bar top")
        groups[label] = {"points": [], "countable": False, "bar": {"mean": mean, "error": err}}
    return {"groups": groups}
