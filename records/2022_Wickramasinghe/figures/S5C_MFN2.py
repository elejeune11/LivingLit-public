"""Fig. S5C middle (supplement p. 11): MFN2 expression (reads, RNA-seq) in hPSC-CMs 4 weeks after PPARd modulation,
five bars (Control, LCFA, GW0742, LCFA + GW0742, GSK0660; mean with an SD whisker and caps) with one ring marker per
biological replicate (legend n = 3). Raster (the page is one image, about 307 dpi). Read with _util.read_bars (the
method of figures/F5C.py).
"""
from _util import read_bars

TICK_VALUES = [15000, 10000, 5000, 0]   # printed tick labels, top to bottom
LABELS = {f"S5C_MFN2/{b}": b for b in ["control", "lcfa", "gw", "lcfa_gw", "gsk"]}
for b in ["gw", "lcfa_gw"]:
    LABELS[f"S5C_MFN2_{b}/{b}"] = b
    LABELS[f"S5C_MFN2_{b}/control"] = "control"


def read(fig):
    return read_bars(fig, TICK_VALUES, LABELS)
