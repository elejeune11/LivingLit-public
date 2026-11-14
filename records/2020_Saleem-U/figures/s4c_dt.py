"""Figure S4C, Relative DT80% [%] (Bay K-8644): mean lines (raster, mmc1.pdf p7).

Tick labels are inside the image; tick marks located by pixel left of the y-axis, assigned top to bottom: (not used), 150, 100, 50, 0.
tick 250 above the axis break is not used; the 100 and 300 nM mean lines lie above the break and are not read.
Mean lines are red; the grey dots overlap, so they are not counted (countable: false).
Mean lines left to right: bl, c30, None, None; x = concentration in nM (BL = 0).
"""
from _util import panel

TICKS = [None, 150, 100, 50, 0]
LABELS = ['bl', 'c30', None, None]
XS = [0, 30, 100, 300]
KEEP = None


def read(fig):
    return panel(fig, TICKS, ch=0, labels=LABELS, xs=XS, keep=KEEP)
