"""Fig. S5D right (supplement p. 11): respiratory spare capacity (OCR, pmol/min) in hPSC-CMs, five bars (Control,
LCFA, GW0742, LCFA + GW0742, GSK0660; mean with an SD whisker and caps) with one ring marker per biological
replicate (n = 4). Raster (the page is one image, about 307 dpi). Read with _util.read_bars (the method of
figures/F5C.py).
"""
from _util import read_bars

TICK_VALUES = [4000, 3000, 2000, 1000, 0]   # printed tick labels, top to bottom
LABELS = {f"S5D_spare/{b}": b for b in ["control", "lcfa", "gw", "lcfa_gw", "gsk"]}
for b in ["lcfa", "lcfa_gw", "gsk"]:
    LABELS[f"S5D_spare_{b}/{b}"] = b
    LABELS[f"S5D_spare_{b}/control"] = "control"


def read(fig):
    return read_bars(fig, TICK_VALUES, LABELS)
