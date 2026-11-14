"""Fig. 3d (journal_version.pdf p. 5): MitoTracker Red intensity (raw RFU) of SCVI20 2D monolayers, SM vs MM (item
F3D_2d). Vector, same crop as F3D_mps. SM 2D open red squares (four rectangles in one path), MM 2D open blue circles
(four circles in one path); each group is read with its mean and the upper end of its s.d. bar."""
import _util as u


def read(fig):
    return {"groups": u.read_split_axis_groups(fig, {
        "SM 2D": (2, u.RED),
        "MM 2D": (3, u.BLUE3),
    }, n_ticks=4)}
