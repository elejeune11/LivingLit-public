"""Fig. 2D: junctional DSP mean intensity.

Vector plots drawn by Prism (p. 3 of sciadv.abh3995.pdf): junctional DSP mean intensity, WT1 vs PKP2tv+/− (left) and WT2 vs PKP2tv−/− (right), points with mean ± error bar. Each region below is one plot, from just
left of its tick labels to just short of the next plot's labels; groups are the error bars left to right.
"""
from _util import read_panel

PANELS = [
    ((242.7, 166.7, 318.1, 254.6), ['WT1', 'PKP2tv+/−'], {}),
    ((306.1, 166.5, 405.1, 252.7), ['WT2', 'PKP2tv−/−'], {}),
]


def read(fig):
    groups = {}
    for region, labels, kw in PANELS:
        groups.update(read_panel(fig, region, labels, **kw))
    return {"groups": groups}
