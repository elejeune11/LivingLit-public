"""Fig. 2f (journal_version.pdf p. 4): APD80 (s) of SCVI20, SM MPS vs MM MPS. Vector: every marker, bar and error bar
is a path. SM MPS are filled red squares, MM MPS filled blue circles; each is read with its mean and the upper end of
its s.d. bar."""
import _util as u


def read(fig):
    return {"groups": u.read_vector_groups(fig, {
        "SM MPS": (0, {u.RED}),
        "MM MPS": (1, {u.BLUE}),
    })}
