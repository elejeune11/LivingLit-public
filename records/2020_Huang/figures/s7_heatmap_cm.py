"""Supplementary Fig. S7 (mmc7.pdf p. 8): heat map of log2(FC), TDI-treated vs untreated hiPSC-CM monolayers.

One raster image. Columns: 12 sets of hiPSC-CMs, then "Avg."; rows: 23 genes in the printed order
TNNT2 ... KCNJ2. Each cell's colour is inverted against the colour key (log2(FC), ticks -6, 0, 6).
A crossed cell ("no data was obtained") gives no point. Only the starred genes are read (the items
whose P a check can test from points). Each set's cell is a point of the TDI group (log2 fold change
relative to its untreated counterpart); the Avg. column is returned as the mean.
"""
import numpy as np

from livinglit.figures.source import calibrate

DPI = 300
# rows of the 23-row grid, in printed order (0 = TNNT2)
GENES = {"MYH7": 1, "MYH6": 2, "ATP2A2": 13, "PLN": 16, "CACNA1G": 18, "SCN1B": 21}
N_SETS = 12
COLOUR_TOL = 3  # RGB units: render/resampling noise allowed around the best colour-key match


def _runs(idx):
    """Centres of runs of consecutive indices."""
    out, start = [], None
    for i, v in enumerate(idx):
        if start is None:
            start = v
        if i == len(idx) - 1 or idx[i + 1] != v + 1:
            out.append(((start + v) / 2, v - start + 1))
            start = None
    return out


def _key(img, g):
    """Colour key: its framed box (bottom of the image), tick-mark positions and a per-column colour table."""
    H, W = g.shape
    dark_rows = [y for y in range(int(H * 0.8), H) if (g[y] < 60).sum() > 0.15 * W]
    top, bot = dark_rows[0], dark_rows[-1]  # the frame's top and bottom edges
    frame_rows = [y for y in dark_rows if y < top + 10]
    inner_top = max(frame_rows) + 1
    inner_bot = min(y for y in dark_rows if y > bot - 10) - 1
    mid = (inner_top + inner_bot) // 2
    edges = _runs(np.where(g[mid] < 80)[0].tolist())  # left and right frame sides
    x_lo, x_hi = int(edges[0][0] + edges[0][1] / 2) + 1, int(edges[-1][0] - edges[-1][1] / 2) - 1
    # tick marks: dark runs just inside the frame's top edge, less the frame sides' own pixels
    sides = set()
    for c, w in (edges[0], edges[-1]):
        sides.update(range(int(c - w / 2), int(c + w / 2) + 1))
    y_tick = inner_top + 3
    ticks = [c for c, w in _runs([x for x in np.where(g[y_tick] < 80)[0].tolist() if x not in sides])]
    rows = slice(mid - 8, mid + 9)
    table = np.median(img[rows, x_lo:x_hi + 1].astype(float), axis=0)  # (n, 3)
    return {"ticks": ticks, "x_lo": x_lo, "x_hi": x_hi, "table": table, "y": (top, bot)}


def _invert(rgb, key, cal, scale):
    d = np.abs(key["table"] - rgb).max(axis=1)
    best = int(np.argmin(d))
    ok = np.where(d <= d[best] + COLOUR_TOL)[0]
    pos = key["x_lo"] + best
    lo_pos, hi_pos = key["x_lo"] + ok.min(), key["x_lo"] + ok.max()
    unc = 0.6 * scale / (300 / 72)
    v = cal.value(pos)
    a, b = cal.value(lo_pos - unc), cal.value(hi_pos + unc)
    lo, hi = min(a, b) - cal.residual, max(a, b) + cal.residual
    saturated = best in (0, len(d) - 1)
    return v, min(lo, v), max(hi, v), saturated, float(d[best])


def read(fig):
    img, scale = fig.render(DPI)
    im = img.astype(float)
    g = im.mean(axis=2)
    H, W = g.shape
    key = _key(img, g)
    t = key["ticks"]
    if len(t) != 3:
        raise ValueError(f"expected 3 colour-key ticks, found {t}")
    cal = calibrate([(t[0], -6.0), (t[1], 0.0), (t[2], 6.0)])

    # grid: vertical extent from rows that are mostly non-white; columns from colour changes between cells
    top_key = key["y"][0]
    nonwhite = (g[:top_key - 20] < 250)
    full = np.where(nonwhite.sum(axis=1) > 0.45 * W)[0].tolist()
    # the cells are the longest block of such rows (the rule under "TDI groups" is a short block above)
    blocks = [(c - w / 2, c + w / 2) for c, w in _runs(full)]
    y0, y1 = max(blocks, key=lambda b: b[1] - b[0])
    y0, y1 = int(y0), int(y1) + 1
    # column edges: positions where the colour changes in most cell rows; keep the evenly spaced chain
    d = np.abs(np.diff(im[y0:y1], axis=1)).sum(axis=2) > 6
    votes = d.sum(axis=0)
    cand = [c + 0.5 for c, w in _runs(np.where(votes > 0.4 * (y1 - y0))[0].tolist())]
    gaps = np.diff(cand)
    pitch = float(np.median(gaps[gaps > 50]))
    chain = [c for c in cand if any(abs(abs(c - o) - pitch) < 3 for o in cand)]
    # an edge starts a column of cells only if the strip to its right is mostly coloured (not gene labels)
    chain = [c for c in chain if nonwhite[y0:y1, int(c) + 10:int(c + pitch) - 10].mean() > 0.5]
    edges = np.array(chain)
    k = np.round((edges - edges[0]) / pitch)
    pitch, x_left = np.polyfit(k, edges, 1)  # left edge of the first column and the column pitch
    if len(chain) != N_SETS + 1:
        raise ValueError(f"expected {N_SETS + 1} column edges, found {chain}")
    n_rows = 23
    row_h = (y1 - y0) / n_rows

    out = {}
    for gene, r in GENES.items():
        cy0, cy1 = y0 + r * row_h, y0 + (r + 1) * row_h
        pts = []
        for c in range(N_SETS + 1):
            cx0, cx1 = x_left + c * pitch, x_left + (c + 1) * pitch
            m = 0.25
            ys = slice(int(cy0 + m * row_h), int(cy1 - m * row_h))
            xs = slice(int(cx0 + m * pitch), int(cx1 - m * pitch))
            patch = im[ys, xs].reshape(-1, 3)
            if (patch.max(axis=1) < 120).mean() > 0.01:  # crossing lines (dark in every channel): no data
                continue
            rgb = np.median(patch, axis=0)
            v, lo, hi, sat, dist = _invert(rgb, key, cal, scale)
            if sat:
                raise ValueError(f"{gene} column {c}: colour beyond the key ({rgb})")
            at = fig.to_page((cx0 + cx1) / 2, (cy0 + cy1) / 2, scale)
            p = {"value": v, "lo": lo, "hi": hi, "at": [float(at[0]), float(at[1])]}
            if c < N_SETS:
                pts.append(p)
            else:
                mean = [v, lo, hi]
        out[f"{gene} TDI"] = {"points": pts, "countable": True, "bar": {"mean": mean}}
    return {"groups": out}
