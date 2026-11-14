"""Fig. 7F: pH3+ cardiomyocytes (%), bars ± SEM (raster). Ticks 0.0-2.0 by 0.5."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0.0, 0.5, 1.0, 1.5, 2.0], ['d0', 'd10'])
