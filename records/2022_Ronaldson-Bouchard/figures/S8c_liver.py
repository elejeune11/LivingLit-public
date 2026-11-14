"""Supplementary Fig. 8c (left): doxorubicinol in the liver tissue chamber, 1, 24 and 72 hr (raster).

Bars are mean ± s.d. (whisker drawn upward only) with n=3 black dots per time point. Nothing is
drawn at 1 hr (no bar, no dots), so 1 hr is not read. The figure is one embedded image; reading is
in _util.read_panel. y axis 0-15 ng/mL, ticks every 5.
"""
from _util import read_panel


def read(fig):
    return {"groups": read_panel(fig, [0, 5, 10, 15], [None, "liver_h24", "liver_h72"], kernel=13)}
