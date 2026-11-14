"""Fig. 4D: peak systolic stress.

Vector plots drawn by Prism (p. 5 of sciadv.abh3995.pdf): peak systolic stress, WT1 vs PKP2tv+/− (left) and WT2 vs PKP2tv−/− (right), points with mean ± error bar. Each region below is one plot, from just
left of its tick labels to just short of the next plot's labels; groups are the error bars left to right.
"""
from _util import read_panel

PANELS = [
    ((306.3, 161.6, 405.3, 262.4), ['WT1', 'PKP2tv+/−'], {}),
    ((394.8, 161.6, 493.8, 262.4), ['WT2', 'PKP2tv−/−'], {}),
]


def read(fig):
    groups = {}
    for region, labels, kw in PANELS:
        groups.update(read_panel(fig, region, labels, **kw))
    return {"groups": groups}
