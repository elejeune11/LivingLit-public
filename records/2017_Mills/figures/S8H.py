"""Fig. S8H: pH3+ cardiomyocytes (%), bars ± SEM (raster). Bars no item compares are located but not returned. Ticks 0.0-2.5 by 0.5."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0.0, 0.5, 1.0, 1.5, 2.0, 2.5], ['dmso', 'chir', None, None, None, None, 'mcs', 'bcat', 'yap'], extra={'mcs (vs YAP)': 'mcs'}, dark_thr=170)
