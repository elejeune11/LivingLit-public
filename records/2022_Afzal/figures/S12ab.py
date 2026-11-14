"""Fig. S12b (mmc1.pdf p. 18, raster): Fura calcium transient amplitude (ΔF/F), d30 vs CMM.

Two columns of translucent discs (d30 orange, left; CMM teal, right), one per cell (n~30), with a
black mean line drawn under the discs and a faint SD whisker in the disc colour. The discs overlap
one another heavily in both columns, so neither column is countable: each group is read as its mean
only (countable: false, no points). The SD caps differ from the discs beneath them by only a few grey
levels and are not read. The y axis has six major ticks 0-2.5 (labels read from the panel).
Fig. S12a (CaTD) is not read: its means and SDs are printed beneath the panel.
"""
import numpy as np

from livinglit.figures.source import calibrate, dark_mask

DPI = 300
TICK_VALUES = [2.5, 2.0, 1.5, 1.0, 0.5, 0.0]  # printed tick labels, top to bottom
LABELS = ["d30", "CMM"]  # left to right


def _runs(idx, gap=1):
    out = []
    for i in idx:
        if out and i - out[-1][1] <= gap:
            out[-1][1] = i
        else:
            out.append([i, i])
    return out


def read(fig):
    img, _ = fig.render(DPI)
    I = img.astype(int)
    dark = dark_mask(img, 110)

    # y axis: the longest dark column; x axis: the longest dark row
    ax = int(np.argmax(dark.sum(0)))
    base = int(np.argmax(dark.sum(1)))
    tick_rows = np.where(dark[:base + 4, ax - 3])[0]
    ticks = [(a + b) / 2 for a, b in _runs(tick_rows)]
    assert len(ticks) == len(TICK_VALUES), ticks
    cal = calibrate(list(zip(ticks, TICK_VALUES)))
    unc = 0.6 + cal.residual / abs(cal.slope)  # px at 300 dpi, plus calibration misfit

    # mean lines: near-black horizontal segments right of the axis (the axis line itself is excluded)
    black = I.max(2) < 100
    black[:, :ax + 6] = False
    black[base - 3:] = False
    # (legend text is taller than a line and is dropped by the thickness test)
    rows = [r for r in range(base) if black[r].sum() >= 8]
    lines = []
    for a, b in _runs(rows):
        cols = np.where(black[a:b + 1].any(0))[0]
        if 2 <= b - a <= 5 and 45 <= cols.max() - cols.min() <= 75:
            lines.append((a, b, int(cols.min()), int(cols.max())))
    lines.sort(key=lambda t: t[2])
    assert len(lines) == len(LABELS), lines

    groups = {}
    for label, (a, b, c0, c1) in zip(LABELS, lines):
        # line centre: darkness-weighted row over the line's columns that no disc covers (white just above and below)
        ends = [c for c in range(c0, c1 + 1) if I[a - 2, c].min() > 200 and I[b + 2, c].min() > 200]
        assert len(ends) >= 2, (label, ends)
        r = np.arange(a - 2, b + 3)
        w = (255 - I[a - 2:b + 3][:, ends].max(2)).sum(1).astype(float)
        y = float((r * w).sum() / w.sum())
        groups[label] = {"points": [], "countable": False,
                         "bar": {"mean": [cal.value(y), *cal.interval(y, unc)]}}
    return {"groups": groups}
