"""Supplementary Fig. 7c (Supplementary_Figures.pdf p. 8): normalized Ca2+ amplitude under flecainide, SCVI20 MPS
pre-treated with SM or MM (the legend prints the high dose as 1mM, the main text and the panel's x label as 1uM).
Raster (see _util.read_s7); every marker stands alone. The p=0.03 bracket is left out of the bars by bar_rows. Only
the 1uM groups are read: the item compares those two."""
import _util as u

LABELS = [6, 4, 2, 0]  # y tick labels, top to bottom
NEAR = {"SM 1uM": (651, "red"), "MM 1uM": (800, "blue")}  # render column (300 dpi) near each group's error-bar line


def read(fig):
    return {"groups": u.read_s7(fig, LABELS, NEAR)}
