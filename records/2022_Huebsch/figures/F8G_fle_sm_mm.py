"""Fig. 8g (journal_version.pdf p. 12): safety margin based on prevalence, SCVI20, flecainide, MPS maturation media vs
MPS standard media (item F8G_fle_sm_mm). Vector, log y axis (10^-3 to 10^3, labels printed as powers of ten). Three
drugs, three open bars each (2D SM black triangles, MPS standard media red squares, MPS maturation media blue circles)
with s.e.m. bars (see _util.read_sem_drug_bars). Each group is read with its points, the bar's top (mean) and the upper
s.e.m. cap."""
import _util as u


def read(fig):
    return {"groups": u.read_sem_drug_bars(fig, 0, ["MPS standard media", "MPS maturation media"])}
