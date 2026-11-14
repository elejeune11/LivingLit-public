"""Fig. 8g (journal_version.pdf p. 12): safety margin based on prevalence, SCVI20, verapamil, MPS maturation media vs
2D SM (item F8G_ver_2d_mm). Laid out as Fig. 8g (see F8G_fle_sm_mm and _util.read_sem_drug_bars)."""
import _util as u


def read(fig):
    return {"groups": u.read_sem_drug_bars(fig, 1, ["2D SM", "MPS maturation media"])}
