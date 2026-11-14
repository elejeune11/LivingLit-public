"""Fig. 2f (journal_version.pdf p. 4): APD80 (s) of SCVI20, SM 2D vs MM 2D. Vector, same crop as F2F_mps. SM 2D are
open red squares, MM 2D open blue circles (drawn as one compound path); each is read with its mean and the upper end
of its s.d. bar."""
import _util as u


def read(fig):
    return {"groups": u.read_vector_groups(fig, {
        "SM 2D": (2, {u.RED}),
        "MM 2D": (3, {u.BLUE}),
    })}
