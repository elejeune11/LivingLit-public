"""Fig. 5V, the groups of item F5_iso_t80_HC_RP_LC_NP only (HC-RP, LC-NP), read by f5v.py."""
from f5v import read as read_panel

LABELS = ['HC-RP', 'LC-NP']


def read(fig):
    r = read_panel(fig)
    return {"groups": {k: r["groups"][k] for k in LABELS}}
