"""Fig. S4D: sarcomere length (μm), bars ± SEM (raster). Ticks 0-3 by 1."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 1, 2, 3], ['ctrl', 'mm'])
