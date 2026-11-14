"""Fig. 2d (author manuscript, p. 20): force-frequency response of hiPS-G1 EHM, '% of FOC at 1 Hz' (y) against
'Stimulation frequency (Hz)' (x, 1, 2, 3). Black circles: Serum-free protocol (n=21); red squares: Starting protocol
(n=8). Each marker is a group mean with a vertical error bar (SEM, Methods); no single EHM is drawn.

The panel is a raster image (300 dpi, rendered at 600 dpi). Only the groups the record's items need are read: the
serum-free means at 1, 2 and 3 Hz (sf1, sf2, sf3) and the Starting protocol mean at 3 Hz (sp3); each is returned as a
bar (mean and upper error end, x = frequency), no points, under the label <item>/<group> for every item that compares
the group. At 1 Hz the red square lies under the black circle.

Axes: the y axis is the longest vertical dark line; its tick stubs (left of it) are matched to the printed labels
80, 100, 120, 140 bottom to top. The x axis is the long horizontal line; its stubs below it are 1, 2, 3 Hz.
Colours: red is R > RED_R with G, B < RED_GB; black is dark (grey mean < DARK) and not red-tinted (R - G < TINT).
Markers are what survives a morphological opening of the colour mask with a disc (lines, bars and caps are thinner
than the disc). The mean is the midpoint of the two error-bar caps (the bars are mean +/- SEM), checked against the
marker's box centre; the upper error end is the top cap. A cap is the run of rows at the end of the bar whose width
within the column is at least CAP_MIN; its row is the middle of that run.
"""
import cv2
import numpy as np

from livinglit.figures.source import calibrate

DPI = 600
UNC_PX = 0.6 * DPI / 300             # 0.6 px at 300 dpi, in px at DPI
Y_TICKS = [80, 100, 120, 140]        # printed y tick labels, bottom to top
X_TICKS = [1, 2, 3]                  # printed x tick labels (Hz), left to right
WANTED = {("black", 1): "sf1", ("black", 2): "sf2", ("black", 3): "sf3", ("red", 3): "sp3"}
ITEMS = {"sf1": ["F2d_sf2_sf1", "F2d_sf3_sf1"], "sf2": ["F2d_sf2_sf1"], "sf3": ["F2d_sf3_sf1", "F2d_sf3_sp3"],
         "sp3": ["F2d_sf3_sp3"]}             # each group's bar is returned once per item that compares it
DARK, TINT = 128, 60
RED_R, RED_GB = 150, 120
AXIS_RUN_MIN = 600                   # axis lines are at least this long (px)
WIN = 26                             # half width of a frequency column (px); the '*' bracket lies ~32 px right of 3 Hz
OPEN_R = 6                           # opening disc radius (px); bars and caps are ~5 px thick, markers ~25-30 px
MARKER_MIN = 15                      # a marker is at least this tall and wide after opening (px)
BAR_HALF = 1                         # half width of the bar probe (px)
CAP_MIN = 14                         # cap width (px); a bar is ~5 px
CAP_RUN_MAX = 9
CENTRE_TOL = 2.5                     # cap midpoint and marker box centre agree within this (px)


def _runs(idx):
    idx = np.asarray(idx)
    return [r for r in np.split(idx, np.flatnonzero(np.diff(idx) > 1) + 1) if len(r)]


def _centres(profile, frac=0.5):
    return [float((r * profile[r]).sum() / profile[r].sum()) for r in _runs(np.flatnonzero(profile > frac * profile.max()))]


def _longest_run(v):
    best, cur = 0, 0
    for b in v:
        cur = cur + 1 if b else 0
        best = max(best, cur)
    return best


