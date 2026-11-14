"""Extended Data Fig. 3e: action potential duration (APD90), bars (raster, 600 dpi; grey axis)."""
import _util as U

LINKS = {"ED3e_apd": ["e_ctrl", "l_int", "e_int"]}


def read(fig):
    g = U.bar_panel(fig, axis_pt=(345, 360), tick_values=[1500, 1000, 500, 0], bar_row_pt=265,
                    labels=["e_ctrl", "l_int", "e_int"], thr=170)
    return {"groups": U.expand(g, LINKS)}
