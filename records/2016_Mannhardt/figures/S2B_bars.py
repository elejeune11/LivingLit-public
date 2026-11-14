"""Fig. S2B: mean fold change in RNA expression, EHT vs. 2D, 21 genes (raster, 220 dpi).

Bars hang from the 0 line (up or down), black outlines, light-grey fill, no error bars. The
y-axis is calibrated on its ticks (4, 2, 0, -2, -4 as printed, top to bottom). Genes sit at the
tick marks below the bottom axis line, left to right in the printed order. A bar's end is the
first outline met, scanning from the far end towards the 0 line, that has grey fill (four rows) on its
inner side (so the dashed line at 1 and the 'n.s.' labels are passed over). The column scanned is set
off from the gene's centre by 0.22 of the gene pitch, clear of the centred 'n.s.' labels. Readings
are labelled for the evidence items they serve (LINKS); genes covered by Table S1 are not linked.
HCN4 is not plotted in this panel."""
import numpy as np

from _util import UNC_PX, axes, cal_from, dark, expand, gray, group_ticks, reading, runs, triple, y_ticks

GENES = ["CACNA1C", "CACNB2", "CACNB3", "SCN1B", "SCN2A", "KCNH2", "KCNJ2", "KCNJ5", "KCNQ1", "ACTN2", "MYL2",
         "PLN", "RYR2", "TNNC1", "TNNT1", "DMD", "ADRB1", "NCX1", "SERCA2"]
V = [4, 2, 0, -2, -4]
# a fold change belongs to the pair (EHT vs. 2D), not to one group: group "_"
LINKS = {f"S2B_{g}|_": f"fc|{g}" for g in ["CACNA1C", "KCNH2", "KCNJ5", "KCNQ1", "ACTN2", "MYL2", "NCX1", "SERCA2"]}


def fill(g, y, x, step, n=4):
    """Grey bar fill for n rows from y in direction step."""
    return all(180 <= g[y + k * step, x] <= 235 for k in range(n))


def read(fig):
    img, scale = fig.render(220)
    img = img.astype(int)
    g = gray(img)
    d = dark(img, 110)
    ax = axes(img)[0]
    ticks = [t for t, _ in y_ticks(img, ax)]
    cal = cal_from(ticks, V)
    zero = int(round(ticks[2]))
    gx, bottom = group_ticks(img, ax, img.shape[1])
    if len(gx) != len(GENES):
        raise ValueError(f"{len(gx)} gene ticks for {len(GENES)} genes")
    pitch = float(np.median(np.diff(gx)))
    out = {}
    for gene, cx in zip(GENES, gx):
        x = int(round(cx - 0.22 * pitch))
        up = 180 <= g[zero - 4, x] <= 235  # grey fill just above the 0 line: an upward bar
        down = 180 <= g[zero + 4, x] <= 235
        if up == down:
            raise ValueError(f"{gene}: cannot tell the bar's direction")
        col = d[:, x]
        if up:
            rr = [r for r in runs(col[ax[2] - 2:zero - 2]) if fill(g, ax[2] - 2 + r[1] + 2, x, +1)]
            a, b = rr[0][0] + ax[2] - 2, rr[0][1] + ax[2] - 2
        else:
            rr = [r for r in runs(col[zero + 3:bottom - 1]) if fill(g, zero + 3 + r[0] - 2, x, -1)]
            a, b = rr[-1][0] + zero + 3, rr[-1][1] + zero + 3
        end = (a + b) / 2.0
        out[f"fc|{gene}"] = {"points": [], "countable": False,
                             "bar": {"mean": triple(reading(cal, end, UNC_PX, fig, scale, (cx, end)))}}
    return expand({"groups": out}, LINKS)
