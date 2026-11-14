"""Fig. 5K, the groups of item F5_def_HC_RP_LC_NP only (HC-RP, LC-NP), read by f5k.py."""
from f5k import read as read_panel

LABELS = ['HC-RP', 'LC-NP']


def read(fig):
    r = read_panel(fig)
    return {"groups": {k: r["groups"][k] for k in LABELS}}
