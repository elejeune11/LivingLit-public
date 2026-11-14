"""Fig. 7g (journal_version.pdf p. 11): safety margin based on prevalence, WTC, verapamil, MPS maturation media vs MPS
standard media (item F7G_ver_sm_mm). Same reading as F7G_ver_2dsm (see _util.read_drug_bars)."""
import _util as u


def read(fig):
    return {"groups": u.read_drug_bars(fig, 1, ["MPS standard media", "MPS maturation media"])}
