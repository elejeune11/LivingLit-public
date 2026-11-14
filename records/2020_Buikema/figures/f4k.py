"""Fig. 4K: Ki67+/TnT+ (%), one dot per biological replicate, mean ± SEM; Dense - DMSO (blue circles),
Sparse - DMSO (red squares), Sparse - 0.1uM (green triangles), Sparse - 1 uM (purple triangles),
Sparse - 10 uM (orange diamonds), left to right."""
from _util import fan_out, read_dot_panel

TICKS = [0, 20, 40, 60, 80]
LINKS = {
    "F4K_vp10/vp10": "vp10",
    "F4K_vp10/sparse_dmso": "sparse_dmso",
}


def read(fig):
    panel = read_dot_panel(fig, TICKS, ["dense_dmso", "sparse_dmso", "vp01", "vp1", "vp10"])
    return fan_out(panel, LINKS)
