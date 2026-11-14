"""Extended Data Fig. 3c: resting membrane potential, bars hanging down from 0 (raster, 600 dpi)."""
import _util as U

LINKS = {"ED3c_rmp": ["e_int", "e_ctrl"]}


def read(fig):
    g = U.bar_panel(fig, axis_pt=(80, 95), tick_values=[0, -20, -40, -60, -80], bar_row_pt=205,
                    labels=["e_ctrl", "l_int", "e_int"], direction=+1)
    return {"groups": U.expand(g, LINKS)}
