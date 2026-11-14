"""Fig. 5b (journal_version.pdf p. 7): HCN4 expression relative to GAPDH, SM SCVI20 monolayers vs adult heart total RNA
(item F5B_hcn4_sm). Vector, log y axis (0.0001 to 1) whose line and ticks are separate paths. Eight genes, three white
bars each (SM red squares, MM blue circles, adult heart green triangles); HCN4 is the fourth gene (bars 9, 10, 11).
The legend calls the bars median ± s.d.; each group is read with its points, the bar's central value (as median) and
the upper end of its error bar."""
import _util as u


def read(fig):
    return {"groups": u.read_log_bars(fig, {
        "SM monolayer": (9, "square"),
        "Adult heart total RNA": (11, "triangle"),
    }, centre_kind="median", axis=u.split_log_vector_axis)}
