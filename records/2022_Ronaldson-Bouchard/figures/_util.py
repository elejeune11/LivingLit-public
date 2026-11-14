"""Helpers for this paper's raster bar charts with dots (GraphPad style, scanned into one image).

Supplementary Fig. 8 is one embedded image (877 x 974 px over 523 x 581 pt, about 121 dpi). Each
panel is rendered at 300 dpi and read from a dark-pixel mask:
- axes: the y axis is the longest dark column, the x axis the longest dark row near the bottom;
- y ticks: short dark runs just left of the y axis, centred, matched bottom-up to the printed
  tick values (the script gives them: the labels are pixels, not words);
- categories: short dark runs just below the x axis (x tick marks);
- dots: a morphological opening with a disc a little smaller than a dot keeps the filled dots and
  drops the thinner bar outlines, whiskers and caps; a dot blob taller or wider than 1.3 dot
  diameters is two or more touching dots, and that category's dots are not counted;
- bar top (mean) and cap (upper end of the s.d. whisker): rows of the mask, dots removed, that
  are dark across most of the bar's width (top) or across the cap's width only (cap). Each is read
  as the centre of its stroke with an interval covering the stroke's full thickness.
Marker uncertainty: one native image pixel (300/121 px at 300 dpi), not 0.6 px, because the
source image is coarser than the render; plus half the excess of a dot's box height over the
panel's smallest dot (a dot touching a line keeps a small bulge) and the calibration misfit.
"""
import cv2
import numpy as np

from livinglit.figures.source import blobs, calibrate, dark_mask

DPI = 300
NATIVE_PX = DPI / (877 / (559.32 - 36.0) * 72)  # one source-image pixel, in 300-dpi pixels


def _runs(idx):
    """Consecutive integer runs -> list of (start, end)."""
    out = []
    for i in idx:
        if out and i == out[-1][1] + 1:
            out[-1][1] = i
        else:
            out.append([i, i])
    return [tuple(r) for r in out]


def _triangle(size):
    """Upward-pointing filled triangle structuring element, size x size px."""
    k = np.zeros((size, size), np.uint8)
    for r in range(size):
        half = (r + 1) / size * size / 2
        k[r, int(round(size / 2 - half)):int(round(size / 2 + half))] = 1
    return k


