"""Extended Data Fig. 5a: cell elongation ratio by regime and week (raster, 600 dpi). No tick marks: calibrated on
the tick labels' centres. Bars touch: told apart by colour (black 1, red 2, grey 3, blue 4 weeks). FCT is not drawn."""
import _util as U

COLOURS = {"w1": (20, 20, 20), "w2": (225, 30, 30), "w3": (190, 190, 200), "w4": (45, 85, 165)}
ORDER = [f"{r}_w{w}" for r in ("ctrl", "const", "int") for w in (1, 2, 3, 4)]
LINKS = {"ED5a_elong": ORDER, "ED5a_regimes": ORDER, "ED5a_int_w4_vs_fct": ["int_w4"]}


def read(fig):
    g = U.colour_bar_panel(fig, axis_pt=(150, 162), tick_values=[1.0, 0.75, 0.5, 0.25, 0], bar_row_pt=186,
                           colours=COLOURS, labels=ORDER, expect=[o.split("_")[1] for o in ORDER], ticks="labels",
                           min_w_pt=2.5)
    return {"groups": U.expand(g, LINKS)}
