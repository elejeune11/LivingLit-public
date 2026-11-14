"""Fig. S7B (procainamide): frequency, force, T1 and T2 scatter plots with red mean lines (raster, 220 dpi).

One y-axis per panel, left to right; tick values as printed on the labels, top to bottom.
Groups left to right in the order of the x labels. Markers overlap, so means only.
Each reading is labelled for every evidence item that rests on it (LINKS)."""
from _util import expand, scatter_row

G = ['bl', 'c1e5', 'c3e5', 'c1e4', 'c3e4', 'c1e3', 'c3e3']
V = [250, 200, 150, 100, 50, 0]
LINKS = {
    'S7B_freq|bl': 'freq|bl',
    'S7B_freq|c1e5': 'freq|c1e5',
    'S7B_freq|c3e5': 'freq|c3e5',
    'S7B_freq|c1e4': 'freq|c1e4',
    'S7B_freq|c3e4': 'freq|c3e4',
    'S7B_freq|c1e3': 'freq|c1e3',
    'S7B_freq|c3e3': 'freq|c3e3',
    'S7B_force|bl': 'force|bl',
    'S7B_force|c1e5': 'force|c1e5',
    'S7B_force|c3e5': 'force|c3e5',
    'S7B_force|c1e4': 'force|c1e4',
    'S7B_force|c3e4': 'force|c3e4',
    'S7B_force|c1e3': 'force|c1e3',
    'S7B_force|c3e3': 'force|c3e3',
    'S7B_T1|bl': 'T1|bl',
    'S7B_T1|c1e5': 'T1|c1e5',
    'S7B_T1|c3e5': 'T1|c3e5',
    'S7B_T1|c1e4': 'T1|c1e4',
    'S7B_T1|c3e4': 'T1|c3e4',
    'S7B_T1|c1e3': 'T1|c1e3',
    'S7B_T1|c3e3': 'T1|c3e3',
    'S7B_T2|bl': 'T2|bl',
    'S7B_T2|c1e5': 'T2|c1e5',
    'S7B_T2|c3e5': 'T2|c3e5',
    'S7B_T2|c1e4': 'T2|c1e4',
    'S7B_T2|c3e4': 'T2|c3e4',
    'S7B_T2|c1e3': 'T2|c1e3',
    'S7B_T2|c3e3': 'T2|c3e3',
}


def read(fig):
    return expand(scatter_row(fig, 220, [
        ("freq", V, G, None),
        ("force", V, G, None),
        ("T1", V, G, None),
        ("T2", V, G, None),
    ]), LINKS)
