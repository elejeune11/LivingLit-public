"""Helpers for 2021_Zhang's figures only (vector panels drawn by Prism, and raster supplement panels).

Vector panels: every marker is a vector sub-path with exact coordinates; error bars are black paths whose
vertical stem runs from the centre of the lower cap to the centre of the upper cap, so the mean is the
midpoint of the stem and the upper end is its top. Axes are calibrated from each tick label matched to the
tick mark drawn just right of it.
"""
from __future__ import annotations

import numpy as np

from livinglit.figures.source import (RASTER_UNCERTAINTY_PX_300DPI, VECTOR_UNCERTAINTY_PT, calibrate,
                                      colour_mask, blobs, point)

BLACKISH = 0.2  # max channel for a "black" path (Prism draws axes and error bars in black or near-black)


def _num(t: str):
    try:
        return float(t.replace("−", "-").replace(",", ""))
    except ValueError:
        return None


def _inside(rect, region):
    x0, y0, x1, y1 = region
    cx, cy = (rect.x0 + rect.x1) / 2, (rect.y0 + rect.y1) / 2
    return x0 <= cx <= x1 and y0 <= cy <= y1


def _black(c):
    return c is not None and max(c) <= BLACKISH


def _paint(d):
    return d.get("fill") if d.get("fill") is not None else d.get("color")


def _subpaths(items):
    """Split a path's items into sub-paths (a new one starts where an item does not continue the last)."""
    subs, cur, last = [], [], None
    for it in items:
        if it[0] == "re":
            if cur:
                subs.append(cur)
                cur = []
            r = it[1]
            subs.append([(r.x0, r.y0), (r.x1, r.y1)])
            last = None
            continue
        pts = [(p.x, p.y) for p in it[1:]]
        if last is not None and (abs(pts[0][0] - last[0]) > 1e-3 or abs(pts[0][1] - last[1]) > 1e-3) and cur:
            subs.append(cur)
            cur = []
        cur += pts
        last = pts[-1]
    if cur:
        subs.append(cur)
    return subs


def ticks(fig, region):
    """(page y of tick centre, value, tick right end x) for every numeric label in region with a tick mark just right of it."""
    cands = []  # (x0, x1, y) of short horizontal black marks
    for d in fig.drawings():
        if not _inside(d["rect"], region) and not any(
                region[0] <= it[1].x <= region[2] and region[1] <= it[1].y <= region[3] for it in d["items"] if it[0] == "l"):
            continue
        if not _black(_paint(d)):
            continue
        r = d["rect"]
        if d.get("fill") is not None and 1.2 <= r.width <= 4.0 and r.height <= 1.2:
            cands.append((r.x0, r.x1, (r.y0 + r.y1) / 2))
        elif d.get("fill") is None:
            for it in d["items"]:
                if it[0] == "l" and abs(it[1].y - it[2].y) < 1e-3 and 1.2 <= abs(it[1].x - it[2].x) <= 4.0:
                    cands.append((min(it[1].x, it[2].x), max(it[1].x, it[2].x), it[1].y))
    marks = []
    for x0, y0, x1, y1, t in fig.words():
        v = _num(t)
        if v is None or not (region[0] <= x0 and x1 <= region[2] and region[1] <= y0 and y1 <= region[3]):
            continue
        cy = (y0 + y1) / 2
        near = [c for c in cands if abs(c[2] - cy) < 3.0 and 0 <= c[0] - x1 < 6.0]
        if near:
            c = min(near, key=lambda c: abs(c[2] - cy))
            marks.append((c[2], v, c[1]))
    return sorted(set(marks))


