"""2017_Mills helpers: raster bar charts and marker curves (this paper's alone).

All panels of this paper are raster images embedded at about 200 dpi, with tick labels drawn into the image (no words),
so each script states the tick values it sees and these helpers find the tick marks, bars, error-bar caps and markers
by pixel. Positions are found by code; values come only from the calibration.
"""
from __future__ import annotations

import numpy as np

from livinglit.figures.source import calibrate

DPI = 300
RASTER_PX_300 = 0.6  # uncertainty at 300 dpi for images embedded at 300 dpi (02-audit)
MARKS: list = []  # pixel positions found, for a reader's overlay outside the repository


def native_dpi(fig) -> float:
    """Resolution of the embedded image under the crop centre."""
    cx, cy = (fig.crop[0] + fig.crop[2]) / 2, (fig.crop[1] + fig.crop[3]) / 2
    best = None
    for im in fig.page.get_images(full=True):
        for r in fig.page.get_image_rects(im[0]):
            if r.x0 <= cx <= r.x1 and r.y0 <= cy <= r.y1 and r.width > 0:
                d = im[2] / r.width * 72
                if best is None or r.width * r.height < best[1]:
                    best = (d, r.width * r.height)
    if best is None:
        raise ValueError("no embedded image under the crop")
    return best[0]


def line_centre(g: np.ndarray, start: int, span: int = 7) -> float:
    """Sub-pixel centre of the first dark line at or below row `start` in an intensity profile g (white above).
    A line that the profile climbs out of again (a border, tick or cap) gives the darkness-weighted centre;
    a step into a fill with no border gives the half-way crossing."""
    lo = max(0, start - 2)
    seg = g[lo:lo + span + 2].astype(float)
    i = int(np.argmin(seg[:span]))
    after = seg[i + 1:i + 5]
    if len(after) and after.max() - seg[i] > 25:
        ref = after.max()
        rows = [j for j in range(max(0, i - 2), min(len(seg), i + 3)) if ref - seg[j] > 0.3 * (ref - seg[i])]
        w = np.array([ref - seg[j] for j in rows])
        return lo + float(np.dot(rows, w) / w.sum())
    fill = seg[i]
    half = (255.0 + fill) / 2
    for j in range(len(seg)):
        if seg[j] <= half:
            if j == 0:
                return float(lo)
            a, b = seg[j - 1], seg[j]
            return lo + j - 1 + (a - half) / (a - b) if a != b else lo + j
    return lo + float(i)


