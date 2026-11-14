"""Fig. 3D: APD30, APD50 and APD80.

Vector plots drawn by Prism (p. 4 of sciadv.abh3995.pdf): action potential duration at 30, 50 and 80% repolarization, WT2 vs PKP2tv−/−; legend markers excluded. Each region below is one plot, from just
left of its tick labels to just short of the next plot's labels; groups are the error bars left to right.
"""
from _util import read_panel

PANELS = [
    ((300, 215, 480, 342), ['WT2 APD30', 'PKP2tv−/− APD30', 'WT2 APD50', 'PKP2tv−/− APD50', 'WT2 APD80', 'PKP2tv−/− APD80'], {'exclude': [(415, 300, 430, 330)]}),
]


def read(fig):
    groups = {}
    for region, labels, kw in PANELS:
        groups.update(read_panel(fig, region, labels, **kw))
    return {"groups": groups}
