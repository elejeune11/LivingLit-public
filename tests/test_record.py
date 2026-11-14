import pytest
from pydantic import ValidationError

from livinglit.models import Record, Item
from livinglit.record import structure_problems, resolve_context, value_at
from tests.helpers import record


def test_unknown_keys_refused():
    """Pydantic models refuse unknown keys (07-building, What the first build taught about the code)."""
    r = record()
    r["evidence"]["E1"]["contrast"] = {"varies": "pacing"}
    with pytest.raises(ValidationError):
        Record.model_validate(r)


@pytest.mark.parametrize("bad", ["E1.a", "E 1", "F2/a"])
def test_ids_without_dots(bad):
    """Unit and item ids are [A-Za-z0-9_]+: no dots, spaces or slashes (02-audit, Ids)."""
    r = record()
    r["evidence"][bad] = r["evidence"].pop("E1")
    with pytest.raises(ValidationError):
        Record.model_validate(r)


def test_item_forms():
    """An item has groups (a measurement) or compares (pair, omnibus with test_of, main effect with sides) (02-audit, One evidence item per printed test)."""
    base = dict(unit="F1", measure="m", finding="f", anchor={"quote": "q", "where": "w"})
    Item.model_validate({**base, "groups": ["a"]})
    Item.model_validate({**base, "compares": ["a", "b"]})
    Item.model_validate({**base, "compares": ["a", "b", "c"], "test_of": "omnibus"})
    Item.model_validate({**base, "compares": {"condition": ["a", "b"], "reference": ["c", "d"]}, "test_of": "main effect"})
    with pytest.raises(ValidationError):
        Item.model_validate({**base, "compares": ["a", "b", "c"]})
    with pytest.raises(ValidationError):
        Item.model_validate({**base, "compares": {"condition": ["a"], "reference": ["c"]}})
    with pytest.raises(ValidationError):
        Item.model_validate({**base, "groups": ["a"], "compares": ["a", "b"]})


def test_value_between_two_groups():
    """A value relating two groups carries between: [a, b], not a group (02-audit, Values)."""
    r = record()
    r["evidence"]["E1"]["values"]["diff"] = {"printed": "65% lower", "unit": "%", "between": ["HC_RP", "HC_NP"]}
    assert structure_problems(Record.model_validate(r)) == []
    r["evidence"]["E1"]["values"]["diff"]["group"] = "HC_RP"
    with pytest.raises(ValidationError):
        Record.model_validate(r)


def test_groups_must_exist():
    """Items, values and n name groups of their own unit (02-audit, Groups)."""
    r = record()
    r["evidence"]["E1"]["compares"] = ["HC_RP", "XX"]
    probs = structure_problems(Record.model_validate(r))
    assert any("XX" in p for p in probs)
    r = record()
    r["evidence"]["E1"]["values"]["force_HC_RP"]["group"] = "LC_RP"
    assert any("LC_RP" in p for p in structure_problems(Record.model_validate(r)))


def test_unit_must_exist():
    """Every item names an existing unit (02-audit, Units)."""
    r = record()
    r["evidence"]["E1"]["unit"] = "F9"
    assert any("F9" in p for p in structure_problems(Record.model_validate(r)))


def test_default_field_may_not_differ_between_units():
    """A field whose value differs between units may not appear in default_context (02-audit, Context per unit; 08 decision 13)."""
    r = record()
    r["units"]["F1"]["context"]["platform"] = "2D monolayer"
    assert any("platform" in p for p in structure_problems(Record.model_validate(r)))


def test_group_field_not_in_unit_or_default():
    """A group's context holds what sets it apart, so its fields are not also in the unit or default context (02-audit, Groups)."""
    r = record()
    r["units"]["F1"]["context"]["pacing"] = "none"
    assert any("pacing" in p for p in structure_problems(Record.model_validate(r)))


def test_context_resolution_order():
    """An item's context for a group is default → unit → group → item, resolved by code and never stored (02-audit, Context per unit)."""
    r = record()
    r["evidence"]["E1"]["context"] = {"day_of_measurement": "day 21"}
    rec = Record.model_validate(r)
    c = resolve_context(rec, "E1", "HC_RP")
    assert c["platform"] == "micropillar tissue"
    assert c["pacing"] == "ramp pacing"
    assert c["day_of_measurement"] == "day 21"


def test_value_paths():
    """Values are addressed as <item>.values.<name> (02-audit, Ids)."""
    rec = Record.model_validate(record())
    assert value_at(rec, "E1.values.force_HC_RP").printed == "2.0 ± 0.5"
    with pytest.raises(KeyError):
        value_at(rec, "E1.values.nope")


def test_stated_claim_needs_judgement():
    """A stated claim is judged on all seven dimensions; the verdict is the worst (02-audit, A stated claim against its own evidence)."""
    from livinglit.models import Claim, claim_verdict
    dims = dict.fromkeys(["direction", "support", "comparison", "scope", "replication", "strength", "presence"], "follows")
    c = Claim(kind="stated", quote="q", where="Abstract", judgement={**dims, "scope": "overstated", "support": "cannot judge"})
    assert claim_verdict(c) == "overstated"
    with pytest.raises(ValidationError):
        Claim(kind="stated", quote="q", where="Abstract")
