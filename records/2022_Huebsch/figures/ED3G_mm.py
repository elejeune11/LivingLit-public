"""Extended Data Fig. 3g (journal_version.pdf p. 22): cAPD80 (msec), MM vs SM (item ED3G_mm). See _util.read_ed3g."""
import _util as u


def read(fig):
    return {"groups": u.read_ed3g(fig, ["MM", "SM"])}
