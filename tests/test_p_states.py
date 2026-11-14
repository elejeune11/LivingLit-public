"""P states and several printed P per item (02-audit, Values)."""
from livinglit.numbers import parse_p, P_SIG_STATE
from livinglit.models import Record
from livinglit.checks import check_item
from livinglit.across import item_direction
from livinglit.checks import gather
from livinglit.formulas import load_library
from tests.helpers import record

LIB = load_library()


def test_significant_threshold_not_stated_is_a_named_state():
    """Asterisks without a stated threshold give the state 'significant, threshold not stated': significant, with no value (02-audit, Values)."""
    pp = parse_p(P_SIG_STATE)
    assert pp is not None and pp.significant and pp.op == "sig"
    assert parse_p("*") is None  # bare asterisks are still not a P


def _rec(p, extra=None):
    r = record()
    r["evidence"]["E1"]["stats"]["p"] = p
    if extra:
        r["evidence"]["E1"]["stats"]["p_values"] = extra
    return Record.model_validate(r)


def test_named_state_allows_direction_but_no_p_check():
    """The named state allows a direction but no P check (02-audit, Values)."""
    rec = _rec(P_SIG_STATE)
    cs = [c for c in check_item(rec, "E1", LIB) if c.check in ("summary to P", "points to P")]
    assert cs and all(c.verdict == "cannot check" for c in cs)
    d = item_direction(rec.evidence["E1"], gather(rec, "E1"))
    assert d.direction == "up"


def test_several_printed_p_are_each_checked_and_compared():
    """Several printed P for one item are each recorded with its anchor and checked; disagreeing significance is a reported-twice finding (02-audit, Values)."""
    rec = _rec("P < 0.01", [{"p": "n.s.", "anchor": {"quote": "no difference in force", "where": "legend"}}])
    cs = check_item(rec, "E1", LIB)
    twice = [c for c in cs if c.check == "reported twice" and "P" in c.note]
    assert twice and twice[0].verdict == "inconsistent"
    assert sum(1 for c in cs if c.check == "summary to P") == 2


def test_agreeing_printed_p_are_consistent():
    """Printed P that agree in significance and value are consistent as reported twice (02-audit, Values)."""
    rec = _rec("P = 0.003", [{"p": "P < 0.01", "anchor": {"quote": "q", "where": "text"}}])
    twice = [c for c in check_item(rec, "E1", LIB) if c.check == "reported twice" and "P" in c.note]
    assert twice and twice[0].verdict == "consistent"
