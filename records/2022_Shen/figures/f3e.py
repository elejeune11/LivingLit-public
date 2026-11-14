"""Fig. 3E (main.pdf p. 4): RT50 change (%). Bars with points, mean ± SEM.

Vector panel. Tick labels are glyph outlines with no text layer, so the y axis is
calibrated from its 5 tick-mark lines (found in _util), paired bottom to top with the
label values read from a render of the label glyphs: -10, -5, 0, 5, 10.
Groups are told apart by colour, left to right as labelled on the x axis.
"""
from _util import read_bars

Y_LABELS = [-10, -5, 0, 5, 10]
GROUPS = [("HC-RP", (0.057, 0.215, 0.986)), ("LC-RP", (0.987, 0.142, 0.046))]
HIDDEN = []


def read(fig):
    return read_bars(fig, Y_LABELS, GROUPS, HIDDEN)
