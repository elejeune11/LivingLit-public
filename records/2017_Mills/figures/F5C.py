"""Fig. 5C: activated β-catenin relative intensity, bars ± SEM (raster), -INS/+INS pairs by glucose and palmitate, then CTRL. Ticks 0.0-2.5 by 0.5."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0.0, 0.5, 1.0, 1.5, 2.0, 2.5], ['noins_g0_p0', 'ins_g0_p0', 'noins_g1_p0', 'ins_g1_p0', 'noins_g55_p0', 'ins_g55_p0', 'noins_g25_p0', 'ins_g25_p0', 'noins_g0_p100', 'ins_g0_p100', 'noins_g1_p100', 'ins_g1_p100', 'noins_g55_p100', 'ins_g55_p100', 'noins_g25_p100', 'ins_g25_p100', 'ctrl'])
