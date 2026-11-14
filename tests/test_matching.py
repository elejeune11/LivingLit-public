from livinglit.vocab import Vocabulary, FieldDecl, apply_version
from livinglit.matching import match_text, compare_terms, compare_qualifiers, Side

FIELDS = {"platform": FieldDecl("platform", "terms"), "substrate": FieldDecl("substrate", "terms")}


def _v():
    v = Vocabulary(FIELDS)
    ev = []
    for tid, label, parent, syns in [
        ("platform:3d", "3D", None, []), ("platform:2d", "2D", None, ["monolayer culture"]),
        ("platform:eht", "anchored EHT", "platform:3d", []),
        ("platform:micropillar", "micropillar tissue", "platform:eht", ["CMT", "cardiac microtissue"]),
        ("platform:strip", "strip between posts", "platform:eht", []),
        ("substrate:fibrin", "fibrin", None, []), ("substrate:matrigel", "Matrigel", None, []),
        ("substrate:pdms", "PDMS", None, ["polydimethylsiloxane and silicone"])]:
        ev.append({"event": "add_term", "field": tid.split(":")[0], "id": tid, "label": label, "parent": parent,
                   "definition": "d", "scope": "s", "synonyms": [{"text": s} for s in syns]})
    apply_version(v, {"version": 1, "paper": "P", "events": ev})
    return v


def test_every_part_must_match():
    """Every part of the stated text must equal a synonym or label to be matched; a leftover sends it to the agent (03-vocabulary, How code matches)."""
    v = _v()
    assert match_text(v, "substrate", "fibrin + Matrigel").terms == {"substrate:fibrin", "substrate:matrigel"}
    assert match_text(v, "substrate", "fibrin + collagen").terms is None
    assert match_text(v, "substrate", "fibrin + collagen").leftover == ["collagen"]


def test_ancestors_dropped():
    """Ancestors are dropped: '3D CMT' gives {3D, micropillar tissue}, which reduces to micropillar tissue (03-vocabulary, How code matches)."""
    assert match_text(_v(), "platform", "3D CMT").terms == {"platform:micropillar"}


def test_multiword_synonyms_first():
    """Multi-word synonyms are matched before splitting on separators such as 'and' (03-vocabulary, How code matches)."""
    assert match_text(_v(), "substrate", "polydimethylsiloxane and silicone").terms == {"substrate:pdms"}


def test_case_and_punctuation_normalised():
    """Matching is on normalized text (03-vocabulary, How code matches)."""
    assert match_text(_v(), "platform", "Cardiac Micro-tissue").terms == {"platform:micropillar"}


def test_compare_same_and_levels():
    """same, same at level k, narrower/broader and differ follow the tree (03-vocabulary, Comparing on terms)."""
    v = _v()
    S = lambda *t: Side(terms=set(t))
    assert compare_terms(v, "platform", S("platform:micropillar"), S("platform:micropillar")) == "same"
    assert compare_terms(v, "platform", S("platform:micropillar"), S("platform:strip"), level=2) == "same at level 2"
    assert compare_terms(v, "platform", S("platform:micropillar"), S("platform:strip")) == "differ"
    assert compare_terms(v, "platform", S("platform:micropillar"), S("platform:eht")) == "narrower / broader"
    assert compare_terms(v, "platform", S("platform:micropillar"), S("platform:2d"), level=1) == "differ"


def test_not_stated_unmapped_flagged():
    """not stated, unmapped and flagged are distinct results; unmapped and flagged mean cannot compare, not differ (03-vocabulary, Comparing on terms)."""
    v = _v()
    a = Side(terms={"platform:2d"})
    assert compare_terms(v, "platform", a, Side(state="not stated")) == "not stated"
    assert compare_terms(v, "platform", a, Side(state="unmapped")) == "unmapped"
    assert compare_terms(v, "platform", a, Side(state="flagged", flag="several conditions")) == "flagged"


def test_qualifiers_compared_at_printed_precision():
    """Qualifiers are compared after terms, at printed precision (03-vocabulary, Comparing on terms)."""
    assert compare_qualifiers({"stiffness": "8 kPa"}, {"stiffness": "8.0 kPa"}) == "same"
    assert compare_qualifiers({"frequency": "2 Hz"}, {"frequency": "0.75 Hz"}) == "differ"
    assert compare_qualifiers({"frequency": "1 Hz"}, {"frequency": "60 bpm"}) == "same"
    assert compare_qualifiers({"frequency": "1 Hz"}, {}) == "not stated"


def test_quantity_written_in_words():
    """A quantity printed with its number in words ('four weeks') parses as a quantity, as printed (03-vocabulary, Fields and terms)."""
    from livinglit.matching import quantity_value
    assert quantity_value("four weeks") is not None and quantity_value("four weeks")[0] == 4
    assert quantity_value("confluent") is None


def test_text_qualifiers_not_compared_by_digits():
    """Qualifiers that are names (genes such as DSC2 and PKP2) are compared as text, never by the digits in them (03-vocabulary, Comparing on terms)."""
    assert compare_qualifiers({"gene": "DSC2"}, {"gene": "PKP2"}) == "differ"
    assert compare_qualifiers({"gene": "MYH6"}, {"gene": "MYH7"}) == "differ"
    assert compare_qualifiers({"gene": "MYH7"}, {"gene": "myh7"}) == "same"
