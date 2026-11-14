"""Fig. S7C: force of contraction (μN) at 48 h, bars ± SEM (raster), -INS/+INS pairs by glucose and palmitate, then CTRL. Ticks 0-300 by 100."""
from _util import bar_panel


def read(fig):
    return bar_panel(fig, [0, 100, 200, 300], ['noins_g0_p0', 'ins_g0_p0', 'noins_g1_p0', 'ins_g1_p0', 'noins_g55_p0', 'ins_g55_p0', 'noins_g25_p0', 'ins_g25_p0', 'noins_g0_p100', 'ins_g0_p100', 'noins_g1_p100', 'ins_g1_p100', 'noins_g55_p100', 'ins_g55_p100', 'noins_g25_p100', 'ins_g25_p100', 'ctrl'])
