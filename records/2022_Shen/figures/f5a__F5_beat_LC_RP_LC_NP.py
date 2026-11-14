"""Fig. 5A, the groups of item F5_beat_LC_RP_LC_NP only (LC-NP, LC-RP), read by f5a.py."""
from f5a import read as read_panel

LABELS = ['LC-NP', 'LC-RP']


def read(fig):
    r = read_panel(fig)
    return {"groups": {k: r["groups"][k] for k in LABELS}}
