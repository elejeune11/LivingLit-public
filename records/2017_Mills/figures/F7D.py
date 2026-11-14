"""Fig. 7D: Ki-67 relative intensity, bars ± SEM (raster). Ticks 0-15 by 5."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 5, 10, 15], ['d0', 'd3', 'd10', 'd30'], extra={'d0 (vs 30 μM)': 'd0'})
