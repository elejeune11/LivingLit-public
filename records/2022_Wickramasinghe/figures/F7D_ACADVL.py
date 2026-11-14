"""Fig. 7D second row, left (journal_version.pdf p. 14): ACADVL expression (reads, bulk RNA-seq) in hPSC-CMs, 14 bars
(2D: Control, LCFA, GW0742, LCFA + GW0742, GSK0660; EHT and Lact: Control, LCFA, GW0742, LCFA + GW0742; EB; mean with an
SD whisker and caps) with one ring marker per replicate (legend n = 3; the 2D GW0742 bars and some others show four).
Raster (the page is one image, about 300 dpi). Read with _util.read_f7d (the method of figures/F5C.py, sized for these
narrow bars).
"""
from _util import read_f7d

TICK_VALUES = [20000, 15000, 10000, 5000, 0]   # printed tick labels, top to bottom


def read(fig):
    return read_f7d(fig, TICK_VALUES, "F7D_ACADVL")
