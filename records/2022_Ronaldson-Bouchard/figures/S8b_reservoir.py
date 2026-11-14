"""Supplementary Fig. 8b (right): doxorubicin in the reservoir, 5 min to 72 hr (raster).

Bars are mean ± s.d. (whisker drawn upward only) with n=3 black dots per time point. The figure
is one embedded image; reading is in _util.read_panel. y axis 0-25000 ng/mL, ticks every 5000.
"""
from _util import read_panel


def read(fig):
    return {"groups": read_panel(fig, [0, 5000, 10000, 15000, 20000, 25000],
                                 ["reservoir_m5", "reservoir_h1", "reservoir_h24", "reservoir_h72"], kernel=15)}
