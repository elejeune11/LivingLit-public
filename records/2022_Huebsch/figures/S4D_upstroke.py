"""Supplementary Fig. 4d (Supplementary_Figures.pdf p. 5): normalized upstroke duration of the calcium transient after
ryanodine, WTC MPS pre-treated with SM or MM. Read as S4B_ff0 (vector, separate paths)."""
import _util as u


def read(fig):
    return {"groups": u.read_supp_groups(fig, {"SM": (0, u.SUPP_RED), "MM": (1, u.SUPP_BLUE)}, n_ticks=4)}
