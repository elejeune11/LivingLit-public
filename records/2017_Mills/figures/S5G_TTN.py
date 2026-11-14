"""Fig. S5G (first): TTN N2B relative to CTRL, bars ± SEM (raster). Ticks 0-15 by 5."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 5, 10, 15], ['ctrl', 'mm'])
