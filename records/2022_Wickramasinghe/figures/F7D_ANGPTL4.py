"""Fig. 7D third row, left (journal_version.pdf p. 14): ANGPTL4 expression (reads, bulk RNA-seq) in hPSC-CMs, 14 bars
(2D: Control, LCFA, GW0742, LCFA + GW0742, GSK0660; EHT and Lact: Control, LCFA, GW0742, LCFA + GW0742; EB; mean with an
SD whisker and caps) with one ring marker per replicate (legend n = 3; the 2D GW0742 bars and some others show four).
Raster (the page is one image, about 300 dpi). Read with _util.read_f7d (the method of figures/F5C.py, sized for these
narrow bars).
"""
from _util import read_f7d

TICK_VALUES = [4000, 3000, 2000, 1000, 0]   # printed tick labels, top to bottom


def read(fig):
    return read_f7d(fig, TICK_VALUES, "F7D_ANGPTL4")
