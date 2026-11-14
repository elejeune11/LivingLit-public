"""Fig. 4C (force, T1, T2 against pacing frequency), bars mean ± SEM (raster, 300 dpi).

One y-axis per panel, left to right; tick values as printed on the labels, top to bottom; bars left
to right in the order of the x labels. Mean = centre of the bar's top outline; error = centre of the
error-bar cap (none when the cap does not clear the bar outline). Bars without points give no n.
Each reading is labelled for every evidence item that rests on it (LINKS)."""
from _util import bar_row, expand

LINKS = {
    'F4C_force|f1p0': 'force|f1p0',
    'F4C_force|f1p1': 'force|f1p1',
    'F4C_force|f1p2': 'force|f1p2',
    'F4C_force|f1p4': 'force|f1p4',
    'F4C_force|f1p6': 'force|f1p6',
    'F4C_force|f1p8': 'force|f1p8',
    'F4C_force|f2p0': 'force|f2p0',
    'F4C_T1|f2p0': 'T1|f2p0',
    'F4C_T1|f1p0': 'T1|f1p0',
    'F4C_T2|f2p0': 'T2|f2p0',
    'F4C_T2|f1p0': 'T2|f1p0',
}


def read(fig):
    return expand(bar_row(fig, 300, [
        ('force', [0.15, 0.1, 0.05, 0], ['f1p0', 'f1p1', 'f1p2', 'f1p4', 'f1p6', 'f1p8', 'f2p0']),
        ('T1', [0.15, 0.1, 0.05, 0], ['f1p0', 'f1p1', 'f1p2', 'f1p4', 'f1p6', 'f1p8', 'f2p0']),
        ('T2', [0.15, 0.1, 0.05, 0], ['f1p0', 'f1p1', 'f1p2', 'f1p4', 'f1p6', 'f1p8', 'f2p0']),
    ]), LINKS)
