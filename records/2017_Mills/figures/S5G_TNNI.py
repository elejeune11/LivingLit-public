"""Fig. S5G (third): TNNI3/1 ratio, bars ± SEM (raster). Ticks 0.00-0.04 by 0.01."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0.0, 0.01, 0.02, 0.03, 0.04], ['ctrl', 'mm'])
