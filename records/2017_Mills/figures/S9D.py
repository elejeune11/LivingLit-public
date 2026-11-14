"""Fig. S9D: pH3+ cardiomyocytes (%), bars ± SEM (raster). Ticks 0-0.6."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 0.2, 0.4, 0.6], ['gfp', 'bcat', 'yap'], extra={'gfp (vs YAP)': 'gfp'})
