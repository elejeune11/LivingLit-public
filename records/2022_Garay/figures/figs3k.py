"""Fig. S3K (% cTnT+MLC-2v+ cells, flow cytometry), mmc1.pdf page 4.

One dot panel: three cell lines (MYL2, PLZ, 19004) x DMSO 30d, SP 30d, 60d, read by _util.dot_panel_9. Every point
is a whole vector circle (four Bezier arcs, 4.7 pt wide; centre = rectangle centre); columns come from the error
bars (cap, stem, cap paths); colours follow the panel's legend (yellow DMSO (30d), purple SP (30d), red 60d); the
axis is calibrated from the printed tick labels and the major tick strokes. The mean is the horizontal stroke
(7.2 pt) on each error bar; the error value is the upper cap. Each column serves every pairwise item it is in.
"""
from _util import dot_panel_9

COLOURS = {"D30": (0.94, 0.72, 0.08), "SP30": (0.71, 0.44, 0.68), "D60": (0.9, 0.15, 0.17)}
LINES = ("MYL2", "PLZ", "19004")
SHORT = {"D30": "DMSO", "SP30": "SP", "D60": "60d"}
PAIRS = [("SP30", "D30"), ("D60", "D30"), ("SP30", "D60")]


def read(fig):
    per = dot_panel_9(fig, COLOURS, LINES, ("D30", "SP30", "D60"), mean_width=(6.5, 8.0), disc_width=(4.5, 4.9))
    groups = {}
    for line in LINES:
        for pair in PAIRS:
            for g in pair:
                groups[f"{line} {SHORT[pair[0]]} vs {SHORT[pair[1]]}: {SHORT[g]}"] = per[(line, g)]
    return {"groups": groups}
