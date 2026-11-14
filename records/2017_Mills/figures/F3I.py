"""Fig. 3I: proteomics expression relative to CTRL, bars ± SEM (raster). Ticks 0-5 by 1."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 1, 2, 3, 4, 5], ['MYH7 ctrl', 'MYH7 mm', 'IRX4 ctrl', 'IRX4 mm', 'MYBPC3 ctrl', 'MYBPC3 mm'])
