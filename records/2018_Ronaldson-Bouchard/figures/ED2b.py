"""Extended Data Fig. 2b: gene expression in early-stage tissues of three lines, five genes, 45 bars (raster, 600 dpi).
Bars touch, so they are told apart by colour (black control, blue constant, red intensity); mean +/- 95% CI."""
import _util as U

GENES = ["SCN5A", "RYR2", "CACNA1C", "ATP2A2", "MYH7_MYH6"]
LINES = ["c2a", "wtc", "imr"]
REG = ["ctrl", "const", "int"]
COLOURS = {"ctrl": (0, 0, 0), "const": (55, 85, 165), "int": (235, 30, 35)}
LINKS = {f"ED2b_{g}": [f"{r}_{l}" for r in REG for l in LINES] for g in GENES}


def read(fig):
    labels, expect = [], []
    for gene in GENES:
        for line in LINES:
            for r in REG:
                labels.append(f"{gene}:{r}_{line}")
                expect.append(r)
    g = U.colour_bar_panel(fig, axis_pt=(75, 85), tick_values=[8, 7, 6, 5, 4, 3, 2, 1, 0], bar_row_pt=310,
                           colours=COLOURS, labels=labels, expect=expect, min_w_pt=2.5)
    out = {}
    for item, gids in LINKS.items():
        gene = item[len("ED2b_"):]
        for gid in gids:
            out[f"{item}/{gid}"] = g[f"{gene}:{gid}"]
    return {"groups": out}
