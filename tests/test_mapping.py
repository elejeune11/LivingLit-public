from livinglit.models import Record, TermsFile
from livinglit.vocab import Vocabulary, FieldDecl, apply_version
from livinglit.mapping import map_record, signer, wording_copies
from livinglit.gate_terms import check_terms
from livinglit.groups import item_contrast, stated_signatures
from tests.helpers import record

FIELDS = {f: FieldDecl(f, "terms") for f in ["platform", "pacing"]}
FIELDS.update({f: FieldDecl(f, "quantity") for f in ["temperature", "day_of_measurement", "culture_calcium_mM"]})
FIELDS["measure"] = FieldDecl("measure", "measure")


def _vocab():
    v = Vocabulary(FIELDS)
    ev = [{"event": "add_term", "field": "platform", "id": "platform:micropillar", "label": "micropillar tissue", "definition": "d"},
          {"event": "add_term", "field": "pacing", "id": "pacing:none", "label": "none paced", "definition": "d", "scope": "s"},
          {"event": "add_term", "field": "pacing", "id": "pacing:ramp", "label": "ramp pacing", "definition": "d", "scope": "s"},
          {"event": "add_term", "field": "measure", "id": "measure:force", "label": "twitch force", "definition": "d",
           "dimension": "force"}]
    apply_version(v, {"version": 1, "paper": "P", "events": ev})
    return v


def _rec():
    return Record.model_validate(record())


def _tf(mappings, edits=()):
    return TermsFile.model_validate({"record": "2099_Synth", "vocabulary_version": 1, "mappings": mappings, "edits": list(edits)})


def test_matched_quantity_and_states():
    """Values are matched by code, parsed as quantities, or named states; matches are never stored (03-vocabulary, Mapping, and flags)."""
    m = map_record(_vocab(), _rec(), None)
    assert m["default_context.platform"].origin == "matched"
    assert m["default_context.temperature"].origin == "quantity"
    assert m["units.F1.groups.HC_NP.context.pacing"].origin == "none"
    assert m["evidence.E1.measure"].origin == "matched"


def test_gate_requires_every_value_mapped_or_flagged():
    """Every stated value is matched, mapped or flagged (03-vocabulary, How the vocabulary grows)."""
    r = record()
    r["default_context"]["platform"] = "3D CMT between pillars"
    rec = Record.model_validate(r)
    probs = check_terms(_vocab(), rec, _tf([]), found=lambda q: True, ontology=None)
    assert any("neither matched" in p for p in probs)
    ok = _tf([{"field": "platform", "stated": "3D CMT between pillars", "terms": ["platform:micropillar"]}])
    assert check_terms(_vocab(), rec, ok, found=lambda q: True, ontology=None) == []


def test_flagged_value_carries_no_terms():
    """A flagged value carries no terms and is not mapped (03-vocabulary, Mapping, and flags)."""
    import pytest
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        _tf([{"field": "platform", "stated": "x", "terms": ["platform:micropillar"],
              "flag": {"kind": "placeholder", "note": "n"}}])


def test_identical_text_mapped_once():
    """Identical stated text within a paper is mapped once and reused (03-vocabulary, How code matches)."""
    r = record()
    r["default_context"]["platform"] = "CMT"
    rec = Record.model_validate(r)
    m = {"field": "platform", "stated": "CMT", "terms": ["platform:micropillar"]}
    assert any("twice" in p for p in check_terms(_vocab(), rec, _tf([m, m]), found=lambda q: True, ontology=None))


def test_stored_match_refused():
    """A value code matches is never stored as a mapping (03-vocabulary, How code matches)."""
    tf = _tf([{"field": "platform", "stated": "micropillar tissue", "terms": ["platform:micropillar"]}])
    assert any("never stored" in p for p in check_terms(_vocab(), _rec(), tf, found=lambda q: True, ontology=None))


def test_contrast_on_mapped_terms():
    """Code computes contrasts on the groups' mapped terms (02-audit, What code computes)."""
    rec = _rec()
    sigs = stated_signatures(rec, "F1", signer(_vocab(), rec, None))
    c = item_contrast(rec, rec.evidence["E1"], sigs)
    assert c.fields == ["pacing"]


