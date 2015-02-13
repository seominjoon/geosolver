from collections import namedtuple

from geosolver.text.semantics.costs.get_grounded_syntax_path_cost import get_grounded_syntax_path_cost
from geosolver.text.semantics.costs.get_ontology_path_cost import get_ontology_path_cost
from geosolver.text.semantics.states import SemanticRelation


__author__ = 'minjoon'

def get_semantic_relation_cost(semantic_relation):
    """
    Returns SyntaxOntologyCostPair

    :param semantic_relation:
    :return:
    """
    assert isinstance(semantic_relation, SemanticRelation)
    grounded_syntax = semantic_relation.grounded_syntax
    basic_ontology = semantic_relation.basic_ontology

    SyntaxOntologyCostPair = namedtuple("SyntaxOntologyCostPair", "syntax_cost ontology_cost")
    syntax_cost = get_grounded_syntax_path_cost(semantic_relation.grounded_syntax_path)
    ontology_cost = get_ontology_path_cost(semantic_relation.ontology_path)

    from_token = semantic_relation.from_grounded_token
    to_token = semantic_relation.to_grounded_token
    entity =basic_ontology.types['entity']
    if from_token.ground.type.name == 'reference' and basic_ontology.isinstance(to_token.ground.type, entity):
        if len(semantic_relation.grounded_syntax_path) > 2:
            syntax_cost += 100
    if to_token.ground.type.name == 'reference' and basic_ontology.isinstance(from_token.ground.type, entity):
        if len(semantic_relation.grounded_syntax_path) > 2:
            syntax_cost += 100

    socp = SyntaxOntologyCostPair(syntax_cost, ontology_cost)
    return socp

