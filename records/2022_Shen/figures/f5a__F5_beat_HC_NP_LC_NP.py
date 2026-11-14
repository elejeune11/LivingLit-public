"""Fig. 5A, the groups of item F5_beat_HC_NP_LC_NP only (HC-NP, LC-NP), read by f5a.py."""
from f5a import read as read_panel

LABELS = ['HC-NP', 'LC-NP']


def read(fig):
    r = read_panel(fig)
    return {"groups": {k: r["groups"][k] for k in LABELS}}
