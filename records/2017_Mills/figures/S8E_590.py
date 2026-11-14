"""Fig. S8E (right): miR-590 expression, bars ± SEM (raster). The scramble bar lies on the axis line and is not found, so only the miR bar is read. Ticks 0-5000 by 1000."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 1000, 2000, 3000, 4000, 5000], ['mir590'], dark_thr=170)
