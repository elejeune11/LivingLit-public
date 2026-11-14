"""Fig. S8G: GFP+ cardiomyocytes (%), bar ± SEM (raster). Ticks 0-100 by 20."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 20, 40, 60, 80, 100], ['gfp'], axis_hi=161)
