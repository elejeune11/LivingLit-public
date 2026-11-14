"""fig. S4B: junctional αT-catenin mean intensity.

Raster bar plots (an embedded image, p. 5 of sciadv.abh3995_sm.pdf): WT2 vs PKP2tv−/−, bars with mean ± SEM and points. Tick labels are part of the image, so their
printed values are listed here top to bottom; tick marks are found in the image and calibrate the axis.
"""
from _util import read_raster_bars

PANELS = [
    ((415, 80, 540, 262), ['WT2', 'PKP2tv−/−'], [95.0, 90.0, 85.0, 80.0, 75.0]),
]


def read(fig):
    groups = {}
    for region, labels, ticks in PANELS:
        groups.update(read_raster_bars(fig, region, labels, ticks))
    return {"groups": groups}
