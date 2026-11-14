"""Fig. S7C (cisapride): frequency, force, T1 and T2 scatter plots with red mean lines (raster, 220 dpi).

One y-axis per panel, left to right; tick values as printed on the labels, top to bottom.
Groups left to right in the order of the x labels. Markers overlap, so means only.
Each reading is labelled for every evidence item that rests on it (LINKS)."""
from _util import expand, scatter_row

G = ['bl', 'c3e10', 'c1e9', 'c3e9', 'c1e8', 'c3e8', 'c1e7']
V = [250, 200, 150, 100, 50, 0]
LINKS = {
    'S7C_freq|bl': 'freq|bl',
    'S7C_freq|c3e10': 'freq|c3e10',
    'S7C_freq|c1e9': 'freq|c1e9',
    'S7C_freq|c3e9': 'freq|c3e9',
    'S7C_freq|c1e8': 'freq|c1e8',
    'S7C_freq|c3e8': 'freq|c3e8',
    'S7C_freq|c1e7': 'freq|c1e7',
    'S7C_force|bl': 'force|bl',
    'S7C_force|c3e10': 'force|c3e10',
    'S7C_force|c1e9': 'force|c1e9',
    'S7C_force|c3e9': 'force|c3e9',
    'S7C_force|c1e8': 'force|c1e8',
    'S7C_force|c3e8': 'force|c3e8',
    'S7C_force|c1e7': 'force|c1e7',
    'S7C_T1|bl': 'T1|bl',
    'S7C_T1|c3e10': 'T1|c3e10',
    'S7C_T1|c1e9': 'T1|c1e9',
    'S7C_T1|c3e9': 'T1|c3e9',
    'S7C_T1|c1e8': 'T1|c1e8',
    'S7C_T1|c3e8': 'T1|c3e8',
    'S7C_T1|c1e7': 'T1|c1e7',
    'S7C_T2|bl': 'T2|bl',
    'S7C_T2|c3e10': 'T2|c3e10',
    'S7C_T2|c1e9': 'T2|c1e9',
    'S7C_T2|c3e9': 'T2|c3e9',
    'S7C_T2|c1e8': 'T2|c1e8',
    'S7C_T2|c3e8': 'T2|c3e8',
    'S7C_T2|c1e7': 'T2|c1e7',
}


def read(fig):
    return expand(scatter_row(fig, 220, [
        ("freq", V, G, None),
        ("force", V, G, None),
        ("T1", V, G, None),
        ("T2", V, G, None),
    ]), LINKS)
