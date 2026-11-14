"""Fig. 6B left (ATX-II, T2): scatter plot with red mean lines (raster, 300 dpi).

Tick values as printed on the labels, top to bottom; groups left to right in the order of the
x labels. Points are kept only when every marker of a group stands alone and their number equals
the printed n (20); otherwise the mean only. Each reading is labelled for every evidence item
that rests on it (LINKS)."""
from _util import expand, scatter_row

G = ['bl', 'c1e9', 'c3e9', 'c1e8', 'c3e8', 'c1e7']
V = [1000, 800, 600, 400, 200, 0]
LINKS = {
    'F6B_ATX_T2|bl': 'T2|bl',
    'F6B_ATX_T2|c1e9': 'T2|c1e9',
    'F6B_ATX_T2|c3e9': 'T2|c3e9',
    'F6B_ATX_T2|c1e8': 'T2|c1e8',
    'F6B_ATX_T2|c3e8': 'T2|c3e8',
    'F6B_ATX_T2|c1e7': 'T2|c1e7',
}


def read(fig):
    return expand(scatter_row(fig, 300, [("T2", V, G, 20)]), LINKS)
