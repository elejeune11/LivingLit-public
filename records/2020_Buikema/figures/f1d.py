"""Fig. 1D: Ki67+/TnT+ (%), one dot per biological replicate, mean ± SEM; w/o PSG, Dense, Sparse (left to right)."""
from _util import fan_out, read_dot_panel

TICKS = [0, 10, 20, 30, 40, 50]
LINKS = {
    "F1D_sparse_nopsg/sparse": "sparse",
    "F1D_sparse_nopsg/nopsg": "nopsg",
    "F1D_dense_nopsg/dense": "dense",
    "F1D_dense_nopsg/nopsg": "nopsg",
    "F1D_sparse_dense/sparse": "sparse",
    "F1D_sparse_dense/dense": "dense",
}


def read(fig):
    return fan_out(read_dot_panel(fig, TICKS, ["nopsg", "dense", "sparse"]), LINKS)
