"""Fig. 7E: Ki-67+ cardiomyocytes (%), bars ± SEM (raster). Ticks 0-60 by 20."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 20, 40, 60], ['d0', 'd3', 'd10', 'd30'], extra={'d0 (vs 30 μM)': 'd0'})
