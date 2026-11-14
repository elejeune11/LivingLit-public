"""Figure 4B, Relative CaT [%] vs pacing frequency (raster, main.pdf p7).

Tick labels are inside the image; tick marks located by pixel left of the y-axis, assigned top to bottom: 400, 300, 200, 100, 0.
Mean lines are red (CaT parameters; pale red dots excluded by saturation); dots overlap, so they are not counted (countable: false).
Mean lines left to right: 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5 Hz (x = frequency in Hz).
"""
from _util import panel


def read(fig):
    return panel(fig, [400, 300, 200, 100, 0], ch=0, labels=['f075', 'f10', 'f125', 'f15', 'f175', 'f20', 'f25'], xs=[0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5], sat=100, keep=['f075', 'f10', 'f125', 'f15', 'f175', 'f20'])
