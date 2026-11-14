"""Fig. 7g (journal_version.pdf p. 11): safety margin based on prevalence, WTC, flecainide, all three groups (item
F7G_flecainide). Same reading as F7G_ver_2dsm (see _util.read_drug_bars)."""
import _util as u


def read(fig):
    return {"groups": u.read_drug_bars(fig, 0, ["2D SM", "MPS standard media", "MPS maturation media"])}
