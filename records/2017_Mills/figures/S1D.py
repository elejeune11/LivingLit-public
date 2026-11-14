"""Fig. S1D: Ki-67 relative intensity, bars ± SEM (raster). Ticks 0-4 by 1."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 1, 2, 3, 4], ['dmso', 'chir'])
