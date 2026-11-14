"""Fig. 6D left (NS-1643, T2): scatter plot with red mean lines (raster, 300 dpi).

Tick values as printed on the labels, top to bottom; groups left to right in the order of the
x labels. Points are kept only when every marker of a group stands alone and their number equals
the printed n (20); otherwise the mean only. Each reading is labelled for every evidence item
that rests on it (LINKS)."""
from _util import expand, scatter_row

G = ['bl', 'c3e7', 'c1e6', 'c3e6', 'c1e5', 'c3e5', 'c1e4']
V = [250, 200, 150, 100, 50, 0]
LINKS = {
    'F6D_NS_T2|bl': 'T2|bl',
    'F6D_NS_T2|c3e7': 'T2|c3e7',
    'F6D_NS_T2|c1e6': 'T2|c1e6',
    'F6D_NS_T2|c3e6': 'T2|c3e6',
    'F6D_NS_T2|c1e5': 'T2|c1e5',
    'F6D_NS_T2|c3e5': 'T2|c3e5',
    'F6D_NS_T2|c1e4': 'T2|c1e4',
    'F6D_NS_T2_c3e5|c3e5': 'T2|c3e5',
    'F6D_NS_T2_c3e5|bl': 'T2|bl',
    'F6D_NS_T2_c1e4|c1e4': 'T2|c1e4',
    'F6D_NS_T2_c1e4|bl': 'T2|bl',
}


def read(fig):
    return expand(scatter_row(fig, 300, [("T2", V, G, 20)]), LINKS)
