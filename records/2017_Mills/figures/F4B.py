"""Fig. 4B: maximum OCR (% baseline), bars ± SEM (raster). Ticks 0-200 by 50."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 50, 100, 150, 200], ['ctrl', 'mm'])
