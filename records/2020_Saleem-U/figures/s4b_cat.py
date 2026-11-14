"""Figure S4B, Relative CaT [%] [Fluorescence] (nifedipine): mean lines (raster, mmc1.pdf p7).

Tick labels are inside the image; tick marks located by pixel left of the y-axis, assigned top to bottom: 250, 200, 150, 100, 50, 0.

Mean lines are red; the grey dots overlap, so they are not counted (countable: false).
Mean lines left to right: bl, c3, c10, c30, c100; x = concentration in nM (BL = 0).
"""
from _util import panel

TICKS = [250, 200, 150, 100, 50, 0]
LABELS = ['bl', 'c3', 'c10', 'c30', 'c100']
XS = [0, 3, 10, 30, 100]
KEEP = None


def read(fig):
    return panel(fig, TICKS, ch=0, labels=LABELS, xs=XS, keep=KEEP)
