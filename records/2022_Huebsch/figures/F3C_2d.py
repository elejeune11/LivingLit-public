"""Fig. 3c (journal_version.pdf p. 5): MitoTracker Red intensity (raw RFU) of WTC 2D monolayers, SM vs MM (item
F3C_2d). Vector, same crop as F3C_mps. SM 2D open red squares (three rectangles in one path), MM 2D open blue circles
(three circles in one path); each group is read with its mean and the upper end of its s.d. bar."""
import _util as u


def read(fig):
    return {"groups": u.read_split_axis_groups(fig, {
        "SM 2D": (2, u.RED),
        "MM 2D": (3, u.BLUE3),
    }, n_ticks=4)}
