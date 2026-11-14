"""Fig. 7h (journal_version.pdf p. 11): safety margin based on cAPD80, WTC, alfuzosin, MPS maturation media vs MPS
standard media (item F7H_alf_sm_mm). Same reading as F7H_alf_2d_sm (see _util.read_drug_bars)."""
import _util as u


def read(fig):
    return {"groups": u.read_drug_bars(fig, 2, ["MPS standard media", "MPS maturation media"])}
