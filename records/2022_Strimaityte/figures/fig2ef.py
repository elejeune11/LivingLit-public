"""Fig. 2e (contraction velocity) and 2f (relaxation velocity), journal p. 3: raster bar charts.

The page carries one embedded image (1254 px across 300.9 pt, i.e. 300 dpi), so the panels are read from a
300 dpi render. Each group plots 60-80 translucent markers that overlap heavily (many stack at 0), so no
marker or count is read (countable False): each group returns its bar mean and the upper end of its error
bar only.

Axis: the four y tick marks of each panel (0, 5, 10, 15 μm/s; the labels are image text) are the dark short
strokes left of each y axis, located by darkness-weighted row centres and fitted by calibrate().

Bars: each bar is outlined in its group colour; the markers are drawn over the bar and often hide its top
edge, while the error bar (vertical line and caps) is drawn over the markers.
- mean: the top row of the bar's top stroke where that stroke is seen reaching a corner of the bar (the
  stroke is drawn inside the bar: in 2f Micropatterned single, where both are seen, its top row lies within
  1 px of the midpoint of the two caps); otherwise the midpoint of the error bar's two cap centres
  (error bars taken as symmetric). Interval: 0.6 px + calibration misfit + 2 px (half a stroke).
- error: the centre of the upper cap (top of the vertical error line plus half the cap's thickness);
  same interval. Not returned where no error bar of the group colour is seen.
"""
import numpy as np

from livinglit.figures.source import RASTER_UNCERTAINTY_PX_300DPI, calibrate, colour_mask, dark_mask

DPI = 300
TICK_VALUES = [15, 10, 5, 0]  # top to bottom, as printed on both axes
STROKE_HALF_PX = 2.0
# bar outline colours (RGB) sampled from the render; 2f iCMF is outlined in a lighter green
COLOURS = {"Random Single": (51, 105, 166), "Random Cluster": (100, 65, 162),
           "Micropatterned single": (168, 50, 163), "iCMF": (101, 161, 52)}
COLOUR_OVERRIDE = {("f", "iCMF"): (138, 182, 102)}
TOL = 35


def _runs(idx, gap=1):
    if len(idx) == 0:
        return []
    runs, cur = [], [int(idx[0])]
    for c in idx[1:]:
        if c - cur[-1] <= gap:
            cur.append(int(c))
        else:
            runs.append(cur)
            cur = [int(c)]
    runs.append(cur)
    return runs


def _y_axes(img):
    """Column ranges of the two y axes: dark vertical lines spanning most of the crop."""
    dm = dark_mask(img, 80)
    cols = np.where(dm.sum(0) > 0.7 * img.shape[0])[0]
    return [(r[0], r[-1]) for r in _runs(cols)]


def _ticks(img, ax0):
    """Row centres of the tick marks left of an axis (darkness-weighted)."""
    prof = 255 - img.astype(float).mean(2)[:, ax0 - 9:ax0 - 1].mean(1)
    out = []
    for r in _runs(np.where(prof > 56)[0]):
        w = prof[r]
        out.append(float((np.array(r) * w).sum() / w.sum()))
    return out


def _sides(m, x_lo, x_hi, base):
    """Outer columns of the bar: the first and last columns holding a vertical run (> 8 px) of its colour."""
    sub = m[:base - 3, x_lo:x_hi]
    longest = np.zeros(sub.shape[1], int)
    for j in range(sub.shape[1]):
        best = cur = 0
        for v in sub[:, j]:
            cur = cur + 1 if v else 0
            best = max(best, cur)
        longest[j] = best
    runs = _runs(np.where(longest > 8)[0])
    return x_lo + int(round(np.mean(runs[0]))), x_lo + int(round(np.mean(runs[-1])))


def _bar(img, colour, x_lo, x_hi, base):
    """(x0, x1), mean row or None, upper-cap row or None (px)."""
    m = colour_mask(img, colour, TOL)
    x0, x1 = _sides(m, x_lo, x_hi, base)
    inner = m[:, x0 + 4:x1 - 3]
    width = inner.shape[1]
    cov = inner.sum(1)
    top_row = None
    for r in _runs([i for i in range(base - 4) if cov[i] >= 12]):
        cols = np.where(inner[r[0]:r[-1] + 1].any(0))[0]
        if cols.min() <= 5 or cols.max() >= width - 6:  # the band reaches a corner: the bar's top stroke
            top_row = float(r[0])
            break
    # error bar: vertical run of the colour at the bar centre (any of three central columns)
    xc = (x0 + x1) // 2
    ctr = m[:base - 2, xc - 1:xc + 2].all(1) | m[:base - 2, xc:xc + 1].any(1)
    runs = _runs(np.where(ctr)[0])
    cap_hi = cap_lo = None
    if runs:
        run = max(runs, key=len)
        caprow = [i for i in range(run[0], run[-1] + 1) if cov[i] >= 12]
        upper = _runs(caprow)[0] if caprow else [run[0]]
        thick = len(upper)
        cap_hi = run[0] + (thick - 1) / 2
        cap_lo = run[-1] - (thick - 1) / 2
    mean_row = top_row if top_row is not None else (None if cap_hi is None else (cap_hi + cap_lo) / 2)
    if cap_hi is not None and mean_row is not None and cap_hi >= mean_row - 2:
        cap_hi = None  # a run that does not rise above the bar is marker edges, not an error bar
    return (x0, x1), mean_row, cap_hi


def _triple(cal, row, unc):
    v = cal.value(row)
    lo, hi = cal.interval(row, unc)
    return [v, min(lo, v), max(hi, v)]


def read(fig):
    img, _ = fig.render(DPI)
    axes = _y_axes(img)
    out = {}
    for panel, (a0, a1) in zip("ef", axes):
        ticks = _ticks(img, a0)
        if len(ticks) != len(TICK_VALUES):
            raise ValueError(f"panel {panel}: found {len(ticks)} tick marks")
        cal = calibrate(list(zip(ticks, TICK_VALUES)))
        unc = RASTER_UNCERTAINTY_PX_300DPI + cal.residual / abs(cal.slope) + STROKE_HALF_PX
        base = int(round(ticks[-1]))
        x_hi = axes[1][0] - 60 if panel == "e" else img.shape[1]
        x_lo = a1 + 3
        for label, colour in COLOURS.items():
            colour = COLOUR_OVERRIDE.get((panel, label), colour)
            (x0, x1), mean_row, cap_row = _bar(img, colour, x_lo, x_hi, base)
            bar = {}
            if mean_row is not None:
                bar["mean"] = _triple(cal, mean_row, unc)
            if cap_row is not None:
                bar["error"] = _triple(cal, cap_row, unc)
            out[f"{panel}:{label}"] = {"points": [], "countable": False, "bar": bar}
            x_lo = x1 + 5
    return {"groups": out}
