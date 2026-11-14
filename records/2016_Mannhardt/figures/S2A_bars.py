"""Fig. S2A: relative RNA expression [AU] of 21 genes in CM (grey), 2D (blue) and EHT (red), log axis
10^0 to 10^5, bars mean ± SEM (raster, 220 dpi).

The y-axis is calibrated (log) on its six decade ticks. Genes sit at the tick marks below the
x-axis, left to right in the printed order; within a gene's window each colour's bar is the widest
run of columns of that colour. The mean is the top edge of the bar's ink (colour fill, or the grey
bars' thin outline; sub-pixel from the ink of the row above) on the bar's first fill column (clear of
the whisker and cap); the error is the centre of the black cap on the bar's
centre column. Readings are labelled for the evidence items they serve (LINKS); genes covered by
Table S1 are not linked."""
import numpy as np

from _util import UNC_PX, axes, cal_from, dark, expand, group_ticks, reading, runs, triple, y_ticks

GENES = ["CACNA1C", "CACNB2", "CACNB3", "SCN1B", "SCN2A", "KCNH2", "KCNJ2", "KCNJ5", "KCNQ1", "HCN4", "ACTN2",
         "MYL2", "PLN", "RYR2", "TNNC1", "TNNT1", "DMD", "ADRB1", "NCX1", "SERCA2"]
DECADES = [1e5, 1e4, 1e3, 1e2, 1e1, 1e0]
LINKS = {f"S2A_{g}|{s}": f"{g}|{s}" for g in ["CACNA1C", "KCNH2", "KCNJ5", "KCNQ1", "HCN4", "ACTN2", "NCX1", "SERCA2"]
         for s in ("cm", "d2", "eht")}
LINKS.update({"S2A_MYL2_d2|d2": "MYL2|d2", "S2A_MYL2_d2|cm": "MYL2|cm",
              "S2A_MYL2_eht|eht": "MYL2|eht", "S2A_MYL2_eht|cm": "MYL2|cm"})


def strength(img, name):
    """Colour strength 0-1 per pixel for grey, blue and red bar fills."""
    r, g, b = img[:, :, 0].astype(float), img[:, :, 1].astype(float), img[:, :, 2].astype(float)
    if name == "blue":
        return np.clip((b - (r + g) / 2) / 255.0, 0, 1)
    if name == "red":
        return np.clip((r - (g + b) / 2) / 255.0, 0, 1)
    sat = img.max(axis=2) - img.min(axis=2)
    lum = img.mean(axis=2)
    return np.clip(1 - np.abs(lum - 160) / 60.0, 0, 1) * (sat < 25)  # mid grey


def read(fig):
    img, scale = fig.render(220)
    img = img.astype(int)
    ax = axes(img)[0]
    ticks = [t for t, _ in y_ticks(img, ax)]
    cal = cal_from(ticks, DECADES, log=True)
    gx, row = group_ticks(img, ax, img.shape[1])
    if len(gx) != len(GENES):
        raise ValueError(f"{len(gx)} gene ticks for {len(GENES)} genes: {gx}")
    pitch = float(np.median(np.diff(gx)))
    d = dark(img, 110)
    out = {}
    for gene, cx in zip(GENES, gx):
        for grp, col in (("cm", "grey"), ("d2", "blue"), ("eht", "red")):
            st = strength(img, col)
            x0, x1 = int(cx - 0.5 * pitch), int(cx + 0.5 * pitch)
            prof = (st[ax[2]:row - 2, x0:x1] > 0.5).sum(axis=0)
            rr = [r for r in runs(prof >= 3) if r[1] - r[0] + 1 >= 4]
            if not rr:
                raise ValueError(f"{gene} {grp}: no {col} bar")
            a, b = max(rr, key=lambda r: r[1] - r[0])
            xl, xr = a + x0, b + x0
            xe = xl  # the first fill column: clear of the whisker and the cap
            colm = st[:row - 2, xe] > 0.5
            r0 = int(np.argmax(colm))
            gy = img[:, xe].mean(axis=1)
            rt = r0
            while rt - 1 > 0 and gy[rt - 1] < 236 and r0 - rt < 2:  # the grey bars' thin outline
                rt -= 1
            edge = rt - 0.5 - (255 - gy[rt - 1]) / 255.0  # top edge of the ink, between pixel rows
            res = {"points": [], "countable": False,
                   "bar": {"mean": triple(reading(cal, edge, UNC_PX, fig, scale, ((xl + xr) / 2, edge)))}}
            xc = int(round((xl + xr) / 2))
            cr = runs(d[:r0, xc])
            if cr:
                ca, cb = cr[-1]  # the dark run nearest above the bar top: whisker and cap
                if cb >= r0 - 2 and ca < r0 - 2:
                    # the cap is the widest row of the run's top rows
                    cap = ca + 0.5 * min(2, cb - ca)
                    res["bar"]["error"] = triple(reading(cal, cap, UNC_PX, fig, scale, (xc, cap)))
            out[f"{gene}|{grp}"] = res
    return expand({"groups": out}, LINKS)
