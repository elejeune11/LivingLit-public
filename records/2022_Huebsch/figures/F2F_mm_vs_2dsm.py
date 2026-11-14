"""Fig. 2f (journal_version.pdf p. 4): APD80 (s) of SCVI20, MM MPS vs SM 2D. Vector, same crop as F2F_mps. MM MPS are
filled blue circles, SM 2D open red squares; each is read with its mean and the upper end of its s.d. bar."""
import _util as u


def read(fig):
    return {"groups": u.read_vector_groups(fig, {
        "MM MPS": (1, {u.BLUE}),
        "SM 2D": (2, {u.RED}),
    })}
