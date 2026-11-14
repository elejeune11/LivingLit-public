"""The explorer: one page that shows a release by question, down to each result (06-releases, The explorer)."""
import json
import re

import pytest


def _release(tmp_path):
    from livinglit.release import build
    from tests.test_across import _write
    recs = tmp_path / "records"
    recs.mkdir()
    _write(recs, "P1")
    _write(recs, "P2", platform="strip")
    build("t", records_dir=recs, out_root=tmp_path / "rel", papers_dir=tmp_path)
    return tmp_path / "rel" / "t"


@pytest.mark.ontologies
def test_release_writes_one_explorer_page_with_results_beside_it(tmp_path):
    """A release writes one explorer page from its own tables, as a standalone page and as a body without document tags, and each paper's result details in their own file beside it (06-releases, The explorer)."""
    out = _release(tmp_path)
    page, body = (out / "explorer.html").read_text(), (out / "explorer_artifact.html").read_text()
    assert page.startswith("<!doctype html>") and "<body>" in page
    assert "<html" not in body and "<head>" not in body and "<title>" in body
    for text in (page, body):
        assert "/*DATA*/" not in text and '"P1"' in text and '"tag":"t"' in text
    assert not (out / "atlas.html").exists()
    js = (out / "explorer_data" / "items_P1.js").read_text()
    assert js.startswith("window.LL_ITEMS = window.LL_ITEMS || {};") and '"P1/' in js and '"P2/' not in js
    item = json.loads(js.split("Object.assign(window.LL_ITEMS, ", 1)[1].rsplit(");", 1)[0])
    one = next(iter(item.values()))
    for k in ("values", "checks", "chains", "map", "anchor", "status"):
        assert k in one, k


@pytest.mark.ontologies
def test_explorer_context_fields_come_from_the_release(tmp_path):
    """The explorer takes the context fields it highlights and links papers by from the release's data, not from a list in code: a field is offered only when its stated values differ between groups (CONTRIBUTING, Fixed rules)."""
    from livinglit.explorer import pack
    d = pack(_release(tmp_path))
    assert "platform" not in d["CTX"] and len(d["CTX"]) <= 7  # 'unmapped' in every group: nothing to highlight
    assert set(d["CTXP"]) <= {k for r in d["NS"] for k in r[:1]}  # graph layers are fields the values state


def test_explorer_template_and_code_hold_no_field_content():
    """The explorer template and its code are generic: no field name, field term or paper is written into them (CONTRIBUTING, Fixed rules)."""
    from livinglit import explorer
    from pathlib import Path
    for text in (explorer.TEMPLATE.read_text(), Path(explorer.__file__).read_text()):
        t = text.lower()
        for word in ("hipsc", "cardiomyocyte", "pacing", "cell_line", "stromal", "maturation_strategy", "ronaldson",
                     "platform", "treatment"):
            assert not re.search(rf"(?<![\w-]){word}(?![\w-])", t), word


def test_explorer_data_escapes_closing_tags():
    """Release text that contains '</script>' cannot end the page's script early (06-releases, The explorer)."""
    from livinglit.explorer import render
    body = render({"tag": "t", "note": "a </script> b"})
    assert "</script> b" not in body and json.loads(re.search(r"const D = (\{.*?\});\n", body).group(1).replace("<\\/", "</"))["note"] == "a </script> b"


def test_explorer_opens_each_result_from_its_papers_file():
    """Every result in the explorer opens on its own page (values, checks, derivations, resolved context), loaded from its paper's file only when asked for (06-releases, The explorer)."""
    from livinglit.explorer import TEMPLATE
    t = TEMPLATE.read_text()
    assert "#result/" in t and "explorer_data/items_" in t
    for section in ("Checks run by code", "Derivations", "Values", "Context, resolved by code"):
        assert section in t, section


@pytest.mark.ontologies
def test_explorer_opens_with_the_field_cover(tmp_path):
    """The explorer opens with a cover: LivingLit's whole-plan diagram, and the field's source review with its citation and summary, read from fields/<field>/cover.yaml through the release (06-releases, The explorer; CONTRIBUTING, Fixed rules)."""
    import yaml
    from livinglit.explorer import pack, render
    from livinglit import FIELDS_DIR
    out = _release(tmp_path)
    field_cover = yaml.safe_load((FIELDS_DIR / "hipsc_cm" / "cover.yaml").read_text())
    assert yaml.safe_load((out / "cover.yaml").read_text()) == field_cover
    for k in ("authors", "title", "journal", "year", "doi"):
        assert field_cover["citation"][k]
    assert 2 <= field_cover["summary"].count(". ") + 1 <= 3
    d = pack(out)
    assert d["COVER"]["citation"]["doi"] == field_cover["citation"]["doi"]
    assert d["COVER"]["image"].startswith("data:image/png;base64,")
    assert 'id="cover"' in render(d)
    (out / "cover.yaml").unlink()
    assert pack(out)["COVER"] is None


def test_site_folder_is_ready_for_static_hosting(tmp_path):
    """`livinglit site` copies a release's explorer into a folder a static host serves as is: the page as index.html, its per-paper files, and .nojekyll, replacing what was there (06-releases, The explorer)."""
    from livinglit.explorer import make_site
    rel = tmp_path / "rel"
    (rel / "explorer_data").mkdir(parents=True)
    (rel / "explorer.html").write_text("<!doctype html><title>explorer</title>")
    (rel / "explorer_data" / "items_P1.js").write_text("x")
    site = tmp_path / "site"
    (site / "explorer_data").mkdir(parents=True)
    (site / "explorer_data" / "items_OLD.js").write_text("old")
    (site / "explorer.html").write_text("an old second page")
    files = make_site(rel, site)
    assert (site / "index.html").read_text() == (rel / "explorer.html").read_text()
    assert not (site / "explorer.html").exists()
    assert (site / "explorer_data" / "items_P1.js").exists() and not (site / "explorer_data" / "items_OLD.js").exists()
    assert (site / ".nojekyll").exists() and "index.html" in files and "explorer_data/items_P1.js" in files


def test_explorer_says_it_is_agent_made_and_unreviewed():
    """The explorer carries a work-in-progress notice: results are produced by LLM agent jobs, checked by code, not yet reviewed by people (06-releases, The explorer)."""
    from livinglit.explorer import TEMPLATE
    html = TEMPLATE.read_text(encoding="utf-8")
    assert 'class="notice" role="note"' in html
    assert "Work in progress:" in html and "LLM agent" in html and "not yet reviewed by people" in html
