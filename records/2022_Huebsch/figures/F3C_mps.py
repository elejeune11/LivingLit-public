"""Fig. 3c (journal_version.pdf p. 5): MitoTracker Red intensity (raw RFU) of WTC MPS, SM vs MM (item F3C_mps).
Vector: every marker, bar and error bar is a path. SM MPS filled red squares (each a fill and an outline path), MM MPS
filled blue circles; each group is read with its mean and the upper end of its s.d. bar. The y axis line and its four
ticks are separate paths and the labels carry thousands commas."""
import _util as u


def read(fig):
    return {"groups": u.read_split_axis_groups(fig, {
        "SM MPS": (0, u.RED),
        "MM MPS": (1, u.BLUE3),
    }, n_ticks=4)}
