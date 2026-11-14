"""Figure S1A, TTP-80% [s], CaT (red) (raster, mmc1.pdf p4).

Tick labels are inside the image; tick marks located by pixel left of the y-axis, assigned top to bottom: 0.4, 0.3, 0.2, 0.1, 0.0.
Mean line ink: saturated red (pale dots excluded). Lines left to right: gcamp5g.
Dots overlap each other or the mean line, so they are not counted (countable: false).
"""
from _util import panel


def read(fig):
    return panel(fig, [0.4, 0.3, 0.2, 0.1, 0.0], ch=0, labels=['gcamp5g'], sat=100)
