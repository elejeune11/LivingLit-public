"""Fig. 3d (journal_version.pdf p. 5): MitoTracker Red intensity (raw RFU) of SCVI20 MPS, SM vs MM (item F3D_mps).
Vector, laid out as Fig. 3c: SM MPS filled red squares (each a fill and an outline path), MM MPS filled blue circles;
each group is read with its mean and the upper end of its s.d. bar. The y axis line and its four ticks are separate
paths and the labels carry thousands commas."""
import _util as u


def read(fig):
    return {"groups": u.read_split_axis_groups(fig, {
        "SM MPS": (0, u.RED),
        "MM MPS": (1, u.BLUE3),
    }, n_ticks=4)}
