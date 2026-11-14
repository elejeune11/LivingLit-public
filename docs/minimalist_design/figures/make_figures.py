"""Draw the design's figures: `uv run python docs/minimalist_design/figures/make_figures.py`.

Each figure is written as SVG and as PNG (2x) beside this file, in one style. The PNG is rendered from the SVG with
PyMuPDF, which ignores SVG markers and dash patterns, so arrowheads and dashes are drawn as plain shapes here.
All examples are made up; nothing is taken from a paper.
"""
from __future__ import annotations

import math
from html import escape
from pathlib import Path

OUT = Path(__file__).parent
FONT = "Helvetica, Arial, sans-serif"
INK, MUTED, LINE, BAND = "#1f2328", "#5d6670", "#9aa3ad", "#f2f4f6"
KIND = {  # fill, stroke, stroke width, dash
    "agent": ("#e6ecf7", "#2a5ab0", 1.6, None),
    "code": ("#ffffff", "#9aa3ad", 1.3, None),
    "library": ("#dde3ea", "#24364f", 2.2, None),
    "release": ("#f8ebe1", "#c2620c", 2.0, None),
    "file": ("#ffffff", "#6b7580", 1.3, (2, 3)),
    "outside": ("#ffffff", "#9aa3ad", 1.3, (6, 4)),
    "judgement": ("#f8f0de", "#d19a17", 1.6, None),
    "good": ("#e3f1e8", "#2f8f57", 1.6, None),
    "bad": ("#f8e3e1", "#c8402f", 1.6, None),
    "plain": ("#ffffff", "#9aa3ad", 1.3, None),
    "band": (BAND, BAND, 0, None),
}
BLUE, RED, GREEN, AMBER, NAVY = "#2a5ab0", "#c8402f", "#2f8f57", "#b07d0c", "#24364f"


