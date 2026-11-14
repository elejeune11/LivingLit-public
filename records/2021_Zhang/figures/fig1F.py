"""Fig. 1F: junctional PKP2 mean intensity.

Vector plots drawn by Prism (p. 2 of sciadv.abh3995.pdf): junctional PKP2 mean intensity, WT1 vs PKP2tv+/− (left) and WT2 vs PKP2tv−/− (right), points with mean ± error bar. Each region below is one plot, from just
left of its tick labels to just short of the next plot's labels; groups are the error bars left to right.
"""
from _util import read_panel

PANELS = [
    ((421.3, 491.4, 497.4, 579.1), ['WT1', 'PKP2tv+/−'], {}),
    ((485.4, 491.4, 584.4, 579.2), ['WT2', 'PKP2tv−/−'], {}),
]


def read(fig):
    groups = {}
    for region, labels, kw in PANELS:
        groups.update(read_panel(fig, region, labels, **kw))
    return {"groups": groups}
