"""Fig. 4g (author manuscript, p. 23): maximal FOC, response to ISO, CM viability and CM size as fold of control
after 1 µmol/L NE with or without metoprolol (Met) or phenoxybenzamine (Phen). Part of the Fig. 4 raster
(~300 dpi), rendered at 300 dpi; the crop holds panel g only.

Four clusters of three bars (NE black, NE+Met grey, NE+Phen white), each bar outlined in black with an upward
error bar (stem and cap); Control is the dashed line (printed at 1.0, no error bar). Only the bars the record's
items compare are read: NE in all four clusters, NE+Phen for ISO, NE+Met for CM size.

Bars are found along a row just above the x axis (a filled bar is one wide run of non-white pixels, an open bar
two narrow outline runs). Coverage of a pixel is (255 - max(R, G, B)) / 255. The top of a bar is the upper edge
of its top outline seen in two probe columns 3 px inside the bar's outer edges (they miss the cap and stem); the
error end is the upper edge of the structure joined to the bar through the stem (rows whose centre columns stay
dark), so an asterisk above the cap, separated by white rows, is never taken. Upper edges are sub-pixel (the first
full row less the partial coverage just above it). A drawn line is centred on its value, so each upper edge is
moved down by half the line width, measured as the integrated coverage of the isolated caps (those separated
from their bar by a bare stem); LW_UNC_PX is added for that. The Control value is the darkness-weighted centre
of the dashed line, read in the columns between the bar clusters. Bars carry no single EHM: bar only, no points.
"""
import numpy as np

from livinglit.figures.source import calibrate

DPI = 300
UNC_PX = 0.6                         # 0.6 px at 300 dpi
LW_UNC_PX = 0.5                      # extra for the half line width added to every upper edge
YTICKS = [0, 0.5, 1.0, 1.5]          # printed y tick labels, bottom to top
AXIS_MIN = 150                       # an axis is a dark line at least this long (px)
FILLED = 0.25                        # coverage of a bar fill in its edge probes (grey fill ~0.37)
STEM = 0.3                           # coverage of the stem in its centre columns
BAR_MIN_W = 12                       # a filled bar's run above the axis (px)
CLUSTERS = ["FOC", "ISO", "viability", "size"]
ORDER = ["ne", "ne_met", "ne_phen"]  # bars left to right in each cluster
# (cluster, bar) -> label(s); Control (dashed line) is given once per item that compares it
READ = {("FOC", "ne"): "foc_ne", ("ISO", "ne"): "iso_ne", ("ISO", "ne_phen"): "iso_ne_phen",
        ("viability", "ne"): "viab_ne", ("size", "ne"): "size_ne", ("size", "ne_met"): "size_ne_met"}
CTR = ["foc_ctr", "iso_ctr for F4g_iso_ne", "iso_ctr for F4g_iso_ne_phen", "viab_ctr",
       "size_ctr for F4g_size_ne", "size_ctr for F4g_size_ne_met"]


def _runs(idx):
    idx = np.asarray(idx)
    return [r for r in np.split(idx, np.flatnonzero(np.diff(idx) > 1) + 1) if len(r)]


def _axes(dark):
    cols = [c for c in range(dark.shape[1]) if max((len(r) for r in _runs(np.flatnonzero(dark[:, c]))), default=0) >= AXIS_MIN]
    rows = [r for r in range(dark.shape[0]) if max((len(q) for q in _runs(np.flatnonzero(dark[r]))), default=0) >= AXIS_MIN]
    if not cols or not rows:
        raise ValueError("axes not found")
    return cols[0], rows[0]


def _yticks(cov, ax, ay):
    w = cov[:ay + 6, ax - 7:ax - 1].sum(axis=1)
    pos = []
    for r in _runs(np.flatnonzero(w > 0.4 * w.max())):
        i = np.arange(max(r[0] - 1, 0), r[-1] + 2)
        pos.append(float((i * w[i]).sum() / w[i].sum()))
    if len(pos) != len(YTICKS):
        raise ValueError(f"found {len(pos)} y ticks, expected {len(YTICKS)}")
    return calibrate(list(zip(sorted(pos, reverse=True), YTICKS)))


