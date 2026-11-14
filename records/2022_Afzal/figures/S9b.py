"""Fig. S9b (mmc1.pdf p. 14, raster): Tnni1 and Tnni3 relative gene expression, d30 vs CMM.

Four bars, left to right: Tnni1 d30 (orange), Tnni1 CMM (teal), Tnni3 d30, Tnni3 CMM, each with
translucent red discs (one per sample) and a dark error bar drawn over them. The y axis has major
ticks 0-4 (labels read from the panel). In the d30 bars discs overlap one another, so those bars
are read as bar only (countable: false); in the CMM bars all six discs stand alone (the error-bar
line splits two of them in half, which is not overlap) and are read as points.
"""
import numpy as np

from livinglit.figures.source import blobs, calibrate, colour_mask, dark_mask, point

DPI = 300
TICK_VALUES = [4, 3, 2, 1, 0]  # printed tick labels, top to bottom
ORANGE, TEAL = (195, 100, 0), (55, 120, 115)
LABELS = ["Tnni1 d30", "Tnni1 CMM", "Tnni3 d30", "Tnni3 CMM"]
COUNTABLE = {"Tnni1 d30": False, "Tnni1 CMM": True, "Tnni3 d30": False, "Tnni3 CMM": True}


def _runs(idx, gap=12):
    out = []
    for i in idx:
        if out and i - out[-1][1] <= gap:
            out[-1][1] = i
        else:
            out.append([i, i])
    return out


def read(fig):
    img, s = fig.render(DPI)
    I = img.astype(int)
    dark = dark_mask(img, 110)

    # y axis: the (leftmost) longest dark column; x axis: the longest dark row
    ax = int(np.argmax(dark.sum(0)))
    base = int(np.argmax(dark.sum(1)))
    # major ticks: dark rows just left of the axis line
    tick_rows = np.where(dark[:base + 4, ax - 2])[0]
    ticks = [(a + b) / 2 for a, b in _runs(tick_rows, gap=1)]
    assert len(ticks) == len(TICK_VALUES), ticks
    cal = calibrate(list(zip(ticks, TICK_VALUES)))
    unc = 0.6 + cal.residual / abs(cal.slope)  # px at 300 dpi, plus calibration misfit

    # bars, left to right, from their fill colours below the discs
    fill = colour_mask(img, ORANGE, 30) | colour_mask(img, TEAL, 30)
    lower = fill[base - 40:base - 2]
    bars = _runs([c for c in range(ax + 3, img.shape[1]) if lower[:, c].sum() > 10])
    assert len(bars) == len(LABELS), bars

    # discs: red-shifted pixels that are not the orange fill
    red = (I[:, :, 0] - I[:, :, 1] > 60) & ~colour_mask(img, ORANGE, 45)
    red[base - 1:] = False
    red[:, :ax + 3] = False

    groups = {}
    for label, (c0, c1) in zip(LABELS, bars):
        cx = (c0 + c1) / 2
        # bar top: the bar's outline, the one row above the axis that is dark across the bar's full width
        width = c1 - c0 + 1
        full = [r for r in range(base - 1) if (I[r, c0:c1 + 1].mean(1) < 85).sum() >= 0.9 * width]
        assert len(full) >= 1, (label, full)
        top = float(np.mean(_runs(full, gap=1)[-1]))
        # error bar: the dark column nearest the bar centre with the longest run; its top is the upper end
        best = None
        for c in range(int(cx) - 4, int(cx) + 5):
            col = dark[:base, c]
            for a, b in _runs(np.where(col)[0], gap=1):
                if best is None or b - a > best[2] - best[1]:
                    best = (c, a, b)
        c, a, _ = best
        cap = [r for r in range(a, a + 4) if dark[r, c - 4:c + 5].sum() >= 6]
        err = float(np.mean(cap)) if cap else float(a)
        g = {"points": [], "countable": COUNTABLE[label],
             "bar": {"mean": [cal.value(top), *cal.interval(top, unc)],
                     "error": [cal.value(err), *cal.interval(err, unc)]}}
        if COUNTABLE[label]:
            m = red.copy()
            m[:, :c0 - 8] = False
            m[:, c1 + 9:] = False
            parts = [b for b in blobs(m, min_area=30, max_area=200) if b["box"][3] <= 16]
            # rejoin halves of a disc split by the error-bar line (same rows, adjacent columns)
            discs = []
            for b in sorted(parts, key=lambda b: (b["box"][1], b["box"][0])):
                x0, y0, w, h = b["box"]
                for d in discs:
                    half = w <= 9 and d[2] - d[0] + 1 <= 9
                    gap = max(x0, d[0]) - min(x0 + w - 1, d[2])
                    if half and abs(d[1] - y0) <= 2 and 0 < gap <= 4:
                        d[0], d[1] = min(d[0], x0), min(d[1], y0)
                        d[2], d[3] = max(d[2], x0 + w - 1), max(d[3], y0 + h - 1)
                        break
                else:
                    discs.append([x0, y0, x0 + w - 1, y0 + h - 1])
            for x0, y0, x1, y1 in discs:
                assert 11 <= x1 - x0 <= 14 and 11 <= y1 - y0 <= 14, (label, x0, y0, x1, y1)
                px, py = (x0 + x1) / 2, (y0 + y1) / 2
                g["points"].append(point(cal, py, unc, fig.to_page(px, py, s)))
        groups[label] = g
    return {"groups": groups}
