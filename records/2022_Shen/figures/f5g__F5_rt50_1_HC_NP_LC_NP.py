"""Fig. 5G, the groups of item F5_rt50_1_HC_NP_LC_NP only (HC-NP, LC-NP), read by f5g.py."""
from f5g import read as read_panel

LABELS = ['HC-NP', 'LC-NP']


def read(fig):
    r = read_panel(fig)
    return {"groups": {k: r["groups"][k] for k in LABELS}}
