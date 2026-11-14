"""Fig. 4B: YAP nuclear/cytoplasmic ratio (pixel intensity), one dot per biological replicate, mean ± SEM;
Dense (red circles), Sparse (green squares), left to right."""
from _util import fan_out, read_dot_panel

TICKS = [0, 5, 10, 15]
LINKS = {
    "F4B/dense": "dense",
    "F4B/sparse": "sparse",
}


def read(fig):
    return fan_out(read_dot_panel(fig, TICKS, ["dense", "sparse"]), LINKS)
