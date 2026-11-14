"""Fig. 1N: pHH3+/TnT+ (%), one dot per biological replicate, mean ± SEM; Dense, Sparse (left to right)."""
from _util import fan_out, read_dot_panel

TICKS = [0, 5, 10, 15]
LINKS = {
    "F1N/dense": "dense",
    "F1N/sparse": "sparse",
}


def read(fig):
    # Dense circles are drawn 3.7 x 4.0 pt, so markers up to 4.5 pt are accepted.
    return fan_out(read_dot_panel(fig, TICKS, ["dense", "sparse"], marker_max=4.5), LINKS)