def read_panel(fig, tick_values, categories, kernel, bar_half=34, cap_in=16, cap_out=26, tri=None, tri_cats=()):
    """Read one bar-and-dot panel. categories: labels left to right, one per x tick
    (None for a category not to be read). bar_half: half-width (px) of a band inside every bar and
    wider than every cap; cap_in / cap_out: half-widths inside and outside the caps.
    tri, tri_cats: the categories in tri_cats are drawn with filled upward triangles, not dots
    (as the figure shows). Their markers are found by an opening with a triangle of tri x tri px
    (thicker than every line, smaller than a marker; only blobs wholly above the x axis, which drops
    the bar-foot corners) and placed at their box centre (the opening keeps the apex and the base),
    with a sixth of the box height added to the interval (box centre against centroid).
    Returns {label: group dict}."""
    img, scale = fig.render(DPI)
    m = dark_mask(img, 128)
    h, w = m.shape
    col = m.sum(0)
    xa = _runs([i for i in range(w) if col[i] > 0.6 * h])
    x_axis0, x_axis1 = max(xa, key=lambda r: col[r[0]])  # y axis column run
    row = m[:, x_axis1 + 1:].sum(1)
    ya = _runs([i for i in range(h) if row[i] > 0.6 * row.max()])
    y_axis0, y_axis1 = ya[-1]  # x axis row run
    y_axis = (y_axis0 + y_axis1) / 2

    # y ticks: dark runs in the 12 px left of the y axis
    left = m[:, x_axis0 - 14:x_axis0 - 2].sum(1)
    ticks = [(a + b) / 2 for a, b in _runs([i for i in range(h) if left[i] >= 8])]
    if len(ticks) != len(tick_values):
        raise ValueError(f"found {len(ticks)} y ticks, expected {len(tick_values)}")
    marks = [(fig.to_page(0, t, scale)[1], v) for t, v in zip(sorted(ticks, reverse=True), tick_values)]
    cal = calibrate(marks)
    cal_px = cal.residual / abs(cal.slope) * scale  # misfit in 300-dpi px

    # x categories: dark runs just below the x axis
    below = m[y_axis1 + 3:y_axis1 + 14, :].sum(0)
    cats = [(a + b) / 2 for a, b in _runs([i for i in range(x_axis1 + 6, w) if below[i] >= 8])]
    if len(cats) != len(categories):
        raise ValueError(f"found {len(cats)} x ticks, expected {len(categories)}")
    half = min(np.diff(cats)) / 2 if len(cats) > 1 else 60

    # dots
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel, kernel))
    op = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, k).astype(bool)
    top_tick = min(ticks)
    dots = [b for b in blobs(op, min_area=kernel * kernel // 2)
            if b["x"] > x_axis1 + 6 and top_tick - 30 < b["y"] < y_axis1]

    def cat(b):
        return min(zip(cats, categories), key=lambda c: abs(c[0] - b["x"]))[1]
    dots = [b for b in dots if cat(b) not in tri_cats]
    diam = float(np.median([min(b["box"][2], b["box"][3]) for b in dots]))
    h_min = min(b["box"][3] for b in dots)
    for b in dots:
        b["size"], b["h_min"], b["extra"] = diam, h_min, 0.0
    if tri:
        top = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, _triangle(tri)).astype(bool)
        tris = [b for b in blobs(top, min_area=tri * tri // 4)
                if b["x"] > x_axis1 + 6 and top_tick - 30 < b["y"] and b["box"][1] + b["box"][3] <= y_axis0
                and cat(b) in tri_cats]
        if tris:
            t_size = float(np.median([min(b["box"][2], b["box"][3]) for b in tris]))
            t_min = min(b["box"][3] for b in tris)
            for b in tris:
                x0, y0, bw, bh = b["box"]
                b["y"] = y0 + (bh - 1) / 2
                b["size"], b["h_min"], b["extra"] = t_size, t_min, bh / 6
                op[y0:y0 + bh, x0:x0 + bw] |= top[y0:y0 + bh, x0:x0 + bw]
            dots = dots + tris
    dotmask = cv2.dilate(op.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
    ink = dark_mask(img, 200)  # thin whiskers and caps are anti-aliased grey

    def val(py):
        return cal.value(fig.to_page(0, py, scale)[1])

    def interval(py0, py1):
        a, b = val(py0), val(py1)
        return min(a, b), max(a, b)

    out = {}
    for cx, lab in zip(cats, categories):
        if lab is None:
            continue
        mine = [b for b in dots if abs(b["x"] - cx) < half]
        merged = [b for b in mine if b["box"][2] > 1.3 * b["size"] or b["box"][3] > 1.3 * b["size"]]
        g = {"points": [], "countable": not merged}
        if not merged:
            for b in sorted(mine, key=lambda b: b["y"]):
                unc_px = NATIVE_PX + (b["box"][3] - b["h_min"]) / 2 + b["extra"] + cal_px
                v = val(b["y"])
                lo, hi = interval(b["y"] + unc_px, b["y"] - unc_px)
                px, py = fig.to_page(b["x"], b["y"], scale)
                g["points"].append({"value": v, "lo": min(lo, v), "hi": max(hi, v), "at": [px, py]})

        # coverage of a row band by ink, counted over pixels not covered by a dot
        def cover(mask, x0, x1):
            free = ~dotmask[:, int(cx + x0):int(cx + x1)]
            ink = (mask[:, int(cx + x0):int(cx + x1)] & free).sum(1)
            n = free.sum(1)
            return np.where(n >= 8, ink / np.maximum(n, 1), 0.0)

        # bar top: rows dark across >= 90% of the central 2 x bar_half px (wider than any cap); a top
        # whose stroke runs into the x axis (a bar a few px high) gives no mean
        top_cov = cover(m, -bar_half, bar_half)
        top_rows = [i for i in range(int(top_tick) - 30, y_axis1 + 1) if top_cov[i] >= 0.9]
        bar = {}
        runs = _runs(top_rows)
        if runs and runs[0][1] < y_axis0 - 1:
            a, b = runs[0]
            mid = (a + b) / 2
            lo, hi = interval(b + 0.5 + NATIVE_PX + cal_px, a - 0.5 - NATIVE_PX - cal_px)
            bar["mean"] = [val(mid), min(lo, val(mid)), max(hi, val(mid))]
            # cap: a grey or dark horizontal stroke above the bar top, inked across >= 70% of the central
            # 2 x cap_in px and across <= 30% of the bands cap_out..bar_half px out on both sides
            c_cov = cover(ink, -cap_in, cap_in)
            s_cov = (cover(ink, -bar_half, -cap_out) + cover(ink, cap_out, bar_half)) / 2
            cap_rows = [i for i in range(int(top_tick) - 30, a - 1) if c_cov[i] >= 0.7 and s_cov[i] <= 0.3]
            # and joined to the bar top by the whisker: every row between inked (or under a dot) at cx
            stem = (ink | dotmask)[:, int(cx - 3):int(cx + 4)].any(1)
            caps = [(c0, c1) for c0, c1 in _runs(cap_rows) if stem[c1 + 1:a].all()]
            if caps:
                c0, c1 = caps[0]
                cm = (c0 + c1) / 2
                lo, hi = interval(c1 + 0.5 + NATIVE_PX + cal_px, c0 - 0.5 - NATIVE_PX - cal_px)
                bar["error"] = [val(cm), min(lo, val(cm)), max(hi, val(cm))]
        if bar:
            g["bar"] = bar
        out[lab] = g
    return out
