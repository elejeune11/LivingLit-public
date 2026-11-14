"""Fig. S4 (E-4031, isoprenaline, HMR-1556: beats per minute, force, T2), bars mean ± SEM (raster, 220 dpi).

One y-axis per panel, left to right; tick values as printed on the labels, top to bottom; bars left
to right in the order of the x labels. Mean = centre of the bar's top outline; error = centre of the
error-bar cap (none when the cap does not clear the bar outline). Bars without points give no n.
Each reading is labelled for every evidence item that rests on it (LINKS)."""
from _util import bar_row, expand

LINKS = {
    'S4_freq_hmr|eih': 'freq|eih',
    'S4_freq_hmr|ei': 'freq|ei',
    'S4_freq_all|bl': 'freq|bl',
    'S4_freq_all|e': 'freq|e',
    'S4_freq_all|ei': 'freq|ei',
    'S4_freq_all|eih': 'freq|eih',
    'S4_force_hmr|eih': 'force|eih',
    'S4_force_hmr|ei': 'force|ei',
    'S4_T2_hmr|eih': 'T2|eih',
    'S4_T2_hmr|ei': 'T2|ei',
    'S4_T2_e|e': 'T2|e',
    'S4_T2_e|bl': 'T2|bl',
    'S4_T2_ei|ei': 'T2|ei',
    'S4_T2_ei|e': 'T2|e',
}


def read(fig):
    return expand(bar_row(fig, 220, [
        ('freq', [80, 60, 40, 20, 0], ['bl', 'e', 'ei', 'eih']),
        ('force', [0.2, 0.15, 0.1, 0.05, 0], ['bl', 'e', 'ei', 'eih']),
        ('T2', [0.3, 0.2, 0.1, 0], ['bl', 'e', 'ei', 'eih']),
    ]), LINKS)
