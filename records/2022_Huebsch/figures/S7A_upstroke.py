"""Supplementary Fig. 7a (Supplementary_Figures.pdf p. 8): normalized Ca2+ upstroke under flecainide, SCVI20 MPS
pre-treated with SM or MM. Raster (see _util.read_s7): open bars with mean + SD, red squares (SM) and blue circles
(MM); MM 1uM's error bar is blue and joins three of its circles, which are found by erosion."""
import _util as u

LABELS = [5, 4, 3, 2, 1, 0]  # y tick labels, top to bottom
NEAR = {  # render column (300 dpi) near each group's error-bar line, and its marker colour
    "SM 100nM": (318, "red"), "MM 100nM": (468, "blue"), "SM 1uM": (617, "red"), "MM 1uM": (766, "blue"),
}


def read(fig):
    return {"groups": u.read_s7(fig, LABELS, NEAR, blue_error={"MM 1uM"})}
