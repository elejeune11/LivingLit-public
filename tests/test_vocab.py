import pytest

from livinglit.vocab import Vocabulary, check_edits, apply_version, rebuild, FieldDecl


FIELDS = {"platform": FieldDecl("platform", "terms"), "substrate": FieldDecl("substrate", "terms"),
          "treatment": FieldDecl("treatment", "adopted", ontology="chebi"),
          "differentiation_factors": FieldDecl("differentiation_factors", "adopted", ontology="chebi"),
          "measure": FieldDecl("measure", "measure")}
TEXT = "we built 3D tissues; the micropillar tissue (CMT) was soft. CHIR99021 at 6 uM. fibrin gel was used"


class FakeOntology:
    known = {"CHEBI:1": ("CHIR99021", False), "CHEBI:2": ("old thing", True)}

    def check(self, oid):
        if oid not in self.known:
            return None
        label, obsolete = self.known[oid]
        return {"label": label, "obsolete": obsolete}

    def ancestors(self, oid):
        return set()


def found(quote):
    from livinglit.text import normalize
    return normalize(quote) in normalize(TEXT)


def add(id, label, parent=None, field="platform", synonyms=(), scope=None, definition="d"):
    return {"add_term": {"field": field, "id": id, "label": label, "parent": parent, "definition": definition,
                         "scope": scope, "synonyms": [{"text": s, "anchor": s} for s in synonyms]}}


def _check(edits, vocab=None):
    return check_edits(vocab or Vocabulary(FIELDS), edits, found=found, ontology=FakeOntology(), paper="P1")


def test_add_term_ok():
    """A new term has a field:slug id, a definition and an anchored synonym (03-vocabulary, Fields and terms)."""
    assert _check([add("platform:3d", "3D", synonyms=["3D tissues"])]) == []


def test_synonym_must_be_found_in_paper():
    """Every new synonym is found in this paper's text at its anchor (03-vocabulary, How the vocabulary grows)."""
    probs = _check([add("platform:3d", "3D", synonyms=["engineered heart tissue"])])
    assert any("not found" in p for p in probs)


def test_parent_exists_same_field():
    """The parent exists in the same field (03-vocabulary, Fields and terms)."""
    probs = _check([add("platform:mt", "micropillar tissue", parent="platform:nope", scope="s")])
    assert any("parent" in p for p in probs)
    probs = _check([add("substrate:x", "x"), add("platform:mt", "mt", parent="substrate:x")])
    assert any("parent" in p for p in probs)


def test_scope_needed_with_siblings():
    """A term needs a scope note when it has siblings, checked after the job (03-vocabulary, Fields and terms)."""
    probs = _check([add("platform:3d", "3D"), add("platform:a", "a", "platform:3d"), add("platform:b", "b", "platform:3d")])
    assert sum("scope" in p for p in probs) == 2
    ok = _check([add("platform:3d", "3D"), add("platform:a", "a", "platform:3d", scope="s"),
                 add("platform:b", "b", "platform:3d", scope="s")])
    assert ok == []


def test_no_collision():
    """No label or synonym collides with another term's in the field (03-vocabulary, Fields and terms)."""
    probs = _check([add("platform:3d", "3D"), add("platform:3dx", "3D", scope="s")])
    assert any("collides" in p for p in probs)


def test_ids_never_reused():
    """Ids are unique and never reused (03-vocabulary, Fields and terms)."""
    v = Vocabulary(FIELDS)
    apply_version(v, {"version": 1, "paper": "P0", "events": [{"event": "add_term", **add("platform:3d", "3D")["add_term"]}]})
    assert any("already" in p for p in _check([add("platform:3d", "three D")], v))


def test_adopted_id_checked_against_pinned_release():
    """An adopted id must exist in the pinned ontology release and not be obsolete (03-vocabulary, Adopted ontologies; 08 decision 18)."""
    ad = lambda oid, label: {"adopt": {"field": "treatment", "id": oid, "label": label, "lookup": "search CHIR"}}
    assert _check([ad("CHEBI:1", "CHIR99021")]) == []
    assert any("not in the pinned" in p for p in _check([ad("CHEBI:9", "x")]))
    assert any("obsolete" in p for p in _check([ad("CHEBI:2", "old thing")]))


def test_one_ontology_id_several_fields():
    """One ontology id may serve several fields; a second adopt adds the field and the id stays one term (03-vocabulary, Adopted ontologies)."""
    v = Vocabulary(FIELDS)
    ev = lambda f: {"event": "adopt", "field": f, "id": "CHEBI:1", "label": "CHIR99021", "lookup": "s"}
    apply_version(v, {"version": 1, "paper": "P0", "events": [ev("treatment")]})
    assert _check([{"adopt": {"field": "differentiation_factors", "id": "CHEBI:1", "label": "CHIR99021", "lookup": "s"}}], v) == []
    apply_version(v, {"version": 2, "paper": "P1", "events": [ev("differentiation_factors")]})
    assert v.terms["CHEBI:1"].fields == ["treatment", "differentiation_factors"]


