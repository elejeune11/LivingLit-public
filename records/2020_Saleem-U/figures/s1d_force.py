"""Figure S1D, Force [mN] at MOI 7x10^4 and 7x10^5 (raster, mmc1.pdf p4).

Tick labels are inside the image; tick marks located by pixel left of the y-axis, assigned top to bottom: 0.3, 0.2, 0.1, 0.0.
Mean line ink: saturated blue (pale dots excluded). Lines left to right: moi_low, moi_high.
Dots overlap each other or the mean line, so they are not counted (countable: false).
"""
from _util import panel


def read(fig):
    return panel(fig, [0.3, 0.2, 0.1, 0.0], ch=2, labels=['moi_low', 'moi_high'], sat=100)
