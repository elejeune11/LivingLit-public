"""Fig. 6C left (Bay K-8644, T2): scatter plot with red mean lines (raster, 300 dpi).

Tick values as printed on the labels, top to bottom; groups left to right in the order of the
x labels. Points are kept only when every marker of a group stands alone and their number equals
the printed n (8); otherwise the mean only. Each reading is labelled for every evidence item
that rests on it (LINKS)."""
from _util import expand, scatter_row

G = ['bl', 'c3e9', 'c1e8', 'c3e8', 'c1e7', 'c3e7']
V = [250, 200, 150, 100, 50, 0]
LINKS = {
    'F6C_BAY_T2|bl': 'T2|bl',
    'F6C_BAY_T2|c3e9': 'T2|c3e9',
    'F6C_BAY_T2|c1e8': 'T2|c1e8',
    'F6C_BAY_T2|c3e8': 'T2|c3e8',
    'F6C_BAY_T2|c1e7': 'T2|c1e7',
    'F6C_BAY_T2|c3e7': 'T2|c3e7',
}


def read(fig):
    return expand(scatter_row(fig, 300, [("T2", V, G, 8)]), LINKS)