def test_adopt_own_needs_lookup_note():
    """adopt_own adds an own term inside an adopted field, with a note of what was searched (03-vocabulary, Adopted ontologies)."""
    e = {"adopt_own": {"field": "treatment", "id": "treatment:none", "label": "none", "definition": "no treatment",
                       "lookup": ""}}
    assert any("lookup" in p for p in _check([e]))
    e["adopt_own"]["lookup"] = "searched ChEBI for 'vehicle'; not a compound"
    assert _check([e]) == []


def test_own_term_in_adopted_field_refused():
    """An adopted field takes no invented add_term; own states go through adopt_own (03-vocabulary, Adopted ontologies)."""
    assert any("adopted" in p for p in _check([add("treatment:x", "x", field="treatment")]))


def test_rebuild_from_log(tmp_path):
    """vocab.yaml is rebuilt from the append-only changes.yaml log; a version with nothing new adds no version (03-vocabulary, How the vocabulary grows; 07-building)."""
    log = [{"version": 1, "paper": "P0", "events": [{"event": "add_term", **add("platform:3d", "3D")["add_term"]}]},
           {"version": 2, "paper": "P1", "events": [{"event": "add_synonym", "id": "platform:3d", "text": "3D tissues",
                                                     "anchor": "3D tissues"}]}]
    v = rebuild(FIELDS, log)
    assert v.version == 2 and v.lexicon("platform")["3dtissues"] == "platform:3d"


def test_canary_refused():
    """No validation-study canary enters the vocabulary (03-vocabulary, How the vocabulary grows)."""
    probs = _check([add("substrate:s", "Sythemax", field="substrate")])
    assert any("canary" in p for p in probs)


def test_synonym_not_broader_label_warning():
    """A synonym is the paper's name for exactly this term: one wording belongs to one term (03-vocabulary, Mapping, and flags)."""
    v = Vocabulary(FIELDS)
    apply_version(v, {"version": 1, "paper": "P0", "events": [{"event": "add_term", **add("platform:3d", "3D")["add_term"]}]})
    probs = _check([{"add_synonym": {"id": "platform:3d", "text": "3D", "anchor": "3D tissues"}}], v)
    assert any("collides" in p or "already" in p for p in probs)


def test_key_accepts_qualifier_on_ancestor():
    """A standing key may name a measure qualifier declared on the measure or an ancestor (05-across-sources, Standing keys)."""
    v = Vocabulary(FIELDS)
    apply_version(v, {"version": 1, "paper": "P", "events": [
        {"event": "add_term", "field": "measure", "id": "measure:expr", "label": "expression", "definition": "d",
         "dimension": "dimensionless", "qualifiers": {"gene": {"dimension": "text"}}},
        {"event": "add_term", "field": "measure", "id": "measure:fold", "label": "fold change", "parent": "measure:expr",
         "definition": "d", "dimension": "dimensionless"}]})
    from livinglit.vocab import check_key
    assert check_key(v, {"measure": "measure:fold", "value": {"must_match": ["measure.gene"]},
                         "direction": {"must_match": ["contrast", "measure.gene"]}}) == []


def test_rename_field_is_a_logged_event():
    """A field renamed by a person's decision is a logged event that renames it in standing keys and terms, so the vocabulary is still rebuilt from its log (03-vocabulary, How the vocabulary grows)."""
    fields = {**FIELDS, "media_calcium_mM": FieldDecl("media_calcium_mM", "quantity"),
              "culture_calcium_mM": FieldDecl("culture_calcium_mM", "quantity")}
    log = [{"version": 1, "paper": "P1", "events": [
        {"event": "standing_key", "measure": "measure:force",
         "value": {"must_match": ["platform@1", "media_calcium_mM"]}, "direction": {"must_match": ["contrast"]}}]},
        {"version": 2, "paper": None, "events": [
            {"event": "rename_field", "old": "media_calcium_mM", "new": "culture_calcium_mM", "reason": "decision 25"}]}]
    v = rebuild(fields, log)
    assert v.keys["measure:force"].value.must_match == ["platform@1", "culture_calcium_mM"]
    assert "media_calcium_mM" not in v.fields


def test_remap_applies_only_edits_not_yet_logged():
    """A re-map's terms.yaml may hold edits already in the log and new ones; only edits not yet logged for the paper are checked and appended (03-vocabulary, Earlier papers)."""
    from livinglit.gate_terms import pending_edits
    old = add("platform:3d", "3D tissue", synonyms=["3D tissues"])
    new = add("platform:cmt", "micropillar tissue", parent="platform:3d", scope="s")
    log = [{"version": 1, "paper": "P1", "events": [{"event": "add_term", **old["add_term"]}]}]
    assert pending_edits([old, new], log, "P1") == [new]
    assert pending_edits([new], log, "P2") == [new]