def markers(fig, region, exclude=()):
    """Centres (x, y) and paint of coloured (not black, white or grey) small vector sub-paths in region.

    A sub-path lying inside a larger one of the same path (the hole of a ring marker) is dropped.
    Some panels redraw parts of markers over the error bar: clipped pieces (not the panel's marker size,
    per colour) are dropped, and a redrawn whole marker (box within 0.3 pt of a marker of another path drawn with a
    different number of items) is counted once. Coincident markers drawn alike are separate markers."""
    from collections import Counter
    cands = []
    for k, d in enumerate(fig.drawings()):
        c = _paint(d)
        if c is None or (max(c) - min(c)) < 0.15:
            continue
        boxes = []
        for sp in _subpaths(d["items"]):
            xs, ys = [p[0] for p in sp], [p[1] for p in sp]
            boxes.append((min(xs), min(ys), max(xs), max(ys)))
        for i, b in enumerate(boxes):
            w, h = b[2] - b[0], b[3] - b[1]
            if not (0.8 < w < 6 and 0.8 < h < 6):
                continue
            if any(j != i and o[0] < b[0] - 0.1 and o[1] < b[1] - 0.1 and o[2] > b[2] + 0.1 and o[3] > b[3] + 0.1
                   for j, o in enumerate(boxes)):
                continue
            cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
            if region[0] <= cx <= region[2] and region[1] <= cy <= region[3] and not any(
                    e[0] <= cx <= e[2] and e[1] <= cy <= e[3] for e in exclude):
                cands.append((cx, cy, w, h, k, len(d["items"]), tuple(round(v, 2) for v in c)))
    out = []
    for col in {m[6] for m in cands}:
        ms = [m for m in cands if m[6] == col]
        mode = Counter((round(m[2], 1), round(m[3], 1)) for m in ms).most_common(1)[0][0]
        ms = [m for m in ms if abs(m[2] - mode[0]) <= 0.15 and abs(m[3] - mode[1]) <= 0.15]
        kept = []
        for m in ms:
            if any(abs(m[0] - o[0]) < 0.3 and abs(m[1] - o[1]) < 0.3 and m[4] != o[4] and m[5] != o[5] for o in kept):
                continue
            kept.append(m)
        out += [(m[0], m[1], m[6]) for m in kept]
    return out


