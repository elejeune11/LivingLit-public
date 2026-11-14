"""Fig. 5e (random cluster) and 5g (iCMF): relative % variation of the peak interval to the input, journal p. 7.

The figure is one embedded raster image (1497 px across 359.3 pt, i.e. 300 dpi), so both panels are read
from a 300 dpi render of one crop holding e (top) and g (bottom). Fig. 5d and 5f (intervals) are bars
without points and are not read.

Axis: each panel's y axis carries 16 tick marks (0 to 150 by 10, image text); they are the dark short
strokes left of the axis, located by darkness-weighted row centres and fitted by calibrate().

Groups: one column per pacing frequency, centred on the x-axis tick marks below each panel. Each column
holds N = 4 markers in the group colour, a wide black mean line and the error bar.
- mean: the rows where the black mean line reaches both of its outer ends (black at +-OUTER px from the
  column centre, where neither caps nor markers reach); its centre is the mean of those rows.
- error (panel e only): the caps are black and narrower than the mean line; the upper cap is the topmost
  run of rows above the mean line that are black at +-CAP px but not at +-OUTER px; its centre is the mean
  of those rows. Where the cap touches the mean line (e 0.5 Hz) only its uncovered rows are seen.
  In panel g the error bars are drawn in the group colour over the markers and are not read.
- points: read only where every one of the column's markers stands alone (countable). This holds for
  e 5 Hz alone: three diamonds stand free and the fourth is crossed by the black error-bar line, which
  leaves two slivers either side of it at one height; their mean row is taken as its centre, with one
  extra pixel of interval. Every other column has markers overlapping each other or the mean line
  (and in g 2 Hz black markers on black lines), so it returns its bar only (countable False).
The legends (markers and black text, above the 3 Hz to 7 Hz columns in g) are blanked before reading.
Intervals: 0.6 px + calibration misfit + 1 px (stroke rows partly anti-aliased).
"""
import numpy as np

from livinglit.figures.source import RASTER_UNCERTAINTY_PX_300DPI, blobs, calibrate, colour_mask, point

DPI = 300
TICK_VALUES = list(range(150, -1, -10))  # top to bottom, as printed on both axes
STROKE_PX = 1.0
OCCLUDED_PX = 1.0
# legend colours (RGB) sampled from the render
COLOURS = {"0.5 Hz": (70, 12, 137), "1 Hz": (0, 42, 254), "2 Hz": (0, 247, 0), "3 Hz": (208, 250, 110),
           "5 Hz": (255, 139, 0), "6 Hz": (255, 33, 0), "7 Hz": (255, 62, 254)}
PANELS = {  # panel: (rows of the plot, labels left to right, half-widths: OUTER (mean line end), CAP, column)
    "e": ((60, 372), ["0.5 Hz", "1 Hz", "2 Hz", "3 Hz", "5 Hz"], 24, 12, 38),
    "g": ((540, 860), ["0.5 Hz", "1 Hz", "2 Hz", "3 Hz", "5 Hz", "6 Hz", "7 Hz"], 17, None, 28),
}
LEGEND = {"e": (160, 80, 265, 255), "g": (380, 545, 600, 775)}  # crop px (x0, y0, x1, y1), blanked
COUNTABLE = {("e", "5 Hz")}
N = 4


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


def _y_axis(dm, r0, r1):
    """First column of the panel's y axis: the leftmost dark column spanning most of the plot rows."""
    cols = np.where(dm[r0:r1].sum(0) > 0.8 * (r1 - r0))[0]
    return int(cols[0])


def _ticks(grey, r0, r1, ax0):
    """Row centres of the tick marks left of the axis (darkness-weighted)."""
    prof = grey[r0:r1, ax0 - 7:ax0 - 1].mean(1)
    out = []
    for r in _runs(np.where(prof > 40)[0]):
        w = prof[r]
        out.append(r0 + float((np.array(r) * w).sum() / w.sum()))
    return out


