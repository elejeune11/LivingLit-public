"""Fig. 5E: systolic work, single CMs.

Vector plots drawn by Prism (p. 5 of sciadv.abh3995.pdf): systolic work, single CMs, WT1 vs PKP2tv+/− (left) and WT2 vs PKP2tv−/− (right), points with mean ± error bar. Each region below is one plot, from just
left of its tick labels to just short of the next plot's labels; groups are the error bars left to right.
"""
from _util import read_panel

PANELS = [
    ((307.8, 432.0, 394.9, 523.3), ['WT1', 'PKP2tv+/−'], {}),
    ((382.9, 432.0, 481.9, 523.2), ['WT2', 'PKP2tv−/−'], {}),
]


def read(fig):
    groups = {}
    for region, labels, kw in PANELS:
        groups.update(read_panel(fig, region, labels, **kw))
    return {"groups": groups}
