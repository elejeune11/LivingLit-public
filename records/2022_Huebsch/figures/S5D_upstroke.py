"""Supplementary Fig. 5d (Supplementary_Figures.pdf p. 6): normalized upstroke duration of the calcium transient after
thapsigargin, WTC MPS pre-treated with SM or MM. Same layout as Supplementary Fig. 4 (vector, separate paths); read as
S4B_ff0."""
import _util as u


def read(fig):
    return {"groups": u.read_supp_groups(fig, {"SM": (0, u.SUPP_RED), "MM": (1, u.SUPP_BLUE)}, n_ticks=5)}
