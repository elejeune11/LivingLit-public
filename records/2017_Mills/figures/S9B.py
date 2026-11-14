"""Fig. S9B: Ki-67 relative intensity, bars ± SEM (raster). Ticks 0-1.5."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 0.5, 1.0, 1.5], ['gfp', 'bcat', 'yap'], extra={'gfp (vs YAP)': 'gfp'})
