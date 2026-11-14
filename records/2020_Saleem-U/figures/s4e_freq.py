"""Figure S4E, Frequency [bpm] (EMD-57033): mean lines (raster, mmc1.pdf p7).

Tick labels are inside the image; tick marks located by pixel left of the y-axis, assigned top to bottom: 150, 100, 50, 0.

Mean lines are red; the grey dots overlap, so they are not counted (countable: false).
Mean lines left to right: bl, c1, c3, c10; x = concentration in µM (BL = 0).
"""
from _util import panel

TICKS = [150, 100, 50, 0]
LABELS = ['bl', 'c1', 'c3', 'c10']
XS = [0, 1, 3, 10]
KEEP = None


def read(fig):
    return panel(fig, TICKS, ch=0, labels=LABELS, xs=XS, keep=KEEP)
