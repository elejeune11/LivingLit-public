from livinglit.ontology import parse_obo, parse_cellosaurus, Ontologies, build_index

OBO = """format-version: 1.2
data-version: chebi/999

[Term]
id: CHEBI:1
name: thing one
synonym: "T1" EXACT []
is_a: CHEBI:2 ! parent

[Term]
id: CHEBI:2
name: parent

[Term]
id: CHEBI:3
name: gone
is_obsolete: true
"""
CELLO = """ Version: 99.0
ID   LINE-1
AC   CVCL_0001
SY   L1; Line one
OX   NCBI_TaxID=9606; ! Homo sapiens (Human)
//
ID   MOUSE
AC   CVCL_0002
OX   NCBI_TaxID=10090; ! Mus musculus
//
"""


def test_obo_parse_and_checks(tmp_path):
    """Adopted ids are checked against a pinned release: unknown and obsolete ids fail; ancestors follow is_a (03-vocabulary, Adopted ontologies; 08 decision 18)."""
    (tmp_path / "chebi_core.obo.gz").write_bytes(__import__("gzip").compress(OBO.encode()))
    (tmp_path / "cellosaurus.txt").write_text(CELLO)
    build_index("chebi", tmp_path)
    build_index("cellosaurus", tmp_path)
    o = Ontologies(tmp_path)
    assert o.check("CHEBI:1")["label"] == "thing one"
    assert o.check("CHEBI:3")["obsolete"] is True
    assert o.check("CHEBI:9") is None
    assert o.ancestors("CHEBI:1") == {"CHEBI:2"}
    assert o.search("chebi", "t1")[0]["id"] == "CHEBI:1"
    assert o.check("CVCL_0001")["label"] == "LINE-1"
    assert o.check("CVCL_0002") is None  # only human lines are indexed


def test_ncbitaxon_is_pinned_and_species_xrefs_are_checked(tmp_path):
    """NCBITaxon (taxslim) is a pinned release; an own term's NCBITaxon xref must exist and not be obsolete in it (08-trials-and-decisions, decision 34; 03-vocabulary, Adopted ontologies and our own terms)."""
    from livinglit.ontology import FILES, PREFIX
    from livinglit.vocab import Vocabulary, FieldDecl, check_edits
    assert FILES["ncbitaxon"] == "taxslim.obo" and PREFIX["NCBITaxon"] == "ncbitaxon"
    (tmp_path / "taxslim.obo").write_text("format-version: 1.2\ndata-version: ncbitaxon/9\n\n[Term]\nid: NCBITaxon:9606\n"
                                          "name: Homo sapiens\n\n[Term]\nid: NCBITaxon:1\nname: old\nis_obsolete: true\n")
    onto = Ontologies(tmp_path)
    assert onto.check("NCBITaxon:9606")["label"] == "Homo sapiens"
    v = Vocabulary({"species": FieldDecl("species", "terms")})
    def edit(x):
        return [{"add_term": {"field": "species", "id": "species:human", "label": "human", "definition": "d",
                              "scope": "s", "xref": [x]}}]
    assert not [p for p in check_edits(v, edit("NCBITaxon:9606"), found=lambda q: True, ontology=onto, paper="P") if "xref" in p]
    assert any("xref" in p for p in check_edits(v, edit("NCBITaxon:7"), found=lambda q: True, ontology=onto, paper="P"))
    assert any("xref" in p for p in check_edits(v, edit("NCBITaxon:1"), found=lambda q: True, ontology=onto, paper="P"))


def test_every_adopted_id_and_xref_is_rechecked_against_the_pinned_releases(tmp_path):
    """Re-checking the vocabulary against the pinned ontology releases lists every adopted id or own-term xref that is missing or obsolete in them, so a new pin cannot silently break terms (03-vocabulary, Adopted ontologies and our own terms; 08-trials-and-decisions, decision 18)."""
    from livinglit.vocab import Vocabulary, FieldDecl, Term, recheck_ontology
    (tmp_path / "chebi_core.obo.gz").write_bytes(__import__("gzip").compress(OBO.encode()))
    build_index("chebi", tmp_path)
    (tmp_path / "taxslim.obo").write_text("format-version: 1.2\ndata-version: ncbitaxon/9\n\n[Term]\nid: NCBITaxon:9606\n"
                                          "name: Homo sapiens\n")
    onto = Ontologies(tmp_path)
    v = Vocabulary({"drug": FieldDecl("drug", "adopted"), "species": FieldDecl("species", "terms")})
    v.terms = {"CHEBI:1": Term("CHEBI:1", ["drug"], "thing one", source="chebi"),
               "CHEBI:3": Term("CHEBI:3", ["drug"], "old", source="chebi"),
               "CHEBI:9": Term("CHEBI:9", ["drug"], "gone", source="chebi"),
               "species:human": Term("species:human", ["species"], "human", xref=["NCBITaxon:9606"]),
               "species:x": Term("species:x", ["species"], "x", xref=["NCBITaxon:7"])}
    probs = recheck_ontology(v, onto)
    assert any("CHEBI:3" in p and "obsolete" in p for p in probs)
    assert any("CHEBI:9" in p and "not in" in p for p in probs)
    assert any("species:x" in p and "NCBITaxon:7" in p for p in probs)
    assert not any("CHEBI:1" in p or "species:human" in p for p in probs)
