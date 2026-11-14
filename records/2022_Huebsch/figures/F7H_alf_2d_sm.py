"""Fig. 7h (journal_version.pdf p. 11): safety margin based on cAPD80, WTC, alfuzosin, MPS standard media vs 2D SM
(item F7H_alf_2d_sm). Laid out as Fig. 7g (see _util.read_drug_bars): vector, log y axis (10^-1 to 10^5), three
drugs, three white bars each, no error bars drawn; each group is read with its points and the bar's top (as mean)."""
import _util as u


def read(fig):
    return {"groups": u.read_drug_bars(fig, 2, ["2D SM", "MPS standard media"])}
