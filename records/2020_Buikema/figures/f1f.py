"""Fig. 1F: pHH3+/TnT+ (%), one dot per biological replicate, mean ± SEM; w/o PSG, Dense, Sparse (left to right)."""
from _util import fan_out, read_dot_panel

TICKS = [0, 5, 10, 15]
LINKS = {
    "F1F_sparse_nopsg/sparse": "sparse",
    "F1F_sparse_nopsg/nopsg": "nopsg",
    "F1F_dense_nopsg/dense": "dense",
    "F1F_dense_nopsg/nopsg": "nopsg",
    "F1F_sparse_dense/sparse": "sparse",
    "F1F_sparse_dense/dense": "dense",
}


def read(fig):
    return fan_out(read_dot_panel(fig, TICKS, ["nopsg", "dense", "sparse"]), LINKS)
