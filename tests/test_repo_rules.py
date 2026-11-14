import re
import subprocess
from pathlib import Path

from livinglit import ROOT

CANARIES = ["Sythemax", "XAY939"]


def _tracked():
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    return [ROOT / p for p in out]


def test_no_papers_or_figures_committed():
    """Papers, figures and overlays are never committed; nothing with dont_commit in its name is tracked (CONTRIBUTING, Fixed rules)."""
    bad = [p for p in _tracked() if "dont_commit" in p.name or "dont_ever_commit" in str(p)
           or (p.suffix.lower() in (".pdf", ".xlsx", ".xls", ".docx", ".png", ".jpg", ".tif")
               and "docs/" not in str(p.relative_to(ROOT)) and "archive/" not in str(p.relative_to(ROOT)))]
    assert bad == []


def test_no_canary_in_fields():
    """No validation-study canary appears in fields/ (09-first-corpus, The curated table stays out)."""
    hits = []
    for p in (ROOT / "fields").rglob("*"):
        if p.is_file():
            t = p.read_text(errors="ignore")
            hits += [(p, c) for c in CANARIES if c.lower() in t.lower()]
    assert hits == []


def test_figures_library_holds_no_figure_specifics():
    """src/livinglit/figures/ offers shared parts only and never holds a crop, page, colour, group label or axis range (CONTRIBUTING, Fixed rules)."""
    pat = re.compile(r"crop\s*=\s*\(?\s*\d|page\s*=\s*\d|#[0-9a-fA-F]{6}\b|\bylim\s*=|\bxlim\s*=|"
                     r"\b(HC|LC)[-_](RP|NP)\b|axis_range\s*=\s*\(", re.I)
    hits = [(p.name, m.group(0)) for p in (ROOT / "src" / "livinglit" / "figures").rglob("*.py")
            for m in pat.finditer(p.read_text())]
    assert hits == []


def test_no_long_quotes_in_records():
    """Records hold short quotes only: at most 30 words (02-audit, Quote matching; CONTRIBUTING, Fixed rules)."""
    import yaml
    long = []
    for p in (ROOT / "records").glob("*/record.yaml"):
        def walk(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k == "quote" and isinstance(v, str) and len(v.split()) > 30:
                        long.append((p.parent.name, v[:40]))
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(yaml.safe_load(p.read_text()))
    assert long == []
