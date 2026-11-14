"""Fig. 3C (main.pdf p. 4): Systolic force increase (%). Bars with points, mean ± SEM.

Vector panel. Tick labels are glyph outlines with no text layer, so the y axis is
calibrated from its 6 tick-mark lines (found in _util), paired bottom to top with the
label values read from a render of the label glyphs: 0, 20, 40, 60, 80, 100.
Groups are told apart by colour, left to right as labelled on the x axis.
"""
from _util import read_bars

Y_LABELS = [0, 20, 40, 60, 80, 100]
GROUPS = [("HC-RP", (0.018, 0.214, 0.983)), ("LC-RP", (0.974, 0.047, 0.06))]
HIDDEN = []


def read(fig):
    return read_bars(fig, Y_LABELS, GROUPS, HIDDEN)
