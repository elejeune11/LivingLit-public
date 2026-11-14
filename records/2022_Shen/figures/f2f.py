"""Fig. 2F (main.pdf p. 3): TTP at 1-3 Hz (TTP [s] vs frequency (Hz)). Mean markers per frequency (error bars not read).

Vector panel. Tick labels are glyph outlines with no text layer, so the y axis is
calibrated from its 5 tick-mark lines (found in _util), paired bottom to top with the
label values read from a render of the label glyphs: 0, 0.1, 0.2, 0.3, 0.4.
Each marker takes x from the x tick it sits on; the 9 x ticks are labelled
1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3 (Hz). The legend's markers lie inside the
crop and are excluded by the rectangle(s) in LEGEND.
"""
from _util import read_curve

Y_LABELS = [0, 0.1, 0.2, 0.3, 0.4]
X_LABELS = [1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3]
GROUPS = [("HC-RP", (0.017, 0.215, 0.985)), ("LC-RP", (0.986, 0.046, 0.05))]
LEGEND = [(374, 194, 406.7, 210)]


def read(fig):
    return read_curve(fig, Y_LABELS, X_LABELS, GROUPS, LEGEND)
