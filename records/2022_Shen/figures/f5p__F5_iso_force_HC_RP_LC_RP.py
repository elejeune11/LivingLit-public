"""Fig. 5P, the groups of item F5_iso_force_HC_RP_LC_RP only (HC-RP, LC-RP), read by f5p.py."""
from f5p import read as read_panel

LABELS = ['HC-RP', 'LC-RP']


def read(fig):
    r = read_panel(fig)
    return {"groups": {k: r["groups"][k] for k in LABELS}}
