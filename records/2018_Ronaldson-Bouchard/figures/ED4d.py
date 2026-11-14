"""Extended Data Fig. 4d: contraction frequency, FCT and early/late stage by regime and week (raster, 600 dpi).
The axis has no tick marks, so it is calibrated on the tick labels' centres. Bars touch: told apart by colour."""
import _util as U

COLOURS = {"fct": (65, 185, 65), "ctrl": (20, 20, 20), "const": (45, 85, 165), "int": (225, 30, 30)}
ORDER = ["fct"] + [f"{st}_{r}_w{w}" for st in ("e", "l") for w in (2, 3, 4) for r in ("ctrl", "const", "int")]
EARLY = [g for g in ORDER if g.startswith("e_")]
LINKS = {"ED4d_freq": ORDER, "ED4d_e_int_w3_vs_ctrl": ["e_int_w3", "e_ctrl_w3"],
         "ED4d_e_int_w4_vs_ctrl": ["e_int_w4", "e_ctrl_w4"], "ED4d_regimes": EARLY}


def read(fig):
    expect = ["fct" if g == "fct" else g.split("_")[1] for g in ORDER]
    g = U.colour_bar_panel(fig, axis_pt=(70, 85), tick_values=[160, 120, 80, 40, 0], bar_row_pt=380,
                           colours=COLOURS, labels=ORDER, expect=expect, ticks="labels", min_w_pt=2.5)
    return {"groups": U.expand(g, LINKS)}
