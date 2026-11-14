"""Figure S1D, CaT [Fluorescence] at MOI 7x10^4 and 7x10^5 (raster, mmc1.pdf p4).

Tick labels are inside the image; tick marks located by pixel left of the y-axis, assigned top to bottom: 40000, 20000, 0.
Mean line ink: saturated red (pale dots excluded). Lines left to right: moi_low, moi_high.
Dots overlap each other or the mean line, so they are not counted (countable: false).
"""
from _util import panel


def read(fig):
    return panel(fig, [40000, 20000, 0], ch=0, labels=['moi_low', 'moi_high'], sat=100)
