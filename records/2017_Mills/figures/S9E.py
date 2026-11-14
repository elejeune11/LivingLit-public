"""Fig. S9E: BIRC5, bars ± SEM (raster). Ticks 0-2.0."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 0.5, 1.0, 1.5, 2.0], ['gfp', 'bcat', 'yap'], extra={'gfp (vs YAP)': 'gfp'})