class Panel:
    """A rendered crop with masks, axis and calibration helpers."""

    def __init__(self, fig, dark_thr: int = 110, white_thr: int = 215, edge_thr: int = 160):
        self.fig = fig
        self.img, self.scale = fig.render(DPI)
        self.dark = self.img.astype(int).mean(axis=2) < dark_thr
        self.nonwhite = self.img.min(axis=2) < white_thr
        self.edge = self.img.astype(int).mean(axis=2) < edge_thr
        # images embedded below 300 dpi carry proportionally wider intervals
        self.unc_px = RASTER_PX_300 * max(1.0, DPI / native_dpi(fig))
        self.unc_pt = self.unc_px / self.scale
        self.cal = None

    # page <-> pixel
    def py(self, page_y: float) -> float:
        return (page_y - self.fig.crop[1]) * self.scale

    def px(self, page_x: float) -> float:
        return (page_x - self.fig.crop[0]) * self.scale

    def page_y(self, py: float) -> float:
        return self.fig.crop[1] + py / self.scale

    def page_x(self, px: float) -> float:
        return self.fig.crop[0] + px / self.scale

    # axis
    def y_axis(self, x_lo: float | None = None, x_hi: float | None = None):
        """Column (px) of the y axis: the longest vertical run of dark pixels in [x_lo, x_hi] (page pt)."""
        h, w = self.dark.shape
        a = 0 if x_lo is None else max(0, int(self.px(x_lo)))
        b = w if x_hi is None else min(w, int(self.px(x_hi)))
        best = (0, 0, 0, 0)
        for x in range(a, b):
            col = self.dark[:, x]
            run, start = 0, 0
            for y in range(h + 1):
                if y < h and col[y]:
                    if run == 0:
                        start = y
                    run += 1
                else:
                    if run > best[0]:
                        best = (run, x, start, start + run - 1)
                    run = 0
        run, x, y0, y1 = best
        xs = [c for c in range(max(0, x - 5), min(w, x + 6)) if self.dark[y0:y1 + 1, c].mean() > 0.8]
        return min(xs), max(xs), y0, y1

    def ticks(self, axis, min_len: int = 2, thr: int = 200):
        """Tick marks left of the y axis: (centre_px, thickness_px), bottom to top."""
        xl, xr, y0, y1 = axis
        light = self.img.astype(int).mean(axis=2) < thr
        while xl > 0 and light[y0:y1 + 1, xl - 1].mean() > 0.8:  # the axis line's own anti-aliased edge
            xl -= 1
        cols = [xl - k for k in range(1, 1 + min_len)]
        rows = np.all(self.img[:, cols].astype(int).mean(axis=2) < thr, axis=1)
        out, y = [], y0 - 3
        while y <= y1 + 3:
            if rows[y]:
                s = y
                while y <= y1 + 3 and rows[y]:
                    y += 1
                g = self.img[:, cols].astype(int).mean(axis=2).mean(axis=1)
                out.append((line_centre(g, s), y - s))
            y += 1
        return sorted(out, key=lambda t: -t[0])

    def calibrate_y(self, axis, values, skip: int = 0, log: bool = False):
        """Fit tick marks (bottom to top, after skipping `skip`) to the printed tick values."""
        tk = self.ticks(axis)[skip:]
        if len(tk) < len(values):
            raise ValueError(f"found {len(tk)} tick marks, expected {len(values)}: {tk}")
        tk = tk[:len(values)]
        self.tick_thickness = float(np.median([t[1] for t in tk]))
        MARKS.extend([(axis[0] - 3, t[0], (0, 160, 0)) for t in tk])
        self.cal = calibrate([(self.page_y(t[0]), v) for t, v in zip(tk, values)], log=log)
        return self.cal

    def value(self, py: float) -> list[float]:
        """[value, lo, hi] for a pixel row: raster interval plus the calibration misfit."""
        pos = self.page_y(py)
        v = self.cal.value(pos)
        a, b = self.cal.value(pos - self.unc_pt), self.cal.value(pos + self.unc_pt)
        lo, hi = min(a, b, v) - self.cal.residual, max(a, b, v) + self.cal.residual
        return [v, lo, hi]

    # bars
    def bars(self, axis, row_above: int = 4, min_w: int = 6, merge: int = 3, x_lo=None, x_hi=None, expect=None):
        """Bars as (x0, x1) px: runs of non-white pixels just above the x axis, right of the y axis."""
        xl, xr, y0, y1 = axis
        base = y1
        r = base - (xr - xl + 1) - row_above
        a = xr + 3 if x_lo is None else int(self.px(x_lo))
        b = self.nonwhite.shape[1] if x_hi is None else int(self.px(x_hi))
        row = self.nonwhite[r - 1:r + 2, a:b].any(axis=0)
        runs, x = [], 0
        while x < len(row):
            if row[x]:
                s = x
                while x < len(row) and row[x]:
                    x += 1
                runs.append([s + a, x - 1 + a])
            x += 1
        merged = []
        for run in runs:
            if merged and run[0] - merged[-1][1] <= merge:
                merged[-1][1] = run[1]
            else:
                merged.append(run)
        # filled bars are wide runs; an outlined white bar shows as two thin runs (its side borders), paired here
        paired, pending = [], None
        for m in merged:
            if m[1] - m[0] + 1 >= min_w:
                paired.append(m)
                pending = None
            elif pending is None:
                pending = m
            else:
                paired.append([pending[0], m[1]])
                pending = None
        merged = paired
        if expect and len(merged) < expect:
            # bars that touch: split the runs that are a whole number of bar widths wide
            unit = min(m[1] - m[0] + 1 for m in merged)
            ks = [max(1, round((a1 - a0 + 1) / unit)) for a0, a1 in merged]
            if sum(ks) != expect and expect % len(merged) == 0:
                ks = [expect // len(merged)] * len(merged)  # every run is a group of touching bars
            out = []
            for (a0, a1), k in zip(merged, ks):
                w = (a1 - a0 + 1) / k
                out += [[int(round(a0 + i * w)), int(round(a0 + (i + 1) * w)) - 1] for i in range(k)]
            merged = out
        return [tuple(m) for m in merged]

    def _run_top(self, x: int, base: int, gap: int = 6) -> int:
        y, last = base, base
        miss = 0
        while y > 0:
            y -= 1
            if self.nonwhite[y, x - 1:x + 2].any():
                last, miss = y, 0
            else:
                miss += 1
                if miss > gap:
                    break
        return last

    def side_top(self, x_from: int, x_to: int, base: int, gap: int = 1) -> int:
        """Top row of the vertical edge run (a bar's side border) in columns [x_from, x_to] from the x axis up."""
        y, last, miss = base, base, 0
        while y > 0:
            y -= 1
            if self.edge[y, x_from:x_to + 1].any():
                last, miss = y, 0
            else:
                miss += 1
                if miss > gap:
                    break
        return last

    def bar_top(self, bar, base: int, inset: int = 5, gap: int = 1) -> float:
        """Top of a bar (px): the side borders give the top row; the top border's centre is taken just inside them."""
        x0, x1 = bar
        g = self.img.astype(int).mean(axis=2)
        tops = []
        for side, x in ((self.side_top(x0, x0 + 2, base, gap), x0 + inset), (self.side_top(x1 - 2, x1, base, gap), x1 - inset)):
            tops.append(line_centre(g[:, x - 1:x + 2].mean(axis=1), side))
        return float(np.mean(tops))

    def error_top(self, bar, top: float, half: int = 2, gap: int = 0, mask=None) -> float:
        """Upper end of the error bar (px): the contiguous whisker above the bar top, cap at line centre."""
        m = self.edge if mask is None else mask
        xc = int(round((bar[0] + bar[1]) / 2))
        y = int(round(top - self.tick_thickness / 2))
        last, miss = None, 0
        while y > 0:
            y -= 1
            if m[y, xc - half:xc + half + 1].any():
                last, miss = y, 0
            else:
                miss += 1
                if miss > gap:
                    break
        if last is None or last >= top - 1:
            return top
        # a significance bracket whose leg stands on the cap: its horizontal runs to one side only.
        # Walk down from the top past bracket rows to the first symmetric (cap) row.
        y = last
        while y < top - 1:
            lft = rgt = 0
            while xc - half - lft - 1 >= 0 and m[y, xc - half - lft - 1]:
                lft += 1
            while xc + half + rgt + 1 < m.shape[1] and m[y, xc + half + rgt + 1]:
                rgt += 1
            if max(lft, rgt) > 8 and min(lft, rgt) < max(lft, rgt) / 3:
                y += 1
                while y < top - 1 and self._wide(m, y, xc, half):
                    y += 1
                while y < top - 1 and not self._wide(m, y, xc, half):
                    y += 1
                last = y
                continue
            break
        if last >= top - 1:
            return top
        g = self.img.astype(int).mean(axis=2)
        return line_centre(g[:, xc - half:xc + half + 1].mean(axis=1), last)

    @staticmethod
    def _wide(m, y, xc, half) -> bool:
        """A row wider than a whisker around the bar centre (a cap or a bracket)."""
        return bool(m[y, xc - half - 2:xc - half].any() or m[y, xc + half + 1:xc + half + 3].any())

    def read_bars(self, axis, labels, **kw):
        base = axis[3]
        found = self.bars(axis, expect=len(labels),
                          **{k: v for k, v in kw.items() if k in ("row_above", "min_w", "merge", "x_lo", "x_hi")})
        if len(found) != len(labels):
            raise ValueError(f"found {len(found)} bars, expected {len(labels)}: "
                             f"{[(round(self.page_x(a), 1), round(self.page_x(b), 1)) for a, b in found]}")
        out = {}
        for lab, bar in zip(labels, found):
            if lab is None:  # a bar no item compares: located (so the others are named right), not returned
                continue
            top = self.bar_top(bar, base, gap=kw.get("gap", 1))
            err = self.error_top(bar, top, half=kw.get("half", 2))
            xc = (bar[0] + bar[1]) / 2
            MARKS.extend([(xc, top, (0, 0, 255)), (xc, err, (255, 0, 0))])
            out[lab] = {"points": [], "countable": False,
                        "bar": {"mean": self.value(top), "error": self.value(err)}}
        return out


def also(out: dict, extra: dict | None) -> dict:
    """The same bar under a second label, so that a group compared in two items feeds both."""
    for new, old in (extra or {}).items():
        out["groups"][new] = out["groups"][old]
    return out


def bar_panel(fig, ticks, labels, x_lo=None, x_hi=None, skip: int = 0, extra: dict | None = None, **kw):
    """Standard panel: y axis at the left of the crop, ticks bottom to top, bars left to right.
    extra = {new label: label} repeats a bar for a second item."""
    p = Panel(fig, **{k: kw.pop(k) for k in ("dark_thr", "white_thr", "edge_thr") if k in kw})
    ax = p.y_axis(x_lo=kw.pop("axis_lo", None), x_hi=kw.pop("axis_hi", None))
    p.calibrate_y(ax, ticks, skip=skip)
    return also({"groups": p.read_bars(ax, labels, x_lo=x_lo, x_hi=x_hi, **kw)}, extra)


# ------------------------------------------------------------------ vector bar charts (Fig. S1 F and L)
VECTOR_PT = 0.5


def _horizontal_ys(d) -> list[float]:
    ys = []
    for it in d["items"]:
        if it[0] == "l" and abs(it[1].y - it[2].y) < 1e-3 and abs(it[1].x - it[2].x) > 0.3:
            ys.append(round(it[1].y, 3))
    return sorted(set(ys))


def _black(d) -> bool:
    f = d.get("fill")
    return f is not None and max(f) < 0.05


def vector_bars(fig, labels, extra: dict | None = None):
    """Bars drawn as vector outlines with vector error bars; y axis calibrated from its tick rects and tick words."""
    dr = fig.drawings()
    # y axis: the tall black path made of rects; its small rects are the tick marks
    axis = max((d for d in dr if _black(d) and d["rect"].height > 20 and d["rect"].width < 4), key=lambda d: d["rect"].height)
    ax_x = axis["rect"].x1
    ticks = [((it[1].y0 + it[1].y1) / 2, it[1]) for it in axis["items"]
             if it[0] == "re" and it[1].width < 2.5 and it[1].height < 2]
    words = [((w[1] + w[3]) / 2, float(w[4])) for w in fig.words()
             if w[2] <= axis["rect"].x0 + 0.5 and _isnum(w[4])]
    marks = []
    for ty, _ in ticks:
        near = [w for w in words if abs(w[0] - ty) < 2.5]
        if near:
            marks.append((ty, min(near, key=lambda w: abs(w[0] - ty))[1]))
    cal = calibrate(marks)
    base = axis["rect"].y1
    outlines = [d for d in dr if _black(d) and len(d["items"]) == 10 and all(it[0] == "l" for it in d["items"])
                and abs(d["rect"].y1 - base) < 3 and 3 < d["rect"].width < 15 and d["rect"].x0 > ax_x]
    outlines.sort(key=lambda d: d["rect"].x0)
    if len(outlines) != len(labels):
        raise ValueError(f"found {len(outlines)} bars, expected {len(labels)}")
    errs = [d for d in dr if _black(d) and len(d["items"]) == 11 and d["rect"].width < 6]

    def val(y):
        v = cal.value(y)
        a, b = cal.value(y - VECTOR_PT), cal.value(y + VECTOR_PT)
        return [v, min(a, b, v) - cal.residual, max(a, b, v) + cal.residual]

    out = {}
    for lab, o in zip(labels, outlines):
        hy = _horizontal_ys(o)
        top = (hy[0] + hy[1]) / 2
        xc = (o["rect"].x0 + o["rect"].x1) / 2
        mine = [e for e in errs if abs((e["rect"].x0 + e["rect"].x1) / 2 - xc) < 1 and abs(e["rect"].y1 - (hy[0] + hy[1]) / 2) < 1.5]
        if mine:
            ey = _horizontal_ys(mine[0])
            et = (ey[0] + ey[1]) / 2
        else:
            et = top
        out[lab] = {"points": [], "countable": False, "bar": {"mean": val(top), "error": val(et)}}
    return also({"groups": out}, extra)


def _isnum(t: str) -> bool:
    try:
        float(t.replace("−", "-"))
        return True
    except ValueError:
        return False


# ------------------------------------------------------------------ marker curves (Fig. 2 B-D, Fig. S1 B and C)
def markers(p: Panel, rgb, tol: int = 100, k: int = 5, min_area: int = 4, x_lo=None, x_hi=None, exclude=()):
    """Marker centres (px) of one colour: the colour mask opened with a k×k disc, which removes whiskers, caps and
    fitted curves (thinner than k) and keeps the filled markers."""
    import cv2
    from livinglit.figures.source import blobs, colour_mask
    m = colour_mask(p.img, rgb, tol)
    a = 0 if x_lo is None else int(p.px(x_lo))
    b = m.shape[1] if x_hi is None else int(p.px(x_hi))
    m[:, :a] = False
    m[:, b:] = False
    for x0, y0, x1, y1 in exclude:  # legend symbols (page rects)
        m[max(0, int(p.py(y0))):int(p.py(y1)) + 1, max(0, int(p.px(x0))):int(p.px(x1)) + 1] = False
    ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
    core = cv2.erode(m.astype(np.uint8), ker)
    found = sorted(blobs(core, min_area=min_area), key=lambda d: d["x"])
    return m, found


def whisker_top(p: Panel, m, cx: float, cy: float, half: int = 1, cap_off: int = 3) -> float | None:
    """Upper end of a marker's error bar (px): the colour run up the marker's column, cap at its centre row."""
    x = int(round(cx))
    y = int(round(cy))
    while y > 0 and m[y - 1, x - half:x + half + 1].any():
        y -= 1
    top = y
    # the marker's own top edge: where the run is still marker-wide
    rows = []
    for yy in range(top, top + 6):
        if m[yy, x - cap_off - 1:x - cap_off + 1].any() or m[yy, x + cap_off:x + cap_off + 2].any():
            rows.append(yy)
        elif rows:
            break
    if not rows:
        return None
    return float(np.mean(rows))


def marker_panel(fig, ticks, series: dict, skip: int = 0, extra: dict | None = None, axis_hi=None, **kw):
    """series = {name: (rgb, [labels in x order])}. Each marker gives a mean; its whisker's cap gives the error.
    A marker whose whisker does not leave it gives error = mean."""
    p = Panel(fig, **{k: kw.pop(k) for k in ("dark_thr", "white_thr", "edge_thr") if k in kw})
    ax = p.y_axis(x_hi=axis_hi)
    p.calibrate_y(ax, ticks, skip=skip)
    out = {}
    for name, (rgb, labels) in series.items():
        m, found = markers(p, rgb, x_lo=p.page_x(ax[1] + 3), **kw)
        if len(found) != len([l for l in labels]):
            raise ValueError(f"{name}: found {len(found)} markers, expected {len(labels)}: "
                             f"{[(round(p.page_x(f['x']), 1), round(p.page_y(f['y']), 1), f['area']) for f in found]}")
        for lab, f in zip(labels, found):
            if lab is None:
                continue
            # marker centre from the opened core is symmetric; the cap is searched from the core's top
            top = whisker_top(p, m, f["x"], f["box"][1])
            mean = p.value(f["y"])
            err = mean if top is None or top >= f["box"][1] - 2 else p.value(top)
            MARKS.extend([(f["x"], f["y"], (0, 0, 255)), (f["x"], top or f["y"], (255, 0, 0))])
            out[lab] = {"points": [], "countable": False, "bar": {"mean": mean, "error": err}}
    return also({"groups": out}, extra)
