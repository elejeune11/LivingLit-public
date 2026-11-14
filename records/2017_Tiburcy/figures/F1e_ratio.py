"""Fig. 1e (author manuscript, p. 18): force per CM (nN, y) against cardiomyocyte percentage (x), one marker per EHM,
for three input ratios (blue 90 % CM/10 % HFF, black 70/30, red 50/50), each with an open mean marker and x and y
error bars; a black fitted curve runs through the cloud.

The panel is a raster image (~300 dpi). Each filled marker gives two readings: its x (output CM percentage, labels
*_cmpct) and its y (force per CM, labels *_force); the two lists share index order (sorted by y, then x).
Markers are found per colour as distance-transform cores (thin lines, error bars and the open mean ring vanish);
each centre is a fixed-shape circle fit to the marker edge where it borders white paper, so a curve or a marker of
another colour lying across it does not pull the centre. A group's markers are returned only when no two of them
touch (centre distance > marker diameter); otherwise the group is bar only (countable false).
The mean is where the two error bars cross (the vertical bar's column, the horizontal bar's row); the upper error
end is the top cap (y) and the right cap (x), each found as the first line crossing the bar on both sides.
"""
import cv2
import numpy as np

from livinglit.figures.source import blobs, calibrate, colour_mask, point

DPI = 600
UNC_PX = 0.6 * DPI / 300             # 0.6 px at 300 dpi, in px at DPI
Y_TICKS = [0, 2, 4, 6, 8, 10]        # printed y tick labels, bottom to top (Force per CM (nN))
X_TICKS = [0, 20, 40, 60, 80, 100]   # printed x tick labels, left to right (Cardiomyocyte percentage)
COLOURS = {"r90": ("blue", (0, 0, 255)), "r70": ("black", None), "r50": ("red", (230, 25, 35))}
LEGEND_BOTTOM_PX = 230               # legend markers lie above this row
BAR_MAX_PX = 7                       # error-bar lines and caps are thinner than this (px at DPI)
CAP_HALF_PX = 5                      # a cap reaches this far on both sides of its bar (px at DPI)
SYM_PX = 2.5                         # upper and lower caps agree within this (px at DPI)


def _runs_centres(profile, frac=0.5):
    on = profile > frac * profile.max()
    idx = np.flatnonzero(on)
    runs = np.split(idx, np.flatnonzero(np.diff(idx) > 1) + 1)
    return [float((r * profile[r]).sum() / profile[r].sum()) for r in runs if len(r)]


def _axes(img):
    dark = 255.0 - img.astype(float).mean(axis=2)
    m = dark > 145
    ax = int(np.argmax(m.sum(0)))                        # y axis column
    while m[:, ax - 1].sum() > 0.8 * m[:, ax].sum():
        ax -= 1
    ay = int(np.argmax(m.sum(1)))                        # x axis row
    while m[ay + 1].sum() > 0.8 * m[ay].sum():
        ay += 1
    yt = _runs_centres(dark[:ay + 10, ax - 8:ax - 2].sum(1))   # y tick stubs left of the axis
    xt = _runs_centres(dark[ay + 3:ay + 9, :].sum(0))         # x tick stubs below the axis
    xt = [t for t in xt if t > ax - 4]
    if len(yt) != len(Y_TICKS) or len(xt) != len(X_TICKS):
        raise ValueError(f"found {len(yt)} y and {len(xt)} x ticks")
    caly = calibrate(list(zip(sorted(yt, reverse=True), Y_TICKS)))
    calx = calibrate(list(zip(sorted(xt), X_TICKS)))
    return ax, ay, calx, caly


def _mask(img, rgb, ax, ay):
    m = (img.max(axis=2) < 110) if rgb is None else colour_mask(img, rgb, 90)
    m = m.astype(np.uint8)
    m[:, :ax + 6] = 0
    m[ay - 3:, :] = 0
    m[:LEGEND_BOTTOM_PX, :] = 0
    return m


