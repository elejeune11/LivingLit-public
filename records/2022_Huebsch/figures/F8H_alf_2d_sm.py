"""Fig. 8h (journal_version.pdf p. 12): safety margin based on cAPD80 (axis label; the legend says APD80), SCVI20,
alfuzosin, MPS standard media vs 2D SM (item F8H_alf_2d_sm). Laid out as Fig. 8g (see F8G_fle_sm_mm and
_util.read_sem_drug_bars)."""
import _util as u


def read(fig):
    return {"groups": u.read_sem_drug_bars(fig, 2, ["2D SM", "MPS standard media"])}
