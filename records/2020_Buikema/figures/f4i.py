"""Fig. 4I: YAP nuclear/cytoplasmic ratio (pixel intensity), one dot per biological replicate, mean line only
(the SEM of the legend is not drawn as vector objects); Dense - DMSO (blue circles), Sparse - DMSO (red squares),
Sparse - 0.1uM (green triangles), Sparse - 1 uM (purple triangles), Sparse - 10 uM (orange diamonds), left to right."""
from _util import fan_out, read_dot_panel

TICKS = [0, 1, 2, 3, 4, 5]
LINKS = {
    "F4I_dense/dense_dmso": "dense_dmso",
    "F4I_dense/sparse_dmso": "sparse_dmso",
    "F4I_vp10/vp10": "vp10",
    "F4I_vp10/sparse_dmso": "sparse_dmso",
}


def read(fig):
    panel = read_dot_panel(fig, TICKS, ["dense_dmso", "sparse_dmso", "vp01", "vp1", "vp10"], error_bars=False)
    return fan_out(panel, LINKS)
