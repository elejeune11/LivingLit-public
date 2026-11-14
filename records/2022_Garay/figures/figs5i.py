"""Fig. S5I (Ca2+ transient downstroke velocity, ΔF/F0 s-1), mmc1.pdf page 6.

One dot panel: three cell lines (MYL2, PLZ, 19004) x DMSO, SP and Untreated 60d, read by _util.dot_panel_9 as for
Fig. S5C-G. This panel's error-bar caps are 4.1 pt wide and its mean strokes 8.3 pt, so those widths are passed.
Every point is a whole vector circle (centre = rectangle centre); colours follow the legend under Fig. S5A (yellow
DMSO, purple SP, red Untreated 60d); the axis is calibrated from the printed tick labels and the major tick strokes.
Group ids are the record's day-40 ids (the key prints "(30d)" for DMSO and SP; see the unit note). Each column
serves every pairwise item it is in.
"""
from _util import dot_panel_9

COLOURS = {"D40": (0.94, 0.72, 0.08), "SP40": (0.71, 0.44, 0.68), "D60": (0.9, 0.15, 0.17)}
LINES = ("MYL2", "PLZ", "19004")
SHORT = {"D40": "DMSO", "SP40": "SP", "D60": "60d"}
PAIRS = [("SP40", "D40"), ("D60", "D40"), ("SP40", "D60")]


def read(fig):
    per = dot_panel_9(fig, COLOURS, LINES, ("D40", "SP40", "D60"), cap_max=4.5, mean_width=(7.5, 9.0))
    groups = {}
    for line in LINES:
        for pair in PAIRS:
            for g in pair:
                groups[f"{line} {SHORT[pair[0]]} vs {SHORT[pair[1]]}: {SHORT[g]}"] = per[(line, g)]
    return {"groups": groups}
