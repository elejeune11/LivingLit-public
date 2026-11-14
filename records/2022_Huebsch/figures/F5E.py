"""Fig. 5e (journal_version.pdf p. 7): expression relative to GAPDH of eight transcripts in WTC MPS, SM vs MM
(items F5E_SLN ... F5E_ALDH1A1). Vector, log y axis (0.0001 to 10). Eight genes, two white bars each (SM red squares,
MM blue circles), genes left to right SLN, HCN2, CACNB2, KCNIP2, MYH7, MYL2, KCND2, ALDH1A1. The bars are outlines,
so groups are found by their 16 error bars. The legend calls the error bars mean ± s.e.m.; each group is read with its
points, the bar's central value (as mean) and the upper end of its error bar (upper end of the s.e.m.)."""
import _util as u

GENES = ["SLN", "HCN2", "CACNB2", "KCNIP2", "MYH7", "MYL2", "KCND2", "ALDH1A1"]


def read(fig):
    labels = [lab for g in GENES for lab in ((f"{g} SM MPS", "square"), (f"{g} MM MPS", "circle"))]
    return {"groups": u.read_log_errorbar_groups(fig, labels)}
