"""Fig. 5D: RMS systolic stress, single CMs.

Vector plots drawn by Prism (p. 5 of sciadv.abh3995.pdf): RMS systolic stress, single CMs, WT1 vs PKP2tv+/− (left) and WT2 vs PKP2tv−/− (right), points with mean ± error bar. Each region below is one plot, from just
left of its tick labels to just short of the next plot's labels; groups are the error bars left to right.
"""
from _util import read_panel

PANELS = [
    ((124.0, 432.0, 213.0, 523.3), ['WT1', 'PKP2tv+/−'], {}),
    ((201.0, 432.0, 300.0, 523.3), ['WT2', 'PKP2tv−/−'], {}),
]


def read(fig):
    groups = {}
    for region, labels, kw in PANELS:
        groups.update(read_panel(fig, region, labels, **kw))
    return {"groups": groups}