def _circle_fit(m, white, cx, cy, r):
    """Least-squares circle through the marker's edge pixels that border white paper, near the expected circle."""
    edge = m.astype(bool) & ~cv2.erode(m, np.ones((3, 3), np.uint8)).astype(bool)
    near_white = cv2.dilate(white.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
    ys, xs = np.nonzero(edge & near_white)
    for _ in range(3):
        d = np.hypot(xs - cx, ys - cy)
        k = np.abs(d - r) < 3
        X, Y = xs[k].astype(float), ys[k].astype(float)
        A = np.c_[2 * X, 2 * Y, np.ones_like(X)]
        (cx, cy, c), *_ = np.linalg.lstsq(A, X ** 2 + Y ** 2, rcond=None)
        rr = np.sqrt(c + cx ** 2 + cy ** 2)
    res = np.hypot(X - cx, Y - cy) - rr
    return float(cx), float(cy), float(rr), float(np.sqrt(np.mean(res ** 2))), int(k.sum())


def _markers(m, white):
    dt = cv2.distanceTransform(m, cv2.DIST_L2, 5)
    cores = [b for b in blobs((dt > 6).astype(np.uint8), 2, 10 ** 6)]
    r = float(np.median([dt[b["box"][1]:b["box"][1] + b["box"][3], b["box"][0]:b["box"][0] + b["box"][2]].max()
                         for b in cores]))
    out = []
    for b in cores:
        if b["area"] > 80:                                # two touching markers share one core
            out.append(None)
            continue
        out.append(_circle_fit(m, white, b["x"], b["y"], r))
    return out, r


def _mean_marker(m):
    """The open mean marker: a round white hole enclosed by the group's colour."""
    inv = (1 - m).astype(np.uint8)
    n, _, st, ce = cv2.connectedComponentsWithStats(inv, connectivity=4)
    holes = []
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if x > 0 and y > 0 and x + w < m.shape[1] and y + h < m.shape[0] and a > 150 and a > 0.6 * w * h \
                and 0.7 < w / h < 1.4:
            holes.append((float(ce[i][0]), float(ce[i][1]), int(w), int(h)))
    if len(holes) != 1:
        raise ValueError(f"expected one mean marker, found {len(holes)}")
    return holes[0]


def _run_centre(profile, near):
    """Weighted centre of the run of a profile holding position `near`, if no wider than a bar line; else NaN."""
    on = profile > 0
    i = int(round(near))
    if not on[i]:
        return float("nan")
    a, b = i, i
    while a > 0 and on[a - 1]:
        a -= 1
    while b < len(on) - 1 and on[b + 1]:
        b += 1
    if b - a + 1 > BAR_MAX_PX:
        return float("nan")
    w = profile[a:b + 1].astype(float)
    return float((np.arange(a, b + 1) * w).sum() / w.sum())


def _centre(m, hx, hy, half):
    """Mean marker centre: median of the hole centre and the bar segments just outside the ring on both sides."""
    o0, o1 = int(half + 5), int(half + 9)
    xs, ys = [hx], [hy]
    for sgn in (-1, 1):
        rows = m[min(int(hy) + sgn * o0, int(hy) + sgn * o1):max(int(hy) + sgn * o0, int(hy) + sgn * o1)]
        xs.append(_run_centre(rows.sum(0), hx))
        cols = m[:, min(int(hx) + sgn * o0, int(hx) + sgn * o1):max(int(hx) + sgn * o0, int(hx) + sgn * o1)]
        ys.append(_run_centre(cols.sum(1), hy))
    return float(np.nanmedian(xs)), float(np.nanmedian(ys))


def _cap(m, cx, cy, half, step):
    """Distance (px) from the centre to the cap ending the bar in direction step=(dx, dy), or None when the cap is
    not clean: the cap is the first run of positions where a line crosses the bar by >= CAP_HALF_PX on both sides; it is
    clean when that run is no thicker than a line and the bar ends there (nothing drawn beyond it)."""
    dx, dy = step
    hits, d, end = [], int(half + 6), None
    while d < int(half + 150):
        x, y = int(round(cx + dx * d)), int(round(cy + dy * d))
        fx, fy = int(np.floor(cx + dx * d)), int(np.floor(cy + dy * d))
        win = m[fy:fy + 2, x] if dx else m[y, fx:fx + 2]   # the two pixels straddling the bar's centre line
        if not win.any():
            end = d
            break
        if dx:   # horizontal bar: the cap is vertical
            col = m[y - 12:y + 13, x]
            a, b = col[:12][::-1], col[13:]
        else:
            row = m[y, x - 12:x + 13]
            a, b = row[:12][::-1], row[13:]
        ea = np.argmin(a) if not a.all() else 12
        eb = np.argmin(b) if not b.all() else 12
        if ea >= CAP_HALF_PX and eb >= CAP_HALF_PX:
            hits.append(d)
        d += 1
    if not hits or end is None:
        return None
    first = [h for h in hits if h - hits[0] < 2 * BAR_MAX_PX]
    if first[-1] - first[0] + 1 > BAR_MAX_PX or end - first[-1] > 2:
        return None
    return float(np.mean(first))


def _upper(m, cx, cy, half, up, down):
    """Distance to the upper (or right) error end; the lower (or left) cap mirrors it when the upper one touches a
    marker. Where both caps are clean they must agree within SYM_PX."""
    u, l = _cap(m, cx, cy, half, up), _cap(m, cx, cy, half, down)
    if u is not None and l is not None and abs(u - l) > SYM_PX:
        raise ValueError(f"error bar not symmetric: {u} vs {l} px")
    if u is None and l is None:
        raise ValueError("no clean error-bar cap")
    return (u if u is not None else l), u is None


def _triple(cal, pos, unc):
    p = point(cal, pos, unc, (0, 0))
    return [p["value"], p["lo"], p["hi"]]


def read(fig):
    img, s = fig.render(DPI)
    ax, ay, calx, caly = _axes(img)
    mis_x = calx.residual / abs(calx.slope)
    mis_y = caly.residual / abs(caly.slope)
    white = img.min(axis=2) > 200
    groups = {}
    for label, (_, rgb) in COLOURS.items():
        m = _mask(img, rgb, ax, ay)
        hx, hy, w, h = _mean_marker(m)
        half = max(w, h) / 2
        mx, my = _centre(m, hx, hy, half)
        ux, uy = UNC_PX + mis_x, UNC_PX + mis_y
        up, up_mirrored = _upper(m, mx, my, half, (0, -1), (0, 1))
        right, right_mirrored = _upper(m, mx, my, half, (1, 0), (-1, 0))
        bar_x = {"mean": _triple(calx, mx, ux), "error": _triple(calx, mx + right, ux)}
        bar_y = {"mean": _triple(caly, my, uy), "error": _triple(caly, my - up, uy)}

        # filled markers: drop the open mean marker's ring (no core survives in a ring) and keep the rest
        found, r = _markers(m, white)
        apart = all(f is not None for f in found)
        if apart:
            c = np.array([[f[0], f[1]] for f in found])
            dd = np.hypot(*(c[:, None, :] - c[None, :, :]).transpose(2, 0, 1)) + np.eye(len(c)) * 1e9
            apart = bool(dd.min() > 2 * r)
        gx = {"points": [], "countable": apart, "bar": bar_x}
        gy = {"points": [], "countable": apart, "bar": bar_y}
        if apart:
            for fx, fy, _, rms, _ in sorted(found, key=lambda f: (f[1], f[0])):
                at = fig.to_page(fx, fy, s)
                gx["points"].append(point(calx, fx, ux + rms, at))
                gy["points"].append(point(caly, fy, uy + rms, at))
        groups[f"{label}_cmpct"] = gx
        groups[f"{label}_force"] = gy
    return {"groups": groups}
