"""Fig. S9C: Ki-67+ cardiomyocytes (%), bars ± SEM (raster). Ticks 0-10."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 2, 4, 6, 8, 10], ['gfp', 'bcat', 'yap'], extra={'gfp (vs YAP)': 'gfp'})
