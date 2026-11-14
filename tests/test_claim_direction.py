"""A claim judged against the computed direction of its evidence (02-audit, A stated claim against its own evidence)."""
from livinglit.models import Record
from livinglit.audit import claim_direction_flags
from tests.helpers import record


def _rec(asserts, judged="follows"):
    r = record()
    j = {d: "follows" for d in ("direction", "support", "comparison", "scope", "replication", "strength", "presence")}
    j["direction"] = judged
    r["claims"] = {"C1": {"kind": "stated", "quote": "q", "where": "Abstract", "rests_on": ["E1"], "judgement": j,
                          "asserts_direction": asserts}}
    return Record.model_validate(r)


def test_follows_against_opposite_computed_direction_is_flagged():
    """A claim whose direction is judged follows while an item it rests on has the opposite computed direction is flagged beside its verdict (02-audit, A stated claim against its own evidence)."""
    flags = claim_direction_flags(_rec("down"), {"E1": {"direction": "up", "origin": "computed"}})
    assert flags["C1"] and "E1" in flags["C1"][0]


def test_agreeing_or_unjudged_not_flagged():
    """No flag when the directions agree, the claim asserts none, or the direction is not judged follows (02-audit, A stated claim against its own evidence)."""
    dirs = {"E1": {"direction": "up", "origin": "computed"}}
    assert not claim_direction_flags(_rec("up"), dirs).get("C1")
    assert not claim_direction_flags(_rec(None), dirs).get("C1")
    assert not claim_direction_flags(_rec("down", judged="overstated"), dirs).get("C1")


def test_no_effect_is_not_opposite():
    """Only up against down is opposite: an item with no significant effect does not contradict a claimed direction (02-audit, A stated claim against its own evidence)."""
    assert not claim_direction_flags(_rec("down"), {"E1": {"direction": "none", "origin": "computed"}}).get("C1")
