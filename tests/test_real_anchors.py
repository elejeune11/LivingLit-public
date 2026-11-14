import pytest
import yaml

from livinglit import ROOT, PAPERS_DIR
from livinglit.text import find_quote

PAPERS = ["2018_Ronaldson-Bouchard", "2020_Saleem-U", "2021_Zhang", "2021_Bliley", "2022_Shen"]


@pytest.mark.papers
@pytest.mark.parametrize("paper", PAPERS)
def test_first_build_anchors_found(paper):
    """The quote matcher finds the first build's evidence anchors in the real papers (02-audit, Quote matching; 07-building, Build order step 0)."""
    rec = yaml.safe_load((ROOT / "archive/v5_code/records" / paper / "record.yaml").read_text())
    quotes = [e["anchor"]["quote"] for e in rec["evidence"].values()
              if isinstance(e.get("anchor"), dict) and e["anchor"].get("quote") and e["anchor"].get("kind", "text") == "text"]
    quotes = list(dict.fromkeys(quotes))[:80]
    missing = [q for q in quotes if find_quote(q, PAPERS_DIR / paper) is None]
    assert len(missing) <= 0.05 * len(quotes), missing[:5]
