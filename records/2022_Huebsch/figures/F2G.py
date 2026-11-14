"""Fig. 2g (journal_version.pdf p. 4): background-normalized calcium amplitude (F/F0) of WTC MPS, SM vs MM. Vector:
open bars at the mean, black mean ± s.d. error bars, SM filled red squares, MM filled blue circles (a darker blue than
panels e,f). Each group is read with every point, its mean and the upper end of its s.d. bar."""
import _util as u

BLUE_G = (0.23, 0.28, 0.62)  # MM circles of panel g


def read(fig):
    return {"groups": u.read_vector_groups(fig, {
        "SM": (0, {u.RED}),
        "MM": (1, {BLUE_G}),
    })}
