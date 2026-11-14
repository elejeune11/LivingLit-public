"""Fig. 4D (main.pdf p. 8): BNP+ cells (%) in CUSO-2 hiPSC-CMs, PE - and + in GLUC, MM and MPAT; raster image
embedded at 300 dpi.

Each group plots its replicate points (one per induction) with a black mean line (~48 px wide) and an SEM error bar
whose caps (~24 px wide) are in the group's colour. GLUC markers are black circles, MM red squares, MPAT blue
triangles. Tick labels are part of the image, so the y axis is calibrated from the five raster tick marks left of the
axis, taken top to bottom as the printed 40, 30, 20, 10, 0 (0 sits on the x axis).
Group centres are the centres of the six mean lines, in x order GLUC -, GLUC +, MM -, MM +, MPAT -, MPAT +.
Markers are separated from error bars and caps by a morphological opening (5 x 5 ellipse) of the group's colour mask.
A marker whose box is larger than the median box of its shape (a cap merged with it) gets half the excess added to
its interval. A marker's position is its box centre (a triangle's centroid sits low). The opening removes ~4 px of
a triangle's apex, so a triangle's box is extended upward along its centre columns while the raw colour mask continues
(at most APEX_MAX px), with 1 px added to its interval.
The same group's points are returned once per item (labels "<item suffix>/<group>"), because a figure label links to
one item.
"""
import cv2
import numpy as np

from livinglit.figures.source import RASTER_UNCERTAINTY_PX_300DPI, blobs, calibrate, colour_mask, dark_mask, point

TICK_VALUES = [40, 30, 20, 10, 0]  # printed y tick labels, top to bottom
GROUPS = ["GLUC_VEH", "GLUC_PE", "MM_VEH", "MM_PE", "MPAT_VEH", "MPAT_PE"]  # x order
COLOURS = {"MM": (255, 0, 0), "MPAT": (0, 55, 255)}  # GLUC is black
ITEMS = {  # item suffix -> its two groups
    "MM_VEH_v_GLUC_VEH": ("MM_VEH", "GLUC_VEH"), "MPAT_VEH_v_GLUC_VEH": ("MPAT_VEH", "GLUC_VEH"),
    "MM_PE_v_MM_VEH": ("MM_PE", "MM_VEH"), "MPAT_PE_v_MPAT_VEH": ("MPAT_PE", "MPAT_VEH"),
}
HALF = 34  # px either side of a group's centre (groups are ~72 px apart)
MEAN_HALF = 22  # a mean-line row is dark over centre +- 22 px
CAP_HALF = 11  # a cap row is filled over centre +- 11 px
TRIANGLES = {"MPAT"}
APEX_MAX = 6  # px of apex the opening can remove (raw triangles are ~18 px tall, opened ~14)


def _bands(rows):
    """Contiguous runs of row indices -> list of (start, end)."""
    out = []
    for r in rows:
        if out and r == out[-1][1] + 1:
            out[-1][1] = r
        else:
            out.append([r, r])
    return [tuple(b) for b in out]


