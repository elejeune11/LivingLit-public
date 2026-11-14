"""Fig. S5G (second): MYH7/6 ratio, bars ± SEM (raster). Ticks 0-10 by 2."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 2, 4, 6, 8, 10], ['ctrl', 'mm'])
