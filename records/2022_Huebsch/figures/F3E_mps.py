"""Fig. 3e (journal_version.pdf p. 5): MitoTracker Red intensity (raw RFU) of G15.AO MPS, SM vs MM (item F3E_mps).
Vector, laid out as Fig. 3c/d with MPS groups only: SM MPS filled red squares (each a fill and an outline path), MM MPS
filled blue circles in a darker blue than panels c and d; each group is read with its mean and the upper end of its s.d.
bar (its caps are 8.35 pt wide, wider than in panels c and d). The y axis line and its five ticks (0–4,000) are
separate paths and the labels carry thousands commas."""
import _util as u

BLUE3E = (0.16, 0.28, 0.52)  # panel e's MM blue


def read(fig):
    return {"groups": u.read_split_axis_groups(fig, {
        "SM MPS": (0, u.RED),
        "MM MPS": (1, BLUE3E),
    }, n_ticks=5, cap_max=9)}