def read(fig):
    img, scale = fig.render(300)
    dark = dark_mask(img, 110)
    h, w = dark.shape
    unc_px = RASTER_UNCERTAINTY_PX_300DPI

    # y axis = the columns with the longest dark vertical runs; its top is the 40 tick, its bottom the x axis
    counts = dark.sum(axis=0)
    yaxis = [c for c in range(w) if counts[c] >= 0.9 * counts.max()]
    ax0, ax1 = min(yaxis), max(yaxis)
    top, bottom = max(_bands(list(np.where(dark[:, ax0])[0])), key=lambda b: b[1] - b[0])

    # y ticks: dark pixels just left of the axis
    tick_rows = [r for r in range(top - 3, bottom + 4) if dark[r, ax0 - 10:ax0 - 1].sum() >= 8]
    bands = _bands(tick_rows)
    if len(bands) != len(TICK_VALUES):
        raise ValueError(f"expected {len(TICK_VALUES)} y ticks, found {bands}")
    marks = []
    for (a, b), v in zip(bands, TICK_VALUES):
        g = 255 - img[a - 1:b + 2, ax0 - 10:ax0 - 1].mean(axis=(1, 2))
        yc = float(np.sum(np.arange(a - 1, b + 2) * g) / g.sum())
        marks.append((fig.to_page(0, yc, scale)[1], v))
    cal = calibrate(marks)
    misfit_pt = cal.residual / abs(cal.slope)

    # mean lines: rows whose dark run through a column spans +-MEAN_HALF; their centres give the groups
    inner = slice(top + 5, bands[-1][0] - 2)  # above the x axis
    lines = []
    for r in range(inner.start, inner.stop):
        row = dark[r]
        c = ax1 + 1
        while c < w:
            if row[c]:
                e = c
                while e + 1 < w and row[e + 1]:
                    e += 1
                if 2 * MEAN_HALF + 1 <= e - c + 1 <= 2 * MEAN_HALF + 8:
                    lines.append((r, (c + e) / 2))
                c = e + 1
            else:
                c += 1
    groups_x = []
    for r, x in sorted(lines, key=lambda t: t[1]):
        if groups_x and abs(x - groups_x[-1][-1][1]) <= 3:
            groups_x[-1].append((r, x))
        else:
            groups_x.append([(r, x)])
    if len(groups_x) != len(GROUPS):
        raise ValueError(f"expected {len(GROUPS)} mean lines, found {len(groups_x)}")

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    found_by, centre_by, mean_by = {}, {}, {}
    for g, rows in zip(GROUPS, groups_x):
        rr = sorted({r for r, _ in rows})
        if len(_bands(rr)) != 1:
            raise ValueError(f"{g}: expected one mean line, found rows {rr}")
        cx = float(np.mean([x for _, x in rows]))
        centre_by[g], mean_by[g] = cx, (rr[0], rr[-1])
        mask = colour_mask(img, COLOURS[g.split("_")[0]], 90) if g.split("_")[0] in COLOURS else dark
        region = np.zeros_like(dark)
        region[top + 5:bands[-1][0] - 2, int(cx - HALF):int(cx + HALF)] = True
        opened = cv2.morphologyEx((mask & region).astype(np.uint8), cv2.MORPH_OPEN, kernel).astype(bool)
        found_by[g] = [b for b in blobs(opened, min_area=60, max_area=400)
                       if 8 <= b["box"][2] <= 20 and 8 <= b["box"][3] <= 26]
        if len(found_by[g]) != 3:
            raise ValueError(f"{g}: expected 3 markers, found {len(found_by[g])}")

    # typical marker box per shape (colour family)
    typical = {}
    for fam in ("GLUC", "MM", "MPAT"):
        bs = [b["box"] for g in GROUPS if g.startswith(fam) for b in found_by[g]]
        typical[fam] = (float(np.median([b[2] for b in bs])), float(np.median([b[3] for b in bs])))

    per_group = {}
    for g in GROUPS:
        fam = g.split("_")[0]
        tw, th = typical[fam]
        pts = []
        raw = colour_mask(img, COLOURS[fam], 90) if fam in COLOURS else dark
        for b in sorted(found_by[g], key=lambda b: b["y"]):
            bx, by, bw, bh = b["box"]
            excess = max(bw - tw, bh - th, 0.0) / 2  # a cap merged with the marker
            u = (unc_px + excess) / scale + misfit_pt
            if fam in TRIANGLES:  # the opening cuts the apex: restore it from the raw mask, straight above the centre
                mid = bx + bw // 2
                grow = 0
                while grow < APEX_MAX and raw[by - grow - 1, mid - 1:mid + 2].any():
                    grow += 1
                by, bh = by - grow, bh + grow
                u += 1.0 / scale  # apex row is anti-aliased
            at = fig.to_page(bx + (bw - 1) / 2, by + (bh - 1) / 2, scale)
            pts.append(point(cal, at[1], u, at))

        # mean line centre, and the upper cap: nearest band above the mean filled over centre +- CAP_HALF
        cx = centre_by[g]
        c0, c1 = int(round(cx - CAP_HALF)), int(round(cx + CAP_HALF)) + 1
        m0, m1 = mean_by[g]
        caps = dark if fam not in COLOURS else colour_mask(img, COLOURS[fam], 90)
        cap_rows = [r for r in range(top + 5, m0 - 1) if caps[r, c0:c1].all()
                    and not dark[r, int(cx - MEAN_HALF):int(cx + MEAN_HALF)].all()]
        cb = _bands(cap_rows)
        if not cb:
            raise ValueError(f"{g}: no upper error-bar cap")
        cy = (cb[-1][0] + cb[-1][1]) / 2
        my = (m0 + m1) / 2
        lu = (unc_px + 1.0) / scale + misfit_pt  # line centre: 2-5 px thick
        my_pt, cy_pt = fig.to_page(0, my, scale)[1], fig.to_page(0, cy, scale)[1]
        mlo, mhi = cal.interval(my_pt, lu)
        elo, ehi = cal.interval(cy_pt, lu)
        per_group[g] = {"points": pts, "countable": True,
                        "bar": {"mean": [cal.value(my_pt), mlo, mhi], "error": [cal.value(cy_pt), elo, ehi]}}

    out = {}
    for suffix, pair in ITEMS.items():
        for g in pair:
            out[f"{suffix}/{g}"] = per_group[g]
    return {"groups": out}
