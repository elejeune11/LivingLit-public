"""Fig. 6C right (verapamil, force): scatter plot with red mean lines (raster, 300 dpi).

Tick values as printed on the labels, top to bottom; groups left to right in the order of the
x labels. Points are kept only when every marker of a group stands alone and their number equals
the printed n (19); otherwise the mean only. Each reading is labelled for every evidence item
that rests on it (LINKS)."""
from _util import expand, scatter_row

G = ['bl', 'c1e8', 'c3e8', 'c1e7', 'c3e7', 'c1e6']
V = [250, 200, 150, 100, 50, 0]
LINKS = {
    'F6C_VER_force|bl': 'force|bl',
    'F6C_VER_force|c1e8': 'force|c1e8',
    'F6C_VER_force|c3e8': 'force|c3e8',
    'F6C_VER_force|c1e7': 'force|c1e7',
    'F6C_VER_force|c3e7': 'force|c3e7',
    'F6C_VER_force|c1e6': 'force|c1e6',
}


def read(fig):
    return expand(scatter_row(fig, 300, [("force", V, G, 19)]), LINKS)
