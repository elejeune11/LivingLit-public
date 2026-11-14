from livinglit.gate_record import check_record
from tests.helpers import record

CFG = {"fields": {f: {"kind": "quantity"} for f in ["platform", "temperature", "day_of_measurement", "culture_calcium_mM", "pacing"]}}
TEXT = ("Results. ramp pacing increased twitch force in all tissues. Methods. temperature was 37 C.")


def _paper(tmp_path):
    (tmp_path / "main.txt").write_text(TEXT)
    return tmp_path


def test_record_gate_passes(tmp_path):
    """A record whose anchors are found and whose fields are filled passes its gate (07-building, Jobs)."""
    rec, probs = check_record(record(), _paper(tmp_path), CFG)
    assert probs == []


def test_unfound_anchor_fails(tmp_path):
    """Every item is anchored: a quote found in the normalized text (02-audit, Anchors and origins)."""
    r = record()
    r["evidence"]["E1"]["anchor"]["quote"] = "ramp pacing doubled force"
    _, probs = check_record(r, _paper(tmp_path), CFG)
    assert any("not found" in p for p in probs)


def test_long_quote_fails(tmp_path):
    """Quotes are at most 30 words (02-audit, Quote matching)."""
    r = record()
    r["evidence"]["E1"]["anchor"]["quote"] = " ".join(["word"] * 31)
    _, probs = check_record(r, _paper(tmp_path), CFG)
    assert any("at most 30" in p for p in probs)


def test_every_field_filled_or_not_stated(tmp_path):
    """Every context field is filled or marked 'not stated' (02-audit, Status and depth; 07-building, Jobs)."""
    cfg = {"fields": {**CFG["fields"], "substrate": {"kind": "terms"}}}
    _, probs = check_record(record(), _paper(tmp_path), cfg)
    assert any("substrate" in p for p in probs)


def test_unknown_field_fails(tmp_path):
    """Context fields are the vocabulary's declared fields (03-vocabulary, Fields and terms)."""
    r = record()
    r["default_context"]["colour"] = "blue"
    _, probs = check_record(r, _paper(tmp_path), CFG)
    assert any("colour" in p for p in probs)


def test_image_only_anchor(tmp_path):
    """Values inside an image are anchored to their unit and say so (02-audit, Quote matching)."""
    r = record()
    r["evidence"]["E1"]["anchor"] = {"quote": "value in an image-only table", "where": "Table 1", "kind": "unit"}
    _, probs = check_record(r, _paper(tmp_path), CFG)
    assert probs == []


def test_benchmark_group_needs_only_its_own_fields(tmp_path):
    """A native or other-study group states only what the source says; code supplies 'not stated in this source' for every other field (02-audit, Groups)."""
    r = record()
    r["units"]["F1"]["groups"]["ADULT"] = {"label": "adult", "kind": "native tissue", "context": {"platform": "native tissue"}}
    r["evidence"]["E2"] = {**r["evidence"]["E1"], "compares": ["HC_RP", "ADULT"], "values": {}, "n": "not stated"}
    _, probs = check_record(r, _paper(tmp_path), CFG)
    assert probs == []


def test_field_added_after_the_record_is_not_yet_read(tmp_path):
    """Open world: a field added to the field set after a record was written resolves to 'not yet read' and does not fail that record's gate; records written for the new set must fill it (02-audit, Context per unit; 03-vocabulary, Fields and terms)."""
    cfg = {"fields": {**CFG["fields"], "species": {"kind": "terms", "since": 2}}, "field_set": 2}
    rec, probs = check_record(record(), _paper(tmp_path), cfg)
    assert probs == []
    r = record()
    r["field_set"] = 2
    rec, probs = check_record(r, _paper(tmp_path), cfg)
    assert any("species" in p for p in probs)


ANCHORED_TEXT = TEXT + (" Tissues formed between micropillar posts and were cultured in 1.8 mM calcium or 0.9 mM calcium,"
                        " unpaced or with ramp pacing, and measured on day 14. Plates were coated with gelatin.")


