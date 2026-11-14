"""Fig. S8E (left): miR-199a expression, bars ± SEM (raster). The scramble bar lies on the axis line and is not found, so only the miR bar is read. Ticks 0-600 by 200."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 200, 400, 600], ['mir199a'], dark_thr=170)
