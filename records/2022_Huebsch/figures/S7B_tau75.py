"""Supplementary Fig. 7b (Supplementary_Figures.pdf p. 8): normalized Ca2+ tau75 under flecainide, SCVI20 MPS
pre-treated with SM or MM. Raster (see _util.read_s7); two pairs of red squares touch, stacked (one in SM 100nM, one
in SM 1uM), and MM 1uM's blue error bar joins two of its circles."""
import _util as u

LABELS = [2.5, 2.0, 1.5, 1.0, 0.5, 0.0]  # y tick labels, top to bottom
NEAR = {  # render column (300 dpi) near each group's error-bar line, and its marker colour
    "SM 100nM": (256, "red"), "MM 100nM": (405, "blue"), "SM 1uM": (554, "red"), "MM 1uM": (703, "blue"),
}


def read(fig):
    return {"groups": u.read_s7(fig, LABELS, NEAR, blue_error={"MM 1uM"})}
