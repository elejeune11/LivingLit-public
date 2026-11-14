"""Fig. 4D (isoprenaline, carbachol: relative force, T1, T2), bars mean ± SEM (raster, 300 dpi).

One y-axis per panel, left to right; tick values as printed on the labels, top to bottom; bars left
to right in the order of the x labels. Mean = centre of the bar's top outline; error = centre of the
error-bar cap (none when the cap does not clear the bar outline). Bars without points give no n.
Each reading is labelled for every evidence item that rests on it (LINKS)."""
from _util import bar_row, expand

LINKS = {
    'F4D_force_iso|iso': 'force|iso',
    'F4D_force_iso|bl': 'force|bl',
    'F4D_force_cch|isocch': 'force|isocch',
    'F4D_force_cch|iso': 'force|iso',
    'F4D_T1_iso|iso': 'T1|iso',
    'F4D_T1_iso|bl': 'T1|bl',
    'F4D_T1_cch|isocch': 'T1|isocch',
    'F4D_T1_cch|iso': 'T1|iso',
    'F4D_T2_iso|iso': 'T2|iso',
    'F4D_T2_iso|bl': 'T2|bl',
    'F4D_T2_cch|isocch': 'T2|isocch',
    'F4D_T2_cch|iso': 'T2|iso',
}


def read(fig):
    return expand(bar_row(fig, 300, [
        ('force', [150, 100, 50, 0], ['bl', 'iso', 'isocch']),
        ('T1', [150, 100, 50, 0], ['bl', 'iso', 'isocch']),
        ('T2', [150, 100, 50, 0], ['bl', 'iso', 'isocch']),
    ]), LINKS)
