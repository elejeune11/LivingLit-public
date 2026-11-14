"""Fig. 7G: BIRC5 expression, bars ± SEM (raster). Ticks 0-8 by 2."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 2, 4, 6, 8], ['d0', 'd10'])
