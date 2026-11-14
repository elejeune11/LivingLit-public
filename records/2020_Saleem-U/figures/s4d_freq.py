"""Figure S4D, Frequency [bpm] (digoxin): mean lines (raster, mmc1.pdf p7).

Tick labels are inside the image; tick marks located by pixel left of the y-axis, assigned top to bottom: 150, 100, 50, 0.

Mean lines are red; the grey dots overlap, so they are not counted (countable: false).
Mean lines left to right: bl, c01, c03, c1; x = concentration in µM (BL = 0).
"""
from _util import panel

TICKS = [150, 100, 50, 0]
LABELS = ['bl', 'c01', 'c03', 'c1']
XS = [0, 0.1, 0.3, 1]
KEEP = None


def read(fig):
    return panel(fig, TICKS, ch=0, labels=LABELS, xs=XS, keep=KEEP)
