"""Fig. 10E: order parameter plateau.

Vector plots drawn by Prism (p. 8 of sciadv.abh3995.pdf): order parameter plateau, WT1 vs PKP2tv+/− (left) and WT2 vs PKP2tv−/− (right), points with mean ± error bar. Each region below is one plot, from just
left of its tick labels to just short of the next plot's labels; groups are the error bars left to right.
"""
from _util import read_panel

PANELS = [
    ((383.8, 446.3, 451.4, 532.1), ['WT1', 'PKP2tv+/−'], {}),
    ((439.4, 446.3, 538.4, 532.1), ['WT2', 'PKP2tv−/−'], {}),
]


def read(fig):
    groups = {}
    for region, labels, kw in PANELS:
        groups.update(read_panel(fig, region, labels, **kw))
    return {"groups": groups}
