"""Fig. S5C right (supplement p. 11): DNM1L expression (reads, RNA-seq) in hPSC-CMs 4 weeks after PPARd modulation,
five bars (Control, LCFA, GW0742, LCFA + GW0742, GSK0660; mean with an SD whisker and caps) with one ring marker per
biological replicate (legend n = 3). Raster (the page is one image, about 307 dpi). Read with _util.read_bars (the
method of figures/F5C.py).
"""
from _util import read_bars

TICK_VALUES = [4000, 3000, 2000, 1000, 0]   # printed tick labels, top to bottom
LABELS = {f"S5C_DNM1L/{b}": b for b in ["control", "lcfa", "gw", "lcfa_gw", "gsk"]}


def read(fig):
    return read_bars(fig, TICK_VALUES, LABELS)