def test_wording_copies_reported():
    """Copies of one value that differ only in wording are reported back to the reader (03-vocabulary, How code matches; 08 decision 13)."""
    r = record()
    r["units"]["F2"] = {"where": "Fig. 2", "title": "t", "context": {"day_of_measurement": "day 14"}, "groups": {}}
    r["units"]["F1"]["context"]["day_of_measurement"] = "day 14"
    r["default_context"].pop("platform")
    r["units"]["F1"]["context"]["platform"] = "CMT"
    r["units"]["F2"]["context"]["platform"] = "micropillar tissue"
    rec = Record.model_validate(r)
    tf = _tf([{"field": "platform", "stated": "CMT", "terms": ["platform:micropillar"]}])
    copies = wording_copies(_vocab(), rec, map_record(_vocab(), rec, tf))
    assert copies and copies[0]["field"] == "platform"


def test_quantity_field_named_states():
    """A quantity field may have named states ('room temperature'), compared by identity (03-vocabulary, Fields and terms)."""
    from livinglit.mapping import Occurrence, map_occurrence
    v = _vocab()
    v.fields["temperature"].states = ["room temperature"]
    m = map_occurrence(v, Occurrence("default_context.temperature", "temperature", "Room temperature"), {})
    assert m.origin == "state" and m.text == "Room temperature"


def test_relative_measure_qualifiers_take_fixed_values():
    """Field-wide measure qualifiers (expressed_as, normalised_to, level) apply to every measure, and expressed_as takes one of its fixed values (03-vocabulary, Fields and terms)."""
    v = _vocab()
    v.measure_qualifiers = {"expressed_as": ["absolute", "% of baseline", "% change", "fold", "normalised"],
                            "normalised_to": None, "level": None}
    r = record()
    r["evidence"]["E1"]["measure"] = "force relative to baseline"
    rec = Record.model_validate(r)
    good = _tf([{"field": "measure", "stated": "force relative to baseline", "terms": ["measure:force"],
                 "qualifiers": {"expressed_as": "% of baseline", "normalised_to": "baseline"}}])
    assert check_terms(v, rec, good, found=lambda q: True, ontology=None) == []
    bad = _tf([{"field": "measure", "stated": "force relative to baseline", "terms": ["measure:force"],
                "qualifiers": {"expressed_as": "percent of control"}}])
    assert any("expressed_as" in p for p in check_terms(v, rec, bad, found=lambda q: True, ontology=None))


def test_declared_state_on_a_terms_field():
    """A field of terms may declare named states (genotype: healthy control line); code matches them, two equal states compare same, and a state against a term is unknown, not a conflict (03-vocabulary, Fields and terms)."""
    from livinglit.matching import compare_terms
    from livinglit.audit import mapped_side
    from livinglit.mapping import map_occurrence, Occurrence
    v = _vocab()
    v.fields["genotype"] = FieldDecl("genotype", "terms", states=["healthy control line"])
    apply_version(v, {"version": 2, "paper": "P", "events": [
        {"event": "add_term", "field": "genotype", "id": "genotype:wild_type", "label": "wild type", "definition": "d"}]})
    m = map_occurrence(v, Occurrence("x", "genotype", "Healthy control line"), {})
    assert m.origin == "state"
    s = mapped_side(m)
    assert compare_terms(v, "genotype", s, s) == "same"
    r = compare_terms(v, "genotype", s, mapped_side(map_occurrence(v, Occurrence("y", "genotype", "wild type"), {})))
    from livinglit.across import is_unknown
    assert is_unknown(f"genotype: {r}")


def test_flag_on_a_declared_state_refused():
    """A value code matches as a declared state is not flagged: the stored flag is refused (03-vocabulary, Mapping, and flags)."""
    v = _vocab()
    v.fields["temperature"] = FieldDecl("temperature", "quantity", states=["room temperature"])
    r = record()
    r["default_context"]["temperature"] = "room temperature"
    rec = Record.model_validate(r)
    tf = _tf([{"field": "temperature", "stated": "room temperature", "flag": {"kind": "not a context", "note": "n"}}])
    assert any("declared state" in p for p in check_terms(v, rec, tf, found=lambda q: True, ontology=None))
