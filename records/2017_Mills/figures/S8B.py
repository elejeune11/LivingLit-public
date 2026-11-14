"""Fig. S8B: pH3+ neonatal rat cardiomyocytes (%), bars ± SEM (raster). Ticks 0-6 by 2."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 2, 4, 6], ['ctrl', 'chir', 'nrg1', 'mir199a', 'mir590', 'adyap'], dark_thr=170)
