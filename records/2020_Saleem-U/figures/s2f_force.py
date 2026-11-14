"""Figure S2F, Force [mN] for three repeated baseline measurements (raster, mmc1.pdf p5).

Tick labels are inside the image; tick marks located by pixel left of the y-axis, assigned top to bottom: 0.3, 0.2, 0.1, 0.0.
Mean line ink: saturated blue (pale dots excluded). Lines left to right: measurement 1, 2, 3.
Dots partly overlap, so they are not counted (countable: false).
"""
from _util import panel


def read(fig):
    return panel(fig, [0.3, 0.2, 0.1, 0.0], ch=2, labels=['m1', 'm2', 'm3'], xs=[1, 2, 3], sat=100)
