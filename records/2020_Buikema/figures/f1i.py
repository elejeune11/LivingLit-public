"""Fig. 1I: Ki67+/TnT+ (%), one dot per biological replicate, mean ± SEM; Fresh, 1X, 0.1X, 0.01X Dense (C/M) (left to right)."""
from _util import fan_out, read_dot_panel

TICKS = [0, 20, 40, 60, 80]
LINKS = {
    "F1I_omnibus/fresh": "fresh",
    "F1I_omnibus/cm1x": "cm1x",
    "F1I_omnibus/cm01x": "cm01x",
    "F1I_omnibus/cm001x": "cm001x",
}


def read(fig):
    return fan_out(read_dot_panel(fig, TICKS, ["fresh", "cm1x", "cm01x", "cm001x"], ytick_max=4.5), LINKS)
