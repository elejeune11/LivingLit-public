"""Fig. 2e (journal_version.pdf p. 4): APD80 (s) of WTC, MM MPS vs the two 2D monolayer groups (the omnibus item
F2E_platform). Vector, same crop as F2E_mps. SM 2D are open red squares, MM 2D open blue circles (all eleven drawn as
one compound path); each group is read with its mean and the upper end of its s.d. bar."""
import _util as u


def read(fig):
    return {"groups": u.read_vector_groups(fig, {
        "MM MPS": (1, {u.BLUE}),
        "SM 2D": (2, {u.RED}),
        "MM 2D": (3, {u.BLUE}),
    })}
