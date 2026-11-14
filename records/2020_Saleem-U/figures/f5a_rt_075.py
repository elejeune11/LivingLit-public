"""Figure 5A, Relative RT80% [%]: baseline (ivabradine) vs omecamtiv mecarbil at each pacing frequency (raster, main.pdf p8).

Tick labels are inside the image; tick marks located by pixel left of the y-axis, assigned top to bottom: 300, 200, 100, 0.
Baseline mean lines are black (every channel < 90); OM mean lines are blue (saturated ink only; pale dots excluded).
Dots overlap, so they are not counted (countable: false). Lines left to right per ink: 0.75 ... 2.5 Hz (x = frequency in Hz).
Returned: the f075 pair only (this entry's item).
"""
from _util import panel


def read(fig):
    return panel(fig, [300, 200, 100, 0], ch=None, labels=None, min_width=21, keep=['blf075', 'omf075'],
                 inks=[((-1, 90, None), ['blf075', 'blf10', 'blf125', 'blf15', 'blf175', 'blf20', 'blf25'], [0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5]),
                       ((2, 40, 100), ['omf075', 'omf10', 'omf125', 'omf15', 'omf175', 'omf20', 'omf25'], [0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5])])
