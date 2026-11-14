"""Fig. 2M (main.pdf p. 3): Post-rest potentiation (relative unit). Bars with points, mean ± SEM.

Vector panel. Tick labels are glyph outlines with no text layer, so the y axis is
calibrated from its 5 tick-mark lines (found in _util), paired bottom to top with the
label values read from a render of the label glyphs: 1.0, 1.5, 2.0, 2.5, 3.0.
Groups are told apart by colour, left to right as labelled on the x axis. Points of HC-RP are not drawn in the panel (bar and error bar only).
"""
from _util import read_bars

Y_LABELS = [1.0, 1.5, 2.0, 2.5, 3.0]
GROUPS = [("HC-RP", (0.017, 0.215, 0.985)), ("LC-RP", (0.986, 0.046, 0.05))]
HIDDEN = ['HC-RP']


def read(fig):
    return read_bars(fig, Y_LABELS, GROUPS, HIDDEN)
