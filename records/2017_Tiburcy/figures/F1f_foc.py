"""Fig. 1f (author manuscript, p. 18): force of contraction (FOC, mN, y) against calcium (mM, x) for 4 week EHM,
Starting Protocol (filled circles) and Serum-free Protocol (open circles); each marker is a group mean at one calcium
concentration with a vertical error bar, and a fitted curve runs through each series.

The panel is a raster image (~300 dpi, rendered at 600 dpi). No single EHM is drawn, so every marker is returned as
a bar (mean and upper error end) under its own label <group>_<calcium>, with the calcium concentration as the bar's x.
Markers are correlation peaks of a synthetic disc and ring of the plot markers' radius (measured from the filled
markers' distance-transform cores; the legend circles are drawn larger, with a thinner ring); the curve and error bar
crossing a marker barely move the peak, which is refined to sub-pixel by a parabola. A marker is filled (Starting)
when its inner disc is dark, open (Serum-free) otherwise. x is the calibrated marker position rounded to 0.1 mM (the
concentrations are not printed; every marker lies within X_TOL of a step, and both series share the steps).
The upper error end is the top cap: the last run of rows along the bar where a line crosses it by >= CAP_HALF_PX on
both sides, taken at its centre, and apart from the marker. When the top cap merges with the marker edge, the bottom
cap is mirrored about the mean; where both are clean they agree within SYM_PX. A bar whose caps both merge with the
marker (the smallest bars, and the steep low-calcium part of the curves) gives no error end.
"""
import cv2
import numpy as np

from livinglit.figures.source import calibrate, point

DPI = 600
UNC_PX = 0.6 * DPI / 300             # 0.6 px at 300 dpi, in px at DPI
Y_TICKS = [0, 0.5, 1, 1.5, 2]        # printed y tick labels, bottom to top (FOC (mN))
X_TICKS = [0, 1, 2, 3, 4]            # printed x tick labels, left to right (Calcium (mM))
LEGEND_BOTTOM_PX = 200               # legend lies above this row
TPL_HALF = 17                        # template half size (px at DPI); the markers are ~25 px across
RING_FRAC = 0.4                      # open-circle line width / radius, as drawn in the plot (the legend ring is thinner)
MATCH_MIN = 0.45                     # a marker peaks at >= 0.50; the curve alone at <= 0.33
FILL_MIN = 0.85                      # dark fraction of the inner disc (0.45 R): filled 1.0, open (curve inside) <= 0.6
X_STEP = 0.1                         # calcium (mM) is read to this step; a marker must lie within X_TOL of it
X_TOL = 0.03
BAR_HALF = 1                         # half width of the error-bar line window (px at DPI)
CAP_HALF_PX = 6                      # a cap reaches this far on both sides of its bar (px at DPI)
SYM_PX = 2.5                         # upper and lower caps agree within this (px at DPI)


def _runs_centres(profile, frac=0.5):
    on = profile > frac * profile.max()
    idx = np.flatnonzero(on)
    runs = np.split(idx, np.flatnonzero(np.diff(idx) > 1) + 1)
    return [float((r * profile[r]).sum() / profile[r].sum()) for r in runs if len(r)]


def _axes(dark):
    m = dark > 145
    ax = int(np.argmax(m.sum(0)))                        # y axis column (the longest vertical line)
    while m[:, ax - 1].sum() > 0.8 * m[:, ax].sum():
        ax -= 1
    ay = int(np.argmax(m.sum(1)))                        # x axis row (the longest horizontal line)
    while m[ay + 1].sum() > 0.8 * m[ay].sum():
        ay += 1
    yt = _runs_centres(dark[LEGEND_BOTTOM_PX:ay, ax - 10:ax - 2].sum(1))   # y tick stubs left of the axis
    yt = [t + LEGEND_BOTTOM_PX for t in yt]
    xt = _runs_centres(dark[ay + 3:ay + 20, ax:].sum(0))                   # x tick stubs below the axis
    xt = [t + ax for t in xt]
    if len(yt) != len(Y_TICKS) or len(xt) != len(X_TICKS):
        raise ValueError(f"found {len(yt)} y and {len(xt)} x ticks")
    caly = calibrate(list(zip(sorted(yt, reverse=True), Y_TICKS)))
    calx = calibrate(list(zip(sorted(xt), X_TICKS)))
    return ax, ay, calx, caly


def _radius(grey, ax, ay):
    """Plot marker radius: the median depth of the filled markers' distance-transform cores."""
    m = (grey < 128).astype(np.uint8)
    m[:LEGEND_BOTTOM_PX], m[:, :ax + 4], m[ay - 2:] = 0, 0, 0
    dt = cv2.distanceTransform(m, cv2.DIST_L2, 5)
    n, lab, st, _ = cv2.connectedComponentsWithStats((dt > 5).astype(np.uint8))
    depths = [float(dt[lab == i].max()) for i in range(1, n)]
    if len(depths) < 3:
        raise ValueError("no filled markers found")
    return float(np.median(depths)) + 0.5


def _templates(R, ring_frac):
    """Synthetic grey templates (white paper, black ink, 4x supersampled edges): a disc and a ring of radius R."""
    k = 4
    c = np.arange((2 * TPL_HALF + 1) * k) / k - TPL_HALF + 0.5 / k - 0.5
    d = np.hypot(*np.meshgrid(c, c))
    sub = {"start": d <= R, "sf": (d <= R) & (d >= R * (1 - ring_frac))}
    return {lab: (255 * (1 - a.reshape(2 * TPL_HALF + 1, k, 2 * TPL_HALF + 1, k).mean(axis=(1, 3))))
            .astype(np.float32) for lab, a in sub.items()}