def _bars(cov, ax, ay):
    """(left, right) outer columns of the bars, from a row 8 px above the x axis."""
    row = cov[ay - 8, ax + 3:]
    runs = [(ax + 3 + r[0], ax + 3 + r[-1]) for r in _runs(np.flatnonzero(row > 0.2))]
    bars, i = [], 0
    while i < len(runs):
        l, r = runs[i]
        if r - l + 1 >= BAR_MIN_W:
            bars.append((l, r))
            i += 1
        elif i + 1 < len(runs) and runs[i + 1][1] - runs[i + 1][0] + 1 < BAR_MIN_W and runs[i + 1][0] - r < 20:
            bars.append((l, runs[i + 1][1]))
            i += 2
        else:
            i += 1
    return bars


def _half_edge(p, r):
    """Sub-pixel upper edge of the structure whose top rows start at r: where the profile first reaches half of
    its peak over the next four rows (linear between pixel centres)."""
    half = p[r:r + 4].max() / 2
    while p[r - 1] >= half:
        r -= 1
    while p[r] < half:
        r += 1
    return r - 1 + (half - p[r - 1]) / (p[r] - p[r - 1])


def _bar(cov, l, r, ay):
    """Upper edges of the bar top and of its error bar; for an isolated cap also its weighted centre."""
    c = int(round((l + r) / 2))
    edge = np.minimum(cov[:, l + 3], cov[:, r - 3])
    k = ay - 8
    if edge[k] >= FILLED:            # filled bar (black or grey): up to the top of the fill
        while edge[k - 1] >= FILLED:
            k -= 1
        k -= 2
    else:                            # open bar: up to its top outline
        while edge[k] < 0.5:
            k -= 1
        k -= 2
    top = _half_edge(edge, k)
    stem = cov[:, c - 2:c + 3].max(axis=1)
    capc = cov[:, [c - 3, c - 2, c + 2, c + 3]].mean(axis=1)
    j = int(top) - 1
    while stem[j] >= STEM:
        j -= 1
    cap = _half_edge(capc, j + 1)
    # isolated cap: below it a bare stem (capc low) before the bar top
    rows = np.arange(j + 1, int(top))
    peak = capc[j + 1:j + 4].max()
    low = rows[capc[rows] < 0.2 * peak]
    centre = None
    if len(low):
        i = np.arange(j, low[0])
        centre = float((i * capc[i]).sum() / capc[i].sum())
    return top, cap, centre


def _dashed(cov, ax, bars, cal):
    """Darkness-weighted row of the dashed control line in the columns between bar clusters."""
    gap = np.ones(cov.shape[1], bool)
    gap[:ax + 3] = False
    for l, r in bars:
        gap[l - 3:r + 4] = False
    y1 = int(round((1.0 - cal.intercept) / cal.slope))
    lo, hi = y1 - 12, y1 + 13
    w = cov[lo:hi, gap].sum(axis=1)
    pk = int(np.argmax(w))
    i = np.arange(max(pk - 3, 0), min(pk + 4, len(w)))
    base = np.median(w)
    wi = (w[i] - base).clip(0)
    return lo + float((i * wi).sum() / wi.sum())


def read(fig):
    img, _ = fig.render(DPI)
    cov = (255 - img.astype(int).max(axis=2)) / 255.0
    ax, ay = _axes(cov > 0.5)
    cal = _yticks(cov, ax, ay)
    unc = UNC_PX + cal.residual / abs(cal.slope)
    bars = _bars(cov, ax, ay)
    if len(bars) != len(CLUSTERS) * len(ORDER):
        raise ValueError(f"found {len(bars)} bars, expected {len(CLUSTERS) * len(ORDER)}")
    found = {}
    for i, (l, r) in enumerate(bars):
        key = (CLUSTERS[i // len(ORDER)], ORDER[i % len(ORDER)])
        if key in READ:
            found[READ[key]] = _bar(cov, l, r, ay)
    offs = [f[2] - f[1] for f in found.values() if f[2] is not None]
    if len(offs) < 2:
        raise ValueError("fewer than two isolated caps to measure the line width")
    half = float(np.median(offs))
    u = unc + LW_UNC_PX

    def triple(pos, un):
        v = cal.value(pos)
        a, b = cal.interval(pos, un)
        return [v, min(a, v), max(b, v)]

    groups = {}
    for label, (top, cap, _) in found.items():
        groups[label] = {"points": [], "countable": False,
                         "bar": {"mean": triple(top + half, u), "error": triple(cap + half, u)}}
    ctr = {"points": [], "countable": False, "bar": {"mean": triple(_dashed(cov, ax, bars, cal), unc)}}
    for label in CTR:
        groups[label] = ctr
    return {"groups": groups}
