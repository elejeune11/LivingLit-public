"""Fig. S10B: pATM cardiomyocyte nuclear intensity (a.u.), bars ± SEM (raster). Ticks 0-100 by 20."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 20, 40, 60, 80, 100], ['d0', 'd10'])
