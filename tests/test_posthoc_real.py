"""Each new statistical check reproduces a consistent printed P before it is trusted (02-audit, Not the paper's error)."""
import pytest

from livinglit import RECORDS_DIR
from livinglit.checks import check_item
from livinglit.formulas import load_library
from livinglit.gate_record import load_record_files


def _verdicts(entry_word):
    lib = load_library()
    out = []
    for d in sorted(RECORDS_DIR.iterdir()):
        if not (d / "record.yaml").exists():
            continue
        rec, figs, rd, data = load_record_files(d.name)
        for iid in rec.evidence:
            for c in check_item(rec, iid, lib, data.data, rd.readings, figs):
                if c.check == "points to P" and c.entry and entry_word in c.entry:
                    out.append(c.verdict)
    return out


@pytest.mark.papers
@pytest.mark.parametrize("entry", ["tukey_kramer_q", "holm_sidak_step", "two_way_anova_f"])
def test_new_check_reproduces_a_printed_p(entry):
    """Tukey, Holm–Šidák and two-way ANOVA checks each reproduce at least one printed P in the corpus (02-audit, Not the paper's error; 04-formulas, Statistical formulas)."""
    vs = _verdicts(entry)
    assert any(v.startswith("consistent") for v in vs), vs[:10]
