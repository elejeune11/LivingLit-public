"""Fig. S9H (right): force of contraction (μN), bars ± SEM (raster). Ticks 0-150 by 50."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 50, 100, 150], ['gfp', 'both'])
