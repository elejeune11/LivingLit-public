"""Fig. 1L: Ki67+/TnT+ (%), one dot per biological replicate, mean ± SEM; Dense, Sparse (left to right)."""
from _util import fan_out, read_dot_panel

TICKS = [0, 10, 20, 30, 40]
LINKS = {
    "F1L/dense": "dense",
    "F1L/sparse": "sparse",
}


def read(fig):
    return fan_out(read_dot_panel(fig, TICKS, ["dense", "sparse"]), LINKS)