def _anchored(**over):
    r = record()
    r["field_set"] = 3
    vals = [("platform", "micropillar tissue", "Tissues formed between micropillar posts"),
            ("temperature", "37 C", "temperature was 37 C"),
            ("day_of_measurement", "day 14", "measured on day 14"),
            ("culture_calcium_mM", "1.8 mM", "cultured in 1.8 mM calcium"),
            ("culture_calcium_mM", "0.9 mM", "or 0.9 mM calcium"),
            ("pacing", "ramp pacing", "unpaced or with ramp pacing")]
    r["context_anchors"] = [{"field": f, "value": v, "anchor": {"quote": q, "where": "Methods"}} for f, v, q in vals]
    r["units"]["F1"]["groups"]["HC_NP"]["context"]["pacing"] = "not stated"
    r["units"]["F1"]["groups"]["LC_NP"]["context"]["pacing"] = "not stated"
    r.update(over)
    return r


def test_context_anchors_pass_when_every_distinct_value_is_quoted(tmp_path):
    """From field set 3, each distinct stated context value carries one anchor whose quote holds its words and numbers; 'not stated' needs none (02-audit, Context is anchored too)."""
    (tmp_path / "main.txt").write_text(ANCHORED_TEXT)
    _, probs = check_record(_anchored(), tmp_path, CFG)
    assert probs == []


def test_unanchored_or_unheld_context_value_fails(tmp_path):
    """A stated context value without an anchor, or whose quote does not hold its words, fails the gate (02-audit, Context is anchored too)."""
    (tmp_path / "main.txt").write_text(ANCHORED_TEXT)
    r = _anchored()
    r["context_anchors"] = [a for a in r["context_anchors"] if a["value"] != "0.9 mM"]
    r["context_anchors"][0]["anchor"]["quote"] = "Plates were coated with gelatin"
    _, probs = check_record(r, tmp_path, CFG)
    assert any("culture_calcium_mM" in p and "0.9 mM" in p and "no anchor" in p for p in probs)
    assert any("platform" in p and "does not hold" in p for p in probs)


def test_context_anchors_not_required_before_field_set_3(tmp_path):
    """Records read against an earlier field set keep passing without context anchors (03-vocabulary, Field sets; 02-audit, Context is anchored too)."""
    rec, probs = check_record(record(), _paper(tmp_path), CFG)
    assert probs == []


def test_other_conditions_are_anchored_and_held(tmp_path):
    """Conditions recorded in other_conditions carry a quote that holds their words, checked like context anchors (03-vocabulary, Fields are designed from the corpus)."""
    (tmp_path / "main.txt").write_text(ANCHORED_TEXT)
    r = _anchored()
    r["units"]["F1"]["other_conditions"] = [{"text": "gelatin coating", "anchor": {"quote": "Plates were coated with gelatin", "where": "Methods"}}]
    _, probs = check_record(r, tmp_path, CFG)
    assert any("other_conditions" in p and "does not hold" in p for p in probs)
    r["units"]["F1"]["other_conditions"][0]["text"] = "plates coated with gelatin"
    _, probs = check_record(r, tmp_path, CFG)
    assert probs == []


def test_every_file_in_the_papers_folder_is_read_or_explained(tmp_path):
    """Readers read every supplement: each file in the paper's folder is in source.files or in source.not_used with what it holds; folders are skipped (02-audit, What a record holds; CONTRIBUTING, Working here)."""
    _paper(tmp_path)
    (tmp_path / "supplement.pdf").write_text("x")
    (tmp_path / "pages_dont_commit").mkdir()
    _, probs = check_record(record(), tmp_path, CFG)
    assert any("supplement.pdf" in p and "not read" in p for p in probs)
    r = record()
    r["source"]["not_used"] = [{"file": "supplement.pdf", "why": "peer review file: no results"}]
    _, probs = check_record(r, tmp_path, CFG)
    assert probs == []
