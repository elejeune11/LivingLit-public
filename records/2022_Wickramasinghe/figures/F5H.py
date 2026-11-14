"""Fig. 5H (journal_version.pdf p. 11): maximal respiration (OCR, pmol/min/cell number) in hPSC-CMs, five bars
(Control, LCFA, GW0742, LCFA + GW0742, GSK0660; mean with an SD whisker and caps) with one ring marker per
biological replicate (n = 4). Raster (the page figure is one image, about 300 dpi). Read with _util.read_bars (the
method of figures/F5C.py). Fig. 5G (OCR over time) plots means with error bars only and is not read.
"""
from _util import read_bars

TICK_VALUES = [5000, 4000, 3000, 2000, 1000, 0]   # printed tick labels, top to bottom
LABELS = {f"F5H_maxresp/{b}": b for b in ["control", "lcfa", "gw", "lcfa_gw", "gsk"]}
for b in ["lcfa", "lcfa_gw", "gsk"]:
    LABELS[f"F5H_maxresp_{b}/{b}"] = b
    LABELS[f"F5H_maxresp_{b}/control"] = "control"


def read(fig):
    return read_bars(fig, TICK_VALUES, LABELS)
