"""Fig. S7D (ajmaline): frequency, force, T1 and T2 scatter plots with red mean lines (raster, 220 dpi).

One y-axis per panel, left to right; tick values as printed on the labels, top to bottom.
Groups left to right in the order of the x labels. Markers overlap, so means only.
Each reading is labelled for every evidence item that rests on it (LINKS)."""
from _util import expand, scatter_row

G = ['bl', 'l1', 'l2', 'l3', 'l4', 'l5', 'l6']
V = [250, 200, 150, 100, 50, 0]
LINKS = {
    'S7D_freq|bl': 'freq|bl',
    'S7D_freq|l1': 'freq|l1',
    'S7D_freq|l2': 'freq|l2',
    'S7D_freq|l3': 'freq|l3',
    'S7D_freq|l4': 'freq|l4',
    'S7D_freq|l5': 'freq|l5',
    'S7D_freq|l6': 'freq|l6',
    'S7D_force|bl': 'force|bl',
    'S7D_force|l1': 'force|l1',
    'S7D_force|l2': 'force|l2',
    'S7D_force|l3': 'force|l3',
    'S7D_force|l4': 'force|l4',
    'S7D_force|l5': 'force|l5',
    'S7D_force|l6': 'force|l6',
    'S7D_T1|bl': 'T1|bl',
    'S7D_T1|l1': 'T1|l1',
    'S7D_T1|l2': 'T1|l2',
    'S7D_T1|l3': 'T1|l3',
    'S7D_T1|l4': 'T1|l4',
    'S7D_T1|l5': 'T1|l5',
    'S7D_T1|l6': 'T1|l6',
    'S7D_T2|bl': 'T2|bl',
    'S7D_T2|l1': 'T2|l1',
    'S7D_T2|l2': 'T2|l2',
    'S7D_T2|l3': 'T2|l3',
    'S7D_T2|l4': 'T2|l4',
    'S7D_T2|l5': 'T2|l5',
    'S7D_T2|l6': 'T2|l6',
}


def read(fig):
    return expand(scatter_row(fig, 220, [
        ("freq", V, G, None),
        ("force", V, G, None),
        ("T1", V, G, None),
        ("T2", V, G, None),
    ]), LINKS)