class Fig:
    def __init__(self, name: str, w: int, h: int):
        self.name, self.w, self.h, self.p = name, w, h, []

    # primitives -------------------------------------------------------------------------------------------------
    def text(self, x, y, s, size=11.5, fill=INK, weight="normal", anchor="start", italic=False):
        st = " font-style='italic'" if italic else ""
        self.p.append(f"<text x='{x:.1f}' y='{y:.1f}' font-family='{FONT}' font-size='{size}' fill='{fill}' "
                      f"font-weight='{weight}' text-anchor='{anchor}'{st}>{escape(s)}</text>")

    def line(self, pts, color=LINE, width=1.4, dash=None):
        if dash is None:
            d = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f} {y:.1f}" for i, (x, y) in enumerate(pts))
            self.p.append(f"<path d='{d}' fill='none' stroke='{color}' stroke-width='{width}' stroke-linejoin='round'/>")
            return
        on, off = dash
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            L = math.hypot(x2 - x1, y2 - y1)
            t = 0.0
            while t < L:
                a, b = t / L, min(t + on, L) / L
                self.p.append(f"<line x1='{x1 + (x2 - x1) * a:.1f}' y1='{y1 + (y2 - y1) * a:.1f}' "
                              f"x2='{x1 + (x2 - x1) * b:.1f}' y2='{y1 + (y2 - y1) * b:.1f}' stroke='{color}' "
                              f"stroke-width='{width}' stroke-linecap='round'/>")
                t += on + off

    def arrow(self, pts, color=LINE, width=1.4, dash=None, head=7):
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        L = math.hypot(x2 - x1, y2 - y1) or 1
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        self.line(pts[:-1] + [(x2 - ux * head * .8, y2 - uy * head * .8)], color, width, dash)
        px, py = -uy, ux
        tri = [(x2, y2), (x2 - ux * head + px * head * .5, y2 - uy * head + py * head * .5),
               (x2 - ux * head - px * head * .5, y2 - uy * head - py * head * .5)]
        self.p.append("<path d='M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in tri) + f" Z' fill='{color}'/>")

    def rect(self, x, y, w, h, kind="plain", rx=8):
        fill, stroke, sw, dash = KIND[kind]
        if dash is None:
            s = f" stroke='{stroke}' stroke-width='{sw}'" if sw else ""
            self.p.append(f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{rx}' fill='{fill}'{s}/>")
        else:
            self.p.append(f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{rx}' fill='{fill}'/>")
            self.line([(x + rx, y), (x + w - rx, y)], stroke, sw, dash)
            self.line([(x + rx, y + h), (x + w - rx, y + h)], stroke, sw, dash)
            self.line([(x, y + rx), (x, y + h - rx)], stroke, sw, dash)
            self.line([(x + w, y + rx), (x + w, y + h - rx)], stroke, sw, dash)
            for cx, cy, a0 in ((x + rx, y + rx, 180), (x + w - rx, y + rx, 270), (x + w - rx, y + h - rx, 0),
                               (x + rx, y + h - rx, 90)):
                a, b = math.radians(a0), math.radians(a0 + 90)
                self.p.append(f"<path d='M{cx + rx * math.cos(a):.1f} {cy + rx * math.sin(a):.1f} A{rx} {rx} 0 0 1 "
                              f"{cx + rx * math.cos(b):.1f} {cy + rx * math.sin(b):.1f}' fill='none' stroke='{stroke}' "
                              f"stroke-width='{sw}'/>")

    # composites -------------------------------------------------------------------------------------------------
    def title(self, s, sub=None):
        self.text(24, 34, s, 16, INK, "bold")
        if sub:
            self.text(24, 56, sub, 11.5, MUTED, italic=True)

    def box(self, x, y, w, h, kind, title=None, lines=(), muted=(), size=11.5, title_color=None, bold=()):
        """A box with a bold title and lines; `muted` lines follow in grey, `bold` indexes lines set in bold."""
        self.rect(x, y, w, h, kind)
        yy = y + 22
        if title:
            tc = title_color or (BLUE if kind == "agent" else {"bad": RED, "good": GREEN}.get(kind, INK))
            self.text(x + 12, yy, title, 12.5, tc if kind in ("agent", "bad", "good") else INK, "bold")
            yy += 20
        for i, s in enumerate(lines):
            self.text(x + 12, yy, s, size, INK, "bold" if i in bold else "normal")
            yy += 16
        for s in muted:
            self.text(x + 12, yy, s, size, MUTED)
            yy += 16

    def band(self, x, y, w, h, label=None):
        self.rect(x, y, w, h, "band", 10)
        if label:
            self.text(x + 12, y + 20, label, 11.5, MUTED, "bold")

    def pill(self, x, y, label, kind="good", w=None):
        fill, stroke, _, _ = KIND[kind]
        w = w or 7 * len(label) + 24
        self.p.append(f"<rect x='{x}' y='{y}' width='{w}' height='24' rx='12' fill='{fill}' stroke='{stroke}' "
                      f"stroke-width='1.6'/>")
        self.text(x + w / 2, y + 16.5, label, 11.5, INK, "bold", "middle")
        return w

    def tag(self, right, y, label, color=BLUE):
        """A small outlined label whose right edge is at `right`."""
        w = 6.6 * len(label) + 20
        x = right - w
        self.p.append(f"<rect x='{x}' y='{y}' width='{w}' height='20' rx='10' fill='#ffffff' stroke='{color}' "
                      f"stroke-width='1.3'/>")
        self.text(x + w / 2, y + 14, label, 10.5, color, "bold", "middle")

    def legend(self, y, items):
        x = 24
        for kind, label in items:
            fill, stroke, sw, dash = KIND[kind]
            self.rect(x, y, 22, 14, kind, 4)
            self.text(x + 28, y + 11.5, label, 11, MUTED)
            x += 28 + 6.2 * len(label) + 22

    def dot(self, x, y, r, fill, stroke=None, sw=0):
        s = f" stroke='{stroke}' stroke-width='{sw}'" if stroke else ""
        self.p.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{r}' fill='{fill}'{s}/>")

    def save(self):
        svg = (f"<svg xmlns='http://www.w3.org/2000/svg' width='{self.w}' height='{self.h}' "
               f"viewBox='0 0 {self.w} {self.h}'><rect width='{self.w}' height='{self.h}' fill='#ffffff'/>"
               + "".join(self.p) + "</svg>\n")
        (OUT / f"{self.name}.svg").write_text(svg, encoding="utf-8")
        import pymupdf
        with pymupdf.open(stream=svg.encode("utf-8"), filetype="svg") as doc:
            doc[0].get_pixmap(dpi=144).save(str(OUT / f"{self.name}.png"))


# ---------------------------------------------------------------------------------------------------------------------
def fig1():
    f = Fig("fig1-whole-plan", 900, 800)
    f.title("The whole plan: agents write, code decides, two libraries grow and are used")
    f.legend(50, [("agent", "LLM agent"), ("code", "code"), ("library", "field library"), ("release", "release"),
                  ("file", "files"), ("outside", "outside LivingLit")])
    f.box(24, 82, 616, 50, "file", "Sources", muted=["papers, supplements, released data; one at a time, never committed"])
    f.arrow([(332, 132), (332, 152)])
    # agents
    f.band(24, 152, 616, 168, "Per source: agents write, nothing else")
    xs = [36, 186, 336, 486]
    agents = [("Record reader", ["evidence items,", "values as printed,", "claims judged"]),
              ("Figure reader", ["writes code that", "reads each figure;", "a first look skips", "plots without points"]),
              ("Formula agent", ["writes derivations;", "reports model", "assumptions;", "proposes formulas"]),
              ("Vocabulary agent", ["maps context,", "contrasts, measures", "to terms; proposes", "terms, synonyms"])]
    for x, (t, ls) in zip(xs, agents):
        f.box(x, 182, 142, 124, "agent", t, ls, size=11)
    # code: each box under the agents whose output it decides on
    f.band(24, 352, 616, 150, "Code decides")
    f.box(36, 382, 292, 108, "code", "Gates", ["anchors found, values as printed, groups and", "n consistent; figure code reruns to the",
                                             "same values; synonyms found in the source"], size=11)
    f.box(336, 382, 142, 108, "code", "Checks", ["statistics, readings,", "formulas on chains,", "status and depth"], size=11)
    f.box(486, 382, 142, 108, "code", "Matching", ["terms under", "standing keys:", "contrasts,", "comparisons"], size=11)
    for x in (150, 257, 407, 557):
        f.arrow([(x, 306), (x, 380)])
    # flags back to the record reader
    f.arrow([(36, 440), (28, 440), (28, 244), (34, 244)], RED, 1.6)
    f.text(40, 338, "flags: read again", 11, RED)
    # libraries
    f.band(660, 82, 220, 420, None)
    f.text(672, 104, "Field libraries: fields/<field>/", 11.5, MUTED, "bold")
    f.text(672, 120, "append-only logs, rebuilt by code", 11, MUTED)
    f.box(672, 136, 196, 80, "code", "Edit checks", ["synonym found in a source;", "one parent; formulas", "cited or proved"], size=11)
    f.box(672, 250, 196, 110, "library", "Controlled vocabulary", ["terms, synonyms, one", "parent, qualifiers,",
                                                                   "groups, ontology anchors,", "standing keys"], size=11)
    f.box(672, 384, 196, 96, "library", "Formula library", ["definitions, models,", "bounds, derived", "formulas with proofs"], size=11)
    # proposals from the vocabulary and formula agents go through the edit checks
    f.line([(557, 182), (557, 168), (650, 168)], NAVY, 1.4)
    f.line([(407, 182), (407, 168), (557, 168)], NAVY, 1.4)
    f.arrow([(650, 168), (650, 176), (670, 176)], NAVY)
    f.text(566, 162, "proposes", 10.5, NAVY)
    f.arrow([(770, 216), (770, 248)], NAVY)
    f.arrow([(868, 200), (878, 200), (878, 430), (870, 430)], NAVY)
    # the libraries are used by matching and checks
    f.arrow([(672, 330), (650, 330), (650, 436), (630, 436)], NAVY)
    f.arrow([(672, 470), (660, 470), (660, 496), (407, 496), (407, 492)], NAVY)
    # records, release, outside
    f.arrow([(332, 502), (332, 528)])
    f.box(24, 530, 616, 56, "file", "records/<paper>/", muted=["record, figure code and readings, terms, derivations; audit generated by code"])
    f.arrow([(332, 586), (332, 614)])
    f.arrow([(770, 502), (770, 614)])
    f.box(24, 616, 856, 70, "release", "Release (tagged): LivingLit's boundary",
          ["documented tables of records, mappings, derivations, checks and comparisons, with the library versions used;",
           "one page, the explorer: the release by question, with a knowledge graph, down to each result"], size=11)
    f.arrow([(452, 686), (452, 712)])
    f.box(24, 714, 856, 60, "outside", "Outside LivingLit",
          muted=["people and agents query a release, synthesize, test hypotheses and cite rows; nothing they write enters a release"])
    f.save()


def fig2():
    f = Fig("fig2-one-source", 900, 440)
    f.title("One source audited: the printed P does not follow from t(8) = 2.3", "made-up example")
    f.text(24, 88, "Source", 11.5, MUTED)
    f.text(250, 88, "Record and mapping: written by agents", 11.5, MUTED)
    f.text(630, 88, "Checked by code; one reader judgement", 11.5, MUTED)
    f.rect(24, 98, 200, 322, "plain")
    f.text(36, 122, "Paper A", 12.5, INK, "bold")
    for i, (t, s) in enumerate([("text", "abstract, methods"), ("figures", "read by a reader's code"),
                                ("source data", "not released")]):
        f.box(36, 136 + i * 92, 176, 72, "plain", t, muted=[s])
    f.arrow([(224, 256), (246, 256)])
    rows = [(98, 132, "Evidence item E3", ["sarcomere length, unpaced vs paced", "1.71 ± 0.05 vs 1.89 ± 0.06 µm (SD)",
                                           "n = 5 tissues per group, one batch", "t(8) = 2.3, p < 0.01; origin: stated"],
             ["finding: sarcomeres longer when paced"]),
            (250, 80, "Stated claim C1, abstract", ["“pacing matured the tissues”"], ["rests on E3"]),
            (350, 70, "Mapping", ["contrast: electrical ramp vs none (assigned)", "platform → anchored EHT (matched)"], [])]
    for y, h, t, ls, mu in rows:
        f.box(250, y, 350, h, "agent", t, ls, mu)
        f.arrow([(600, y + h / 2), (626, y + h / 2)])
    f.box(630, 98, 246, 132, "code", "Statistic to P", ["t(8) = 2.3 gives P = 0.05,", "not < 0.01"])
    f.text(642, 186, "status: inconsistent", 11.5, RED, "bold")
    f.text(642, 204, "depth: printed only", 11.5, MUTED)
    f.box(630, 250, 246, 80, "judgement", "Claim judgement", ["strength, scope, replication:", "overstated"], bold=(1,))
    f.box(630, 350, 246, 70, "code", "Mapping checked", ["terms exist, anchored;", "no value mapped by inference"])
    f.save()


def fig3():
    f = Fig("fig3-reading-figures", 900, 536)
    f.title("Reading values from figures",
            "made-up example · a reader writes code for each figure; the code is kept with the record and every audit reruns it")
    # two small plots: the panel and the overlay
    def plot(ox, oy, label, overlay):
        f.text(ox + 70, oy - 12, label, 11.5, MUTED, "bold", "middle")
        f.line([(ox, oy), (ox, oy + 130), (ox + 140, oy + 130)], INK, 1.2)
        for v in (0, 10, 20, 30):
            y = oy + 130 - v * 4.2
            f.line([(ox - 4, y), (ox, y)], RED if overlay else INK, 2 if overlay else 1.2)
            f.text(ox - 8, y + 4, str(v), 10, INK, anchor="end")
        f.text(ox + 40, oy + 148, "control", 10.5, INK, anchor="middle")
        f.text(ox + 100, oy + 148, "mutant", 10.5, INK, anchor="middle")
        a = [14, 17, 19, 21, 22, 22, 24, 25, 26, 27]
        b = [9, 11, 13, 14, 15, 16, 17, 19, 14]
        for xs, vals, col in ((ox + 40, a, "#4a7fc1"), (ox + 100, b, "#d4553f")):
            for i, v in enumerate(vals):
                x, y = xs - 12 + (i % 5) * 6, oy + 130 - v * 4.2
                if overlay:
                    f.dot(x, y, 5, "none", "#e3a21a", 1.6)
                f.dot(x, y, 3, col)
            m = sum(vals) / len(vals)
            f.line([(xs - 16, oy + 130 - m * 4.2), (xs + 16, oy + 130 - m * 4.2)], INK, 1.6)
            f.line([(xs, oy + 130 - (m - 2) * 4.2), (xs, oy + 130 - (m + 2) * 4.2)], INK, 1.2)
    plot(52, 96, "a figure panel", False)
    plot(52, 318, "the overlay, kept with the record", True)
    f.box(240, 80, 312, 124, "code", "Vector figure: the code uses the PDF's objects",
          ["every marker, bar and cap is a separate object:", "exact coordinates, even when markers overlap;",
           "tick marks and their labels calibrate the axis", "counts: exact", "uncertainty (measured): ≤ 0.5 pt"],
          size=11, bold=(3, 4))
    f.box(566, 80, 310, 124, "code", "Raster figure: the code uses the image",
          ["axis and ticks found in the image; the reader", "transcribes tick labels, code fits even spacing;",
           "markers found by colour, error bars removed", "counts: only if every marker stands alone",
           "uncertainty (measured, 300 ppi): ≤ 0.6 px"], size=11, bold=(3, 4))
    f.box(240, 218, 312, 70, "agent", "The reader's code, kept with the record",
          ["figures/fig2c.py: each point with an interval,", "its page position, and whether it may be counted"], size=11)
    f.box(566, 218, 310, 70, "code", "Calibration sets the uncertainty",
          ["figures with released data are read blind, then", "compared; the worst error per method is the floor"], size=11)
    f.text(240, 316, "What a reading enables", 12.5, INK, "bold")
    cards = [("Count n", ["plotted: 10 and 9", "legend: 12 and 11"], "inconsistent", "bad", "n differs from the legend"),
             ("Recompute P as an interval", ["printed: P = 0.001", "from the points, ±0.5 pt:", "P = 0.0002–0.0004"],
              "inconsistent", "bad", "printed P outside the interval"),
             ("n implied by the error bar", ["(SD of points ÷ SEM bar)²", "= 10.1 and 8.9", "matches the plotted points"],
              "consistent", "good", "bar computed from what is plotted")]
    for i, (t, ls, st, k, why) in enumerate(cards):
        x = 240 + i * 214
        f.box(x, 328, 204, 140, "code", t, ls, size=11)
        f.pill(x + 12, 412, st, k)
        f.text(x + 12, 454, why, 10.5, MUTED, italic=True)
    f.text(240, 500, "Every value read from a figure is labelled “read”, with its method and uncertainty. A check on read values",
           10.5, MUTED)
    f.text(240, 516, "passes as “consistent within reading” and fails only when the difference is larger than the reading explains.",
           10.5, MUTED)
    f.save()


def fig4():
    f = Fig("fig4-one-parent", 900, 400)
    f.title("One parent per term",
            "a second parent is a sign that a field mixes two dimensions · made-up excerpt of the substrate field")
    for ox, head in ((24, "Proposed: a tree, with qualifiers and groups"), (462, "Not proposed: a second parent")):
        f.band(ox, 72, 414, 316)
        f.text(ox + 12, 94, head, 12.5, INK, "bold")

    def node(cx, cy, label, kind="plain", color=INK):
        w = 7 * len(label) + 28
        f.rect(cx - w / 2, cy - 13, w, 26, kind, 6)
        f.text(cx, cy + 4.5, label, 11.5, color, "bold" if kind != "plain" else "normal", "middle")
    # left tree; the group outline is drawn first so the nodes sit on top
    G = (216, 226, 216, 80)
    gx, gy, gw, gh = G
    for p0, p1 in (((gx, gy), (gx + gw, gy)), ((gx, gy + gh), (gx + gw, gy + gh)), ((gx, gy), (gx, gy + gh)),
                   ((gx + gw, gy), (gx + gw, gy + gh))):
        f.line([p0, p1], AMBER, 1.4, (5, 4))
    f.line([(231, 136), (120, 176)], MUTED); f.line([(231, 136), (312, 176)], MUTED)
    f.line([(120, 202), (70, 236)], MUTED); f.line([(120, 202), (170, 236)], MUTED)
    f.line([(312, 202), (262, 236)], MUTED); f.line([(312, 202), (356, 236)], MUTED)
    node(231, 124, "substrate", "code")
    node(120, 189, "natural matrix", "agent", BLUE)
    node(312, 189, "synthetic material", "agent", BLUE)
    node(70, 249, "fibrin"); node(170, 249, "Matrigel"); node(262, 249, "PDMS"); node(358, 249, "polyacrylamide")
    f.text(262, 290, "stiffness “8 kPa”", 10.5, MUTED, anchor="middle", italic=True)
    f.text(362, 290, "stiffness “4 kPa”", 10.5, MUTED, anchor="middle", italic=True)
    f.text(324, 322, "group “soft substrate”: stiffness < 100 kPa", 10.5, AMBER, anchor="middle", italic=True)
    for i, s in enumerate(["PDMS has one ancestor at each level, so “substrate@1” has one answer.",
                           "Stiffness is a qualifier, compared at printed precision. A group is a named",
                           "rule over terms and qualifiers, usable by keys; it does not change ancestors."]):
        f.text(36, 344 + i * 15, s, 10.5, MUTED)
    # right tree
    f.line([(669, 136), (580, 176)], MUTED); f.line([(669, 136), (770, 176)], MUTED)
    f.line([(580, 202), (580, 236)], MUTED); f.line([(580, 202), (770, 236)], MUTED)
    f.line([(770, 202), (580, 236)], RED, 1.4, (5, 4)); f.line([(770, 202), (770, 236)], RED, 1.4, (5, 4))
    node(669, 124, "substrate", "code")
    node(580, 189, "synthetic material", "agent", BLUE)
    node(770, 189, "soft substrate", "bad", RED)
    node(580, 249, "PDMS"); node(770, 249, "polyacrylamide")
    f.text(669, 290, "but stiff PDMS (MPa) is not soft: the parent depends on a number", 10.5, RED, anchor="middle", italic=True)
    for i, s in enumerate(["“Same at level 1” has two answers for PDMS, and every move or split",
                           "has to be replayed along every path. The second parent is really a",
                           "second dimension (stiffness): a qualifier or a group instead."]):
        f.text(474, 344 + i * 15, s, 10.5, MUTED)
    f.save()


def fig5():
    f = Fig("fig5-contrasts", 900, 660)
    f.title("The reader writes groups and tests; code computes the contrasts",
            "made-up unit with a 2 × 2 design, and a matching pair from a second paper")
    f.rect(24, 72, 520, 290, "plain")
    f.text(36, 96, "Paper A · unit F3 · four groups", 12.5, INK, "bold")
    f.tag(532, 82, "reader writes")
    f.text(220, 120, "no pacing", 11, MUTED, anchor="middle", italic=True)
    f.text(420, 120, "ramp pacing", 11, MUTED, anchor="middle", italic=True)
    f.text(40, 176, "low Ca", 11, MUTED, italic=True)
    f.text(40, 290, "high Ca", 11, MUTED, italic=True)
    groups = [(140, 130, "LC-NP", "“low Ca, unpaced”", "calcium: 0.6 mM", "pacing: none"),
              (340, 130, "LC-RP", "“low Ca, ramp-paced”", "calcium: 0.6 mM", "pacing: electrical_ramp"),
              (140, 244, "HC-NP", "“high Ca, unpaced”", "calcium: 1.8 mM", "pacing: none"),
              (340, 244, "HC-RP", "“high Ca, ramp-paced”", "calcium: 1.8 mM", "pacing: electrical_ramp")]
    for x, y, t, q, a, b in groups:
        f.box(x, y, 160, 82, "plain", t, [q], [a, b], size=10.5)
    f.arrow([(300, 285), (338, 285)], BLUE, 2)
    f.text(319, 278, "E1", 11, BLUE, "bold", "middle")
    f.arrow([(300, 214), (340, 242)], RED, 1.6, (4, 3))
    f.text(306, 238, "E2", 11, RED, "bold", "end")
    f.line([(144, 334), (144, 340), (296, 340), (296, 334)], GREEN, 1.6)
    f.line([(344, 334), (344, 340), (496, 340), (496, 334)], GREEN, 1.6)
    f.text(220, 355, "E3 reference", 11, GREEN, "bold", "middle")
    f.text(420, 355, "E3 condition", 11, GREEN, "bold", "middle")
    f.rect(560, 72, 316, 290, "plain")
    f.text(572, 96, "Paper A · items in F3", 12.5, INK, "bold")
    f.tag(864, 82, "reader writes")
    items = [(BLUE, "E1", ["compares: [HC-NP, HC-RP]"], "a t-test"),
             (RED, "E2", ["compares: [LC-NP, HC-RP]"], "one post-hoc pair"),
             (GREEN, "E3", ["test_of: main effect", "condition: [LC-RP, HC-RP]", "reference: [LC-NP, HC-NP]"], None)]
    y = 124
    for col, k, ls, sub in items:
        f.text(572, y, k, 11.5, col, "bold")
        for s in ls:
            f.text(598, y, s, 11)
            y += 16
        if sub:
            f.text(598, y, sub, 10.5, MUTED, italic=True)
            y += 16
        y += 8
    f.text(572, y + 6, "measure: sarcomere_length, all three", 11, MUTED)
    f.text(572, y + 30, "No item says what varies: the reader names", 10.5, MUTED, italic=True)
    f.text(572, y + 45, "groups, code finds the difference.", 10.5, MUTED, italic=True)
    f.arrow([(284, 362), (284, 384)], MUTED)
    f.band(24, 386, 852, 112, "Code compares each item's groups on their mapped terms and quantities")
    f.tag(864, 394, "code computes, never stored", MUTED)
    res = [("good", "E1 · contrast", ["one field differs:", "pacing, ramp vs none"]),
           ("bad", "E2 · confound", ["calcium and pacing differ;", "flagged by code"]),
           ("good", "E3 · main effect of pacing", ["sides differ in pacing,", "balanced on calcium"]),
           ("plain", "F3 · factorial", ["calcium × pacing,", "all four combinations"])]
    for i, (k, t, ls) in enumerate(res):
        f.box(36 + i * 210, 418, 200, 68, k, t, ls, size=11)
    f.arrow([(136, 486), (136, 510), (640, 510), (640, 530)], GREEN, 1.6)
    f.box(24, 532, 300, 112, "plain", "Paper B · item E5", ["compares: [paced, unpaced]"],
          ["paced: pacing electrical_ramp", "unpaced: pacing none", "code: contrast on pacing, ramp vs none"], size=11)
    f.tag(312, 540, "reader writes")
    f.arrow([(324, 588), (352, 588)], GREEN, 1.6)
    f.box(354, 532, 522, 112, "good", "Same contrast, same measure → directions compared",
          ["A · E1 and B · E5: pacing ramp vs none, sarcomere_length,", "matched under the standing key for sarcomere length",
           "(direction part); A · E2 is left out as a confound"], ["no reader or agent linked the two papers"], size=11)
    f.save()


def fig6():
    f = Fig("fig6-two-post-formula", 900, 400)
    f.title("A wrong derivation is caught from the methods text alone", "made-up example")
    f.text(24, 88, "Given: two models, cited", 11.5, MUTED)
    f.text(330, 88, "Derived formula: proved by code", 11.5, MUTED)
    f.text(640, 88, "The paper: anchored", 11.5, MUTED)
    f.box(24, 98, 250, 62, "code", "Hooke's law (model)", ["F = k·δ, for each post"])
    f.box(24, 178, 250, 62, "code", "Static equilibrium (model)", ["F1 = F2 = T, tissue at rest"])
    f.box(330, 112, 260, 100, "code", "two_post_force_balance", ["T = k·d1 = k·d2", "so k·(d1 + d2) = 2T"],
          ["proved with SymPy, tests pass"])
    f.arrow([(274, 129), (300, 129), (300, 150), (328, 150)])
    f.arrow([(274, 209), (300, 209), (300, 174), (328, 174)])
    f.box(640, 98, 236, 82, "code", "Paper's methods", ["F = k·(d1 + d2)"], ["written with its quote"])
    f.box(640, 200, 236, 62, "code", "Symbolic check", ["the paper's F = 2T"])
    f.arrow([(758, 180), (758, 198)])
    f.arrow([(590, 162), (614, 162), (614, 231), (638, 231)])
    f.arrow([(758, 262), (758, 290)])
    f.box(24, 292, 852, 92, "bad", "Flag: inconsistent with two_post_force_balance (derived) ← Hooke + equilibrium",
          ["Within the paper: a constant factor of 2, so t, P and direction are unchanged: conclusion unaffected.",
           "Absolute values: rebuilt force = printed force / 2, labelled derived by LivingLit; the printed value is kept.",
           "Claims against adult values, and comparisons with other papers, use the rebuilt value."], size=11)
    f.save()


def fig7():
    f = Fig("fig7-chain", 900, 440)
    f.title("One reading checks every link of the chain",
            "made-up paper: deflection read from a figure, force and stress printed with P values")
    links = [("Post deflection", ["read from a figure by code"], ["8 tissues per group"]),
             ("Force", ["via two_post_force_balance"], ["printed: P = 0.02"]),
             ("Stress", ["via F / A"], ["printed: mean ± SD, P = 0.04"])]
    for i, (t, ls, mu) in enumerate(links):
        x = 24 + i * 292
        f.box(x, 76, 268, 80, "code", t, ls, mu)
        f.line([(x + 134, 156), (x + 134, 182)], LINE)
        if i < 2:
            f.arrow([(x + 268, 116), (x + 290, 116)])
    f.box(24, 184, 852, 74, "code", "Carried along by code",
          ["Read deflections × k give force values; ÷ A give stress values, labelled derived by LivingLit.",
           "Every printed mean, spread and P on the chain is checked against them, not only the panel that was read."],
          title_color=INK)
    f.arrow([(450, 258), (450, 280)])
    f.rect(24, 282, 852, 142, "plain")
    f.text(36, 306, "Formulas across the chain", 12.5, INK, "bold")
    f.text(560, 306, "Result", 12.5, INK, "bold")
    f.line([(36, 316), (864, 316)], "#dfe3e7", 1)
    rows = [("Constant scaling: force and stress share one P if A is constant", "0.02 vs 0.04: inconsistent if A constant"),
            ("Same n: the n of force carries to stress", "8 = 8: consistent"),
            ("A not stated as one constant or per tissue", "both run as labelled alternatives"),
            ("An input item found inconsistent upstream", "a separate flag; status unchanged")]
    for i, (a, b) in enumerate(rows):
        f.text(36, 338 + i * 22, a, 11.5)
        f.text(560, 338 + i * 22, b, 11.5, INK, "bold" if i == 0 else "normal")
    f.save()


def fig8():
    f = Fig("fig8-standing-key", 900, 420)
    f.title("One standing key, four pairs: code names why each is or is not comparable",
            "contractile stress, value part of its key; made-up items from five papers")
    f.rect(24, 74, 270, 330, "plain")
    f.text(36, 98, "Standing key: stress", 12.5, INK, "bold")
    f.text(36, 116, "in the vocabulary, versioned", 11, MUTED)
    f.text(36, 146, "must match", 11.5, INK, "bold")
    for i, s in enumerate(["platform at level 2", "temperature", "preparation", "derivation (same formula)"]):
        f.text(36, 164 + i * 16, s, 11.5)
    f.text(36, 244, "may vary", 11.5, INK, "bold")
    f.text(36, 262, "cell line, substrate", 11.5)
    for i, s in enumerate(["When a pair is not comparable,", "code coarsens each field one level,", "then drops it, and reports",
                           "where the verdict changes."]):
        f.text(36, 300 + i * 16, s, 11, MUTED)
    pairs = [("A · E7 vs B · E4", ["12 ± 2 vs 14 ± 3 mN/mm²; every field matches"], "agree", "good"),
             ("A · E7 vs C · E2", ["temperature: 37 °C vs room temperature"], "not comparable", "bad"),
             ("A · E7 vs D · E5", ["platform: anchored EHT vs spheroid;", "at level 1 both 3D: then they differ"],
              "differ if relaxed", "judgement"),
             ("A · E7 vs E · E1", ["E summed both posts (formula flag);", "rebuilt value, labelled derived"],
              "agree, rebuilt", "agent")]
    for i, (t, ls, v, k) in enumerate(pairs):
        y = 74 + i * 84
        f.box(314, y, 562, 72, "plain", t, muted=ls, size=11)
        f.pill(740, y + 24, v, k, 124)
    f.save()


if __name__ == "__main__":
    for fn in (fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8):
        fn()
    print("figures written to", OUT)
