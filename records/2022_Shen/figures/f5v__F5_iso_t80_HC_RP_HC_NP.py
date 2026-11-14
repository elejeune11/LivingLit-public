"""Fig. 5V, the groups of item F5_iso_t80_HC_RP_HC_NP only (HC-NP, HC-RP), read by f5v.py."""
from f5v import read as read_panel

LABELS = ['HC-NP', 'HC-RP']


def read(fig):
    r = read_panel(fig)
    return {"groups": {k: r["groups"][k] for k in LABELS}}
