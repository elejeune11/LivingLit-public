"""Fig. 5J: Ki-67 relative intensity, bars ± SEM (raster). Ticks 0-3 by 1."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 1, 2, 3], ['ctrl_dmso', 'ctrl_chir', 'mm_dmso', 'mm_chir'], extra={'ctrl_chir (between)': 'ctrl_chir', 'mm_chir (between)': 'mm_chir'})
