"""Fig. 9C: net displacement of sarcomeric α-actinin-2.

Vector plots drawn by Prism (p. 8 of sciadv.abh3995.pdf): net displacement of sarcomeric α-actinin-2, WT1 vs PKP2tv+/− (left) and WT2 vs PKP2tv−/− (right), points with mean ± error bar. Each region below is one plot, from just
left of its tick labels to just short of the next plot's labels; groups are the error bars left to right.
"""
from _util import read_panel

PANELS = [
    ((81.6, 166.0, 149.3, 253.5), ['WT1', 'PKP2tv+/−'], {}),
    ((137.3, 166.0, 236.3, 253.5), ['WT2', 'PKP2tv−/−'], {}),
]


def read(fig):
    groups = {}
    for region, labels, kw in PANELS:
        groups.update(read_panel(fig, region, labels, **kw))
    return {"groups": groups}