def _x_centres(dm, row, x0):
    """Column centres of the x-axis tick marks just below the axis line."""
    return [x0 + float(np.mean(r)) for r in _runs(np.where(dm[row, x0:])[0]) if len(r) <= 6]


def _triple(cal, row, unc):
    v = cal.value(row)
    lo, hi = cal.interval(row, unc)
    return [v, min(lo, v), max(hi, v)]


def read(fig):
    img, _ = fig.render(DPI)
    scale = DPI / 72.0
    grey = 255 - img.astype(float).mean(2)
    dm = img.astype(int).max(2) < 90  # black (the coloured markers all have a channel above 90)
    for x0, y0, x1, y1 in LEGEND.values():
        img[y0:y1, x0:x1] = 255
        dm[y0:y1, x0:x1] = False
    out = {}
    for panel, ((r0, r1), labels, outer, cap, half) in PANELS.items():
        ax0 = _y_axis(dm, r0 + 20, r1 - 20)
        ticks = _ticks(grey, r0, r1, ax0)
        if len(ticks) != len(TICK_VALUES):
            raise ValueError(f"panel {panel}: found {len(ticks)} tick marks")
        cal = calibrate(list(zip(ticks, TICK_VALUES)))
        unc = RASTER_UNCERTAINTY_PX_300DPI + cal.residual / abs(cal.slope) + STROKE_PX
        base = int(round(ticks[-1]))
        centres = _x_centres(dm, base + 4, ax0 + 10)
        if len(centres) != len(labels):
            raise ValueError(f"panel {panel}: found {len(centres)} x tick marks for {len(labels)} groups")
        for label, xc in zip(labels, centres):
            c = int(round(xc))
            band = slice(r0, base - 2)
            ends = dm[band, c - outer - 1:c - outer + 2].any(1) & dm[band, c + outer - 1:c + outer + 2].any(1)
            mean_runs = _runs(np.where(ends)[0])
            if not mean_runs:
                raise ValueError(f"panel {panel} {label}: no mean line")
            mean_rows = max(mean_runs, key=len)
            mean_row = r0 + float(np.mean(mean_rows))
            bar = {"mean": _triple(cal, mean_row, unc)}
            if cap is not None:
                capped = dm[band, c - cap] & dm[band, c + cap] & ~ends
                above = [i for i in np.where(capped)[0] if i < mean_rows[0]]
                caps = _runs(above)
                if caps:
                    bar["error"] = _triple(cal, r0 + float(np.mean(caps[0])), unc)
            points = []
            countable = (panel, label) in COUNTABLE
            if countable:
                m = colour_mask(img, COLOURS[label], 50)
                m[:r0] = False
                m[base - 2:] = False
                m[:, :c - half] = False
                m[:, c + half + 1:] = False
                found = blobs(m, 3)
                whole = [(b["x"], b["y"], 0.0) for b in found if b["area"] >= 30]
                slivers = sorted((b for b in found if b["area"] < 30), key=lambda b: b["y"])
                for grp in _runs([int(round(b["y"])) for b in slivers], gap=2):
                    ys = [b["y"] for b in slivers if int(round(b["y"])) in grp]
                    xs = [b["x"] for b in slivers if int(round(b["y"])) in grp]
                    if len(ys) == 2 and min(xs) < c < max(xs):  # one marker split by the error-bar line
                        whole.append((float(np.mean(xs)), float(np.mean(ys)), OCCLUDED_PX))
                    else:
                        raise ValueError(f"panel {panel} {label}: marker fragment not split by the error line")
                if len(whole) != N:
                    raise ValueError(f"panel {panel} {label}: {len(whole)} markers, legend N = {N}")
                for x, y, extra in sorted(whole, key=lambda t: (t[1], t[0])):
                    points.append(point(cal, y, unc + extra, fig.to_page(x, y, scale)))
            out[f"{panel}:{label}"] = {"points": points, "countable": countable, "bar": bar}
    return {"groups": out}