def error_bars(fig, region, min_w=3.0, max_w=13.0):
    """Pure black error-bar paths in region (P-value lines are near-black and excluded): (x centre, upper cap centre y, lower cap centre y)."""
    out = []
    for d in fig.drawings():
        r = d["rect"]
        c = _paint(d)
        if not _inside(r, region) or c is None or max(c) > 0.05 or not (min_w <= r.width <= max_w):
            continue
        stems = [it for it in d["items"] if it[0] == "l" and abs(it[1].x - it[2].x) < 1e-3 and abs(it[1].y - it[2].y) > 1e-3]
        horiz = [it for it in d["items"] if it[0] == "l" and abs(it[1].y - it[2].y) < 1e-3]
        if not horiz:
            continue
        if stems and max(p.x for it in stems for p in it[1:]) - min(p.x for it in stems for p in it[1:]) > 1.5:
            continue  # two separated verticals: a bar outline, not an error bar
        if stems:
            ys = [p.y for it in stems for p in it[1:]]
            xs = [p.x for it in stems for p in it[1:]]
            out.append(((min(xs) + max(xs)) / 2, min(ys), max(ys)))
        else:  # error smaller than the cap: no stem drawn
            out.append(((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2, (r.y0 + r.y1) / 2, False))
            continue
        out[-1] = out[-1] + (True,)
    # one error bar may be drawn in several pieces (parts left over where markers knock it out):
    # pieces within 3 pt of each other in x are one bar; a stemless piece next to a stemmed one adds nothing
    merged = []
    for e in sorted(out):
        if merged and abs(e[0] - merged[-1][0][0]) < 3.0:
            merged[-1].append(e)
        else:
            merged.append([e])
    res = []
    for grp in merged:
        stemmed = [e for e in grp if e[3]] or grp
        main = max(stemmed, key=lambda e: e[2] - e[1])
        res.append((main[0], min(e[1] for e in stemmed), max(e[2] for e in stemmed)))
    return res


def read_panel(fig, region, labels, exclude=(), err_w=(3.0, 13.0), points=True):
    """One plot (bars or scatter with mean ± error): groups left to right get `labels`."""
    marks = ticks(fig, region)
    cal = calibrate([(m[0], m[1]) for m in marks])
    unc = VECTOR_UNCERTAINTY_PT + abs(cal.residual / cal.slope)
    axis_x = max(m[2] for m in marks)  # right end of the tick marks: the y axis; the plot lies right of it
    errs = [e for e in error_bars(fig, region, *err_w) if e[0] > axis_x]
    if len(errs) != len(labels):
        raise ValueError(f"found {len(errs)} error bars for {len(labels)} groups in {region}")
    groups = {}
    for (x, top, bot), lab in zip(errs, labels):
        mid = (top + bot) / 2
        m = point(cal, mid, unc, (x, mid))
        e = point(cal, top, unc, (x, top))
        groups[lab] = {"points": [], "countable": points,
                       "bar": {"mean": [m["value"], m["lo"], m["hi"]], "error": [e["value"], e["lo"], e["hi"]]}}
    if points:
        xs = [e[0] for e in errs]
        paints = {lab: set() for lab in labels}
        for cx, cy, col in sorted(markers(fig, region, exclude), key=lambda m: (m[0], m[1])):
            if cx <= axis_x:
                continue
            k = int(np.argmin([abs(cx - x) for x in xs]))
            groups[labels[k]]["points"].append(point(cal, cy, unc, (cx, cy)))
            paints[labels[k]].add(col)
        mixed = {lab: p for lab, p in paints.items() if len(p) > 1}
        if mixed:  # each group is drawn in one colour; a mix means markers were given to the wrong group
            raise ValueError(f"markers of several colours in one group: {mixed}")
    return groups


# ---------------------------------------------------------------- raster panels (the supplement's figures are images)

BLUE, RED = (70, 135, 200), (230, 40, 35)


def _runs(mask_1d):
    """(start, end) index pairs of True runs."""
    out, start = [], None
    for i, v in enumerate(mask_1d):
        if v and start is None:
            start = i
        if not v and start is not None:
            out.append((start, i - 1))
            start = None
    if start is not None:
        out.append((start, len(mask_1d) - 1))
    return out


def read_raster_bars(fig, region, labels, tick_values, colours=(BLUE, RED), dpi=300, colour_tol=70):
    """One raster bar plot: bars left to right get `labels`; ticks top to bottom carry `tick_values`
    (the printed tick labels, which are part of the image).

    Mean = midpoint of the error bar's two caps (a cap hidden in the bar's top edge is read as that edge),
    error = the upper cap. Markers are counted only when every marker of the plot stands alone (blob areas
    all within 0.8-1.2 x the median blob of their colour); otherwise the group gives its bar only."""
    img, scale = fig.render(dpi)
    ox, oy = (region[0] - fig.crop[0]) * scale, (region[1] - fig.crop[1]) * scale
    sub = img[int(oy):int((region[3] - fig.crop[1]) * scale), int(ox):int((region[2] - fig.crop[0]) * scale)]
    to_page = lambda px, py: fig.to_page(px + int(ox), py + int(oy), scale)
    black = sub.astype(int).max(axis=2) < 90
    H, W = black.shape
    cols = [(x, a, b) for x in range(W) for a, b in _runs(black[:, x]) if b - a >= 12]
    xs = sorted({c[0] for c in cols})
    lines = []  # adjacent columns with tall black runs form one vertical line
    for x in xs:
        if lines and x - lines[-1][-1] <= 1:
            lines[-1].append(x)
        else:
            lines.append([x])
    longest = max(cols, key=lambda c: c[2] - c[1])  # the y axis is the longest single run
    axis = next(l for l in lines if longest[0] in l)
    axis_x = (axis[0] + axis[-1]) / 2
    axis_bottom = longest[2]
    # a line's extent counts only runs starting above the x axis (labels below it are not part of it)
    span = lambda l: (min(c[1] for c in cols if c[0] in l and c[1] < axis_bottom - 5),
                      max(c[2] for c in cols if c[0] in l and c[1] < axis_bottom - 5))
    lines = [l for l in lines if any(c[1] < axis_bottom - 5 for c in cols if c[0] in l)]
    # bar sides reach down to the x axis; error-bar stems end above it
    sides = [(l[0] + l[-1]) / 2 for l in lines if l is not axis and (l[0] + l[-1]) / 2 > axis_x
             and abs(span(l)[1] - axis_bottom) <= 4]
    if len(sides) != 2 * len(labels):
        raise ValueError(f"found {len(sides)} bar sides for {len(labels)} bars in {region}")
    bars = [(sides[2 * i], sides[2 * i + 1]) for i in range(len(labels))]
    # ticks: short horizontal black runs ending at the axis, top to bottom
    tk = [y for y in range(H) for a, b in _runs(black[y, :int(axis_x) + 2]) if b >= axis_x - 2 and 4 <= b - a <= 20]
    tick_y = [(a + b) / 2 for a, b in _runs(np.isin(np.arange(H), tk))]
    if len(tick_y) != len(tick_values):
        raise ValueError(f"found {len(tick_y)} ticks for {len(tick_values)} tick labels in {region}")
    cal = calibrate(list(zip(tick_y, tick_values)))
    unc = RASTER_UNCERTAINTY_PX_300DPI * dpi / 300 + abs(cal.residual / cal.slope)
    pt = lambda px, py: point(cal, py, unc, to_page(px, py))
    groups = {}
    for (l, r), lab in zip(bars, labels):
        w = r - l
        xc = int(round((l + r) / 2))
        colour = (sub.astype(int).max(axis=2) - sub.astype(int).min(axis=2)) > 80
        stem = (black | colour)[:, xc - 1:xc + 2].any(axis=1)  # stem, or a marker drawn over it
        # the bar's top edge: a mostly black row joining both sides (a P-value line does not reach both)
        side_l = black[:, int(l) - 1:int(l) + 2].any(axis=1)
        side_r = black[:, int(r) - 1:int(r) + 2].any(axis=1)
        top_rows = (black[:, int(l + 4):int(r - 3)].mean(axis=1) >= 0.6) & side_l & side_r & (np.arange(H) < axis_bottom - 3)
        top = _runs(top_rows)[0]
        # cap rows: many black pixels within the cap's reach (markers drawn over a cap hide parts of it),
        # none just beyond it (the P-value line runs on past the cap), and not the bar's top edge
        win = black[:, int(xc - 0.3 * w):int(xc + 0.3 * w) + 1].sum(axis=1)
        beyond = np.maximum(black[:, int(xc + 0.33 * w):int(xc + 0.45 * w) + 1].mean(axis=1),
                            black[:, int(xc - 0.45 * w):int(xc - 0.33 * w) + 1].mean(axis=1))
        capr = (win >= 0.25 * w) & (beyond < 0.5)
        capr[max(top[0] - 1, 0):top[1] + 2] = False
        caps = [c for c in _runs(capr) if c[1] < axis_bottom - 3 and c[1] - c[0] <= 8]
        above = [c for c in caps if c[1] < top[0]]
        below = [c for c in caps if c[0] > top[1]]
        # the error bar's caps are the bands nearest the bar's top edge on either side; one hidden in the
        # top edge is read as the edge itself
        upper = above[-1] if above else top
        lower = below[0] if below else top
        uy = (upper[0] + upper[1]) / 2
        my = ((lower[0] + lower[1]) / 2 + uy) / 2
        if above and stem[int(uy):int(my) + 1].mean() < 0.6:  # the stem, or markers over it, joins cap and mean
            raise ValueError(f"{lab}: no stem between cap and mean")
        m, e = pt(xc, my), pt(xc, uy)
        groups[lab] = {"points": [], "countable": True,
                       "bar": {"mean": [m["value"], m["lo"], m["hi"]], "error": [e["value"], e["lo"], e["hi"]]}}
    found, alone = [], True
    for col in colours:
        mask = colour_mask(sub, col, colour_tol)
        mask[:, :int(axis_x) + 2] = False
        # colour fringes of antialiased black lines and text are 1-2 px thin: not markers
        bl = [x for x in blobs(mask, min_area=8) if min(x["box"][2], x["box"][3]) >= 5]
        if not bl:
            continue
        areas = sorted(x["area"] for x in bl)
        med = areas[len(areas) // 2]
        if not all(0.8 * med <= x["area"] <= 1.2 * med for x in bl):  # merged or split markers
            alone = False
        found += bl
    alone = alone and bool(found)
    centres_x = [(l + r) / 2 for l, r in bars]
    for lab in labels:
        groups[lab]["countable"] = alone
    if alone:
        for b in sorted(found, key=lambda b: (b["x"], b["y"])):
            k = int(np.argmin([abs(b["x"] - c) for c in centres_x]))
            groups[labels[k]]["points"].append(pt(b["x"], b["y"]))
    return groups
