"""Fig. 5a (journal_version.pdf p. 7): CACNB2 expression relative to GAPDH in WTC monolayers, SM vs MM (item F5A_cacnb2_mm).
Vector, log y axis (0.0001 to 1). Eight genes, three white bars each (SM red squares, MM blue circles, adult heart green
triangles); CACNB2 is the second gene (bars 3, 4, 5). The legend calls the bars median ± s.d.; each group is read with
its points, the bar's central value (as median) and the upper end of its error bar."""
import _util as u


def read(fig):
    return {"groups": u.read_log_bars(fig, {
        "SM monolayer": (3, "square"),
        "MM monolayer": (4, "circle"),
    }, centre_kind="median")}
