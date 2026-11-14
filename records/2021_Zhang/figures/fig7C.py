"""Fig. 7C: N-cadherin mobile fraction (FRAP plateau).

Vector plots drawn by Prism (p. 6 of sciadv.abh3995.pdf): mobile fraction, WT1 vs PKP2tv+/− (top) and WT2 vs PKP2tv−/− (bottom), bars with mean ± SEM, no points. Each region below is one plot, from just
left of its tick labels to just short of the next plot's labels; groups are the error bars left to right.
"""
from _util import read_panel

PANELS = [
    ((416, 341, 520, 434), ['WT1', 'PKP2tv+/−'], {'points': False}),
    ((416, 435, 520, 525), ['WT2', 'PKP2tv−/−'], {'points': False}),
]


def read(fig):
    groups = {}
    for region, labels, kw in PANELS:
        groups.update(read_panel(fig, region, labels, **kw))
    return {"groups": groups}
