"""Fig. 3C (SEA-0400, beating frequency): scatter plot with red mean lines (raster, 300 dpi).

Tick values as printed on the labels, top to bottom; groups left to right in the order of the
x labels. Points are kept only when every marker of a group stands alone and their number equals
the printed n (None); otherwise the mean only. Each reading is labelled for every evidence item
that rests on it (LINKS)."""
from _util import expand, scatter_row

G = ['bl', 'c3e8', 'c1e7', 'c3e7', 'c1e6', 'c3e6', 'c1e5']
V = [150, 100, 50, 0]
LINKS = {
    'F3C_freq|bl': 'freq|bl',
    'F3C_freq|c3e8': 'freq|c3e8',
    'F3C_freq|c1e7': 'freq|c1e7',
    'F3C_freq|c3e7': 'freq|c3e7',
    'F3C_freq|c1e6': 'freq|c1e6',
    'F3C_freq|c3e6': 'freq|c3e6',
    'F3C_freq|c1e5': 'freq|c1e5',
}


def read(fig):
    return expand(scatter_row(fig, 300, [("freq", V, G, None)]), LINKS)
