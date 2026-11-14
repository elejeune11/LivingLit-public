"""Fig. 6C: pATM cardiomyocyte nuclear intensity (a.u.), bars ± SEM (raster). Ticks 0-150 by 50."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 50, 100, 150], ['ctrl', 'mm'])
