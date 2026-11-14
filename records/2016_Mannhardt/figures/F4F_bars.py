"""Fig. 4F right (post-rest potentiation: force), bars mean ± SEM (raster, 300 dpi).

One y-axis per panel, left to right; tick values as printed on the labels, top to bottom; bars left
to right in the order of the x labels. Mean = centre of the bar's top outline; error = centre of the
error-bar cap (none when the cap does not clear the bar outline). Bars without points give no n.
Each reading is labelled for every evidence item that rests on it (LINKS)."""
from _util import bar_row, expand

LINKS = {
    'F4F_prp|post': 'force|post',
    'F4F_prp|prior': 'force|prior',
}


def read(fig):
    return expand(bar_row(fig, 300, [
        ('force', [0.2, 0.15, 0.1, 0.05, 0], ['prior', 'post']),
    ]), LINKS)
