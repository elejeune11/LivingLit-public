"""Synthetic fixtures with no paper content (07-building, Test-driven development)."""
import copy

BASE = {
    "id": "2099_Synth",
    "source": {"title": "A synthetic study", "year": "2099", "files": ["main.txt"]},
    "default_context": {"platform": "micropillar tissue", "temperature": "37 C"},
    "units": {
        "F1": {"where": "Fig. 1a-b", "title": "Pacing and calcium", "context": {"day_of_measurement": "day 14"},
               "groups": {
                   "HC_NP": {"label": "HC-NP", "context": {"culture_calcium_mM": "1.8 mM", "pacing": "none"}},
                   "HC_RP": {"label": "HC-RP", "context": {"culture_calcium_mM": "1.8 mM", "pacing": "ramp pacing"}},
                   "LC_NP": {"label": "LC-NP", "context": {"culture_calcium_mM": "0.9 mM", "pacing": "none"}},
                   "LC_RP": {"label": "LC-RP", "context": {"culture_calcium_mM": "0.9 mM", "pacing": "ramp pacing"}},
               }},
    },
    "evidence": {
        "E1": {"unit": "F1", "measure": "twitch force", "finding": "ramp pacing raised force",
               "compares": ["HC_RP", "HC_NP"],
               "values": {"force_HC_RP": {"printed": "2.0 ± 0.5", "unit": "mN", "group": "HC_RP", "spread": "SD"},
                          "force_HC_NP": {"printed": "1.0 ± 0.4", "unit": "mN", "group": "HC_NP", "spread": "SD"}},
               "n": {"printed": "n = 6", "counts": "tissues", "per_group": {"HC_RP": "6", "HC_NP": "6"}},
               "stats": {"test": "unpaired t-test", "p": "P < 0.01"},
               "anchor": {"quote": "ramp pacing increased twitch force", "where": "Results"}},
    },
    "claims": {}, "citations": {},
}


def record(**changes):
    r = copy.deepcopy(BASE)
    for k, v in changes.items():
        r[k] = v
    return r
