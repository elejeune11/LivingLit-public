"""Supplementary Fig. 7d: FITC-dextran in the reservoir ("Reservoir"), 5 min to 72 hr (raster).

Bars are mean ± s.d. (whiskers both ways) with n=4 markers per time point: dots, and filled
triangles at 1 hr. The figure is one embedded image; reading is in _util.read_panel (discs by a
15 px disc opening, triangles by a 13 px triangle opening). y axis 0-30 µM, ticks every 10.
"""
from _util import read_panel


def read(fig):
    return {"groups": read_panel(fig, [0, 10, 20, 30],
                                 ["reservoir_m5", "reservoir_h1", "reservoir_h24", "reservoir_h48", "reservoir_h72"],
                                 kernel=15, tri=13, tri_cats=("reservoir_h1",))}
