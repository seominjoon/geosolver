from collections import namedtuple
from geosolver.text.semantics.get_ontology_path_cost import get_ontology_path_cost
from geosolver.text.semantics.get_syntax_path_cost import get_syntax_path_cost
from geosolver.text.semantics.states import SemanticRelation

__author__ = 'minjoon'

def get_semantic_relation_cost(semantic_relation):
    """
    Returns SyntaxOntologyCostPair

    :param semantic_relation:
    :return:
    """
    assert isinstance(semantic_relation, SemanticRelation)
    syntax = semantic_relation.syntax
    basic_ontology = semantic_relation.basic_ontology

    SyntaxOntologyCostPair = namedtuple("SyntaxOntologyCostPair", "syntax_cost ontology_cost")
    syntax_cost = get_syntax_path_cost(syntax, semantic_relation.syntax_path)
    ontology_cost = get_ontology_path_cost(basic_ontology, semantic_relation.ontology_path)
    socp = SyntaxOntologyCostPair(syntax_cost, ontology_cost)
    return socp

