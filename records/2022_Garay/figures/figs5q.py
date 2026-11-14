"""Fig. S5Q (HCN4 relative to TBP·POLR2A; D vs SP), mmc1.pdf page 6.

One GraphPad dot panel of two columns, D (DMSO) and SP, read by _util.dot_panel_2: every point is a whole vector
circle (centre = rectangle centre); colours follow the column (yellow D, purple SP, as in the S5N key); columns are
the x-axis tick strokes, checked against the x-axis labels; the axis is calibrated from the printed tick labels
matched to the major tick strokes. Means are the 15.3 pt horizontal strokes, the upper error-bar end is the upper
cap of the cap-stem-cap path (7.66 pt caps); the significance bracket is not an error bar.
"""
from _util import dot_panel_2

COLOURS = {"D": (0.94, 0.72, 0.08), "SP": (0.71, 0.44, 0.68)}


def read(fig):
    return {"groups": dot_panel_2(fig, COLOURS, ("D", "SP"), cap_width=(7.0, 8.5), mean_width=(14.5, 16.0),
                                  disc_width=(4.4, 5.0))}
