"""Fig. 7J: cardiomyocyte area (μm²), bars ± SEM (raster). Ticks 0-250 by 50."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 50, 100, 150, 200, 250], ['d0', 'd10'])
