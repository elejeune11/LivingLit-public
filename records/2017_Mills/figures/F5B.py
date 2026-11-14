"""Fig. 5B: pH3+ cardiomyocytes (%), bars ± SEM (raster). Ticks 0.0-0.6 by 0.2."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0.0, 0.2, 0.4, 0.6], ['ctrl', 'mm'])
