"""Fig. 2d: enrichment of gene processes (CM+EC+MC versus CM+EC), two horizontal bar charts in a raster image.

Each chart has its axis at the top (printed title "-log(pValue)"), tick marks drawn upward from the axis line, and bars
drawn as dark-outlined white rectangles starting at the 0 tick, one per process, with "genes/total" printed inside.
Left chart: GO processes, ticks 0, 5, 10, 15, 20. Right chart: pathway maps / process networks, ticks 0, 1, 2, ...
(one per unit). The value of a bar is the page position of the centre of its right outline, read on the axis
calibrated on its tick marks. One value per bar (the enrichment -log p of the comparison); nothing is countable.
"""
import numpy as np

from livinglit.figures.source import RASTER_UNCERTAINTY_PX_300DPI, calibrate

DPI = 300
# bar order top to bottom, as printed beside the bars
LEFT = ["muscle_structure", "cv_system", "cardiac_muscle_tissue", "heart_dev", "myofibril", "cardiac_muscle_cell",
        "blood_vessel", "cardiac_cell"]
RIGHT = ["muscle_contract", "cytoskeleton", "fgf_erbb", "wnt_notch", "bmp_tgfb"]
LEFT_STEP, RIGHT_STEP = 5, 1  # printed tick labels: 0, 5, 10, 15, 20 and 0, 1, 2, ...


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


def _segments(dark, min_len):
    """Horizontal dark lines at least min_len px long: (first row, last row, first col, last col)."""
    segs = []
    for r in range(dark.shape[0]):
        for run in _runs(np.where(dark[r])[0]):
            if len(run) >= min_len:
                for s in segs:
                    if s[1] == r - 1 and abs(s[2] - run[0]) <= 3 and abs(s[3] - run[-1]) <= 3:
                        s[1] = r
                        break
                else:
                    segs.append([r, r, run[0], run[-1]])
    return segs


def _ticks(dark, inten, seg):
    """Tick centres (px columns): columns dark over the rows just above the axis line, within its extent."""
    top, c0, c1 = seg[0], seg[2], seg[3]
    band = slice(top - 6, top - 1)
    cols = [c for c in range(c0, c1 + 1) if dark[band, c].all()]
    out = []
    for run in _runs(cols):
        if len(run) > 8:
            continue
        cc = np.arange(run[0] - 1, run[-1] + 2)
        w = (255.0 - inten[band][:, cc]).sum(0)
        out.append(float((w * (cc + 0.5)).sum() / w.sum()))
    return out


def _edge(inten, rows, cols):
    """Darkness-weighted centre (px) of a vertical line over the given rows, within cols (one past each end)."""
    cc = np.arange(cols[0] - 1, cols[-1] + 2)
    w = (255.0 - inten[rows][:, cc]).mean(0)
    w = np.clip(w - w.min(), 0, None)
    return float((w * (cc + 0.5)).sum() / w.sum())


def _bars(dark, inten, seg, x0, n):
    """(top row, bottom row, left edge px, right edge px) of each bar below an axis, top to bottom."""
    bottom = seg[1]
    probe = int(round(x0)) + 6
    rows = [r for r in _runs(np.where(dark[bottom + 3:, probe])[0] + bottom + 3) if len(r) <= 6]
    if len(rows) != 2 * n:
        raise ValueError(f"expected {2 * n} bar outlines at column {probe}, found {len(rows)}")
    bars = []
    for top_line, bot_line in zip(rows[0::2], rows[1::2]):
        inner = np.arange(top_line[-1] + 2, bot_line[0] - 1)
        full = dark[inner][:, int(round(x0)) - 6:seg[3] + 8].mean(0) >= 0.8
        cols = [c + int(round(x0)) - 6 for c in np.where(full)[0]]
        lines = _runs(cols)
        if len(lines) < 2:
            raise ValueError(f"bar at rows {top_line[0]}-{bot_line[-1]}: outline not found")
        bars.append((top_line[0], bot_line[-1], _edge(inten, inner, lines[0]), _edge(inten, inner, lines[-1])))
    return bars


def read(fig):
    img, scale = fig.render(DPI)
    inten = img.astype(float).mean(2)
    dark = inten < 128
    axes = []
    for seg in _segments(dark, 150):
        ticks = _ticks(dark, inten, seg)
        if len(ticks) >= 5:
            axes.append((seg, ticks))
    if len(axes) != 2:
        raise ValueError(f"expected 2 axes with tick marks, found {len(axes)}")
    axes.sort(key=lambda a: a[0][2])
    unc_px = RASTER_UNCERTAINTY_PX_300DPI * DPI / 300
    groups = {}
    for (seg, ticks), names, step in ((axes[0], LEFT, LEFT_STEP), (axes[1], RIGHT, RIGHT_STEP)):
        ticks_pt = [fig.to_page(x, 0, scale)[0] for x in sorted(ticks)]
        cal = calibrate([(x, i * step) for i, x in enumerate(ticks_pt)])
        unc = unc_px / scale + cal.residual / abs(cal.slope)
        for name, (_, _, left, right) in zip(names, _bars(dark, inten, seg, sorted(ticks)[0], len(names))):
            xpt = fig.to_page(right, 0, scale)[0]
            v = cal.value(xpt)
            lo, hi = cal.interval(xpt, unc)
            groups[name] = {"points": [], "countable": False, "bar": {"mean": [v, min(lo, v), max(hi, v)]}}
    return {"groups": groups}
