"""Test conventions (07-building, Test-driven development).

Every test's docstring names its rule in one sentence and cites its source
document, e.g. "(02-audit, Anchors and origins)"; collection fails otherwise.
Tests marked ``papers`` are skipped when papers_dont_ever_commit/ is absent, and tests marked ``ontologies``
(a release of the real field re-checks its adopted ids) when the pinned ontology files are.
"""
import re

import pytest

from livinglit import ONTOLOGY_DIR, PAPERS_DIR

DOC_CITATION = re.compile(r"\((0[1-9]-[a-z][a-z-]*|README|CONTRIBUTING)\b[^)]*\)")


def cites_a_doc(doc):
    return bool(doc and DOC_CITATION.search(doc))


def pytest_collection_modifyitems(config, items):
    bad = [i.nodeid for i in items if isinstance(i, pytest.Function)
           and not cites_a_doc(getattr(i.function, "__doc__", None))]
    if bad:
        raise pytest.UsageError("Every test needs a docstring naming its rule and source document, e.g. "
                                "'(02-audit, Anchors and origins)'. Missing or uncited:\n  " + "\n  ".join(bad))
    if not PAPERS_DIR.is_dir():
        skip = pytest.mark.skip(reason="papers not present")
        for item in items:
            if "papers" in item.keywords:
                item.add_marker(skip)
    if not (ONTOLOGY_DIR / "chebi_core.obo.gz").exists():
        skip = pytest.mark.skip(reason="pinned ontology files not present")
        for item in items:
            if "ontologies" in item.keywords:
                item.add_marker(skip)
