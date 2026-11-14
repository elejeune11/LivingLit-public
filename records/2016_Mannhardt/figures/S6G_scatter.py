"""Fig. S6G (NS-1643): frequency, force, T1 and T2 scatter plots with red mean lines (raster, 220 dpi).

One y-axis per panel, left to right; tick values as printed on the labels, top to bottom.
Groups left to right in the order of the x labels. Markers overlap, so means only.
Each reading is labelled for every evidence item that rests on it (LINKS)."""
from _util import expand, scatter_row

G = ['bl', 'c3e7', 'c1e6', 'c3e6', 'c1e5', 'c3e5', 'c1e4']
V = [250, 200, 150, 100, 50, 0]
LINKS = {
    'S6G_freq|bl': 'freq|bl',
    'S6G_freq|c3e7': 'freq|c3e7',
    'S6G_freq|c1e6': 'freq|c1e6',
    'S6G_freq|c3e6': 'freq|c3e6',
    'S6G_freq|c1e5': 'freq|c1e5',
    'S6G_freq|c3e5': 'freq|c3e5',
    'S6G_freq|c1e4': 'freq|c1e4',
    'S6G_freq_c3e5|c3e5': 'freq|c3e5',
    'S6G_freq_c3e5|bl': 'freq|bl',
    'S6G_force|bl': 'force|bl',
    'S6G_force|c3e7': 'force|c3e7',
    'S6G_force|c1e6': 'force|c1e6',
    'S6G_force|c3e6': 'force|c3e6',
    'S6G_force|c1e5': 'force|c1e5',
    'S6G_force|c3e5': 'force|c3e5',
    'S6G_force|c1e4': 'force|c1e4',
    'S6G_force_c3e5|c3e5': 'force|c3e5',
    'S6G_force_c3e5|bl': 'force|bl',
    'S6G_force_c1e4|c1e4': 'force|c1e4',
    'S6G_force_c1e4|bl': 'force|bl',
    'S6G_T1|bl': 'T1|bl',
    'S6G_T1|c3e7': 'T1|c3e7',
    'S6G_T1|c1e6': 'T1|c1e6',
    'S6G_T1|c3e6': 'T1|c3e6',
    'S6G_T1|c1e5': 'T1|c1e5',
    'S6G_T1|c3e5': 'T1|c3e5',
    'S6G_T1|c1e4': 'T1|c1e4',
    'S6G_T1_c1e4|c1e4': 'T1|c1e4',
    'S6G_T1_c1e4|bl': 'T1|bl',
    'S6G_T2|bl': 'T2|bl',
    'S6G_T2|c3e7': 'T2|c3e7',
    'S6G_T2|c1e6': 'T2|c1e6',
    'S6G_T2|c3e6': 'T2|c3e6',
    'S6G_T2|c1e5': 'T2|c1e5',
    'S6G_T2|c3e5': 'T2|c3e5',
    'S6G_T2|c1e4': 'T2|c1e4',
    'S6G_T2_c3e5|c3e5': 'T2|c3e5',
    'S6G_T2_c3e5|bl': 'T2|bl',
    'S6G_T2_c1e4|c1e4': 'T2|c1e4',
    'S6G_T2_c1e4|bl': 'T2|bl',
}


def read(fig):
    return expand(scatter_row(fig, 220, [
        ("freq", V, G, None),
        ("force", V, G, None),
        ("T1", V, G, None),
        ("T2", V, G, None),
    ]), LINKS)
