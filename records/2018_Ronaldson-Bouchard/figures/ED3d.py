"""Extended Data Fig. 3d: action potential peak amplitude, bars (raster, 600 dpi; grey axis)."""
import _util as U

LINKS = {"ED3d_amp": ["e_ctrl", "l_int", "e_int"]}


def read(fig):
    g = U.bar_panel(fig, axis_pt=(203, 215), tick_values=[60, 40, 20, 0], bar_row_pt=265,
                    labels=["e_ctrl", "l_int", "e_int"], thr=170)
    return {"groups": U.expand(g, LINKS)}
