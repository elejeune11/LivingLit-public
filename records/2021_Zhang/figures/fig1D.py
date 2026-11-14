"""Fig. 1D: PKP2 RNA expression (2^−ΔΔCT).

Vector plots drawn by Prism (p. 2 of sciadv.abh3995.pdf): PKP2 RNA expression (2^−ΔΔCT), WT1 vs PKP2tv+/− (left) and WT2 vs PKP2tv−/− (right), points with mean ± error bar. Each region below is one plot, from just
left of its tick labels to just short of the next plot's labels; groups are the error bars left to right.
"""
from _util import read_panel

PANELS = [
    ((317.2, 482.1, 365.3, 549.1), ['WT1', 'PKP2tv+/−'], {}),
    ((353.3, 481.7, 433.3, 548.7), ['WT2', 'PKP2tv−/−'], {}),
]


def read(fig):
    groups = {}
    for region, labels, kw in PANELS:
        groups.update(read_panel(fig, region, labels, **kw))
    return {"groups": groups}
