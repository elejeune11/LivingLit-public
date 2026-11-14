"""Supplementary Fig. S8 (mmc7.pdf p. 9): heat map of log2(FC), TDI-treated vs untreated CMTs.

One raster image. A framed grid of 23 gene rows (printed order TNNT2 ... KCNJ2) by 4 columns: CMT arrays
1, 2, 3 (each from an independent differentiation) and "Avg.". Below it a framed colour key, blue to white
to red, with tick marks inside its top edge labelled -2, 0, 2, 4 (log2(FC)). Each cell's colour is inverted
against the key. Only the starred genes are read. Each array's cell is a point of the TDI group (log2 fold
change relative to its untreated counterpart); the Avg. column is returned as the mean.

A cell whose colour lies off the key cannot be inverted: ATP2A2 array 3 is pure red (the plotting program's
colour for a value beyond the key's range) and MYL2 array 3 is darker than the key's red end. Such a gene
returns the Avg. only, with no points, since the readable points would not be the whole group.
"""
import numpy as np

from livinglit.figures.source import calibrate

DPI = 300
N_ROWS, N_COLS = 23, 4  # gene rows; arrays 1-3 then Avg.
# rows of the grid in printed order (0 = TNNT2); the figure prints ACTN2 as "ACNT2"
GENES = {"MYH6": 2, "ACTN2": 4, "MYL2": 5, "JPH2": 6, "PPARA": 12, "ATP2A2": 13, "RYR2": 14, "PLN": 16,
         "SCN5A": 20, "KCNJ2": 22}
TICKS = (-2.0, 0.0, 2.0, 4.0)  # tick labels of the colour key, left to right
COLOUR_TOL = 3  # RGB units: render/resampling noise allowed around the best colour-key match
OFF_KEY = 12  # RGB units: a cell farther than this from every key colour is off the key


def _runs(idx):
    """(centre, length) of runs of consecutive indices."""
    out, start = [], None
    for i, v in enumerate(idx):
        if start is None:
            start = v
        if i == len(idx) - 1 or idx[i + 1] != v + 1:
            out.append(((start + v) / 2, v - start + 1))
            start = None
    return out


def _frame(g, rows):
    """Inner edges of a black rectangular frame within a band of image rows: (top, bottom, left, right)."""
    band = g[rows]
    H, W = band.shape
    horiz = [r for r in range(H) if (band[r] < 60).sum() > 0.2 * W]
    hb = _runs(horiz)
    (ct, wt), (cb, wb) = hb[0], hb[-1]
    top, bot = int(ct + wt / 2) + 1, int(cb - wb / 2) - 1
    vert = np.where((band[top:bot + 1] < 60).mean(axis=0) > 0.9)[0].tolist()
    vb = _runs(vert)
    (cl, wl), (cr, wr) = vb[0], vb[-1]
    return rows.start + top, rows.start + bot, int(cl + wl / 2) + 1, int(cr - wr / 2) - 1


def read(fig):
    img, scale = fig.render(DPI)
    im = img.astype(float)
    g = im.mean(axis=2)
    H, W = g.shape

    # the grid is the upper frame, the colour key the lower one: four horizontal frame edges in all
    edges = _runs(np.where((g < 60).sum(axis=1) > 0.2 * W)[0].tolist())
    if len(edges) != 4:
        raise ValueError(f"expected 4 horizontal frame edges (grid and key), found {edges}")
    split = int((edges[1][0] + edges[2][0]) / 2)
    y0, y1, x0, x1 = _frame(g, slice(0, split))
    ky0, ky1, kx0, kx1 = _frame(g, slice(split, H))
    # the key's colour band can carry a dark anti-aliased edge just inside the frame
    while im[(ky0 + ky1) // 2, kx0].max() < 150:
        kx0 += 1
    while im[(ky0 + ky1) // 2, kx1].max() < 150:
        kx1 -= 1

    # key ticks: dark runs just inside the top edge, between the colour band's ends
    y_tick = ky0 + 3
    ticks = [c for c, w in _runs([x for x in range(kx0 + 1, kx1) if g[y_tick, x] < 80])]
    if len(ticks) != len(TICKS):
        raise ValueError(f"expected {len(TICKS)} colour-key ticks, found {ticks}")
    cal = calibrate(list(zip(ticks, TICKS)))
    kmid = (ky0 + ky1) // 2
    table = np.median(im[kmid - 8:kmid + 9, kx0:kx1 + 1], axis=0)  # (n, 3)

    row_h = (y1 - y0 + 1) / N_ROWS
    col_w = (x1 - x0 + 1) / N_COLS
    unc = 0.6 * scale / (300 / 72)

    out = {}
    for gene, r in GENES.items():
        cy0, cy1 = y0 + r * row_h, y0 + (r + 1) * row_h
        cells, off = [], []
        for c in range(N_COLS):
            cx0, cx1 = x0 + c * col_w, x0 + (c + 1) * col_w
            m = 0.25
            patch = im[int(cy0 + m * row_h):int(cy1 - m * row_h), int(cx0 + m * col_w):int(cx1 - m * col_w)]
            rgb = np.median(patch.reshape(-1, 3), axis=0)
            d = np.abs(table - rgb).max(axis=1)
            best = int(np.argmin(d))
            # off the key: far from every key colour, or past one of its ends (best match at an end, not exact)
            if d[best] > OFF_KEY or (best in (0, len(d) - 1) and d[best] > COLOUR_TOL):
                off.append(c)
                cells.append(None)
                continue
            ok = np.where(d <= d[best] + COLOUR_TOL)[0]
            v = cal.value(kx0 + best)
            a, b = cal.value(kx0 + ok.min() - unc), cal.value(kx0 + ok.max() + unc)
            lo, hi = min(a, b) - cal.residual, max(a, b) + cal.residual
            at = fig.to_page((cx0 + cx1) / 2, (cy0 + cy1) / 2, scale)
            cells.append({"value": v, "lo": min(lo, v), "hi": max(hi, v), "at": [float(at[0]), float(at[1])]})
        if cells[-1] is None:
            raise ValueError(f"{gene}: Avg. cell off the colour key")
        mean = cells[-1]
        pts = cells[:-1]
        group = {"bar": {"mean": [mean["value"], mean["lo"], mean["hi"]]}}
        if off:
            group.update(points=[], countable=False)
        else:
            group.update(points=pts, countable=True)
        out[f"{gene} TDI"] = group
    return {"groups": out}
