"""Fig. 7g (journal_version.pdf p. 11): safety margin based on prevalence, WTC, verapamil, MPS standard media vs 2D SM
(item F7G_ver_2dsm). Vector, log y axis (10^-1 to 10^5, labels printed as powers of ten). Three drugs, three white bars
each (2D SM black triangles, MPS standard media red squares, MPS maturation media blue circles); no error bars are
drawn. Each group is read with its points and the bar's top (as mean)."""
import _util as u


def read(fig):
    return {"groups": u.read_drug_bars(fig, 1, ["2D SM", "MPS standard media"])}
