"""Figure S1E, CaT [Fluorescence] at 0.6 and 1.8 mM Ca2+ (raster, mmc1.pdf p4).

Tick labels are inside the image; tick marks located by pixel left of the y-axis, assigned top to bottom: 40000, 20000, 0.
Mean line ink: saturated red (pale dots excluded). Lines left to right: ca06, ca18.
Dots overlap each other or the mean line, so they are not counted (countable: false).
"""
from _util import panel


def read(fig):
    return panel(fig, [40000, 20000, 0], ch=0, labels=['ca06', 'ca18'], sat=100)
