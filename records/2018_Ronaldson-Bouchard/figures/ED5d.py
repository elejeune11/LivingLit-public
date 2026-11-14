"""Extended Data Fig. 5d: sarcomere-containing cells, early and late stage by regime (raster, 600 dpi). No tick
marks: calibrated on the tick labels' centres. Bars touch: told apart by colour."""
import _util as U

COLOURS = {"ctrl": (5, 5, 5), "const": (45, 85, 165), "int": (225, 30, 30)}
ORDER = ["e_ctrl", "e_const", "e_int", "l_ctrl", "l_const", "l_int"]
LINKS = {"ED5d_sarc": ORDER}


def read(fig):
    g = U.colour_bar_panel(fig, axis_pt=(334, 342), tick_values=[90, 80, 70, 60, 50, 40, 30, 20, 10, 0],
                           bar_row_pt=352, colours=COLOURS, labels=ORDER, expect=[o.split("_")[1] for o in ORDER],
                           ticks="labels", thr=170, min_w_pt=3)
    return {"groups": U.expand(g, LINKS)}
