"""Fig. 3d (author manuscript, p. 22): histogram of cardiomyocyte maturation genes by expression level (RPKM)
relative to fetal heart; 2D D22 (grey), 2D D60 (blue), 6 week EHM (red).

The panel is a raster image (~300 dpi). Each group is a filled frequency polygon with a black outline; the fills
overlap (red over grey over blue) and the outlines are drawn over every fill. The y axis (number of cardiomyocyte
specific genes, ticks 0-80) is calibrated from its tick stubs. The x axis has no numeric scale: only the dashed
"Fetal heart" line, with "Embryonic-Fetal" to its left and "Fetal-Adult" to its right. So x is the horizontal
offset from the dashed line in page points (negative: Embryonic-Fetal side), sampled every 1 pt; it is a page
position, not an expression level.

Each outline is the centre of a dark run in a pixel column, named by the fill on either side of it:
- EHM (red): the topmost dark run with red below and no red above.
- 2D D60 (blue): a run with blue below (where blue is the highest curve); a run with grey on both sides (blue is
  under grey and only its outline shows); right of the dashed line, the upper of exactly two runs inside the red
  fill (grey's outline is the lower one). Where the two runs inside red merge (the outlines cross) and beyond,
  which outline is which is not determined, so D60 is not read there. Columns where outlines touch, the dashed
  line, and the bottom few px above the x axis are skipped.
"""
import numpy as np

from livinglit.figures.source import calibrate, point

DPI = 600
UNC_PX = 0.6 * DPI / 300          # 0.6 px at 300 dpi, in px at DPI
TICKS = [0, 20, 40, 60, 80]       # printed y tick labels, bottom to top
DARK = 70                         # mean grey level below which a pixel is outline
STEP_PT = 1.0                     # sampling step along x, page points
BASE_PX = 10                      # runs this close to the x axis are not read (outlines merge with the axis)


def _classes(img):
    g = img.astype(int)
    r, gg, b = g[..., 0], g[..., 1], g[..., 2]
    grey = (np.abs(r - gg) < 20) & (np.abs(gg - b) < 20)
    c = np.full(r.shape, "?", dtype="<U1")
    c[(r > 200) & (gg < 80) & (b < 80)] = "R"
    c[(b > 200) & (r < 80) & (gg < 80)] = "B"
    c[grey & (r >= 110) & (r <= 160)] = "g"
    c[grey & (r > 220)] = "."
    c[g.mean(axis=2) < DARK] = "k"
    return c


def _runs(col, top, bottom):
    """Dark runs (centre, start, end) in one column between rows top and bottom, with the fill above and below.
    Anti-aliased pixels ('?') between dark pixels of one run (up to 3) are joined into it."""
    out, y = [], top
    while y < bottom:
        if col[y] != "k":
            y += 1
            continue
        s = e = y
        while e + 1 < bottom and (col[e + 1] == "k" or ("k" in col[e + 2:e + 5] and col[e + 1] == "?")):
            e += 1
        a = s - 1
        while a > top and col[a] in "?k":
            a -= 1
        b = e + 1
        while b < bottom and col[b] in "?k":
            b += 1
        out.append({"y": (s + e) / 2, "s": s, "e": e, "above": col[a], "below": col[b] if b < bottom else "?"})
        y = e + 1
    return out


def _axes(c):
    dark = c == "k"
    col = dark.sum(0)
    ax = int(np.argmax(col))                       # y axis: the longest dark column
    while ax > 0 and col[ax - 1] > 0.8 * col[ax]:
        ax -= 1
    stub = dark[:, ax - 8:ax - 2].all(axis=1)      # tick stubs to the left of the axis
    rows = np.flatnonzero(stub)
    ticks = [float(g.mean()) for g in np.split(rows, np.flatnonzero(np.diff(rows) > 1) + 1) if len(g)]
    row = dark[:, ax + 20:].sum(1)
    base = int(np.argmax(row))                     # x axis: the longest dark row
    while base > 0 and row[base - 1] > 0.8 * row[base]:
        base -= 1
    return ax, ticks, base


def _dashed(c, ax, top, base):
    """The dashed 'Fetal heart' line: the column right of the y axis with most dark pixels above the x axis."""
    dark = (c[top:base - 2, ax + 20:] == "k").sum(0)
    x = int(np.argmax(dark))
    cols = np.flatnonzero(dark >= 0.8 * dark[x])
    cols = cols[np.abs(cols - x) <= 6]
    return ax + 20 + float(cols.mean()), (ax + 20 + cols.min(), ax + 20 + cols.max())


def read(fig):
    img, s = fig.render(DPI)
    c = _classes(img)
    ax, ticks, base = _axes(c)
    if len(ticks) != len(TICKS):
        raise ValueError(f"found {len(ticks)} y ticks, expected {len(TICKS)}")
    cal = calibrate(list(zip(sorted(ticks, reverse=True), TICKS)))
    unc = UNC_PX + cal.residual / abs(cal.slope)
    top = int(min(ticks)) - 10
    xline, (d0, d1) = _dashed(c, ax, top, base)
    right_end = int(np.flatnonzero((c[base, :] == "k"))[-1])

    ehm, d60 = [], []
    crossed = False
    kmin = int(np.ceil((ax + 4 - xline) / (STEP_PT * s)))
    kmax = int(np.floor((right_end - 4 - xline) / (STEP_PT * s)))
    for k in range(kmin, kmax + 1):
        px = int(round(xline + k * STEP_PT * s))
        if d0 - 4 <= px <= d1 + 4:
            continue
        runs = [r for r in _runs(c[:, px], top, base) if r["e"] < base - BASE_PX]
        at = lambda y: fig.to_page(px, y, s)
        x = float(k * STEP_PT)
        red = [r for r in runs if r["below"] == "R" and r["above"] != "R"]
        if red:
            y = red[0]["y"]
            ehm.append(point(cal, y, unc, at(y), x=x))
        blue = [r for r in runs if r["below"] == "B"]
        under_grey = [r for r in runs if r["above"] == "g" and r["below"] == "g"]
        in_red = [r for r in runs if r["above"] == "R" and r["below"] == "R"]
        if px < xline:
            cand = blue if blue else under_grey
            if len(cand) == 1:
                y = cand[0]["y"]
                d60.append(point(cal, y, unc, at(y), x=x))
        elif not crossed:
            if len(in_red) == 2:
                y = in_red[0]["y"]
                d60.append(point(cal, y, unc, at(y), x=x))
            elif blue and not in_red:
                y = blue[0]["y"]
                d60.append(point(cal, y, unc, at(y), x=x))
            else:
                crossed = True
    return {"groups": {"ehm6": {"points": ehm}, "d60": {"points": d60}}}
