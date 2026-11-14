"""Supplementary Fig. 4b (Supplementary_Figures.pdf p. 5): normalized F/F0 after ryanodine, WTC MPS pre-treated with SM
or MM. Vector: open bars at the mean with mean ± s.d. error bars, SM filled red squares, MM filled blue circles; every
axis, tick, bar and error-bar line is its own path. Each group is read with every point, its mean and the upper end of
its s.d. bar."""
import _util as u


def read(fig):
    return {"groups": u.read_supp_groups(fig, {"SM": (0, u.SUPP_RED), "MM": (1, u.SUPP_BLUE)}, n_ticks=3)}
