"""Fig. S6B (% cTnT+ TUNEL+ nuclei, PLZ, day 30; DMSO, SP, DNase I control), mmc1.pdf page 7.

One GraphPad dot panel of three columns (DMSO, SP, Dnase I) on a log10 axis (0.0001 to 1000), read by
_util.dot_panel_2 with log=True: every point is a whole vector circle (7.88 pt wide, centre = rectangle centre);
colours follow the column (yellow DMSO, purple SP, dark grey Dnase I); columns are the x-axis tick strokes, checked
against the x-axis labels; the axis is calibrated from the printed tick labels matched to the major tick strokes.
Means are the 14.4 pt horizontal strokes, the upper error-bar end is the upper cap of the cap-stem-cap path (7.18 pt
caps); the ns and **** brackets are not error bars. Each column serves every pairwise item it is part of.
"""
from _util import dot_panel_2

COLOURS = {"DMSO": (0.94, 0.72, 0.08), "SP": (0.71, 0.44, 0.68), "Dnase": (0.17, 0.13, 0.09)}
PAIRS = [("SP", "DMSO"), ("Dnase", "DMSO"), ("Dnase", "SP")]


def read(fig):
    col = dot_panel_2(fig, COLOURS, ("DMSO", "SP", "Dnase"), cap_width=(6.5, 7.8), mean_width=(13.5, 15.0),
                      disc_width=(7.5, 8.2), log=True)
    return {"groups": {f"{a} vs {b}: {g}": col[g] for a, b in PAIRS for g in (a, b)}}
