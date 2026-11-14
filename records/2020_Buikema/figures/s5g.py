"""Fig. S5G (relative pHH3+/TnT+ cells, P10 mouse myocardium), mmc1.pdf p. 10: filled triangles, one per biological
replicate (grey CTR, yellow CHIR), and a black mean line; no error bars or y tick marks. The legend triangles sit above
the panel and are kept out of its box; the stray '0 2 4' labels under the x axis are below it too. Fig. S5F is images."""
from _util import read_text_axis_triangles

BOX = (1240, 620, 1420, 1010.5)   # page box
TICKS = [0, 0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]   # tick labels as printed
GROUPS = ["ctr", "chir"]   # left to right


def read(fig):
    panel = read_text_axis_triangles(fig, BOX, TICKS, GROUPS)
    return {"groups": {f"S5G/{g}": panel[g] for g in GROUPS}}
