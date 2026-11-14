"""Fig. 10B: number of sarcomeres per cardiac patch.

Vector plots drawn by Prism (p. 8 of sciadv.abh3995.pdf): number of sarcomeres per cardiac patch, WT1 vs PKP2tv+/− (left) and WT2 vs PKP2tv−/− (right), points with mean ± error bar. Each region below is one plot, from just
left of its tick labels to just short of the next plot's labels; groups are the error bars left to right.
"""
from _util import read_panel

PANELS = [
    ((367.4, 343.6, 440.8, 431.8), ['WT1', 'PKP2tv+/−'], {}),
    ((428.8, 343.7, 527.8, 431.9), ['WT2', 'PKP2tv−/−'], {}),
]


def read(fig):
    groups = {}
    for region, labels, kw in PANELS:
        groups.update(read_panel(fig, region, labels, **kw))
    return {"groups": groups}
