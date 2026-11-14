"""Fig. 5K, the groups of item F5_def_HC_RP_HC_NP only (HC-NP, HC-RP), read by f5k.py."""
from f5k import read as read_panel

LABELS = ['HC-NP', 'HC-RP']


def read(fig):
    r = read_panel(fig)
    return {"groups": {k: r["groups"][k] for k in LABELS}}