def _sig_bar(grey, ax):
    """Column of the significance bar: the long vertical line right of the y axis."""
    m = grey[LEGEND_BOTTOM_PX:, ax + 10:] < 128
    col = m.sum(0)
    c = int(np.argmax(col))
    if col[c] < 0.3 * m.shape[0]:
        raise ValueError("no significance bar found")
    return c + ax + 10


def _peak(score, y, x):
    """Sub-pixel peak by a parabola through the peak and its neighbours along each axis."""
    def par(a, b, c):
        d = a - 2 * b + c
        return 0.0 if d == 0 else 0.5 * (a - c) / d
    return (x + par(score[y, x - 1], score[y, x], score[y, x + 1]),
            y + par(score[y - 1, x], score[y, x], score[y + 1, x]))


def _markers(grey, tpls, r, ax, ay):
    """(label, cx, cy) for every correlation peak in the plot area: filled (start) when the inner disc is dark,
    open (sf) otherwise; the centre is refined on the matching template's score."""
    x0, y0, x1, y1 = ax + 4, LEGEND_BOTTOM_PX, _sig_bar(grey, ax) - 3, ay - 2
    region = cv2.copyMakeBorder(grey[y0:y1, x0:x1].astype(np.float32), *(TPL_HALF + 1,) * 4,
                                cv2.BORDER_CONSTANT, value=255.0)   # white margin: a marker at the edge still peaks
    x0, y0 = x0 - TPL_HALF - 1, y0 - TPL_HALF - 1
    scores = {k: cv2.matchTemplate(region, t, cv2.TM_CCOEFF_NORMED) for k, t in tpls.items()}
    best = np.maximum(*scores.values())
    peaks = (best == cv2.dilate(best, np.ones((2 * TPL_HALF + 1,) * 2, np.uint8))) & (best >= MATCH_MIN)
    yy, xx = np.mgrid[:grey.shape[0], :grey.shape[1]]
    out = []
    for py, px in zip(*np.nonzero(peaks)):
        if not (0 < py < best.shape[0] - 1 and 0 < px < best.shape[1] - 1):
            raise ValueError(f"marker peak on the edge of the plot area at {px + x0}, {py + y0}")
        cx, cy = px + x0 + TPL_HALF, py + y0 + TPL_HALF
        fill = float((grey[np.hypot(xx - cx, yy - cy) < 0.45 * r] < 128).mean())
        label = "start" if fill >= FILL_MIN else "sf"
        fx, fy = _peak(scores[label], py, px)
        out.append((label, fx + x0 + TPL_HALF, fy + y0 + TPL_HALF))
    return out


def _cap(m, cx, cy, r, sgn):
    """Distance (px) from the centre to the cap ending the bar above (sgn=-1) or below (sgn=+1), or None when the bar
    does not reach beyond the marker or its cap is not clean."""
    x = int(round(cx))
    d = int(r + 3)
    if not m[int(round(cy + sgn * d)), x - BAR_HALF:x + BAR_HALF + 1].any():
        return None
    while m[int(round(cy + sgn * d)), x - BAR_HALF:x + BAR_HALF + 1].any():
        d += 1
        if d > 200:
            return None
    first = int(r + 1)
    hits = [dd for dd in range(first, d)
            if m[int(round(cy + sgn * dd)), x - CAP_HALF_PX:x - 2].all()
            and m[int(round(cy + sgn * dd)), x + 3:x + CAP_HALF_PX + 1].all()]
    run = []
    for dd in reversed(hits):                         # the last run of cap rows, ending where the bar ends
        if run and dd != run[-1] - 1:
            break
        run.append(dd)
    if not run or run[0] != d - 1 or run[-1] == first or len(run) > 6:
        return None                                   # a clean cap is one line-thick run, apart from the marker
    return (run[0] + run[-1]) / 2


def _triple(cal, pos, unc):
    p = point(cal, pos, unc, (0, 0))
    return [p["value"], p["lo"], p["hi"]]


def read(fig):
    img, s = fig.render(DPI)
    grey = img.astype(float).mean(axis=2)
    ax, ay, calx, caly = _axes(255.0 - grey)
    mis_y = caly.residual / abs(caly.slope)
    r = _radius(grey, ax, ay)
    tpls = _templates(r, RING_FRAC)
    m = grey < 128
    found = sorted(_markers(grey, tpls, r, ax, ay), key=lambda t: (t[0], t[1]))
    xs = {lab: [round(calx.value(cx) / X_STEP) for l, cx, _ in found if l == lab] for lab in ("start", "sf")}
    if xs["start"] != xs["sf"]:
        raise ValueError(f"the two series are not read at the same calcium concentrations: {xs}")
    groups = {}
    for label, cx, cy in found:
        ca = round(round(calx.value(cx) / X_STEP) * X_STEP, 6)
        if abs(calx.value(cx) - ca) > X_TOL:
            raise ValueError(f"{label} marker at {calx.value(cx):.3f} mM is not on a {X_STEP} mM step")
        key = f"{label}_{ca:g}"
        if key in groups:
            raise ValueError(f"two {label} markers at {ca} mM")
        u, l = _cap(m, cx, cy, r, -1), _cap(m, cx, cy, r, 1)
        if u is not None and l is not None and abs(u - l) > SYM_PX:
            raise ValueError(f"{key}: error bar not symmetric ({u} vs {l} px)")
        bar = {"mean": _triple(caly, cy, UNC_PX + mis_y), "x": ca}
        up = u if u is not None else l                # mirrored lower cap when the upper one is not clean
        if up is not None:
            bar["error"] = _triple(caly, cy - up, UNC_PX + mis_y)
        groups[key] = {"points": [], "countable": False, "bar": bar}
    return {"groups": groups}
