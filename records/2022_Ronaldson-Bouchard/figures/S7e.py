"""Supplementary Fig. 7e: FITC-dextran in the chamber 1 ("Chamber 1"), 5 min to 72 hr (raster).

Bars are mean ± s.d. (whiskers both ways) with n=4 markers per time point: dots, and filled
triangles at 1 hr. The figure is one embedded image; reading is in _util.read_panel (discs by a
15 px disc opening, triangles by a 13 px triangle opening). y axis 0-15 µM, ticks every 5.
"""
from _util import read_panel


def read(fig):
    return {"groups": read_panel(fig, [0, 5, 10, 15],
                                 ["ch1_m5", "ch1_h1", "ch1_h24", "ch1_h48", "ch1_h72"],
                                 kernel=15, tri=13, tri_cats=("ch1_h1",))}
