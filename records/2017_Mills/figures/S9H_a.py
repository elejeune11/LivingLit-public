"""Fig. S9H (left): force of contraction (μN), bars ± SEM (raster). The AAV6-GFP (1X) bar is no group of the record: located, not returned. Ticks 0-200 by 50."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 50, 100, 150, 200], [None, 'bcat', 'yap'])
