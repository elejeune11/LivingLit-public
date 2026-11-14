"""Fig. 2E: junctional Cx43 mean intensity.

Vector plots drawn by Prism (p. 3 of sciadv.abh3995.pdf): junctional Cx43 mean intensity, WT1 vs PKP2tv+/− (left) and WT2 vs PKP2tv−/− (right), points with mean ± error bar. Each region below is one plot, from just
left of its tick labels to just short of the next plot's labels; groups are the error bars left to right.
"""
from _util import read_panel

PANELS = [
    ((416.8, 166.7, 492.0, 254.6), ['WT1', 'PKP2tv+/−'], {}),
    ((480.0, 166.4, 579.0, 252.7), ['WT2', 'PKP2tv−/−'], {}),
]


def read(fig):
    groups = {}
    for region, labels, kw in PANELS:
        groups.update(read_panel(fig, region, labels, **kw))
    return {"groups": groups}
