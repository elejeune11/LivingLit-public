"""Fig. S9G: BIRC5, bars ± SEM (raster). Ticks 0-5 by 1."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 1, 2, 3, 4, 5], ['gfp', 'both'])
