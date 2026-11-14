"""Extended Data Fig. 10c: cell area by stage, treatment and regime (raster, 600 dpi). Calibrated on the tick
labels' centres (no tick marks found). Bars touch: told apart by colour. Mean +/- 95% CI."""
import _util as U

COLOURS = {"ctrl": (5, 5, 5), "const": (45, 65, 145), "int": (225, 10, 25)}
ORDER = [f"{st}_{t}_{r}" for st in ("e", "l") for t in ("none", "angii", "et1", "iso") for r in ("ctrl", "const", "int")]
LINKS = {"ED10c_area": ORDER, "ED10c_long_lines": ORDER}
for t in ("none", "angii", "et1", "iso"):
    LINKS[f"ED10c_e_{t}_regimes"] = [f"e_{t}_{r}" for r in ("ctrl", "const", "int")]


def read(fig):
    g = U.colour_bar_panel(fig, axis_pt=(92, 104), tick_values=[2500, 2000, 1500, 1000, 500, 0], bar_row_pt=362,
                           colours=COLOURS, labels=ORDER, expect=[o.split("_")[2] for o in ORDER], ticks="labels",
                           min_w_pt=3)
    return {"groups": U.expand(g, LINKS)}
