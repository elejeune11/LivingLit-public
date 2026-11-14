"""Fig. 4D: fatty acid oxidation OCR (% baseline), bars ± SEM (raster). Ticks 0-25 by 5."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 5, 10, 15, 20, 25], ['ctrl', 'mm'])
