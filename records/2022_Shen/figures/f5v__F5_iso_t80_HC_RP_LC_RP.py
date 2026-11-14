"""Fig. 5V, the groups of item F5_iso_t80_HC_RP_LC_RP only (HC-RP, LC-RP), read by f5v.py."""
from f5v import read as read_panel

LABELS = ['HC-RP', 'LC-RP']


def read(fig):
    r = read_panel(fig)
    return {"groups": {k: r["groups"][k] for k in LABELS}}
