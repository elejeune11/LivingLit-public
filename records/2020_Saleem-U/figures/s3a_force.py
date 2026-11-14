"""Figure S3A, Relative force [%] (isoprenaline): mean lines (raster, mmc1.pdf p6).

Tick labels are inside the image; tick marks located by pixel left of the y-axis, assigned top to bottom: 250, 200, 150, 100, 50, 0.

Mean lines are blue; the grey dots overlap, so they are not counted (countable: false).
Mean lines left to right: bl, c10; x = concentration in nM (BL = 0).
"""
from _util import panel

TICKS = [250, 200, 150, 100, 50, 0]
LABELS = ['bl', 'c10']
XS = [0, 10]
KEEP = None


def read(fig):
    return panel(fig, TICKS, ch=2, labels=LABELS, xs=XS, keep=KEEP)
