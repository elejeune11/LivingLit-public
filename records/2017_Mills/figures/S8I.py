"""Fig. S8I: force of contraction (μN), bars ± SEM (raster). Bars no item compares are located but not returned. Ticks 0-400 by 100."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 100, 200, 300, 400], ['dmso', 'chir', None, None, None, None, None, None, None], dark_thr=170)
