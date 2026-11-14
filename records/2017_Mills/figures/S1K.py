"""Fig. S1K: tissue viability (%), bars ± SEM (raster), CTRL/SF pairs by matrix. Ticks 0-100 by 20."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 20, 40, 60, 80, 100], ['ctrl_low', 'sf_low', 'ctrl_high', 'sf_high', 'ctrl_highmg', 'sf_highmg'], merge=6)
