"""Fig. 1b: heat map of gene expression (log2 fold change), vector cells read against the raster colour bar.

Cells are vector rectangles (each drawn as a black frame plus a smaller coloured fill; the fill is used). Rows are
FCT, adult, early control/constant/intensity, late control/constant/intensity (top to bottom); columns fall into five
gene blocks separated by gaps (conduction, maturation, structural, energetics, calcium handling), in the gene order
of each item's measure. The colour bar (an embedded image) is sampled along its middle row and calibrated on its
tick labels (-4 ... 4, text words); a cell's value is the bar position of the nearest colour, its interval the
span of bar positions within 6 RGB units of that best match (plus 0.5 pt). Each cell is a point at x = the gene's
1-based position in its block (cells of one group are genes, not replicates)."""
import numpy as np

from livinglit.figures.source import calibrate

ROWS = ["fct", "adult", "e_ctrl", "e_const", "e_int", "l_ctrl", "l_const", "l_int"]
BLOCKS = ["F1b_conduction", "F1b_maturation", "F1b_structural", "F1b_energetics", "F1b_calcium"]
SIZES = {"F1b_conduction": 10, "F1b_maturation": 4, "F1b_structural": 9, "F1b_energetics": 6, "F1b_calcium": 10}
LINKS = {b: ROWS for b in BLOCKS}
BAR_Y = (278.2, 286.5)      # the colour-bar image's vertical extent (page points)


def _clusters(vals, gap):
    vals = sorted(vals)
    out = [[vals[0]]]
    for v in vals[1:]:
        (out[-1] if v - out[-1][-1] < gap else out.append([v]) or out[-1]).append(v)
    return [float(np.mean(c)) for c in out]


def read(fig):
    # 1. cells: per centre keep the smaller filled rectangle (the coloured fill inside the black frame)
    cells = {}
    for d in fig.drawings():
        r, f = d["rect"], d.get("fill")
        if f is None or not (6 < r.width < 10 and 6 < r.height < 10) or r.y0 > BAR_Y[0] - 2:
            continue
        key = (round((r.x0 + r.x1) / 2 * 2) / 2, round((r.y0 + r.y1) / 2 * 2) / 2)
        area = r.width * r.height
        if key not in cells or area < cells[key][0]:
            cells[key] = (area, tuple(255 * c for c in f))
    ys = _clusters([k[1] for k in cells], 3)
    xs = _clusters([k[0] for k in cells], 3)
    if len(ys) != len(ROWS):
        raise ValueError(f"found {len(ys)} rows")
    blocks, cur = [], [xs[0]]
    for a, b in zip(xs, xs[1:]):
        if b - a > 9.5:
            blocks.append(cur)
            cur = []
        cur.append(b)
    blocks.append(cur)
    if [len(b) for b in blocks] != [SIZES[b] for b in BLOCKS]:
        raise ValueError(f"block sizes {[len(b) for b in blocks]}")
    # 2. colour bar: tick labels (words) calibrate x; sample the middle row of the bar image
    marks = []
    for x0, y0, x1, y1, t in fig.words():
        if y0 > BAR_Y[1] - 2 and y1 < BAR_Y[1] + 9 and x0 > 390:
            try:
                marks.append(((x0 + x1) / 2, float(t.replace("–", "-").replace("−", "-"))))
            except ValueError:
                pass
    if sorted(v for _, v in marks) != [-4, -2, 0, 2, 4]:
        raise ValueError(f"colour bar labels {marks}")
    cal = calibrate(marks)
    img, scale = fig.render(600)
    row = int(((BAR_Y[0] + BAR_Y[1]) / 2 - fig.crop[1]) * scale)
    xa = int((394.9 - fig.crop[0]) * scale)
    xb = int((463.0 - fig.crop[0]) * scale)
    grad = img[row - 2:row + 3, xa:xb].astype(float).mean(axis=0)
    gx = fig.crop[0] + (np.arange(xa, xb) + 0.5) / scale
    gv = np.array([cal.value(x) for x in gx])
    res = abs(cal.residual / cal.slope)
    # 3. each cell against the bar
    groups = {}
    for bi, item in enumerate(BLOCKS):
        for ri, g in enumerate(ROWS):
            pts = []
            for ci, x in enumerate(blocks[bi]):
                key = min(cells, key=lambda k: abs(k[0] - x) + abs(k[1] - ys[ri]))
                rgb = np.array(cells[key][1])
                dist = np.abs(grad - rgb).sum(axis=1)
                ok = dist <= dist.min() + 6
                j = int(dist.argmin())
                lo_x, hi_x = gx[ok].min() - 0.5 - res, gx[ok].max() + 0.5 + res
                v, lo, hi = float(gv[j]), float(cal.value(lo_x)), float(cal.value(hi_x))
                pts.append({"value": v, "lo": min(lo, v), "hi": max(hi, v), "at": [key[0], key[1]], "x": ci + 1})
            groups[f"{item}/{g}"] = {"points": pts, "countable": False}
    return {"groups": groups}
