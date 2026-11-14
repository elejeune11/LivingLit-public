"""Figure S2G, CaT [Fluorescence] for three repeated baseline measurements (raster, mmc1.pdf p5).

Tick labels are inside the image; tick marks located by pixel left of the y-axis, assigned top to bottom: 12000, 8000, 4000, 0.
Mean line ink: saturated red (pale dots excluded). Lines left to right: measurement 1, 2, 3.
Dots partly overlap, so they are not counted (countable: false).
"""
from _util import panel


def read(fig):
    return panel(fig, [12000, 8000, 4000, 0], ch=0, labels=['m1', 'm2', 'm3'], xs=[1, 2, 3], sat=100)
