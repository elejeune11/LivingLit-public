"""Fig. 8E: ramble of junctional N-cadherin.

Vector plots drawn by Prism (p. 7 of sciadv.abh3995.pdf): ramble of junctional N-cadherin, WT1 vs PKP2tv+/− (left) and WT2 vs PKP2tv−/− (right), points with mean ± error bar. Each region below is one plot, from just
left of its tick labels to just short of the next plot's labels; groups are the error bars left to right.
"""
from _util import read_panel

PANELS = [
    ((370.4, 164.4, 444.6, 258.0), ['WT1', 'PKP2tv+/−'], {}),
    ((432.6, 164.4, 531.6, 258.0), ['WT2', 'PKP2tv−/−'], {}),
]


def read(fig):
    groups = {}
    for region, labels, kw in PANELS:
        groups.update(read_panel(fig, region, labels, **kw))
    return {"groups": groups}
