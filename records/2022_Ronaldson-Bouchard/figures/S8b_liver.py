"""Supplementary Fig. 8b (left): doxorubicin in the liver tissue chamber, 5 min to 72 hr (raster).

Bars are mean ± s.d. (whisker drawn upward only) with n=3 black dots per time point. The figure
is one embedded image; reading is in _util.read_panel. y axis 0-5000 ng/mL, ticks every 1000.
"""
from _util import read_panel


def read(fig):
    return {"groups": read_panel(fig, [0, 1000, 2000, 3000, 4000, 5000],
                                 ["liver_m5", "liver_h1", "liver_h24", "liver_h72"], kernel=15)}
