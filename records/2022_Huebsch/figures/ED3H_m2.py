"""Extended Data Fig. 3h (journal_version.pdf p. 22): prevalence of beating (1 Hz pacing), M2 vs SM (item ED3H_m2).
See _util.read_ed3h."""
import _util as u


def read(fig):
    return {"groups": u.read_ed3h(fig)}
