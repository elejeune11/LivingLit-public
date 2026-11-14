from livinglit.measures import new_terms_per_paper, refinements
from livinglit.mapping import Mapped


def test_new_terms_per_paper_from_log():
    """New terms per paper are counted by paper order from the log (03-vocabulary, How the vocabulary grows)."""
    log = [{"version": 1, "paper": "A", "events": [{"event": "add_term", "id": "p:x"}, {"event": "adopt", "id": "CHEBI:1"}]},
           {"version": 2, "paper": "B", "events": [{"event": "add_synonym", "id": "p:x", "text": "t"}]}]
    rows = new_terms_per_paper(log)
    assert [r["new_terms"] for r in rows] == [2, 0] and rows[1]["synonyms"] == 1


def test_refinement_list():
    """A new term lists earlier values under its parent as possible refinements, by paper (03-vocabulary, How the vocabulary grows)."""
    log = [{"version": 1, "paper": "A", "events": [{"event": "add_term", "id": "p:3d"}]},
           {"version": 2, "paper": "B", "events": [{"event": "add_term", "id": "p:mt", "parent": "p:3d"}]}]
    mapped = {"A": {"default_context.platform": Mapped("assigned", ["p:3d"], text="3D tissue")}, "B": {}}
    rows = refinements(log, None, mapped)
    assert rows == [{"new_term": "p:mt", "added_by": "B", "paper": "A", "at": "default_context.platform",
                     "stated": "3D tissue", "mapped_to": "p:3d"}]


def test_expressed_as_from_printed_unit():
    """When a measure's mapping does not say how it is expressed, code takes expressed_as from the value's printed unit ("% of baseline", "% change", "fold"; a physical unit is absolute), never from words elsewhere (03-vocabulary, Relative measures)."""
    from livinglit.audit import expressed_as_from_unit
    assert expressed_as_from_unit("% of baseline") == "% of baseline"
    assert expressed_as_from_unit("% change") == "% change"
    assert expressed_as_from_unit("ΔF/F0") == "% change" and expressed_as_from_unit("F/F0") == "fold"
    assert expressed_as_from_unit("a.u.") is None
    assert expressed_as_from_unit("fold") == "fold"
    assert expressed_as_from_unit("mN") == "absolute"  # a physical unit is an absolute value
    assert expressed_as_from_unit("%") is None


def test_value_level_normalisation_wins_over_mapping():
    """A value may carry expressed_as and normalised_to read from its own legend; code prefers them to the measure mapping's, so one wording normalised differently in two figures stays apart (03-vocabulary, Relative measures)."""
    from livinglit.models import Value
    from livinglit.audit import value_qualifiers
    v = Value.model_validate({"printed": "1.4", "unit": "fold", "group": "g", "expressed_as": "fold", "normalised_to": "GAPDH"})
    q = value_qualifiers({"expressed_as": "normalised", "normalised_to": "1x constrained"}, [v])
    assert q == {"expressed_as": "fold", "normalised_to": "GAPDH"}
    assert value_qualifiers({"level": "APD50"}, []) == {"level": "APD50"}
