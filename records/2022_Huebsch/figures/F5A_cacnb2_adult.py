"""Fig. 5a (journal_version.pdf p. 7): CACNB2 expression relative to GAPDH, SM WTC monolayers vs adult heart total RNA
(item F5A_cacnb2_adult). Same panel and reading as F5A_cacnb2_mm.py: CACNB2's SM bar (3) with red squares and adult heart
bar (5) with green triangles."""
import _util as u


def read(fig):
    return {"groups": u.read_log_bars(fig, {
        "SM monolayer": (3, "square"),
        "Adult heart total RNA": (5, "triangle"),
    }, centre_kind="median")}
