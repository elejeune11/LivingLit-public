from livinglit.models import Record
from livinglit.groups import item_contrast, unit_design, stated_signatures
from tests.helpers import record


def _rec(**kw):
    return Record.model_validate(record(**kw))


def _contrast(rec, compares, test_of=None):
    it = rec.evidence["E1"].model_copy(update={"compares": compares, "test_of": test_of})
    return item_contrast(rec, it, stated_signatures(rec, "F1"))


def test_pair_with_one_differing_field_is_a_contrast():
    """For a pair, one differing field gives a contrast on that field (02-audit, What code computes)."""
    c = _contrast(_rec(), ["HC_RP", "HC_NP"])
    assert c.kind == "pair" and c.fields == ["pacing"] and not c.confound


def test_pair_with_two_fields_is_a_confound():
    """A pair differing in more than one field is a confound, flagged by code (02-audit, What code computes)."""
    c = _contrast(_rec(), ["HC_RP", "LC_NP"])
    assert c.confound and set(c.fields) == {"pacing", "culture_calcium_mM"}


def test_main_effect_balanced():
    """For a main effect, the sides differ in one field and are balanced on the others (02-audit, What code computes)."""
    from livinglit.models import Sides
    c = _contrast(_rec(), Sides(condition=["HC_RP", "LC_RP"], reference=["HC_NP", "LC_NP"]), "main effect")
    assert c.fields == ["pacing"] and c.balanced and not c.problems


def test_main_effect_unbalanced_flagged():
    """A main effect whose sides are not balanced on the other fields is flagged (02-audit, What code computes)."""
    from livinglit.models import Sides
    c = _contrast(_rec(), Sides(condition=["HC_RP", "LC_RP"], reference=["HC_NP", "HC_NP"]), "main effect")
    assert not c.balanced and c.problems


def test_factorial_recognised():
    """A unit whose groups cross two fields in all combinations is labelled factorial, with its factors (02-audit, What code computes)."""
    d = unit_design(_rec(), "F1", stated_signatures(_rec(), "F1"))
    assert d.factorial and set(d.factors) == {"pacing", "culture_calcium_mM"}


def test_not_factorial_when_a_combination_is_missing():
    """Two fields not crossed in all combinations are not factorial (02-audit, What code computes)."""
    r = record()
    del r["units"]["F1"]["groups"]["LC_RP"]
    rec = Record.model_validate(r)
    assert not unit_design(rec, "F1", stated_signatures(rec, "F1")).factorial


def test_number_contrast_from_qualifiers():
    """Contrasts on a number come from the groups' quantities and qualifiers (03-vocabulary, Contrasts)."""
    r = record()
    g = r["units"]["F1"]["groups"]
    g["HC_RP"]["context"]["pacing"] = {"value": "electrical pacing", "qualifiers": {"frequency": "2 Hz"}}
    g["HC_NP"]["context"]["pacing"] = {"value": "electrical pacing", "qualifiers": {"frequency": "0.75 Hz"}}
    c = _contrast(Record.model_validate(r), ["HC_RP", "HC_NP"])
    assert c.fields == ["pacing"]


def test_omnibus_makes_no_pair():
    """An omnibus test gives no pairwise comparison; it lists the fields that vary (02-audit, One evidence item per printed test)."""
    c = _contrast(_rec(), ["HC_RP", "HC_NP", "LC_NP"], "omnibus")
    assert c.kind == "omnibus" and c.pairwise is False


def test_identical_groups_flagged():
    """A pair whose groups have identical context gives no contrast and is flagged (02-audit, What code computes)."""
    r = record()
    r["units"]["F1"]["groups"]["HC_NP"]["context"]["pacing"] = "ramp pacing"
    c = _contrast(Record.model_validate(r), ["HC_RP", "HC_NP"])
    assert c.fields == [] and c.problems


def _aliased_rec():
    r = record()
    for g, med in (("HC_NP", "DMEM"), ("HC_RP", "DMEM"), ("LC_NP", "RPMI"), ("LC_RP", "RPMI")):
        r["units"]["F1"]["groups"][g]["context"]["cm_medium"] = med
    return Record.model_validate(r)


def test_aliased_fields_labelled_in_confound():
    """A pair differing in two fields is still a confound; when those fields vary together across all the unit's groups, code labels them aliased (02-audit, What code computes)."""
    rec = _aliased_rec()
    c = _contrast(rec, ["HC_RP", "LC_RP"])
    assert c.confound and c.aliased and set(c.fields) == {"cm_medium", "culture_calcium_mM"}
    assert not _contrast(_rec(), ["HC_RP", "LC_NP"]).aliased


def test_factorial_with_aliased_compound_factor():
    """A unit whose groups cross a compound of aliased fields with another field in all combinations is factorial, the compound named as one factor (02-audit, What code computes)."""
    rec = _aliased_rec()
    d = unit_design(rec, "F1", stated_signatures(rec, "F1"))
    assert d.factorial and set(d.factors) == {"cm_medium+culture_calcium_mM", "pacing"}


def test_three_factor_factorial():
    """Groups crossing three fields in all combinations are factorial with three factors (02-audit, What code computes)."""
    r = record()
    gs = {}
    for ca in ("1.8 mM", "0.9 mM"):
        for pa in ("none", "ramp pacing"):
            for ld in ("1x", "8x"):
                gs[f"g{len(gs)}"] = {"label": f"{ca}-{pa}-{ld}", "context": {"culture_calcium_mM": ca, "pacing": pa,
                                                                            "platform": {"value": "strip", "qualifiers": {"load": ld}}}}
    r["units"]["F1"]["groups"] = gs
    r["default_context"].pop("platform")
    r["evidence"] = {}
    rec = Record.model_validate(r)
    d = unit_design(rec, "F1", stated_signatures(rec, "F1"))
    assert d.factorial and set(d.factors) == {"culture_calcium_mM", "pacing", "platform"}


def test_members_of_a_set_field_are_factors():
    """Groups that differ in which members a set-valued field holds (glucose, palmitate, insulin) are recognised as factorial on those members; each group's stated set is the complete list for that group (02-audit, What code computes)."""
    r = record()
    r["default_context"].update({"pacing": "none", "culture_calcium_mM": "1.8 mM"})
    sets = {"G": "glucose", "GI": "glucose + insulin", "GP": "glucose + palmitate", "GPI": "glucose + palmitate + insulin"}
    r["units"]["F1"]["groups"] = {k: {"label": k, "context": {"treatment": v}} for k, v in sets.items()}
    r["evidence"]["E1"].update({"compares": ["GI", "G"], "values": {}, "n": "not stated"})
    rec = Record.model_validate(r)
    signer = lambda at, f, v: ("terms", tuple(sorted(x.strip() for x in (v if isinstance(v, str) else v.value).split("+"))), ()) \
        if f == "treatment" else ("stated", v if isinstance(v, str) else v.value, ())
    sigs = stated_signatures(rec, "F1", signer)
    assert not unit_design(rec, "F1", sigs).factorial
    d = unit_design(rec, "F1", sigs, set_fields=("treatment",))
    assert d.factorial and set(d.factors) == {"treatment[insulin]", "treatment[palmitate]"}
