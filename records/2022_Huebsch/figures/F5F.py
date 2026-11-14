"""Fig. 5f (journal_version.pdf p. 7): expression relative to GAPDH of six transcripts in SCVI20 MPS, SM vs MM.
Only MYL2 (item F5F_MYL2) is returned: it is the one item group of this panel that needs figure values. Vector, log
y axis (0.0001 to 10). Six genes, two outline bars each (SM red squares, MM blue circles), genes left to right KCND2,
SLN, CACNB1, MYH7, MYL2, KCNJ2; groups are found by their 12 error bars, as in Fig. 5e. The legend calls the error bars
mean ± s.e.m.; each group is read with its points, the bar's central value (as mean) and the upper end of its error bar.
The SLN SM error bar reaches the x axis and is drawn as separate paths, so it is not one of the error bars found and
is left out of the labels (11 bars, left to right)."""
import _util as u

GENES = ["KCND2", "SLN", "CACNB1", "MYH7", "MYL2", "KCNJ2"]
READ = {"MYL2"}


def read(fig):
    labels = [lab for g in GENES for lab in ((f"{g} SM MPS", "square"), (f"{g} MM MPS", "circle"))
              if lab[0] != "SLN SM MPS"]
    groups = u.read_log_errorbar_groups(fig, labels)
    return {"groups": {k: v for k, v in groups.items() if k.split()[0] in READ}}
