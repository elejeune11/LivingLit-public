"""Figure S5, Relative force [%] vs pacing frequency, hiPSC-EHTs without GCaMP6f (raster, mmc1.pdf p8).

Tick labels are inside the image; tick marks located by pixel left of the y-axis, assigned top to bottom: 200, 150, 100, 50.
Tick 400 above the axis break is not used.
Mean lines are blue; grey dots overlap, so they are not counted (countable: false).
Mean lines left to right: 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5 Hz (x = frequency in Hz).
"""
from _util import panel


def read(fig):
    return panel(fig, [200, 150, 100, 50], ch=2, labels=['f075', 'f10', 'f125', 'f15', 'f175', 'f20', 'f25'], xs=[0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5])
