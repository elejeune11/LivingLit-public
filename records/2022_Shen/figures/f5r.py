"""Fig. 5R (main.pdf p. 6): RT50 change (%) with ISO. Bars with points, mean ± SEM.

Vector panel. Tick labels are glyph outlines with no text layer, so the y axis is
calibrated from its 4 tick-mark lines (found in _util), paired bottom to top with the
label values read from a render of the label glyphs: -20, 0, 20, 40.
Groups are told apart by colour, left to right as labelled on the x axis.
"""
from _util import read_bars

Y_LABELS = [-20, 0, 20, 40]
GROUPS = [("HC-NP", (0.336, 0.623, 0.977)), ("HC-RP", (0.017, 0.215, 0.985)), ("LC-NP", (0.982, 0.502, 0.504)), ("LC-RP", (0.986, 0.046, 0.05))]
HIDDEN = []


def read(fig):
    return read_bars(fig, Y_LABELS, GROUPS, HIDDEN)
