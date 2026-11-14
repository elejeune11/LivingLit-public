"""Fig. S1F: cardiac troponin I (pg/ml), vector bars ± SEM; axis from tick rects and tick words."""
from _util import vector_bars


def read(fig):
    return vector_bars(fig, ["g0_p0", "g1_p0", "g55_p0", "g1_p1", "g1_p10", "g0_p100", "g1_p100", "g55_p100", "neg", "pos"])
