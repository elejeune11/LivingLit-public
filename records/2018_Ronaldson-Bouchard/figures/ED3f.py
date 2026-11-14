"""Extended Data Fig. 3f: mean upstroke velocity, bars (raster, 600 dpi)."""
import _util as U

LINKS = {"ED3f_e_int_vs_e_ctrl": ["e_int", "e_ctrl"], "ED3f_e_int_vs_l_int": ["e_int", "l_int"]}


def read(fig):
    g = U.bar_panel(fig, axis_pt=(460, 472), tick_values=[30, 20, 10, 0], bar_row_pt=270,
                    labels=["e_ctrl", "l_int", "e_int"])
    return {"groups": U.expand(g, LINKS)}
