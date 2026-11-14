"""Fig. 5K: Ki-67+ cardiomyocytes (%), bars ± SEM (raster). Ticks 0-40 by 10."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 10, 20, 30, 40], ['ctrl_dmso', 'ctrl_chir', 'mm_dmso', 'mm_chir'], extra={'ctrl_chir (between)': 'ctrl_chir', 'mm_chir (between)': 'mm_chir'})
