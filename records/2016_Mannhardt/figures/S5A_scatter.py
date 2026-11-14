"""Fig. S5A (calcium): frequency, force, T1 and T2 scatter plots with red mean lines (raster, 220 dpi).

One y-axis per panel, left to right; tick values as printed on the labels, top to bottom.
Groups left to right in the order of the x labels. Markers overlap, so means only.
Each reading is labelled for every evidence item that rests on it (LINKS)."""
from _util import expand, scatter_row

G = ['c1e4', 'c2e4', 'c4e4', 'c6e4', 'c1e3', 'c1p4e3', 'c1p8e3', 'c2p4e3', 'c3p3e3', 'c5e3']
V = [250, 200, 150, 100, 50, 0]
LINKS = {
    'S5A_freq|c1e4': 'freq|c1e4',
    'S5A_freq|c2e4': 'freq|c2e4',
    'S5A_freq|c4e4': 'freq|c4e4',
    'S5A_freq|c6e4': 'freq|c6e4',
    'S5A_freq|c1e3': 'freq|c1e3',
    'S5A_freq|c1p4e3': 'freq|c1p4e3',
    'S5A_freq|c1p8e3': 'freq|c1p8e3',
    'S5A_freq|c2p4e3': 'freq|c2p4e3',
    'S5A_freq|c3p3e3': 'freq|c3p3e3',
    'S5A_freq|c5e3': 'freq|c5e3',
    'S5A_force|c1e4': 'force|c1e4',
    'S5A_force|c2e4': 'force|c2e4',
    'S5A_force|c4e4': 'force|c4e4',
    'S5A_force|c6e4': 'force|c6e4',
    'S5A_force|c1e3': 'force|c1e3',
    'S5A_force|c1p4e3': 'force|c1p4e3',
    'S5A_force|c1p8e3': 'force|c1p8e3',
    'S5A_force|c2p4e3': 'force|c2p4e3',
    'S5A_force|c3p3e3': 'force|c3p3e3',
    'S5A_force|c5e3': 'force|c5e3',
    'S5A_T1|c1e4': 'T1|c1e4',
    'S5A_T1|c2e4': 'T1|c2e4',
    'S5A_T1|c4e4': 'T1|c4e4',
    'S5A_T1|c6e4': 'T1|c6e4',
    'S5A_T1|c1e3': 'T1|c1e3',
    'S5A_T1|c1p4e3': 'T1|c1p4e3',
    'S5A_T1|c1p8e3': 'T1|c1p8e3',
    'S5A_T1|c2p4e3': 'T1|c2p4e3',
    'S5A_T1|c3p3e3': 'T1|c3p3e3',
    'S5A_T1|c5e3': 'T1|c5e3',
    'S5A_T2|c1e4': 'T2|c1e4',
    'S5A_T2|c2e4': 'T2|c2e4',
    'S5A_T2|c4e4': 'T2|c4e4',
    'S5A_T2|c6e4': 'T2|c6e4',
    'S5A_T2|c1e3': 'T2|c1e3',
    'S5A_T2|c1p4e3': 'T2|c1p4e3',
    'S5A_T2|c1p8e3': 'T2|c1p8e3',
    'S5A_T2|c2p4e3': 'T2|c2p4e3',
    'S5A_T2|c3p3e3': 'T2|c3p3e3',
    'S5A_T2|c5e3': 'T2|c5e3',
}


def read(fig):
    return expand(scatter_row(fig, 220, [
        ("freq", V, G, None),
        ("force", [500, 400, 300, 200, 100, 0], G, None),
        ("T1", V, G, None),
        ("T2", V, G, None),
    ]), LINKS)
