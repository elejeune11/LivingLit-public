"""Group kinds, linked fields, values over several groups (02-audit, Groups; What code computes; Values)."""
import copy

import pytest
from pydantic import ValidationError

from livinglit.models import Record, Value
from livinglit.groups import item_contrast, unit_design, stated_signatures
from livinglit.record import structure_problems, group_context, resolve_context, BENCHMARK_STATE
from tests.helpers import record


def _with_native():
    r = record()
    r["units"]["F1"]["groups"]["ADULT"] = {"label": "adult ventricle", "kind": "native tissue",
                                           "context": {"platform": "native tissue", "temperature": "37 C"}}
    return r


def test_group_kind_defaults_to_engineered():
    """A group's kind is engineered unless stated (02-audit, Groups)."""
    rec = Record.model_validate(record())
    assert rec.units["F1"].groups["HC_NP"].kind == "engineered"


def test_other_study_group_needs_citation():
    """An other-study group carries its citation (02-audit, Groups)."""
    r = record()
    r["units"]["F1"]["groups"]["SIM"] = {"label": "Sim et al.", "kind": "other study", "context": {}}
    with pytest.raises(ValidationError):
        Record.model_validate(r)


def test_native_group_resolves_only_its_own_context():
    """A native or other-study group resolves only its own context; nothing is inherited (02-audit, Groups)."""
    rec = Record.model_validate(_with_native())
    ctx = group_context(rec, "F1", "ADULT")
    assert ctx["platform"] == "native tissue"
    assert "day_of_measurement" not in ctx  # the unit's day is not inherited
    assert BENCHMARK_STATE == "not stated in this source"


def test_native_group_may_state_fields_the_default_holds():
    """A benchmark group may state a field that the unit or default context holds, since it inherits neither (02-audit, Groups)."""
    rec = Record.model_validate(_with_native())
    assert not [p for p in structure_problems(rec) if "ADULT" in p]


def test_pair_with_native_group_is_against_benchmark():
    """A pair with a native or other-study group is against benchmark: no contrast, no confound (02-audit, Groups)."""
    rec = Record.model_validate(_with_native())
    it = rec.evidence["E1"].model_copy(update={"compares": ["HC_RP", "ADULT"]})
    c = item_contrast(rec, it, stated_signatures(rec, "F1"))
    assert c.benchmark and not c.confound and c.field is None and not c.problems


def test_benchmark_groups_left_out_of_design():
    """Benchmark groups take no part in factorial recognition (02-audit, What code computes)."""
    rec = Record.model_validate(_with_native())
    d = unit_design(rec, "F1", stated_signatures(rec, "F1"))
    assert d.factorial and "ADULT" not in d.groups


def _linked_record():
    r = record()
    g = r["units"]["F1"]["groups"]
    g["HC_NP"]["context"].update({"genotype": "PKP2 c.2013delC", "disease_model": "ACM"})
    g["HC_RP"]["context"].update({"genotype": "wild type", "disease_model": "none"})
    for k in ("LC_NP", "LC_RP"):
        g[k]["context"].update({"genotype": "wild type", "disease_model": "none"})
    return Record.model_validate(r)


def test_linked_fields_are_one_contrast_on_the_first():
    """A pair differing only in fields declared linked is one contrast on the first field (02-audit, What code computes)."""
    rec = _linked_record()
    it = rec.evidence["E1"].model_copy(update={"compares": ["LC_NP", "HC_NP"]})
    sigs = stated_signatures(rec, "F1")
    plain = item_contrast(rec, it, sigs)
    assert plain.confound  # media_calcium + genotype + disease_model without links
    rec2 = copy.deepcopy(rec)
    it2 = rec2.evidence["E1"].model_copy(update={"compares": ["HC_RP", "HC_NP"]})
    c = item_contrast(rec2, it2, sigs, linked=[["genotype", "disease_model"]])
    # HC_RP vs HC_NP differ in pacing as well, so still a confound; build a clean pair:
    assert c.confound
    rec3 = Record.model_validate({**record(), "units": {"F1": {**record()["units"]["F1"], "groups": {
        "MUT": {"label": "mut", "context": {"genotype": "PKP2 het", "disease_model": "ACM"}},
        "WT": {"label": "wt", "context": {"genotype": "wild type", "disease_model": "none"}}}}},
        "default_context": {**record()["default_context"], "pacing": "none", "culture_calcium_mM": "1.8 mM"}})
    it3 = rec3.evidence["E1"].model_copy(update={"compares": ["MUT", "WT"], "values": {}, "n": "not stated"})
    s3 = stated_signatures(rec3, "F1")
    c3 = item_contrast(rec3, it3, s3, linked=[["genotype", "disease_model"]])
    assert c3.field == "genotype" and not c3.confound and c3.linked == ["genotype", "disease_model"]
    assert item_contrast(rec3, it3, s3).confound  # without the declaration it is a confound


def test_linked_does_not_hide_a_third_field():
    """A pair differing in linked fields and another field (a non-isogenic line) stays a confound (02-audit, What code computes)."""
    r = record()
    r["default_context"].update({"pacing": "none", "culture_calcium_mM": "1.8 mM"})
    r["units"]["F1"]["groups"] = {
        "MUT": {"label": "mut", "context": {"genotype": "DSP het", "disease_model": "ACM", "cell_line": "line A"}},
        "WT": {"label": "wt", "context": {"genotype": "wild type", "disease_model": "none", "cell_line": "line B"}}}
    rec = Record.model_validate(r)
    it = rec.evidence["E1"].model_copy(update={"compares": ["MUT", "WT"], "values": {}, "n": "not stated"})
    c = item_contrast(rec, it, stated_signatures(rec, "F1"), linked=[["genotype", "disease_model"]])
    assert c.confound


def test_value_over_several_groups():
    """A value printed for several groups at once carries over: [groups], not group or between (02-audit, Values)."""
    v = Value.model_validate({"printed": "13", "unit": "%", "over": ["a", "b", "c"]})
    assert v.over == ["a", "b", "c"]
    with pytest.raises(ValidationError):
        Value.model_validate({"printed": "13", "unit": "%", "over": ["a"], "group": "a"})


def test_value_over_names_groups_of_the_unit():
    """Groups named by over belong to the item's unit (02-audit, Values)."""
    r = record()
    r["evidence"]["E1"]["values"]["shared"] = {"printed": "13", "unit": "%", "over": ["HC_RP", "ZZ"]}
    rec = Record.model_validate(r)
    assert any("ZZ" in p for p in structure_problems(rec))


def test_field_config_declares_linked_and_new_fields():
    """Field content declares genotype ~ disease_model as linked and the fields mechanical_load, transgene, culture and measurement calcium and donor_age (03-vocabulary, Fields and terms)."""
    from livinglit.vocab import field_config
    cfg = field_config()
    assert ["genotype", "disease_model"] in cfg["linked"]
    for f in ("mechanical_load", "transgene", "culture_calcium_mM", "measurement_calcium_mM", "donor_age"):
        assert f in cfg["fields"]
    assert "media_calcium_mM" not in cfg["fields"]
    assert BENCHMARK_STATE in cfg["named_states"]
