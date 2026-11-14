"""Fig. 6D: RMS systolic stress, cardiac patches.

Vector plots drawn by Prism (p. 6 of sciadv.abh3995.pdf): RMS systolic stress, cardiac patches, WT1 vs PKP2tv+/− (left) and WT2 vs PKP2tv−/− (right), points with mean ± error bar. Each region below is one plot, from just
left of its tick labels to just short of the next plot's labels; groups are the error bars left to right.
"""
from _util import read_panel

PANELS = [
    ((123.2, 151.0, 212.3, 242.4), ['WT1', 'PKP2tv+/−'], {}),
    ((200.3, 151.0, 299.3, 242.4), ['WT2', 'PKP2tv−/−'], {}),
]


def read(fig):
    groups = {}
    for region, labels, kw in PANELS:
        groups.update(read_panel(fig, region, labels, **kw))
    return {"groups": groups}
