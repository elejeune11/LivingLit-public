"""Fig. S7K (paracetamol): frequency, force, T1 and T2 scatter plots with red mean lines (raster, 220 dpi).

One y-axis per panel, left to right; tick values as printed on the labels, top to bottom.
Groups left to right in the order of the x labels. Markers overlap, so means only.
Each reading is labelled for every evidence item that rests on it (LINKS)."""
from _util import expand, scatter_row

G = ['bl', 'c1e5', 'c3e5', 'c1e4', 'c3e4', 'c1e3']
V = [250, 200, 150, 100, 50, 0]
LINKS = {
    'S7K_freq|bl': 'freq|bl',
    'S7K_freq|c1e5': 'freq|c1e5',
    'S7K_freq|c3e5': 'freq|c3e5',
    'S7K_freq|c1e4': 'freq|c1e4',
    'S7K_freq|c3e4': 'freq|c3e4',
    'S7K_force|bl': 'force|bl',
    'S7K_force|c1e5': 'force|c1e5',
    'S7K_force|c3e5': 'force|c3e5',
    'S7K_force|c1e4': 'force|c1e4',
    'S7K_force|c3e4': 'force|c3e4',
    'S7K_force|c1e3': 'force|c1e3',
    'S7K_T1|bl': 'T1|bl',
    'S7K_T1|c1e5': 'T1|c1e5',
    'S7K_T1|c3e5': 'T1|c3e5',
    'S7K_T1|c1e4': 'T1|c1e4',
    'S7K_T1|c3e4': 'T1|c3e4',
    'S7K_T2|bl': 'T2|bl',
    'S7K_T2|c1e5': 'T2|c1e5',
    'S7K_T2|c3e5': 'T2|c3e5',
    'S7K_T2|c1e4': 'T2|c1e4',
    'S7K_T2|c3e4': 'T2|c3e4',
    'S7_safe|bl': 'T2|bl',
    'S7_safe|c1e5': 'T2|c1e5',
    'S7_safe|c3e5': 'T2|c3e5',
    'S7_safe|c1e4': 'T2|c1e4',
    'S7_safe|c3e4': 'T2|c3e4',
}


def read(fig):
    return expand(scatter_row(fig, 220, [
        ("freq", V, G[:5], None),  # only five concentrations are plotted in this panel
        ("force", V, G, None),
        ("T1", V, G[:5], None),  # only five concentrations are plotted in this panel
        ("T2", V, G[:5], None),  # only five concentrations are plotted in this panel
    ], thr=225), LINKS)