def _axes(m):
    cols = [c for c in range(m.shape[1]) if _longest_run(m[:, c]) >= AXIS_RUN_MIN]
    rows = [r for r in range(m.shape[0]) if _longest_run(m[r]) >= AXIS_RUN_MIN]
    if not cols or not rows or _runs(cols)[0][-1] != cols[-1] or _runs(rows)[0][-1] != rows[-1]:
        raise ValueError(f"expected one y axis and one x axis, found columns {cols} and rows {rows}")
    a0, xr0, xr1 = cols[0], rows[0], rows[-1]
    yt = _centres(m[:xr0, a0 - 12:a0 - 2].sum(1).astype(float))
    xs = max(_runs(np.flatnonzero(m[(xr0 + xr1) // 2])), key=len)   # the x axis line (the '80' label shares rows)
    xt = _centres(m[xr1 + 2:xr1 + 8, xs[0]:xs[-1] + 1].sum(0).astype(float))
    xt = [t + xs[0] for t in xt]
    if len(yt) != len(Y_TICKS) or len(xt) != len(X_TICKS):
        raise ValueError(f"found {len(yt)} y and {len(xt)} x ticks")
    return calibrate(list(zip(sorted(yt, reverse=True), Y_TICKS))), xt, xr0


def _marker(mask, xc, ay):
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * OPEN_R + 1, 2 * OPEN_R + 1))
    sub = np.zeros_like(mask, np.uint8)
    x0, x1 = int(round(xc)) - WIN, int(round(xc)) + WIN + 1
    sub[:ay - 2, x0:x1] = mask[:ay - 2, x0:x1]
    op = cv2.morphologyEx(sub, cv2.MORPH_OPEN, k)
    n, _, st, _ = cv2.connectedComponentsWithStats(op)
    found = [(x, y, w, h) for x, y, w, h, _ in st[1:] if w >= MARKER_MIN and h >= MARKER_MIN]
    if len(found) != 1:
        raise ValueError(f"expected one marker near x={xc:.0f}, found {len(found)}")
    x, y, w, h = found[0]
    return {"cx": x + (w - 1) / 2, "cy": y + (h - 1) / 2, "top": int(y), "bot": int(y + h - 1)}


def _width(mask, y, x):
    row = mask[y, x - WIN:x + WIN + 1]
    c = WIN
    if not row[c - BAR_HALF:c + BAR_HALF + 1].any():
        return 0
    c = c - BAR_HALF + int(np.flatnonzero(row[c - BAR_HALF:c + BAR_HALF + 1])[0])
    lo = hi = c
    while lo > 0 and row[lo - 1]:
        lo -= 1
    while hi < len(row) - 1 and row[hi + 1]:
        hi += 1
    return hi - lo + 1


def _cap(mask, b, sgn):
    """Row (middle of the cap) ending the bar above (sgn=-1) or below (sgn=+1) the marker."""
    x = int(round(b["cx"]))
    y = b["top"] if sgn < 0 else b["bot"]
    while mask[y + sgn, x - BAR_HALF:x + BAR_HALF + 1].any():
        y += sgn
    run = []
    for r in range(y, y - sgn * (CAP_RUN_MAX + 2), -sgn):
        if _width(mask, r, x) >= CAP_MIN:
            run.append(r)
        elif run:
            break
    if not run or len(run) > CAP_RUN_MAX:
        raise ValueError(f"no clean cap at x={x} ({'top' if sgn < 0 else 'bottom'})")
    return (run[0] + run[-1]) / 2


def _triple(cal, pos, unc):
    v = cal.value(pos)
    lo, hi = cal.interval(pos, unc)
    return [v, min(lo, v), max(hi, v)]


def read(fig):
    img, _ = fig.render(DPI)
    g = img.astype(int)
    r, gr, bl = g[..., 0], g[..., 1], g[..., 2]
    red = (r > RED_R) & (gr < RED_GB) & (bl < RED_GB)
    black = (g.mean(axis=2) < DARK) & (r - gr < TINT)
    cal, xt, ay = _axes(black)
    unc = UNC_PX + cal.residual / abs(cal.slope)
    groups = {}
    for (colour, hz), label in WANTED.items():
        mask = black if colour == "black" else red
        b = _marker(mask, xt[X_TICKS.index(hz)], ay)
        up, low = _cap(mask, b, -1), _cap(mask, b, 1)
        mean = (up + low) / 2
        if abs(mean - b["cy"]) > CENTRE_TOL:
            raise ValueError(f"{label}: cap midpoint {mean} and marker centre {b['cy']} disagree")
        bar = {"mean": _triple(cal, mean, unc), "error": _triple(cal, up, unc), "x": hz}
        for item in ITEMS[label]:
            groups[f"{item}/{label}"] = {"points": [], "countable": False, "bar": dict(bar)}
    return {"groups": groups}
