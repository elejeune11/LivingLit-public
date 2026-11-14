"""fig. S1A: t50_contract of CMTs paced at 1 Hz.

Raster bar plots (an embedded image, p. 2 of sciadv.abh3995_sm.pdf): t50_contract, WT1 vs PKP2tv+/− (left) and WT2 vs PKP2tv−/− (right), bars with mean ± SEM and points. Tick labels are part of the image, so their
printed values are listed here top to bottom; tick marks are found in the image and calibrate the axis.
"""
from _util import read_raster_bars

PANELS = [
    ((101, 85, 200, 194), ['WT1', 'PKP2tv+/−'], [0.5, 0.4, 0.3, 0.2, 0.1, 0.0]),
    ((203.5, 85, 300, 194), ['WT2', 'PKP2tv−/−'], [0.5, 0.4, 0.3, 0.2, 0.1, 0.0]),
]


def read(fig):
    groups = {}
    for region, labels, ticks in PANELS:
        groups.update(read_raster_bars(fig, region, labels, ticks))
    return {"groups": groups}
