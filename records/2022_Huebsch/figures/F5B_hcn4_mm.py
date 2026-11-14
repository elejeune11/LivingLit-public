"""Fig. 5b (journal_version.pdf p. 7): HCN4 expression relative to GAPDH, MM SCVI20 monolayers vs adult heart total RNA
(item F5B_hcn4_mm). Same panel and reading as F5B_hcn4_sm.py: HCN4's MM bar (10) with blue circles and adult heart
bar (11) with green triangles."""
import _util as u


def read(fig):
    return {"groups": u.read_log_bars(fig, {
        "MM monolayer": (10, "circle"),
        "Adult heart total RNA": (11, "triangle"),
    }, centre_kind="median", axis=u.split_log_vector_axis)}
