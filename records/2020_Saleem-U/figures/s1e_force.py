"""Figure S1E, Force [mN] at 0.6 and 1.8 mM Ca2+ (raster, mmc1.pdf p4).

Tick labels are inside the image; tick marks located by pixel left of the y-axis, assigned top to bottom: 0.3, 0.2, 0.1, 0.0.
Mean line ink: saturated blue (pale dots excluded). Lines left to right: ca06, ca18.
Dots overlap each other or the mean line, so they are not counted (countable: false).
"""
from _util import panel


def read(fig):
    return panel(fig, [0.3, 0.2, 0.1, 0.0], ch=2, labels=['ca06', 'ca18'], sat=100)
