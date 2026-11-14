"""Fig. 5I (journal_version.pdf p. 11): FAO flux (pmol/h/mg protein) in hPSC-CMs 4 weeks after PPARd modulation,
five bars (Control, LCFA, GW0742, LCFA + GW0742, GSK0660; mean with an SD whisker and caps) with one ring marker per
biological replicate (n = 4). Raster (the page figure is one image, about 300 dpi). Read with _util.read_bars (the
method of figures/F5C.py), as Fig. 5H; its tick marks reach only 2 px past the axis line at 300 dpi, so
tick_min is 2.
"""
from _util import read_bars

TICK_VALUES = [3, 2, 1, 0]   # printed tick labels, top to bottom
LABELS = {f"F5I_fao/{b}": b for b in ["control", "lcfa", "gw", "lcfa_gw", "gsk"]}
for b in ["lcfa", "gw", "lcfa_gw"]:
    LABELS[f"F5I_fao_{b}/{b}"] = b
    LABELS[f"F5I_fao_{b}/control"] = "control"


def read(fig):
    return read_bars(fig, TICK_VALUES, LABELS, tick_min=2)
