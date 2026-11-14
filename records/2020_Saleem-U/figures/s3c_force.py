"""Figure S3C, Relative force [%] (Bay K-8644): mean lines (raster, mmc1.pdf p6).

Tick labels are inside the image; tick marks located by pixel left of the y-axis, assigned top to bottom: 250, 200, 150, 100, 50, 0.
ticks 500 and 1 above the axis break are not used.
Mean lines are blue; the grey dots overlap, so they are not counted (countable: false).
Mean lines left to right: bl, c30, c100, c300; x = concentration in nM (BL = 0).
"""
from _util import panel

TICKS = [250, 200, 150, 100, 50, 0]
LABELS = ['bl', 'c30', 'c100', 'c300']
XS = [0, 30, 100, 300]
KEEP = None


def read(fig):
    return panel(fig, TICKS, ch=2, labels=LABELS, xs=XS, keep=KEEP)
