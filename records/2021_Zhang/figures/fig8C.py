"""Fig. 8C: net displacement of junctional N-cadherin.

Vector plots drawn by Prism (p. 7 of sciadv.abh3995.pdf): net displacement of junctional N-cadherin, WT1 vs PKP2tv+/− (left) and WT2 vs PKP2tv−/− (right), points with mean ± error bar. Each region below is one plot, from just
left of its tick labels to just short of the next plot's labels; groups are the error bars left to right.
"""
from _util import read_panel

PANELS = [
    ((83.0, 164.6, 151.7, 258.0), ['WT1', 'PKP2tv+/−'], {}),
    ((139.7, 164.6, 238.7, 258.0), ['WT2', 'PKP2tv−/−'], {}),
]


def read(fig):
    groups = {}
    for region, labels, kw in PANELS:
        groups.update(read_panel(fig, region, labels, **kw))
    return {"groups": groups}
