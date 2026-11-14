"""Extended Data Fig. 3g (journal_version.pdf p. 22): cAPD80 (msec), M2 vs SM (item ED3G_m2). See _util.read_ed3g."""
import _util as u


def read(fig):
    return {"groups": u.read_ed3g(fig, ["M2", "SM"])}
